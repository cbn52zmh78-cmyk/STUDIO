#!/usr/bin/env python3
"""Generate GFE project packages: actor profile PDFs + 3-reference casting shot sheets."""

from __future__ import annotations

import sys
from pathlib import Path

GFE_ROOT = Path(__file__).resolve().parent.parent
STUDIO_ROOT = GFE_ROOT.parent / "Studio"
_SCRIPTS_DIR = Path(__file__).resolve().parent
for p in (_SCRIPTS_DIR, _SCRIPTS_DIR.parent / "lib", STUDIO_ROOT):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

from actor_profile_generator import STUDIO_ROOT, generate_actor_profile_pdf
from ensure_gfe_folder_structure import ensure_actor_dirs
from gfe_roster_data import GFE_ROSTER_20

GFE_DIR = STUDIO_ROOT / "GFE"


def _physical_hook(actor) -> str:
    """Short physical descriptor for composite prompts."""
    return actor.base_physical_description.split(".")[0].strip()


def gfe_actor_dir(actor) -> Path:
    return GFE_DIR / actor.stage_name


def write_casting_shot_sheet(actor, path: Path) -> None:
    hook = _physical_hook(actor)
    ethnicity_noun = actor.ethnicity.lower()
    prompt = (
        f"Photorealistic composite casting sheet for {actor.stage_name}, "
        f"{actor.age}-year-old {ethnicity_noun} alt model, {hook}, "
        "three side-by-side panels on white background: "
        "left - white satin dress with black lace trim, "
        "center - red string bikini showing tattoos, "
        "right - white string bikini on bed playful direct-to-camera pose, "
        "clean professional layout, sharp focus, studio lighting"
    )
    lines = [
        f"CASTING SHOT — {actor.stage_name} | 3 Reference Views",
        "",
        "1. White satin dress with black lace trim",
        "2. Red string bikini (maximum tattoo visibility)",
        "3. White string bikini on bed (playful/direct-to-camera)",
        "",
        "Standard Studio turnaround (separate file):",
        actor.build_actor_casting_shot_prompt(),
        "",
        f"Grok Imagine Prompt for Composite:",
        f"'{prompt}'",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    GFE_DIR.mkdir(parents=True, exist_ok=True)
    ok = 0

    for actor in GFE_ROSTER_20:
        ensure_actor_dirs(actor.stage_name)
        actor_dir = gfe_actor_dir(actor)
        ref_dir = actor_dir / "02_reference_views"

        pdf_path = actor_dir / "actor_profile.pdf"
        generate_actor_profile_pdf(actor, output_path=pdf_path)

        shot_path = ref_dir / "casting_shot_3view.txt"
        write_casting_shot_sheet(actor, shot_path)

        ok += 1
        print(f"✅ Generated {actor.stage_name} → GFE/{actor.stage_name}/")

    print(f"\nAll {ok} GFE actresses created. Folder: {GFE_DIR}")
    return 0 if ok == len(GFE_ROSTER_20) else 1


if __name__ == "__main__":
    sys.exit(main())