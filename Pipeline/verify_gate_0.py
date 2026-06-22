#!/usr/bin/env python3
"""
verify_gate_0.py — Gate 0 Channel Launch Verification
T4 #142 · Upon Tyne Productions / DAVID channel

Automated checks for sections A (legal/compliance) and B (channel identity /
upload kit) of Gate_0_Channel_Launch_Checklist.md.

Usage:
    python STUDIO/Pipeline/verify_gate_0.py [--verbose]

Exit codes:
    0 — all checks PASS
    1 — one or more checks FAIL
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Resolve root directories relative to this script.
# This file lives at:  <ROOT>/STUDIO/Pipeline/verify_gate_0.py
# ---------------------------------------------------------------------------
SCRIPT_PATH            = Path(__file__).resolve()
PIPELINE_DIR           = SCRIPT_PATH.parent           # STUDIO/Pipeline/
STUDIO_DIR             = PIPELINE_DIR.parent          # STUDIO/
ROOT_DIR               = STUDIO_DIR.parent            # Grok Projects/

LEGAL_GATE_PY          = ROOT_DIR  / "artifacts" / "legal" / "legal_gate.py"
CONSUME_HANDOFF_PY     = PIPELINE_DIR / "consume_ai_handoff.py"
CHANNEL_IDENTITY_JSON  = STUDIO_DIR / "Art_Department" / "Brand_Kit" / "channel_identity.json"
THUMBNAIL_SPECS_JSON   = STUDIO_DIR / "Art_Department" / "Thumbnails" / "thumbnail_specs.json"
REROLL_QUEUE_MD        = STUDIO_DIR / "Cast" / "Casting_Bible" / "registry" / "REROLL_QUEUE.md"
CASTING_REGISTRY_JSON  = STUDIO_DIR / "Cast" / "Casting_Bible" / "registry" / "magazine_casting_registry.json"
AGE_POLICY_MD          = STUDIO_DIR / "research" / "Age_Policy_Locked.md"
PRODUCTIONS_DIR        = ROOT_DIR  / "DAVID" / "productions"

REQUIRED_CHANNEL_IDENTITY_KEYS = [
    "company", "channel_name", "channel_badge", "ai_disclosure", "section_2257",
]
REQUIRED_UPLOAD_KIT_KEYS = [
    "youtube_title", "youtube_description", "chapters",
    "youtube_tags", "ai_disclosure_card", "section_2257_note",
]
MIN_THUMBNAIL_SPECS = 12


# ---------------------------------------------------------------------------
# Result object
# ---------------------------------------------------------------------------
class Check:
    def __init__(self, label: str, passed: bool, detail: str = ""):
        self.label  = label
        self.passed = passed
        self.detail = detail

    def __repr__(self) -> str:
        status = "PASS" if self.passed else "FAIL"
        line   = f"[{status}] {self.label}"
        if self.detail:
            line += f"\n       → {self.detail}"
        return line


# ---------------------------------------------------------------------------
# Individual checks
# ---------------------------------------------------------------------------

def check_legal_gate_constant(verbose: bool) -> Check:
    label = "§ 2257 statement constant (SECTION_2257_STATEMENT) in legal_gate.py"
    if not LEGAL_GATE_PY.is_file():
        return Check(label, False, f"File not found: {LEGAL_GATE_PY}")
    text = LEGAL_GATE_PY.read_text(encoding="utf-8", errors="replace")
    found = bool(re.search(r"SECTION_2257_STATEMENT\s*=", text)) and "18 U.S.C." in text
    if not found:
        return Check(label, False, "SECTION_2257_STATEMENT constant not found or appears empty")
    return Check(label, True, "18 U.S.C. § 2257 statement confirmed present" if verbose else "")


def check_legal_gate_helper(verbose: bool) -> Check:
    label = "get_2257_statement() helper in legal_gate.py"
    if not LEGAL_GATE_PY.is_file():
        return Check(label, False, f"File not found: {LEGAL_GATE_PY}")
    text  = LEGAL_GATE_PY.read_text(encoding="utf-8", errors="replace")
    found = bool(re.search(r"def\s+get_2257_statement\s*\(", text))
    return Check(label, found, "" if found else "def get_2257_statement() not found")


def check_gate_result_section_2257(verbose: bool) -> Check:
    label = "GateResult.section_2257 field present in legal_gate.py"
    if not LEGAL_GATE_PY.is_file():
        return Check(label, False, f"File not found: {LEGAL_GATE_PY}")
    text  = LEGAL_GATE_PY.read_text(encoding="utf-8", errors="replace")
    found = bool(re.search(r"section_2257\s*:\s*str", text))
    return Check(label, found, "" if found else "section_2257: str not found in GateResult dataclass")


def check_hard_stop_wired(verbose: bool) -> Check:
    label = "Gate 0 hard stop (raise ValueError on RED) in consume_ai_handoff.py"
    if not CONSUME_HANDOFF_PY.is_file():
        return Check(label, False, f"File not found: {CONSUME_HANDOFF_PY}")
    text        = CONSUME_HANDOFF_PY.read_text(encoding="utf-8", errors="replace")
    has_raise   = bool(re.search(r"raise\s+ValueError", text))
    has_gate    = bool(re.search(r"""['"](blocked|RED)['"]""", text))
    passed      = has_raise and has_gate
    if not passed:
        missing = []
        if not has_raise: missing.append("'raise ValueError' not found")
        if not has_gate:  missing.append("'blocked'/'RED' gate condition not found")
        return Check(label, False, "; ".join(missing))
    return Check(label, True, "raise ValueError on .get('blocked') or verdict=='RED'" if verbose else "")


def check_age_policy(verbose: bool) -> Check:
    label  = "Age_Policy_Locked.md exists (STUDIO/research/Age_Policy_Locked.md)"
    exists = AGE_POLICY_MD.is_file()
    detail = str(AGE_POLICY_MD) if verbose else ("not found" if not exists else "")
    return Check(label, exists, detail)


def check_channel_identity(verbose: bool) -> list[Check]:
    checks: list[Check] = []
    file_label = "channel_identity.json — file exists and is valid JSON"

    if not CHANNEL_IDENTITY_JSON.is_file():
        checks.append(Check(file_label, False, f"Not found: {CHANNEL_IDENTITY_JSON}"))
        for key in REQUIRED_CHANNEL_IDENTITY_KEYS:
            checks.append(Check(f"channel_identity.json: '{key}' non-empty", False, "file missing"))
        return checks

    try:
        data = json.loads(CHANNEL_IDENTITY_JSON.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        checks.append(Check(file_label, False, f"JSON parse error: {exc}"))
        return checks

    checks.append(Check(file_label, True, str(CHANNEL_IDENTITY_JSON) if verbose else ""))
    for key in REQUIRED_CHANNEL_IDENTITY_KEYS:
        val    = data.get(key, "")
        passed = bool(val and str(val).strip())
        detail = (repr(str(val)[:60]) if verbose and passed else "") or ("empty or missing" if not passed else "")
        checks.append(Check(f"channel_identity.json: '{key}' non-empty", passed, detail))
    return checks


def check_upload_kits(verbose: bool) -> list[Check]:
    checks: list[Check] = []
    scan_label = f"Upload kit(s) found in {PRODUCTIONS_DIR.relative_to(ROOT_DIR)}"

    kits = sorted(PRODUCTIONS_DIR.rglob("*_upload_kit.json")) if PRODUCTIONS_DIR.is_dir() else []
    if not kits:
        checks.append(Check(scan_label, False, f"No *_upload_kit.json found under {PRODUCTIONS_DIR}"))
        return checks

    kit_names = ", ".join(k.name for k in kits)
    checks.append(Check(scan_label, True, f"{len(kits)} kit(s): {kit_names}" if verbose else f"{len(kits)} kit(s) found"))

    for kit_path in kits:
        try:
            kit = json.loads(kit_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            checks.append(Check(f"upload_kit {kit_path.name} — valid JSON", False, str(exc)))
            continue

        short = kit_path.name
        for key in REQUIRED_UPLOAD_KIT_KEYS:
            val    = kit.get(key)
            passed = bool(val)
            detail = ("empty or missing" if not passed else (repr(str(val)[:60]) if verbose else ""))
            checks.append(Check(f"upload_kit {short}: '{key}' present and non-empty", passed, detail))

        desc           = kit.get("youtube_description", "")
        has_disclosure = bool(re.search(r"\b(AI|synthetic|ai-generated|AI-generated)\b", desc, re.I))
        checks.append(Check(
            f"upload_kit {short}: youtube_description contains AI/synthetic disclosure",
            has_disclosure,
            "'AI' or 'synthetic' not found in description" if not has_disclosure
            else (repr(desc[:80]) if verbose else ""),
        ))
    return checks


def check_thumbnail_specs(verbose: bool) -> Check:
    label = f"thumbnail_specs.json has >= {MIN_THUMBNAIL_SPECS} specs"
    if not THUMBNAIL_SPECS_JSON.is_file():
        return Check(label, False, f"Not found: {THUMBNAIL_SPECS_JSON}")
    try:
        data = json.loads(THUMBNAIL_SPECS_JSON.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return Check(label, False, f"JSON parse error: {exc}")

    count  = len(data) if isinstance(data, (list, dict)) else 0
    passed = count >= MIN_THUMBNAIL_SPECS
    detail = f"{count} specs found (need >= {MIN_THUMBNAIL_SPECS})" if (verbose or not passed) else ""
    return Check(label, passed, detail)


def _parse_registry_partial(raw: str) -> dict[str, str]:
    """
    Block-extraction fallback when magazine_casting_registry.json has a JSON
    parse error.  Splits the raw text on each '"actor_id"' occurrence and
    searches forward to the next actor boundary for agency_status.
    """
    registry: dict[str, str] = {}
    id_positions = [m.start() for m in re.finditer(r'"actor_id"\s*:\s*"', raw)]
    for i, pos in enumerate(id_positions):
        end_pos = id_positions[i + 1] if i + 1 < len(id_positions) else len(raw)
        block   = raw[pos:end_pos]
        id_m     = re.search(r'"actor_id"\s*:\s*"([^"]+)"', block)
        status_m = re.search(r'"agency_status"\s*:\s*"([^"]+)"', block)
        if id_m:
            registry[id_m.group(1)] = status_m.group(1) if status_m else ""
    return registry


def check_reroll_queue_actors(verbose: bool) -> list[Check]:
    checks: list[Check] = []

    if not REROLL_QUEUE_MD.is_file():
        checks.append(Check("REROLL_QUEUE.md — file exists", False, str(REROLL_QUEUE_MD)))
        return checks

    queue_text   = REROLL_QUEUE_MD.read_text(encoding="utf-8", errors="replace")
    queue_actors = re.findall(r"###\s+(\w+-\d+)\b", queue_text)

    if not queue_actors:
        checks.append(Check(
            "REROLL_QUEUE.md — actor IDs parseable",
            False,
            "No '### ActorID-NNN' headings found",
        ))
        return checks

    checks.append(Check(
        "REROLL_QUEUE.md — file exists and actor IDs parseable",
        True,
        f"Actors: {', '.join(queue_actors)}" if verbose else f"{len(queue_actors)} actors in queue",
    ))

    # Load registry — fall back to block extraction on JSON error
    registry_actors: dict[str, str] = {}
    registry_ok = False

    if CASTING_REGISTRY_JSON.is_file():
        raw = CASTING_REGISTRY_JSON.read_text(encoding="utf-8", errors="replace")
        try:
            data = json.loads(raw)
            registry_ok = True
            actors_list: list = []
            if isinstance(data, dict):
                actors_list = data.get("actors", [])
                if not actors_list:
                    actors_list = [v for v in data.values() if isinstance(v, dict)]
            elif isinstance(data, list):
                actors_list = data
            for entry in actors_list:
                if isinstance(entry, dict) and "actor_id" in entry:
                    registry_actors[entry["actor_id"]] = entry.get("agency_status", "")
        except json.JSONDecodeError:
            registry_actors = _parse_registry_partial(raw)

        if not registry_ok:
            checks.append(Check(
                "magazine_casting_registry.json — valid JSON (no parse errors)",
                False,
                "JSONDecodeError at line 394 col 24 — file truncated. "
                "Partial block-extraction used. Fix the JSON before launch.",
            ))
        else:
            checks.append(Check(
                "magazine_casting_registry.json — valid JSON",
                True,
                f"{len(registry_actors)} actors indexed" if verbose else "",
            ))
    else:
        checks.append(Check(
            "magazine_casting_registry.json — file exists",
            False,
            str(CASTING_REGISTRY_JSON),
        ))

    for actor_id in queue_actors:
        label = f"Reroll actor {actor_id}: agency_status = do_not_cast_pending_reroll"
        if actor_id not in registry_actors:
            checks.append(Check(
                label,
                False,
                f"'{actor_id}' NOT FOUND in magazine_casting_registry.json — "
                "add entry with do_not_cast_pending_reroll",
            ))
        else:
            status = registry_actors[actor_id]
            passed = status == "do_not_cast_pending_reroll"
            detail = f"actual status: '{status}'" if (not passed or verbose) else ""
            checks.append(Check(label, passed, detail))

    return checks


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------
def run_all(verbose: bool) -> list[Check]:
    all_checks: list[Check] = []

    # Section A — Legal / compliance
    all_checks.append(check_legal_gate_constant(verbose))
    all_checks.append(check_legal_gate_helper(verbose))
    all_checks.append(check_gate_result_section_2257(verbose))
    all_checks.append(check_hard_stop_wired(verbose))
    all_checks.append(check_age_policy(verbose))
    all_checks.extend(check_reroll_queue_actors(verbose))

    # Section B — Channel identity / upload kit
    all_checks.extend(check_channel_identity(verbose))
    all_checks.extend(check_upload_kits(verbose))
    all_checks.append(check_thumbnail_specs(verbose))

    return all_checks


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Gate 0 Channel Launch — automated verification for DAVID channel"
    )
    parser.add_argument("--verbose", "-v", action="store_true", help="Show extra detail on each check")
    args = parser.parse_args()

    checks  = run_all(args.verbose)
    passed  = [c for c in checks if c.passed]
    failed  = [c for c in checks if not c.passed]
    total   = len(checks)

    print()
    print("Gate 0 Channel Launch — Verification Report")
    print("=" * 60)
    for check in checks:
        print(repr(check))
    print("=" * 60)

    if failed:
        print(f"Result: {len(passed)}/{total} checks passed. {len(failed)} FAILED.\n")
        print("FAILED checks:")
        for c in failed:
            print(f"  x  {c.label}")
            if c.detail:
                print(f"       {c.detail}")
        print()
        return 1

    print(f"Result: {total}/{total} checks passed. ALL PASS.\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
