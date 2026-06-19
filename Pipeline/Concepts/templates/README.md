# Concept templates (#98 formats)

Copy a template, replace every `[BRACKET]` field, save as `STUDIO/Pipeline/Concepts/<slug>.concept.json`, then run the fill-and-run block for that format.

Validate all templates (CI / smoke): `python STUDIO/Pipeline/Concepts/templates/validate_templates.py`

| Format | Template | Default actor | Anchor mapping |
|--------|----------|---------------|----------------|
| documentary-host | `documentary-host.concept.template.json` | `David-001` (fixed) | `@David-001` — §4 exemption |
| narrative-short-film | `narrative-short-film.concept.template.json` | `[ActorID]` e.g. `Aiko-001` | `@Talent-001` → roster |
| conversational-companion | `conversational-companion.concept.template.json` | `[ActorID]` e.g. `Amara-001` | `@Companion-001` → roster |
| explainer-ad | `explainer-ad.concept.template.json` | `[ActorID]` e.g. `Julian-001` | `@Presenter-001` → roster |