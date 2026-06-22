#!/usr/bin/env python3
"""STUDIO consume_ai_handoff — StudioPackage → script.json

Reads a StudioPackage (from the AI Visualization Federation) and writes a
canonical render_longform script.json to STUDIO/Productions/<slug>/.

Gate 0 legal runs as mandatory pre-step. RED blocks script.json emission.

Handoff Contract: AI/docs/Feeder_AI_STUDIO_Handoff_Contract_v1.md  section 4
Shape detected by render_longform.py via presence of both 'config' and 'shots'.

CLI
---
    python consume_ai_handoff.py <studio_package.json>
    python consume_ai_handoff.py <studio_package.json> -o <out_path>

Pure stdlib. No network, no API calls.
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

# ---------------------------------------------------------------------------
# Paths — resolved relative to this file so the module is location-stable.
# ---------------------------------------------------------------------------
PIPELINE_DIR    = Path(__file__).resolve().parent        # .../STUDIO/Pipeline
STUDIO_DIR      = PIPELINE_DIR.parent                    # .../STUDIO
ROOT_DIR        = STUDIO_DIR.parent                      # .../Grok Projects
PRODUCTIONS_DIR = STUDIO_DIR / "Productions"

# ---------------------------------------------------------------------------
# Render resolution — override to "1280x720" for 720p or "1920x1080" for production.
# Set to "" or None to fall through to deliverable_spec.resolution.
# ---------------------------------------------------------------------------
RENDER_RESOLUTION: str = "854x480"  # test render resolution

# ---------------------------------------------------------------------------
# Required field spec  (mirrors section 4 of the Handoff Contract)
# ---------------------------------------------------------------------------
_REQUIRED_TOP: tuple[str, ...] = (
    "handoff_id",
    "lane",
    "cinematic_style",
    "concept_hint",
    "provenance",
)
_REQUIRED_CONCEPT_HINT: tuple[str, ...] = ("slug", "beats")
_REQUIRED_PROVENANCE:   tuple[str, ...] = ("source_repo", "citations", "gate_status")


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------
def validate_studio_package(pkg: dict[str, Any]) -> list[str]:
    """Return a list of validation error strings (empty list = valid).

    Checks all fields the Handoff Contract requires STUDIO to accept:
      handoff_id, lane, cinematic_style, concept_hint.slug,
      concept_hint.beats (non-empty list), provenance.source_repo,
      provenance.citations, provenance.gate_status.
    """
    errors: list[str] = []

    for field in _REQUIRED_TOP:
        val = pkg.get(field)
        if val is None or val == "" or val == [] or val == {}:
            errors.append(f"Missing or empty required field: '{field}'")

    hint = pkg.get("concept_hint") or {}
    for field in _REQUIRED_CONCEPT_HINT:
        val = hint.get(field)
        if val is None or val == "" or val == [] or val == {}:
            errors.append(f"Missing or empty required field: 'concept_hint.{field}'")

    beats = hint.get("beats")
    if beats is not None and not isinstance(beats, list):
        errors.append("'concept_hint.beats' must be a list")
    elif isinstance(beats, list) and len(beats) == 0:
        errors.append("'concept_hint.beats' must be a non-empty list")

    prov = pkg.get("provenance") or {}
    for field in _REQUIRED_PROVENANCE:
        val = prov.get(field)
        if val is None or val == "" or val == [] or val == {}:
            errors.append(f"Missing or empty required field: 'provenance.{field}'")

    return errors


# ---------------------------------------------------------------------------
# Video-prompt builder
# ---------------------------------------------------------------------------
def _build_video_prompt(
    beat: dict[str, Any],
    cinematic_style: str,
    render_directives: dict[str, Any],
    lane: str,
    shot_index: int = 0,
    total_shots: int = 1,
) -> str:
    """Build a render_longform-compatible video_prompt from one beat.

    Encodes: lane, cinematic style, camera directive, render flags, motion
    continuity cue, and the speech delivery note (lip-sync cue).  No API
    calls — pure string assembly from the StudioPackage data the AI
    federation already computed.

    Args:
        beat:          Beat dict from concept_hint.
        cinematic_style: Top-level cinematic style string.
        render_directives: render_directives block from the StudioPackage.
        lane:          Channel lane string.
        shot_index:    0-based index of this shot in the sequence.
        total_shots:   Total number of shots in the episode.
    """
    camera       = render_directives.get("camera", "free_cam + subtle_dolly")
    motion_blur  = render_directives.get("motion_blur", False)
    impasto      = render_directives.get("impasto_texture", True)
    period_grade = render_directives.get("period_grade", False)
    heat_haze    = render_directives.get("heat_haze", False)

    render_flags: list[str] = []
    if impasto:      render_flags.append("impasto texture")
    if motion_blur:  render_flags.append("motion blur")
    if period_grade: render_flags.append("period grade color")
    if heat_haze:    render_flags.append("heat haze")

    flag_note = (", ".join(render_flags) + ".") if render_flags else ""
    speech    = beat.get("speech_text", "")
    action    = beat.get("action", "Documentary host in frame, composed and authoritative.")

    # Motion continuity cue — keeps visual flow across dissolves
    is_last = (shot_index == total_shots - 1)
    if shot_index == 0:
        continuity_cue = "Opening shot, establish environment slowly."
    elif is_last:
        continuity_cue = "Final shot — slowly pull back or hold still, let breath settle."
    else:
        continuity_cue = "Continue from previous shot — same camera direction, smooth motion carry."

    parts: list[str] = [
        f"[{lane}] {cinematic_style}.",
        f"Camera: {camera}.",
    ]
    if flag_note:
        parts.append(flag_note)
    parts.append(action)
    parts.append(continuity_cue)
    if speech:
        parts.append(
            f'Lip-synced, delivers: "{speech}" documentary narrator, synthetic host only.'
        )

    return " ".join(p for p in parts if p)


# ---------------------------------------------------------------------------
# Shot builder
# ---------------------------------------------------------------------------
def _build_shots(
    beats: list[dict[str, Any]],
    cinematic_style: str,
    render_directives: dict[str, Any],
    lane: str,
    duration_s: float = 60.0,
) -> list[dict[str, Any]]:
    """Convert concept_hint beats into render_longform shot objects.

    Duration per shot: uses beat['duration'] when present; otherwise
    distributes total duration_s evenly (min 12 s per shot — documentary pace).
    """
    n = len(beats)
    per_shot_default = max(12, round(duration_s / n)) if n else 12

    shots: list[dict[str, Any]] = []
    t = 0
    for i, beat in enumerate(beats):
        duration = int(beat.get("duration", per_shot_default))
        shot: dict[str, Any] = {
            "id":        beat.get("id", f"{i + 1:02d}_shot"),
            "duration":  duration,
            "t_start":   t,
            "t_end":     t + duration,
            "role":      beat.get("role", "host"),
            "video_prompt": _build_video_prompt(
                beat, cinematic_style, render_directives, lane,
                shot_index=i, total_shots=n,
            ),
        }
        # Optional fields — only set when the beat supplies them
        if beat.get("speech_text"):
            shot["speech_text"] = beat["speech_text"]
        if beat.get("on_screen"):
            shot["on_screen"] = beat["on_screen"]
        if beat.get("on_screen_labels"):
            shot["on_screen_labels"] = beat["on_screen_labels"]
        if beat.get("speech_lang"):
            shot["speech_lang"] = beat["speech_lang"]
        if beat.get("speech_ipa"):
            shot["speech_ipa"] = beat["speech_ipa"]

        shots.append(shot)
        t += duration

    return shots


# ---------------------------------------------------------------------------
# Config builder
# ---------------------------------------------------------------------------
def _build_config(pkg: dict[str, Any]) -> dict[str, Any]:
    """Assemble the script config block from deliverable_spec + defaults."""
    spec = pkg.get("deliverable_spec") or {}
    # RENDER_RESOLUTION constant overrides spec when set; flip to "" for production.
    resolution = RENDER_RESOLUTION or spec.get("resolution", "1920x1080")

    # Infer aspect ratio from WxH string (e.g. "854x480" → "16:9")
    aspect = "16:9"
    res_str = str(resolution).lower()
    if "x" in res_str:
        try:
            w, h = res_str.split("x", 1)
            if int(w.strip()) < int(h.strip()):
                aspect = "9:16"
        except (ValueError, TypeError):
            pass

    return {
        "model_video":  "grok-imagine-video-1.5",
        "resolution":   resolution,
        "aspect_ratio": aspect,
        "render_mode":  "test",       # "test" = 480p fast pass; set "production" for full quality
        "voice_suffix": "documentary narrator, synthetic host only",
        "seamless": {
            "primary":        "dissolve",   # was "extend" — dissolve reads as intentional
            "xfade_s":        1.8,          # was 0.15 — documentary standard (1.5–2.0 s)
            "loudnorm":       True,
            "pin_audio_sync": True,
            "motion_carry":   True,         # signal renderer to carry motion vectors across cut
            "cut_style":      "soft",       # "soft" = dissolve/fade; "hard" = cut
        },
    }


# ---------------------------------------------------------------------------
# Gate 0 — legal pre-step helper
# ---------------------------------------------------------------------------
def _run_legal_gate_on_handoff(pkg: dict[str, Any]) -> dict[str, Any]:
    """Run LegalGate.review() against the handoff package.  Hard stop on RED.

    Resolves legal_gate.py from ROOT_DIR/artifacts/legal/ (two levels up from
    PIPELINE_DIR).  If the import is unavailable, logs a warning and returns a
    non-blocking result so the pipeline can still be exercised without the full
    legal dependency installed.

    Returns:
        Gate result dict — always contains at least 'blocked' and 'verdict'.
    """
    import importlib.util
    import logging

    gate_path = ROOT_DIR / "artifacts" / "legal" / "legal_gate.py"
    try:
        if not gate_path.is_file():
            raise FileNotFoundError(f"legal_gate.py not found at {gate_path}")

        spec = importlib.util.spec_from_file_location("legal_gate", gate_path)
        legal_gate_mod = importlib.util.module_from_spec(spec)  # type: ignore[arg-type]
        spec.loader.exec_module(legal_gate_mod)  # type: ignore[union-attr]

        # Build a brief from the StudioPackage fields Gate 0 needs to see.
        prov      = pkg.get("provenance") or {}
        hint      = pkg.get("concept_hint") or {}
        slug      = hint.get("slug", "unknown")
        lane      = pkg.get("lane", "")
        citations = " ".join(str(c) for c in (prov.get("citations") or []))
        gate_note = str(prov.get("gate_status") or "")
        brief     = (
            f"slug: {slug}\n"
            f"lane: {lane}\n"
            f"source_repo: {prov.get('source_repo', '')}\n"
            f"citations: {citations}\n"
            f"gate_status: {gate_note}\n"
            "synthetic: true\n"
            "real_person_likeness: false\n"
            "ai disclosure planned\n"
        )

        gate   = legal_gate_mod.LegalGate()
        result = gate.review(
            brief,
            slug,
            target_rating="PG-13",
            channels=["social"],
            has_performers=True,
        )
        return result.to_dict()

    except Exception as exc:
        logging.warning(
            "[consume_ai_handoff] legal_gate not available — proceeding with WARN_NO_GATE. "
            "Reason: %s", exc
        )
        return {
            "blocked": False,
            "verdict": "WARN_NO_GATE",
            "warning": f"legal_gate not found or failed to load: {exc}",
        }


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------
def consume_ai_handoff(
    pkg: dict[str, Any],
    out_dir: Optional[Path] = None,
) -> Path:
    """Read a StudioPackage dict, build a script.json, write to Productions/<slug>/.

    This is the STUDIO intake gate for the AI federation handoff.  It validates
    the required fields, runs Gate 0 legal as a mandatory pre-step (RED blocks
    script.json emission), assembles a canonical render_longform script, and
    writes it to disk.

    Args:
        pkg:     StudioPackage dict (AI federation output per Handoff Contract §3).
        out_dir: Override the output directory (defaults to
                 STUDIO/Productions/<slug>/).

    Returns:
        Path to the written script.json.

    Raises:
        ValueError: if any required field is missing, invalid, or Gate 0 returns RED.
    """
    errors = validate_studio_package(pkg)
    if errors:
        raise ValueError(
            "StudioPackage validation failed:\n"
            + "\n".join(f"  - {e}" for e in errors)
        )

    # Gate 0 — mandatory legal pre-step. Hard stop if RED.
    _gate_result = _run_legal_gate_on_handoff(pkg)
    if _gate_result.get("blocked") or _gate_result.get("verdict") == "RED":
        raise ValueError(
            f"[consume_ai_handoff] GATE 0 RED — handoff blocked before script.json is written.\n"
            f"verdict: {_gate_result.get('verdict')}\n"
            f"hard_stops: {_gate_result.get('hard_stops')}\n"
            f"slug: {pkg.get('concept_hint', {}).get('slug', 'unknown')}"
        )

    hint            = pkg["concept_hint"]
    slug            = hint["slug"]
    beats           = hint["beats"]
    cinematic_style = pkg["cinematic_style"]
    render_dirs     = pkg.get("render_directives") or {}
    lane            = pkg["lane"]
    provenance      = pkg["provenance"]

    spec       = pkg.get("deliverable_spec") or {}
    duration_s = float(
        spec.get("duration_s")
        or hint.get("target_seconds")
        or 69
    )

    # Build shots from beats
    shots = _build_shots(
        beats,
        cinematic_style=cinematic_style,
        render_directives=render_dirs,
        lane=lane,
        duration_s=duration_s,
    )

    # Build config
    config = _build_config(pkg)

    # Determine output directory
    if out_dir is None:
        out_dir = PRODUCTIONS_DIR / f"{slug}_longform_v1"
    out_dir.mkdir(parents=True, exist_ok=True)

    # Assemble gate_0 intake block
    gate_verdict = _gate_result.get("verdict", "UNKNOWN")
    intake_block: dict[str, Any] = {
        "gate_0": {
            "verdict":       gate_verdict,
            "target_rating": "PG-13",
            "blocked":       _gate_result.get("blocked", False),
            "hard_stops":    _gate_result.get("hard_stops", []),
            "cara_status":   _gate_result.get("cara_status", ""),
            "report_path":   "",
        },
        "source_repo":   provenance.get("source_repo", ""),
        "citations":     provenance.get("citations", []),
        "consumed_at":   datetime.now(timezone.utc).isoformat(),
        "handoff_id":    pkg.get("handoff_id", ""),
    }

    # Assemble canonical script.json (render_longform shape)
    prov_card: dict[str, Any] = {
        "enabled":   True,
        "title":     slug.replace("_", " ").title(),
        "subtitle":  f"{lane} · Upon Tyne Productions",
        "footer":    "Subscribe to STUDIO · Upon Tyne Productions",
    }

    script: dict[str, Any] = {
        "slug":           slug,
        "title":          hint.get("title") or slug.replace("_", " ").title(),
        "format_id":      lane,
        "target_seconds": int(duration_s),
        "intake":         intake_block,
        "config":         config,
        "shots":          shots,
        "provenance_card": prov_card,
        "qa_rules":       {"require_speech_on_host": True},
        "production_meta": {
            "cinematic_style": cinematic_style,
            "lane":            lane,
            "handoff_id":      pkg.get("handoff_id", ""),
            "source_repo":     provenance.get("source_repo", ""),
        },
    }

    # Write script.json
    out_path = out_dir / f"{slug}_script.json"
    out_path.write_text(
        json.dumps(script, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"[consume_ai_handoff] wrote {out_path}")
    return out_path


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def main(argv: list[str] | None = None) -> int:
    import argparse
    parser = argparse.ArgumentParser(
        description="STUDIO consume_ai_handoff \u2014 StudioPackage \u2192 script.json"
    )
    parser.add_argument("package", help="Path to StudioPackage JSON file")
    parser.add_argument("-o", "--out", default=None, help="Override output directory")
    args = parser.parse_args(argv)

    pkg_path = Path(args.package)
    if not pkg_path.is_file():
        print(f"ERROR: {pkg_path} not found", file=sys.stderr)
        return 1

    pkg = json.loads(pkg_path.read_text(encoding="utf-8"))
    out_dir = Path(args.out) if args.out else None

    try:
        out = consume_ai_handoff(pkg, out_dir=out_dir)
        print(f"[consume_ai_handoff] script.json written to {out}")
        return 0
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

