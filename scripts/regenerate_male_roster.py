#!/usr/bin/env python3
"""Regenerate profiles and casting prompts for male roster actors only."""

from actor_profile_generator import generate_actor_roster_package
from roster_50_data import ROSTER_50

if __name__ == "__main__":
    males = [a for a in ROSTER_50 if a.gender == "male"]
    print(f"Regenerating {len(males)} male actor packages...\n")
    for actor in males:
        generate_actor_roster_package(actor)
        print(f"✅ {actor.stage_name}")
    print("\nDone.")