#!/usr/bin/env python3
"""T2 #198 — spec-only: Creator #3 teardown viz plates + next-12 ACTORS figure plate specs."""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

WORKSPACE = Path(__file__).resolve().parents[2]
CREATOR_SPECS = (
    WORKSPACE / "Science" / "reference_plates" / "creator" / "creator_3_how_it_works_teardown_specs.json"
)
NEXT_12_REGISTRY = WORKSPACE / "History" / "Historical_Figures_Bible" / "registry" / "v1_next_12.json"
ACTORS_SPECS = (
    WORKSPACE / "History" / "Historical_Figures_Bible" / "registry" / "t2_198_next_12_actors_plate_specs.json"
)
SUMMARY_PATH = WORKSPACE / "History" / "Historical_Figures_Bible" / "registry" / "t2_198_spec_summary.json"

DISCLOSURE = "SPECULATIVE AI RECONSTRUCTION — NOT PHOTOGRAPHIC LIKENESS"
TURNAROUND_PREFIX = (
    "INTERPRETIVE HISTORICAL RECONSTRUCTION PLATE — NOT photographic likeness. "
    "16:9 three-view turnaround on solid neutral grey #808080. "
    "LEFT profile left, CENTER front three-quarter, RIGHT profile right. "
    "Full-length wide shot every panel — head to toe, feet visible. "
)
TURNAROUND_SUFFIX = (
    " Lower margin legible text: SPECULATIVE AI RECONSTRUCTION — NOT PHOTOGRAPHIC LIKENESS. "
    "Synthetic interpretive figure only. No celebrity likeness. No living-person impersonation."
)

CREATOR_TEARDOWN_PLATES: list[dict[str, Any]] = [
    {
        "plate_id": "@Creator-TearDown-001",
        "slug": "lithium-ion-cell",
        "subject": "Lithium-ion battery cell — layered teardown",
        "domain": "engineering",
        "field": "chemistry",
        "principle_set": "general_scientific",
        "source": {
            "primary_citation": "NREL Battery Research — Li-ion cell architecture (cathode, separator, anode, current collectors)",
            "repository": "NREL / DOE battery education materials",
            "url": "https://www.nrel.gov/transportation/batteries.html",
            "license": "U.S. Government work / educational use",
        },
        "illustrative_note": "Teaches jelly-roll vs stacked pouch anatomy — not a branded phone battery. Label MODEL.",
        "plate_spec": {
            "plate_type": "creator_how_it_works_teardown_v1",
            "status": "SPEC_ONLY",
            "canvas": "16:9",
            "teardown_view": "exploded_lateral",
            "imagine_prompt": (
                "Scientific engineering teardown visualization, lithium-ion pouch cell exploded lateral view — "
                "aluminum pouch shell, copper anode current collector, graphite anode layer, polymer separator, "
                "lithium-metal-oxide cathode, aluminum cathode collector, electrolyte fill zone indicated, "
                "clean neutral #E8EEF2 background, Observable cool-clinical documentary style, "
                "no brand logos, no flame or explosion, 16:9, space for MODEL chip lower-left"
            ),
            "plate_lock_verbatim": (
                "Li-ion cell teardown — pouch layers: cathode | separator | anode | collectors; "
                "MODEL illustrative cross-section, not CT scan, no Samsung/Apple branding."
            ),
            "fidelity_anchors": [
                "Separator between anode and cathode",
                "Dual current collectors",
                "Pouch enclosure",
            ],
            "prohibited": [
                "Brand logos",
                "Thermal runaway fire",
                "Single-block battery without layers",
            ],
            "component_zones": ["pouch", "cathode", "separator", "anode", "collectors", "electrolyte"],
            "on_screen_labels": ["MODEL", "ILLUSTRATIVE"],
            "delivery_filename": "lithium_ion_cell_teardown_reference.jpg",
            "reference_file": "Science/reference_plates/creator/lithium_ion_cell_teardown_reference.jpg",
        },
    },
    {
        "plate_id": "@Creator-TearDown-002",
        "slug": "brushless-motor",
        "subject": "Brushless DC motor — magnetic path teardown",
        "domain": "engineering",
        "field": "physics",
        "principle_set": "general_scientific",
        "source": {
            "primary_citation": "NIST / engineering physics — BLDC stator windings, permanent-magnet rotor, Hall sensors",
            "repository": "Textbook-established motor topology",
            "url": "https://www.nist.gov/pml",
            "license": "Educational / public domain synthesis",
        },
        "illustrative_note": "Shows stator/rotor magnetic circuit for creator explainers — not a specific drone SKU.",
        "plate_spec": {
            "plate_type": "creator_how_it_works_teardown_v1",
            "status": "SPEC_ONLY",
            "canvas": "16:9",
            "teardown_view": "isometric_exploded",
            "imagine_prompt": (
                "Scientific engineering teardown, brushless DC motor isometric exploded view — "
                "stator with three-phase copper windings, permanent-magnet rotor ring, shaft, "
                "bearing seats, optional Hall sensor PCB, magnetic flux arrows subtle and accurate, "
                "neutral clinical background, no consumer product branding, documentary engineering, 16:9"
            ),
            "plate_lock_verbatim": (
                "BLDC motor teardown — stator windings + PM rotor + shaft; flux path visible; "
                "MODEL illustrative, no DJI/Apple trademark housings."
            ),
            "fidelity_anchors": ["Stator windings", "Permanent-magnet rotor", "Shaft and bearings"],
            "prohibited": ["Branded drone shell", "Universal motor brushes", "Cartoon magnets"],
            "component_zones": ["stator", "rotor", "shaft", "bearings", "sensors"],
            "on_screen_labels": ["MODEL", "ILLUSTRATIVE"],
            "delivery_filename": "brushless_motor_teardown_reference.jpg",
            "reference_file": "Science/reference_plates/creator/brushless_motor_teardown_reference.jpg",
        },
    },
    {
        "plate_id": "@Creator-TearDown-003",
        "slug": "cmos-camera-stack",
        "subject": "Smartphone CMOS camera module stack",
        "domain": "engineering",
        "field": "physics",
        "principle_set": "general_scientific",
        "source": {
            "primary_citation": "IEEE / SPIE smartphone optics — lens stack, IR filter, CMOS sensor, OIS voice-coil",
            "repository": "Peer-reviewed mobile imaging reviews",
            "license": "Educational synthesis",
        },
        "illustrative_note": "Lens-sensor stack for 'how autofocus works' — generic module, no iPhone silhouette.",
        "plate_spec": {
            "plate_type": "creator_how_it_works_teardown_v1",
            "status": "SPEC_ONLY",
            "canvas": "16:9",
            "teardown_view": "exploded_lateral",
            "imagine_prompt": (
                "Scientific camera module teardown, smartphone CMOS stack exploded lateral — "
                "aspheric lens elements, IR-cut filter, CMOS Bayer sensor die, autofocus voice-coil "
                "actuator, ceramic lens barrel, flex PCB bond pads, neutral grey background, "
                "documentary optics fidelity, no phone chassis branding, 16:9"
            ),
            "plate_lock_verbatim": (
                "CMOS module teardown — lens stack → IR filter → sensor → VCM actuator; "
                "MODEL not die photograph, no Apple/Samsung housing."
            ),
            "fidelity_anchors": ["Multi-element lens", "Bayer CMOS sensor", "Voice-coil AF"],
            "prohibited": ["Phone back glass with logo", "DSLR mirror box", "Fake macro bug-eye lens"],
            "component_zones": ["lenses", "ir_filter", "sensor", "vcm", "flex_pcb"],
            "on_screen_labels": ["MODEL", "ILLUSTRATIVE", "NOT TO SCALE"],
            "delivery_filename": "cmos_camera_stack_teardown_reference.jpg",
            "reference_file": "Science/reference_plates/creator/cmos_camera_stack_teardown_reference.jpg",
        },
    },
    {
        "plate_id": "@Creator-TearDown-004",
        "slug": "hard-disk-drive",
        "subject": "Hard disk drive — magnetic recording teardown",
        "domain": "engineering",
        "field": "physics",
        "principle_set": "general_scientific",
        "source": {
            "primary_citation": "Seagate / IBM Almaden HDD primer — platters, read/write head, voice-coil actuator, spindle",
            "repository": "Industry educational HDD diagrams",
            "license": "Educational fair-use synthesis",
        },
        "illustrative_note": "Classic HDD anatomy for storage explainers — not SSD/NVMe.",
        "plate_spec": {
            "plate_type": "creator_how_it_works_teardown_v1",
            "status": "SPEC_ONLY",
            "canvas": "16:9",
            "teardown_view": "cutaway_top",
            "imagine_prompt": (
                "Scientific engineering teardown, hard disk drive cutaway top view — "
                "aluminum platters, read/write head on actuator arm, voice-coil actuator pivot, "
                "spindle motor hub, sealed chamber indicated, clinical neutral background, "
                "no brand decals, documentary precision, 16:9"
            ),
            "plate_lock_verbatim": (
                "HDD teardown — platters + R/W head + VCM actuator + spindle; sealed chamber; "
                "MODEL illustrative, not SSD."
            ),
            "fidelity_anchors": ["Magnetic platters", "Actuator arm", "Spindle motor"],
            "prohibited": ["SSD flash chips", "Brand logo top cover", "Exposed dust contamination glam"],
            "component_zones": ["platters", "head", "actuator", "spindle", "chassis"],
            "on_screen_labels": ["MODEL", "ILLUSTRATIVE"],
            "delivery_filename": "hard_disk_drive_teardown_reference.jpg",
            "reference_file": "Science/reference_plates/creator/hard_disk_drive_teardown_reference.jpg",
        },
    },
    {
        "plate_id": "@Creator-TearDown-005",
        "slug": "microwave-magnetron",
        "subject": "Microwave oven — magnetron and waveguide teardown",
        "domain": "engineering",
        "field": "physics",
        "principle_set": "general_scientific",
        "source": {
            "primary_citation": "FDA / NIST microwave oven engineering — magnetron cavity, waveguide, stirrer, Faraday cage",
            "repository": "FDA consumer physics notes",
            "url": "https://www.fda.gov/radiation-emitting-products/home-business-and-entertainment-products/microwave-ovens",
            "license": "U.S. Government educational",
        },
        "illustrative_note": "2.45 GHz heating path — never show exposed operation glam.",
        "plate_spec": {
            "plate_type": "creator_how_it_works_teardown_v1",
            "status": "SPEC_ONLY",
            "canvas": "16:9",
            "teardown_view": "cutaway_lateral",
            "imagine_prompt": (
                "Scientific engineering teardown, microwave oven cutaway lateral — "
                "cavity magnetron tube with copper fins, waveguide to cooking chamber, "
                "metal stirrer fan, Faraday mesh door screen, turntable motor, "
                "safety interlock switch indicated, neutral clinical background, no food glam, 16:9"
            ),
            "plate_lock_verbatim": (
                "Microwave teardown — magnetron → waveguide → chamber + mesh door; "
                "MODEL illustrative; no operating oven with exposed microwaves."
            ),
            "fidelity_anchors": ["Magnetron tube", "Waveguide", "Faraday mesh door"],
            "prohibited": ["Glowing plasma inside home kitchen", "Removed door operating", "Brand logo"],
            "component_zones": ["magnetron", "waveguide", "chamber", "door_mesh", "turntable"],
            "on_screen_labels": ["MODEL", "ILLUSTRATIVE"],
            "delivery_filename": "microwave_magnetron_teardown_reference.jpg",
            "reference_file": "Science/reference_plates/creator/microwave_magnetron_teardown_reference.jpg",
        },
    },
    {
        "plate_id": "@Creator-TearDown-006",
        "slug": "led-bulb",
        "subject": "LED bulb — solid-state lighting teardown",
        "domain": "engineering",
        "field": "physics",
        "principle_set": "general_scientific",
        "source": {
            "primary_citation": "DOE SSL program — LED die, phosphor converter, driver PCB, heatsink",
            "repository": "U.S. DOE Solid-State Lighting",
            "url": "https://www.energy.gov/eere/ssl",
            "license": "U.S. Government work",
        },
        "illustrative_note": "Replaces incandescent filament misconception with LED + driver anatomy.",
        "plate_spec": {
            "plate_type": "creator_how_it_works_teardown_v1",
            "status": "SPEC_ONLY",
            "canvas": "16:9",
            "teardown_view": "exploded_lateral",
            "imagine_prompt": (
                "Scientific engineering teardown, A19 LED bulb exploded lateral — "
                "LED chip on MCPCB, yellow phosphor dome, aluminum heatsink fins, "
                "constant-current driver PCB, Edison screw base, diffuser globe shell, "
                "neutral background, no brand silkscreen, documentary lighting engineering, 16:9"
            ),
            "plate_lock_verbatim": (
                "LED bulb teardown — LED die + phosphor + heatsink + driver + base; "
                "MODEL illustrative, not incandescent filament."
            ),
            "fidelity_anchors": ["LED die on MCPCB", "Phosphor converter", "Driver PCB", "Heatsink"],
            "prohibited": ["Incandescent filament", "CFL spiral tube only", "Brand logo"],
            "component_zones": ["led_die", "phosphor", "heatsink", "driver", "base", "diffuser"],
            "on_screen_labels": ["MODEL", "ILLUSTRATIVE"],
            "delivery_filename": "led_bulb_teardown_reference.jpg",
            "reference_file": "Science/reference_plates/creator/led_bulb_teardown_reference.jpg",
        },
    },
]


def _plate_spec(
    *,
    age: int,
    appearance: str,
    costume: str,
    anchors: list[str],
    prompt_core: str,
    prohibited: list[str],
    slug: str,
) -> dict[str, Any]:
    return {
        "plate_type": "historical_reconstruction_turnaround_v1",
        "status": "SPEC_ONLY",
        "canvas": "16:9",
        "views": ["front_three_quarter", "profile_left", "profile_right"],
        "age_at_depiction": age,
        "appearance_lock_verbatim": appearance,
        "costume_lock_verbatim": costume,
        "reference_anchors": anchors,
        "imagine_prompt": prompt_core,
        "prohibited": prohibited,
        "delivery_filename": f"{slug}_reconstruction_plate_v1.jpg",
        "spec_issue": 198,
    }


def _actors_prompt(core: str) -> str:
    return f"{TURNAROUND_PREFIX}{core.strip()}{TURNAROUND_SUFFIX}"


NEXT_12_FIGURES: list[dict[str, Any]] = [
    {
        "id": "ROM-004",
        "slug": "marcus-aurelius",
        "name": "Marcus Aurelius",
        "birth_death": "121–180 CE",
        "birth_year": 121,
        "death_year": 180,
        "death_year_floor_pass": True,
        "era": "High Roman Empire — Antonine dynasty (2nd century CE)",
        "region_civilization": "Roman Italy / Danube frontier",
        "titles_roles": ["Roman Emperor (161–180 CE)", "Stoic philosopher", "Philosopher-king"],
        "appearance_basis": {
            "likeness_tier": "attested_visual",
            "summary": "Capitoline equestrian bronze and Antonine busts — full beard, mature emperor.",
            "permitted_claims": ["Full beard per Capitoline type", "Equestrian armor", "Mature 50s–59"],
            "explicit_gaps": ["Eye color not specified", "No Gladiator film casting"],
            "sources": [
                {
                    "type": "sculpture",
                    "label": "Capitoline Equestrian Statue of Marcus Aurelius",
                    "citation": "Bronze equestrian statue, Musei Capitolini, Rome, c. 175–180 CE",
                }
            ],
        },
        "period_languages": [{"language": "Latin (Classical)", "role": "Imperial administration"}],
        "anchor_facts": ["Author of Meditations", "Marcomannic Wars", "Died 180 CE"],
        "reconstruction_plate_spec": _plate_spec(
            age=58,
            appearance=(
                "Marcus Aurelius age 58, Capitoline equestrian and Antonine bust — full beard with drilled curls, "
                "mature weathered face, equestrian armor with paludamentum, Stoic bearing, no Hollywood casting."
            ),
            costume="Antonine muscled cuirass or scale armor, purple paludamentum.",
            anchors=["Capitoline Equestrian Statue", "Antonine portrait bust", "RIC III coin portrait"],
            prompt_core=(
                "Historical reconstruction, Marcus Aurelius age 58, Capitoline equestrian and Antonine bust — "
                "full beard, curly hair, mature emperor, equestrian armor, purple cloak, philosopher-king, "
                "documentary museum lighting, 16:9, no Gladiator casting."
            ),
            prohibited=["Gladiator (2000) likeness", "Clean-shaven face", "Medieval plate armor"],
            slug="marcus-aurelius",
        ),
        "roster_crossref": "History/data/roster.json#ROM-004",
        "tags": ["rome", "stoicism", "emperor"],
    },
    {
        "id": "HEN-001",
        "slug": "henry-ii",
        "name": "Henry II",
        "birth_death": "1133–1189",
        "birth_year": 1133,
        "death_year": 1189,
        "death_year_floor_pass": True,
        "era": "High Medieval — Angevin Empire (12th century)",
        "region_civilization": "Angevin Plantagenet",
        "titles_roles": ["King of England (1154–1189)", "Duke of Normandy", "Count of Anjou"],
        "appearance_basis": {
            "likeness_tier": "partial_visual",
            "summary": "Fontevraud effigy — crowned Plantagenet king; no youth portrait.",
            "permitted_claims": ["Crowned recumbent king per effigy", "Compact energetic build"],
            "explicit_gaps": ["Hair and eye color not attested"],
            "sources": [
                {
                    "type": "effigy",
                    "label": "Fontevraud Abbey effigy of Henry II",
                    "citation": "Royal Abbey of Fontevraud, recumbent effigy c. 1204",
                }
            ],
        },
        "period_languages": [{"language": "Anglo-Norman French", "role": "Court language"}],
        "anchor_facts": ["Becket conflict 1170", "Constitutions of Clarendon", "Died at Chinon 1189"],
        "reconstruction_plate_spec": _plate_spec(
            age=50,
            appearance=(
                "Henry II age 50, Fontevraud effigy — compact energetic Angevin king, royal mantle, "
                "mature 12th-century bearing, no invented facial specifics beyond effigy form."
            ),
            costume="12th-c. Angevin royal mantle, hunting dress, crown for formal scenes.",
            anchors=["Fontevraud effigy of Henry II"],
            prompt_core=(
                "Historical reconstruction, Henry II age 50, Fontevraud effigy — Angevin king, royal mantle, "
                "12th-century court, Plantagenet continuity, documentary lighting, 16:9."
            ),
            prohibited=["Modern fantasy armor", "Celebrity likeness"],
            slug="henry-ii",
        ),
        "roster_crossref": "History/data/roster.json#HEN-001",
        "tags": ["angevin", "becket"],
    },
    {
        "id": "THO-001",
        "slug": "thomas-becket",
        "name": "Thomas Becket",
        "birth_death": "1119/20–1170",
        "birth_year": 1120,
        "death_year": 1170,
        "death_year_floor_pass": True,
        "era": "High Medieval Angevin (12th century)",
        "region_civilization": "Plantagenet / Canterbury",
        "titles_roles": ["Archbishop of Canterbury", "Former Chancellor"],
        "appearance_basis": {
            "likeness_tier": "partial_visual",
            "summary": "Canterbury Trinity Chapel windows and reliquary tradition — archbishop in pallium and mitre.",
            "permitted_claims": ["Archbishop liturgical dress", "Mature cleric bearing"],
            "explicit_gaps": ["No verified lifetime facial portrait"],
            "sources": [
                {
                    "type": "manuscript_illustration",
                    "label": "Canterbury Cathedral Trinity Chapel Becket windows",
                    "citation": "Canterbury stained glass martyr cycle, 12th–13th c.",
                },
                {
                    "type": "primary_description",
                    "label": "Edward Grim eyewitness account 1170",
                    "citation": "Edward Grim, murder of Becket at Canterbury Cathedral",
                },
            ],
        },
        "period_languages": [{"language": "Latin (Medieval)", "role": "Church administration"}],
        "anchor_facts": ["Chancellor to archbishop", "Murdered Canterbury 1170", "Martyr and saint"],
        "reconstruction_plate_spec": _plate_spec(
            age=50,
            appearance=(
                "Thomas Becket age 50, Canterbury martyr tradition — mature archbishop, strong clerical bearing, "
                "pallium and mitre, 12th-century English churchman, no Hollywood glam."
            ),
            costume="Archbishop pallium, mitre, chasuble; episcopal staff for formal depiction.",
            anchors=["Canterbury Trinity Chapel windows", "Edward Grim eyewitness 1170"],
            prompt_core=(
                "Historical reconstruction, Thomas Becket age 50, Canterbury archbishop — pallium, mitre, "
                "12th-century liturgical dress, martyr bishop bearing, documentary lighting, 16:9."
            ),
            prohibited=["Royal knight armor", "Celebrity likeness", "19th-c. romantic opera styling"],
            slug="thomas-becket",
        ),
        "roster_crossref": "History/data/roster.json#THO-001",
        "tags": ["church", "martyrdom", "angevin"],
    },
    {
        "id": "GRC-001",
        "slug": "alexander-the-great",
        "name": "Alexander the Great",
        "birth_death": "356–323 BCE",
        "birth_year": -356,
        "death_year": -323,
        "death_year_floor_pass": True,
        "era": "Hellenistic Age — Macedonian expansion (4th century BCE)",
        "region_civilization": "Ancient Macedon",
        "titles_roles": ["King of Macedon", "Hegemon of the Hellenic League"],
        "appearance_basis": {
            "likeness_tier": "attested_visual",
            "summary": "Lysippan tradition — Alexander Mosaic, coins, sarcophagus reliefs.",
            "permitted_claims": ["Anastole upswept hair", "Lean athletic build", "Royal diadem"],
            "explicit_gaps": ["Heterochromia tradition disputed"],
            "sources": [
                {
                    "type": "mosaic",
                    "label": "Alexander Mosaic (Pompeii)",
                    "citation": "House of the Faun, Naples Archaeological Museum",
                }
            ],
        },
        "period_languages": [{"language": "Ancient Greek (Koine)", "role": "Court and command"}],
        "anchor_facts": ["Gaugamela 331 BCE", "Campaign to India", "Died Babylon 323 BCE"],
        "reconstruction_plate_spec": _plate_spec(
            age=30,
            appearance=(
                "Alexander the Great age 30, Lysippan tradition — lean athletic build, anastole upswept hair, "
                "royal diadem, Macedonian royal bearing, no modern film casting."
            ),
            costume="Macedonian cuirass, chlamys, diadem; Persian robes only for specific court scenes.",
            anchors=["Alexander Mosaic Naples", "Macedonian tetradrachm profile"],
            prompt_core=(
                "Historical reconstruction, Alexander the Great age 30, Lysippan type — anastole hair, "
                "lean athletic, royal diadem, 4th c. BCE Macedon, documentary lighting, 16:9."
            ),
            prohibited=["Colin Farrell likeness", "Medieval armor"],
            slug="alexander-the-great",
        ),
        "roster_crossref": "History/data/roster.json#GRC-001",
        "tags": ["macedon", "hellenistic"],
    },
    {
        "id": "EGY-001",
        "slug": "tutankhamun",
        "name": "Tutankhamun",
        "birth_death": "c. 1341–1323 BCE",
        "birth_year": -1341,
        "death_year": -1323,
        "death_year_floor_pass": True,
        "era": "New Kingdom Egypt — Amarna restoration (18th dynasty)",
        "region_civilization": "Ancient Egypt",
        "titles_roles": ["Pharaoh", "King of Upper and Lower Egypt"],
        "appearance_basis": {
            "likeness_tier": "attested_visual",
            "summary": "KV62 gold mask — idealized royal iconography, late-teen age.",
            "permitted_claims": ["Youthful face per mask", "Nemes headdress with uraeus"],
            "explicit_gaps": ["Mask is funerary idealization not candid portrait"],
            "sources": [
                {
                    "type": "artifact",
                    "label": "Gold funerary mask KV62",
                    "citation": "Tutankhamun tomb, Valley of the Kings, c. 1323 BCE",
                }
            ],
        },
        "period_languages": [{"language": "Late Egyptian", "role": "Royal court"}],
        "anchor_facts": ["Tomb discovered 1922", "Amun cult restoration", "Died late teens"],
        "reconstruction_plate_spec": _plate_spec(
            age=18,
            appearance=(
                "Tutankhamun age 18, KV62 gold mask reference — youthful pharaoh, nemes headdress, "
                "idealized royal features, label as funerary iconography."
            ),
            costume="Royal nemes, pectoral collars, crook and flail; fine linen ceremonial dress.",
            anchors=["KV62 gold funerary mask"],
            prompt_core=(
                "Historical reconstruction, Tutankhamun age 18, KV62 gold mask — youthful Egyptian pharaoh, "
                "nemes headdress, New Kingdom, documentary museum lighting, 16:9."
            ),
            prohibited=["Adult mature depiction", "Modern drama casting"],
            slug="tutankhamun",
        ),
        "roster_crossref": "History/data/roster.json#EGY-001",
        "tags": ["egypt", "pharaoh"],
    },
    {
        "id": "CHN-001",
        "slug": "qin-shi-huang",
        "name": "Qin Shi Huang",
        "birth_death": "259–210 BCE",
        "birth_year": -259,
        "death_year": -210,
        "death_year_floor_pass": True,
        "era": "Qin dynasty (3rd century BCE)",
        "region_civilization": "Imperial China",
        "titles_roles": ["First Emperor of Qin", "King of Qin"],
        "appearance_basis": {
            "likeness_tier": "partial_visual",
            "summary": "No verified portrait — Terracotta workshop style for era; Shiji for regalia.",
            "permitted_claims": ["Imperial mianliu crown tradition", "Black dragon robe per Qin cosmology"],
            "explicit_gaps": ["Terracotta faces are warrior types not emperor likeness"],
            "sources": [
                {
                    "type": "archaeological",
                    "label": "Terracotta Army Lintong",
                    "citation": "Emperor Qinshihuang Mausoleum Site Museum, Pit 1–3",
                },
                {
                    "type": "primary_description",
                    "label": "Sima Qian, Shiji — Qin annals",
                    "citation": "Records of the Grand Historian, First Emperor chronicle",
                },
            ],
        },
        "period_languages": [{"language": "Old Chinese (Qin)", "role": "Imperial court"}],
        "anchor_facts": ["Unified China 221 BCE", "Terracotta Army", "Died 210 BCE"],
        "reconstruction_plate_spec": _plate_spec(
            age=49,
            appearance=(
                "Qin Shi Huang age 49, Shiji imperial regalia tradition — authoritative First Emperor bearing, "
                "no verified facial likeness, era-appropriate Qin workshop style face genericized, "
                "black imperial robe cosmology, no Terracotta warrior face copy."
            ),
            costume="Qin imperial mianliu crown, black dragon robe, jade belt ornaments.",
            anchors=["Sima Qian Shiji First Emperor", "Terracotta Army era costume archaeology"],
            prompt_core=(
                "Historical reconstruction, Qin Shi Huang age 49, Shiji regalia — black imperial robe, "
                "mianliu crown, 3rd c. BCE China, documentary dignity, no verified portrait invention, 16:9."
            ),
            prohibited=["Terracotta soldier face as emperor", "Han/Tang anachronism", "Wuxia glam"],
            slug="qin-shi-huang",
        ),
        "roster_crossref": "History/data/roster.json#CHN-001",
        "tags": ["china", "emperor", "qin"],
    },
    {
        "id": "AZT-001",
        "slug": "montezuma-ii",
        "name": "Moctezuma II",
        "birth_death": "c. 1466–1520",
        "birth_year": 1466,
        "death_year": 1520,
        "death_year_floor_pass": True,
        "era": "Late Postclassic Mesoamerica (Aztec Empire)",
        "region_civilization": "Aztec (Mexica)",
        "titles_roles": ["Tlatoani of Tenochtitlan", "Huey Tlatoani"],
        "appearance_basis": {
            "likeness_tier": "partial_visual",
            "summary": "Codex Mendoza tlatoani depiction — regalia authoritative; face stylized.",
            "permitted_claims": ["Turquoise xiuhuitzolli crown", "Feathered tilma and maxtlatl"],
            "explicit_gaps": ["No verified naturalistic portrait"],
            "sources": [
                {
                    "type": "manuscript_illustration",
                    "label": "Codex Mendoza",
                    "citation": "Bodleian Library, Oxford — Mexica ruler portraits",
                },
                {
                    "type": "archaeological",
                    "label": "Templo Mayor INAH",
                    "citation": "Tenochtitlan archaeological zone, Mexico City",
                },
            ],
        },
        "period_languages": [{"language": "Classical Nahuatl", "role": "Imperial court"}],
        "anchor_facts": ["Tlatoani at empire height", "Cortés encounter 1519", "Fall of Tenochtitlan 1521"],
        "reconstruction_plate_spec": _plate_spec(
            age=52,
            appearance=(
                "Moctezuma II age 52, Codex Mendoza regalia tradition — mature tlatoani bearing, "
                "xiuhuitzolli crown, dignified Mesoamerican emperor, codex-mediated stylization acknowledged."
            ),
            costume="Turquoise xiuhuitzolli crown, feathered tilma, maxtlatl, gold lip plug tradition.",
            anchors=["Codex Mendoza tlatoani portrait", "Templo Mayor INAH regalia context"],
            prompt_core=(
                "Historical reconstruction, Moctezuma II age 52, Codex Mendoza — xiuhuitzolli crown, "
                "feathered tilma, Aztec imperial regalia, Postclassic Mesoamerica, documentary lighting, 16:9."
            ),
            prohibited=["VIenna headdress as verified portrait", "Conquistador armor on figure", "Hollywood Aztec glam"],
            slug="montezuma-ii",
        ),
        "roster_crossref": "History/data/roster.json#AZT-001",
        "tags": ["aztec", "mesoamerica"],
    },
    {
        "id": "WIL-002",
        "slug": "william-the-conqueror",
        "name": "William the Conqueror",
        "birth_death": "c. 1028–1087",
        "birth_year": 1028,
        "death_year": 1087,
        "death_year_floor_pass": True,
        "era": "11th-c. Norman",
        "region_civilization": "Norman / England",
        "titles_roles": ["Duke of Normandy", "King of England"],
        "appearance_basis": {
            "likeness_tier": "partial_visual",
            "summary": "Bayeux Tapestry stylized narrative — stocky Norman king; no facial likeness.",
            "permitted_claims": ["Stocky powerful build per chroniclers", "Norman royal mantle and gonfalon"],
            "explicit_gaps": ["Bayeux is not facial portrait", "Hair color from chronicler tradition only"],
            "sources": [
                {
                    "type": "textile",
                    "label": "Bayeux Tapestry",
                    "citation": "Musée de la Tapisserie de Bayeux, 11th c.",
                },
                {
                    "type": "primary_description",
                    "label": "William of Poitiers, Gesta Guillelmi",
                    "citation": "Norman chronicle tradition",
                },
            ],
        },
        "period_languages": [{"language": "Norman French", "role": "Court"}],
        "anchor_facts": ["Hastings 1066", "Domesday Book 1086", "Norman conquest of England"],
        "reconstruction_plate_spec": _plate_spec(
            age=59,
            appearance=(
                "William the Conqueror age 59, Bayeux Tapestry and chronicler tradition — stocky powerful Norman, "
                "mature king bearing, reddish hair tradition optional, no tapestry cartoon face copy."
            ),
            costume="Norman royal mantle, mail hauberk for military scenes, gonfalon banner.",
            anchors=["Bayeux Tapestry William scenes", "Orderic Vitalis chronicle tradition"],
            prompt_core=(
                "Historical reconstruction, William the Conqueror age 59, Norman king — stocky build, "
                "royal mantle, 11th-century harness, documentary lighting, 16:9, no tapestry cartoon face."
            ),
            prohibited=["Bayeux cartoon facial copy", "High medieval plate armor anachronism"],
            slug="william-the-conqueror",
        ),
        "roster_crossref": "History/data/roster.json#WIL-002",
        "tags": ["norman", "conquest"],
    },
    {
        "id": "SAL-001",
        "slug": "saladin",
        "name": "Saladin",
        "birth_death": "1137–1193",
        "birth_year": 1137,
        "death_year": 1193,
        "death_year_floor_pass": True,
        "era": "Ayyubid / Crusader era (12th c.)",
        "region_civilization": "Ayyubid Sultanate",
        "titles_roles": ["Sultan of Egypt and Syria"],
        "appearance_basis": {
            "likeness_tier": "text_only",
            "summary": "Baha al-Din ibn Shaddad biography — temperament and dress; no verified portrait.",
            "permitted_claims": ["Turban and Ayyubid kaftan", "Mature sultan bearing", "Modest scholarly dignity"],
            "explicit_gaps": ["No facial features attested", "Later miniatures are secondary only"],
            "sources": [
                {
                    "type": "primary_description",
                    "label": "Baha al-Din ibn Shaddad, al-Nawadir al-Sultaniyya",
                    "citation": "Eyewitness biography of Saladin",
                }
            ],
        },
        "period_languages": [{"language": "Arabic (Medieval)", "role": "Court and command"}],
        "anchor_facts": ["Hattin 1187", "Jerusalem recapture", "Third Crusade vs Richard I"],
        "reconstruction_plate_spec": _plate_spec(
            age=55,
            appearance=(
                "Saladin age 55, Baha al-Din tradition — mature Ayyubid sultan, turban and kaftan, "
                "dignified bearing, generic face (no verified likeness), no Hollywood Crusades casting."
            ),
            costume="Ayyubid turban, kaftan, sword belt; no European crusader armor.",
            anchors=["Baha al-Din ibn Shaddad biography", "Ayyubid dress archaeology secondary"],
            prompt_core=(
                "Historical reconstruction, Saladin age 55, Ayyubid sultan — turban, kaftan, "
                "12th-century Islamic court dress, text-only likeness tier, documentary dignity, 16:9."
            ),
            prohibited=["Verified portrait claim from later miniatures", "Richard Gere / celebrity likeness"],
            slug="saladin",
        ),
        "roster_crossref": "History/data/roster.json#SAL-001",
        "tags": ["crusades", "ayyubid"],
    },
    {
        "id": "JPN-001",
        "slug": "murasaki-shikibu",
        "name": "Murasaki Shikibu",
        "birth_death": "c. 973–1014",
        "birth_year": 973,
        "death_year": 1014,
        "death_year_floor_pass": True,
        "era": "Heian period (10th–11th c.)",
        "region_civilization": "Japan — Imperial court",
        "titles_roles": ["Lady-in-waiting", "Author of The Tale of Genji"],
        "appearance_basis": {
            "likeness_tier": "no_contemporary_likeness",
            "summary": "No contemporary portrait — Heian junihitoe court dress from era archaeology and Genji scrolls.",
            "permitted_claims": ["Heian court lady junihitoe layers", "Long hair tradition", "Composed court bearing"],
            "explicit_gaps": ["No facial likeness", "Do not invent beauty from fiction illustrations alone"],
            "sources": [
                {
                    "type": "manuscript_illustration",
                    "label": "Tale of Genji emaki (12th c. scrolls)",
                    "citation": "Heian court costume reference — not author portrait",
                },
                {
                    "type": "primary_description",
                    "label": "Murasaki Shikibu Diary (Muraski Shikibu nikki)",
                    "citation": "Heian court autobiographical text, early 11th c.",
                },
            ],
        },
        "period_languages": [{"language": "Classical Japanese (Heian)", "role": "Court literature"}],
        "anchor_facts": ["Author of Genji monogatari", "Heian court service", "Pioneer of novel form"],
        "reconstruction_plate_spec": _plate_spec(
            age=38,
            appearance=(
                "Murasaki Shikibu age 38, Heian court lady — junihitoe layered robes, long black hair, "
                "composed scholarly bearing, no contemporary likeness, generic dignified face."
            ),
            costume="Heian junihitoe twelve-layer court dress, fan, court hairstyle.",
            anchors=["Heian junihitoe archaeology", "Genji emaki costume reference (not portrait)"],
            prompt_core=(
                "Historical reconstruction, Murasaki Shikibu age 38, Heian court lady — junihitoe robes, "
                "long hair, imperial court Japan 11th c., no verified likeness, documentary dignity, 16:9."
            ),
            prohibited=["Modern kimono anachronism", "Anime face style", "Claimed portrait from fiction scrolls"],
            slug="murasaki-shikibu",
        ),
        "roster_crossref": "History/figures/murasaki-shikibu/research/research_brief.json",
        "tags": ["japan", "heian", "literature"],
    },
    {
        "id": "GRE-001",
        "slug": "hypatia-alexandria",
        "name": "Hypatia of Alexandria",
        "birth_death": "c. 360–415 CE",
        "birth_year": 360,
        "death_year": 415,
        "death_year_floor_pass": True,
        "era": "Late Roman Alexandria / Neoplatonism",
        "region_civilization": "Roman Egypt",
        "titles_roles": ["Philosopher", "Mathematician", "Astronomer"],
        "appearance_basis": {
            "likeness_tier": "text_only",
            "summary": "Socrates Scholasticus and Damascius — philosopher teacher; no contemporary portrait.",
            "permitted_claims": ["Mature woman scholar", "Late Roman mantle and tunic"],
            "explicit_gaps": ["No eye color, skin tone, or facial structure attested"],
            "sources": [
                {
                    "type": "primary_description",
                    "label": "Socrates Scholasticus, Ecclesiastical History VII.15",
                    "citation": "Philosopher of Alexandria, public teacher",
                }
            ],
        },
        "period_languages": [{"language": "Ancient Greek", "role": "Philosophical teaching"}],
        "anchor_facts": ["Neoplatonist philosopher", "Murdered Alexandria 415", "Daughter of Theon"],
        "reconstruction_plate_spec": _plate_spec(
            age=45,
            appearance=(
                "Hypatia of Alexandria age 45, primary chronicle descriptions only — mature woman scholar, "
                "dignified philosopher bearing, late Roman Alexandrian dress, no surviving portrait."
            ),
            costume="Late Roman scholar mantle over linen tunic, modest stole, sandals.",
            anchors=["Socrates Scholasticus VII.15", "Damascius Life of Isidore fragment"],
            prompt_core=(
                "Historical reconstruction, Hypatia of Alexandria age 45 — philosopher scholar, "
                "mantle and linen tunic, late Roman Alexandria, text-only likeness, documentary dignity, 16:9."
            ),
            prohibited=["Rachel Weisz / Agora film likeness", "Pagan priestess glam", "Celebrity face"],
            slug="hypatia-alexandria",
        ),
        "roster_crossref": "History/Historical_Figures_Bible/entries/hypatia_alexandria.json",
        "tags": ["alexandria", "philosophy", "neoplatonism"],
    },
    {
        "id": "ROM-002",
        "slug": "augustus",
        "name": "Augustus (Octavian)",
        "birth_death": "63 BCE–14 CE",
        "birth_year": -63,
        "death_year": 14,
        "death_year_floor_pass": True,
        "era": "Early Roman Empire (1st c. BCE–1st c. CE)",
        "region_civilization": "Roman Italy",
        "titles_roles": ["First Roman Emperor", "Princeps"],
        "appearance_basis": {
            "likeness_tier": "attested_visual",
            "summary": "Prima Porta and Augustan portrait type — youthful ideal, comma curls, clean-shaven.",
            "permitted_claims": ["Augustan comma curls", "Primaporta cuirass reliefs", "Idealized youthful face"],
            "explicit_gaps": ["Skin tone from marble only"],
            "sources": [
                {
                    "type": "sculpture",
                    "label": "Augustus of Prima Porta",
                    "citation": "Vatican Museums — idealized Augustan portrait with cuirass",
                }
            ],
        },
        "period_languages": [{"language": "Latin (Classical)", "role": "Imperial administration"}],
        "anchor_facts": ["Actium 31 BCE", "Pax Romana architect", "First emperor"],
        "reconstruction_plate_spec": _plate_spec(
            age=35,
            appearance=(
                "Augustus age 35, Prima Porta portrait type — Augustan comma curls, clean-shaven idealized face, "
                "athletic build, early Empire bearing, no older gravitas of later portraits."
            ),
            costume="Muscled cuirass with Primaporta relief program, purple paludamentum.",
            anchors=["Augustus of Prima Porta", "Augustan portrait typology coins"],
            prompt_core=(
                "Historical reconstruction, Augustus age 35, Prima Porta type — comma curls, clean-shaven, "
                "cuirass breastplate, early Roman Empire, documentary museum lighting, 16:9."
            ),
            prohibited=["Older bearded Augustus type", "Medieval armor", "Modern political likeness"],
            slug="augustus",
        ),
        "roster_crossref": "History/data/roster.json#ROM-002",
        "tags": ["rome", "empire", "augustan"],
    },
]


def write_creator_specs() -> dict[str, Any]:
    CREATOR_SPECS.parent.mkdir(parents=True, exist_ok=True)
    doc = {
        "issue": 198,
        "task": "T2 #198 — Creator #3 How It Works teardown viz plate specs",
        "product": "Creator #3",
        "format": "how-it-works-teardown",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "swap_slot": "@2",
        "label_policy": ["MODEL", "ILLUSTRATIVE", "NOT TO SCALE"],
        "principle_set_default": "general_scientific",
        "feeds": ["Observable creator/B2B lane", "ACTORS teardown render queue"],
        "plates": CREATOR_TEARDOWN_PLATES,
        "total": len(CREATOR_TEARDOWN_PLATES),
    }
    CREATOR_SPECS.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return doc


def write_next_12_registry() -> dict[str, Any]:
    doc = {
        "issue": 198,
        "version": "1.1",
        "task": "T2 #198 — Historical Figures Bible next-12 ACTORS plate specs",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "death_year_floor": {
            "rule": "death_year ≤ current_year - 100",
            "as_of_year": 2026,
            "max_death_year": 1926,
            "all_entries_pass": True,
        },
        "bible_path": "History/Historical_Figures_Bible/Historical_Figures_Bible_v1.md",
        "schema_path": "History/Historical_Figures_Bible/schema/figure_bible_schema.json",
        "source_catalog": "History/research/v1_next_12_sources.md",
        "figures": NEXT_12_FIGURES,
    }
    NEXT_12_REGISTRY.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return doc


def write_actors_specs(registry: dict[str, Any]) -> dict[str, Any]:
    figures_out = []
    for fig in registry["figures"]:
        spec = fig["reconstruction_plate_spec"]
        core = spec["imagine_prompt"]
        figures_out.append(
            {
                "figure_id": fig["id"],
                "slug": fig["slug"],
                "name": fig["name"],
                "likeness_tier": fig["appearance_basis"]["likeness_tier"],
                "status": "SPEC_ONLY",
                "plate_type": spec["plate_type"],
                "canvas": spec["canvas"],
                "views": spec["views"],
                "age_at_depiction": spec["age_at_depiction"],
                "appearance_lock_verbatim": spec["appearance_lock_verbatim"],
                "costume_lock_verbatim": spec.get("costume_lock_verbatim"),
                "reference_anchors": spec["reference_anchors"],
                "imagine_prompt": core,
                "actors_turnaround_prompt": _actors_prompt(core),
                "prohibited": spec.get("prohibited", []),
                "delivery_filename": spec["delivery_filename"],
                "delivery_path": f"History/figures/{fig['slug']}/01_reconstruction_plates/reconstruction_turnaround_v1.jpg",
                "disclosure": DISCLOSURE,
            }
        )
    doc = {
        "issue": 198,
        "task": "T2 #198 — next-12 figure plate specs for ACTORS",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "disclosure": DISCLOSURE,
        "total": len(figures_out),
        "figures": figures_out,
    }
    ACTORS_SPECS.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return doc


def validate_next_12(registry: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if len(registry.get("figures", [])) != 12:
        errors.append(f"expected 12 figures, got {len(registry.get('figures', []))}")
    for fig in registry.get("figures", []):
        fid = fig.get("id", "?")
        spec = fig.get("reconstruction_plate_spec", {})
        if spec.get("status") != "SPEC_ONLY":
            errors.append(f"{fid}: status must be SPEC_ONLY")
        if len(spec.get("views", [])) < 3:
            errors.append(f"{fid}: requires 3 turnaround views")
        if not spec.get("appearance_lock_verbatim"):
            errors.append(f"{fid}: missing appearance_lock_verbatim")
        if not spec.get("imagine_prompt"):
            errors.append(f"{fid}: missing imagine_prompt")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="T2 #198 spec-only plate specs")
    parser.add_argument("--summary-only", action="store_true")
    args = parser.parse_args()

    creator = write_creator_specs()
    registry = write_next_12_registry()
    errors = validate_next_12(registry)
    if errors:
        for e in errors:
            print(f"FAIL: {e}")
        return 1
    actors = write_actors_specs(registry)

    summary = {
        "issue": 198,
        "task": "T2 #198 — spec work (no render)",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "creator_3_teardown": {
            "count": creator["total"],
            "path": str(CREATOR_SPECS),
            "slugs": [p["slug"] for p in creator["plates"]],
        },
        "next_12_figures": {
            "count": actors["total"],
            "registry": str(NEXT_12_REGISTRY),
            "actors_specs": str(ACTORS_SPECS),
            "slugs": [f["slug"] for f in actors["figures"]],
        },
    }
    SUMMARY_PATH.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())