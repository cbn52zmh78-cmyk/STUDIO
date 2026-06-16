#!/usr/bin/env python3
"""Write GFE casting prompts and verify casting_turnaround_v1.jpg coverage."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from actor_profile_generator import ActorProfile, STUDIO_ROOT
from ensure_gfe_folder_structure import ensure_actor_dirs
from gfe_roster_data import GFE_ROSTER_20

GFE_DIR = STUDIO_ROOT / "GFE"
OUT_NAME = "casting_turnaround_v1.jpg"
QUEUE_PATH = Path(__file__).resolve().parent / "gfe_casting_queue.json"


def build_gfe_casting_person_description(actor: ActorProfile) -> str:
    segments = [
        f"{actor.prompt_prefix()}, {actor.base_physical_description.strip().rstrip('.')}",
    ]
    if actor._has_tattoos():
        segments.append(f"Tattoos: {actor.tattoo_inventory.strip().rstrip('.')}")
    segments.append(
        f"wearing a regular thin-strap {actor.casting_wardrobe_color} triangle bikini top "
        f"and matching {actor.casting_wardrobe_color} bikini bottoms"
    )
    return ", ".join(segments)


def build_gfe_casting_prompt(actor: ActorProfile) -> str:
    root = str(STUDIO_ROOT)
    if root not in sys.path:
        sys.path.insert(0, root)
    from studio.prompting.production_images import build_gfe_casting_shot_prompt

    return build_gfe_casting_shot_prompt(build_gfe_casting_person_description(actor))


def gfe_casting_dir(actor: ActorProfile) -> Path:
    return GFE_DIR / actor.stage_name / "01_casting_shots"


def write_prompts() -> list[dict]:
    items: list[dict] = []
    for actor in GFE_ROSTER_20:
        ensure_actor_dirs(actor.stage_name)
        shot_dir = gfe_casting_dir(actor)
        prompt_path = shot_dir / "casting_prompt.txt"
        prompt = build_gfe_casting_prompt(actor)
        prompt_path.write_text(prompt + "\n", encoding="utf-8")
        out_file = shot_dir / OUT_NAME
        items.append(
            {
                "actor": actor.stage_name,
                "out_dir": str(shot_dir),
                "out_file": str(out_file),
                "prompt_path": str(prompt_path),
                "has_image": out_file.exists(),
                "prompt": prompt,
            }
        )
        print(f"✅ {actor.stage_name} → {prompt_path.relative_to(STUDIO_ROOT)}")
    return items


def main() -> int:
    print("\nGFE Casting Shot Generator — thin-strap bikini turnarounds")
    print(f"Root: {GFE_DIR}\n")

    items = write_prompts()
    QUEUE_PATH.write_text(json.dumps(items, indent=2) + "\n", encoding="utf-8")

    have = sum(1 for x in items if x["has_image"])
    need = len(items) - have
    print(f"\nPrompts: {len(items)} | Images: {have} | Need: {need}")
    print(f"Queue: {QUEUE_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())