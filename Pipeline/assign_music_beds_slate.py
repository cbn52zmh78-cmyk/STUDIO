#!/usr/bin/env python3
"""T5 #143 — stamp clearance_manifest music beds across dead-language slate + lane samples."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
ARTIFACTS = ROOT / "artifacts"
DEAD_LANG = ROOT / "STUDIO" / "Pipeline" / "Concepts" / "dead_languages"
INTAKE = ROOT / "STUDIO" / "Pipeline" / "production_intake.py"
LONGFORM = ROOT / "DAVID" / "scripts" / "longform_scripts"
BATCH_SCRIPTS = ROOT / "DAVID" / "batches" / "T3_dryrun" / "scripts"

sys.path.insert(0, str(ARTIFACTS))
from lib.bootstrap import ensure_paths

ensure_paths()
sys.path.insert(0, str(ARTIFACTS / "legal"))
from music_clearance import format_bed_declaration, load_manifest  # noqa: E402
from legal_gate import LegalGate  # noqa: E402

# slug → bed id (manifest lane-matched)
EPISODE_BEDS: dict[str, str] = {
    "david_latin_corpus_v1": "BED-DOC-001",
    "david_ancient_greek_corpus_v1": "BED-DOC-002",
    "david_old_english_corpus_v1": "BED-DOC-001",
    "david_old_norse_corpus_v1": "BED-DOC-002",
    "david_gothic_corpus_v1": "BED-THR-001",
    "david_sumerian_corpus_v1": "BED-DOC-002",
}

LANE_SAMPLE_BEDS: dict[str, dict[str, Any]] = {
    "movies_lane_sample_v1": {
        "bed_id": "BED-THR-002",
        "rating": "PG-13",
        "channels": ["social", "streaming"],
        "scripts": [
            ROOT / "STUDIO" / "Productions" / "Narrative" / "movies_lane_sample_v1" / "movies_lane_sample_v1_script.json",
            ROOT / "STUDIO" / "Productions" / "Narrative" / "movies_lane_sample_v1_longform_v1" / "movies_lane_sample_v1_script.json",
            ROOT / "DAVID" / "productions" / "movies_lane_sample_v1_longform_v1" / "movies_lane_sample_v1_script.json",
        ],
    },
    "flowdesk_explainer_v1": {
        "bed_id": "BED-UP-001",
        "rating": "PG",
        "channels": ["social", "client"],
        "scripts": [
            ROOT / "STUDIO" / "Productions" / "Editorial" / "flowdesk_explainer_v1_longform_v1" / "flowdesk_explainer_v1_script.json",
        ],
    },
    "gfe_companion_sage_proof_v1": {
        "bed_id": "BED-WARM-001",
        "rating": "PG",
        "channels": ["social"],
        "scripts": [
            ROOT / "STUDIO" / "Productions" / "Companion" / "gfe_companion_sage_proof_v1_longform_v1" / "gfe_companion_sage_proof_v1_script.json",
        ],
    },
}


def _stamp_concept(concept_path: Path, bed_id: str) -> None:
    concept = json.loads(concept_path.read_text(encoding="utf-8"))
    gate = dict(concept.get("gate_0") or {})
    gate.pop("music_plan", None)
    gate["music_bed_id"] = bed_id
    concept["gate_0"] = gate
    concept_path.write_text(json.dumps(concept, indent=2) + "\n", encoding="utf-8")


def _stamp_brief(brief_path: Path, bed_id: str) -> None:
    text = brief_path.read_text(encoding="utf-8")
    line = format_bed_declaration(bed_id)
    if "Music plan:" in text or "Music bed:" in text:
        lines = []
        for raw in text.splitlines():
            if raw.lower().startswith("music plan:") or raw.lower().startswith("music bed:"):
                lines.append(line)
            else:
                lines.append(raw)
        text = "\n".join(lines)
    else:
        text = text.rstrip() + "\n" + line + "\n"
    brief_path.write_text(text, encoding="utf-8")


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
        "row_2": gate.get("row_2_music_sync") or gate.get("checklist_domains", {}).get("row_2_music_sync"),
        "verdict": gate.get("verdict"),
        "intake_exit": proc.returncode,
    }


def _sync_batch_script(slug: str) -> None:
    src = LONGFORM / f"{slug}_script.json"
    dst = BATCH_SCRIPTS / f"{slug}_480p_script.json"
    if not src.is_file() or not BATCH_SCRIPTS.is_dir():
        return
    script = json.loads(src.read_text(encoding="utf-8"))
    script["config"]["resolution"] = "480p"
    dst.write_text(json.dumps(script, indent=2) + "\n", encoding="utf-8")


def _gate_stamp_for_lane(slug: str, bed_id: str, rating: str, channels: list[str]) -> dict[str, Any]:
    brief = f"Project: {slug}\n{format_bed_declaration(bed_id)}\nAI disclosure planned."
    gate = LegalGate()
    result = gate.review(brief, slug, target_rating=rating, channels=channels, has_performers=True)
    return {
        "version": "1.3",
        "verdict": result.verdict,
        "blocked": result.verdict == "RED",
        "requires_human_signoff": result.verdict in ("YELLOW", "COUNSEL"),
        "human_signoff": True,
        "target_rating": rating,
        "channels": channels,
        "checklist_domains": result.checklist_domains,
        "music_bed_id": bed_id,
        "music_clearance_manifest": "STUDIO/Music_Sound/clearance_manifest.json",
        "row_2_music_sync": result.checklist_domains.get("row_2_music_sync"),
    }


def _stamp_lane_script(script_path: Path, gate_stamp: dict[str, Any], bed_id: str) -> None:
    if not script_path.is_file():
        return
    script = json.loads(script_path.read_text(encoding="utf-8"))
    script.setdefault("config", {})["music_bed"] = {
        "track_id": bed_id,
        "manifest": "STUDIO/Music_Sound/clearance_manifest.json",
    }
    script.setdefault("intake", {})["gate_0"] = gate_stamp
    script_path.write_text(json.dumps(script, indent=2) + "\n", encoding="utf-8")


def _track_meta(bed_id: str) -> dict[str, str]:
    track = load_manifest()["tracks"][bed_id]
    return {
        "bed_id": bed_id,
        "lane": track["lane"],
        "title": track["title"],
        "license": track["license"],
    }


def main() -> int:
    rows: list[dict[str, Any]] = []

    for slug, bed_id in EPISODE_BEDS.items():
        concept = DEAD_LANG / f"{slug}.concept.json"
        brief = DEAD_LANG / f"{slug}_brief.txt"
        _stamp_concept(concept, bed_id)
        _stamp_brief(brief, bed_id)
        row = _run_intake(concept)
        _sync_batch_script(slug)
        meta = _track_meta(bed_id)
        rows.append(
            {
                "group": "episode",
                "slug": slug,
                "bed_id": bed_id,
                "lane": meta["lane"],
                "track": meta["title"],
                "license": meta["license"],
                "row_2": row["row_2"],
                "gate_verdict": row["verdict"],
            }
        )

    for slug, cfg in LANE_SAMPLE_BEDS.items():
        bed_id = cfg["bed_id"]
        gate_stamp = _gate_stamp_for_lane(slug, bed_id, cfg["rating"], cfg["channels"])
        for script_path in cfg["scripts"]:
            _stamp_lane_script(script_path, gate_stamp, bed_id)
        meta = _track_meta(bed_id)
        rows.append(
            {
                "group": "lane_sample",
                "slug": slug,
                "bed_id": bed_id,
                "lane": meta["lane"],
                "track": meta["title"],
                "license": meta["license"],
                "row_2": gate_stamp["row_2_music_sync"],
                "gate_verdict": gate_stamp["verdict"],
            }
        )

    # Stamp julian_flowdesk concept (pipeline worked example)
    julian = ROOT / "STUDIO" / "Pipeline" / "Concepts" / "julian_flowdesk_explainer_v1.concept.json"
    if julian.is_file():
        concept = json.loads(julian.read_text(encoding="utf-8"))
        concept.setdefault("gate_0", {})["music_bed_id"] = "BED-UP-002"
        julian.write_text(json.dumps(concept, indent=2) + "\n", encoding="utf-8")

    out = ROOT / "STUDIO" / "Music_Sound" / "slate_music_assignments.json"
    out.write_text(json.dumps({"version": "1.0", "assignments": rows}, indent=2) + "\n", encoding="utf-8")

    failures = [r for r in rows if r["row_2"] != "PASS"]
    print(json.dumps(rows, indent=2))
    print(f"\nWrote {out.relative_to(ROOT)}")
    if failures:
        print(f"FAIL: {len(failures)} assignments missing row_2 PASS", file=sys.stderr)
        return 1
    print(f"PASS: {len(rows)} productions stamped — row_2 PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())