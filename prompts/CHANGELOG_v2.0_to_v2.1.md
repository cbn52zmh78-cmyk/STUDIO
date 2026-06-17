# STUDIO Master JSON Prompt Template — Changelog

## v2.1 — 2026-06-17

**From v2.0. Five rule additions/clarifications established in session today.**

---

### 1. Resolution Default — `output.resolution`
Added `"resolution": "480p"` as a named field in the `output` block. Previously absent/pending. 480p is the generation default; upscale in post if needed.

---

### 2. Character Behavioral Direction Rule (hard rule — most significant update)
**Added to `_DOC_scene` and Validation Rail.**

Characters/actors in the `scene` field and `prose_prompt`: write **behavioral direction only** — what they are doing, how they are moving, what their energy and intention are. **Do not describe appearance** (hair, skin, face, body). The editor has the 3D render reference; Grok has the casting reference.

Settings/environments: rich visual description **is** appropriate. Grok generates environments from scratch — give it everything.

New validation checks added:
- `character_behavioral_direction_only`
- `setting_description_present`

---

### 3. Concurrent Blocking Style Rule (hard rule)
**Added to `_DOC_scene` and `blocking._DOC_principles` and Validation Rail.**

Multi-character scenes: write spatial/concurrent movement — not sequential beats. The spatial relationship between bodies is the action. Everything simultaneous.

- Correct: *"She moves upstage through the corridor as he shifts into frame from the right, the gap between them closing, neither acknowledging the other."*
- Wrong: *"She walks forward, then he steps in, then she turns."*

No "and then" sequential character action chains. Existing `no_and_then_sequencing` check retained; new `multi_character_concurrent_not_sequential` check added to Validation Rail.

---

### 4. @1 / @2 Reference Clarification
**Updated `@1._DOC` and `@2._DOC` / `@2._DOC_rules`.**

- **@1** = body/clothing physics reference (fabric weight, drape, movement behavior). Clarified in `_DOC` header.
- **@2** = head/face reference. Now explicitly stated: always the **casting reference from History** — the image Grok uses to identify who the character is.
- **Backside follow shots**: use the back panel of the casting reference as @2. Grok reads the full image; the back panel provides the rear-view reference for character consistency from behind.

New validation check added: `@2_casting_reference_correct`.

---

### 5. 2257 Compliance — Prose Verification
**Already present in `compliance._DOC_age_rule` — confirmed and added to Validation Rail.**

Age + ethnicity + gender must appear **directly in prose text** for every character — not just in compliance metadata. Format: `[age] year old [ethnicity] [gender]` leads each character description in `prose_prompt`.

New validation check added: `compliance_2257_age_ethnicity_gender_in_prose`.

---

## v2.0 — 2026-06-17

Initial expanded template. Added blocking, pacing, beat context, and validation rail from Canon §1 base schema.
