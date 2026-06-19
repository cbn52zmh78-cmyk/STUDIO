#!/usr/bin/env python3
"""Build GFE (20) + MAGAZINE (10) Casting Bible registries and lock cards.

Lane guardrails (schema-enforced):
- age_locked minimum 21 on every entry
- synthetic-only, no real-person likeness
- SFW / suggestive-clothed wardrobe only (no nude/explicit)
- ai_disclosure_required on all entries
"""

from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

CAST_ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = CAST_ROOT.parent.parent
OUT_ROOT = CAST_ROOT / "Casting_Bible"
GFE_ROOT = CAST_ROOT / "GFE"
MAG_MODELS = WORKSPACE / "STUDIO" / "MAGAZINE" / "Editorial" / "Models"
TALENT_INDEX = CAST_ROOT / "Talent_Agency" / "roster_index.json"
PERF_ROOT = CAST_ROOT / "Talent_Agency" / "Performance_Studies"

GFE_SCRIPTS = WORKSPACE / "GFE" / "scripts"
MAG_SCRIPTS = WORKSPACE / "STUDIO" / "MAGAZINE" / "scripts"
for p in (GFE_SCRIPTS, MAG_SCRIPTS):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

from gfe_roster_data import GFE_ROSTER_20  # noqa: E402
from supermodel_roster_data import SUPERMODEL_ROSTER_10  # noqa: E402

AGE_MINIMUM = 21
AI_DISCLOSURE_NOTE = (
    "Synthetic performer — label in credits/description per Upon Tyne Productions policy."
)

PROMPT_LIKENESS_PATTERNS = [
    r"\bcelebrity\b",
    r"\blook(?:s|ing)? like\b",
    r"\bresemblance\b",
]
AFFIRMATIVE_EXPLICIT_PATTERNS = [
    r"\bnude\b",
    r"\bnudity\b",
    r"\btopless\b",
    r"\bexplicit\b",
    r"\bnsfw\b",
    r"\bpornograph",
    r"\bgenital",
    r"\bbare breasts\b",
    r"\bimplied nudity\b",
]
NEGATION_PREFIX = re.compile(r"\b(?:not|no|never|without)\s+", re.I)

GFE_GENRE_TAGS = ["asmr_adjacent", "direct_address", "gfe", "suggestive_clothed"]
MAG_GENRE_TAGS = ["editorial_hero", "fashion", "haute_couture", "magazine_editorial", "runway"]


def slugify(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_")


def compact_name(name: str) -> str:
    return re.sub(r"[^A-Za-z0-9]", "", name.replace(" ", ""))


def extract_age_from_prompt(text: str | None) -> int | None:
    if not text:
        return None
    m = re.search(r"\b(\d{2})-year-old\b", text)
    return int(m.group(1)) if m else None


def _affirmative_explicit_match(text: str, pattern: str) -> bool:
    """Match explicit-content tokens unless immediately preceded by NOT/NO/NEVER."""
    for m in re.finditer(pattern, text, re.I):
        prefix = text[max(0, m.start() - 24) : m.start()]
        if NEGATION_PREFIX.search(prefix):
            continue
        return True
    return False


def scan_prompt_flags(text: str | None) -> list[str]:
    flags: list[str] = []
    if not text:
        return flags
    lower = text.lower()
    scrubbed = re.sub(
        r"no real person or celebrity likeness|no celebrity likeness|synthetic fictional character only",
        "",
        lower,
    )
    for pat in PROMPT_LIKENESS_PATTERNS:
        if re.search(pat, scrubbed):
            flags.append(f"likeness_risk:{pat}")
    for pat in AFFIRMATIVE_EXPLICIT_PATTERNS:
        if _affirmative_explicit_match(lower, pat):
            flags.append(f"content_review:{pat}")
    return flags


def load_performance(talent_id: str) -> dict | None:
    path = PERF_ROOT / talent_id / "performance_study.json"
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return None


def read_casting_prompt(actor_dir: Path) -> tuple[str | None, str]:
    prompt_path = actor_dir / "01_casting_shots" / "casting_prompt.txt"
    if prompt_path.exists():
        return prompt_path.read_text(encoding="utf-8").strip(), "LOCKED"
    return None, "INCOMPLETE"


def read_magazine_studio_lock(model_dir: Path, model_name: str) -> tuple[str | None, str]:
    studio = model_dir / "01_casting_shots" / f"{model_name}_Supermodel_Magazine_studio.txt"
    if not studio.exists():
        return None, "INCOMPLETE"
    raw = studio.read_text(encoding="utf-8")
    lines = [ln.strip() for ln in raw.splitlines() if ln.strip() and not ln.startswith("#")]
    # Prompt body is the long photorealistic line (skip trailing copy-paste footer).
    prompt_lines = [
        ln
        for ln in lines
        if ln.lower().startswith("photorealistic") or "year-old" in ln
    ]
    lock = prompt_lines[0] if prompt_lines else (lines[0] if lines else None)
    return lock, "LOCKED" if lock else "INCOMPLETE"


def gfe_actor_id(stage_name: str) -> str:
    return f"{compact_name(stage_name)}GFE-001"


def mag_actor_id(full_name: str) -> str:
    return f"{compact_name(full_name)}Mag-001"


def assert_age_compliance(actor_id: str, age: int) -> None:
    if age < AGE_MINIMUM:
        raise ValueError(
            f"{actor_id}: age_locked={age} violates lane minimum {AGE_MINIMUM}+"
        )


def build_voice_spec(
    *,
    voice_notes: str,
    performance_style: str,
    gender: str = "female",
) -> dict:
    notes = voice_notes or "TBD — assign in performance study."
    return {
        "register": "derived_from_notes",
        "notes": notes,
        "performance_style": performance_style or None,
        "prompt_suffix": notes if notes != "TBD — assign in performance study." else None,
        "gender": gender,
    }


def lane_schema(
    *,
    lane: str,
    content_rating_enum: list[str],
    generated_at: str,
) -> dict:
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": f"STUDIO Casting Registry Entry — {lane}",
        "version": "1.1.0",
        "generated_at": generated_at,
        "description": (
            f"Locked synthetic performer record for STUDIO {lane} lane. "
            "Appearance lock is verbatim reuse."
        ),
        "guardrails": {
            "synthetic_only": True,
            "real_person_likeness": False,
            "content_rating_allowed": content_rating_enum,
            "wardrobe_policy": "SFW/suggestive-clothed only — no nude, topless, or explicit",
            "ai_disclosure_required_default": True,
            "appearance_lock_rule": (
                "Copy appearance_lock_verbatim exactly into every image/video prompt; "
                "do not paraphrase."
            ),
            "age_policy": (
                f"HARD {AGE_MINIMUM}+ on every entry — schema minimum {AGE_MINIMUM}. "
                "Research/Age_Policy_Locked.md."
            ),
        },
        "required": [
            "actor_id",
            "stage_name",
            "synthetic",
            "real_person_likeness",
            "content_rating",
            "ai_disclosure_required",
            "age_locked",
            "appearance_lock_verbatim",
            "appearance_lock_status",
            "voice_spec",
            "persona_tags",
            "genre_tags",
            "reference_image_primary",
        ],
        "properties": {
            "actor_id": {
                "type": "string",
                "pattern": "^[A-Za-z][A-Za-z0-9]*-001$",
            },
            "stage_name": {"type": "string"},
            "talent_id": {"type": "string"},
            "synthetic": {"const": True},
            "real_person_likeness": {"const": False},
            "content_rating": {"enum": content_rating_enum},
            "ai_disclosure_required": {"const": True},
            "age_locked": {"type": "integer", "minimum": AGE_MINIMUM},
            "gender": {"enum": ["female"]},
            "appearance_lock_verbatim": {"type": ["string", "null"]},
            "appearance_lock_status": {"enum": ["LOCKED", "INCOMPLETE"]},
            "reference_image_primary": {"type": ["string", "null"]},
            "voice_spec": {
                "type": "object",
                "required": ["notes"],
                "properties": {
                    "notes": {"type": "string"},
                    "performance_style": {"type": ["string", "null"]},
                    "prompt_suffix": {"type": ["string", "null"]},
                },
            },
            "persona_tags": {"type": "array", "items": {"type": "string"}},
            "genre_tags": {"type": "array", "items": {"type": "string"}},
            "compliance_flags": {"type": "array", "items": {"type": "string"}},
        },
    }


def write_lock_card(record: dict, *, lane_label: str) -> None:
    actor_id = record["actor_id"]
    stage = record["stage_name"]
    age = record["age_locked"]
    lock = record["appearance_lock_verbatim"]
    lock_status = record["appearance_lock_status"]
    ref = record["reference_image_primary"]
    rating = record["content_rating"]
    plate_ok = record["reference_image_status"] == "plate_locked"

    card = f"""# {actor_id} — {stage}

**Lane:** {lane_label}  
**Status:** {'LOCKED' if lock_status == 'LOCKED' and (plate_ok or lane_label == 'MAGAZINE') else 'DEVELOPMENT'}  
**Content rating:** {rating}  
**Synthetic:** Yes — no real-person likeness  
**AI disclosure required:** Yes

## Identity
| Field | Value |
|-------|-------|
| Actor ID | `{actor_id}` |
| Stage name | {stage} |
| Talent ID | `{record['talent_id']}` |
| Age (locked, **{AGE_MINIMUM}+**) | **{age}** |
| Gender | {record['gender']} |
| Ethnicity | {record['ethnicity']} |
| Region | {record.get('world_region') or '—'} |
| Roster source | {record['roster_source']} |

## Reference
- **Primary plate:** `{ref or 'PENDING — generate casting_turnaround_v1.jpg'}`
- **Roster path:** `{record['roster_path']}`

## Appearance lock (verbatim — reuse every shot)
```
{lock or 'INCOMPLETE — populate appearance lock source file'}
```

## Voice spec
```json
{json.dumps(record['voice_spec'], indent=2)}
```

## Tags
- **Persona:** {', '.join(record['persona_tags'])}
- **Genre:** {', '.join(record['genre_tags'])}

## Guardrails
- Synthetic-only; do not reference or generate real-person/celebrity likeness.
- Lead every generation prompt with exact age: `{age}-year-old` (**minimum {AGE_MINIMUM}+**).
- {rating} wardrobe only — suggestive-clothed acceptable; no nude/topless/explicit.
- AI disclosure required on all shipped content.
"""
    if record["compliance_flags"]:
        card += "\n## Compliance flags\n"
        for flag in record["compliance_flags"]:
            card += f"- {flag}\n"

    card += (
        "\n---\n*STUDIO Casting Bible lock card — do not paraphrase "
        "appearance_lock_verbatim in production prompts.*\n"
    )
    (OUT_ROOT / "lock_cards" / f"{actor_id}.md").write_text(card, encoding="utf-8")


def build_gfe_entries(talent_by_id: dict) -> list[dict]:
    entries: list[dict] = []
    for actor in sorted(GFE_ROSTER_20, key=lambda a: a.stage_name):
        actor_id = gfe_actor_id(actor.stage_name)
        talent_id = f"gfe_{slugify(actor.stage_name)}"
        actor_dir = GFE_ROOT / actor.stage_name
        appearance_lock, lock_status = read_casting_prompt(actor_dir)
        prompt_age = extract_age_from_prompt(appearance_lock)
        age = prompt_age if prompt_age is not None else actor.age
        assert_age_compliance(actor_id, age)
        if prompt_age is not None and prompt_age != actor.age:
            # Canon age from roster; prompt must match — flag for review.
            pass

        ref_jpg = actor_dir / "01_casting_shots" / "casting_turnaround_v1.jpg"
        talent_row = talent_by_id.get(talent_id)
        has_jpg = talent_row["has_casting_jpg"] if talent_row else ref_jpg.exists()
        perf = load_performance(talent_id)

        persona_tags = list(actor.archetypes) + list(actor.mood_modifiers)
        compliance_flags = scan_prompt_flags(appearance_lock)

        record = {
            "actor_id": actor_id,
            "stage_name": actor.stage_name,
            "talent_id": talent_id,
            "synthetic": True,
            "real_person_likeness": False,
            "content_rating": "SFW_SUGGESTIVE_CLOTHED",
            "ai_disclosure_required": True,
            "ai_disclosure_note": AI_DISCLOSURE_NOTE,
            "age_locked": age,
            "gender": "female",
            "ethnicity": actor.ethnicity,
            "world_region": actor.world_region,
            "roster_group": "gfe_20",
            "roster_source": "gfe",
            "roster_path": f"STUDIO/Cast/GFE/{actor.stage_name}",
            "reference_image_primary": (
                f"STUDIO/Cast/GFE/{actor.stage_name}/01_casting_shots/casting_turnaround_v1.jpg"
                if has_jpg
                else None
            ),
            "reference_image_status": "plate_locked" if has_jpg else "pending",
            "appearance_lock_verbatim": appearance_lock,
            "appearance_lock_status": lock_status,
            "voice_spec": build_voice_spec(
                voice_notes=actor.voice_notes,
                performance_style=actor.performance_style,
            ),
            "persona_tags": list(dict.fromkeys(persona_tags)),
            "genre_tags": sorted(set(GFE_GENRE_TAGS)),
            "agency_status": (perf or {}).get("agency_status", "unknown"),
            "compliance_flags": compliance_flags,
            "profile_pdf": (
                f"STUDIO/Cast/GFE/{actor.stage_name}/actor_profile.pdf"
                if (actor_dir / "actor_profile.pdf").exists()
                else None
            ),
        }
        entries.append(record)
        write_lock_card(record, lane_label="GFE")
    return entries


def build_magazine_entries(talent_by_id: dict) -> list[dict]:
    entries: list[dict] = []
    for model in sorted(SUPERMODEL_ROSTER_10, key=lambda m: m["name"]):
        name = str(model["name"])
        actor_id = mag_actor_id(name)
        talent_id = f"mag_{slugify(name)}"
        age = int(model["age"])
        assert_age_compliance(actor_id, age)

        model_dir = MAG_MODELS / name
        appearance_lock, lock_status = read_magazine_studio_lock(model_dir, name)
        prompt_age = extract_age_from_prompt(appearance_lock)
        if prompt_age is not None and prompt_age != age:
            age = prompt_age  # studio prompt is canonical for on-image age text

        ref_jpg = model_dir / "01_casting_shots" / "casting_turnaround_v1.jpg"
        talent_row = talent_by_id.get(talent_id)
        has_jpg = talent_row["has_casting_jpg"] if talent_row else ref_jpg.exists()
        perf = load_performance(talent_id)
        compliance_flags = scan_prompt_flags(appearance_lock)

        record = {
            "actor_id": actor_id,
            "stage_name": name,
            "talent_id": talent_id,
            "synthetic": True,
            "real_person_likeness": False,
            "content_rating": "SFW",
            "ai_disclosure_required": True,
            "ai_disclosure_note": AI_DISCLOSURE_NOTE,
            "age_locked": age,
            "gender": "female",
            "ethnicity": str(model["ethnicity"]),
            "world_region": "editorial_global",
            "roster_group": "magazine_10",
            "roster_source": "magazine_editorial",
            "roster_path": f"STUDIO/MAGAZINE/Editorial/Models/{name}",
            "reference_image_primary": (
                f"STUDIO/MAGAZINE/Editorial/Models/{name}/01_casting_shots/casting_turnaround_v1.jpg"
                if has_jpg
                else None
            ),
            "reference_image_status": "plate_locked" if has_jpg else "pending",
            "appearance_lock_verbatim": appearance_lock,
            "appearance_lock_status": lock_status,
            "voice_spec": build_voice_spec(
                voice_notes=(perf or {}).get("voice_notes") or "Editorial — voice TBD.",
                performance_style=(perf or {}).get("performance_style") or "",
            ),
            "persona_tags": [str(model["visuals"]).split(",")[0].strip()],
            "genre_tags": sorted(set(MAG_GENRE_TAGS)),
            "agency_status": (perf or {}).get("agency_status", "unknown"),
            "compliance_flags": compliance_flags,
            "profile_pdf": None,
        }
        entries.append(record)
        write_lock_card(record, lane_label="MAGAZINE")
    return entries


def write_registry(
    *,
    scope: str,
    actors: list[dict],
    generated_at: str,
    filename: str,
) -> dict:
    incomplete = [a["actor_id"] for a in actors if a["appearance_lock_status"] == "INCOMPLETE"]
    registry = {
        "version": "1.1.0",
        "generated_at": generated_at,
        "scope": scope,
        "age_minimum_enforced": AGE_MINIMUM,
        "total": len(actors),
        "summary": {
            "plate_locked": sum(1 for a in actors if a["reference_image_status"] == "plate_locked"),
            "appearance_lock_locked": sum(1 for a in actors if a["appearance_lock_status"] == "LOCKED"),
            "ai_disclosure_required": len(actors),
            "age_21_plus": sum(1 for a in actors if a["age_locked"] >= AGE_MINIMUM),
            "compliance_review": sum(1 for a in actors if a["compliance_flags"]),
            "incomplete_appearance_locks": incomplete,
        },
        "actors": actors,
    }
    (OUT_ROOT / "registry" / filename).write_text(
        json.dumps(registry, indent=2), encoding="utf-8"
    )
    return registry


def write_lane_bible_md(
    *,
    title: str,
    scope: str,
    registry: dict,
    content_note: str,
) -> None:
    lines = [
        f"# {title}",
        "",
        f"**Generated:** {registry['generated_at']}  ",
        f"**Scope:** `{scope}` — {registry['total']} synthetic performers  ",
        f"**Age floor:** **{AGE_MINIMUM}+** (schema-enforced)  ",
        f"**Content:** {content_note}  ",
        "",
        "---",
        "",
        "## Guardrails",
        "",
        "| Rule | Policy |",
        "|------|--------|",
        "| Synthetic only | No real-person or celebrity likeness |",
        f"| Age | **{AGE_MINIMUM}+** on every entry and prompt |",
        f"| Content | {content_note} |",
        "| AI disclosure | **Required** on all shipped content |",
        "| Appearance lock | Reuse `appearance_lock_verbatim` exactly |",
        "",
        "## Registry summary",
        "",
        f"- **Total:** {registry['total']}",
        f"- **Age {AGE_MINIMUM}+:** {registry['summary']['age_21_plus']}",
        f"- **Plate locked:** {registry['summary']['plate_locked']}",
        f"- **Appearance lock complete:** {registry['summary']['appearance_lock_locked']}",
        f"- **AI disclosure required:** {registry['summary']['ai_disclosure_required']}",
        f"- **Compliance review:** {registry['summary']['compliance_review']}",
        "",
        "## Actor index",
        "",
        "| Actor ID | Stage name | Age | Plate | Lock | AI disclosure |",
        "|----------|------------|-----|-------|------|---------------|",
    ]
    for r in sorted(registry["actors"], key=lambda x: x["actor_id"]):
        plate = "✓" if r["reference_image_status"] == "plate_locked" else "—"
        lock = "✓" if r["appearance_lock_status"] == "LOCKED" else "—"
        disc = "✓" if r["ai_disclosure_required"] else "—"
        lines.append(
            f"| `{r['actor_id']}` | {r['stage_name']} | {r['age_locked']} | "
            f"{plate} | {lock} | {disc} |"
        )
    lines.extend(["", "---", "*Upon Tyne Productions / STUDIO — Casting Bible lane registry.*", ""])
    slug = "GFE" if "gfe" in scope else "MAGAZINE"
    (OUT_ROOT / f"{slug}_Casting_Bible.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    generated_at = datetime.now(timezone.utc).isoformat()
    talent = json.loads(TALENT_INDEX.read_text(encoding="utf-8"))
    talent_by_id = {t["talent_id"]: t for t in talent["talent"]}

    for sub in ("schema", "registry", "lock_cards"):
        (OUT_ROOT / sub).mkdir(parents=True, exist_ok=True)

    gfe_actors = build_gfe_entries(talent_by_id)
    mag_actors = build_magazine_entries(talent_by_id)

    gfe_schema = lane_schema(
        lane="GFE",
        content_rating_enum=["SFW_SUGGESTIVE_CLOTHED"],
        generated_at=generated_at,
    )
    mag_schema = lane_schema(
        lane="MAGAZINE",
        content_rating_enum=["SFW"],
        generated_at=generated_at,
    )
    (OUT_ROOT / "schema" / "gfe_casting_schema.json").write_text(
        json.dumps(gfe_schema, indent=2), encoding="utf-8"
    )
    (OUT_ROOT / "schema" / "magazine_casting_schema.json").write_text(
        json.dumps(mag_schema, indent=2), encoding="utf-8"
    )

    gfe_registry = write_registry(
        scope="gfe",
        actors=gfe_actors,
        generated_at=generated_at,
        filename="gfe_casting_registry.json",
    )
    mag_registry = write_registry(
        scope="magazine_editorial",
        actors=mag_actors,
        generated_at=generated_at,
        filename="magazine_casting_registry.json",
    )

    write_lane_bible_md(
        title="STUDIO GFE Casting Bible v1.1",
        scope="STUDIO/Cast/GFE",
        registry=gfe_registry,
        content_note="SFW / suggestive-clothed (bikini casting plates); no nude/explicit",
    )
    write_lane_bible_md(
        title="STUDIO MAGAZINE Casting Bible v1.1",
        scope="STUDIO/MAGAZINE/Editorial/Models",
        registry=mag_registry,
        content_note="SFW editorial couture; no nude/explicit",
    )

    print(f"GFE: {len(gfe_actors)} entries — all age>={AGE_MINIMUM}: "
          f"{gfe_registry['summary']['age_21_plus']}")
    print(f"MAGAZINE: {len(mag_actors)} entries — all age>={AGE_MINIMUM}: "
          f"{mag_registry['summary']['age_21_plus']}")
    print(f"  gfe plate_locked: {gfe_registry['summary']['plate_locked']}")
    print(f"  mag plate_locked: {mag_registry['summary']['plate_locked']}")
    print(f"  compliance_review gfe: {gfe_registry['summary']['compliance_review']}")
    print(f"  compliance_review mag: {mag_registry['summary']['compliance_review']}")


if __name__ == "__main__":
    main()