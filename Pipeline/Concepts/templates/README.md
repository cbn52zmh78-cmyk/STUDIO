# Concept templates (#98 formats)

Copy a template, replace every `[BRACKET]` field, save as `STUDIO/Pipeline/Concepts/<slug>.concept.json`, then run the fill-and-run block for that format.

Validate all templates (CI / smoke): `python STUDIO/Pipeline/Concepts/templates/validate_templates.py`

## Template → Format ID Mapping

All 7 per-format templates. Each template file ships with `slug`, `title`, `format_id`, `tags`, `beats` (with `speech_text` placeholders), and a `gate_0` block (`rating`, `channels`, `music_bed_id`).

| format_id | Template file | Default actor | Anchor mapping | gate_0.rating | gate_0.channels |
|-----------|---------------|---------------|----------------|---------------|-----------------|
| `documentary-host` | `documentary-host.concept.template.json` | `David-001` (fixed) | `@David-001` — §4 exemption | PG | social, streaming |
| `historical-figure-documentary` | `historical-figure-documentary.concept.template.json` | `David-001` (fixed) | `@David-001` — §4 exemption | PG | social, streaming |
| `science-explainer` | `science-explainer.concept.template.json` | `Julian-001` (fixed) | `@Julian-001` | PG | social, streaming |
| `technical-explainer` | `technical-explainer.concept.template.json` | `Elijah-001` (fixed) | `@Elijah-001` | PG | social, streaming |
| `narrative-short-film` | `narrative-short-film.concept.template.json` | `[ActorID]` e.g. `Aiko-001` | `@Talent-001` → roster | PG-13 | social, streaming, festival |
| `conversational-companion` | `conversational-companion.concept.template.json` | `[ActorID]` e.g. `Amara-001` | `@Companion-001` → roster | PG | social, streaming |
| `explainer-ad` | `explainer-ad.concept.template.json` | `[ActorID]` e.g. `Julian-001` | `@Presenter-001` → roster | PG | social, client |

## Wiring to concept_selector

The `concept_selector.formats` block in `Production_Templates_v1.json` routes an untagged concept text to the correct `format_id` via keyword scoring. All 7 formats above have entries in `concept_selector.formats`. To force a format, set `format_id` explicitly in your concept JSON — the selector is a fallback only.

## Required fields per template

- `slug` — kebab-case production identifier
- `title` — human display title
- `format_id` — must match one of the 7 values above exactly
- `tags` — at least one tag
- `beats` — non-empty list; each beat must have `id` and `speech_text` (use `""` for b-roll silent beats)
- `gate_0.rating` — CARA target ceiling (G | PG | PG-13 | R)
- `gate_0.channels` — list of distribution channels (social | streaming | theatrical | festival | client)
- `gate_0.music_bed_id` — clearance manifest ID for the music bed

## Bible patch note

Templates wired to `concept_selector.formats` as part of Bible v1.0.1 patch (#128 — 2026-06-19).
Previously all 7 format entries existed in `Production_Templates_v1.json` but the per-format template
files (conversational-companion, documentary-host, explainer-ad, narrative-short-film) were missing
`gate_0` blocks. Fixed in this patch — all 7 templates now carry complete `gate_0` data.