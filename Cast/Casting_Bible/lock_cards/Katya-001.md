# Katya-001 — Katya Morozova

**Status:** LOCKED  
**Content rating:** SFW  
**Synthetic:** Yes — no real-person likeness  
**AI disclosure required:** Yes

## Identity
| Field | Value |
|-------|-------|
| Actor ID | `Katya-001` |
| Stage name | Katya Morozova |
| Talent ID | `katya_morozova` |
| Age (locked) | **24** |
| Gender | female |
| Ethnicity | Ukrainian |
| Region | europe_east |
| Roster group | stunning_10 |

## Reference
- **Primary plate:** `STUDIO/Cast/actors_roster/female/europe_east/Katya_Morozova/01_casting_shots/casting_turnaround_v1.jpg`
- **Roster path:** `STUDIO/Cast/actors_roster/female/europe_east/Katya_Morozova`

## Appearance lock (verbatim — reuse every shot)
```
GENERATE 3D MODEL of back, side and front profiles of 24-year-old Ukrainian woman, 5'9", statuesque model proportions, ice-blue almond eyes, platinum-blonde straight hair to waist, angular cheekbones, pale luminous skin, striking arched brows, wearing a fully covered high-waisted ice blue bikini top and matching ice blue bikini bottoms. Single 16:9 turnaround reference sheet on solid pure white background. LEFT panel: side profile. CENTER panel: front view. RIGHT panel: back view. FULL-LENGTH WIDE SHOT in every panel — camera pulled back, entire body head to toe with headroom and footroom, feet visible on the floor. NOT a close-up. NOT a medium close-up. NOT a medium shot. NOT a bust shot. NOT waist-up. NOT knee-up. NOT cropped. Fully covered high-waisted bikini top and matching bikini bottoms in all three views — fully clothed casting wardrobe, NOT topless, NOT nude, NOT implied nudity. Standing upright, arms at their sides, hands free of any objects. Same person, identical proportions, hairstyle, and wardrobe in all three panels. Even soft studio lighting, full-length body illumination. Hyper-realistic photoreal 3D character reference model. No text, no labels, no props. Synthetic fictional character only. No real person or celebrity likeness. Clearly adult with mature facial features and adult bone structure — unambiguously 21+ adult, not teen, not school-age.
```

## Voice spec
```json
{
  "register": "derived_from_notes",
  "notes": "Cool low register; softens in intimate dialogue.",
  "performance_style": "Physical discipline; emotion lives in posture and breath.",
  "prompt_suffix": "Cool low register; softens in intimate dialogue.",
  "gender": "female"
}
```

## Tags
- **Persona:** glacial, defiant, sensual, Ice queen lead, Ballet-trained survivor, Cover-model turned actor
- **Genre:** cold_war, editorial_ready, leading_role, noir, prestige_tv, thriller

## Guardrails
- Synthetic-only; do not reference or generate real-person/celebrity likeness.
- Lead every generation prompt with exact age: `24-year-old`.
- SFW wardrobe baseline on casting plates; story wardrobe via `image_edit` from plate.

## Compliance flags
- prompt_pattern:\bcelebrity\b

---
*STUDIO Casting Bible lock card — do not paraphrase appearance_lock_verbatim in production prompts.*
