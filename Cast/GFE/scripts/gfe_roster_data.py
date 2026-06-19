"""Twenty GFE (Girlfriend Experience) actress profiles — alt romantic-interest line."""

from __future__ import annotations

import sys
from pathlib import Path

GFE_ROOT = Path(__file__).resolve().parent.parent
STUDIO_ROOT = GFE_ROOT.parent / "Studio"
_SCRIPTS_DIR = Path(__file__).resolve().parent
for p in (_SCRIPTS_DIR, _SCRIPTS_DIR.parent / "lib", STUDIO_ROOT):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

from roster_50_data import _a
from actor_profile_generator import ActorProfile

_GFE_COMFORT = (
    "Open to tasteful, story-serving intimacy per Cinematic_Intimacy_Safe_Legal_Protocol_v1.3. "
    "Topless acceptable when narratively earned; age must lead every prompt. "
    "Not available for explicit adult content."
)
_GFE_REFS = [
    "White satin dress with black lace trim",
    "Red string bikini (maximum tattoo visibility)",
    "White string bikini on bed (playful/direct-to-camera)",
]
_TATTOO_HEAVY = (
    "Heavy irezumi continuity: floral choker band at throat; bilateral peony-and-wave sleeves "
    "shoulder to wrist; large thigh panels both legs. No tattoo reduction without director sign-off."
)
_TATTOO_MEDIUM = (
    "Moderate tattoo continuity: fine-line floral sternum piece; half-sleeve botanicals left arm; "
    "ankle band both legs. Ink must remain visible in swimwear and slip-dress beats."
)
_TATTOO_LIGHT = (
    "Light tattoo continuity: small kanji wrist (left); constellation cluster right collarbone; "
    "minimal thigh script (right). Do not add ink without canon update."
)


def _gfe(
    *,
    stage_name: str,
    age: int,
    ethnicity: str,
    nationality: str,
    heritage: str,
    languages: list[str],
    physical: str,
    archetypes: list[str],
    moods: list[str],
    on_screen_mood: str,
    off_screen_mood: str,
    performance_style: str,
    voice_notes: str,
    personality: str,
    signature_looks: str,
    casting_notes: str,
    tattoos: str,
    wardrobe_color: str = "black",
    dob: str = "Month DD, YYYY",
    full_legal_name: str | None = None,
) -> ActorProfile:
    actor = _a(
        stage_name=stage_name,
        gender="female",
        world_region="east_asia",
        age=age,
        ethnicity=ethnicity,
        nationality=nationality,
        heritage=heritage,
        languages=languages,
        physical=physical,
        archetypes=archetypes,
        moods=moods,
        on_screen_mood=on_screen_mood,
        off_screen_mood=off_screen_mood,
        performance_style=performance_style,
        voice_notes=voice_notes,
        personality=personality,
        signature_looks=signature_looks,
        casting_notes=casting_notes,
        refs=_GFE_REFS,
        tattoos=tattoos,
        wardrobe_color=wardrobe_color,
        dob=dob,
        full_legal_name=full_legal_name or stage_name,
    )
    actor.on_screen_comfort = _GFE_COMFORT
    return actor


GFE_ROSTER_20: list[ActorProfile] = [
    _gfe(
        stage_name="Aiko",
        age=24,
        ethnicity="Japanese-American",
        nationality="United States",
        heritage="Osaka maternal line; Los Angeles upbringing",
        languages=["Japanese (native, Kansai warmth)", "English (West Coast neutral)"],
        physical=(
            "5'4\", compact athletic build, jet-black chin-length hair with blunt fringe, "
            "dark brown steady eyes, warm ivory skin, dancer posture."
        ),
        archetypes=["Edgy alt girlfriend", "Tattooed romantic lead", "Punk-adjacent love interest"],
        moods=["guarded", "playful", "intense"],
        on_screen_mood="Cool surface; warmth leaks through micro-smiles and held gaze.",
        off_screen_mood="Dry humor with crew; protective of quiet moments on set.",
        performance_style="Underplayed naturalism; emotional turns in the exhale.",
        voice_notes="Soft breathy baseline; Kansai warmth when unguarded.",
        personality="Outsider poise with fierce loyalty; mischief in safe company.",
        signature_looks="High messy bun, winged liner, silver hoop, thrift-punk layers.",
        casting_notes="Lead GFE intimacy arcs; tattoos featured in reference panels 2–3.",
        tattoos=_TATTOO_HEAVY,
        wardrobe_color="black",
        dob="March 14, 2002",
        full_legal_name="Aiko Ayumi Mori",
    ),
    _gfe(
        stage_name="Vesper",
        age=26,
        ethnicity="Japanese-British",
        nationality="United Kingdom",
        heritage="Tokyo mother; London father; Shoreditch creative scene",
        languages=["English (native, RP-soft)", "Japanese (fluent)"],
        physical=(
            "5'6\", lean model build, raven hair in slick low ponytail, grey-green eyes, "
            "porcelain-olive skin, sharp cheekbones."
        ),
        archetypes=["Goth girlfriend fantasy", "Noir romantic interest", "Late-night confessional lead"],
        moods=["nocturnal", "wry", "sensual"],
        on_screen_mood="Smokescreen cool until a single crack reveals need.",
        off_screen_mood="Cigarette-and-jazz playlist energy; candid with cinematographer.",
        performance_style="Stillness with predator-prey eye-line games.",
        voice_notes="Low melodic register; British clip when deflecting.",
        personality="Irony as armor; tenderness reserved for earned trust.",
        signature_looks="Black satin, berry lip, throat tattoo band exposed.",
        casting_notes="Best in moody two-handers; panel 1 slip-dress is signature beat.",
        tattoos=_TATTOO_HEAVY,
        wardrobe_color="deep wine",
        dob="November 2, 1999",
        full_legal_name="Vesper Hana Cross",
    ),
    _gfe(
        stage_name="Mika",
        age=24,
        ethnicity="Japanese-American",
        nationality="United States",
        heritage="Yokohama paternal roots; Bay Area raised",
        languages=["Japanese (native)", "English (native)"],
        physical=(
            "5'4\", compact athletic build, jet-black hair in high messy bun or blunt bob, "
            "dark brown unblinking eyes, warm ivory skin."
        ),
        archetypes=["Survivor girlfriend", "Reaction-shot specialist", "Rebellious romantic interest"],
        moods=["stoic", "dry", "warm"],
        on_screen_mood="Holds eye contact one beat too long; hurt lands before armor returns.",
        off_screen_mood="Quiet on set; fixes collars and shares food without asking.",
        performance_style="Rooney Mara stillness meets Plaza dry mischief.",
        voice_notes="Quiet sudden laugh; drops half octave when lying.",
        personality="Low tolerance for bullies; warmth in private gestures.",
        signature_looks="Berry lip or bare lip; combat boots; vintage band tee.",
        casting_notes="Canon matches Mika Sato archetype; heavy tattoo continuity.",
        tattoos=_TATTOO_HEAVY,
        wardrobe_color="crimson",
        dob="June 8, 2002",
        full_legal_name="Mika Ayumi Sato",
    ),
    _gfe(
        stage_name="Sora",
        age=23,
        ethnicity="Korean-Japanese",
        nationality="Japan",
        heritage="Busan mother; Osaka father",
        languages=["Japanese (native)", "Korean (fluent)", "English (conversational)"],
        physical=(
            "5'5\", slim toned build, ash-brown layered hair, soft monolid eyes, "
            "peachy fair skin, gentle jaw."
        ),
        archetypes=["Soft girlfriend fantasy", "Morning-after intimacy lead", "Slice-of-life romance"],
        moods=["gentle", "curious", "flirty"],
        on_screen_mood="Sunlit openness; shyness in first touch beats.",
        off_screen_mood="Playlist curator; brings snacks to video village.",
        performance_style="Naturalistic warmth; excels in over-the-shoulder close work.",
        voice_notes="Bright mid register; breath hitches on honest lines.",
        personality="Optimistic with realistic edges; hates performative cruelty.",
        signature_looks="Loose knit cardigan, bare face, hair in claw clip.",
        casting_notes="Panel 3 bed pose is primary hook; keep playful not explicit.",
        tattoos=_TATTOO_LIGHT,
        wardrobe_color="soft pink",
        dob="April 21, 2003",
        full_legal_name="Sora Min-jae Park",
    ),
    _gfe(
        stage_name="Hana",
        age=22,
        ethnicity="Japanese",
        nationality="Japan",
        heritage="Kyoto geisha-district adjacent arts family (modern branch)",
        languages=["Japanese (native, Kyoto polish)", "English (intermediate)"],
        physical=(
            "5'2\", petite slim build, black hair in long straight curtain, round dark eyes, "
            "porcelain skin, rosebud lips."
        ),
        archetypes=["Innocent-with-edge girlfriend", "Coming-of-age intimacy", "Shy-to-bold arc"],
        moods=["shy", "earnest", "sparkling"],
        on_screen_mood="Blush-forward honesty; boldness surprises the room.",
        off_screen_mood="Formal politeness melts into giggles after first take.",
        performance_style="Big eyes carry subtext; minimal dialogue scenes shine.",
        voice_notes="Light airy tone; Kyoto softness on affection lines.",
        personality="Tradition-aware but self-directed; chooses her own rebellion.",
        signature_looks="White satin slip beats; subtle peach blush; bare shoulders.",
        casting_notes="Age-locked 22 in every prompt; panel 1 lace trim is hero look.",
        tattoos=_TATTOO_LIGHT,
        wardrobe_color="ivory",
        dob="January 15, 2004",
        full_legal_name="Hana Fujiwara",
    ),
    _gfe(
        stage_name="Rin",
        age=25,
        ethnicity="Japanese",
        nationality="Japan",
        heritage="Harajuku street-fashion lineage; Nagoya roots",
        languages=["Japanese (native, Tokyo slang)", "English (fluent)"],
        physical=(
            "5'5\", athletic dancer build, platinum-streaked black hair in space buns, "
            "sharp brown eyes, fair skin, defined collarbones."
        ),
        archetypes=["Club-scene girlfriend", "High-energy flirt lead", "Music-video romance"],
        moods=["electric", "teasing", "loyal"],
        on_screen_mood="Flirt as sport until real jealousy lands.",
        off_screen_mood="Dance battles with crew; fearless with stunt coordination.",
        performance_style="Physical comedy and intimacy share the same rhythm.",
        voice_notes="Fast Tokyo cadence; slows for whisper beats.",
        personality="Chaos gremlin with a devoted core; hates boredom.",
        signature_looks="Neon eyeliner, platform boots, mesh layers over bikini panels.",
        casting_notes="Red string bikini panel must show sleeve tattoos clearly.",
        tattoos=_TATTOO_MEDIUM,
        wardrobe_color="hot pink",
        dob="August 30, 2000",
        full_legal_name="Rin Aoki",
    ),
    _gfe(
        stage_name="Yume",
        age=21,
        ethnicity="Japanese-Filipina",
        nationality="United States",
        heritage="Manila mother; Fukuoka father; Hawaii childhood",
        languages=["English (native)", "Japanese (conversational)", "Tagalog (basic)"],
        physical=(
            "5'3\", soft curvy build, wavy chestnut hair to shoulders, honey-brown eyes, "
            "golden tan skin, full lips."
        ),
        archetypes=["Island girlfriend fantasy", "Beach-house romance", "Laugh-first intimacy"],
        moods=["sunny", "mischievous", "affectionate"],
        on_screen_mood="Direct-to-camera warmth; infectious smile before the line.",
        off_screen_mood="Sunscreen and playlist captain; hugs the gaffer.",
        performance_style="Improvisational touch beats; excels in handheld intimacy.",
        voice_notes="Hawaiian-tinged English; melodic laugh.",
        personality="Disarms with humor; serious when consent boundaries discussed.",
        signature_looks="Wet-hair beach aesthetic; white string bikini is canon.",
        casting_notes="Youngest roster member; age 21 non-negotiable in prompts.",
        tattoos=_TATTOO_LIGHT,
        wardrobe_color="coral",
        dob="December 3, 2004",
        full_legal_name="Yume Reyes Tanaka",
    ),
    _gfe(
        stage_name="Kira",
        age=27,
        ethnicity="Japanese",
        nationality="Japan",
        heritage="Sapporo snow-country; moved to Tokyo at 18",
        languages=["Japanese (native)", "English (business fluent)"],
        physical=(
            "5'7\", tall model proportions, straight black hair to waist, ice-brown eyes, "
            "cool fair skin, long legs."
        ),
        archetypes=["Cool older-sister girlfriend", "Executive-off-hours romance", "Power-balance intimacy"],
        moods=["composed", "smoldering", "protective"],
        on_screen_mood="Control until partner earns vulnerability.",
        off_screen_mood="Spreadsheet jokester; brings quality coffee to set.",
        performance_style="Vertical line and posture tell the story.",
        voice_notes="Calm low register; rare smile disarms.",
        personality="Competence is seduction; softness is the prize.",
        signature_looks="Tailored slip over bare shoulders; minimalist jewelry.",
        casting_notes="Tallest GFE cast; frame panels full-length head-to-toe.",
        tattoos=_TATTOO_MEDIUM,
        wardrobe_color="charcoal",
        dob="February 18, 1999",
        full_legal_name="Kira Matsumoto",
    ),
    _gfe(
        stage_name="Luna",
        age=24,
        ethnicity="Japanese-Mexican",
        nationality="United States",
        heritage="Oaxaca mother; Hiroshima grandfather line",
        languages=["English (native)", "Spanish (fluent)", "Japanese (conversational)"],
        physical=(
            "5'4\", hourglass athletic build, dark wavy hair with copper tips, amber-brown eyes, "
            "warm olive skin."
        ),
        archetypes=["Bicultural girlfriend", "Passion-with-tenderness lead", "Kitchen-table intimacy"],
        moods=["warm", "fiery", "tender"],
        on_screen_mood="Heat in argument; melt in reconciliation beats.",
        off_screen_mood="Cooks for crew; teaches Spanish phrases between takes.",
        performance_style="Hands tell truth before dialogue.",
        voice_notes="Rich mid tone; Spanish lilt on pet names.",
        personality="Family-first values; chooses partners who respect both cultures.",
        signature_looks="Copper-tip waves; satin dress with lace; gold hoops.",
        casting_notes="Bilingual ad-libs welcome in panel 3 direct-to-camera beat.",
        tattoos=_TATTOO_MEDIUM,
        wardrobe_color="terracotta",
        dob="July 9, 2002",
        full_legal_name="Luna Esperanza Ito",
    ),
    _gfe(
        stage_name="Nova",
        age=23,
        ethnicity="Japanese-American",
        nationality="United States",
        heritage="Seattle tech-family; Sendai summer visits",
        languages=["English (native)", "Japanese (fluent)"],
        physical=(
            "5'5\", slim runner build, silver-dyed bob, sharp hazel eyes, fair skin, "
            "angular brows."
        ),
        archetypes=["Futurist alt girlfriend", "Gamer-room romance", "Late-shift intimacy"],
        moods=["clever", "restless", "devoted"],
        on_screen_mood="Irony masks longing until the headset comes off.",
        off_screen_mood="Mechanical keyboard ASMR jokes; fiercely punctual.",
        performance_style="Tech-naturalism; intimacy in LED glow.",
        voice_notes="Dry Pacific Northwest delivery; softens on goodnight lines.",
        personality="Builds worlds online; craves offline honesty.",
        signature_looks="Silver bob; RGB glow rim light; oversized hoodie to slip dress shift.",
        casting_notes="Panel 3 bed pose uses warm practical lamp not explicit staging.",
        tattoos=_TATTOO_LIGHT,
        wardrobe_color="electric blue",
        dob="October 27, 2002",
        full_legal_name="Nova Rei Takahashi",
    ),
    _gfe(
        stage_name="Ember",
        age=26,
        ethnicity="Japanese",
        nationality="Japan",
        heritage="Nagoya automotive family; underground jazz scene",
        languages=["Japanese (native)", "English (fluent)"],
        physical=(
            "5'6\", toned build, auburn-tinted black hair in shag cut, amber eyes, "
            "light olive skin, freckles across nose."
        ),
        archetypes=["Jazz-bar girlfriend", "Smoky intimacy lead", "Slow-burn romance"],
        moods=["smoldering", "witty", "nostalgic"],
        on_screen_mood="Cigarette-without-cigarette energy; heat in pauses.",
        off_screen_mood="Hums standards between setups; flirts with lighting crew.",
        performance_style="Phrasing like song lyrics; silence is a verse.",
        voice_notes="Smoky alto; laughs low in the chest.",
        personality="Romantic realist; remembers every small promise.",
        signature_looks="Shag cut; wine satin; throat tattoo peek in panel 1.",
        casting_notes="Warm tungsten in composite prompt for panel 3.",
        tattoos=_TATTOO_HEAVY,
        wardrobe_color="burnt orange",
        dob="May 5, 2000",
        full_legal_name="Ember Yoshida",
    ),
    _gfe(
        stage_name="Jade",
        age=25,
        ethnicity="Chinese-Japanese",
        nationality="Japan",
        heritage="Shanghai mother; Kyoto father; bilingual household",
        languages=["Japanese (native)", "Mandarin (fluent)", "English (fluent)"],
        physical=(
            "5'5\", graceful slim build, jade-green dip-dye on black hair, almond dark eyes, "
            "porcelain-gold skin."
        ),
        archetypes=["Elegant girlfriend fantasy", "Hotel-suite romance", "Slow-dance intimacy"],
        moods=["elegant", "mysterious", "devoted"],
        on_screen_mood="Poise until partner breaks the ritual.",
        off_screen_mood="Tea service on set; precise call times.",
        performance_style="Gesture economy; every turn intentional.",
        voice_notes="Mandarin-Japanese code-switch on emotional peaks.",
        personality="Ritual lover; chaos only with trusted partner.",
        signature_looks="Jade hair dip; satin dress; minimal gold jewelry.",
        casting_notes="Panel 1 white satin/black lace is wardrobe anchor.",
        tattoos=_TATTOO_MEDIUM,
        wardrobe_color="jade green",
        dob="September 19, 2000",
        full_legal_name="Jade Lin Watanabe",
    ),
    _gfe(
        stage_name="Scarlet",
        age=28,
        ethnicity="Japanese",
        nationality="Japan",
        heritage="Kabukicho-adjacent nightlife family (legitimate hospitality)",
        languages=["Japanese (native, Tokyo polished)", "English (fluent)"],
        physical=(
            "5'6\", curvy athletic build, true red-tinted black hair in voluminous waves, "
            "dark fox eyes, fair skin, bold lips."
        ),
        archetypes=["Mature girlfriend fantasy", "After-hours confessional", "Confidence-forward romance"],
        moods=["bold", "knowing", "generous"],
        on_screen_mood="Leads the scene until asked to surrender control.",
        off_screen_mood="Mentors younger cast; frank about boundaries.",
        performance_style="Camera-aware without breaking fourth wall in drama.",
        voice_notes="Confident mezzo; drops to whisper for vulnerability.",
        personality="Oldest-soul on roster; generosity without martyrdom.",
        signature_looks="Red-wave hair; scarlet lip; red string bikini hero panel.",
        casting_notes="Senior GFE member; age 28 locked in all prompts.",
        tattoos=_TATTOO_HEAVY,
        wardrobe_color="scarlet",
        dob="December 12, 1997",
        full_legal_name="Scarlet Inoue",
    ),
    _gfe(
        stage_name="Violet",
        age=22,
        ethnicity="Japanese-Brazilian",
        nationality="Brazil",
        heritage="São Paulo mother; Okinawa father",
        languages=["Portuguese (native)", "Japanese (fluent)", "English (conversational)"],
        physical=(
            "5'4\", dancer curves, violet-tinted black curls, lilac-brown eyes, "
            "caramel skin, wide smile."
        ),
        archetypes=["Carnival-to-quiet girlfriend", "Dance-then-intimacy arc", "Joyful romance lead"],
        moods=["joyful", "sensual", "grounded"],
        on_screen_mood="Party energy collapses into intimate stillness.",
        off_screen_mood="Samba steps in holding; hugs every background artist.",
        performance_style="Rhythm in hips and hands; dialogue secondary in love scenes.",
        voice_notes="Portuguese pet names; melodic laugh.",
        personality="Celebrates life loudly; private moments are sacred.",
        signature_looks="Violet curl tint; white satin; festival makeup to bare face.",
        casting_notes="Motion blur acceptable in panel 3 playful beat only.",
        tattoos=_TATTOO_MEDIUM,
        wardrobe_color="violet",
        dob="March 3, 2004",
        full_legal_name="Violet Okada Silva",
    ),
    _gfe(
        stage_name="Raven",
        age=24,
        ethnicity="Japanese-American",
        nationality="United States",
        heritage="Portland arts district; Hokkaido grandmother",
        languages=["English (native)", "Japanese (conversational)"],
        physical=(
            "5'5\", lean angular build, blue-black hair in wolf cut, pale grey-brown eyes, "
            "cool fair skin, sharp cupid's bow."
        ),
        archetypes=["Indie-goth girlfriend", "Record-store romance", "Rainy-window intimacy"],
        moods=["melancholic", "dry", "fierce"],
        on_screen_mood="Sad-girl aesthetic with steel underneath.",
        off_screen_mood="Recommends zines; allergic to small talk.",
        performance_style="Micro-flinch beats; excels in rain and neon.",
        voice_notes="Monotone until laughter breaks through.",
        personality="Art-school cynic who still believes in one person.",
        signature_looks="Wolf cut; black lace slip; smudged liner.",
        casting_notes="Pacific Northwest overcast lighting note for composite.",
        tattoos=_TATTOO_HEAVY,
        wardrobe_color="midnight blue",
        dob="June 21, 2002",
        full_legal_name="Raven Sato",
    ),
    _gfe(
        stage_name="Willow",
        age=23,
        ethnicity="Japanese",
        nationality="Japan",
        heritage="Kamakura temple-town adjacent; yoga-instructor lineage",
        languages=["Japanese (native)", "English (fluent)"],
        physical=(
            "5'6\", long-limbed yoga build, soft black hair in loose braid, calm brown eyes, "
            "warm beige skin, serene brow."
        ),
        archetypes=["Wellness girlfriend fantasy", "Morning ritual intimacy", "Breath-led romance"],
        moods=["calm", "sensual", "present"],
        on_screen_mood="Breath-synced closeness; touch after consent beat.",
        off_screen_mood="Leads stretch circle for cast; herbal tea on set.",
        performance_style="Body as text; stillness is dialogue.",
        voice_notes="ASMR-soft register; long exhales before lines.",
        personality="Boundaries articulated with grace; warmth without rush.",
        signature_looks="Loose braid; ivory satin; bare feet in panel 3.",
        casting_notes="Clinical consent language in intimate prompt extensions.",
        tattoos=_TATTOO_LIGHT,
        wardrobe_color="sage green",
        dob="April 8, 2003",
        full_legal_name="Willow Hayashi",
    ),
    _gfe(
        stage_name="Iris",
        age=25,
        ethnicity="Japanese-French",
        nationality="France",
        heritage="Lyon father; Nagasaki mother; Paris 11th upbringing",
        languages=["French (native)", "Japanese (fluent)", "English (fluent)"],
        physical=(
            "5'7\", elegant slim build, chestnut hair with honey balayage, grey-brown eyes, "
            "light olive skin, refined nose."
        ),
        archetypes=["Parisian-Japanese girlfriend", "Café-table romance", "Cigarette-and-wine intimacy"],
        moods=["chic", "wistful", "passionate"],
        on_screen_mood="European cool melts in Japanese tenderness beats.",
        off_screen_mood="Fashion references in every conversation.",
        performance_style="Wardrobe transitions signal emotional arcs.",
        voice_notes="French-Japanese code-switch; low intimate register.",
        personality="Aesthetic-driven but emotionally honest.",
        signature_looks="Balayage waves; white satin; thin gold chain.",
        casting_notes="Panel 1 lace trim reads European boudoir not costume.",
        tattoos=_TATTOO_LIGHT,
        wardrobe_color="champagne",
        dob="November 28, 2000",
        full_legal_name="Iris Moreau Tanaka",
    ),
    _gfe(
        stage_name="Sage",
        age=26,
        ethnicity="Japanese",
        nationality="Japan",
        heritage="Kanazawa gold-leaf crafts family; literature graduate",
        languages=["Japanese (native, literary register)", "English (fluent)"],
        physical=(
            "5'5\", bookish slim build, straight black hair with blunt glasses-off appeal, "
            "thoughtful dark eyes, pale skin, quiet lips."
        ),
        archetypes=["Intellectual girlfriend", "Library-to-bedroom arc", "Quote-heavy romance"],
        moods=["thoughtful", "dry", "suddenly bold"],
        on_screen_mood="Reads partner like a text until misread sparks heat.",
        off_screen_mood="Annotates scripts; recommends Murakami breaks.",
        performance_style="Subtext-heavy; silence after literary references.",
        voice_notes="Measured cadence; rushes when embarrassed.",
        personality="Introvert who chooses extroversion for love.",
        signature_looks="Blunt bob; glasses on/off beat; satin dress panel 1.",
        casting_notes="Glasses are optional continuity — pick one per project.",
        tattoos=_TATTOO_LIGHT,
        wardrobe_color="forest green",
        dob="January 30, 2000",
        full_legal_name="Sage Komatsu",
    ),
    _gfe(
        stage_name="Lyra",
        age=22,
        ethnicity="Japanese",
        nationality="Japan",
        heritage="Okinawa island roots; moved to Tokyo for music school",
        languages=["Japanese (native, Okinawan accent in casual)", "English (basic)"],
        physical=(
            "5'3\", petite toned build, sun-lightened brown hair, bright dark eyes, "
            "golden skin, easy grin."
        ),
        archetypes=["Island-pop girlfriend", "Ukulele serenade romance", "Barefoot intimacy"],
        moods=["breezy", "sweet", "stubborn"],
        on_screen_mood="Music as foreplay; sings before she confesses.",
        off_screen_mood="Hums on set; barefoot unless safety requires shoes.",
        performance_style="Song-and-touch beats; performance confidence in intimacy.",
        voice_notes="Bright soprano; Okinawan lilt on nicknames.",
        personality="Small-island loyalty; Tokyo hustle with island heart.",
        signature_looks="Sun-lightened hair; white string bikini; natural tan.",
        casting_notes="Panel 3 direct-to-camera smile is signature hook.",
        tattoos=_TATTOO_LIGHT,
        wardrobe_color="seafoam",
        dob="August 14, 2003",
        full_legal_name="Lyra Shimabukuro",
    ),
    _gfe(
        stage_name="Niko",
        age=27,
        ethnicity="Japanese-Thai",
        nationality="Thailand",
        heritage="Bangkok mother; Osaka father; night-market childhood",
        languages=["Thai (native)", "Japanese (fluent)", "English (fluent)"],
        physical=(
            "5'6\", athletic build, black hair in undercut with long top, sharp brown eyes, "
            "warm tan skin, strong brows."
        ),
        archetypes=["Night-market girlfriend", "Street-food romance", "Tough-soft intimacy"],
        moods=["bold", "playful", "guarded"],
        on_screen_mood="Teases until honesty is the only move left.",
        off_screen_mood="Brings street food; negotiates like a pro.",
        performance_style="Street realism; fights then forgiveness in one breath.",
        voice_notes="Thai-Japanese switch on anger and affection.",
        personality="Survivor charm; generosity shown through food and fixes.",
        signature_looks="Undercut; red string bikini; gold neck chain.",
        casting_notes="Bangkok humidity sheen OK in panel 2 only.",
        tattoos=_TATTOO_MEDIUM,
        wardrobe_color="gold",
        dob="July 22, 1998",
        full_legal_name="Niko Srinak Mori",
    ),
]