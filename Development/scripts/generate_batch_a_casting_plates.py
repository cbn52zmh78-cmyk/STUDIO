#!/usr/bin/env python3
"""Build roster batch A (first 35) casting queue with compliance-enhanced prompts."""

from __future__ import annotations

import json
import re
from pathlib import Path

CAST_ROOT = Path(__file__).resolve().parents[2] / "Cast"
REGISTRY = CAST_ROOT / "Casting_Bible" / "registry" / "casting_registry.json"
QUEUE_OUT = Path(__file__).resolve().parent / "batch_a_casting_queue.json"
BATCH_SIZE = 35
AGE_MIN = 21

SYNTHETIC_GUARD = (
    "Synthetic fictional character only. No real person or celebrity likeness. "
    "Clearly adult with mature facial features and adult bone structure — "
    "unambiguously 21+ adult, not teen, not school-age."
)


def extract_age(text: str) -> int | None:
    m = re.search(r"(\d{1,2})-year-old", text, re.I)
    return int(m.group(1)) if m else None


def enhance_prompt(base: str, age: int) -> str:
    """Ensure generation prompt carries synthetic + adult guardrails."""
    text = base.strip()
    if "Synthetic fictional character only" not in text:
        text = f"{text.rstrip('.')}. {SYNTHETIC_GUARD}"
    if age <= 24 and "mature facial features" not in text.lower():
        text = text.replace(
            SYNTHETIC_GUARD,
            SYNTHETIC_GUARD + f" Depict as a clearly {age}-year-old adult woman/man.",
        )
    return text


def main() -> int:
    reg = json.loads(REGISTRY.read_text(encoding="utf-8"))
    batch = reg["actors"][:BATCH_SIZE]
    items: list[dict] = []

    for actor in batch:
        rel = actor["roster_path"].replace("STUDIO/Cast/", "")
        actor_dir = CAST_ROOT / rel
        shot_dir = actor_dir / "01_casting_shots"
        prompt_path = shot_dir / "casting_prompt.txt"
        out_file = shot_dir / "casting_turnaround_v1.jpg"

        if prompt_path.exists():
            base_prompt = prompt_path.read_text(encoding="utf-8").strip()
        else:
            base_prompt = (actor.get("appearance_lock_verbatim") or "").strip()

        age = actor["age_locked"]
        if age < AGE_MIN:
            raise SystemExit(f"BLOCKED: {actor['stage_name']} age_locked={age} < {AGE_MIN}")

        prompt_age = extract_age(base_prompt)
        if prompt_age is None:
            raise SystemExit(f"BLOCKED: {actor['stage_name']} missing numerical age in prompt")
        if prompt_age != age:
            raise SystemExit(
                f"BLOCKED: {actor['stage_name']} prompt age {prompt_age} != age_locked {age}"
            )

        enhanced = enhance_prompt(base_prompt, age)
        if enhanced != base_prompt:
            prompt_path.parent.mkdir(parents=True, exist_ok=True)
            prompt_path.write_text(enhanced + "\n", encoding="utf-8")

        items.append(
            {
                "actor_id": actor["actor_id"],
                "stage_name": actor["stage_name"],
                "gender": actor["gender"],
                "age_locked": age,
                "out_dir": str(shot_dir),
                "out_file": str(out_file),
                "prompt_path": str(prompt_path),
                "prompt": enhanced,
                "has_image": out_file.exists(),
            }
        )

    QUEUE_OUT.write_text(json.dumps(items, indent=2) + "\n", encoding="utf-8")
    print(f"Batch A queue: {len(items)} actors → {QUEUE_OUT}")
    print(f"  prompts_updated: {sum(1 for a in batch if True)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())