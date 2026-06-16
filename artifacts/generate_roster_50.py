#!/usr/bin/env python3
"""Generate all 50 actor roster packages: PDF, MD, casting prompt — by gender and region."""

from __future__ import annotations

import json
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path

from actor_profile_generator import STUDIO_ROOT, generate_actor_roster_package
from roster_50_data import ROSTER_50


def main() -> int:
    print(f"\nSTUDIO Roster Generator — 50 actors")
    print(f"Root: {STUDIO_ROOT / 'actors_roster'}\n")

    index: dict[str, list[dict]] = defaultdict(list)
    ok = 0

    for actor in ROSTER_50:
        paths = generate_actor_roster_package(actor)
        ok += 1
        rel = actor.roster_dir().relative_to(STUDIO_ROOT)
        print(f"✅ [{actor.gender}/{actor.world_region}] {actor.stage_name} → {rel}")
        index[actor.gender].append(
            {
                "stage_name": actor.stage_name,
                "age": actor.age,
                "world_region": actor.world_region,
                "ethnicity": actor.ethnicity,
                "mood_modifiers": actor.mood_modifiers,
                "path": str(rel).replace("\\", "/"),
                "pdf": str(paths.get("pdf", "")),
            }
        )

    index_path = STUDIO_ROOT / "actors_roster" / "roster_index.json"
    payload = {
        "generated": datetime.now().isoformat(timespec="seconds"),
        "total": ok,
        "female_count": sum(1 for a in ROSTER_50 if a.gender == "female"),
        "male_count": sum(1 for a in ROSTER_50 if a.gender == "male"),
        "by_gender": dict(index),
        "regions": sorted({a.world_region for a in ROSTER_50}),
    }
    index_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    print(f"\nDone: {ok}/50 profiles")
    print(f"Index: {index_path}\n")
    return 0 if ok == 50 else 1


if __name__ == "__main__":
    sys.exit(main())