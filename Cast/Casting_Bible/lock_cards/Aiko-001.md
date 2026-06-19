# Aiko-001 — Aiko Nakamura

**Status:** LOCKED  
**Content rating:** SFW  
**Synthetic:** Yes — no real-person likeness  
**AI disclosure required:** Yes

## Identity
| Field | Value |
|-------|-------|
| Actor ID | `Aiko-001` |
| Stage name | Aiko Nakamura |
| Talent ID | `aiko_nakamura` |
| Age (locked) | **26** |
| Gender | female |
| Ethnicity | Japanese-American |
| Region | east_asia |
| Roster group | — |

## Reference
- **Primary plate:** `STUDIO/Cast/actors_roster/female/east_asia/Aiko_Nakamura/01_casting_shots/casting_turnaround_v1.jpg`
- **Roster path:** `STUDIO/Cast/actors_roster/female/east_asia/Aiko_Nakamura`

## Appearance lock (verbatim — reuse every shot)
```
GENERATE 3D MODEL of back, side and front profiles of 26-year-old Japanese-American woman, 5'3", petite athletic build, straight jet-black bob, almond dark brown eyes, fair-to-light olive skin, wearing a fully covered high-waisted navy blue bikini top and matching navy blue bikini bottoms. Single 16:9 turnaround reference sheet on solid pure white background. LEFT panel: side profile. CENTER panel: front view. RIGHT panel: back view. FULL-LENGTH WIDE SHOT in every panel — camera pulled back, entire body head to toe with headroom and footroom, feet visible on the floor. NOT a close-up. NOT a medium close-up. NOT a medium shot. NOT a bust shot. NOT waist-up. NOT knee-up. NOT cropped. Fully covered high-waisted bikini top and matching bikini bottoms in all three views — fully clothed casting wardrobe, NOT topless, NOT nude, NOT implied nudity. Standing upright, arms at their sides, hands free of any objects. Same person, identical proportions, hairstyle, and wardrobe in all three panels. Even soft studio lighting, full-length body illumination. Hyper-realistic photoreal 3D character reference model. No text, no labels, no props. Synthetic fictional character only. No real person or celebrity likeness. Clearly adult with mature facial features and adult bone structure — unambiguously 21+ adult, not teen, not school-age.
```

## Voice spec
```json
{
  "register": "derived_from_notes",
  "notes": "Soft neutral tone; sharpens on technical jargon.",
  "performance_style": "Minimalist; impact in timing.",
  "prompt_suffix": "Soft neutral tone; sharpens on technical jargon.",
  "gender": "female"
}
```

## Tags
- **Persona:** precise, reserved, dry, Tech noir lead, Stoic partner, Precision fighter
- **Genre:** anime_live_action_adjacent, family_drama, tech_thriller

## Guardrails
- Synthetic-only; do not reference or generate real-person/celebrity likeness.
- Lead every generation prompt with exact age: `26-year-old`.
- SFW wardrobe baseline on casting plates; story wardrobe via `image_edit` from plate.

## Compliance flags
- prompt_pattern:\bcelebrity\b

---
*STUDIO Casting Bible lock card — do not paraphrase appearance_lock_verbatim in production prompts.*
