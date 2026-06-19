#!/usr/bin/env python3
"""Validate dead-language slate: Gate 0 + intake + render_longform --script-only."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

SLATE_DIR = Path(__file__).resolve().parent
ROOT = SLATE_DIR.parents[3]
INTAKE = ROOT / "Studio" / "Pipeline" / "production_intake.py"
RENDER = ROOT / "DAVID" / "scripts" / "render_longform.py"
GATE = ROOT / "artifacts" / "legal" / "legal_gate.py"
SCRIPTS = ROOT / "DAVID" / "scripts" / "longform_scripts"

EPISODES = [
    # Launch six (eps 1-6)
    "david_latin_corpus_v1",
    "david_ancient_greek_corpus_v1",
    "david_old_english_corpus_v1",
    "david_old_norse_corpus_v1",
    "david_gothic_corpus_v1",
    "david_sumerian_corpus_v1",
    # Backlog (eps 7-12) - runway past launch (#168)
    "david_sanskrit_corpus_v1",
    "david_biblical_hebrew_corpus_v1",
    "david_akkadian_corpus_v1",
    "david_middle_egyptian_corpus_v1",
    "david_classical_nahuatl_corpus_v1",
    "david_old_church_slavonic_corpus_v1",
]


def run(cmd: list[str]) -> tuple[int, str]:
    p = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace")
    out = (p.stdout or "") + (p.stderr or "")
    return p.returncode, out.strip()


def main() -> int:
    ok = True
    results: list[dict] = []

    for slug in EPISODES:
        concept = SLATE_DIR / f"{slug}.concept.json"
        brief = SLATE_DIR / f"{slug}_brief.txt"
        script = SCRIPTS / f"{slug}_script.json"
        row = {"slug": slug, "gate": "?", "intake": "?", "script_only": "?"}

        code, out = run(
            [
                sys.executable,
                str(GATE),
                "--project",
                slug,
                "--file",
                str(brief),
                "--rating",
                "PG",
                "--channels",
                "social,streaming",
            ]
        )
        if code == 2:
            row["gate"] = "RED"
            ok = False
        elif code == 0:
            row["gate"] = "GREEN/YELLOW"
        else:
            row["gate"] = f"exit {code}"
            ok = False

        code, out = run([sys.executable, str(INTAKE), str(concept), "-o", str(script)])
        row["intake"] = "OK" if code == 0 else f"FAIL {code}"
        ok = ok and code == 0

        code, out = run([sys.executable, str(RENDER), str(script), "--script-only"])
        row["script_only"] = "OK" if code == 0 else f"FAIL {code}"
        ok = ok and code == 0

        results.append(row)
        icon = "✓" if row["gate"] != "RED" and row["intake"] == "OK" and row["script_only"] == "OK" else "✗"
        print(f"{icon} {slug}: gate={row['gate']} intake={row['intake']} script-only={row['script_only']}")

    report = SLATE_DIR / "validation_report.json"
    report.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"\nReport → {report}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())