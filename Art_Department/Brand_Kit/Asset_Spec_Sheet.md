# Asset Spec Sheet — DAVID · The Archive

**Task:** #141  
**Purpose:** Production reference — dimensions, format, prompt source, and render status for all brand assets  
**Prompt source:** `STUDIO/Art_Department/Brand_Kit/Grok_Imagine_Prompts.md`  
**Full pixel specs:** `DAVID/brand/Upon_Tyne_DAVID_Brand_Kit_v1.md` §5  
**Date:** 2026-06-19

---

## Asset Table

| Asset | Dimensions | Format | Prompt Section | Output Path | Status |
|-------|-----------|--------|----------------|-------------|--------|
| Channel banner | 2560 × 1440 | JPG (sRGB, ≤6 MB) | Asset 1 — Channel Banner | `DAVID/brand/export/youtube_banner_2560x1440.jpg` | PROMPT_READY |
| Channel logo icon | 512 × 512 | PNG (concept for SVG redraw) | Asset 2 — Channel Logo Icon | `DAVID/brand/export/david_monogram_avatar_800.png` | PROMPT_READY |
| Lower-third template | 1920 × 1080 | PNG (RGBA transparent) | Asset 3 — Lower-Third Graphic | `DAVID/brand/templates/lower_third_master_1920x1080.png` | PROMPT_READY |
| End card | 1920 × 1080 | JPG (+ optional 5s MP4) | Asset 4 — End Card | `DAVID/brand/templates/end_card_closing_1920x1080.png` | PROMPT_READY |
| Intro sting keyframe | 1920 × 1080 | JPG (single frame ref) | Asset 5 — Intro Sting Keyframe | `DAVID/brand/export/intro_sting_keyframe.jpg` | PROMPT_READY |
| Social profile image | 1000 × 1000 | PNG (square, no bleed) | Asset 6 — Social Media Profile | `DAVID/brand/export/channel_avatar_800.png` | PROMPT_READY |

---

## Extended Specs

### Channel Banner (2560 × 1440)
- **Safe zone (TV):** Center 1546 × 423 px — all critical type/logos inside
- **Safe zone (mobile):** Center 640 × 360 px — wordmark minimum
- **Post-composite:** DAVID · The Archive wordmark (EB Garamond 600, `#DCBE78`) center-right; tagline "Dead languages, actually pronounced." (Inter 400, `#C8CDD7`) below wordmark; "Upon Tyne Productions" credit (Inter 400, `#C9A84C`, 11px) bottom-right inside safe zone
- **Source ref:** Archive set at `DAVID/productions/host_identity_v1/references/archive_set_reference.jpg`

### Channel Logo Icon (512 × 512)
- **Use:** YouTube avatar, social profile picture, favicon concept
- **Deliverable chain:** Grok render → designer SVG trace → `david_archive_wordmark.svg` + `david_monogram_avatar_800.png`
- **Display size:** renders at 98 × 98 px on YouTube; must read at that size

### Lower-Third Template (1920 × 1080)
- **Pipeline note:** Actual lower-thirds rendered by `render_dead_language_proof.py` → `render_shot_overlay_png()` — this Grok render is art direction reference only
- **Channel bug:** `DAVID · The Archive` — EB Garamond small, `archive-title` on `(18,20,28,210)` plate, top-bar at 16px margin
- **Lower-third bar:** Bottom, height 72px (110px if IPA line present), `(0,0,0,185)` gradient
- **Honesty labels:** Rounded rect r=6, 10px padding — see `Brand_Identity_v1.md` §4 for colors

### End Card (1920 × 1080)
- **Background:** `archive-bg` `#0C0E14`
- **Frame:** Rect inset 40px, 3px stroke `archive-border` `#B4965A`
- **Post-composite:** DAVID · The Archive wordmark (EB Garamond 56px, `#DCBE78`) center; episode subtitle (Inter 24px, `#C8CDD7`); CTA footer (Inter 20px, `#FFB45A`); Upon Tyne Productions parent line (Inter 14px, `#C8CDD7` 70% opacity) bottom 40px
- **Duration (if animated):** 4–6 s

### Intro Sting Keyframe (1920 × 1080)
- **Context:** Single peak frame from the 4-second animated sting (camera move through stone archway)
- **Full sting:** Edit from `DAVID/productions/david_intro_60s_v4_longform_v1/output/` OR `host_identity_v1/output/david_host_test_signature_beat_v1.mp4`
- **Export target for finished sting:** `DAVID/brand/export/intro_sting_4s_1080p.mp4` (H.264, yuv420p)

### Social Profile Image (1000 × 1000)
- **Variant shown:** Logo mark on dark field (no host face)
- **Alternate variant:** Host avatar crop — chest-up from `david_avatar_reference.jpg`, eyes upper-third, soft Archive bokeh or solid `archive-bg`, optional 2px `archive-border` ring

---

## Designer Export Checklist

| Deliverable | Format | Path | Status |
|-------------|--------|------|--------|
| `upon_tyne_wordmark_dark.svg` | SVG | `DAVID/brand/export/` | ⬜ design export |
| `upon_tyne_wordmark_light.svg` | SVG | `DAVID/brand/export/` | ⬜ design export |
| `upon_tyne_wordmark_dark_2x.png` | PNG | `DAVID/brand/export/` | ⬜ design export |
| `david_archive_wordmark.svg` | SVG | `DAVID/brand/export/` | ⬜ design export |
| `david_archive_wordmark_1x.png` | PNG 1280w transparent | `DAVID/brand/export/` | ⬜ design export |
| Font bundle (EB Garamond, Inter, Charis SIL) | OTF/TTF | `DAVID/brand/fonts/` | ⬜ license + bundle |

---

## Render Queue Status Key

| Status | Meaning |
|--------|---------|
| `PROMPT_READY` | Grok prompt written; ready to paste into terminal |
| `RENDER_DONE` | Grok render complete; raw file saved |
| `COMPOSITE_DONE` | Text/badges composited; final file exported |
| `APPROVED` | Director-approved; locked for use |
| `⬜ design export` | Requires designer pass (SVG / vector work) |

---

*Upon Tyne Productions / DAVID · The Archive — T3 #141*
