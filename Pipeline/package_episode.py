#!/usr/bin/env python3
"""MP4 → platform upload kit — SEO, chapters, end-screen, thumbnail hand-off.

Usage:
    python package_episode.py <production_dir_or_manifest.json>
    python package_episode.py <script.json> --mp4 path/to/final.mp4

Called automatically when render_longform.py finishes with --package.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

WORKSPACE = Path(__file__).resolve().parents[2]
DAVID_SCRIPTS = WORKSPACE / "DAVID" / "scripts"

FORMAT_PROFILES: dict[str, dict[str, Any]] = {
    "narrative-short-film": {
        "title_suffix": "| Cinematic Short",
        "tag_pool": [
            "short film", "cinematic", "thriller", "synthetic media",
            "AI film", "indie film", "drama", "suspense",
        ],
        "category": "Film & Animation",
        "playlist": "STUDIO Movies Lane",
    },
    "documentary-host": {
        "title_suffix": "| Documentary",
        "tag_pool": [
            "documentary", "history", "linguistics", "education",
            "dead languages", "synthetic host", "archive",
        ],
        "category": "Education",
        "playlist": "DAVID · The Archive",
    },
    "explainer-ad": {
        "title_suffix": "| Product Explainer",
        "tag_pool": [
            "explainer", "product demo", "SaaS", "app", "advertisement",
            "synthetic talent", "brand video",
        ],
        "category": "Science & Technology",
        "playlist": "STUDIO Editorial",
    },
    "science-explainer": {
        "title_suffix": "| Science Explainer",
        "tag_pool": [
            "science", "physics", "explainer", "education", "phenomenon",
            "visualization", "STEM", "synthetic media",
        ],
        "category": "Science & Technology",
        "playlist": "STUDIO Science",
    },
    "conversational-companion": {
        "title_suffix": "| Companion",
        "tag_pool": [
            "companion", "conversational AI", "synthetic talent", "PG",
        ],
        "category": "People & Blogs",
        "playlist": "STUDIO Companion",
    },
}

ROLE_CHAPTER_LABELS: dict[str, str] = {
    "b_roll": "Establishing",
    "host": "Host",
    "character": "Scene",
    "companion": "Check-in",
    "presenter": "Presenter",
    "card": "Card",
}


def _ffmpeg_exe() -> str:
    try:
        import imageio_ffmpeg

        return imageio_ffmpeg.get_ffmpeg_exe()
    except ImportError:
        return "ffmpeg"


def _probe_duration(video: Path) -> float:
    ff = _ffmpeg_exe()
    r = subprocess.run(
        [ff, "-i", str(video)],
        capture_output=True,
        text=True,
    )
    for line in r.stderr.splitlines():
        if "Duration:" in line:
            ts = line.split("Duration:")[1].split(",")[0].strip()
            h, m, s = ts.split(":")
            return int(h) * 3600 + int(m) * 60 + float(s)
    raise RuntimeError(f"cannot probe duration: {video}")


def _extract_frame(video: Path, at_s: float, out_jpg: Path) -> Path:
    ff = _ffmpeg_exe()
    out_jpg.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            ff, "-y", "-ss", f"{at_s:.3f}", "-i", str(video),
            "-frames:v", "1", "-q:v", "2", "-update", "1", str(out_jpg),
        ],
        check=True,
        capture_output=True,
    )
    return out_jpg


def _slug_to_title(slug: str) -> str:
    return re.sub(r"\s+", " ", slug.replace("_", " ").replace("-", " ").strip()).title()


def _shot_id_label(shot_id: str) -> str:
    parts = shot_id.split("_", 1)
    if len(parts) == 2 and parts[0].isdigit():
        return parts[1].replace("_", " ").title()
    return shot_id.replace("_", " ").title()


def chapter_label(shot: dict[str, Any]) -> str:
    speech = (shot.get("speech_text") or "").strip()
    if speech and len(speech) <= 48:
        return speech
    custom = shot.get("chapter_title")
    if custom:
        return str(custom)
    role = shot.get("role", "host")
    base = ROLE_CHAPTER_LABELS.get(role, "Beat")
    detail = _shot_id_label(shot["id"])
    if role in ("b_roll", "host") or detail.lower() in base.lower():
        return detail
    return f"{base}: {detail}"


def format_youtube_timestamp(seconds: float) -> str:
    total = max(0, int(seconds))
    h, rem = divmod(total, 3600)
    m, s = divmod(rem, 60)
    if h:
        return f"{h}:{m:02d}:{s:02d}"
    return f"{m:02d}:{s:02d}"


def build_chapters(
    script: dict[str, Any],
    *,
    xfade_s: float = 0.0,
) -> list[dict[str, Any]]:
    """Chapter markers from shot timings (xfade overlap shifts later chapters slightly)."""
    shots = [s for s in script.get("shots", []) if s.get("role") != "card"]
    chapters: list[dict[str, Any]] = []
    drift = 0.0
    for i, shot in enumerate(shots):
        if shot.get("t_start") is not None:
            start = float(shot["t_start"]) - drift
        else:
            start = sum(
                float(shots[j].get("duration", 0)) - (xfade_s if j > 0 else 0.0)
                for j in range(i)
            )
        if i > 0 and xfade_s:
            drift += xfade_s
        label = chapter_label(shot)
        chapters.append({
            "shot_id": shot["id"],
            "start_s": round(max(0.0, start), 2),
            "label": label,
            "youtube": f"{format_youtube_timestamp(start)} {label}",
        })
    prov = script.get("provenance_card") or {}
    if prov.get("enabled", True):
        perf_end = chapters[-1]["start_s"] + float(shots[-1].get("duration", 0)) if chapters else 0.0
        if chapters:
            perf_end = float(shots[-1].get("t_end", perf_end))
        prov_start = perf_end - (xfade_s if xfade_s and chapters else 0.0)
        prov_label = prov.get("title") or "Credits"
        chapters.append({
            "shot_id": "provenance_card",
            "start_s": round(max(0.0, prov_start), 2),
            "label": prov_label,
            "youtube": f"{format_youtube_timestamp(prov_start)} {prov_label}",
        })
    return chapters


def _format_profile(script: dict[str, Any]) -> dict[str, Any]:
    fmt = script.get("format_id", "documentary-host")
    return FORMAT_PROFILES.get(fmt, FORMAT_PROFILES["documentary-host"])


def build_seo(
    script: dict[str, Any],
    *,
    chapters: list[dict[str, Any]],
    video_duration_s: float | None = None,
) -> dict[str, Any]:
    publish = script.get("publish") or {}
    prov = script.get("provenance_card") or {}
    meta = script.get("production_meta") or {}
    profile = _format_profile(script)

    card_title = prov.get("title") or _slug_to_title(script.get("slug", "episode"))
    title = publish.get("title") or f"{card_title} {profile['title_suffix']}".strip()
    title = title[:100]

    actor = meta.get("actor_id") or meta.get("identity_anchor", "").lstrip("@")
    set_id = (meta.get("set_id") or "").replace("@Set-", "").replace("-", " ")
    rating = meta.get("target_rating") or meta.get("content_rating") or "PG"

    hook = publish.get("hook") or script.get("concept") or card_title
    lines = [
        hook,
        "",
        publish.get("body") or (
            f"{card_title} — synthetic {script.get('format_id', 'production').replace('-', ' ')} "
            f"from Upon Tyne Productions / STUDIO pipeline."
        ),
        "",
    ]
    if actor:
        lines.append(f"Performer: synthetic talent ({actor}) · {rating}")
    if set_id:
        lines.append(f"Set: {set_id.strip()}")
    lines.extend([
        "",
        "── Chapters ──",
        *[c["youtube"] for c in chapters],
        "",
        "Synthetic media disclosure: characters and performances are fully synthetic.",
        "No real-person likeness. SFW / age-verified talent roster.",
        "",
        publish.get("cta") or prov.get("footer") or "Subscribe for more STUDIO productions.",
    ])
    description = "\n".join(lines).strip()

    tags = list(publish.get("tags") or [])
    for tag in profile["tag_pool"]:
        if tag not in tags:
            tags.append(tag)
    if card_title.lower() not in {t.lower() for t in tags}:
        tags.insert(0, card_title)
    tags = tags[:30]

    return {
        "title": title,
        "description": description,
        "tags": tags,
        "category": publish.get("category") or profile["category"],
        "playlist": publish.get("playlist") or profile["playlist"],
        "language": publish.get("language", "en"),
        "made_for_kids": bool(publish.get("made_for_kids", False)),
    }


def build_end_screen(
    script: dict[str, Any],
    *,
    video_duration_s: float,
) -> dict[str, Any]:
    publish = script.get("publish") or {}
    end_cfg = publish.get("end_screen") or {}
    prov = script.get("provenance_card") or {}
    trigger_lead = float(end_cfg.get("trigger_lead_s", 20))
    trigger_at = max(0.0, video_duration_s - trigger_lead)

    elements = end_cfg.get("elements")
    if not elements:
        elements = [
            {
                "type": "subscribe",
                "position": "bottom_left",
                "start_s": round(trigger_at, 1),
                "duration_s": trigger_lead,
            },
            {
                "type": "best_for_viewer",
                "position": "top_right",
                "start_s": round(trigger_at, 1),
                "duration_s": trigger_lead,
                "placeholder": "NEXT_VIDEO_ID",
            },
            {
                "type": "playlist",
                "position": "center",
                "start_s": round(trigger_at, 1),
                "duration_s": trigger_lead,
                "playlist": publish.get("playlist") or _format_profile(script)["playlist"],
            },
        ]
        link = publish.get("channel_url")
        if link:
            elements.append({
                "type": "link",
                "position": "bottom_right",
                "label": prov.get("subtitle") or "STUDIO Channel",
                "url": link,
                "start_s": round(trigger_at, 1),
                "duration_s": trigger_lead,
            })

    return {
        "platform": end_cfg.get("platform", "youtube"),
        "video_duration_s": round(video_duration_s, 2),
        "trigger_at_s": round(trigger_at, 2),
        "trigger_lead_s": trigger_lead,
        "elements": elements,
        "editor_notes": end_cfg.get("editor_notes") or (
            "Import elements in YouTube Studio → Editor → End screen. "
            "Align subscribe + suggested video to final 20s; provenance card is the natural outro."
        ),
    }


def build_thumbnail_brief(
    script: dict[str, Any],
    *,
    candidates: list[dict[str, Any]],
) -> dict[str, Any]:
    publish = script.get("publish") or {}
    thumb = publish.get("thumbnail") or {}
    prov = script.get("provenance_card") or {}
    meta = script.get("production_meta") or {}
    card_title = prov.get("title") or _slug_to_title(script.get("slug", "episode"))

    return {
        "status": "HANDOFF",
        "title_overlay": thumb.get("title_overlay") or card_title.upper(),
        "subtitle_overlay": thumb.get("subtitle_overlay") or prov.get("subtitle", ""),
        "channel_badge": "DAVID · The Archive",
        "aspect_ratio": "16:9",
        "target_px": [1280, 720],
        "candidates": candidates,
        "prompt": thumb.get("prompt") or (
            f"YouTube thumbnail, cinematic high-contrast, title-safe negative space left third, "
            f"{card_title}, {meta.get('set_id', 'dramatic set')}, "
            f"synthetic performer {meta.get('actor_id', '')}, no real person likeness, "
            f"bold readable mood, film grain, no clutter, SFW"
        ),
        "design_notes": thumb.get("design_notes") or [
            "Use candidate_peak_frame.jpg as base unless art-directed override",
            "Keep face in right two-thirds; title text in left third",
            "Warehouse window light 4800K warm key; deep shadows",
            "Export PNG 1280×720 under 2MB",
        ],
        "delivery_filename": thumb.get("delivery_filename") or "thumbnail_1280x720.png",
    }


# ── Upload-kit constants ──────────────────────────────────────────────────────

AI_DISCLOSURE_FULL: str = (
    "AI Disclosure — Upon Tyne Productions\n\n"
    "This video features AI-generated synthetic performers. No real persons depicted. "
    "All characters, voices, and performances are fully computer-generated by the STUDIO "
    "synthetic pipeline. Synthetic media is labelled per YouTube's AI-generated content "
    "disclosure policy.\n\n"
    "Producer: Upon Tyne Productions · STUDIO pipeline\n"
    "Render engine: DAVID (Documentary Archive of Vocal Intelligence Data)\n"
    "Performers: Synthetic talent roster — no real-person likeness used or implied\n\n"
    "For full provenance, credits, and production notes see the closing card."
)

SECTION_2257_NOTE: str = (
    "18 U.S.C. § 2257 Compliance — Upon Tyne Productions\n\n"
    "All performers depicted in Upon Tyne Productions content are synthetic "
    "(AI-generated). No real persons are depicted. Upon Tyne Productions maintains "
    "documentation confirming the fully synthetic nature of all talent per the "
    "STUDIO Casting Bible and synthetic talent registry.\n\n"
    "Custodian of records: Upon Tyne Productions / STUDIO / Legal_Gate"
)


def build_youtube_description(
    script: dict[str, Any],
    *,
    chapters: list[dict[str, Any]],
) -> str:
    """3-4 paragraph YouTube description: hook, summary, AI disclosure, CTA.

    Mandatory inclusions:
      · "AI-generated synthetic performers. No real persons depicted."
      · "Upon Tyne Productions"
    """
    publish = script.get("publish") or {}
    prov = script.get("provenance_card") or {}
    intake = script.get("intake") or {}
    gate = intake.get("gate_0") or {}

    card_title = prov.get("title") or _slug_to_title(script.get("slug", "episode"))
    rating = gate.get("target_rating") or "PG"
    hook = publish.get("hook") or script.get("title") or card_title

    # ¶1 — hook / cold-open line
    para1 = hook

    # ¶2 — summary
    para2 = publish.get("body") or (
        f"{card_title} — a documentary episode from DAVID · The Archive, "
        f"the Upon Tyne Productions series on dead languages, actually pronounced. "
        f"Format: {script.get('format_id', 'documentary-host').replace('-', ' ').title()}. "
        f"Rating: {rating}."
    )

    # Chapters block
    ch_block = "\n".join(["── Chapters ──"] + [c["youtube"] for c in chapters])

    # ¶3 — AI disclosure (mandatory language)
    para3 = (
        "AI-generated synthetic performers. No real persons depicted. "
        "This production is entirely synthetic — characters, voice, and visuals rendered by the "
        "STUDIO pipeline. Created by Upon Tyne Productions."
    )

    # ¶4 — CTA
    cta = publish.get("cta") or prov.get("footer") or (
        "Subscribe to DAVID · The Archive — new dead language every week."
    )

    lines = [
        para1, "",
        para2, "",
        ch_block, "",
        para3, "",
        "──────────────────────────",
        "Upon Tyne Productions · STUDIO · DAVID · The Archive",
        "AI-generated synthetic content disclosed per platform policy.",
        "",
        cta,
    ]
    return "\n".join(lines).strip()


def package_episode(
    script_json_path: "Path | str",
    mp4_path: "Path | str | None",
    out_dir: "Path | str",
) -> "tuple[dict[str, Any], Path, Path]":
    """Generate upload kit JSON + human-readable brief TXT for one episode.

    This is the programmatic API called by batch_runner.py.  Unlike
    ``package_production()``, it takes explicit paths and does not require
    an MP4 (it falls back to ``target_seconds`` for duration estimates).

    Args:
        script_json_path: Path to ``<slug>_script.json``
        mp4_path:         Path to rendered MP4, or ``None`` if not yet rendered
        out_dir:          Directory to write output files into

    Returns:
        ``(kit_dict, upload_kit_json_path, upload_brief_txt_path)``
    """
    script_json_path = Path(script_json_path)
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    script: dict[str, Any] = json.loads(script_json_path.read_text(encoding="utf-8"))

    slug      = script.get("slug", script_json_path.stem.replace("_script", ""))
    title     = script.get("title", _slug_to_title(slug))
    format_id = script.get("format_id", "documentary-host")
    target_s  = int(script.get("target_seconds") or 69)
    prov      = script.get("provenance_card") or {}
    intake    = script.get("intake") or {}
    gate      = intake.get("gate_0") or {}

    # ── Chapters ──────────────────────────────────────────────────────────────
    seam    = (script.get("config") or {}).get("seamless") or {}
    xfade_s = float(seam.get("xfade_s", 0.2)) if seam else 0.0
    raw_chapters = build_chapters(script, xfade_s=xfade_s)
    chapters = [
        {"timestamp": c["youtube"].split(" ", 1)[0], "label": c["label"]}
        for c in raw_chapters
    ]

    # ── Duration ──────────────────────────────────────────────────────────────
    video_duration_s: float = float(target_s)
    if mp4_path and Path(mp4_path).is_file():
        try:
            video_duration_s = _probe_duration(Path(mp4_path))
        except Exception:
            pass  # fall back to target_seconds

    # ── SEO base ──────────────────────────────────────────────────────────────
    seo = build_seo(script, chapters=raw_chapters, video_duration_s=video_duration_s)
    # Prefer the script-level title (episode-specific hook) over the generic
    # prov-card title that build_seo() falls back to when publish.title is absent.
    _script_title = (script.get("title") or "").strip()
    youtube_title = (_script_title if _script_title else seo["title"])[:100]

    # Tags: merge seo pool + mandatory channel tags, cap at 15
    must_have_tags = [
        "Upon Tyne Productions", "DAVID The Archive", "dead languages",
        "synthetic media", "AI documentary", "linguistics", "language history",
    ]
    seen: set[str] = set()
    merged_tags: list[str] = []
    for t in (list(seo.get("tags") or []) + must_have_tags):
        low = t.lower()
        if low not in seen:
            seen.add(low)
            merged_tags.append(t)
    youtube_tags = merged_tags[:15]

    # ── Description ───────────────────────────────────────────────────────────
    youtube_description = build_youtube_description(script, chapters=raw_chapters)

    # ── End screen (simplified kit field) ────────────────────────────────────
    trigger_s = round(max(0.0, video_duration_s - 20.0), 1)
    end_screen = {
        "cta_text": prov.get("footer") or "Subscribe to DAVID · The Archive",
        "subscribe_prompt": "Follow the Archive — new dead language every week.",
        "timestamp_s": trigger_s,
    }

    # ── Gate summary ──────────────────────────────────────────────────────────
    gate_summary = {
        "verdict":       gate.get("verdict", "UNKNOWN"),
        "target_rating": gate.get("target_rating", "UNKNOWN"),
        "blocked":       gate.get("blocked"),
        "hard_stops":    gate.get("hard_stops", []),
        "cara_status":   gate.get("cara_status", "UNKNOWN"),
        "report_path":   gate.get("report_path", ""),
    }

    # ── Assemble kit dict ─────────────────────────────────────────────────────
    kit: dict[str, Any] = {
        "slug":                slug,
        "title":               title,
        "format_id":           format_id,
        "target_seconds":      target_s,
        "youtube_title":       youtube_title,
        "youtube_description": youtube_description,
        "youtube_tags":        youtube_tags,
        "chapters":            chapters,
        "youtube_chapters":    [c["youtube"] for c in raw_chapters],
        "end_screen":          end_screen,
        "ai_disclosure_card":  AI_DISCLOSURE_FULL,
        "section_2257_note":   SECTION_2257_NOTE,
        "gate_summary":        gate_summary,
        "mp4_path":            str(mp4_path) if mp4_path else None,
        "video_duration_s":    round(video_duration_s, 2),
        # Populated by batch_runner or manually from Music_Bed_Manifest.json after clearance
        # Stamp via: script.json → intake.music_bed_id (see STUDIO/Art_Department/Music/Clearance_SOP.md)
        "music_bed_id":        (intake.get("music_bed_id") or None),
        "music_attribution":   (intake.get("music_attribution") or None),
        "generated_by":        "package_episode() · STUDIO Pipeline",
    }

    # -- Write upload_kit.json
    kit_json_path = out_dir / f"{slug}_upload_kit.json"
    kit_json_path.write_text(
        json.dumps(kit, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )

    # -- Write upload_brief.txt (copy-paste ready for YouTube Studio)
    brief_lines = [
        "=" * 63,
        f"  UPLOAD BRIEF -- {slug}",
        "  Upon Tyne Productions | STUDIO | DAVID | The Archive",
        "=" * 63,
        "",
        "TITLE  (paste into YouTube Studio -> Title field)",
        "-" * 49,
        youtube_title,
        "",
        "DESCRIPTION  (paste into Description field)",
        "-" * 49,
        youtube_description,
        "",
        "TAGS  (paste comma-separated into Tags field)",
        "-" * 49,
        ", ".join(youtube_tags),
        "",
        "CHAPTERS  (already embedded in description above)",
        "-" * 49,
        *[c["youtube"] for c in raw_chapters],
        "",
        "END SCREEN",
        "-" * 49,
        f"CTA text:         {end_screen['cta_text']}",
        f"Subscribe prompt: {end_screen['subscribe_prompt']}",
        f"Trigger at:       {end_screen['timestamp_s']}s  (final 20s of video)",
        "",
        "AI DISCLOSURE CARD",
        "-" * 49,
        AI_DISCLOSURE_FULL,
        "",
        "MUSIC BED",
        "-" * 49,
        f"music_bed_id:     {kit.get('music_bed_id') or 'NOT ASSIGNED — see STUDIO/Art_Department/Music/'}",
        f"music_attribution:{' ' + kit['music_attribution'] if kit.get('music_attribution') else ' n/a (no attribution required)'}",
        "",
        "GATE SUMMARY",
        "-" * 49,
        f"Verdict:       {gate_summary['verdict']}",
        f"Target rating: {gate_summary['target_rating']}",
        f"CARA status:   {gate_summary['cara_status']}",
        f"Blocked:       {gate_summary['blocked']}",
        "",
        "18 U.S.C. Sec. 2257 NOTE",
        "-" * 49,
        SECTION_2257_NOTE,
        "",
        "=" * 63,
        "  Generated by: STUDIO Pipeline | package_episode()",
        "=" * 63,
    ]
    brief_txt_path = out_dir / f"{slug}_upload_brief.txt"
    brief_txt_path.write_text("\n".join(brief_lines) + "\n", encoding="utf-8")

    print(f"[package_episode] {slug} -> {kit_json_path.name} + {brief_txt_path.name}")
    return kit, kit_json_path, brief_txt_path


def resolve_production(path: Path) -> tuple[Path, dict[str, Any], dict[str, Any], Path]:
    """Return (prod_dir, script, manifest, mp4_path)."""
    path = path.resolve()
    if path.is_file():
        if path.name == "manifest.json":
            prod_dir = path.parent
            manifest = json.loads(path.read_text(encoding="utf-8"))
        elif path.suffix == ".json" and "shots" in json.loads(path.read_text(encoding="utf-8")):
            prod_dir = path.parent
            manifest = json.loads((prod_dir / "manifest.json").read_text(encoding="utf-8")) if (prod_dir / "manifest.json").is_file() else {}
            script = json.loads(path.read_text(encoding="utf-8"))
            mp4 = _resolve_mp4(prod_dir, manifest, script)
            return prod_dir, script, manifest, mp4
        else:
            raise FileNotFoundError(f"Unrecognized input file: {path}")
        script_path = Path(manifest.get("script", prod_dir / f"{manifest.get('qa', {}).get('slug', 'longform')}_script.json"))
        if not script_path.is_file():
            candidates = list(prod_dir.glob("*_script.json"))
            script_path = candidates[0] if candidates else script_path
        script = json.loads(script_path.read_text(encoding="utf-8"))
        mp4 = _resolve_mp4(prod_dir, manifest, script)
        return prod_dir, script, manifest, mp4
    if path.is_dir():
        prod_dir = path
        manifest = json.loads((prod_dir / "manifest.json").read_text(encoding="utf-8")) if (prod_dir / "manifest.json").is_file() else {}
        script_candidates = list(prod_dir.glob("*_script.json"))
        if not script_candidates:
            raise FileNotFoundError(f"No script JSON in {prod_dir}")
        script = json.loads(script_candidates[0].read_text(encoding="utf-8"))
        mp4 = _resolve_mp4(prod_dir, manifest, script)
        return prod_dir, script, manifest, mp4
    raise FileNotFoundError(f"Not found: {path}")


def _resolve_mp4(prod_dir: Path, manifest: dict[str, Any], script: dict[str, Any]) -> Path:
    if manifest.get("output"):
        p = Path(manifest["output"])
        if p.is_file():
            return p
    slug = script.get("slug", "longform")
    out_dir = prod_dir / "output"
    for pattern in (f"*_{slug}_seamless_v1.mp4", f"*_{slug}_longform_v1.mp4", "*.mp4"):
        matches = sorted(out_dir.glob(pattern), key=lambda x: x.stat().st_mtime, reverse=True)
        if matches:
            return matches[0]
    raise FileNotFoundError(f"No output MP4 in {out_dir}")


def package_production(
    path: Path,
    *,
    mp4: "Path | None" = None,
    require_qa_pass: bool = True,
    out_subdir: str = "upload_kit",
) -> dict[str, Any]:
    prod_dir, script, manifest, resolved_mp4 = resolve_production(path)
    video = mp4 or resolved_mp4
    if not video.is_file():
        raise FileNotFoundError(f"MP4 not found: {video}")

    qa = manifest.get("qa") or {}
    if require_qa_pass and qa and not qa.get("pass"):
        raise RuntimeError(f"QA pass required before packaging (pass={qa.get('pass')})")

    kit_dir = prod_dir / out_subdir
    if kit_dir.exists():
        shutil.rmtree(kit_dir)
    kit_dir.mkdir(parents=True)

    seam = (script.get("config") or {}).get("seamless") or {}
    xfade_s = float(seam.get("xfade_s", 0.2) if seam else 0.0)
    duration_s = _probe_duration(video)
    chapters = build_chapters(script, xfade_s=xfade_s)
    seo = build_seo(script, chapters=chapters, video_duration_s=duration_s)
    end_screen = build_end_screen(script, video_duration_s=duration_s)

    shots = [s for s in script.get("shots", []) if s.get("role") != "card"]
    thumb_dir = kit_dir / "thumbnail"
    thumb_dir.mkdir()
    candidates: list[dict[str, Any]] = []

    peak = next((s for s in shots if "peak" in s["id"]), shots[len(shots) // 2] if shots else None)
    establish = shots[0] if shots else None
    if peak:
        at = float(peak.get("t_start", 0)) + float(peak.get("duration", 8)) * 0.45
        out = thumb_dir / "candidate_peak_frame.jpg"
        _extract_frame(video, at, out)
        candidates.append({"file": out.name, "shot_id": peak["id"], "at_s": round(at, 2), "role": "primary"})
    if establish and establish != peak:
        at = float(establish.get("t_start", 0)) + float(establish.get("duration", 7)) * 0.5
        out = thumb_dir / "candidate_establishing_frame.jpg"
        _extract_frame(video, at, out)
        candidates.append({"file": out.name, "shot_id": establish["id"], "at_s": round(at, 2), "role": "alternate"})

    prov_png = prod_dir / "provenance_card.png"
    if prov_png.is_file():
        shutil.copy2(prov_png, thumb_dir / "provenance_reference.png")
        candidates.append({"file": "provenance_reference.png", "shot_id": "provenance_card", "role": "credit_reference"})

    thumb_brief = build_thumbnail_brief(script, candidates=candidates)

    video_dir = kit_dir / "video"
    video_dir.mkdir()
    dest_mp4 = video_dir / video.name
    shutil.copy2(video, dest_mp4)

    seo_dir = kit_dir / "seo"
    seo_dir.mkdir()
    (seo_dir / "title.txt").write_text(seo["title"] + "\n", encoding="utf-8")
    (seo_dir / "description.txt").write_text(seo["description"] + "\n", encoding="utf-8")
    (seo_dir / "tags.txt").write_text(", ".join(seo["tags"]) + "\n", encoding="utf-8")
    (seo_dir / "seo.json").write_text(json.dumps(seo, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    ch_dir = kit_dir / "chapters"
    ch_dir.mkdir()
    youtube_lines = [c["youtube"] for c in chapters]
    (ch_dir / "youtube_chapters.txt").write_text("\n".join(youtube_lines) + "\n", encoding="utf-8")
    (ch_dir / "chapters.json").write_text(
        json.dumps({"chapters": chapters, "xfade_s": xfade_s}, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    end_dir = kit_dir / "end_screen"
    end_dir.mkdir()
    (end_dir / "end_screen.json").write_text(
        json.dumps(end_screen, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )

    (thumb_dir / "THUMBNAIL_BRIEF.json").write_text(
        json.dumps(thumb_brief, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )

    checklist = "\n".join([
        "# Upload checklist",
        "",
        f"- [ ] Video: `video/{dest_mp4.name}` ({duration_s:.1f}s)",
        f"- [ ] Title: `{seo['title']}`",
        "- [ ] Description: paste `seo/description.txt` (chapters pre-embedded)",
        f"- [ ] Tags: `{', '.join(seo['tags'][:8])}...`",
        f"- [ ] Category: {seo['category']}",
        f"- [ ] Playlist: {seo['playlist']}",
        "- [ ] Thumbnail: finalize from `thumbnail/THUMBNAIL_BRIEF.json`",
        "- [ ] End screen: configure per `end_screen/end_screen.json`",
        "- [ ] Synthetic media disclosure: included in description",
        f"- [ ] QA pass verified: {qa.get('pass', 'n/a')}",
    ])
    (kit_dir / "CHECKLIST.md").write_text(checklist + "\n", encoding="utf-8")

    kit_manifest = {
        "packaged_at": datetime.now(timezone.utc).isoformat(),
        "slug": script.get("slug"),
        "format_id": script.get("format_id"),
        "production_dir": str(prod_dir),
        "source_video": str(video),
        "video_duration_s": round(duration_s, 2),
        "qa_pass": qa.get("pass"),
        "paths": {
            "video": str(dest_mp4.relative_to(kit_dir)),
            "seo": "seo/seo.json",
            "chapters": "chapters/youtube_chapters.txt",
            "end_screen": "end_screen/end_screen.json",
            "thumbnail_brief": "thumbnail/THUMBNAIL_BRIEF.json",
            "checklist": "CHECKLIST.md",
        },
    }
    (kit_dir / "manifest.json").write_text(
        json.dumps(kit_manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    print(f"[package_production] {script.get('slug')} → {kit_dir.name}/")
    return kit_manifest


# ── CLI ───────────────────────────────────────────────────────────────────────

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="MP4 → platform upload kit (SEO, chapters, end-screen, thumbnail brief)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "path",
        help="Production dir, manifest.json, or script.json",
    )
    parser.add_argument("--mp4", default=None, help="Override path to rendered MP4")
    parser.add_argument(
        "--no-qa-check", dest="require_qa_pass", action="store_false",
        help="Skip QA pass requirement",
    )
    args = parser.parse_args(argv)

    prod_path = Path(args.path)
    mp4_path  = Path(args.mp4) if args.mp4 else None

    kit = package_production(
        prod_path,
        mp4=mp4_path,
        require_qa_pass=args.require_qa_pass,
    )
    print(f"[package_episode] Done. Kit written to: {kit.get('paths', {})}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
