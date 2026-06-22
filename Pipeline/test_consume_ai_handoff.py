#!/usr/bin/env python3
"""End-to-end test: Julius Caesar StudioPackage → consume_ai_handoff → script.json.

Validates (Handoff Contract section 5, item 4):
  - Validation logic: valid package passes; missing required fields are caught.
  - consume_ai_handoff() writes STUDIO/Productions/julius-caesar/script.json.
  - script.json has correct render_longform shape (config + shots keys).
  - Each shot has: id, duration, t_start, t_end, role, video_prompt.
  - Shots with speech_text / on_screen carry those fields.
  - Timing is sequential (t_end of shot N == t_start of shot N+1).
  - Provenance chain intact: handoff_id, source_repo, citations, gate_status.
  - video_prompt references the AI-supplied cinematic_style / lane.

Run:
    cd "C:\\Users\\NCG\\Videos\\Grok Projects\\STUDIO\\Pipeline"
    python test_consume_ai_handoff.py
"""
from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

# ── path setup ───────────────────────────────────────────────────────────────
PIPELINE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(PIPELINE_DIR))

from consume_ai_handoff import consume_ai_handoff, validate_studio_package

# ── Julius Caesar StudioPackage fixture ──────────────────────────────────────
JULIUS_CAESAR_PACKAGE: dict = {
    "handoff_id": "test-uuid-julius-caesar-001",
    "source": "Visualization Federation v1.0",
    "task": "Julius Caesar",
    "lane": "DAVID",
    "cinematic_style": "impasto + dramatic_cam + period_lighting",
    "render_directives": {
        "motion_blur":    False,
        "heat_haze":      False,
        "negative_space": False,
        "impasto_texture": True,
        "camera":         "dramatic_cam + push_in",
        "period_grade":   True,
    },
    "assets": {
        "frame_paths": [],
        "plates":      [],
        "particle_data": {},
    },
    "deliverable_spec": {
        "resolution": "1920x1080",
        "fps":        24,
        "codec":      "H.264",
        "duration_s": 60.0,
    },
    "concept_hint": {
        "slug":      "julius-caesar",
        "format_id": "longform_documentary",
        "beats": [
            {
                "id":          "01_rise",
                "speech_text": "Tonight: Gaius Julius Caesar — general, dictator, "
                               "and the man who made Rome an empire in all but name.",
                "on_screen":   "Julius Caesar · d. 44 BCE",
            },
            {
                "id":          "02_conquest",
                "speech_text": "Born into a patrician family in 100 BCE, he climbed "
                               "from quaestor to consul and conquered Gaul in a decade.",
                "on_screen":   "Gaul · 58–50 BCE",
            },
            {
                "id":          "03_rubicon",
                "speech_text": "He crossed the Rubicon with a civil war in his wake.",
                "on_screen":   "Rubicon · 49 BCE",
            },
            {
                "id":            "04_period_line",
                "speech_text":   "Veni, vidi, vici.",
                "on_screen":     "I came, I saw, I conquered.",
                "on_screen_labels": ["ATTESTED", "PERIOD LANGUAGE"],
                "speech_lang":   "Latin",
            },
            {
                "id":          "05_legacy",
                "speech_text": "They killed him on the Ides of March — but his name "
                               "became the title of emperors.",
                "on_screen":   "Ides of March · 44 BCE",
            },
        ],
    },
    "provenance": {
        "source_repo": "HISTORY",
        "citations": [
            "Suetonius, The Twelve Caesars",
            "Plutarch, Life of Caesar",
            "British Museum — Roman Republican denarius portraits of Caesar",
        ],
        "jantzen_compliance_score": 0.0,
        "gate_status": {
            "historical_figure_gate": "PASS",
            "science_gate":           "N/A",
            "knowledge_gate":         "PASS",
        },
    },
}

# ── test runner ──────────────────────────────────────────────────────────────
_PASS = 0
_FAIL = 0


def _ok(label: str) -> None:
    global _PASS
    _PASS += 1
    print(f"  \033[32m✓\033[0m {label}")


def _fail(label: str, detail: str = "") -> None:
    global _FAIL
    _FAIL += 1
    suffix = f": {detail}" if detail else ""
    print(f"  \033[31m✗\033[0m {label}{suffix}")


def check(cond: bool, label: str, detail: str = "") -> bool:
    if cond:
        _ok(label)
    else:
        _fail(label, detail)
    return cond


# ── individual tests ─────────────────────────────────────────────────────────

def test_validation_valid() -> None:
    print("\n[1] validate_studio_package — valid package")
    errs = validate_studio_package(JULIUS_CAESAR_PACKAGE)
    check(len(errs) == 0, "No validation errors", str(errs))


def test_validation_missing_handoff_id() -> None:
    print("\n[2] validate_studio_package — empty handoff_id caught")
    bad = {**JULIUS_CAESAR_PACKAGE, "handoff_id": ""}
    errs = validate_studio_package(bad)
    check(any("handoff_id" in e for e in errs), "Error references 'handoff_id'")


def test_validation_missing_lane() -> None:
    print("\n[3] validate_studio_package — missing lane caught")
    bad = {k: v for k, v in JULIUS_CAESAR_PACKAGE.items() if k != "lane"}
    errs = validate_studio_package(bad)
    check(any("lane" in e for e in errs), "Error references 'lane'")


def test_validation_empty_beats() -> None:
    print("\n[4] validate_studio_package — empty beats list caught")
    bad_hint = {**JULIUS_CAESAR_PACKAGE["concept_hint"], "beats": []}
    bad = {**JULIUS_CAESAR_PACKAGE, "concept_hint": bad_hint}
    errs = validate_studio_package(bad)
    check(any("beats" in e for e in errs), "Error references 'beats'")


def test_validation_missing_provenance_field() -> None:
    print("\n[5] validate_studio_package — missing provenance.source_repo caught")
    bad_prov = {k: v for k, v in JULIUS_CAESAR_PACKAGE["provenance"].items()
                if k != "source_repo"}
    bad = {**JULIUS_CAESAR_PACKAGE, "provenance": bad_prov}
    errs = validate_studio_package(bad)
    check(any("source_repo" in e for e in errs), "Error references 'source_repo'")


def test_consume_writes_file() -> Path | None:
    print("\n[6] consume_ai_handoff() — writes script.json to Productions/julius-caesar/")
    with tempfile.TemporaryDirectory() as tmp:
        out_dir = Path(tmp) / "julius-caesar"
        out_path = consume_ai_handoff(JULIUS_CAESAR_PACKAGE, out_dir=out_dir)
        check(out_path.exists(), f"File written: {out_path.name}")
        check(out_path.name == "script.json", "File named script.json")
        check("julius-caesar" in str(out_path), "Path contains slug 'julius-caesar'")
        # Copy the script for downstream tests
        script_json = json.loads(out_path.read_text(encoding="utf-8"))

    # Run the remaining shape tests using the in-memory script
    _test_script_shape(script_json)
    _test_shots_shape(script_json)
    _test_video_prompt_style(script_json)
    _test_provenance_chain(script_json)
    _test_intake_fields(script_json)
    return None


# ── shape sub-tests (run against in-memory script dict) ──────────────────────

def _test_script_shape(script: dict) -> None:
    print("\n[7] script.json top-level shape")
    check(script.get("slug") == "julius-caesar", "slug = 'julius-caesar'")
    check(script.get("title") == "Julius Caesar", "title = 'Julius Caesar'")
    check(script.get("format_id") == "longform_documentary", "format_id correct")
    check(script.get("target_seconds") == 60.0, "target_seconds = 60.0")
    check("config" in script, "'config' key present")
    check("shots" in script, "'shots' key present")
    check("provenance" in script, "'provenance' key present")
    check("intake" in script, "'intake' key present")

    cfg = script.get("config", {})
    check("model_video" in cfg, "config.model_video present")
    check("resolution" in cfg, "config.resolution present")
    check("seamless" in cfg, "config.seamless present")


def _test_shots_shape(script: dict) -> None:
    print("\n[8] shots shape and timing")
    shots = script.get("shots", [])
    check(len(shots) == 5, f"5 shots built (got {len(shots)})")

    t = 0
    for shot in shots:
        sid = shot.get("id", "?")
        check("id" in shot,       f"shot '{sid}': id present")
        check("duration" in shot,  f"shot '{sid}': duration present")
        check("t_start" in shot,   f"shot '{sid}': t_start present")
        check("t_end" in shot,     f"shot '{sid}': t_end present")
        check("role" in shot,      f"shot '{sid}': role present")
        check(
            bool(shot.get("video_prompt")),
            f"shot '{sid}': video_prompt non-empty",
        )
        # Timing is sequential
        check(
            shot["t_start"] == t,
            f"shot '{sid}': t_start={shot['t_start']} (expected {t})",
        )
        check(
            shot["t_end"] == t + shot["duration"],
            f"shot '{sid}': t_end={shot['t_end']} = t_start + duration",
        )
        t = shot["t_end"]

    # Spot-check beat fields carried through
    s0 = shots[0] if shots else {}
    check(
        "Tonight" in s0.get("speech_text", ""),
        "shot 01: speech_text starts with 'Tonight'",
    )
    check(
        s0.get("on_screen") == "Julius Caesar · d. 44 BCE",
        "shot 01: on_screen correct",
    )

    # Period line shot carries labels + speech_lang
    period = next((s for s in shots if s.get("id") == "04_period_line"), None)
    if period:
        check(
            period.get("on_screen_labels") == ["ATTESTED", "PERIOD LANGUAGE"],
            "shot 04: on_screen_labels = ['ATTESTED', 'PERIOD LANGUAGE']",
        )
        check(
            period.get("speech_lang") == "Latin",
            "shot 04: speech_lang = 'Latin'",
        )
    else:
        _fail("shot '04_period_line' not found in shots list")


def _test_video_prompt_style(script: dict) -> None:
    print("\n[9] video_prompt content")
    shots = script.get("shots", [])
    for shot in shots:
        sid    = shot.get("id", "?")
        prompt = shot.get("video_prompt", "")
        check(
            "DAVID" in prompt,
            f"shot '{sid}': video_prompt contains lane [DAVID]",
            f"prompt: {prompt[:100]}",
        )
        check(
            "impasto" in prompt.lower(),
            f"shot '{sid}': video_prompt references 'impasto'",
        )
        check(
            "dramatic_cam" in prompt.lower(),
            f"shot '{sid}': video_prompt references camera directive",
        )
        # Speech text echoed in prompt
        speech = shot.get("speech_text", "")
        if speech:
            check(
                speech[:20] in prompt,
                f"shot '{sid}': speech_text echoed in video_prompt",
            )


def _test_provenance_chain(script: dict) -> None:
    print("\n[10] provenance chain")
    prov = script.get("provenance", {})
    check(
        prov.get("handoff_id") == "test-uuid-julius-caesar-001",
        "provenance.handoff_id matches input",
    )
    check(prov.get("source_repo") == "HISTORY", "provenance.source_repo = 'HISTORY'")
    cites = prov.get("citations", [])
    check(
        isinstance(cites, list) and len(cites) == 3,
        f"provenance.citations has 3 entries (got {len(cites)})",
    )
    gs = prov.get("gate_status", {})
    check(
        gs.get("historical_figure_gate") == "PASS",
        "provenance.gate_status.historical_figure_gate = 'PASS'",
    )
    check(
        prov.get("jantzen_compliance_score") == 0.0,
        "provenance.jantzen_compliance_score = 0.0",
    )


def _test_intake_fields(script: dict) -> None:
    print("\n[11] intake metadata")
    intake = script.get("intake", {})
    check(
        intake.get("handoff_id") == "test-uuid-julius-caesar-001",
        "intake.handoff_id matches",
    )
    check(intake.get("lane") == "DAVID", "intake.lane = 'DAVID'")
    check(
        intake.get("cinematic_style") == "impasto + dramatic_cam + period_lighting",
        "intake.cinematic_style correct",
    )
    check("ingested_at" in intake, "intake.ingested_at timestamp present")


# ── main ─────────────────────────────────────────────────────────────────────

def main() -> int:
    BOLD  = "\033[1m"
    RESET = "\033[0m"
    GREEN = "\033[32m"
    RED   = "\033[31m"

    print(f"\n{BOLD}{'=' * 62}{RESET}")
    print(f"{BOLD}NEXUS — consume_ai_handoff End-to-End Test{RESET}")
    print("Julius Caesar StudioPackage → script.json")
    print(f"{BOLD}{'=' * 62}{RESET}")

    test_validation_valid()
    test_validation_missing_handoff_id()
    test_validation_missing_lane()
    test_validation_empty_beats()
    test_validation_missing_provenance_field()
    test_consume_writes_file()

    print(f"\n{BOLD}{'=' * 62}{RESET}")
    if _FAIL == 0:
        print(f"  {GREEN}{BOLD}ALL {_PASS} CHECKS PASS ✓{RESET}")
        print(f"  Handoff Contract §5 item 4: AI → STUDIO consume_ai_handoff → script.json")
        return 0
    else:
        print(f"  {RED}{BOLD}{_FAIL} FAILURE(S) / {_PASS} passed{RESET}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
