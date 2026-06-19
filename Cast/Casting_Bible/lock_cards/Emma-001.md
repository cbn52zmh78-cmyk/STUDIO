# Emma-001 — Emma Larsen

**Status:** LOCKED  
**Content rating:** SFW  
**Synthetic:** Yes — no real-person likeness  
**AI disclosure required:** Yes

## Identity
| Field | Value |
|-------|-------|
| Actor ID | `Emma-001` |
| Stage name | Emma Larsen |
| Talent ID | `emma_larsen` |
| Age (locked) | **31** |
| Gender | female |
| Ethnicity | Norwegian |
| Region | europe_west |
| Roster group | — |

## Reference
- **Primary plate:** `STUDIO/Cast/actors_roster/female/europe_west/Emma_Larsen/01_casting_shots/casting_turnaround_v1.jpg`
- **Roster path:** `STUDIO/Cast/actors_roster/female/europe_west/Emma_Larsen`

## Appearance lock (verbatim — reuse every shot)
```
GENERATE 3D MODEL of back, side and front profiles of 31-year-old Norwegian woman, 5'9", strong swimmer's shoulders, strawberry-blonde braid, grey-blue eyes, light freckles, weather-ready fair skin, wearing a fully covered high-waisted slate grey bikini top and matching slate grey bikini bottoms. Single 16:9 turnaround reference sheet on solid pure white background. LEFT panel: side profile. CENTER panel: front view. RIGHT panel: back view. FULL-LENGTH WIDE SHOT in every panel — camera pulled back, entire body head to toe with headroom and footroom, feet visible on the floor. NOT a close-up. NOT a medium close-up. NOT a medium shot. NOT a bust shot. NOT waist-up. NOT knee-up. NOT cropped. Fully covered high-waisted bikini top and matching bikini bottoms in all three views — fully clothed casting wardrobe, NOT topless, NOT nude, NOT implied nudity. Standing upright, arms at their sides, hands free of any objects. Same person, identical proportions, hairstyle, and wardrobe in all three panels. Even soft studio lighting, full-length body illumination. Hyper-realistic photoreal 3D character reference model. No text, no labels, no props. Synthetic fictional character only. No real person or celebrity likeness. Clearly adult with mature facial features and adult bone structure — unambiguously 21+ adult, not teen, not school-age.
```

## Voice spec
```json
{
  "register": "derived_from_notes",
  "notes": "Direct cadence; laughs through nose.",
  "performance_style": "Physical truth; exhaustion reads real.",
  "prompt_suffix": "Direct cadence; laughs through nose.",
  "gender": "female"
}
```

## Tags
- **Persona:** wry, steady, blunt, Survival drama lead, Rescue-worker type, Quiet resilience
- **Genre:** coastal, literary, period_drama, prestige_tv

## Guardrails
- Synthetic-only; do not reference or generate real-person/celebrity likeness.
- Lead every generation prompt with exact age: `31-year-old`.
- SFW wardrobe baseline on casting plates; story wardrobe via `image_edit` from plate.

## Compliance flags
- prompt_pattern:\bcelebrity\b

---
*STUDIO Casting Bible lock card — do not paraphrase appearance_lock_verbatim in production prompts.*
