#!/usr/bin/env python3
"""STUDIO new-production intake flow.

concept  ->  Gate 0 legal (mandatory)  ->  actor (Casting Bible)  +  format (#98)
         +   set/style (#99 Set/Style libraries)  ->  canonical render_longform script.json

Gate 0 runs on every intake (``artifacts/legal/legal_gate.py`` v1.2). RED blocks the run
and emits no script. YELLOW/COUNSEL stamp ``requires_human_signoff`` for render.

This is the implementation the locked libraries reference in their `usage` fields:

    Production_Templates_v1.json:
        "Select format via concept_selector or explicit format_id.
         Instantiate with production_templates.build_longform_script()."

It reads only the locked v1.0 libraries (never mutates them) and emits a script.json
that `DAVID/scripts/render_longform.py` accepts as its canonical shape
(detected by the presence of both `config` and `shots`).

Pure stdlib. No network, no third-party deps.

CLI
---
    # From a concept file:
    python production_intake.py concept.json
    python production_intake.py concept.json -o ../../DAVID/scripts/longform_scripts/foo_script.json

    # Quick one-off from flags (uses format defaults + placeholder beats):
    python production_intake.py --slug my_short --format documentary-host --actor David-001

The emitted file can be validated/normalized without any API calls:

    python DAVID/scripts/render_longform.py <emitted_script.json> --script-only
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Optional

# --------------------------------------------------------------------------- #
# Paths — resolved relative to this file so the module is location-stable.
# --------------------------------------------------------------------------- #
PIPELINE_DIR = Path(__file__).resolve().parent           # .../STUDIO/Pipeline
STUDIO_DIR = PIPELINE_DIR.parent                         # .../STUDIO
ROOT = STUDIO_DIR.parent                                 # .../Grok Projects

SET_LIBRARY = PIPELINE_DIR / "Set_Library_v1.json"               # #99
STYLE_LIBRARY = PIPELINE_DIR / "Style_Library_v1.json"           # #99
FORMAT_LIBRARY = PIPELINE_DIR / "Production_Templates" / "Production_Templates_v1.json"  # #98
CASTING_REGISTRY = STUDIO_DIR / "Cast" / "Casting_Bible" / "registry" / "casting_registry.json"
CONCEPTS_DIR = PIPELINE_DIR / "Concepts"
LEGAL_GATE_DIR = ROOT / "artifacts" / "legal"

SYNTHETIC_GUARD = "synthetic host only"
SYNTHETIC_TALENT_GUARD = "synthetic talent only"
GATE_EXIT_RED = 2
GATE_EXIT_SIGNOFF_REQUIRED = 3

# Brief compliance phrase — never use substring ``minor`` (CARA false-positive).
ADULT_CAST_PHRASE = "adult cast only (21+)"


# --------------------------------------------------------------------------- #
# Library loading
# --------------------------------------------------------------------------- #
def _load_json(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise FileNotFoundError(f"Required library not found: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def _import_legal_gate():
    """Load legal_gate v1.2 from artifacts (stdlib-only intake stays dep-free otherwise)."""
    if str(LEGAL_GATE_DIR) not in sys.path:
        sys.path.insert(0, str(LEGAL_GATE_DIR))
    from legal_gate import LegalGate  # noqa: WPS433

    return LegalGate


def _sanitize_gate_brief(text: str) -> str:
    """Replace legacy minor-phrasing with Gate 0 / CARA-safe adult-cast wording."""
    import re

    text = re.sub(r"\bno minors?\b", ADULT_CAST_PHRASE, text, flags=re.I)
    text = re.sub(r"\bzero minors?\b", ADULT_CAST_PHRASE, text, flags=re.I)
    return text


def _concept_brief_path(concept: dict[str, Any]) -> Optional[Path]:
    explicit = concept.get("gate_brief") or concept.get("brief_file")
    if explicit:
        p = Path(explicit)
        return p if p.is_absolute() else (CONCEPTS_DIR / p)
    slug = concept.get("slug")
    if slug:
        candidate = CONCEPTS_DIR / f"{slug}_brief.txt"
        if candidate.is_file():
            return candidate
    return None


def _gate_channels(concept: dict[str, Any]) -> list[str]:
    gate = concept.get("gate_0") or {}
    raw = gate.get("channels") or concept.get("channels") or ["social"]
    if isinstance(raw, str):
        return [c.strip() for c in raw.split(",") if c.strip()]
    return [str(c).strip() for c in raw if str(c).strip()]


def _gate_rating(concept: dict[str, Any], fmt: dict[str, Any]) -> str:
    gate = concept.get("gate_0") or {}
    return str(
        gate.get("rating")
        or concept.get("target_rating")
        or fmt.get("default_rating")
        or "PG-13"
    )


def build_gate_brief_text(
    concept: dict[str, Any],
    *,
    actor: Optional[dict[str, Any]],
    actor_id: Optional[str],
    fmt: dict[str, Any],
    format_id: str,
) -> str:
    """Compose Gate 0 brief text; prefer ``{slug}_brief.txt`` when present."""
    path = _concept_brief_path(concept)
    if path:
        return _sanitize_gate_brief(path.read_text(encoding="utf-8"))

    lines = [
        f"Project: {concept.get('slug', 'untitled')}",
        f"Title: {concept.get('title', '')}",
        f"Format: {format_id}",
        f"Rating target: {_gate_rating(concept, fmt)}",
        f"Channels: {', '.join(_gate_channels(concept))}",
    ]
    if actor:
        lines.append(
            f"Performer: {actor['actor_id']} ({actor.get('age_locked')}-year-old synthetic "
            f"{actor.get('gender', 'performer')}, {actor.get('stage_name', '')}). "
            f"Casting Bible synthetic: true, real_person_likeness: false."
        )
    elif actor_id:
        lines.append(f"Performer anchor: {actor_id}")
    lines.append(f"Content: {concept.get('logline') or concept.get('summary') or concept.get('title', 'SFW production')}")
    lines.append(
        "AI disclosure: synthetic performer labeled in provenance card and platform metadata."
    )
    lines.append(
        f"Synthetic fictional performer only. No celebrity mimicry. {ADULT_CAST_PHRASE}."
    )
    brand = concept.get("brand") or {}
    if brand.get("legal_line"):
        lines.append(f"Brand legal: {brand['legal_line']}")
    music = (concept.get("gate_0") or {}).get("music_plan") or concept.get("music_plan")
    if music:
        lines.append(f"Music plan: {music}")
    return "\n".join(lines)


def run_gate_0(
    concept: dict[str, Any],
    *,
    actor: Optional[dict[str, Any]],
    actor_id: Optional[str],
    fmt: dict[str, Any],
    format_id: str,
) -> dict[str, Any]:
    """Run mandatory Gate 0; save report; return stamp for intake."""
    brief = build_gate_brief_text(
        concept, actor=actor, actor_id=actor_id, fmt=fmt, format_id=format_id
    )
    LegalGate = _import_legal_gate()
    gate = LegalGate()
    result = gate.review(
        brief,
        concept["slug"],
        target_rating=_gate_rating(concept, fmt),
        channels=_gate_channels(concept),
        has_performers=bool(actor or actor_id or fmt.get("identity_anchor")),
    )
    report_path = gate.save_report(result, brief)
    try:
        rel_report = str(report_path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        rel_report = str(report_path)

    blocked = result.verdict == "RED"
    requires_signoff = result.verdict in ("YELLOW", "COUNSEL")

    return {
        "version": "1.2",
        "verdict": result.verdict,
        "blocked": blocked,
        "requires_human_signoff": requires_signoff,
        "human_signoff": bool((concept.get("gate_0") or {}).get("human_signoff")),
        "target_rating": result.target_rating,
        "channels": result.channels,
        "report_path": rel_report,
        "checklist_domains": result.checklist_domains,
        "hard_stops": result.hard_stops,
        "counsel_flags": result.counsel_flags,
        "distribution_flags": result.distribution_flags,
        "warnings": result.warnings,
        "rating_flags": result.rating_flags,
        "cara_status": result.cara_status,
        "notes": result.notes,
        "brief_source": str(_concept_brief_path(concept) or "composed"),
    }


def load_libraries() -> dict[str, Any]:
    """Load the locked format (#98), set/style (#99), and casting libraries."""
    return {
        "formats": _load_json(FORMAT_LIBRARY),
        "sets": _load_json(SET_LIBRARY),
        "styles": _load_json(STYLE_LIBRARY),
        "casting": _load_json(CASTING_REGISTRY),
    }


# --------------------------------------------------------------------------- #
# Selectors
# --------------------------------------------------------------------------- #
def concept_selector(concept: dict[str, Any], libs: dict[str, Any]) -> str:
    """Pick a format_id from a free-form concept when none is supplied.

    Honors an explicit `format_id`; otherwise keyword-matches the concept's
    text/tags against each format's name + description. Falls back to the
    first 'documentary-*' format, else the first format in the library.
    """
    formats: dict[str, Any] = libs["formats"]["formats"]

    explicit = concept.get("format_id")
    if explicit:
        if explicit not in formats:
            raise KeyError(
                f"format_id '{explicit}' not in Production_Templates "
                f"(available: {', '.join(formats)})"
            )
        return explicit

    haystack = " ".join(
        str(concept.get(k, ""))
        for k in ("title", "logline", "summary", "brief", "topic")
    ).lower()
    haystack += " " + " ".join(str(t).lower() for t in concept.get("tags", []))

    best_id, best_score = None, 0
    for fid, fmt in formats.items():
        terms = set()
        for field in ("name", "description"):
            terms.update(str(fmt.get(field, "")).lower().replace("/", " ").split())
        terms.update(fid.replace("-", " ").split())
        score = sum(1 for t in terms if len(t) > 3 and t in haystack)
        if score > best_score:
            best_id, best_score = fid, score

    if best_id:
        return best_id
    for fid in formats:
        if fid.startswith("documentary"):
            return fid
    return next(iter(formats))


def select_format(format_id: str, libs: dict[str, Any]) -> dict[str, Any]:
    formats = libs["formats"]["formats"]
    if format_id not in formats:
        raise KeyError(f"Unknown format_id '{format_id}'")
    return formats[format_id]


def select_set_style(
    set_id: Optional[str], style_id: Optional[str], fmt: dict[str, Any], libs: dict[str, Any]
) -> tuple[str, dict[str, Any], str, dict[str, Any]]:
    """Resolve set + style, defaulting to the format's locked pairing."""
    set_id = set_id or fmt.get("default_set")
    style_id = style_id or fmt.get("default_style")

    sets = libs["sets"]["sets"]
    styles = libs["styles"]["styles"]
    if set_id not in sets:
        raise KeyError(f"Unknown set_id '{set_id}' (available: {', '.join(sets)})")
    if style_id not in styles:
        raise KeyError(f"Unknown style_id '{style_id}' (available: {', '.join(styles)})")
    return set_id, sets[set_id], style_id, styles[style_id]


def select_actor(
    actor_id: Optional[str], fmt: dict[str, Any], libs: dict[str, Any]
) -> Optional[dict[str, Any]]:
    """Resolve a Casting Bible actor.

    `actor_id` may be the registry handle ('David-001') or the bare anchor the
    format declares ('@David-001'). Returns None when the actor is not in the
    registry (e.g. the DAVID host anchor, whose identity lives in an identity
    lock JSON rather than the synthetic actors_roster).
    """
    wanted = (actor_id or fmt.get("identity_anchor") or "").lstrip("@")
    if not wanted:
        return None
    for actor in libs["casting"]["actors"]:
        if actor.get("actor_id", "").lower() == wanted.lower():
            return actor
    return None


# --------------------------------------------------------------------------- #
# Prompt composition  (follows formats.compose_contract.video_prompt_order)
# --------------------------------------------------------------------------- #
def _ensure_guard(voice_suffix: str, guard: str) -> str:
    return voice_suffix if "synthetic" in voice_suffix.lower() else f"{voice_suffix}, {guard}"


def _identity_lock_text(
    fmt: dict[str, Any], actor: Optional[dict[str, Any]], actor_id: Optional[str]
) -> str:
    """Continuity lock prefix for the talent.

    Uses the format's verbatim anchor lock when the chosen actor *is* the
    format anchor; otherwise synthesizes a lock from the actor's locked
    attributes, leading with numerical age per Age_Policy_Locked.md.
    """
    anchor = (fmt.get("identity_anchor") or "").lstrip("@").lower()
    chosen = (actor_id or anchor or "").lstrip("@").lower()
    if fmt.get("identity_continuity_lock") and chosen == anchor:
        return fmt["identity_continuity_lock"]

    if actor:
        handle = actor["actor_id"]
        age = actor.get("age_locked")
        ethnicity = actor.get("ethnicity", "")
        gender = actor.get("gender", "")
        desc = " ".join(p for p in [f"{age}-year-old" if age else "", ethnicity, gender] if p)
        return (
            f"CONTINUITY LOCK @{handle}: identical {desc} performer ({actor.get('stage_name','')}), "
            "same face, wardrobe, hair, eye-line and blocking — "
            "seamless continuation of prior take, zero jump cut."
        )

    # Fall back to the format anchor lock even if names didn't match.
    return fmt.get(
        "identity_continuity_lock",
        f"CONTINUITY LOCK @{chosen or 'Talent-001'}: identical performer, same wardrobe, "
        "hair, eye-line — seamless continuation of prior take, zero jump cut.",
    )


def compose_video_prompt(
    *,
    identity_lock: str,
    action_prompt: str,
    set_obj: dict[str, Any],
    style_obj: dict[str, Any],
    speech_text: str,
    voice_suffix: str,
    speaking: bool,
) -> str:
    """Assemble one shot's video_prompt in the locked compose order:

    {identity}{set.continuity}{style.continuity}{action}{set.lighting}{style.lighting}
    {set.color_guard}{style.color_guard}{style.lens_motion}
    [Lip-synced, delivers: "<speech>" <voice>] {style.end_guard}
    """
    parts: list[str] = [
        identity_lock,
        set_obj.get("continuity_lock", ""),
        style_obj.get("continuity_lock", ""),
        action_prompt,
        set_obj.get("lighting_lock", ""),
        style_obj.get("lighting_lock", ""),
        set_obj.get("color_guard", ""),
        style_obj.get("color_guard", ""),
        style_obj.get("lens_motion", ""),
    ]
    if speaking and speech_text:
        parts.append(f'Lip-synced, delivers: "{speech_text}" {voice_suffix}.')
    parts.append(style_obj.get("end_guard", ""))
    return " ".join(p.strip() for p in parts if p and p.strip())


# --------------------------------------------------------------------------- #
# Shot assembly
# --------------------------------------------------------------------------- #
# Must match Master Prompt Bible §10 speaking roles.
_SPEAKING_ROLES = {
    "host",
    "character",
    "companion",
    "presenter",
    "host_pie",
    "talent",
    "dialogue",
    "vo",
    "voiceover",
}


def _is_speaking(role: str) -> bool:
    return role.lower() in _SPEAKING_ROLES


def _build_shots(
    concept: dict[str, Any],
    fmt: dict[str, Any],
    set_obj: dict[str, Any],
    style_obj: dict[str, Any],
    identity_lock: str,
    voice_suffix: str,
) -> list[dict[str, Any]]:
    """Merge concept beats over the format's shot blueprints.

    - If the concept supplies `beats`, each beat is matched to a blueprint by
      `id` (falling back to positional order) so writers only provide speech +
      any overrides; blueprint supplies duration/role/camera/action defaults.
    - If no beats are supplied, the blueprints are emitted with their
      speech placeholders so the file is render-ready after a copy pass.
    """
    blueprints: list[dict[str, Any]] = fmt.get("shot_blueprints", [])
    beats: list[dict[str, Any]] = concept.get("beats", [])

    by_id = {b["id"]: b for b in beats if "id" in b}
    rows: list[dict[str, Any]] = []

    if beats and not blueprints:
        rows = list(beats)
    else:
        for idx, bp in enumerate(blueprints):
            beat = by_id.get(bp["id"]) or (beats[idx] if idx < len(beats) and "id" not in beats[idx] else {})
            rows.append({**bp, **beat})
        # Any extra beats beyond the blueprint count get appended verbatim.
        for extra in beats[len(blueprints):]:
            if extra.get("id") not in {r["id"] for r in rows}:
                rows.append(extra)

    shots: list[dict[str, Any]] = []
    t = 0
    for i, row in enumerate(rows, 1):
        role = row.get("role", "host")
        duration = int(row.get("duration", 8))
        action = row.get("action") or row.get("action_template") or "Performer in frame, motivated camera."
        camera = row.get("camera")
        if camera:
            action = f"{action} Camera: {camera}."
        speech = row.get("speech_text") or row.get("speech") or row.get("speech_placeholder", "")
        speaking = _is_speaking(role)

        shot: dict[str, Any] = {
            "id": row.get("id", f"{i:02d}_shot"),
            "duration": duration,
            "t_start": t,
            "t_end": t + duration,
            "role": role,
            "video_prompt": compose_video_prompt(
                identity_lock=identity_lock,
                action_prompt=action,
                set_obj=set_obj,
                style_obj=style_obj,
                speech_text=speech,
                voice_suffix=voice_suffix,
                speaking=speaking,
            ),
        }
        if speaking:
            shot["speech_text"] = speech
        if row.get("speech_ipa"):
            shot["speech_ipa"] = row["speech_ipa"]
        if row.get("on_screen"):
            shot["on_screen"] = row["on_screen"]
        if row.get("on_screen_labels"):
            shot["on_screen_labels"] = row["on_screen_labels"]
        shots.append(shot)
        t += duration

    return shots


# --------------------------------------------------------------------------- #
# Config assembly
# --------------------------------------------------------------------------- #
def _build_config(
    concept: dict[str, Any],
    fmt: dict[str, Any],
    format_id: str,
    set_obj: dict[str, Any],
    actor: Optional[dict[str, Any]],
    voice_suffix: str,
    libs: dict[str, Any],
) -> dict[str, Any]:
    cfg: dict[str, Any] = {
        "model_video": concept.get("model_video", "grok-imagine-video-1.5"),
        "resolution": concept.get("resolution", "720p"),
        "aspect_ratio": concept.get("aspect_ratio", "16:9"),
        "voice_suffix": voice_suffix,
    }

    pairings = libs["styles"].get("recommended_pairings", {})
    # Identity lock JSON only exists for the DAVID host anchor today.
    identity_lock = concept.get("identity_lock")
    if not identity_lock and format_id == "documentary-host":
        identity_lock = pairings.get("DAVID_host", {}).get(
            "identity_lock", "productions/host_identity_v1/david_identity_lock.json"
        )
        # render_longform resolves DAVID-relative paths; strip the DAVID/ prefix.
        identity_lock = identity_lock.replace("DAVID/", "")
    if identity_lock:
        cfg["identity_lock"] = identity_lock
    else:
        cfg["use_identity_lock"] = False

    avatar = concept.get("avatar_reference")
    if not avatar and actor:
        avatar = actor.get("reference_image_primary")
    if not avatar and format_id == "documentary-host":
        avatar = "productions/host_identity_v1/references/david_avatar_reference.jpg"
    if avatar:
        cfg["avatar_reference"] = avatar

    if set_obj.get("reference_file"):
        cfg["set_reference"] = set_obj["reference_file"]

    # Seamless: library defaults, with host audio/lamp locks for the host format,
    # then any concept overrides on top.
    seamless = dict(
        libs["formats"]["compose_contract"].get("seamless_defaults", {})
    )
    if format_id == "documentary-host":
        seamless.update(
            {
                "lamp_lock": True,
                "glasses_lock": True,
                "loudnorm": True,
                "pin_audio_sync": True,
                "reground_interval": fmt.get("guardrails") and 2 or 2,
                "magenta_clamp": True,
            }
        )
    seamless.update(concept.get("seamless", {}))
    cfg["seamless"] = seamless

    if concept.get("compare_v1"):
        cfg["compare_v1"] = concept["compare_v1"]

    return cfg


# --------------------------------------------------------------------------- #
# Provenance card
# --------------------------------------------------------------------------- #
def _build_provenance(concept: dict[str, Any], fmt: dict[str, Any]) -> dict[str, Any]:
    template = dict(fmt.get("provenance_card", {"enabled": False}))
    brand = concept.get("brand", {})
    overrides = concept.get("provenance_card", {})

    # Substitute brand placeholders ({brand_title} etc.) used by the templates.
    subs = {
        "brand_title": brand.get("title", concept.get("title", "")),
        "brand_subtitle": brand.get("subtitle", ""),
        "cta": brand.get("cta", ""),
        "title": concept.get("title", ""),
        "subtitle": brand.get("subtitle", ""),
        "credit_line": brand.get("credit_line", brand.get("cta", "")),
    }
    for key, val in list(template.items()):
        if isinstance(val, str) and val.startswith("{") and val.endswith("}"):
            template[key] = subs.get(val.strip("{}"), "")
    template.update(overrides)
    return template


class Gate0BlockedError(Exception):
    """Gate 0 RED — intake must not emit a script."""

    def __init__(self, stamp: dict[str, Any]) -> None:
        self.stamp = stamp
        super().__init__(stamp.get("verdict", "RED"))


# --------------------------------------------------------------------------- #
# Public entry point
# --------------------------------------------------------------------------- #
def build_longform_script(
    concept: dict[str, Any], libs: Optional[dict[str, Any]] = None
) -> dict[str, Any]:
    """Turn a concept dict into a canonical render_longform script.json dict.

    Concept schema (all but `slug` optional; sensible format defaults fill the rest)::

        {
          "slug": "david_why_latin_60s",          # required
          "title": "Why Latin Never Really Died",
          "format_id": "documentary-host",         # optional -> concept_selector
          "actor_id": "David-001",                 # optional -> format anchor
          "set_id": "@Set-Archive-001",            # optional -> format default
          "style_id": "@Style-Documentary-Prestige-001",
          "target_seconds": 69,
          "tags": ["history", "language"],
          "brand": {"title": "...", "subtitle": "...", "cta": "..."},
          "seamless": { ... overrides ... },
          "beats": [
            {"id": "01_cold_open", "speech_text": "...", "on_screen": "..."},
            ...
          ]
        }
    """
    if "slug" not in concept or not concept["slug"]:
        raise ValueError("concept must include a non-empty 'slug'")
    libs = libs or load_libraries()

    format_id = concept_selector(concept, libs)
    fmt = select_format(format_id, libs)

    actor_id = concept.get("actor_id")
    actor = select_actor(actor_id, fmt, libs)

    gate_stamp = run_gate_0(
        concept, actor=actor, actor_id=actor_id, fmt=fmt, format_id=format_id
    )
    if gate_stamp["blocked"]:
        raise Gate0BlockedError(gate_stamp)

    set_id, set_obj, style_id, style_obj = select_set_style(
        concept.get("set_id"), concept.get("style_id"), fmt, libs
    )

    # Voice suffix: actor voice for non-anchor casting; else the format voice.
    anchor = (fmt.get("identity_anchor") or "").lstrip("@").lower()
    is_anchor = (actor_id or anchor or "").lstrip("@").lower() == anchor
    if actor and not is_anchor and actor.get("voice_spec", {}).get("prompt_suffix"):
        voice_suffix = _ensure_guard(
            actor["voice_spec"]["prompt_suffix"], SYNTHETIC_TALENT_GUARD
        )
    else:
        voice_suffix = _ensure_guard(
            concept.get("voice_suffix", fmt.get("voice_suffix", "")), SYNTHETIC_GUARD
        )

    identity_lock = _identity_lock_text(fmt, actor, actor_id)

    shots = _build_shots(concept, fmt, set_obj, style_obj, identity_lock, voice_suffix)
    config = _build_config(concept, fmt, format_id, set_obj, actor, voice_suffix, libs)

    target = concept.get("target_seconds")
    if target is None:
        ts = fmt.get("target_seconds", {})
        target = ts.get("default") if isinstance(ts, dict) else ts

    script: dict[str, Any] = {
        "slug": concept["slug"],
        "title": concept.get("title", concept["slug"]),
        "format_id": format_id,
        "target_seconds": target,
        "intake": {
            "format_id": format_id,
            "actor_id": actor["actor_id"] if actor else (actor_id or fmt.get("identity_anchor")),
            "set_id": set_id,
            "style_id": style_id,
            "source": "STUDIO/Pipeline/production_intake.py",
            "gate_0": gate_stamp,
            "libraries": {
                "formats": "Production_Templates_v1.json (#98)",
                "sets": "Set_Library_v1.json (#99)",
                "styles": "Style_Library_v1.json (#99)",
                "casting": "Casting_Bible/registry/casting_registry.json",
            },
        },
        "config": config,
        "shots": shots,
        "provenance_card": _build_provenance(concept, fmt),
        "qa_rules": fmt.get(
            "qa_rules",
            {"require_identity_lock": True, "require_synthetic_guard": True, "min_shots": 1},
        ),
    }
    return script


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #
def _default_output_path(slug: str, format_id: str) -> Path:
    """Mirror render_longform's longform_scripts/ convention for inputs."""
    return ROOT / "DAVID" / "scripts" / "longform_scripts" / f"{slug}_script.json"


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="STUDIO new-production intake: concept -> canonical render_longform script.json"
    )
    parser.add_argument("concept", nargs="?", type=Path, help="Path to a concept JSON file")
    parser.add_argument("-o", "--out", type=Path, help="Output script.json path")
    parser.add_argument("--slug", help="Slug (overrides concept / required if no concept file)")
    parser.add_argument("--title", help="Title override")
    parser.add_argument("--format", dest="format_id", help="format_id (#98); skips concept_selector")
    parser.add_argument("--actor", dest="actor_id", help="Casting Bible actor_id")
    parser.add_argument("--set", dest="set_id", help="set_id (#99)")
    parser.add_argument("--style", dest="style_id", help="style_id (#99)")
    parser.add_argument("--print", action="store_true", help="Print to stdout instead of writing")
    args = parser.parse_args(argv)

    concept: dict[str, Any] = {}
    if args.concept:
        concept = json.loads(Path(args.concept).read_text(encoding="utf-8"))
    for key, val in (
        ("slug", args.slug),
        ("title", args.title),
        ("format_id", args.format_id),
        ("actor_id", args.actor_id),
        ("set_id", args.set_id),
        ("style_id", args.style_id),
    ):
        if val:
            concept[key] = val

    if not concept.get("slug"):
        parser.error("a 'slug' is required (in the concept file or via --slug)")

    try:
        script = build_longform_script(concept)
    except Gate0BlockedError as exc:
        stamp = exc.stamp
        print(f"\n🛑 GATE 0 RED — intake blocked (no script written)")
        print(f"   Report: {stamp.get('report_path')}")
        for msg in stamp.get("hard_stops", []):
            print(f"   HARD STOP: {msg}")
        return GATE_EXIT_RED

    gate = script["intake"]["gate_0"]
    payload = json.dumps(script, indent=2, ensure_ascii=False)

    if args.print:
        print(payload)
        _print_gate_summary(gate)
        return 0

    out = args.out or _default_output_path(script["slug"], script["format_id"])
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(payload, encoding="utf-8")

    n_speaking = sum(1 for s in script["shots"] if "speech_text" in s)
    print(f"Wrote {out}")
    print(
        f"  format={script['format_id']}  set={script['intake']['set_id']}  "
        f"style={script['intake']['style_id']}  actor={script['intake']['actor_id']}"
    )
    print(f"  shots={len(script['shots'])} ({n_speaking} speaking)  target={script['target_seconds']}s")
    _print_gate_summary(gate)
    print("Next:  python DAVID/scripts/render_longform.py "
          f"{out} --script-only   # validate, no API")
    if gate.get("requires_human_signoff") and not gate.get("human_signoff"):
        return GATE_EXIT_SIGNOFF_REQUIRED
    return 0


def _print_gate_summary(gate: dict[str, Any]) -> None:
    icon = {"GREEN": "✅", "YELLOW": "⚠️", "COUNSEL": "⚖️", "RED": "🛑"}.get(
        gate.get("verdict", "?"), "?"
    )
    print(f"  gate_0={icon} {gate.get('verdict')}  report={gate.get('report_path')}")
    if gate.get("requires_human_signoff") and not gate.get("human_signoff"):
        print("  ⚠️  Human Gate 0 sign-off required before render (YELLOW/COUNSEL).")
    if gate.get("checklist_domains"):
        domains = ", ".join(f"{k}={v}" for k, v in gate["checklist_domains"].items())
        print(f"  checklist: {domains}")


if __name__ == "__main__":
    sys.exit(main())
