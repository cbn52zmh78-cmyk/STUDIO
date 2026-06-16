"""Batch helper: list actors needing casting_turnaround_v1.jpg and verify completion."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ROSTER = ROOT / "actors_roster"
QUEUE = Path(__file__).resolve().parent / "roster_casting_queue.json"
OUT_NAME = "casting_turnaround_v1.jpg"


def build_queue() -> list[dict]:
    items = []
    for prompt_path in sorted(ROSTER.rglob("01_casting_shots/casting_prompt.txt")):
        shot_dir = prompt_path.parent
        out = shot_dir / OUT_NAME
        items.append(
            {
                "actor": shot_dir.parent.name,
                "out_dir": str(shot_dir),
                "out_file": str(out),
                "has_image": out.exists(),
                "prompt": prompt_path.read_text(encoding="utf-8").strip(),
            }
        )
    return items


def main() -> None:
    items = build_queue()
    QUEUE.write_text(json.dumps(items, indent=2), encoding="utf-8")
    need = [x for x in items if not x["has_image"]]
    have = [x for x in items if x["has_image"]]
    print(f"Total: {len(items)} | Have image: {len(have)} | Need image: {len(need)}")
    if need:
        print("\nMissing:")
        for x in need:
            print(f"  - {x['actor']}")


if __name__ == "__main__":
    main()