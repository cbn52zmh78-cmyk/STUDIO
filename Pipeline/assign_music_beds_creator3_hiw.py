#!/usr/bin/env python3
"""T5 #200 — Creator #3 How It Works beds + chem/physics concept stamps (no render)."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
ARTIFACTS = ROOT / "artifacts"
CHEM_PHYSICS = ROOT / "STUDIO" / "Pipeline" / "Concepts" / "chem_physics_mini_slate"
INTAKE = ROOT / "STUDIO" / "Pipeline" / "production_intake.py"
LONGFORM = ROOT / "DAVID" / "scripts" / "longform_scripts"

sys.path.insert(0, str(ARTIFACTS))
from lib.bootstrap import ensure_paths

ensure_paths()
sys.path.insert(0, str(ARTIFACTS / "legal"))
from music_clearance import format_bed_declaration, load_manifest, reload_manifest  # noqa: E402

# slug → (bed_id, slate_group)
CREATOR3_BEDS: dict[str, tuple[str, str]] = {
    "science_covalent_bonding_v1": ("BED-HIW-002", "chem_physics"),
    "science_ionic_crystal_v1": ("BED-HIW-001", "chem_physics"),
    "science_electromagnetism_v1": ("BED-HIW-002", "chem_physics"),
}

MUSIC_LINE_RE = re.compile(
    r"^(Music(?:\s+plan|\s+bed)?|Music)\s*[:=].*$",
    re.I,
)

_MANIFEST_CHANNELS = frozenset({"social", "streaming", "theatrical", "festival", "client"})


def _stamp_concept(concept_path: Path, bed_id: str) -> None:
    concept = json.loads(concept_path.read_text(encoding="utf-8"))
    gate = dict(concept.get("gate_0") or {})
    gate.pop("music_plan", None)
    gate["music_bed_id"] = bed_id
    raw_channels = [str(c).lower().strip() for c in (gate.get("channels") or []) if str(c).strip()]
    cleared = [c for c in raw_channels if c in _MANIFEST_CHANNELS]
    if not cleared or len(cleared) < len(raw_channels):
        gate["channels"] = cleared or ["social", "streaming"]
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

    for slug, (bed_id, group) in CREATOR3_BEDS.items():
        concept = CHEM_PHYSICS / f"{slug}.concept.json"
        brief = CHEM_PHYSICS / f"{slug}_brief.txt"
        if not concept.is_file():
            raise FileNotFoundError(concept)
        _stamp_concept(concept, bed_id)
        _stamp_brief(brief, bed_id)
        row = _run_intake(concept)
        meta = _track_meta(bed_id)
        rows.append(
            {
                "creator": "creator_3_observable",
                "series": "How It Works",
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

    out = ROOT / "STUDIO" / "Music_Sound" / "creator3_music_assignments.json"
    manifest = load_manifest()
    hiw_tracks = {
        bed_id: {
            "title": meta["title"],
            "lane": meta["lane"],
            "license": meta["license"],
            "domain": manifest["tracks"][bed_id].get("domain", ""),
        }
        for bed_id in ("BED-HIW-001", "BED-HIW-002")
        for meta in [_track_meta(bed_id)]
    }
    payload = {
        "version": "1.0",
        "task": "T5-200",
        "creator": "creator_3_observable",
        "channel": "Observable",
        "series": "How It Works",
        "new_lane": "how-it-works",
        "beds": hiw_tracks,
        "reserve_beds": {
            "chemistry": ["BED-CHE-001", "BED-CHE-002"],
            "physics": ["BED-PHY-001", "BED-PHY-002"],
        },
        "assignments": rows,
    }
    out.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    failures = [r for r in rows if r["row_2"] != "PASS"]
    print(json.dumps(payload, indent=2))
    print(f"\nWrote {out.relative_to(ROOT)}")
    if failures:
        print(f"FAIL: {len(failures)} missing row_2 PASS", file=sys.stderr)
        return 1
    print(f"PASS: {len(rows)} chem/physics concepts stamped — row_2 PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())