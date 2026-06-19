#!/usr/bin/env python3
"""Re-intake concept files to apply duration pre-clamp (#177) and emit audit list (#179)."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

PIPELINE = Path(__file__).resolve().parent
ROOT = PIPELINE.parents[1]
INTAKE = PIPELINE / "production_intake.py"
CONCEPTS = PIPELINE / "Concepts"
SCRIPTS_OUT = ROOT / "DAVID" / "scripts" / "longform_scripts"
RENDER = ROOT / "DAVID" / "scripts" / "render_longform.py"

# Formats whose seamless chain uses 7–9s pre-clamp at intake.
REINTAKE_FORMATS = frozenset({"science-explainer", "historical-figure-documentary"})


def _stale_shots(script: dict) -> list[str]:
    bad: list[str] = []
    for shot in script.get("shots", []):
        dur = int(shot.get("duration", 0))
        if dur < 7 or dur > 9:
            bad.append(f"{shot['id']}:{dur}s")
    return bad


def reintake_one(concept_path: Path) -> dict:
    raw = json.loads(concept_path.read_text(encoding="utf-8"))
    slug = raw.get("slug") or concept_path.stem.replace(".concept", "")
    format_id = raw.get("format_id", "")
    out = SCRIPTS_OUT / f"{slug}_script.json"
    proc = subprocess.run(
        [sys.executable, str(INTAKE), str(concept_path), "-o", str(out)],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )
    entry: dict = {
        "slug": slug,
        "format_id": format_id,
        "concept": str(concept_path.relative_to(ROOT)).replace("\\", "/"),
        "script": str(out.relative_to(ROOT)).replace("\\", "/"),
        "intake_rc": proc.returncode,
    }
    if proc.returncode not in (0, 3) or not out.is_file():
        entry["status"] = "FAIL"
        entry["error"] = (proc.stdout + proc.stderr)[-500:]
        return entry

    script = json.loads(out.read_text(encoding="utf-8"))
    stale = _stale_shots(script)
    entry["duration_clamp"] = (script.get("intake") or {}).get("duration_clamp")
    entry["stale_shots_after"] = stale
    entry["viz_duration"] = next(
        (
            s.get("duration")
            for s in script.get("shots", [])
            if s.get("id") in ("04_visualization_payoff", "04_period_line")
        ),
        None,
    )

    render_proc = subprocess.run(
        [sys.executable, str(RENDER), str(out), "--script-only"],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )
    entry["render_script_only_rc"] = render_proc.returncode
    entry["status"] = "OK" if not stale and render_proc.returncode == 0 else "WARN"
    if render_proc.returncode != 0:
        entry["render_error"] = (render_proc.stdout + render_proc.stderr)[-300:]
    return entry


def main() -> int:
    concepts = sorted(CONCEPTS.rglob("*.concept.json"))
    results: list[dict] = []
    for path in concepts:
        try:
            fmt = json.loads(path.read_text(encoding="utf-8")).get("format_id", "")
        except json.JSONDecodeError:
            continue
        if fmt not in REINTAKE_FORMATS:
            continue
        results.append(reintake_one(path))

    report_path = PIPELINE / "reintake_stale_durations_report.json"
    report_path.write_text(json.dumps(results, indent=2), encoding="utf-8")

    ok = sum(1 for r in results if r.get("status") == "OK")
    print(f"Re-intake complete: {ok}/{len(results)} OK → {report_path}")
    for row in results:
        icon = "✓" if row.get("status") == "OK" else "✗"
        clamp = (row.get("duration_clamp") or {}).get("shots_clamped", "?")
        print(
            f"{icon} {row['slug']} ({row['format_id']}) "
            f"viz/period={row.get('viz_duration')}s clamped={clamp}"
        )
    return 0 if ok == len(results) else 1


if __name__ == "__main__":
    raise SystemExit(main())