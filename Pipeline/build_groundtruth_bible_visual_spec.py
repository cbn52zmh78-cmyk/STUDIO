#!/usr/bin/env python3
"""ACTORS #241 — GroundTruth bible visual/design spec (no render).

Writes and validates the machine-readable house style for cited GroundTruth bibles:
academic typography, citation chips, status taxonomy, gate stamp, gap/disclosure
treatment — unified across compliance SoT, science synthesis, and figure bibles.
"""
from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

WORKSPACE = Path(__file__).resolve().parents[2]
SPEC_PATH = (
    WORKSPACE
    / "STUDIO"
    / "Reference_Library"
    / "style_bibles"
    / "GroundTruth_Bible_Visual_Design_Spec_v1.json"
)
NOTES_PATH = SPEC_PATH.parent / "actors_241_fidelity_review.json"

REQUIRED_TOP = (
    "artifact",
    "version",
    "issue",
    "status",
    "render",
    "principle",
    "tokens",
    "citation_systems",
    "status_taxonomy",
    "knowledge_gate",
    "components",
    "vertical_variants",
    "render_surfaces",
    "implementation_anchors",
    "prohibitions",
)

HEX_RE = re.compile(r"^#[0-9a-fA-F]{6}$")
WEDGE_STATUSES = (
    "FOUND",
    "EXEMPT",
    "REQUIRES_CONFIRMATION",
    "NOT FOUND",
    "ACCESS_RESTRICTED",
    "SAMPLE",
)


def load_spec() -> dict[str, Any]:
    return json.loads(SPEC_PATH.read_text(encoding="utf-8"))


def validate_spec(spec: dict[str, Any]) -> list[str]:
    issues: list[str] = []

    for key in REQUIRED_TOP:
        if key not in spec:
            issues.append(f"missing top-level key: {key}")

    if spec.get("issue") != 241:
        issues.append(f"issue must be 241, got {spec.get('issue')}")
    if spec.get("render") is not False:
        issues.append("render must be false for #241 (spec-only)")
    if spec.get("status") != "SPEC_LOCKED":
        issues.append(f"status must be SPEC_LOCKED, got {spec.get('status')}")

    colors = spec.get("tokens", {}).get("color", {})
    for name, value in colors.items():
        if value is not None and not HEX_RE.match(str(value)):
            issues.append(f"invalid hex token colors.{name}: {value}")

    taxonomy = spec.get("status_taxonomy", {})
    values = taxonomy.get("values", [])
    if list(values) != list(WEDGE_STATUSES):
        issues.append("status_taxonomy.values must match WEDGE_STATUS_VALUES order")
    for status in WEDGE_STATUSES:
        if status not in taxonomy.get("meanings", {}):
            issues.append(f"status_taxonomy.meanings missing: {status}")

    variants = spec.get("vertical_variants", {})
    for name in ("compliance_sot", "science_synthesis", "figure_bible"):
        if name not in variants:
            issues.append(f"vertical_variants missing: {name}")

    cites = spec.get("citation_systems", {})
    if "STD-CITE-001" not in cites or "APA7_INLINE" not in cites:
        issues.append("citation_systems must include STD-CITE-001 and APA7_INLINE")

    components = spec.get("components", {})
    for comp in (
        "title_block",
        "meta_rail",
        "gate_stamp",
        "claim_row",
        "datum_table",
        "references",
        "ai_disclosure",
        "gaps_to_close",
    ):
        if comp not in components:
            issues.append(f"components missing: {comp}")

    if "render_in_this_issue" not in spec.get("prohibitions", []):
        issues.append("prohibitions must include render_in_this_issue")

    for rel in spec.get("implementation_anchors", []):
        if not (WORKSPACE / rel).is_file():
            issues.append(f"implementation anchor missing: {rel}")

    return issues


def write_fidelity_review(spec: dict[str, Any], issues: list[str]) -> dict[str, Any]:
    review = {
        "task": "ACTORS #241",
        "artifact": "groundtruth_bible_visual_design_spec",
        "issue": 241,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "spec_path": str(SPEC_PATH.relative_to(WORKSPACE)).replace("\\", "/"),
        "render": False,
        "pass": len(issues) == 0,
        "issues": issues,
        "checks": {
            "spec_locked": spec.get("status") == "SPEC_LOCKED",
            "no_render_flag": spec.get("render") is False,
            "status_taxonomy_complete": len(spec.get("status_taxonomy", {}).get("values", [])) == 6,
            "vertical_variants": sorted(spec.get("vertical_variants", {}).keys()),
            "citation_systems": sorted(spec.get("citation_systems", {}).keys()),
            "implementation_anchors": len(spec.get("implementation_anchors", [])),
            "principle": spec.get("principle"),
        },
        "verticals": {
            k: {
                "citation_system": v.get("citation_system"),
                "gate": v.get("gate"),
                "outputs": v.get("outputs"),
            }
            for k, v in spec.get("vertical_variants", {}).items()
        },
    }
    NOTES_PATH.write_text(json.dumps(review, indent=2) + "\n", encoding="utf-8")
    return review


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate GroundTruth bible visual spec (#241)")
    parser.add_argument("--check-only", action="store_true", help="Validate without rewriting notes")
    args = parser.parse_args()

    if not SPEC_PATH.is_file():
        raise SystemExit(f"spec not found: {SPEC_PATH}")

    spec = load_spec()
    issues = validate_spec(spec)
    if not args.check_only:
        write_fidelity_review(spec, issues)

    if issues:
        for i in issues:
            print(f"FAIL: {i}")
        return 1

    print(f"SPEC_LOCKED: {SPEC_PATH}")
    print(f"Notes: {NOTES_PATH}")
    print(f"Principle: {spec['principle']} | Verticals: {', '.join(spec['vertical_variants'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())