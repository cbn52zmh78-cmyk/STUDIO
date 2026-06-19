# STUDIO New-Production Intake Flow

**Document:** Pipeline/INTAKE_FLOW.md
**Owner:** Producer's Office
**Version:** 1.0
**Effective Date:** 2026-06-18
**Status:** Active
**Implements:** `Pipeline/production_intake.py`

The one path from a **concept** to a render-ready **canonical `script.json`** that
`DAVID/scripts/render_longform.py` consumes. It wires together the three locked
libraries the studio already maintains — no copy-paste prompt assembly by hand.

```
                ┌─────────── concept_selector ───────────┐
                │                                          ▼
  CONCEPT  ──►  ACTOR (Casting Bible)  +  FORMAT (#98)  +  SET / STYLE (#99)
   (.json)             │                      │                    │
                       └──────────────┬───────┴────────────────────┘
                                      ▼
                       build_longform_script()
                                      ▼
                    canonical render_longform script.json
                                      ▼
                 python DAVID/scripts/render_longform.py … --seamless
```

## The inputs it reads (never mutates)

| Role | Library | Notes |
|---|---|---|
| **Format** (#98) | `Pipeline/Production_Templates/Production_Templates_v1.json` | Beat structure, pacing, camera grammar, default set/style, identity anchor, voice suffix, QA rules, provenance card, shot blueprints. |
| **Set** (#99) | `Pipeline/Set_Library_v1.json` | `continuity_lock`, `lighting_lock`, `color_guard`, Kelvin, reference plate. |
| **Style** (#99) | `Pipeline/Style_Library_v1.json` | `continuity_lock`, `lighting_lock`, `color_guard`, `lens_motion`, `end_guard`. |
| **Actor** | `Cast/Casting_Bible/registry/casting_registry.json` | 70 locked synthetic actors; numerical age, appearance/voice spec, casting plate. |

These three libraries name this exact entry point in their own `usage` fields
("Select format via `concept_selector` … instantiate with
`production_templates.build_longform_script()`"). `production_intake.py` is that
implementation.

## Concept schema

Only `slug` is required; format defaults fill everything else.

```json
{
  "slug": "david_why_latin_60s",
  "title": "DAVID — Why Latin Never Really Died",
  "format_id": "documentary-host",
  "actor_id": "David-001",
  "set_id": "@Set-Archive-001",
  "style_id": "@Style-Documentary-Prestige-001",
  "target_seconds": 69,
  "tags": ["history", "language"],
  "brand": { "title": "...", "subtitle": "...", "cta": "..." },
  "seamless": { "...optional overrides..." },
  "beats": [
    { "id": "01_cold_open", "speech_text": "...", "on_screen": "..." }
  ]
}
```

- **`format_id`** — omit it and `concept_selector` keyword-matches the concept
  text/tags against each format (defaults to `documentary-host`).
- **`actor_id`** — a Casting Bible handle (`Aiko-001`) or the format's anchor
  (`@David-001`). The DAVID host anchor lives in an identity-lock JSON rather
  than the synthetic roster, so it resolves to `use_identity_lock` instead of a
  casting plate.
- **`set_id` / `style_id`** — omit to take the format's locked pairing.
- **`beats`** — one per shot, matched to the format's `shot_blueprints` by `id`
  (then by order). Writers supply only `speech_text` + overrides; the blueprint
  supplies duration / role / camera / action. Omit `beats` entirely to emit the
  blueprint placeholders for a copy pass.

## What it composes

Each shot's `video_prompt` is assembled in the locked order from
`Production_Templates_v1.json → compose_contract.video_prompt_order`:

```
{identity_continuity_lock} {set.continuity_lock} {style.continuity_lock}
{action} {set.lighting_lock} {style.lighting_lock}
{set.color_guard} {style.color_guard} {style.lens_motion}
Lip-synced, delivers: "{speech_text}" {voice_suffix}
{style.end_guard}
```

Non-speaking roles (`b_roll`, `silent_establishing`) drop the lip-sync clause.
The synthetic-talent guard is always present on the voice suffix, age is always
numerical on synthesized identity locks, and one set/style pair is held for the
whole scene.

## Usage

```bash
# From a concept file (default output: DAVID/scripts/longform_scripts/<slug>_script.json)
python STUDIO/Pipeline/production_intake.py STUDIO/Pipeline/Concepts/<name>.concept.json

# Explicit output path
python STUDIO/Pipeline/production_intake.py concept.json -o out_script.json

# Quick one-off from flags
python STUDIO/Pipeline/production_intake.py --slug my_short \
    --format narrative-short-film --actor Aiko-001 \
    --set "@Set-Warehouse-Industrial-001" --style "@Style-Noir-Dramatic-001"

# Print to stdout without writing
python STUDIO/Pipeline/production_intake.py concept.json --print
```

As a library:

```python
from production_intake import build_longform_script
script = build_longform_script(concept_dict)   # -> canonical script.json dict
```

## Validate before you spend API credits

`render_longform.py --script-only` normalizes the file and writes the imagine
pack **without any API calls** — the cheapest correctness check:

```bash
python DAVID/scripts/render_longform.py \
    DAVID/scripts/longform_scripts/<slug>_script.json --script-only
```

A clean exit and a written `<slug>_imagine_pack.json` mean the file is
render-ready. Then:

```bash
python DAVID/scripts/render_longform.py <script.json> --seamless --match-color --cut-on-motion
```

> On Windows consoles, set `PYTHONIOENCODING=utf-8` — the script emits em-dashes
> and `·` in its status lines.

## Concept templates

Ready-to-fill templates (one per format): `Concepts/templates/*.concept.template.json`  
Smoke-test all four: `python STUDIO/Pipeline/Concepts/templates/validate_templates.py`

## Worked example

`Concepts/david_why_latin_60s.concept.json` → 8-shot documentary-host script,
Archive set + Documentary-Prestige style + `@David-001`, 69s target, validated
with `--script-only` (exit 0).

## Version History

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-06-18 | Initial intake flow + `production_intake.py` (concept → actor + format #98 + set/style #99 → canonical `script.json`). |
