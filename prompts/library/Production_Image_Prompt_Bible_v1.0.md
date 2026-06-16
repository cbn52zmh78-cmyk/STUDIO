# Production Image Prompt Bible v1.0

**Purpose:** VFX-ready image generation — setting plates, head composites, props, mattes, and supporting assets.

**Tooling:** `Studio/scripts/make_image_pack.py` + `studio/prompting/production_images.py`

**Default aspect ratio:** `16:9` for all asset types unless you specify otherwise.

**Casting stance (profile shots):** Standing upright, arms at their sides, hands free of any objects — applied to every casting/profile view automatically.

**Trigger:** When the user says **"casting shot"** + person description → generate the 3-view 16:9 turnaround **immediately** (see `.grok/skills/casting-shot/SKILL.md`).

**Wardrobe rule:** **Casting shots only** → high-waisted bikini (color from prompt). **All other images** → exact outfit requested; never default to high-waisted.

**Variation rule:** Always use the character's **canonical source image** for model lock (e.g. Mary → `CONCEPTS/MARY/01_casting_shots/mary_casting_turnaround_v2.jpg`). Reference it on every variation; change outfit only.

---

## Asset types

| Type | Use |
|------|-----|
| `setting_plate` | Empty environment for comp |
| `head_composite` | Face/head for body or scene comp |
| `costume_plate` | Wardrobe reference |
| `prop_plate` | Isolated object |
| `environment_establishing` | Full hero environment |
| `lighting_reference` | Match-back lighting only |
| `crowd_plate` | Background extras |
| `matte_extension` | Sky/horizon extension |
| `texture_surface` | Tileable material macro |
| `character_turnaround` | Full-body reference |
| `turnaround_sheet_3view` | Front + side + back on one 16:9 sheet |

---

## Workflow

1. **Plan** — List assets per shot (plate + head + prop).
2. **Pack** — `python Studio/scripts/make_image_pack.py --project Plantagenet --type setting_plate --subject "..."`.
3. **Generate** — Base image from prompt (`image_gen`).
4. **Iterate** — `image_edit` with reference for consistency across shots.
5. **Animate** — `image_to_video` from frame 1 when motion is needed.

---

## Rules

- **Casting / profile shots:** `turnaround_sheet_3view`, `character_turnaround`, `head_composite`, `costume_plate` — always staged standing upright, arms at sides, hands empty. Three views on one 16:9 sheet when profiles are needed.
- **Setting plates:** No people. Stable geometry. Match lens height to talent comp.
- **Head composites:** Neutral expression, even key/fill, plain background. Real people require a reference photo (`image_edit`).
- **Continuity:** Generate one hero base, then edit for variations — do not re-roll from scratch.
- **Named historical figures:** Search canon first; use reference-first workflow.

---

## Quick CLI

```bash
python Studio/scripts/make_image_pack.py \
  --project Plantagenet \
  --type setting_plate \
  --type head_composite \
  --subject "Plantagenet throne room, stone arches, winter daylight through high windows" \
  --era "12th century English royal court, photoreal historical drama" \
  --token "HENRY THE SECOND (@1)" \
  --lighting "soft window key, warm torch fill" \
  --camera "35mm eye-level, centered one-point perspective"
```

Output: `Studio/renders/prompt_packs/image_pack_*.json`