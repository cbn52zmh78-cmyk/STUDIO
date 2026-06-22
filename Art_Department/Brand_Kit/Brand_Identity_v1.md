# Brand Identity v1 — Upon Tyne Productions / DAVID · The Archive

**Task:** #141 — T3 Weekend Dispatch  
**Status:** LOCKED (design export pending)  
**Canonical source for DAVID specs:** `DAVID/brand/Upon_Tyne_DAVID_Brand_Kit_v1.md`  
**Date:** 2026-06-19

---

## 1. Entity Hierarchy

```
Upon Tyne Productions                    ← legal entity · IP owner · parent credit
    └── DAVID · The Archive              ← YouTube/social channel (documentary-host)
            └── Dead Languages Slate     ← launch content pillar (6 eps, Season 1)
            └── Lost Civilizations       ← content pillar (planned)
            └── Origin of Science        ← content pillar (planned)
```

| Entity | Public Name | Role | Appears On |
|--------|-------------|------|------------|
| **Parent** | Upon Tyne Productions | IP owner, production company | End-card footer, About, credits, contracts |
| **Channel** | DAVID · The Archive | Documentary host channel | Banner, avatar, lower-thirds, intros |
| **Host** | DAVID (`@David-001`) | Synthetic keeper of the Archive | On-camera; not a separate consumer brand |

**Rule:** Audience-facing video branding leads with **DAVID · The Archive**. Parent credit is always present but subordinate — footer line, About section, description tail, end-card.

---

## 2. Upon Tyne Productions

### Positioning
Independent AI-assisted cinematic production company. Synthetic performers, director-controlled output, legally gate-cleared. Every frame earns its shot list.

### Taglines (Director to select one)

| Option | Tone |
|--------|------|
| *Directed. Not generated.* | Asserts craft and authorial control — preferred candidate |
| *Cinema at the speed of thought.* | Positions speed as feature without sacrificing quality |
| *Frame by frame. Character by character.* | Emphasizes granular craft |

### Company Tagline (working): "Where History Speaks"
*Applied specifically to DAVID channel context. Pending Director lock.*

### Mission
Produce premium AI-assisted documentary content that makes history, language, and science accessible. Synthetic AI host (DAVID) + Grok-rendered visuals + human editorial oversight.

### Voice
Assured. Precise. Never apologetic about using AI, never over-explaining it. The craft sells itself.

### Production Credits Format
```
Directed by Benjamin Cartwright
Produced by Upon Tyne Productions
Visual production: STUDIO
```

---

## 3. DAVID · The Archive — Channel Identity

### Channel Badge (mandatory string)
```
DAVID · The Archive
```

### Locked Copy

| Use | Copy | Status |
|-----|------|--------|
| Channel title | DAVID · The Archive | LOCKED |
| Subtitle / tagline | Dead languages, actually pronounced. | LOCKED |
| CTA | Bring the dead tongues back — one attestation at a time. DAVID. | LOCKED |
| Signature beat | What did they actually say? … And how do we prove it? | LOCKED |
| Cold open | I am DAVID. I bring dead languages back — not as words on a page, but as sound you can hear. | LOCKED |
| AI disclosure (short) | Synthetic host · Educational demonstration · See description for attribution | LOCKED |
| Playlist | DAVID · Dead Languages | LOCKED |

### Channel Pitch
"The channel where dead languages aren't dead — and history talks back."

### Content Pillars
1. **Dead Languages** — Latin, Ancient Greek, Old English, Old Norse, Gothic, Sumerian (launch slate)
2. **Lost Civilizations** — Archaeology-led documentary (planned)
3. **Origin of Science** — History of scientific ideas and methods (planned)

### Target Audience
25–45, intellectually curious, documentary fans, language enthusiasts, humanities-educated.

---

## 4. Color System

### Upon Tyne Productions (Parent)

| Token | Hex | RGB | Use |
|-------|-----|-----|-----|
| `ut-black` | `#0D0D0D` | 13, 13, 13 | Letterpress wordmark, legal footer |
| `ut-warm-white` | `#F5F0E8` | 245, 240, 232 | Parent wordmark on dark backgrounds |
| `ut-gold` | `#C9A84C` | 201, 168, 76 | Parent accent, credit line |

### DAVID · The Archive (Channel / Primary UI)

| Token | Hex | RGB | Use |
|-------|-----|-----|-----|
| `archive-bg` | `#0C0E14` | 12, 14, 20 | Cards, overlays, end screens, channel background |
| `archive-title` | `#DCBE78` | 220, 190, 120 | Wordmark, titles, channel caption (amber gold) |
| `archive-border` | `#B4965A` | 180, 150, 90 | Frame strokes, closing card border |
| `archive-body` | `#C8CDD7` | 200, 205, 215 | Subtitles, body text on dark cards |
| `archive-cta` | `#FFB45A` | 255, 180, 90 | CTA buttons, footer links |
| `archive-wood-dark` | `#3D2B1F` | 61, 43, 31 | Set reference, banner mood fill |
| `archive-wood-mid` | `#5C4033` | 92, 64, 51 | Set accent |
| `archive-parchment` | `#F5F0E6` | 245, 240, 230 | Manuscript tone, light text on bars |
| `archive-shadow` | `#2A2520` | 42, 37, 32 | Shadow neutral |

**Palette note:** `ut-gold` (#C9A84C) and `archive-title` (#DCBE78) are intentional kinship — same warm-gravitas family, parent and channel reconciled. Do not substitute one for the other; each has its role.

### Honesty Labels (mandatory on pronunciation content)

| Label | RGBA | Hex | When |
|-------|------|-----|------|
| ATTESTED TEXT | 34, 110, 72, 230 | `#226E48` | Manuscript/inscription survives |
| RECONSTRUCTED PRONUNCIATION | 140, 88, 28, 230 | `#8C581C` | Inferred phonology |
| NOT ATTESTED | 160, 55, 30, 230 | `#A0371E` | Speculative line |

### Lighting Canon
Brass desk lamp **3200K** key. No magenta ambient. No teal shadows. Reference: `Set_Library_v1.json`.

---

## 5. Typography

| Role | Typeface | Fallback | Weight | Tracking |
|------|----------|----------|--------|----------|
| Parent wordmark | EB Garamond | Cormorant Garamond, Georgia | 500 | +2% |
| Channel wordmark | EB Garamond | same | 600 | DAVID +3%, · The Archive 0% |
| On-screen titles | EB Garamond | same | 600 | 0% |
| Lower-third body | Inter | DM Sans, Arial | 400 | 0% |
| IPA / transliteration | Charis SIL | Gentium Plus, Arial | 400 | 0% |
| Label chips | Inter | Arial | 600 | +4% all-caps |
| Legal footer | Inter | Arial | 400 | 0% |

**Font bundle target:** `DAVID/brand/fonts/` (EB Garamond, Inter, Charis SIL).  
**Pipeline note:** `render_longform.py` and `render_dead_language_proof.py` currently use Arial — swap to EB Garamond (titles) + Inter (body) when fonts are bundled.

---

## 6. Visual Language

### Aesthetic Pillars
- **Texture:** Impasto oil paint quality on all AI renders; aged parchment where appropriate
- **Lighting:** Dramatic Rembrandt-style side lighting, warm key (3200K brass lamp) / cool fill
- **Color grade:** Documentary prestige — warm amber key, pushed midtones, no magenta
- **Motion:** Slow dolly-push, zero jump-cuts, seamless transitions

### Logo Concepts

**Upon Tyne Productions (wordmark):**
```
UPON TYNE
PRODUCTIONS
```
Two lines, centered or left-aligned. Color on dark: `ut-warm-white` + `ut-gold` rule (1px, 60% width) between lines. Letterpress aesthetic. No icons, no gradients.

**DAVID · The Archive (channel wordmark):**
```
DAVID · The Archive
```
DAVID in EB Garamond 600, `archive-title`. Separator `·` at 50% title size, `archive-border`. "The Archive" in EB Garamond 400 italic, 72% of DAVID size. Single-line only for YouTube bug; stacked only on end cards.

---

## 7. AI Disclosure & Legal

### Short AI Disclosure (in-video)
> Synthetic host · Educational demonstration · See description for attribution

### Full AI Disclosure (YouTube description)
> AI-generated synthetic performers. No real persons depicted. This production is entirely synthetic — characters, voice, and visuals rendered by the STUDIO pipeline. Created by Upon Tyne Productions.

### 18 U.S.C. § 2257 Compliance Note
> 18 U.S.C. § 2257: All performers depicted in Upon Tyne Productions content are synthetic (AI-generated). No real persons are depicted. Upon Tyne Productions maintains documentation confirming the fully synthetic nature of all talent per the STUDIO Casting Bible and synthetic talent registry. Custodian of records: Upon Tyne Productions / STUDIO / Legal_Gate.

---

## 8. References

| Document | Path | Notes |
|----------|------|-------|
| Full DAVID brand kit | `DAVID/brand/Upon_Tyne_DAVID_Brand_Kit_v1.md` | Canonical — per-asset pixel specs live here |
| Machine-readable specs | `DAVID/brand/asset_specs.json` | Pipeline integration |
| Channel About copy | `DAVID/brand/CHANNEL_ABOUT.md` | Paste-ready YouTube copy |
| STUDIO branding | `STUDIO/BRANDING.md` | Company-level positioning |
| Identity lock | `DAVID/productions/host_identity_v1/david_identity_lock.json` | DAVID host anchors |
| Brand kit (this doc) | `STUDIO/Art_Department/Brand_Kit/Brand_Identity_v1.md` | STUDIO Art Department copy |

---

## 9. Version History

| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-06-19 | #141 — Initial brand identity doc for STUDIO Art Department |

*Upon Tyne Productions / DAVID · The Archive — corpus-first, legally gated, directed.*
