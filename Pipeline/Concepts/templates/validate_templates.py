#!/usr/bin/env python3
"""Round-trip validator for concept templates.

Substitutes [BRACKET] placeholders with minimal valid values, then runs:
  production_intake.py → render_longform.py --script-only

Exit 0 only if all six formats pass.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

TEMPLATES_DIR = Path(__file__).resolve().parent
ROOT = TEMPLATES_DIR.parents[3]  # .../Grok Projects
INTAKE = ROOT / "STUDIO" / "Pipeline" / "production_intake.py"
RENDER = ROOT / "DAVID" / "scripts" / "render_longform.py"
SCRIPTS_OUT = ROOT / "DAVID" / "scripts" / "longform_scripts"

# Validation actor_id substitutions (bracketed actor_id fields)
ACTOR_FILLS = {
    "narrative-short-film": "Aiko-001",
    "conversational-companion": "Amara-001",
    "explainer-ad": "Julian-001",
    "historical-figure-documentary": "David-001",
    "science-explainer": "Julian-001",
}

BRACKET_RE = re.compile(r"\[[^\]]+\]")


def fill_brackets(value: str, *, slug: str, key: str = "") -> str:
    if "[" not in value:
        return value
    if key == "slug" or value.startswith("[slug"):
        return slug
    if key == "title":
        return f"Template Validate — {slug.replace('_', ' ')}"
    if key == "actor_id":
        return value  # filled separately per format
    if key == "speech_text":
        return "Template validation spoken line."
    if key == "death_year":
        return 415
    if key == "figure_id":
        return "template_figure"
    if key == "era":
        return "Template Era"
    if key == "citation":
        return "Template Source Citation"
    if key == "attestation":
        return "RECONSTRUCTED"
    if key == "subject_id":
        return "template_subject"
    if key == "domain":
        return "Template Domain"
    if key == "phenomenon":
        return "Template Phenomenon"
    if key == "visualization_prompt":
        return "Template scientific visualization."
    if key == "music_bed_id":
        return ""
    if key in ("title", "subtitle", "cta", "credit_line", "legal_line") or "BRAND" in value:
        return "Template"
    if key == "on_screen":
        return "Template"
    if key == "tags" or value.startswith("[tag") or value.startswith("[genre"):
        return "template"
    return BRACKET_RE.sub("template", value)


def fill_value(val: Any, format_id: str, slug: str, key: str = "") -> Any:
    if isinstance(val, dict):
        return {k: fill_value(v, format_id, slug, k) for k, v in val.items()}
    if isinstance(val, list):
        return [fill_value(item, format_id, slug, key) for item in val]
    if isinstance(val, str):
        if key == "actor_id" and "[" in val:
            return ACTOR_FILLS.get(format_id, "Julian-001")
        return fill_brackets(val, slug=slug, key=key)
    return val


def fill_concept(raw: dict[str, Any], format_id: str, slug: str) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, val in raw.items():
        if key == "_template":
            continue
        out[key] = fill_value(val, format_id, slug, key)
    if format_id in ("documentary-host", "historical-figure-documentary", "science-explainer"):
        gate = dict(out.get("gate_0") or {})
        gate.setdefault("human_signoff", True)
        out["gate_0"] = gate
    if out.get("music_bed_id") in (None, "", "template"):
        out.pop("music_bed_id", None)
    gate = out.get("gate_0")
    if isinstance(gate, dict) and gate.get("music_bed_id") in (None, "", "template"):
        gate.pop("music_bed_id", None)
    return out


def run(cmd: list[str], *, cwd: Path) -> int:
    print(">", " ".join(str(c) for c in cmd))
    return subprocess.run(cmd, cwd=cwd, check=False).returncode


def validate_one(template_path: Path) -> tuple[bool, str]:
    raw = json.loads(template_path.read_text(encoding="utf-8"))
    format_id = raw.get("format_id") or raw.get("_template", {}).get("format_id", "unknown")
    slug = f"template_validate_{format_id.replace('-', '_')}"
    concept = fill_concept(raw, format_id, slug)

    tmp_concept = TEMPLATES_DIR / f".validate_{slug}.concept.json"
    script_path = SCRIPTS_OUT / f"{slug}_script.json"
    tmp_concept.write_text(json.dumps(concept, indent=2, ensure_ascii=False), encoding="utf-8")

    try:
        intake_rc = run(
            [sys.executable, str(INTAKE), str(tmp_concept), "-o", str(script_path)], cwd=ROOT
        )
        if intake_rc not in (0, 3) or not script_path.is_file():
            return False, f"{format_id}: intake failed (rc={intake_rc})"
        if run(
            [sys.executable, str(RENDER), str(script_path), "--script-only"],
            cwd=ROOT,
        ) != 0:
            return False, f"{format_id}: render_longform --script-only failed"
        return True, f"{format_id}: OK → {script_path.name}"
    finally:
        if tmp_concept.exists():
            tmp_concept.unlink()


def main() -> int:
    templates = sorted(TEMPLATES_DIR.glob("*.concept.template.json"))
    if len(templates) != 6:
        print(f"Expected 6 templates, found {len(templates)}")
        return 1

    ok = True
    for path in templates:
        passed, msg = validate_one(path)
        icon = "✓" if passed else "✗"
        print(f"{icon} {msg}")
        ok = ok and passed

    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())