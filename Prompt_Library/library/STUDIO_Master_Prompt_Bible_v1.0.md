# STUDIO Master Prompt Bible v1.0

**Status:** LOCKED operator reference  
**Scope:** Full STUDIO image + long-form video pipeline — casting through seamless assembly  
**Supersedes:** `Production_Image_Prompt_Bible_v1.0.md` as the single entry point (that file remains for image-pack CLI detail)  
**Task ref:** Format templates #98 (4 locked production formats)  
**Generated:** 2026-06-19

---

## Master index

| § | Section | Use when |
|---|---------|----------|
| [0](#0-operator-quickstart) | Operator quickstart | Running the whole pipeline from one doc |
| [1](#1-casting-system-v21) | Casting System v2.1 | Locking talent, generating plates, variations |
| [2](#2-outfit-protocol) | Outfit protocol | Wardrobe changes via `image_edit` |
| [3](#3-compliance-rules) | Compliance rules | Age, synthetic-only, legal gate, AI disclosure |
| [4](#4-david-001-host-exemption) | **David-001 host exemption** | DAVID host — not roster casting rules |
| [5](#5-canonical-render_longform-schema) | Canonical `render_longform` schema | Writing or validating script JSON |
| [6](#6-seamless-continuity-protocol) | Seamless continuity protocol | Multi-segment host/talent takes |
| [7](#7-set-library-index) | Set Library index | Environment continuity locks |
| [8](#8-style-library-index) | Style Library index | Grade, lens, end-guard locks |
| [9](#9-production-format-templates-98) | Production format templates (#98) | 4 format blueprints → script JSON |
| [10](#10-video_prompt-compose-contract) | `video_prompt` compose contract | Assembling seamless-ready prompts |
| [11](#11-cli-reference) | CLI reference | Commands operators run |
| [12](#12-canonical-file-manifest) | Canonical file manifest | Paths to locked JSON/MD sources |

---

## 0. Operator quickstart

End-to-end pipeline — one pass, no doc-hopping:

```
1. LEGAL GATE          → GREEN before any generation (RED = hard stop)
2. CAST                → Pick ActorID from Casting Bible; verify plate + appearance_lock_verbatim
3. SET + STYLE         → Pick @Set-* and @Style-* (one each per scene; never swap mid-take)
4. FORMAT              → Pick format template (#98) or explicit format_id
5. SCRIPT              → Build canonical render_longform JSON (§5)
6. COMPOSE PROMPTS     → Apply compose contract (§10) to every shot video_prompt
7. GENERATE            → render_longform.py (add --seamless for continuous takes)
8. QA                  → qa_report.json + plate_locked registry check
```

**Image-only path (no video):**

```
Casting plate locked → image_edit from plate for outfit/scene changes (§1–§2)
Never re-roll face/body from scratch when a canonical plate exists.
```

**DAVID host path:** Skip roster casting (§4). Use `david_identity_lock.json` + `@Set-Archive-001` + `@Style-Documentary-Prestige-001` + `documentary-host` format.

---

## 1. Casting System v2.1

**OG neutral base + reference-first continuity for all roster talent.**

### 1.1 Principles

| Rule | Policy |
|------|--------|
| OG neutral base | Casting plates on **solid pure white** (not grey seamless) — body-first, age-led, full-length 3-view |
| Reference-first | `image_edit` from locked plate; **never** re-roll face/body |
| Appearance lock | Copy `appearance_lock_verbatim` exactly from registry — never paraphrase |
| Synthetic only | No real-person or celebrity likeness |
| AI disclosure | Required on all shipped content featuring synthetic performers |
| SFW default | Roster casting wardrobe is SFW baseline |

### 1.2 OG neutral base — casting plate spec

**Trigger:** `casting shot` + person description → generate immediately.

| Field | Value |
|-------|--------|
| Layout | Single 16:9 canvas — LEFT: side · CENTER: front · RIGHT: back |
| Background | Solid pure white |
| Framing | FULL-LENGTH WIDE SHOT every panel — head to toe, feet visible, camera pulled back |
| Stance | Standing upright, arms at sides, hands empty |
| Opener | `GENERATE 3D MODEL of back, side and front profiles of {AGE}-year-old {DESCRIPTION},` |

**Women (roster casting):** fully covered high-waisted bikini top + matching bottoms (color from prompt).  
**Men (roster casting):** loose athletic gym shorts + fitted tank top — **never** speedo / swim briefs / tight swim trunks.

**Non-casting 3-view:** use outfit exactly as specified; do **not** default to high-waisted.

### 1.3 Casting prompt tail (locked prose)

Append after person description:

```
Single 16:9 turnaround reference sheet on solid pure white background.
LEFT panel: side profile. CENTER panel: front view. RIGHT panel: back view.
FULL-LENGTH WIDE SHOT in every panel — camera pulled back, entire body head to toe
with headroom and footroom, feet visible on the floor.
NOT a close-up. NOT a medium close-up. NOT a medium shot. NOT a bust shot.
NOT waist-up. NOT knee-up. NOT cropped.
[WARDROBE LINE — bikini or gym shorts per gender]
Standing upright, arms at their sides, hands free of any objects.
Same person, identical proportions, hairstyle, and wardrobe in all three panels.
Even soft studio lighting, full-length body illumination.
Hyper-realistic photoreal 3D character reference model. No text, no labels, no props.
```

### 1.4 Registry integration

| Artifact | Path |
|----------|------|
| Registry (70 actors) | `STUDIO/Cast/Casting_Bible/registry/casting_registry.json` |
| Schema (blocks <21) | `STUDIO/Cast/Casting_Bible/schema/casting_schema.json` |
| Lock cards | `STUDIO/Cast/Casting_Bible/lock_cards/{ActorID}.md` |
| Plates | `STUDIO/Cast/actors_roster/.../01_casting_shots/casting_turnaround_v1.jpg` |
| Prompts | `.../01_casting_shots/casting_prompt.txt` |

**Build / validate registry:**

```powershell
python STUDIO/Cast/Scripts/build_casting_bible.py
```

Exits **1** if any entry lacks 21+ age in prompt, age mismatch, or incomplete appearance lock.

### 1.5 Variations (outfit / scene)

1. Load canonical plate (`casting_turnaround_v1.jpg` or designated v2 source).
2. `image_edit` with plate as reference — change **outfit/scene only**.
3. Lock face, body, hair, skin from source.
4. Keep 3-view · 16:9 · white background · stance unless user overrides.

### 1.6 Code source

Prompt builder: `STUDIO/Development/studio/prompting/production_images.py`  
CLI helper: `STUDIO/Development/scripts/casting_shot.py`

---

## 2. Outfit protocol

**From STUDIO Production Canon §3 — non-negotiable syntax for wardrobe changes.**

### 2.1 Exact change syntax

```
change her outfit to [garments + layers + footwear + accessories]
change his outfit to [garments + layers + footwear + accessories]
```

- Concise but complete: main garments, layers, footwear, key accessories.
- **Do not repeat** physical description — the reference image handles appearance.

| Wrong | Right |
|-------|-------|
| `winter clothes with a coat and scarf` (too vague) | `black turtleneck under long camel wool coat, dark grey straight-leg trousers, black leather knee-high boots, thick cream scarf, black beanie` |
| Re-stating age, ethnicity, face, lighting | Clothing items only |

### 2.2 Workflow

1. Start from locked casting plate or costume plate.
2. `image_edit` with `change her/his outfit to …` prompt.
3. Fabric physics belong in **scene** field for video (v2.2 JSON template), not in @1.

### 2.3 Clothing state rules

- Nudity cannot begin on frame 1 — extend from clothed generation.
- Same-color top+bottom can merge visually — specify layers explicitly.
- Removing clothing mid-sequence breaks continuity — bake intended end-state from frame 1 when possible.

---

## 3. Compliance rules

### 3.1 Age policy (roster floor: 21+)

| Rule | Requirement |
|------|-------------|
| Numerical age first | `{N}-year-old woman/man` at opening of every performer prompt |
| Roster floor | **21+** — schema-enforced in `casting_schema.json` |
| No vague youth | `young woman`, `teen`, `youthful` alone — **blocked** |
| Zero tolerance | Sexual/exploitative content involving minors — RED, do not generate |

Source: `STUDIO/research/Age_Policy_Locked.md`  
Enforcement: `build_casting_bible.py` + `content_rating_compliance_guard.py`

### 3.2 Synthetic performer policy

- All roster talent: `synthetic: true`, `real_person_likeness: false`
- Label synthetic performers in credits, descriptions, platform metadata
- No celebrity mimicry in image, video, or voice

### 3.3 Content rating defaults

| Context | Default |
|---------|---------|
| Roster casting plates | SFW |
| Narrative short film format | PG-13 |
| Conversational companion format | PG / SFW mandatory |
| Documentary host | PG |
| Explainer ad | PG |

### 3.4 Legal gate

**Legal Gate 0** runs before any generation. **RED = hard stop.** No generation, no shoot, no publish.

### 3.5 Intimacy language (when applicable)

Clinical/neutral only: bosom, waist, hips, lower back, shoulder, neck, thigh.  
Explicit genital contact — permanently forbidden.

---

## 4. David-001 host exemption

**`@David-001` is NOT a roster casting entry. Separate identity lock applies.**

| Roster rule | David-001 |
|-------------|-----------|
| 21+ casting floor + bikini/gym casting wardrobe | **Exempt** — host reads age 45–55; modern charcoal/navy wardrobe |
| `actors_roster` / `appearance_lock_verbatim` | **Exempt** — uses `david_identity_lock.json` |
| White OG casting 3-view plate | **Exempt** — `david_avatar_reference.jpg` chest-up host ref |
| Casting Bible registry | **Exempt** — lives in `DAVID/productions/host_identity_v1/` |
| Age policy | Host age stated as **reads 45–55** in identity lock — not roster 21+ floor |

### 4.1 David-001 locked assets

| Asset | Path | Slot |
|-------|------|------|
| Identity lock | `DAVID/productions/host_identity_v1/david_identity_lock.json` | config.identity_lock |
| Avatar reference | `DAVID/productions/host_identity_v1/references/david_avatar_reference.jpg` | @2 / image_url frame 1 |
| Archive set plate | `DAVID/productions/host_identity_v1/references/archive_set_reference.jpg` | @1 environment |
| Default set lock | `@Set-Archive-001` | continuity in video_prompt |
| Default style lock | `@Style-Documentary-Prestige-001` | grade + end guard |

### 4.2 David continuity prefix (embed in every host `video_prompt`)

```
CONTINUITY LOCK @David-001: identical host face, charcoal sweater, Archive desk,
warm gold brass desk lamp 3200K key light locked, reading glasses pushed up into hair,
same eye-line — seamless continuation of prior take, zero jump cut.
```

### 4.3 David voice suffix

```
mid-low resonant unhurried voice, precise diction, documentary gravitas,
Attenborough-calm, accessible never stuffy, synthetic host only
```

### 4.4 When to use exemption

- Any `documentary-host` format production
- Any shot with `@David-001` in `video_prompt`
- `render_longform.py` warm-gold clamp + magenta suppression targets David-001 reference — not roster talent

**All other talent** → full Casting System v2.1 + roster registry.

---

## 5. Canonical `render_longform` schema

**Only valid script shape for `DAVID/scripts/render_longform.py`.**  
Legacy fields accepted at load time via `normalize_script()` — persisted copies use canonical fields.

```json
{
  "slug": "production_slug",
  "title": "Human-readable title",
  "target_seconds": 69,
  "format_id": "documentary-host",
  "concept": "optional concept string",
  "config": {
    "model_video": "grok-imagine-video-1.5",
    "resolution": "720p",
    "aspect_ratio": "16:9",
    "identity_lock": "path/to/identity_lock.json",
    "avatar_reference": "path/to/avatar.jpg",
    "voice_suffix": "voice descriptor … synthetic only",
    "seamless": {
      "primary": "extend",
      "xfade_s": 0.2,
      "match_color": true,
      "cut_on_motion": true
    }
  },
  "shots": [
    {
      "id": "01_cold_open",
      "duration": 8,
      "t_start": 0,
      "t_end": 8,
      "role": "host",
      "video_prompt": "CONTINUITY LOCK … Lip-synced, delivers: \"…\" … Finish on gesture peak …",
      "speech_text": "Spoken line verbatim",
      "on_screen": "optional lower-third",
      "on_screen_labels": ["ATTESTED", "RECONSTRUCTED"]
    }
  ],
  "provenance_card": {
    "enabled": true,
    "duration_s": 6,
    "card_type": "closing",
    "title": "Brand title",
    "subtitle": "Tagline",
    "footer": "CTA"
  },
  "qa_rules": {
    "require_identity_lock": true,
    "require_synthetic_guard": true,
    "min_shots": 1
  },
  "guardrails": []
}
```

### 5.1 Required fields

| Path | Notes |
|------|-------|
| `slug` | Production folder: `productions/<slug>_longform_v1/` |
| `config` | Model, locks, refs, optional `seamless` |
| `shots[]` | Each: `id`, `duration`, `video_prompt`, `speech_text`, `t_start`, `t_end` |
| `provenance_card` | Closing/provenance still segment |
| `qa_rules` | Gates for `qa_report.json` |

### 5.2 Seamless config (`config.seamless`)

| Key | Default | Meaning |
|-----|---------|---------|
| `primary` | `"extend"` | Grok Imagine EXTEND within scene; frame-chain fallback |
| `xfade_s` | `0.2` | Video xfade + audio acrossfade at joins |
| `match_color` | `false` | Histogram match segment B to A before join |
| `cut_on_motion` | `false` | Trim ~0.15s tail stillness before join |

CLI flags override at runtime.

### 5.3 Per-shot prompt contract

Continuity prefix + end guard are **embedded in `video_prompt`** — not separate top-level fields.

**End guard (mandatory every segment):**

```
Finish on gesture peak (hand motion or lean), never hold dead stillness or dead frame.
```

**Duration discipline:** 5–15s per shot; prefer **7–9s** for seamless extend chains.

### 5.4 Deliverables per production

| Artifact | Path |
|----------|------|
| Final MP4 | `productions/<slug>_longform_v1/output/` |
| QA report | `qa_report.json` |
| Extend state | `shots/extend_state.json` |
| Manifest | `manifest.json` |

Source spec: `STUDIO/Techniques/STUDIO_Canonical_Schema_and_Seamless_Spec_v1.md`

---

## 6. Seamless continuity protocol

**Pairs with:** `render_longform.py --seamless`  
Source: `STUDIO/Techniques/STUDIO_Seamless_Continuity_Protocol_v1.1.md`

### 6.1 Priority stack

| Tier | Method | When |
|------|--------|------|
| **PRIMARY** | Grok Imagine **EXTEND** | Same scene / same take — host continues speaking |
| **JOINS** | Frame-chain + **0.2s xfade** + **acrossfade** | Scene change or non-video insert (closing card) |
| **Pre-join** | `--match-color` | Always before frame-chain join |
| **Hard cut** | `--cut-on-motion` only | Gesture peak — never on stillness |

### 6.2 Extend chain (PRIMARY)

```
Segment 1: video.generate(image_url=@avatar, duration=7–9s)
Segment 2..N: video.extend(video_url=prior.url, duration=7–9s)
```

**API note (2026-06):** `grok-imagine-video-1.5` may reject EXTEND via API. Pipeline auto-falls back to **frame-chain i2v** (last-frame → next start-image) with identical prompt contract. Finding recorded in `extend_state.json`.

### 6.3 Frame-chain join (scene change / card)

```
1. ffmpeg extract last frame of segment A → chain_frame.jpg
2. optional: --match-color segment B to A
3. video.generate(image_url=upload(chain_frame), prompt=segment B)
   OR xfade A + B if B is non-generated (PNG card)
4. xfade=0.2s + acrossfade=0.2s at join
```

### 6.4 CLI

```powershell
python DAVID/scripts/render_longform.py scripts/longform_scripts/<script>.json --seamless
python DAVID/scripts/render_longform.py <script.json> --seamless --match-color --cut-on-motion
python DAVID/scripts/render_longform.py <script.json> --seamless --concat-only
```

| Flag | Effect |
|------|--------|
| `--seamless` | Extend-primary; frame-chain + xfade for joins |
| `--match-color` | Histogram match before joins; David re-ground every 2 segments |
| `--cut-on-motion` | Trim tail stillness before joins |
| `--xfade SEC` | Crossfade duration (default **0.2**) |
| `--force-shot ID` | Regenerate one shot only |
| `--concat-only` | Reassemble cached shots — no API |

---

## 7. Set Library index

**Source:** `STUDIO/Pipeline/Set_Library_v1.json`  
**Usage:** Prepend `set.continuity_lock` to every `video_prompt`. One `set_id` per scene — never swap mid-take.

### 7.1 Global hue discipline

- Declare Kelvin on every key — do not say "warm" without a number.
- One dominant color temperature per scene; fill ≤15% intensity.
- Forbidden globally: magenta ambient, purple glass reflection, teal fill on tungsten sets, green skin shift.
- Re-ground lighting lock every **2 segments** in long-form assembly.

### 7.2 Set catalog

| ID | Name | Kelvin (key) | Default pairing |
|----|------|--------------|-----------------|
| `@Set-Archive-001` | The Archive | 3200K | DAVID host, documentary |
| `@Set-Studio-Interior-001` | Editorial Cyclorama | 5600K | Fashion editorial |
| `@Set-Modern-Apartment-001` | Modern Apartment | 5200K | Companion, lifestyle |
| `@Set-Outdoor-Golden-001` | Outdoor Golden Hour | 4000K | Location editorial |
| `@Set-Outdoor-Overcast-001` | Outdoor Overcast | 6000K | Naturalistic daylight |
| `@Set-Seamless-Neutral-001` | Neutral Seamless Grey | 5500K | Product, explainer ad |
| `@Set-Warehouse-Industrial-001` | Warehouse Loft | 4800K | Narrative, noir |
| `@Set-Rooftop-Urban-001` | Rooftop Dusk | 4300K | Cinematic exterior |

Each entry carries: `continuity_lock`, `lighting_lock`, `color_guard`, `kelvin`, `forbidden`, `reference_file`.

**Casting OG white base** ≠ `@Set-Seamless-Neutral-001` — casting uses pure white; seamless neutral grey is for **in-scene** product/explainer sets.

---

## 8. Style Library index

**Source:** `STUDIO/Pipeline/Style_Library_v1.json`  
**Usage:** After set lock, prepend `style.continuity_lock`. Append `style.lens_motion` + `style.end_guard`.

### 8.1 Global style discipline

- Style lock = grade intent; set lock = geometry + base Kelvin.
- If style Kelvin conflicts with set Kelvin, **set wins**.
- End guard mandatory on every generated segment.

### 8.2 Style catalog

| ID | Name | Best for |
|----|------|----------|
| `@Style-Documentary-Prestige-001` | Documentary Prestige | DAVID host, corpus-first |
| `@Style-Cinematic-001` | Cinematic | Narrative short film |
| `@Style-Soft-Warm-001` | Soft Warm | Companion, lifestyle |
| `@Style-High-Key-Fashion-001` | High-Key Fashion | Editorial, runway |
| `@Style-Cool-Clinical-001` | Cool Clinical | Product, explainer ad |
| `@Style-Noir-Dramatic-001` | Noir Dramatic | Low-key thriller |
| `@Style-Naturalistic-Daylight-001` | Naturalistic Daylight | Observational realism |
| `@Style-Intimate-Close-001` | Intimate Close | PG-13 editorial intimacy |

### 8.3 Recommended pairings

| Use case | Set | Style |
|----------|-----|-------|
| DAVID host | `@Set-Archive-001` | `@Style-Documentary-Prestige-001` |
| Fashion editorial hero | `@Set-Studio-Interior-001` | `@Style-High-Key-Fashion-001` |
| Lifestyle apartment | `@Set-Modern-Apartment-001` | `@Style-Soft-Warm-001` |
| Neutral product | `@Set-Seamless-Neutral-001` | `@Style-Cool-Clinical-001` |

---

## 9. Production format templates (#98)

**Source:** `STUDIO/Pipeline/Production_Templates/Production_Templates_v1.json`  
**Builder:** `artifacts/production/production_templates.py`

Four locked formats. Select via `concept_selector` or explicit `format_id`.

### 9.1 Format summary

| format_id | Name | Rating | Default seconds | Default set | Default style | Identity anchor |
|-----------|------|--------|-----------------|-------------|---------------|-----------------|
| `documentary-host` | Documentary Host | PG | 69 | `@Set-Archive-001` | `@Style-Documentary-Prestige-001` | `@David-001` |
| `narrative-short-film` | Narrative / Short Film | PG-13 | 60 | `@Set-Warehouse-Industrial-001` | `@Style-Cinematic-001` | `@Talent-001` |
| `conversational-companion` | Conversational / Companion (SFW) | PG | 40 | `@Set-Modern-Apartment-001` | `@Style-Soft-Warm-001` | `@Companion-001` |
| `explainer-ad` | Explainer / Ad | PG | 30 | `@Set-Seamless-Neutral-001` | `@Style-Cool-Clinical-001` | `@Presenter-001` |

### 9.2 `documentary-host` — shot blueprint

| Shot ID | Duration | Role | Beat |
|---------|----------|------|------|
| `01_cold_open` | 8s | host | Hook — name and promise |
| `02_stakes` | 8s | host | What was lost / unknown |
| `03_signature_question` | 8s | host | Signature question |
| `04_proof_beat` | 7s | host | How do we prove it |
| `05_method` | 8s | host | Corpus-first method |
| `06_honesty` | 8s | host | Attested vs reconstructed |
| `07_demonstration` | 10s | host | Example pronunciation |
| `08_invitation` | 8s | host | CTA / welcome |

Uses David-001 exemption (§4). `min_shots: 6`. Provenance card enabled.

### 9.3 `narrative-short-film` — shot blueprint

| Shot ID | Duration | Role | Beat |
|---------|----------|------|------|
| `01_establishing` | 6s | b_roll | World |
| `02_character_intro` | 8s | character | Want / wound |
| `03_inciting` | 8s | character | Disruption |
| `04_rising` | 8s | character | Rising tension |
| `05_turn` | 8s | character | Reversal |
| `06_peak` | 8s | character | Emotional peak |
| `07_resolution` | 7s | character | Button |

Talent from roster casting (§1). `min_shots: 5`.

### 9.4 `conversational-companion` — shot blueprint

| Shot ID | Duration | Role | Beat |
|---------|----------|------|------|
| `01_greeting` | 6s | companion | Warm hello |
| `02_check_in` | 7s | companion | Acknowledge viewer |
| `03_core_message` | 8s | companion | Main point |
| `04_reflective_pause` | 6s | companion | Pause beat |
| `05_encouragement` | 7s | companion | Affirm viewer |
| `06_soft_close` | 6s | companion | Sign-off |

SFW mandatory. No lingerie/bedroom staging. Provenance card disabled.

### 9.5 `explainer-ad` — shot blueprint

| Shot ID | Duration | Role | Beat |
|---------|----------|------|------|
| `01_hook` | 5s | presenter | Pattern interrupt |
| `02_pain` | 5s | presenter | Pain point |
| `03_solution` | 6s | presenter | Solution reveal |
| `04_benefit_a` | 5s | presenter | Benefit 1 |
| `05_benefit_b` | 5s | presenter | Benefit 2 |
| `06_cta` | 5s | presenter | Single clear CTA |

Claims require verification flag until legal approves.

### 9.6 Instantiate a script

```powershell
python artifacts/production/production_templates.py list
python artifacts/production/production_templates.py select "warm daily check-in companion"
python artifacts/production/production_templates.py build documentary-host --slug my_intro --out DAVID/scripts/longform_scripts/my_intro.json
```

---

## 10. `video_prompt` compose contract

**Locked order** — from `Production_Templates_v1.json` `compose_contract`:

```
{identity_continuity_lock}
{set.continuity_lock}
{style.continuity_lock}
{action_prompt}
{set.lighting_lock}
{style.lighting_lock}
{set.color_guard}
{style.color_guard}
{style.lens_motion}
Lip-synced, delivers: "{speech_text}"    ← speaking roles only
{voice_suffix}
{style.end_guard}
```

**Speaking roles:** `host`, `character`, `companion`, `presenter`, `host_pie`  
**Silent roles:** omit lip-sync clause (`b_roll`, `silent_establishing`)

**Synthetic guard:** append `synthetic host only` / `synthetic talent only` if not already in voice_suffix.

**Implementation:** `compose_video_prompt()` in `artifacts/production/production_templates.py`

### 10.1 JSON video template (single-shot Grok payload)

For non-longform single clips, use `STUDIO/prompts/MASTER_JSON_Prompt_Template_ACTIVE.json` (v2.2):

| Slot | Role |
|------|------|
| `@1` | Setting / environment plate |
| `@2` | Head / casting reference — `"see attached render"` only |
| `scene` | Stage direction + fabric physics + behavioral direction |
| `camera` | Shot size + movement (never physical distance in meters) |

**v2.2 correction:** @1 is environment, not body reference. Clothing physics live in `scene`.

---

## 11. CLI reference

| Task | Command |
|------|---------|
| Build casting registry | `python STUDIO/Cast/Scripts/build_casting_bible.py` |
| Casting prompt helper | `python STUDIO/Development/scripts/casting_shot.py <description>` |
| List formats | `python artifacts/production/production_templates.py list` |
| Build longform script | `python artifacts/production/production_templates.py build <format_id> --slug X --out script.json` |
| Render longform | `python DAVID/scripts/render_longform.py <script.json>` |
| Seamless render | `python DAVID/scripts/render_longform.py <script.json> --seamless --match-color --cut-on-motion` |
| Re-concat only | `python DAVID/scripts/render_longform.py <script.json> --concat-only` |
| Image pack | `python STUDIO/Development/scripts/make_image_pack.py --project X --type setting_plate --subject "..."` |

---

## 12. Canonical file manifest

| Document / data | Path |
|-----------------|------|
| **This bible** | `STUDIO/Prompt_Library/library/STUDIO_Master_Prompt_Bible_v1.0.md` |
| Casting registry | `STUDIO/Cast/Casting_Bible/registry/casting_registry.json` |
| Casting schema | `STUDIO/Cast/Casting_Bible/schema/casting_schema.json` |
| Age policy | `STUDIO/research/Age_Policy_Locked.md` |
| Production canon | `STUDIO/STUDIO_Production_Canon_v1.0.md` |
| JSON prompt template (active) | `STUDIO/prompts/MASTER_JSON_Prompt_Template_ACTIVE.json` |
| Set Library | `STUDIO/Pipeline/Set_Library_v1.json` |
| Style Library | `STUDIO/Pipeline/Style_Library_v1.json` |
| Format templates (#98) | `STUDIO/Pipeline/Production_Templates/Production_Templates_v1.json` |
| Canonical schema spec | `STUDIO/Techniques/STUDIO_Canonical_Schema_and_Seamless_Spec_v1.md` |
| Seamless protocol | `STUDIO/Techniques/STUDIO_Seamless_Continuity_Protocol_v1.1.md` |
| Long-form assembly | `STUDIO/Techniques/STUDIO_LongForm_Video_Assembly_v1.md` |
| Render pipeline | `DAVID/scripts/render_longform.py` |
| David identity lock | `DAVID/productions/host_identity_v1/david_identity_lock.json` |
| Template builder | `artifacts/production/production_templates.py` |
| Image prompt code | `STUDIO/Development/studio/prompting/production_images.py` |

---

## Version history

| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-06-19 | Master fold: Casting v2.1 + outfit + compliance + David-001 exemption + render_longform schema + seamless + Set/Style libraries + 4 format templates (#98) |

---

*Upon Tyne Productions / STUDIO — single operator reference. When in doubt: Legal Gate → Casting plate → Set/Style lock → Format template → Canonical script → Seamless render → QA.*