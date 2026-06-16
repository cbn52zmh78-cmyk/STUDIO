#!/usr/bin/env python3
"""Generate 10 stunning-feature male actor packages and merge into roster index."""

from __future__ import annotations

import json
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path

from actor_profile_generator import STUDIO_ROOT, generate_actor_roster_package
from roster_10_stunning_females_data import ROSTER_STUNNING_10
from roster_10_stunning_males_data import ROSTER_STUNNING_MALES_10
from roster_50_data import ROSTER_50


def load_existing_index() -> dict:
    index_path = STUDIO_ROOT / "actors_roster" / "roster_index.json"
    if index_path.exists():
        return json.loads(index_path.read_text(encoding="utf-8"))
    return {"by_gender": {"female": [], "male": []}}


def main() -> int:
    print("\nSTUDIO Roster Generator — 10 stunning male actors")
    print(f"Root: {STUDIO_ROOT / 'actors_roster'}\n")

    ok = 0
    new_entries: dict[str, list[dict]] = defaultdict(list)

    for actor in ROSTER_STUNNING_MALES_10:
        paths = generate_actor_roster_package(actor)
        ok += 1
        rel = actor.roster_dir().relative_to(STUDIO_ROOT)
        print(f"✅ [male/{actor.world_region}] {actor.stage_name} → {rel}")
        new_entries["male"].append(
            {
                "stage_name": actor.stage_name,
                "age": actor.age,
                "world_region": actor.world_region,
                "ethnicity": actor.ethnicity,
                "mood_modifiers": actor.mood_modifiers,
                "path": str(rel).replace("\\", "/"),
                "pdf": str(paths.get("pdf", "")),
                "roster_group": "stunning_10",
            }
        )

    existing = load_existing_index()
    by_gender = existing.get("by_gender", {"female": [], "male": []})
    by_gender.setdefault("male", []).extend(new_entries["male"])

    female_count = len(by_gender.get("female", []))
    male_count = len(by_gender["male"])
    total = female_count + male_count

    stunning_female = sum(
        1 for a in by_gender.get("female", []) if a.get("roster_group") == "stunning_10"
    )
    stunning_male = len(ROSTER_STUNNING_MALES_10)

    index_path = STUDIO_ROOT / "actors_roster" / "roster_index.json"
    payload = {
        "generated": datetime.now().isoformat(timespec="seconds"),
        "total": total,
        "female_count": female_count,
        "male_count": male_count,
        "stunning_female_count": stunning_female,
        "stunning_male_count": stunning_male,
        "by_gender": by_gender,
        "regions": sorted(
            {a.world_region for a in ROSTER_50}
            | {a.world_region for a in ROSTER_STUNNING_10}
            | {a.world_region for a in ROSTER_STUNNING_MALES_10}
        ),
    }
    index_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    print(f"\nDone: {ok}/10 new profiles")
    print(f"Roster total: {total} ({female_count} female, {male_count} male)")
    print(f"Index: {index_path}\n")
    return 0 if ok == 10 else 1


if __name__ == "__main__":
    sys.exit(main())