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
    mp4: Path | None = None,
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
        f"- [ ] Tags: `{', '.join(seo['tags'][:8])}…`",
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
        json.dumps(kit_manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )

    print(f"[package] upload kit → {kit_dir}")
    return {"upload_kit": str(kit_dir), "manifest": kit_manifest, "seo": seo}


def main() -> int:
    parser = argparse.ArgumentParser(description="Package rendered episode for platform upload")
    parser.add_argument("path", type=Path, help="Production dir, manifest.json, or script.json")
    parser.add_argument("--mp4", type=Path, default=None, help="Override output MP4 path")
    parser.add_argument("--allow-fail-qa", action="store_true", help="Package even if QA did not pass")
    args = parser.parse_args()

    result = package_production(
        args.path,
        mp4=args.mp4,
        require_qa_pass=not args.allow_fail_qa,
    )
    print(json.dumps(result["manifest"], indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())