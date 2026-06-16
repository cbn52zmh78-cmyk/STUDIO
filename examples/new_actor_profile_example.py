#!/usr/bin/env python3
"""Example: create a new actor profile PDF using the ActorProfile API."""

import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from actor_profile_generator import ActorProfile, generate_actor_profile_pdf

OUTPUT_DIR = ROOT / "examples" / "output"

new_actor = ActorProfile(
    stage_name="YourStageName",
    full_legal_name="Full Legal Name",
    professional_stage_name="Stage Name (if different)",
    age=22,  # replace with exact age — must lead every prompt
    date_of_birth="Month DD, YYYY",
    ethnicity="...",
    nationality="...",
    heritage="...",
    languages=[
        "Japanese (native, Tokyo dialect)",
        "English (fluent...)",
    ],
    base_physical_description=(
        "5'X\" (... detailed paragraph with build, hair, eyes, tattoos, skin tone...)"
    ),
    archetypes=[
        "Edgy alternative / Rebellious romantic interest",
        "Punk rock girlfriend / Tattooed “stag girl” type",
    ],
    performance_style=(
        "Blend of [Actor1] + [Actor2] + [Actor3]. Description of underplaying, "
        "micro-expressions, stillness..."
    ),
    voice_notes="Soft, slightly breathy... accent notes... emotional shifts...",
    on_screen_comfort=(
        "Relatively open to tasteful nudity... topless OK when story-serving. "
        "Not available for explicit porn..."
    ),
    personality=(
        "Full paragraph covering surface vs. cracks, warmth, mischief, outsider status..."
    ),
    base_reference_images=[
        "White satin dress with black lace trim",
        "Red string bikini (maximum tattoo visibility)",
    ],
    tattoo_inventory=(
        "Large floral/choker... full irezumi sleeves... heavy coverage on thighs/legs. "
        "Critical continuity note..."
    ),
    signature_looks=(
        "Strong visual presence... hair in high bun... sharp defined makeup... "
        "cool-to-warm shifts..."
    ),
    casting_notes=(
        "Primarily love interest... excels in edgy alternative tattooed girlfriend roles... "
        "heavy tattoos should usually be featured... best with emotional layers beneath "
        "the surface..."
    ),
    profile_date=datetime.now().strftime("%B %d, %Y"),
)

if __name__ == "__main__":
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    pdf_path = generate_actor_profile_pdf(
        new_actor,
        output_path=OUTPUT_DIR / "NewActor_Actor_Profile.pdf",
    )
    print(f"✅ PDF created: {pdf_path}")