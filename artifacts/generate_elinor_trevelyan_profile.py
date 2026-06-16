#!/usr/bin/env python3
"""Generate locked director-bible profile for fictional actress Elinor Trevelyan."""

from datetime import datetime
from pathlib import Path

from actor_profile_generator import ActorProfile, generate_actor_profile

OUTPUT_DIR = Path(__file__).resolve().parent / "output" / "profiles"

elinor_trevelyan = ActorProfile(
    stage_name="Elinor Trevelyan",
    full_legal_name="Elinor Catherine Trevelyan",
    professional_stage_name="Elinor Trevelyan",
    age=26,
    date_of_birth="August 2, 1999",
    ethnicity="White British",
    nationality="United Kingdom",
    heritage=(
        "Cornish — Penwith coast family roots (St Ives / Zennor line); "
        "Trevelyan surname traceable to west Cornwall mining and fishing communities"
    ),
    languages=[
        "English (native RP with Cornish coastal lilt when relaxed)",
        "Cornish (basic conversational — greetings, place names, occasional phrase in character)",
    ],
    base_physical_description=(
        "5'7\", lean swimmer's build with strong shoulders and long limbs. "
        "Honey-blonde hair, naturally wavy, worn loose to mid-back or pinned in a low "
        "practical knot for work scenes. Grey-green eyes that read pale in overcast light, "
        "warmer in golden hour. Fair skin with light freckling across nose and shoulders; "
        "tans unevenly after long Cornish summers. Hands show faint callus from climbing and "
        "outdoor work — continuity detail for rural/coastal roles. No tattoos; no piercings "
        "except small gold studs in both ears."
    ),
    archetypes=[
        "Coastal drama lead — stubborn, wind-scoured, quietly brave",
        "Period piece ingénue with steel beneath the manners",
        "Modern British indie romantic lead",
        "Grief-carrier who keeps moving until she breaks in private",
    ],
    performance_style=(
        "Grounded British naturalism in the tradition of Carey Mulligan's restraint and "
        "Jodie Comer's emotional precision, with flashes of Billie Piper warmth in intimate "
        "scenes. Underplays big moments; lets the camera find the crack. Physicality is "
        "athletic and unshowy — climbs, walks, works with her body rather than posing. "
        "Strong in landscape-led storytelling and silence."
    ),
    voice_notes=(
        "Clear West Country warmth when guard is down — softened consonants, longer vowels on "
        "'ar' and 'o'. Can shift to neutral London RP for urban or period roles. Laugh is "
        "open and sudden; anger arrives quiet first, then precise. Singing voice untrained "
        "but honest — folk-adjacent, not musical-theatre."
    ),
    on_screen_comfort=(
        "Comfortable with tasteful, story-serving intimacy per "
        "Cinematic_Intimacy_Safe_Legal_Protocol_v1.3. Topless only when narratively earned; "
        "clinical/neutral prompt language required. Not available for explicit adult content. "
        "Nude staging acceptable in arthouse context with compliance review."
    ),
    personality=(
        "Outwardly composed and practical — the person who checks the tide, fixes the gate, "
        "and makes tea before discussing feelings. Cornish stubbornness is real: she will not "
        "be talked out of something she believes is right. Beneath the reserve: deep attachment "
        "to place and family, dry humour, and a fierce protectiveness of the vulnerable. "
        "Does not perform vulnerability for approval; grief and longing surface in small "
        "physical tells — a tightened jaw, a longer stare at the sea."
    ),
    base_reference_images=[
        "Waxed Barbour-style jacket, cream fisherman's knit, mud-splashed boots — coastal winter",
        "Ivory linen dress, bare shoulders, Cornwall cliff light — period / romance beat",
        "Dark navy swimsuit, wind-wet hair — sea swimming continuity plate",
        "1940s-inspired tea dress, structured collar — period drama reference",
    ],
    tattoo_inventory="None — continuity: no tattoo additions without canon update.",
    signature_looks=(
        "Wind-tousled honey-blonde; minimal makeup (freckles visible); rose-beige lip. "
        "Cool coastal palette in wardrobe — slate, cream, navy, olive. Silver signet ring "
        "(family heirloom) on right hand — continuity prop in most modern roles."
    ),
    casting_notes=(
        "Lead and co-lead in British drama, period pieces, coastal/rural thriller, and "
        "indie romance. Cornish background should inform character when script allows — "
        "not caricature. Age must lead every prompt: '26-year-old White British woman...' "
        "Excels when environment is a character (sea, cliff, rain, stone). Avoid casting "
        "as generic 'English rose' without interior complexity."
    ),
    profile_date=datetime.now().strftime("%B %d, %Y"),
)

if __name__ == "__main__":
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    md_path, pdf_path = generate_actor_profile(elinor_trevelyan, OUTPUT_DIR)
    print("✅ Elinor Trevelyan profile generated")
    if md_path:
        print(f"   MD:  {md_path}")
    if pdf_path:
        print(f"   PDF: {pdf_path}")