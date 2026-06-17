# STUDIO Master JSON Prompt Template — Changelog

## v2.2 — 2026-06-17

**From v2.1. One structural correction — @1 reference slot redefined.**

---

### 1. @1 Slot — Relabeled SETTING/ENVIRONMENT PLATE (hard correction)

**Previous (v2.1, incorrect):** @1 = "BODY / CLOTHING PHYSICS REFERENCE"  
**Corrected (v2.2):** @1 = SETTING/ENVIRONMENT PLATE

#### Why the correction:
In the Grok Imagine workflow, @1 is the currently open post — the page you generate from. It is the **base environment image**, not a clothing physics reference. The old label was a mislabeling that did not match the actual Grok @ reference system.

#### Canon §2 definition (restored):
- @1 IS the currently open post. In Grok Imagine: navigate to the setting plate post, then generate from that page. The open post IS @1.
- @1 is implicit — it does not need to be loaded. It is always the current page.
- **Describe @1 atmospherically:** energy, ambient behavior, light quality, spatial mood, sound design intent. Direct it like a character.
- Correct: `"(@1, pre-storm atmospheric pressure — the light has gone greenish and flat, the street unnaturally silent)"`
- Wrong: `"(@1, character in red dress, fabric drapes over shoulders)"` — appearance description, not atmospheric direction

#### Clothing/fabric physics — moved:
Clothing and fabric physics direction (drape, weight, movement behavior) moves to the `scene` field and `prose_prompt`. It is no longer a @1 concern.

#### Validation rail update:
- Removed: `@1_no_appearance_description`
- Added: `@1_is_setting_plate_direction_only`
- Check: @1 content must be atmospheric/environmental direction, not character appearance or clothing description

---

## v2.1 — 2026-06-17

See `CHANGELOG_v2.0_to_v2.1.md`

## v2.0 — 2026-06-17

Initial expanded template.
