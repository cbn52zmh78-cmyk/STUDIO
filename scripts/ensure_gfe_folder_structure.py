#!/usr/bin/env python3
"""Ensure standard subfolder tree exists for every GFE actor."""

from __future__ import annotations

import sys
from pathlib import Path

from actor_profile_generator import STUDIO_ROOT
from gfe_roster_data import GFE_ROSTER_20

GFE_DIR = STUDIO_ROOT / "GFE"

GFE_SUBFOLDERS = (
    "01_casting_shots",
    "02_reference_views",
    "SCENES",
    "VARIATIONS",
    "CLIPS",
    "PROMOTIONAL",
    "STAGED SHOTS",
)


def ensure_actor_dirs(actor_name: str) -> list[Path]:
    base = GFE_DIR / actor_name
    created: list[Path] = []
    for sub in GFE_SUBFOLDERS:
        path = base / sub
        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)
            created.append(path)
        else:
            path.mkdir(parents=True, exist_ok=True)
    return created


def main() -> int:
    print(f"GFE folder structure — {GFE_DIR}\n")
    total_new = 0
    for actor in GFE_ROSTER_20:
        created = ensure_actor_dirs(actor.stage_name)
        new_count = len(created)
        total_new += new_count
        status = f"+{new_count} new" if new_count else "ok"
        print(f"  {actor.stage_name}: {status}")
    print(f"\nActors: {len(GFE_ROSTER_20)} | New folders: {total_new}")
    return 0


if __name__ == "__main__":
    sys.exit(main())