#!/usr/bin/env python3
"""T2 #178 orchestrator — render + lock all science + figure plates; emit domain lock counts."""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

WORKSPACE = Path(__file__).resolve().parents[2]
PIPELINE = WORKSPACE / "Studio" / "Pipeline"
SUMMARY_PATH = WORKSPACE / "Science" / "reference_plates" / "t2_178_plate_lock_summary.json"
LIBRARY = WORKSPACE / "Science" / "reference_plates" / "science_plate_library_v1.json"


def _run(script: str, *extra: str) -> None:
    cmd = [sys.executable, str(PIPELINE / script), *extra]
    print(f"\n>>> {' '.join(cmd)}")
    subprocess.run(cmd, cwd=str(WORKSPACE), check=True)


def _flip_molecular_library() -> None:
    """Ensure library v1 molecular entries match manifest PLATE_LOCKED state."""
    lib = json.loads(LIBRARY.read_text(encoding="utf-8"))
    manifest_path = WORKSPACE / "Science" / "reference_plates" / "science_plate_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    locked = {
        pid: entry for pid, entry in manifest.get("plates", {}).items()
        if entry.get("status") == "PLATE_LOCKED" and entry.get("domain") == "molecular"
    }
    for p in lib["plates"]:
        if p["plate_id"] in locked:
            p["plate_spec"]["status"] = "PLATE_LOCKED"
            p["plate_spec"]["locked_at"] = locked[p["plate_id"]].get("locked_at")
    LIBRARY.write_text(json.dumps(lib, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _count_locked() -> dict[str, Any]:
    summary: dict[str, Any] = {
        "issue": 178,
        "task": "T2 #178 — render + lock plates with fidelity notes",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "locked_by_domain": {},
        "blocked": {},
        "notes": {},
    }

    astro_notes = WORKSPACE / "Science" / "reference_plates" / "astro" / "t2_178_astro_fidelity_review.json"
    if astro_notes.is_file():
        data = json.loads(astro_notes.read_text(encoding="utf-8"))
        summary["locked_by_domain"]["astro"] = len(data.get("plates", []))
        summary["notes"]["astro"] = str(astro_notes)

    mol_notes = WORKSPACE / "Science" / "reference_plates" / "molecular" / "actors_172_fidelity_review.json"
    if mol_notes.is_file():
        data = json.loads(mol_notes.read_text(encoding="utf-8"))
        summary["locked_by_domain"]["molecular"] = len(data.get("plates", []))
        summary["notes"]["molecular"] = str(mol_notes)

    r4_notes = WORKSPACE / "Science" / "reference_plates" / "r4_178_fidelity_review.json"
    if r4_notes.is_file():
        data = json.loads(r4_notes.read_text(encoding="utf-8"))
        chem = sum(1 for p in data.get("plates", []) if p.get("domain") == "chemistry")
        phys = sum(1 for p in data.get("plates", []) if p.get("domain") == "physics")
        summary["locked_by_domain"]["chemistry"] = chem
        summary["locked_by_domain"]["physics"] = phys
        summary["notes"]["chemistry_physics"] = str(r4_notes)
        summary["blocked"].update(data.get("blocked", {}))

    fig_notes = WORKSPACE / "History" / "Historical_Figures_Bible" / "registry" / "t2_178_figure_fidelity_review.json"
    if fig_notes.is_file():
        data = json.loads(fig_notes.read_text(encoding="utf-8"))
        summary["locked_by_domain"]["figures"] = len(data.get("figures", []))
        summary["notes"]["figures"] = str(fig_notes)

    summary["total_locked"] = sum(summary["locked_by_domain"].values())
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description="T2 #178 plate lock orchestrator")
    parser.add_argument("--skip-astro", action="store_true")
    parser.add_argument("--skip-molecular", action="store_true")
    parser.add_argument("--skip-r4", action="store_true")
    parser.add_argument("--skip-figures", action="store_true")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--summary-only", action="store_true")
    args = parser.parse_args()

    if args.summary_only:
        summary = _count_locked()
        SUMMARY_PATH.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(json.dumps(summary, indent=2))
        return 0

    force = ["--force"] if args.force else []

    if not args.skip_astro:
        _run("build_astro_r1_plate_lock.py", *force)

    if not args.skip_molecular:
        _flip_molecular_library()
        mol_meta = WORKSPACE / "Science" / "reference_plates" / "molecular" / "protein_hemoglobin_reference.json"
        if not mol_meta.is_file() or args.force:
            _run("build_molecular_at2_plates.py", *force)

    if not args.skip_r4:
        _run("build_r4_chem_physics_plates.py", *force)

    if not args.skip_figures:
        _run("build_figure_reconstruction_bible_v1.py", *force)

    summary = _count_locked()
    SUMMARY_PATH.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("\n=== T2 #178 LOCK SUMMARY ===")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())