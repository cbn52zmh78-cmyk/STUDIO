#!/usr/bin/env python3
"""STUDIO new-production intake flow.

concept  ->  Gate 0 legal (mandatory)  ->  actor (Casting Bible)  +  format (#98)
         +   set/style (#99 Set/Style libraries)  ->  canonical render_longform script.json

Gate 0 runs on every intake (``artifacts/legal/legal_gate.py`` v1.3). RED blocks the run
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

if str(PIPELINE_DIR) not in sys.path:
    sys.path.insert(0, str(PIPELINE_DIR))

from shot_duration import apply_duration_clamp_to_shots, should_clamp_shot_durations  # noqa: E402
from science_field import enrich_science_subject  # noqa: E402

# --------------------------------------------------------------------------- #
# QA Gate 0 — reasoning-backed content check on incoming packets               #
# Imported lazily so the module stays dep-free when QA is unavailable.         #
# Set _QA_GATE_SKIP = True (via --skip-qa-gate flag) for emergency override.   #
# --------------------------------------------------------------------------- #
_QA_FEDERATION_DIR = ROOT / "AI" / "federation"
_QA_AVAILABLE = False
_qa_import_err: str = ""
try:
    if str(_QA_FEDERATION_DIR) not in sys.path:
        sys.path.insert(0, str(_QA_FEDERATION_DIR))
    from qa_gate import qa_check as _qa_check  # noqa: E402
    _QA_AVAILABLE = True
except ImportError as _qe:
    _qa_import_err = str(_qe)

_EDITING_QA_AVAILABLE = False
_editing_qa_import_err: str = ""
try:
    _EDITING_FED_DIR = ROOT / "AI" / "Federations" / "Editing_Federation"
    if str(_EDITING_FED_DIR) not in sys.path:
        sys.path.insert(0, str(_EDITING_FED_DIR))
    from editing_federation_dispatcher import EditingFederationDispatcher as _EFDispatcher
    _EDITING_QA_AVAILABLE = True
except ImportError as _efe:
    _editing_qa_import_err = str(_efe)

_QA_GATE_SKIP: bool = False   # flipped to True by --skip-qa-gate at parse time
_EDITING_QA_GATE_ACTIVE: bool = False   # flipped to True by --editing-qa at parse time


def _run_qa_gate_0(concept: dict[str, Any], brief: str) -> dict[str, Any]:
    """Run qa_check on the incoming concept brief at Gate 0.

    Returns a dict with keys: gate, safe_to_send, issues, verdict, summary.
    When QA is unavailable or --skip-qa-gate is active, returns a pass-through
    result so the rest of the intake pipeline is unaffected.
    """
    if _QA_GATE_SKIP:
        return {
            "gate": "SKIPPED", "safe_to_send": True,
            "issues": [], "verdict": "SKIPPED",
            "summary": "QA Gate 0 skipped via --skip-qa-gate flag.",
        }
    if not _QA_AVAILABLE:
        print(
            f"[WARN] Gate 0 QA unavailable ({_qa_import_err}) — skipping QA check.",
            file=sys.stderr,
        )
        return {
            "gate": "UNAVAILABLE", "safe_to_send": True,
            "issues": [], "verdict": "UNAVAILABLE",
            "summary": "QA gate module not importable.",
        }

    subject = concept.get("slug") or concept.get("title") or "incoming concept"
    facts: list[str] = []
    hf = concept.get("historical_figure") or {}
    ss = concept.get("science_subject") or {}
    ts = concept.get("technical_subject") or {}
    for src in (hf, ss, ts):
        for s in (src.get("sources") or [])[:4]:
            cit = s.get("citation", "")
            if cit:
                facts.append(cit)
    if not facts:
        facts = [brief[:200]]   # fallback: brief excerpt as a fact sentinel

    try:
        result = _qa_check(
            content=brief,
            content_type="general",
            subject=subject,
            facts=facts,
            mode="draft_critique",   # fast 3-pass for Gate 0 turnaround
        )
    except Exception as exc:
        print(f"[WARN] QA Gate 0 exception: {exc}", file=sys.stderr)
        return {
            "gate": "YELLOW", "safe_to_send": True,
            "issues": [str(exc)], "verdict": "PARTIAL",
            "summary": f"QA gate raised exception: {exc}",
        }

    if result["gate"] == "RED":
        # RED blocks: log detailed error and re-raise as Gate0BlockedError later
        print(
            f"[ERROR] QA Gate 0 RED for '{subject}' — {result['summary']}",
            file=sys.stderr,
        )
        for issue in result["issues"][:5]:
            print(f"  [!] {issue}", file=sys.stderr)
    elif result["gate"] == "YELLOW":
        print(
            f"[WARN] QA Gate 0 YELLOW for '{subject}' — {result['summary']}",
            file=sys.stderr,
        )
    return result

SET_LIBRARY = PIPELINE_DIR / "Set_Library_v1.json"               # #99
STYLE_LIBRARY = PIPELINE_DIR / "Style_Library_v1.json"           # #99
FORMAT_LIBRARY = PIPELINE_DIR / "Production_Templates" / "Production_Templates_v1.json"  # #98
NEUTRAL_LIGHTING_SPEC = PIPELINE_DIR / "neutral_lighting_prompt_spec_v1.json"  # #199 T4
CASTING_REGISTRY = STUDIO_DIR / "Cast" / "Casting_Bible" / "registry" / "casting_registry.json"
CONCEPTS_DIR = PIPELINE_DIR / "Concepts"
LEGAL_GATE_DIR = ROOT / "artifacts" / "legal"
EDITORIAL_ENGINE_DIR = ROOT / "Scribe" / "SCRIBE"      # #212 editorial engine

SYNTHETIC_GUARD = "synthetic host only"
SYNTHETIC_TALENT_GUARD = "synthetic talent only"
GATE_EXIT_RED = 2
GATE_EXIT_SIGNOFF_REQUIRED = 3

# Brief compliance phrase — never use substring ``minor`` (CARA false-positive).
ADULT_CAST_PHRASE = "adult cast only (21+)"
HISTORICAL_FIGURE_FORMAT = "historical-figure-documentary"
SCIENCE_EXPLAINER_FORMAT = "science-explainer"
TECHNICAL_EXPLAINER_FORMAT = "technical-explainer"
EDITORIAL_FORMAT = "editorial"          # #213 — written client deliverables route to SCRIBE
EDITORIAL_LANE = "editorial"
PERIOD_LINE_SHOT_ID = "04_period_line"
VIZ_PAYOFF_SHOT_ID = "04_visualization_payoff"
DIAGRAM_PAYOFF_SHOT_ID = "04_diagram_payoff"


# --------------------------------------------------------------------------- #
# Library loading
# --------------------------------------------------------------------------- #
def _run_editing_qa_gate(content_str: str, concept: dict) -> dict:
    """Run the Editing Federation dispatcher on intake content after Gate 0.

    Returns a result dict with keys: gate, safe, summary.
    """
    if not _EDITING_QA_AVAILABLE:
        return {
            "gate": "UNAVAILABLE",
            "safe": True,
            "summary": f"Editing QA unavailable: {_editing_qa_import_err}",
        }
    try:
        dispatcher = _EFDispatcher(mode="draft_critique", dry_run=False)
        report = dispatcher.run_all(
            document=content_str,
            format_id=concept.get("format_id", "documentary-host"),
            subject=concept.get("slug", ""),
        )
        return {
            "gate": report.overall_gate,
            "safe": report.overall_gate != "RED",
            "summary": report.summary,
            "results": [r for r in report.results],
        }
    except Exception as exc:
        return {
            "gate": "YELLOW",
            "safe": True,
            "summary": f"Editing QA exception: {exc}",
        }


def _load_json(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise FileNotFoundError(f"Required library not found: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def _import_legal_gate():
    """Load legal_gate v1.5 from artifacts (stdlib-only intake stays dep-free otherwise)."""
    if str(LEGAL_GATE_DIR) not in sys.path:
        sys.path.insert(0, str(LEGAL_GATE_DIR))
    from legal_gate import LegalGate  # noqa: WPS433

    return LegalGate


def _import_historical_figure_gate():
    """Historical Figure Gate constants (#154) — shared with T2 bible validator."""
    if str(LEGAL_GATE_DIR) not in sys.path:
        sys.path.insert(0, str(LEGAL_GATE_DIR))
    from historical_figure_gate import DEATH_YEAR_HARD_CEILING, recency_floor_year  # noqa: WPS433

    return {
        "DEATH_YEAR_HARD_CEILING": DEATH_YEAR_HARD_CEILING,
        "recency_floor_year": recency_floor_year,
    }


def _import_music_clearance():
    artifacts = ROOT / "artifacts"
    if str(artifacts) not in sys.path:
        sys.path.insert(0, str(artifacts))
    from lib.bootstrap import ensure_paths  # noqa: WPS433

    ensure_paths()
    if str(LEGAL_GATE_DIR) not in sys.path:
        sys.path.insert(0, str(LEGAL_GATE_DIR))
    from music_clearance import resolve_music_from_concept  # noqa: WPS433

    return resolve_music_from_concept


def _sanitize_gate_brief(text: str) -> str:
    """Replace legacy minor-phrasing with Gate 0 / CARA-safe adult-cast wording."""
    import re

    text = re.sub(r"\bno minors?\b", ADULT_CAST_PHRASE, text, flags=re.I)
    text = re.sub(r"\bzero minors?\b", ADULT_CAST_PHRASE, text, flags=re.I)
    return text


def _concept_brief_path(
    concept: dict[str, Any], concept_file: Optional[Path] = None
) -> Optional[Path]:
    """Resolve Gate 0 brief file — honors gate_brief, brief_file, brief, or {slug}_brief.txt."""
    explicit = concept.get("gate_brief") or concept.get("brief_file") or concept.get("brief")
    if explicit:
        p = Path(str(explicit))
        if p.is_absolute() and p.is_file():
            return p
        for base in (
            concept_file.parent if concept_file else None,
            CONCEPTS_DIR,
            CONCEPTS_DIR / "dead_languages",
            CONCEPTS_DIR / "astro_mini_slate",
            CONCEPTS_DIR / "chem_physics_mini_slate",
            CONCEPTS_DIR / "molecular_mini_slate",
            CONCEPTS_DIR / "royal_tongues",
        ):
            if base is None:
                continue
            candidate = base / p
            if candidate.is_file():
                return candidate
    slug = concept.get("slug")
    if slug:
        for base in (
            concept_file.parent if concept_file else None,
            CONCEPTS_DIR / "dead_languages",
            CONCEPTS_DIR / "astro_mini_slate",
            CONCEPTS_DIR / "chem_physics_mini_slate",
            CONCEPTS_DIR / "molecular_mini_slate",
            CONCEPTS_DIR / "royal_tongues",
            CONCEPTS_DIR,
        ):
            if base is None:
                continue
            candidate = base / f"{slug}_brief.txt"
            if candidate.is_file():
                return candidate
    return None


def _parse_brief_field(brief: str, label: str) -> Optional[str]:
    for line in brief.splitlines():
        if line.lower().startswith(label.lower()):
            return line.split(":", 1)[1].strip()
    return None


def _gate_channels(concept: dict[str, Any], brief: Optional[str] = None) -> list[str]:
    gate = concept.get("gate_0") or {}
    raw = gate.get("channels") or concept.get("channels")
    if not raw and brief:
        parsed = _parse_brief_field(brief, "Channels")
        if parsed:
            raw = parsed
    if not raw:
        raw = ["social"]
    if isinstance(raw, str):
        return [c.strip() for c in raw.replace("·", ",").split(",") if c.strip()]
    return [str(c).strip() for c in raw if str(c).strip()]


def _gate_rating(concept: dict[str, Any], fmt: dict[str, Any], brief: Optional[str] = None) -> str:
    gate = concept.get("gate_0") or {}
    rating = gate.get("rating") or concept.get("target_rating")
    if not rating and brief:
        parsed = _parse_brief_field(brief, "Rating target")
        if parsed:
            rating = parsed.split()[0]  # "PG" from "PG" or "PG-13 (note)"
    return str(rating or fmt.get("default_rating") or "PG-13")


def build_gate_brief_text(
    concept: dict[str, Any],
    *,
    actor: Optional[dict[str, Any]],
    actor_id: Optional[str],
    fmt: dict[str, Any],
    format_id: str,
    concept_file: Optional[Path] = None,
) -> str:
    """Compose Gate 0 brief text; prefer ``{slug}_brief.txt`` when present."""
    path = _concept_brief_path(concept, concept_file)
    if path:
        return _sanitize_gate_brief(path.read_text(encoding="utf-8"))

    lines = [
        f"Project: {concept.get('slug', 'untitled')}",
        f"Title: {concept.get('title', '')}",
        f"Format: {format_id}",
        f"Rating target: {_gate_rating(concept, fmt, None)}",
        f"Channels: {', '.join(_gate_channels(concept, None))}",
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
    hf = concept.get("historical_figure") or {}
    if hf and format_id == HISTORICAL_FIGURE_FORMAT:
        name = hf.get("name") or hf.get("figure_id", "historical figure")
        lines.append(f"Historical figure: {name}")
        lines.append(f"death_year: {hf.get('death_year')}")
        lines.append(f"Era: {hf.get('era', '')}")
        lines.append(
            "Reconstruction disclosure: AI-rendered likeness is speculative reconstruction "
            "from period art and scholarly sources — not a photographic likeness."
        )
        srcs = hf.get("sources") or []
        if srcs:
            cites = "; ".join(str(s.get("citation", "")) for s in srcs[:4] if s.get("citation"))
            lines.append(f"Sources: {cites}")
        else:
            lines.append("Sources: scholarly sources required at intake.")
        lines.append(
            "Dignity: SFW scholarly portrayal only; no NSFW; no humiliation or anachronistic caricature."
        )
        if hf.get("period_language"):
            lines.append(
                f"Period language beat: {hf['period_language']} — attested/reconstructed labeled on screen."
            )
    ss = concept.get("science_subject") or {}
    if ss and format_id == SCIENCE_EXPLAINER_FORMAT:
        lines.append(f"Science subject: {ss.get('phenomenon') or ss.get('subject_id', 'science episode')}")
        lines.append(f"Domain: {ss.get('domain', '')}")
        if ss.get("field"):
            lines.append(f"Science field: {ss['field']}")
        if ss.get("principle_set"):
            lines.append(f"Principle set: {ss['principle_set']}")
        lines.append(f"subject_id: {ss.get('subject_id', '')}")
        if ss.get("key_measurement"):
            lines.append(f"Key measurement: {ss['key_measurement']}")
        srcs = ss.get("sources") or []
        if srcs:
            cites = "; ".join(str(s.get("citation", "")) for s in srcs[:4] if s.get("citation"))
            lines.append(f"Sources: {cites}")
        lines.append(
            "Scientific visualization @2 payoff — illustrative frames labeled NOT TO SCALE where applicable."
        )
        lines.append(
            "Dignity: SFW scholarly science communication; no medical or legal advice as professional counsel."
        )
    ts = concept.get("technical_subject") or {}
    if ts and format_id == TECHNICAL_EXPLAINER_FORMAT:
        lines.append(f"Technical subject: {ts.get('system') or ts.get('subject_id', 'systems episode')}")
        lines.append(f"Domain: {ts.get('domain', '')}")
        lines.append(f"subject_id: {ts.get('subject_id', '')}")
        if ts.get("key_spec"):
            lines.append(f"Key spec: {ts['key_spec']}")
        srcs = ts.get("sources") or []
        if srcs:
            cites = "; ".join(str(s.get("citation", "")) for s in srcs[:4] if s.get("citation"))
            lines.append(f"Sources: {cites}")
        lines.append(
            "Technical diagram @2 payoff — AS-BUILT / SPEC / EXPLODED VIEW / ILLUSTRATIVE / NOT TO SCALE labels."
        )
        lines.append(
            "Dignity: SFW educational systems communication; not professional engineering certification."
        )
    resolve_music = _import_music_clearance()
    music_line = resolve_music(concept)
    if music_line:
        lines.append(music_line)
    return "\n".join(lines)


def run_gate_0(
    concept: dict[str, Any],
    *,
    actor: Optional[dict[str, Any]],
    actor_id: Optional[str],
    fmt: dict[str, Any],
    format_id: str,
    concept_file: Optional[Path] = None,
) -> dict[str, Any]:
    """Run mandatory Gate 0; save report; return stamp for intake.

    Gate 0 now runs two sub-gates in order:
      1. QA Gate 0 — reasoning-backed content check (_run_qa_gate_0).
         RED blocks the intake before the legal gate is even reached.
         YELLOW logs a warning to stderr and proceeds.
         Override with --skip-qa-gate for emergency bypass.
      2. Legal Gate — existing legal_gate.py v1.3 check (unchanged).
    """
    brief = build_gate_brief_text(
        concept,
        actor=actor,
        actor_id=actor_id,
        fmt=fmt,
        format_id=format_id,
        concept_file=concept_file,
    )

    # --- QA Gate 0: reasoning check on the brief before legal review ---
    qa_result = _run_qa_gate_0(concept, brief)
    if qa_result["gate"] == "RED":
        # QA RED: build a minimal blocked stamp and raise Gate0BlockedError
        qa_stamp: dict[str, Any] = {
            "version": "1.3",
            "verdict": "RED",
            "blocked": True,
            "requires_human_signoff": False,
            "human_signoff": False,
            "target_rating": _gate_rating(concept, fmt, brief),
            "channels": _gate_channels(concept, brief),
            "report_path": "qa_gate_0_blocked",
            "hard_stops": qa_result["issues"],
            "counsel_flags": [],
            "distribution_flags": [],
            "warnings": [],
            "rating_flags": [],
            "cara_status": None,
            "checklist_domains": {},
            "music_bed_id": None,
            "music_clearance_manifest": None,
            "row_2_music_sync": None,
            "notes": qa_result["summary"],
            "brief_source": "qa_gate_0",
            "qa_gate_0": qa_result,
        }
        raise Gate0BlockedError(qa_stamp)

    rating = _gate_rating(concept, fmt, brief)
    channels = _gate_channels(concept, brief)
    LegalGate = _import_legal_gate()
    gate = LegalGate()
    result = gate.review(
        brief,
        concept["slug"],
        target_rating=rating,
        channels=channels,
        has_performers=bool(actor or actor_id or fmt.get("identity_anchor")),
    )
    report_path = gate.save_report(result, brief)
    try:
        rel_report = str(report_path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        rel_report = str(report_path)

    blocked = result.verdict == "RED"
    requires_signoff = result.verdict in ("YELLOW", "COUNSEL")
    gate_cfg = concept.get("gate_0") or {}
    music_bed_id = gate_cfg.get("music_bed_id") or concept.get("music_bed_id")
    music_bed_id = str(music_bed_id).upper() if music_bed_id else None
    row2 = (result.checklist_domains or {}).get("row_2_music_sync")

    return {
        "version": "1.3",
        "verdict": result.verdict,
        "blocked": blocked,
        "requires_human_signoff": requires_signoff,
        "human_signoff": bool((concept.get("gate_0") or {}).get("human_signoff")),
        "target_rating": result.target_rating or rating,
        "channels": result.channels or channels,
        "report_path": rel_report,
        "checklist_domains": result.checklist_domains,
        "hard_stops": result.hard_stops,
        "counsel_flags": result.counsel_flags,
        "distribution_flags": result.distribution_flags,
        "warnings": result.warnings,
        "rating_flags": result.rating_flags,
        "cara_status": result.cara_status,
        "music_bed_id": music_bed_id,
        "music_clearance_manifest": "Studio/Music_Sound/clearance_manifest.json",
        "row_2_music_sync": row2,
        "notes": result.notes,
        "brief_source": str(_concept_brief_path(concept) or "composed"),
        "qa_gate_0": qa_result,   # attached for audit; GREEN/YELLOW/SKIPPED/UNAVAILABLE
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
    if concept.get("historical_figure"):
        haystack += " historical figure biography legacy period language sources"
    if concept.get("science_subject"):
        haystack += " science explainer phenomenon how we know visualization significance sources"

    selector = libs["formats"].get("concept_selector", {})
    selector_formats = selector.get("formats", {})
    if selector_formats:
        best_id, best_score = None, -999.0
        for fid, signals in selector_formats.items():
            if fid not in formats:
                continue
            score = 0.0
            for kw in signals.get("keywords", []):
                if kw.lower() in haystack:
                    score += 2.0
            for nkw in signals.get("negative_keywords", []):
                if nkw.lower() in haystack:
                    score -= 3.0
            score *= float(signals.get("weight", 1.0))
            if score > best_score:
                best_id, best_score = fid, score
        if best_id and best_score > 0:
            return best_id

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


def _load_neutral_lighting_spec() -> dict[str, Any]:
    if not NEUTRAL_LIGHTING_SPEC.is_file():
        return {}
    return json.loads(NEUTRAL_LIGHTING_SPEC.read_text(encoding="utf-8"))


def _apply_neutral_generation_prompt(
    *,
    format_id: str,
    set_id: str,
    style_id: str,
    set_obj: dict[str, Any],
    style_obj: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    """#199 — inject balanced 5500K + RGB parity blocks at generation for clinical sets."""
    spec = _load_neutral_lighting_spec()
    applies = format_id in spec.get("applies_to", []) or set_id in spec.get(
        "applies_to", []
    ) or style_id in spec.get("applies_to", [])
    if not applies:
        return set_obj, style_obj
    patched_set = dict(set_obj)
    patched_style = dict(style_obj)
    if spec.get("lighting_block"):
        patched_set["lighting_lock"] = spec["lighting_block"]
    if spec.get("color_block"):
        patched_set["color_guard"] = spec["color_block"]
    return patched_set, patched_style


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


def _parse_historical_figure(concept: dict[str, Any], format_id: str) -> dict[str, Any]:
    """Validate and normalize concept.historical_figure for biography format."""
    if format_id != HISTORICAL_FIGURE_FORMAT:
        return {}
    hf = concept.get("historical_figure")
    if not isinstance(hf, dict):
        raise ValueError(
            f"format '{HISTORICAL_FIGURE_FORMAT}' requires a 'historical_figure' object "
            "(figure_id, death_year, era, sources)"
        )
    for key in ("figure_id", "death_year", "era", "sources"):
        if key not in hf or hf[key] in (None, "", []):
            raise ValueError(f"historical_figure.{key} is required")
    sources = hf["sources"]
    if not isinstance(sources, list) or not sources:
        raise ValueError("historical_figure.sources must be a non-empty list")
    normalized_sources: list[dict[str, Any]] = []
    for i, src in enumerate(sources):
        if not isinstance(src, dict) or not str(src.get("citation", "")).strip():
            raise ValueError(f"historical_figure.sources[{i}] must include a non-empty 'citation'")
        src_type = str(src.get("type", "secondary")).lower().strip()
        if src_type not in ("primary", "secondary"):
            raise ValueError(
                f"historical_figure.sources[{i}].type must be 'primary' or 'secondary' "
                f"(Historical_SoT_Standard_v1.md)"
            )
        normalized_sources.append({
            "citation": str(src["citation"]).strip(),
            "url": src.get("url"),
            "type": src_type,
            "notes": src.get("notes"),
            "supports": src.get("supports"),
        })
    death_year = hf["death_year"]
    if isinstance(death_year, str) and death_year.isdigit():
        death_year = int(death_year)
    if not isinstance(death_year, int):
        raise ValueError("historical_figure.death_year must be an integer year")
    _import_hist_gate = _import_historical_figure_gate()
    ceiling = _import_hist_gate["DEATH_YEAR_HARD_CEILING"]
    floor = _import_hist_gate["recency_floor_year"]()
    if death_year > ceiling:
        raise ValueError(
            f"historical_figure.death_year {death_year} exceeds hard {ceiling} CE ceiling (#154)"
        )
    if death_year > floor:
        raise ValueError(
            f"historical_figure.death_year {death_year} within 100-year recency floor (max {floor})"
        )
    return {
        "figure_id": str(hf["figure_id"]).strip(),
        "name": str(hf.get("name") or hf["figure_id"]).strip(),
        "death_year": death_year,
        "era": str(hf["era"]).strip(),
        "period_language": hf.get("period_language"),
        "birth_year": hf.get("birth_year"),
        "sources": normalized_sources,
    }


def _parse_science_subject(concept: dict[str, Any], format_id: str) -> dict[str, Any]:
    """Validate and normalize concept.science_subject for science-explainer format."""
    if format_id != SCIENCE_EXPLAINER_FORMAT:
        return {}
    ss = concept.get("science_subject")
    if not isinstance(ss, dict):
        raise ValueError(
            f"format '{SCIENCE_EXPLAINER_FORMAT}' requires a 'science_subject' object "
            "(subject_id, domain, phenomenon, sources)"
        )
    for key in ("subject_id", "domain", "phenomenon", "sources"):
        if key not in ss or ss[key] in (None, "", []):
            raise ValueError(f"science_subject.{key} is required")
    sources = ss["sources"]
    if not isinstance(sources, list) or not sources:
        raise ValueError("science_subject.sources must be a non-empty list")
    normalized_sources: list[dict[str, Any]] = []
    for i, src in enumerate(sources):
        if not isinstance(src, dict) or not str(src.get("citation", "")).strip():
            raise ValueError(f"science_subject.sources[{i}] must include a non-empty 'citation'")
        normalized_sources.append({
            "citation": str(src["citation"]).strip(),
            "url": src.get("url"),
            "type": src.get("type", "secondary"),
            "notes": src.get("notes"),
        })
    base = {
        "subject_id": str(ss["subject_id"]).strip(),
        "domain": str(ss["domain"]).strip(),
        "phenomenon": str(ss["phenomenon"]).strip(),
        "field": ss.get("field"),
        "key_measurement": ss.get("key_measurement"),
        "visualization_ref": ss.get("visualization_ref"),
        "visualization_prompt": ss.get("visualization_prompt"),
        "principle_set": ss.get("principle_set"),
        "plate_id": ss.get("plate_id"),
        "institutions": ss.get("institutions") or [],
        "sources": normalized_sources,
    }
    return enrich_science_subject(base)


def _parse_technical_subject(concept: dict[str, Any], format_id: str) -> dict[str, Any]:
    """Validate and normalize concept.technical_subject for technical-explainer format."""
    if format_id != TECHNICAL_EXPLAINER_FORMAT:
        return {}
    ts = concept.get("technical_subject")
    if not isinstance(ts, dict):
        raise ValueError(
            f"format '{TECHNICAL_EXPLAINER_FORMAT}' requires a 'technical_subject' object "
            "(subject_id, domain, system, sources)"
        )
    for key in ("subject_id", "domain", "system", "sources"):
        if key not in ts or ts[key] in (None, "", []):
            raise ValueError(f"technical_subject.{key} is required")
    sources = ts["sources"]
    if not isinstance(sources, list) or not sources:
        raise ValueError("technical_subject.sources must be a non-empty list")
    normalized_sources: list[dict[str, Any]] = []
    for i, src in enumerate(sources):
        if not isinstance(src, dict) or not str(src.get("citation", "")).strip():
            raise ValueError(f"technical_subject.sources[{i}] must include a non-empty 'citation'")
        normalized_sources.append({
            "citation": str(src["citation"]).strip(),
            "url": src.get("url"),
            "type": src.get("type", "secondary"),
            "notes": src.get("notes"),
        })
    return {
        "subject_id": str(ts["subject_id"]).strip(),
        "domain": str(ts["domain"]).strip(),
        "system": str(ts["system"]).strip(),
        "key_spec": ts.get("key_spec"),
        "visualization_ref": ts.get("visualization_ref"),
        "diagram_prompt": ts.get("diagram_prompt"),
        "diagram_class_default": ts.get("diagram_class_default", "exploded"),
        "plate_id": ts.get("plate_id"),
        "sources": normalized_sources,
    }


def _viz_payoff_labels(beat: dict[str, Any], ss: dict[str, Any]) -> list[str]:
    if beat.get("on_screen_labels"):
        return list(beat["on_screen_labels"])
    labels = ["SCIENCE VISUALIZATION"]
    if beat.get("scale_label", ss.get("scale_label", "NOT TO SCALE")):
        labels.append(str(beat.get("scale_label", ss.get("scale_label", "NOT TO SCALE"))))
    return labels


def _diagram_payoff_labels(beat: dict[str, Any], ts: dict[str, Any]) -> list[str]:
    if beat.get("on_screen_labels"):
        return list(beat["on_screen_labels"])
    diagram_class = str(
        beat.get("diagram_class") or ts.get("diagram_class_default") or "exploded"
    ).lower().replace(" ", "_").replace("-", "_")
    presets: dict[str, list[str]] = {
        "as_built": ["AS-BUILT"],
        "spec": ["SPEC"],
        "exploded": ["EXPLODED VIEW", "ILLUSTRATIVE", "NOT TO SCALE"],
        "exploded_view": ["EXPLODED VIEW", "ILLUSTRATIVE", "NOT TO SCALE"],
        "illustrative": ["ILLUSTRATIVE", "NOT TO SCALE"],
    }
    return presets.get(diagram_class, ["EXPLODED VIEW", "ILLUSTRATIVE", "NOT TO SCALE"])


def _period_line_labels(beat: dict[str, Any], hf: dict[str, Any]) -> list[str]:
    if beat.get("on_screen_labels"):
        return list(beat["on_screen_labels"])
    attestation = str(beat.get("attestation") or hf.get("default_attestation") or "RECONSTRUCTED").upper()
    if attestation == "ATTESTED":
        return ["ATTESTED", "PERIOD LANGUAGE"]
    return ["RECONSTRUCTED", "PERIOD LANGUAGE"]


def _build_shots(
    concept: dict[str, Any],
    fmt: dict[str, Any],
    set_obj: dict[str, Any],
    style_obj: dict[str, Any],
    identity_lock: str,
    voice_suffix: str,
    historical_figure: Optional[dict[str, Any]] = None,
    science_subject: Optional[dict[str, Any]] = None,
    technical_subject: Optional[dict[str, Any]] = None,
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
        if historical_figure and shot["id"] == PERIOD_LINE_SHOT_ID:
            shot["on_screen_labels"] = _period_line_labels(row, historical_figure)
            if historical_figure.get("period_language"):
                shot["speech_lang"] = historical_figure["period_language"]
            shot["historical_figure_ref"] = historical_figure["figure_id"]
        if science_subject and shot["id"] == VIZ_PAYOFF_SHOT_ID:
            shot["on_screen_labels"] = _viz_payoff_labels(row, science_subject)
            shot["reference_slots"] = {"@2": "visualization"}
            shot["science_subject_ref"] = science_subject["subject_id"]
            viz_prompt = row.get("visualization_prompt") or science_subject.get("visualization_prompt")
            if viz_prompt:
                shot["visualization_prompt"] = viz_prompt
            if science_subject.get("visualization_ref"):
                shot["visualization_ref"] = science_subject["visualization_ref"]
        if technical_subject and shot["id"] == DIAGRAM_PAYOFF_SHOT_ID:
            shot["on_screen_labels"] = _diagram_payoff_labels(row, technical_subject)
            shot["reference_slots"] = {"@2": "diagram"}
            shot["technical_subject_ref"] = technical_subject["subject_id"]
            diagram_prompt = row.get("diagram_prompt") or technical_subject.get("diagram_prompt")
            if diagram_prompt:
                shot["diagram_prompt"] = diagram_prompt
            if technical_subject.get("visualization_ref"):
                shot["diagram_ref"] = technical_subject["visualization_ref"]
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
    *,
    science_subject: Optional[dict[str, Any]] = None,
    technical_subject: Optional[dict[str, Any]] = None,
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
    if not identity_lock and format_id in ("documentary-host", HISTORICAL_FIGURE_FORMAT):
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
    if not avatar and format_id in ("documentary-host", HISTORICAL_FIGURE_FORMAT):
        avatar = "productions/host_identity_v1/references/david_avatar_reference.jpg"
    if avatar:
        cfg["avatar_reference"] = avatar

    if set_obj.get("reference_file"):
        cfg["set_reference"] = set_obj["reference_file"]

    viz_ref = None
    if science_subject and science_subject.get("visualization_ref"):
        viz_ref = science_subject["visualization_ref"]
    if technical_subject and technical_subject.get("visualization_ref"):
        viz_ref = technical_subject["visualization_ref"]
    if viz_ref:
        cfg["visualization_reference"] = viz_ref

    # Seamless: library defaults, with host audio/lamp locks for the host format,
    # then any concept overrides on top.
    seamless = dict(
        libs["formats"]["compose_contract"].get("seamless_defaults", {})
    )
    if format_id in ("documentary-host", HISTORICAL_FIGURE_FORMAT):
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
    if format_id == SCIENCE_EXPLAINER_FORMAT:
        seamless.update(
            {
                "lamp_lock": False,
                "glasses_lock": True,
                "loudnorm": True,
                "pin_audio_sync": True,
                "reground_interval": 2,
                "magenta_clamp": True,
                "neutral_grade": True,
                "match_color": True,
                "cut_on_motion": True,
            }
        )
    if format_id == TECHNICAL_EXPLAINER_FORMAT:
        seamless.update(
            {
                "lamp_lock": False,
                "glasses_lock": False,
                "loudnorm": True,
                "pin_audio_sync": True,
                "reground_interval": 2,
                "magenta_clamp": True,
                "neutral_grade": False,
            }
        )
    seamless.update(concept.get("seamless", {}))
    cfg["seamless"] = seamless

    if concept.get("compare_v1"):
        cfg["compare_v1"] = concept["compare_v1"]

    bed_id = (concept.get("gate_0") or {}).get("music_bed_id") or concept.get("music_bed_id")
    if bed_id:
        cfg["music_bed"] = {
            "track_id": str(bed_id).upper(),
            "manifest": "Studio/Music_Sound/clearance_manifest.json",
        }

    return cfg


# --------------------------------------------------------------------------- #
# Provenance card
# --------------------------------------------------------------------------- #
def _sources_summary(sources: list[dict[str, Any]], *, max_items: int = 3) -> str:
    parts: list[str] = []
    for src in sources[:max_items]:
        cite = str(src.get("citation", "")).strip()
        if len(cite) > 72:
            cite = cite[:69] + "…"
        parts.append(cite)
    return " · ".join(parts)


def _build_provenance(
    concept: dict[str, Any],
    fmt: dict[str, Any],
    *,
    historical_figure: Optional[dict[str, Any]] = None,
    science_subject: Optional[dict[str, Any]] = None,
    technical_subject: Optional[dict[str, Any]] = None,
) -> dict[str, Any]:
    template = dict(fmt.get("provenance_card", {"enabled": False}))
    brand = concept.get("brand", {})
    overrides = concept.get("provenance_card", {})

    hf = historical_figure or {}
    ss = science_subject or {}
    ts = technical_subject or {}
    subject_sources = ts.get("sources") or ss.get("sources") or hf.get("sources") or []
    subs = {
        "brand_title": brand.get("title", concept.get("title", "")),
        "brand_subtitle": brand.get("subtitle", ""),
        "cta": brand.get("cta", ""),
        "title": concept.get("title", ""),
        "subtitle": brand.get("subtitle", ""),
        "credit_line": brand.get("credit_line", brand.get("cta", "")),
        "figure_name": hf.get("name") or hf.get("figure_id", ""),
        "figure_era": hf.get("era", ""),
        "death_year": str(hf.get("death_year", "")),
        "phenomenon_name": ss.get("phenomenon") or ss.get("subject_id", ""),
        "science_domain": ss.get("domain", ""),
        "system_name": ts.get("system") or ts.get("subject_id", ""),
        "technical_domain": ts.get("domain", ""),
        "sources_summary": _sources_summary(subject_sources),
    }
    for key, val in list(template.items()):
        if isinstance(val, str) and "{" in val:
            out = val
            for ph, repl in subs.items():
                out = out.replace(f"{{{ph}}}", repl)
            template[key] = out
    template.update(overrides)
    if hf:
        template["card_type"] = template.get("card_type", "sources")
        template["sources"] = hf.get("sources", [])
        template["historical_figure_id"] = hf.get("figure_id")
    if ss:
        template["card_type"] = template.get("card_type", "sources")
        template["sources"] = ss.get("sources", [])
        template["science_subject_id"] = ss.get("subject_id")
    if ts:
        template["card_type"] = template.get("card_type", "sources")
        template["sources"] = ts.get("sources", [])
        template["technical_subject_id"] = ts.get("subject_id")
    return template


class Gate0BlockedError(Exception):
    """Gate 0 RED — intake must not emit a script."""

    def __init__(self, stamp: dict[str, Any]) -> None:
        self.stamp = stamp
        super().__init__(stamp.get("verdict", "RED"))


# --------------------------------------------------------------------------- #
# Editorial routing  (#213 — written client deliverables → SCRIBE editorial engine)
# --------------------------------------------------------------------------- #
def is_editorial_intake(concept: dict[str, Any]) -> bool:
    """True when an intake form/concept belongs to the Editorial lane.

    Recognised signals (any one is sufficient):
      * ``format_id == "editorial"``
      * ``auto_route.lane == "Editorial"`` (NEXUS routing map)
      * ``auto_route.service_id`` starting ``editorial.`` (e.g. ``editorial.screenplay_dev``)
      * ``editorial`` listed in ``auto_route.gates`` / ``gates``
      * an explicit ``editorial`` / ``editorial_brief`` block on the concept
    """
    if str(concept.get("format_id", "")).strip().lower() == EDITORIAL_FORMAT:
        return True
    auto = concept.get("auto_route") or {}
    if str(auto.get("lane", "")).strip().lower() == EDITORIAL_LANE:
        return True
    if str(auto.get("service_id", "")).strip().lower().startswith("editorial."):
        return True
    gates = list(auto.get("gates") or []) + list(concept.get("gates") or [])
    if any(str(g).strip().lower() == EDITORIAL_LANE for g in gates):
        return True
    return bool(concept.get("editorial") or concept.get("editorial_brief"))


def _editorial_source_rank(path_str: str) -> int:
    """Prefer the deliverable manuscript: screenplay > markdown > plain text > other."""
    suffix = Path(str(path_str)).suffix.lower()
    return {".fountain": 0, ".spmd": 0, ".md": 1, ".markdown": 1, ".txt": 2}.get(suffix, 3)


def _resolve_editorial_source(
    form: dict[str, Any], concept_file: Optional[Path] = None
) -> Path:
    """Resolve the primary editorial document from the form's source/attachments."""
    explicit = form.get("editorial_source") or form.get("source")
    attachments = list(form.get("attachments") or [])
    ordered = sorted(attachments, key=_editorial_source_rank)
    candidates = ([explicit] if explicit else []) + ordered

    bases = [ROOT]
    if concept_file is not None:
        bases.insert(0, concept_file.parent)
    for cand in candidates:
        if not cand:
            continue
        p = Path(str(cand))
        search = [p] if p.is_absolute() else [base / p for base in bases]
        for candidate in search:
            if candidate.is_file():
                return candidate
    raise FileNotFoundError(
        "editorial intake: no readable source document found in 'source'/'attachments' "
        f"(looked for {', '.join(str(c) for c in candidates) or 'nothing'})"
    )


def _editorial_meta_from_form(form: dict[str, Any]) -> dict[str, Any]:
    """Translate a NEXUS intake form into editorial-engine meta."""
    meta: dict[str, Any] = {"client_deliverable": True}
    field_map = {
        "project_title": "title",
        "title": "title",
        "genre_tone": "genre",
        "content_rating": "content_rating",
        "client_contact": "client",
        "business_entity": "business_entity",
    }
    for src, dest in field_map.items():
        if form.get(src):
            meta.setdefault(dest, form[src])
    if "real_people_depicted" in form:
        meta["names_real_people"] = bool(form["real_people_depicted"])
    pid = form.get("project_id") or form.get("slug")
    if pid:
        meta["project_id"] = pid
    # Carry through any explicit attestations / meta the form already supplies.
    meta.update(form.get("editorial_meta") or {})
    return meta


def route_editorial_intake(
    form: dict[str, Any],
    *,
    concept_file: Optional[Path] = None,
) -> dict[str, Any]:
    """Hand an editorial brief/form to the SCRIBE editorial engine.

    Runs the engine's intake stage — which evaluates the Editorial Gate and routes
    its report into the shared ``Studio/Legal/Gate_Reports`` sink — and returns a
    routing stamp the pipeline (or NEXUS dispatch) can act on. No Gate-0 legal /
    video script is produced here; that happens later only if the dispatch calls
    for synthetic video work.
    """
    if str(EDITORIAL_ENGINE_DIR) not in sys.path:
        sys.path.insert(0, str(EDITORIAL_ENGINE_DIR))
    import editorial_engine as ee  # noqa: WPS433

    source = _resolve_editorial_source(form, concept_file)
    meta = _editorial_meta_from_form(form)
    pid = meta.get("project_id") or form.get("slug") or form.get("project_id")

    project = ee.open_project(str(source), None, None, pid)
    project.meta = {**project.meta, **meta}

    gate = ee.stage_intake(project)
    ee.write_manifest(project, gate, None, 1)

    auto = form.get("auto_route") or {}
    return {
        "lane": "Editorial",
        "engine": "Scribe/SCRIBE/editorial_engine.py",
        "service_id": auto.get("service_id", "editorial.screenplay_dev"),
        "tier": form.get("tier") or auto.get("tier"),
        "project_id": project.project_id,
        "doc_kind": project.doc_kind,
        "source": ee._rel(source),
        "gate": "editorial",
        "gate_verdict": gate.get("verdict"),
        "gate_report": gate.get("report_path"),
        "gate_report_json": gate.get("report_json"),
        "blocked": bool(gate.get("blocked")),
        "requires_human_signoff": bool(gate.get("requires_human_signoff")),
        "intake_record": ee._rel(project.out_dir / "intake.json"),
        "project_dir": ee._rel(project.out_dir),
        "deliverables": form.get("deliverables"),
        "next": "python Scribe/SCRIBE/editorial_engine.py run "
                f"{ee._rel(source)} --project-id {project.project_id}",
    }


# --------------------------------------------------------------------------- #
# Public entry point
# --------------------------------------------------------------------------- #
def build_longform_script(
    concept: dict[str, Any],
    libs: Optional[dict[str, Any]] = None,
    *,
    concept_file: Optional[Path] = None,
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
        concept,
        actor=actor,
        actor_id=actor_id,
        fmt=fmt,
        format_id=format_id,
        concept_file=concept_file,
    )
    if gate_stamp["blocked"]:
        raise Gate0BlockedError(gate_stamp)

    # --- Editing QA gate (post Gate 0, when --editing-qa is active) ---
    if _EDITING_QA_GATE_ACTIVE:
        _content_for_editing = json.dumps(concept, ensure_ascii=False)
        _editing_result = _run_editing_qa_gate(_content_for_editing, concept)
        gate_stamp["editing_qa"] = _editing_result
        if _editing_result["gate"] == "RED":
            print(
                f"[ERROR] Gate1EditingHoldError for '{concept.get('slug','')}': "
                f"{_editing_result['summary']}",
                file=sys.stderr,
            )
            gate_stamp["blocked"] = True
            gate_stamp["verdict"] = "RED"
            gate_stamp["hard_stops"] = gate_stamp.get("hard_stops", []) + [
                f"Editing Federation RED: {_editing_result['summary']}"
            ]
            raise Gate0BlockedError(gate_stamp)
        elif _editing_result["gate"] == "YELLOW":
            print(
                f"[WARN] Editing QA YELLOW for '{concept.get('slug','')}': "
                f"{_editing_result['summary']}",
                file=sys.stderr,
            )

    set_id, set_obj, style_id, style_obj = select_set_style(
        concept.get("set_id"), concept.get("style_id"), fmt, libs
    )
    set_obj, style_obj = _apply_neutral_generation_prompt(
        format_id=format_id,
        set_id=set_id,
        style_id=style_id,
        set_obj=set_obj,
        style_obj=style_obj,
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
    historical_figure = _parse_historical_figure(concept, format_id)
    science_subject = _parse_science_subject(concept, format_id)
    technical_subject = _parse_technical_subject(concept, format_id)

    config = _build_config(
        concept, fmt, format_id, set_obj, actor, voice_suffix, libs,
        science_subject=science_subject or None,
        technical_subject=technical_subject or None,
    )
    shots = _build_shots(
        concept, fmt, set_obj, style_obj, identity_lock, voice_suffix,
        historical_figure=historical_figure or None,
        science_subject=science_subject or None,
        technical_subject=technical_subject or None,
    )
    duration_clamp_meta: dict[str, Any] | None = None
    if should_clamp_shot_durations(config.get("seamless")):
        shots, duration_clamp_meta = apply_duration_clamp_to_shots(shots)

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
            "actor_id": actor["actor_id"] if actor else (actor_id or fmt.get("identity_anchor", "")),
            "gate_0": gate_stamp,
        },
        "concept": concept.get("concept", ""),
        "config": config,
        "shots": shots,
        "production_meta": {
            "actor_id": actor["actor_id"] if actor else (actor_id or ""),
            "identity_anchor": (fmt.get("identity_anchor") or "").lstrip("@"),
            "set_id": set_obj.get("set_id") if set_obj else concept.get("set_id", ""),
            "target_rating": _resolve_rating(concept, fmt),
            "content_rating": _resolve_rating(concept, fmt),
            "plate_id": (science_subject or {}).get("plate_id") if science_subject else None,
            "visualization_reference": (science_subject or {}).get("visualization_reference") if science_subject else None,
        },
        "provenance_card": _build_provenance(
            concept, fmt,
            historical_figure=historical_figure or None,
            science_subject=science_subject or None,
            technical_subject=technical_subject or None,
        ),
        "publish": concept.get("publish") or {},
    }

    if duration_clamp_meta:
        script.setdefault("_meta", {})["duration_clamp"] = duration_clamp_meta

    return script, gate_stamp


def intake(
    concept: dict[str, Any],
    libs: Optional[dict[str, Any]] = None,
    *,
    concept_file: Optional[Path] = None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Route an intake concept/form to the correct pipeline path.

    Returns ``(script_or_routing_dict, gate_stamp)`` where *gate_stamp* always
    carries ``verdict`` (GREEN/YELLOW/RED) and ``blocked`` (bool).

    * **Editorial lane** -- ``format_id == "editorial"`` or any signal detected
      by :func:`is_editorial_intake` -- is forwarded to
      :func:`route_editorial_intake` (SCRIBE editorial engine).  The routing
      dict is returned as the *script* side of the pair; a minimal gate stamp
      is synthesised from ``gate_verdict`` / ``blocked``.

    * **Everything else** -- delegated to :func:`build_longform_script` which
      runs Gate 0 and returns the canonical ``render_longform`` ``script.json``
      dict together with the gate stamp.
    """
    if is_editorial_intake(concept):
        result = route_editorial_intake(concept, concept_file=concept_file)
        gate: dict[str, Any] = {
            "verdict": result.get("gate_verdict") or (
                "RED" if result.get("blocked") else "GREEN"
            ),
            "blocked": bool(result.get("blocked")),
            "requires_human_signoff": bool(result.get("requires_human_signoff")),
        }
        return result, gate
    return build_longform_script(concept, libs, concept_file=concept_file)


def main(argv=None) -> int:
    import argparse as _argparse

    parser = _argparse.ArgumentParser(
        description="STUDIO production intake -- concept.json -> script.json + Gate 0"
    )
    parser.add_argument(
        "concept",
        nargs="?",
        help="Path to *.concept.json or intake form JSON",
    )
    parser.add_argument("-o", "--out", default=None, help="Output script path")
    parser.add_argument("--slug", help="Override slug")
    parser.add_argument("--title", help="Override title")
    parser.add_argument("--format", dest="format_id", help="Override format")
    parser.add_argument("--actor", help="Override actor_id")
    parser.add_argument("--set", help="Override set_id")
    parser.add_argument("--style", help="Override style_id")
    parser.add_argument("--print", dest="print_only", action="store_true",
                        help="Print script JSON to stdout without writing")
    parser.add_argument(
        "--skip-qa-gate",
        action="store_true",
        help=(
            "Emergency override: skip the QA Gate 0 reasoning check. "
            "Legal Gate 0 still runs. Use only when QA gate is unavailable "
            "or for emergency production bypass. Logged in gate stamp."
        ),
    )
    parser.add_argument(
        "--editing-qa",
        action="store_true",
        help=(
            "After Gate 0 passes, run the Editing Federation dispatcher on the "
            "intake content. RED blocks with Gate1EditingHoldError (logged to stderr). "
            "YELLOW logs a warning and continues. GREEN is silent."
        ),
    )
    args = parser.parse_args(argv)

    # Wire --skip-qa-gate into module-level flag before any intake call
    global _QA_GATE_SKIP, _EDITING_QA_GATE_ACTIVE
    if args.skip_qa_gate:
        _QA_GATE_SKIP = True
        print("[WARN] --skip-qa-gate active: QA Gate 0 reasoning check bypassed.",
              file=__import__("sys").stderr)
    if args.editing_qa:
        _EDITING_QA_GATE_ACTIVE = True

    if not args.concept:
        parser.print_help()
        return 1

    import json as _json
    concept_path = Path(args.concept)
    concept = _json.loads(concept_path.read_text(encoding="utf-8"))

    # CLI overrides
    if args.slug:
        concept["slug"] = args.slug
    if args.title:
        concept["title"] = args.title
    if args.format_id:
        concept["format_id"] = args.format_id
    if args.actor:
        concept["actor_id"] = args.actor
    if args.set:
        concept["set_id"] = args.set
    if args.style:
        concept["style_id"] = args.style

    script, gate = intake(concept)

    out_str = _json.dumps(script, indent=2, ensure_ascii=False)

    if args.print_only:
        print(out_str)
        return 0

    if args.out:
        out_path = Path(args.out)
    else:
        prod_dir = concept_path.parent.parent / "productions" / f"{concept['slug']}_longform_v1"
        prod_dir.mkdir(parents=True, exist_ok=True)
        out_path = prod_dir / f"{concept['slug']}_script.json"

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(out_str + "\n", encoding="utf-8")
    print(f"[intake] script -> {out_path}")
    verdict = gate.get("verdict", "?")
    print(f"[intake] Gate 0: {verdict}")
    return 0 if verdict != "RED" else 2


if __name__ == "__main__":
    raise SystemExit(main())
