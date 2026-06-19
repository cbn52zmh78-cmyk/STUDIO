#!/usr/bin/env python3
"""Build Casting Bible, schema, registry, and per-actor lock cards from actors_roster."""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path

CAST_ROOT = Path(__file__).resolve().parents[1]
ROSTER_INDEX = CAST_ROOT / "actors_roster" / "roster_index.json"
TALENT_INDEX = CAST_ROOT / "Talent_Agency" / "roster_index.json"
PERF_ROOT = CAST_ROOT / "Talent_Agency" / "Performance_Studies"
OUT_ROOT = CAST_ROOT / "Casting_Bible"

# Celebrity-adjacent names / prompt patterns requiring review (synthetic-only guardrail)
CELEBRITY_NAME_FLAGS: dict[str, str] = {}

PROMPT_LIKENESS_PATTERNS = [
    r"\bcelebrity\b",
    r"\blook(?:s|ing)? like\b",
    r"\bresemblance\b",
    r"\bAttenborough\b",  # voice reference only in host, not roster
]

AGE_POLICY_MINIMUM = 21
AGE_PROMPT_PATTERN = re.compile(r"(\d{1,2})-year-old", re.IGNORECASE)

GENRE_BY_REGION: dict[str, list[str]] = {
    "europe_west": ["period_drama", "literary", "coastal", "prestige_tv"],
    "europe_east": ["thriller", "cold_war", "noir", "prestige_tv"],
    "north_america": ["indie_drama", "procedural", "rom_com", "prestige_tv"],
    "east_asia": ["tech_thriller", "family_drama", "anime_live_action_adjacent"],
    "southeast_asia": ["immigrant_story", "romance", "indie_drama"],
    "south_asia": ["family_saga", "romance", "mentor_drama"],
    "sub_saharan_africa": ["diaspora_drama", "prestige_tv", "romance"],
    "latin_america": ["telenovela_adjacent", "crime_drama", "romance"],
    "middle_east_north_africa": ["political_drama", "romance", "thriller"],
    "oceania_pacific": ["outdoor_drama", "indie", "rom_com"],
}


def slugify(stage_name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", stage_name.lower()).strip("_")


def first_name(stage_name: str) -> str:
    return stage_name.split()[0].replace("'", "").replace("-", "")


def load_performance(talent_id: str) -> dict | None:
    path = PERF_ROOT / talent_id / "performance_study.json"
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return None


def read_casting_prompt(actor_dir: Path) -> tuple[str | None, str]:
    prompt_path = actor_dir / "01_casting_shots" / "casting_prompt.txt"
    if prompt_path.exists():
        text = prompt_path.read_text(encoding="utf-8").strip()
        return text, "LOCKED"
    return None, "INCOMPLETE"


def read_voice_from_profile(actor_dir: Path) -> str | None:
    md = actor_dir / "actor_profile.md"
    if not md.exists():
        return None
    text = md.read_text(encoding="utf-8")
    m = re.search(r"## Voice Notes\s*\n(.+?)(?:\n##|\Z)", text, re.DOTALL)
    if m:
        return m.group(1).strip()
    return None


def extract_prompt_age(text: str | None) -> int | None:
    if not text:
        return None
    m = AGE_PROMPT_PATTERN.search(text)
    return int(m.group(1)) if m else None


def validate_age_compliance(locked_age: int, appearance_lock: str | None) -> list[str]:
    """Return blocking errors when age is missing, under 21, or mismatched vs roster."""
    errors: list[str] = []
    if locked_age < AGE_POLICY_MINIMUM:
        errors.append(f"age_locked:{locked_age} below minimum {AGE_POLICY_MINIMUM}")
    prompt_age = extract_prompt_age(appearance_lock)
    if prompt_age is None:
        errors.append("appearance_lock_missing_numerical_age")
    else:
        if prompt_age < AGE_POLICY_MINIMUM:
            errors.append(f"appearance_lock_age:{prompt_age} below minimum {AGE_POLICY_MINIMUM}")
        if prompt_age != locked_age:
            errors.append(f"appearance_lock_age_mismatch:prompt={prompt_age} locked={locked_age}")
    return errors


def scan_prompt_flags(text: str | None) -> list[str]:
    """Return compliance review flags (likeness risk), not routine AI-disclosure items."""
    flags: list[str] = []
    if not text:
        return flags
    lower = text.lower()
    for pat in PROMPT_LIKENESS_PATTERNS:
        if re.search(pat, lower):
            flags.append(f"prompt_pattern:{pat}")
    return flags


def assign_actor_ids(actors: list[dict]) -> dict[str, str]:
    """Map stage_name -> locked ID like David-001 pattern using FirstName-001."""
    first_counts: dict[str, int] = {}
    for a in actors:
        fn = first_name(a["stage_name"])
        first_counts[fn] = first_counts.get(fn, 0) + 1

    ids: dict[str, str] = {}
    used: set[str] = set()
    for a in sorted(actors, key=lambda x: x["stage_name"]):
        stage = a["stage_name"]
        fn = first_name(stage)
        if first_counts[fn] > 1:
            parts = stage.split()
            base = f"{fn}{parts[-1]}" if len(parts) > 1 else fn
        else:
            base = fn
        candidate = f"{base}-001"
        if candidate in used:
            candidate = f"{slugify(stage).title().replace('_', '')}-001"
        used.add(candidate)
        ids[stage] = candidate
    return ids


def build_voice_spec(perf: dict | None, profile_voice: str | None, gender: str) -> dict:
    notes = (perf or {}).get("voice_notes") or profile_voice or "TBD — assign in performance study."
    style = (perf or {}).get("performance_style", "")
    return {
        "register": "derived_from_notes",
        "notes": notes,
        "performance_style": style or None,
        "prompt_suffix": notes if notes != "TBD — assign in performance study." else None,
        "gender": gender,
    }


def relative_cast_path(full: Path) -> str:
    try:
        return str(full.relative_to(CAST_ROOT.parent)).replace("\\", "/")
    except ValueError:
        return str(full).replace("\\", "/")


def main() -> None:
    roster = json.loads(ROSTER_INDEX.read_text(encoding="utf-8"))
    talent = json.loads(TALENT_INDEX.read_text(encoding="utf-8"))
    talent_by_name: dict[str, dict] = {}
    for t in talent["talent"]:
        name = t["display_name"]
        existing = talent_by_name.get(name)
        if existing is None or (
            existing.get("roster_source") != "actors_roster"
            and t.get("roster_source") == "actors_roster"
        ):
            talent_by_name[name] = t
    # Fix Maeve display name mismatch
    talent_by_name["Maeve O'Sullivan"] = next(
        t for t in talent["talent"] if t["talent_id"] == "maeve_o_sullivan"
    )

    actors: list[dict] = []
    for gender in ("female", "male"):
        for entry in roster["by_gender"][gender]:
            actors.append({**entry, "gender": gender})

    id_map = assign_actor_ids(actors)
    generated_at = datetime.now(timezone.utc).isoformat()

    registry_entries: list[dict] = []
    disclosure_flags: list[dict] = []
    incomplete_locks: list[str] = []

    lock_cards_dir = OUT_ROOT / "lock_cards"
    lock_cards_dir.mkdir(parents=True, exist_ok=True)
    (OUT_ROOT / "schema").mkdir(parents=True, exist_ok=True)
    (OUT_ROOT / "registry").mkdir(parents=True, exist_ok=True)

    for entry in sorted(actors, key=lambda x: id_map[x["stage_name"]]):
        stage = entry["stage_name"]
        actor_id = id_map[stage]
        rel_path = entry["path"]
        actor_dir = CAST_ROOT / rel_path.replace("actors_roster/", "actors_roster/")
        if not actor_dir.exists():
            actor_dir = CAST_ROOT.parent / rel_path  # fallback

        talent_row = talent_by_name.get(stage)
        talent_id = talent_row["talent_id"] if talent_row else slugify(stage)
        perf = load_performance(talent_id)

        appearance_lock, lock_status = read_casting_prompt(actor_dir)
        age_errors = validate_age_compliance(entry["age"], appearance_lock)
        if age_errors:
            lock_status = "INCOMPLETE"
            incomplete_locks.append(actor_id)
        ref_jpg = actor_dir / "01_casting_shots" / "casting_turnaround_v1.jpg"
        ref_rel = (
            f"STUDIO/Cast/{rel_path}/01_casting_shots/casting_turnaround_v1.jpg"
            if ref_jpg.exists()
            else None
        )

        profile_voice = read_voice_from_profile(actor_dir)
        voice_spec = build_voice_spec(perf, profile_voice, entry["gender"])

        persona_tags = list(entry.get("mood_modifiers", []))
        if perf and perf.get("archetype_tags"):
            persona_tags = list(dict.fromkeys(persona_tags + perf["archetype_tags"]))

        genre_tags = list(GENRE_BY_REGION.get(entry["world_region"], ["narrative"]))
        if entry.get("roster_group") == "stunning_10":
            genre_tags.append("leading_role")
            genre_tags.append("editorial_ready")

        compliance_flags: list[str] = []
        for err in age_errors:
            compliance_flags.append(f"age_policy_block:{err}")
        if stage in CELEBRITY_NAME_FLAGS:
            compliance_flags.append(f"celebrity_name_review:{CELEBRITY_NAME_FLAGS[stage]}")
        compliance_flags.extend(scan_prompt_flags(appearance_lock))

        ai_disclosure = True  # all synthetic performers — separate from compliance_flags
        if compliance_flags:
            disclosure_flags.append(
                {"actor_id": actor_id, "stage_name": stage, "flags": compliance_flags}
            )

        agency_status = (perf or {}).get("agency_status", "unknown")
        has_casting_jpg = talent_row["has_casting_jpg"] if talent_row else ref_jpg.exists()

        record = {
            "actor_id": actor_id,
            "stage_name": stage,
            "talent_id": talent_id,
            "synthetic": True,
            "real_person_likeness": False,
            "content_rating": "SFW",
            "ai_disclosure_required": ai_disclosure,
            "ai_disclosure_note": "Synthetic performer — label in credits/description per Upon Tyne Productions policy.",
            "age_locked": entry["age"],
            "gender": entry["gender"],
            "ethnicity": entry["ethnicity"],
            "world_region": entry["world_region"],
            "roster_group": entry.get("roster_group"),
            "roster_source": "actors_roster",
            "roster_path": f"STUDIO/Cast/{rel_path}",
            "reference_image_primary": ref_rel,
            "reference_image_status": "plate_locked" if has_casting_jpg else "pending",
            "appearance_lock_verbatim": appearance_lock,
            "appearance_lock_status": lock_status,
            "voice_spec": voice_spec,
            "persona_tags": persona_tags,
            "genre_tags": sorted(set(genre_tags)),
            "agency_status": agency_status,
            "compliance_flags": compliance_flags,
            "profile_pdf": f"STUDIO/Cast/{rel_path}/actor_profile.pdf",
        }
        registry_entries.append(record)

        # Per-actor lock card
        card = f"""# {actor_id} — {stage}

**Status:** {'LOCKED' if lock_status == 'LOCKED' and has_casting_jpg else 'DEVELOPMENT'}  
**Content rating:** SFW  
**Synthetic:** Yes — no real-person likeness  
**AI disclosure required:** Yes

## Identity
| Field | Value |
|-------|-------|
| Actor ID | `{actor_id}` |
| Stage name | {stage} |
| Talent ID | `{talent_id}` |
| Age (locked) | **{entry['age']}** |
| Gender | {entry['gender']} |
| Ethnicity | {entry['ethnicity']} |
| Region | {entry['world_region']} |
| Roster group | {entry.get('roster_group') or '—'} |

## Reference
- **Primary plate:** `{ref_rel or 'PENDING — generate casting_turnaround_v1.jpg'}`
- **Roster path:** `STUDIO/Cast/{rel_path}`

## Appearance lock (verbatim — reuse every shot)
```
{appearance_lock or 'INCOMPLETE — populate 01_casting_shots/casting_prompt.txt'}
```

## Voice spec
```json
{json.dumps(voice_spec, indent=2)}
```

## Tags
- **Persona:** {', '.join(persona_tags)}
- **Genre:** {', '.join(sorted(set(genre_tags)))}

## Guardrails
- Synthetic-only; do not reference or generate real-person/celebrity likeness.
- Lead every generation prompt with exact age: `{entry['age']}-year-old`.
- SFW wardrobe baseline on casting plates; story wardrobe via `image_edit` from plate.
"""
        if compliance_flags:
            card += "\n## Compliance flags\n"
            for f in compliance_flags:
                card += f"- {f}\n"

        card += "\n---\n*STUDIO Casting Bible lock card — do not paraphrase appearance_lock_verbatim in production prompts.*\n"
        (lock_cards_dir / f"{actor_id}.md").write_text(card, encoding="utf-8")

    # Schema
    schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": "STUDIO Casting Registry Entry",
        "version": "1.0.0",
        "generated_at": generated_at,
        "description": "Locked synthetic actor record for STUDIO actors_roster. Appearance lock is verbatim reuse.",
        "guardrails": {
            "synthetic_only": True,
            "real_person_likeness": False,
            "content_rating_default": "SFW",
            "ai_disclosure_required_default": True,
            "appearance_lock_rule": "Copy appearance_lock_verbatim exactly into every image/video prompt; do not paraphrase.",
            "age_policy": f"Research/Age_Policy_Locked.md — numerical age required in all prompts; roster floor {AGE_POLICY_MINIMUM}+.",
        },
        "required": [
            "actor_id",
            "stage_name",
            "synthetic",
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
                "description": "Locked handle like David-001 (FirstName-001 or FirstLast-001 on collision).",
            },
            "stage_name": {"type": "string"},
            "talent_id": {"type": "string"},
            "synthetic": {"const": True},
            "real_person_likeness": {"const": False},
            "content_rating": {"enum": ["SFW"]},
            "ai_disclosure_required": {"type": "boolean"},
            "age_locked": {
                "type": "integer",
                "minimum": AGE_POLICY_MINIMUM,
                "description": "Roster floor 21+ per Age_Policy_Locked.md; must match appearance_lock_verbatim.",
            },
            "gender": {"enum": ["female", "male"]},
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

    registry = {
        "version": "1.0.0",
        "generated_at": generated_at,
        "scope": "actors_roster",
        "total": len(registry_entries),
        "summary": {
            "plate_locked": sum(1 for r in registry_entries if r["reference_image_status"] == "plate_locked"),
            "appearance_lock_locked": sum(1 for r in registry_entries if r["appearance_lock_status"] == "LOCKED"),
            "ai_disclosure_required": sum(1 for r in registry_entries if r["ai_disclosure_required"]),
            "compliance_review": len(disclosure_flags),
            "incomplete_appearance_locks": incomplete_locks,
        },
        "actors": registry_entries,
    }

    (OUT_ROOT / "schema" / "casting_schema.json").write_text(
        json.dumps(schema, indent=2), encoding="utf-8"
    )
    (OUT_ROOT / "registry" / "casting_registry.json").write_text(
        json.dumps(registry, indent=2), encoding="utf-8"
    )

    # Master Casting Bible MD
    bible_lines = [
        "# STUDIO Casting Bible v1.0",
        "",
        f"**Generated:** {generated_at}  ",
        "**Scope:** `STUDIO/Cast/actors_roster` — 70 synthetic narrative actors  ",
        "**Status:** Locked registry for production continuity",
        "",
        "---",
        "",
        "## Guardrails (non-negotiable)",
        "",
        "| Rule | Policy |",
        "|------|--------|",
        "| Synthetic only | No real-person or celebrity likeness in image, video, or voice |",
        "| Content rating | **SFW** default for all roster entries |",
        "| AI disclosure | **Required** on all shipped content featuring synthetic performers |",
        "| Appearance lock | Reuse `appearance_lock_verbatim` exactly — never paraphrase |",
        f"| Age | **{AGE_POLICY_MINIMUM}+** numerical age in every prompt per `Research/Age_Policy_Locked.md` |",
        "| Reference-first | `image_edit` from casting plate; do not re-roll face/body |",
        "",
        "## ID convention",
        "",
        "Locked handles follow `{Name}-001` (e.g. `David-001` for host). Roster actors use first name,",
        "with last-name suffix on first-name collision (`BridgetWalsh-001`, `BridgetOkafor-001`).",
        "",
        "## Registry summary",
        "",
        f"- **Total actors:** {registry['total']}",
        f"- **Plate locked:** {registry['summary']['plate_locked']}",
        f"- **Appearance lock complete:** {registry['summary']['appearance_lock_locked']}",
        f"- **AI disclosure required:** {registry['summary']['ai_disclosure_required']}",
        f"- **Compliance review items:** {registry['summary']['compliance_review']}",
        "",
        "## Files",
        "",
        "| Artifact | Path |",
        "|----------|------|",
        "| Schema | `STUDIO/Cast/Casting_Bible/schema/casting_schema.json` |",
        "| Registry | `STUDIO/Cast/Casting_Bible/registry/casting_registry.json` |",
        "| Lock cards | `STUDIO/Cast/Casting_Bible/lock_cards/{ActorID}.md` |",
        "",
        "## Actor index",
        "",
        "| Actor ID | Stage name | Age | Region | Plate | Lock | AI disclosure |",
        "|----------|------------|-----|--------|-------|------|---------------|",
    ]

    for r in sorted(registry_entries, key=lambda x: x["actor_id"]):
        plate = "✓" if r["reference_image_status"] == "plate_locked" else "—"
        lock = "✓" if r["appearance_lock_status"] == "LOCKED" else "—"
        disc = "✓" if r["ai_disclosure_required"] else "—"
        bible_lines.append(
            f"| `{r['actor_id']}` | {r['stage_name']} | {r['age_locked']} | {r['world_region']} | {plate} | {lock} | {disc} |"
        )

    bible_lines.extend([
        "",
        "## AI disclosure (all roster actors)",
        "",
        "Every entry has `ai_disclosure_required: true`. Label synthetic performers in credits,",
        "descriptions, and platform metadata per Upon Tyne Productions policy.",
        "",
    ])

    if disclosure_flags:
        bible_lines.extend(["## Compliance review queue", ""])
        for item in disclosure_flags:
            bible_lines.append(f"### `{item['actor_id']}` — {item['stage_name']}")
            for f in item["flags"]:
                bible_lines.append(f"- {f}")
            bible_lines.append("")

    if incomplete_locks:
        bible_lines.extend(["", "## Incomplete appearance locks", ""])
        for aid in incomplete_locks:
            bible_lines.append(f"- `{aid}`")

    bible_lines.extend([
        "",
        "---",
        "*Upon Tyne Productions / STUDIO — Casting Bible. Host identity `David-001` lives separately in `DAVID/productions/host_identity_v1/`.*",
    ])

    (OUT_ROOT / "Casting_Bible.md").write_text("\n".join(bible_lines), encoding="utf-8")

    age_compliant = sum(
        1
        for r in registry_entries
        if r["age_locked"] >= AGE_POLICY_MINIMUM
        and extract_prompt_age(r["appearance_lock_verbatim"]) == r["age_locked"]
        and r["appearance_lock_status"] == "LOCKED"
    )
    blocked_age = [r["actor_id"] for r in registry_entries if r["appearance_lock_status"] != "LOCKED"]

    print(f"Wrote Casting Bible: {len(registry_entries)} actors")
    print(f"  plate_locked: {registry['summary']['plate_locked']}")
    print(f"  appearance_lock_locked: {registry['summary']['appearance_lock_locked']}")
    print(f"  age_compliant_21plus: {age_compliant}/{len(registry_entries)}")
    print(f"  compliance_review: {registry['summary']['compliance_review']}")
    if blocked_age:
        print(f"  BLOCKED (age/lock): {', '.join(blocked_age)}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()