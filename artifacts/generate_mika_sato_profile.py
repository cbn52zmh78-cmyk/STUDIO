#!/usr/bin/env python3
"""Generate locked director-bible profile for fictional actress Mika Sato."""

from datetime import datetime
from pathlib import Path

from actor_profile_generator import (
    ActorProfile,
    generate_actor_profile,
)

OUTPUT_DIR = Path(__file__).resolve().parent / "output" / "profiles"

mika_sato = ActorProfile(
    stage_name="Mika Sato",
    full_legal_name="Mika Ayumi Sato",
    professional_stage_name="Mika Sato",
    age=24,
    date_of_birth="March 14, 2002",
    ethnicity="Japanese-American",
    nationality="United States",
    heritage="Japanese (Osaka maternal line; Yokohama paternal roots)",
    languages=[
        "Japanese (native fluency, Kansai-influenced warmth in casual register)",
        "English (native West Coast neutral; code-switches to sharper clipped delivery under stress)",
    ],
    base_physical_description=(
        "5'4\", compact athletic build with dancer's posture and defined shoulders. "
        "Jet-black hair worn chin-length with blunt fringe or swept into a high messy bun "
        "for action beats. Dark brown eyes with a steady, unblinking quality in close-ups. "
        "Warm ivory skin with a faint natural flush at the cheeks. Small silver hoop in left "
        "ear; no other piercings. Wardrobe range spans thrift-store punk layers to tailored "
        "minimalist evening wear — always reads as intentional, never careless."
    ),
    archetypes=[
        "Edgy alternative / Rebellious romantic interest",
        "Punk-adjacent girlfriend with hidden vulnerability",
        "Survivor who smiles before the room turns hostile",
        "Reaction-shot specialist — micro-hurt before the armor clicks back",
    ],
    performance_style=(
        "Underplayed naturalism in the vein of early-career Rooney Mara meets Rinko Kikuchi's "
        "stillness, with flashes of Aubrey Plaza dry mischief in safe company. Holds eye contact "
        "one beat longer than comfortable. Emotional turns land in the exhale, not the shout. "
        "Excels in silence between lines."
    ),
    voice_notes=(
        "Soft, slightly breathy baseline; drops half an octave when lying or deflecting. "
        "Kansai warmth surfaces in unguarded moments with family or love-interest scenes. "
        "Laugh is quiet and sudden — more exhale than sound."
    ),
    on_screen_comfort=(
        "Open to tasteful, story-serving intimacy per Cinematic_Intimacy_Safe_Legal_Protocol_v1.3. "
        "Topless acceptable when narratively earned and age-led in every prompt. "
        "Not available for explicit adult content. Clinical/neutral language required in all "
        "generation prompts for intimate beats."
    ),
    personality=(
        "Surface reads as cool, slightly unreachable — the girl who sits at the edge of the party "
        "and watches. Beneath that: fierce loyalty, dry humor, and a low tolerance for bullies. "
        "Outsider status is real but worn lightly; she does not perform woundedness for sympathy. "
        "Warmth unlocks in private scenes — small gestures (fixing someone's collar, sharing food "
        "without asking) carry more weight than speeches."
    ),
    base_reference_images=[
        "Black cropped moto jacket over white ribbed tank (tattoo visibility: forearms)",
        "Ivory slip dress with black lace trim — evening vulnerability beat",
        "Red string bikini — maximum tattoo visibility for beach / pool continuity plates",
        "Oversized vintage band tee, ripped black jeans, combat boots — default street look",
    ],
    tattoo_inventory=(
        "Heavy irezumi continuity — NON-NEGOTIABLE in most looks: full floral choker band at "
        "throat; bilateral peony-and-wave sleeves from shoulder to wrist; large thigh panels "
        "(both legs) visible in shorts, swimwear, or intimate staging. No tattoo reduction or "
        "cover-up in canon without director sign-off. Makeup may soften but never erase ink."
    ),
    signature_looks=(
        "High messy bun exposing neck tattoo band; sharp winged liner with bare lip or deep berry "
        "stain; cool-to-warm shift — starts guarded in steel tones, opens into amber warmth in "
        "resolution scenes. Silver hoop catches light in profile shots."
    ),
    casting_notes=(
        "Primary casting: love interest, co-lead drama, neo-noir and indie thriller. "
        "Best when tattoos are featured — do not default to long-sleeve coverage unless script "
        "demands. Age must lead every prompt: '24-year-old Japanese-American woman...' "
        "Pair with emotionally layered material; comedy only when character's dryness is the joke."
    ),
    profile_date=datetime.now().strftime("%B %d, %Y"),
)

if __name__ == "__main__":
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    md_path, pdf_path = generate_actor_profile(mika_sato, OUTPUT_DIR)
    print(f"✅ Mika Sato profile generated")
    if md_path:
        print(f"   MD:  {md_path}")
    if pdf_path:
        print(f"   PDF: {pdf_path}")