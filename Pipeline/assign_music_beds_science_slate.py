#!/usr/bin/env python3
"""T5 #182 — stamp clearance_manifest music beds across science slates."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
ARTIFACTS = ROOT / "artifacts"
ASTRO = ROOT / "STUDIO" / "Pipeline" / "Concepts" / "astro_mini_slate"
MOLECULAR = ROOT / "STUDIO" / "Pipeline" / "Concepts" / "molecular_mini_slate"
SCIENCE = ROOT / "STUDIO" / "Pipeline" / "Concepts" / "science"
INTAKE = ROOT / "STUDIO" / "Pipeline" / "production_intake.py"
LONGFORM = ROOT / "DAVID" / "scripts" / "longform_scripts"

sys.path.insert(0, str(ARTIFACTS))
from lib.bootstrap import ensure_paths

ensure_paths()
sys.path.insert(0, str(ARTIFACTS / "legal"))
from music_clearance import format_bed_declaration, load_manifest, reload_manifest  # noqa: E402

# slug → bed (lane-matched)
SCIENCE_BEDS: dict[str, tuple[str, str]] = {
    # (bed_id, slate_group)
    "science_black_hole_anatomy_v1": ("BED-COS-002", "astro"),
    "science_star_lifecycle_v1": ("BED-COS-001", "astro"),
    "science_galaxy_formation_v1": ("BED-COS-002", "astro"),
    "science_protein_folding_v1": ("BED-CLI-001", "molecular"),
    "science_dna_replication_v1": ("BED-CLI-002", "molecular"),
    "science_immune_checkpoint_v1": ("BED-CLI-001", "molecular"),
    "julian_why_sky_blue_60s": ("BED-PHY-001", "physics"),
}

CONCEPT_DIRS: dict[str, Path] = {
    "science_black_hole_anatomy_v1": ASTRO,
    "science_star_lifecycle_v1": ASTRO,
    "science_galaxy_formation_v1": ASTRO,
    "science_protein_folding_v1": MOLECULAR,
    "science_dna_replication_v1": MOLECULAR,
    "science_immune_checkpoint_v1": MOLECULAR,
    "julian_why_sky_blue_60s": SCIENCE,
}

MUSIC_LINE_RE = re.compile(
    r"^(Music(?:\s+plan|\s+bed)?|Music)\s*[:=].*$",
    re.I,
)


def _stamp_concept(concept_path: Path, bed_id: str) -> None:
    concept = json.loads(concept_path.read_text(encoding="utf-8"))
    gate = dict(concept.get("gate_0") or {})
    gate.pop("music_plan", None)
    gate["music_bed_id"] = bed_id
    concept["gate_0"] = gate
    concept_path.write_text(json.dumps(concept, indent=2) + "\n", encoding="utf-8")


def _stamp_brief(brief_path: Path, bed_id: str) -> None:
    if not brief_path.is_file():
        return
    line = format_bed_declaration(bed_id)
    out_lines: list[str] = []
    replaced = False
    for raw in brief_path.read_text(encoding="utf-8").splitlines():
        if MUSIC_LINE_RE.match(raw.strip()) or re.search(r"\bMusic:\s*BED-", raw, re.I):
            if not replaced:
                out_lines.append(line)
                replaced = True
            continue
        out_lines.append(raw)
    if not replaced:
        out_lines.append(line)
    brief_path.write_text("\n".join(out_lines) + "\n", encoding="utf-8")


def _run_intake(concept_path: Path) -> dict[str, Any]:
    proc = subprocess.run(
        [sys.executable, str(INTAKE), str(concept_path)],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    slug = json.loads(concept_path.read_text(encoding="utf-8"))["slug"]
    script_path = LONGFORM / f"{slug}_script.json"
    if not script_path.is_file():
        raise RuntimeError(f"Intake failed for {slug}: {proc.stdout}\n{proc.stderr}")
    script = json.loads(script_path.read_text(encoding="utf-8"))
    gate = script["intake"]["gate_0"]
    return {
        "slug": slug,
        "bed_id": gate.get("music_bed_id"),
        "row_2": gate.get("row_2_music_sync")
        or gate.get("checklist_domains", {}).get("row_2_music_sync"),
        "verdict": gate.get("verdict"),
    }


def _track_meta(bed_id: str) -> dict[str, str]:
    track = load_manifest()["tracks"][bed_id]
    return {
        "bed_id": bed_id,
        "lane": track["lane"],
        "title": track["title"],
        "license": track["license"],
    }


def main() -> int:
    reload_manifest()
    rows: list[dict[str, Any]] = []

    for slug, (bed_id, group) in SCIENCE_BEDS.items():
        base = CONCEPT_DIRS[slug]
        concept = base / f"{slug}.concept.json"
        brief = base / f"{slug}_brief.txt"
        if not concept.is_file():
            raise FileNotFoundError(concept)
        _stamp_concept(concept, bed_id)
        _stamp_brief(brief, bed_id)
        row = _run_intake(concept)
        meta = _track_meta(bed_id)
        rows.append(
            {
                "slate": group,
                "slug": slug,
                "bed_id": bed_id,
                "lane": meta["lane"],
                "track": meta["title"],
                "license": meta["license"],
                "row_2": row["row_2"],
                "gate_verdict": row["verdict"],
            }
        )

    out = ROOT / "STUDIO" / "Music_Sound" / "science_music_assignments.json"
    payload = {
        "version": "1.0",
        "task": "T5-182",
        "new_lanes": ["physics-precision", "chemistry-lab"],
        "reserve_beds": {
            "chemistry": ["BED-CHE-001", "BED-CHE-002"],
            "physics_alt": ["BED-PHY-002"],
        },
        "assignments": rows,
    }
    out.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    failures = [r for r in rows if r["row_2"] != "PASS"]
    print(json.dumps(rows, indent=2))
    print(f"\nWrote {out.relative_to(ROOT)}")
    if failures:
        print(f"FAIL: {len(failures)} missing row_2 PASS", file=sys.stderr)
        return 1
    print(f"PASS: {len(rows)} science productions stamped — row_2 PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())