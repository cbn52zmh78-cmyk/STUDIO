#!/usr/bin/env python3
"""Validate Royal Tongues slate: Gate 0 + intake + render_longform --script-only."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

SLATE_DIR = Path(__file__).resolve().parent
ROOT = SLATE_DIR.parents[3]
INTAKE = ROOT / "STUDIO" / "Pipeline" / "production_intake.py"
RENDER = ROOT / "DAVID" / "scripts" / "render_longform.py"
SCRIPTS = ROOT / "DAVID" / "scripts" / "longform_scripts"

EPISODES = [
    "david_eleanor_aquitaine_v1",
    "david_richard_lionheart_v1",
    "david_elizabeth_tudor_v1",
]


def run(cmd: list[str]) -> int:
    return subprocess.run(cmd, cwd=ROOT).returncode


def main() -> int:
    ok = True
    results: list[dict] = []

    for slug in EPISODES:
        concept = SLATE_DIR / f"{slug}.concept.json"
        script = SCRIPTS / f"{slug}_script.json"
        row = {"slug": slug, "intake": "?", "script_only": "?", "gate_verdict": "?"}

        code = run([sys.executable, str(INTAKE), str(concept), "-o", str(script)])
        row["intake"] = "OK" if code == 0 else f"FAIL {code}"
        ok = ok and code == 0

        if script.is_file():
            data = json.loads(script.read_text(encoding="utf-8"))
            row["gate_verdict"] = (data.get("intake") or {}).get("gate_0", {}).get("verdict", "?")
            row["format_id"] = data.get("format_id")
            row["sources"] = len(
                ((data.get("intake") or {}).get("historical_figure") or {}).get("sources")
                or (data.get("provenance_card") or {}).get("sources")
                or []
            )

        code = run([sys.executable, str(RENDER), str(script), "--script-only"])
        row["script_only"] = "OK" if code == 0 else f"FAIL {code}"
        ok = ok and code == 0

        results.append(row)
        blocked = row["gate_verdict"] == "RED"
        passed = row["intake"] == "OK" and row["script_only"] == "OK" and not blocked
        icon = "✓" if passed else "✗"
        print(
            f"{icon} {slug}: gate={row['gate_verdict']} intake={row['intake']} "
            f"script-only={row['script_only']} sources={row.get('sources', 0)}"
        )
        if blocked:
            ok = False

    (SLATE_DIR / "validation_report.json").write_text(
        json.dumps(results, indent=2), encoding="utf-8"
    )
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())