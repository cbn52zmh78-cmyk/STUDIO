#!/usr/bin/env python3
"""Validate mandatory Gate 0 integration in production_intake.py."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

PIPELINE = Path(__file__).resolve().parent
ROOT = PIPELINE.parent.parent
INTAKE = PIPELINE / "production_intake.py"
RENDER = ROOT / "DAVID" / "scripts" / "render_longform.py"
JULIAN_CONCEPT = PIPELINE / "Concepts" / "julian_flowdesk_explainer_v1.concept.json"
RED_CONCEPT = PIPELINE / "Concepts" / "test_gate_red_music_v1.concept.json"
COMPLIANCE = ROOT / "artifacts" / "compliance" / "content_rating_compliance_guard.py"


def _run_intake(concept_path: Path, out: Path | None = None) -> subprocess.CompletedProcess:
    cmd = [sys.executable, str(INTAKE), str(concept_path)]
    if out:
        cmd.extend(["-o", str(out)])
    return subprocess.run(cmd, cwd=str(ROOT), capture_output=True, text=True)


def test_cara_adult_cast_phrase() -> None:
    sys.path.insert(0, str(ROOT / "artifacts"))
    from compliance.content_rating_compliance_guard import ContentRatingGuard

    guard = ContentRatingGuard(output_dir=tempfile.gettempdir())
    report = guard.analyze_prompt(
        "Synthetic presenter. adult cast only (21+). SFW explainer.",
        target_rating="PG",
        name="CARA_adult_cast_safe",
    )
    assert report["status"] == "COMPLIANT", report


def test_julian_yellow_intake() -> dict:
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "julian_script.json"
        proc = _run_intake(JULIAN_CONCEPT, out)
        assert out.is_file(), proc.stdout + proc.stderr
        script = json.loads(out.read_text(encoding="utf-8"))
        gate = script["intake"]["gate_0"]
        assert gate["verdict"] == "YELLOW", gate
        assert gate["requires_human_signoff"] is True
        assert gate["blocked"] is False
        assert "checklist_domains" in gate
        # Julian/FlowDesk reference path — client channel flags, proceed at intake
        assert proc.returncode == 3, proc.stdout  # sign-off required exit
        return gate


def test_red_blocks_intake() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "red_script.json"
        proc = _run_intake(RED_CONCEPT, out)
        assert proc.returncode == 2, proc.stdout + proc.stderr
        assert not out.exists(), "RED must not write script"
        assert "GATE 0 RED" in proc.stdout


def test_red_blocks_render() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        fake = Path(tmp) / "blocked_script.json"
        fake.write_text(
            json.dumps(
                {
                    "slug": "fake_red",
                    "title": "fake",
                    "config": {"voice_suffix": "test, synthetic host only"},
                    "shots": [
                        {
                            "id": "01",
                            "duration": 8,
                            "video_prompt": "test prompt synthetic host only",
                        }
                    ],
                    "intake": {
                        "gate_0": {
                            "verdict": "RED",
                            "blocked": True,
                            "report_path": "STUDIO/Producers_Office/Legal_Gate/GATE_RED_test.json",
                        }
                    },
                }
            ),
            encoding="utf-8",
        )
        proc = subprocess.run(
            [sys.executable, str(RENDER), str(fake), "--script-only"],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
        )
        assert proc.returncode != 0
        assert "Gate 0 RED" in proc.stderr + proc.stdout


def main() -> int:
    test_cara_adult_cast_phrase()
    julian_gate = test_julian_yellow_intake()
    test_red_blocks_intake()
    test_red_blocks_render()

    print("PASS: CARA adult cast only (21+) — no false RED on minor substring")
    print(f"PASS: Julian/FlowDesk intake — Gate 0 {julian_gate['verdict']} stamped, sign-off required")
    print("PASS: RED music concept — intake exit 2, no script written")
    print("PASS: RED gate stamp — render_longform blocked")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())