# Theo-001 — Theo Nakamura

**Status:** LOCKED  
**Content rating:** SFW  
**Synthetic:** Yes — no real-person likeness  
**AI disclosure required:** Yes

## Identity
| Field | Value |
|-------|-------|
| Actor ID | `Theo-001` |
| Stage name | Theo Nakamura |
| Talent ID | `theo_nakamura` |
| Age (locked) | **25** |
| Gender | male |
| Ethnicity | Japanese-American |
| Region | east_asia |
| Roster group | — |

## Reference
- **Primary plate:** `STUDIO/Cast/actors_roster/male/east_asia/Theo_Nakamura/01_casting_shots/casting_turnaround_v1.jpg`
- **Roster path:** `STUDIO/Cast/actors_roster/male/east_asia/Theo_Nakamura`

## Appearance lock (verbatim — reuse every shot)
```
GENERATE 3D MODEL of back, side and front profiles of 25-year-old Japanese-American man, 5'9", skateboarder lean build, bleached-streak black hair, brown eyes, light olive skin, small ear hoop, wearing loose athletic gym shorts in white and a fitted white tank top (not speedo, not swim briefs, not tight swim trunks). Single 16:9 turnaround reference sheet on solid pure white background. LEFT panel: side profile. CENTER panel: front view. RIGHT panel: back view. FULL-LENGTH WIDE SHOT in every panel — camera pulled back, entire body head to toe with headroom and footroom, feet visible on the floor. NOT a close-up. NOT a medium close-up. NOT a medium shot. NOT a bust shot. NOT waist-up. NOT knee-up. NOT cropped. Loose athletic gym shorts and a fitted tank top in all three views — fully clothed casting wardrobe, NOT speedo, NOT swim briefs, NOT tight swim trunks, NOT topless, NOT nude, NOT implied nudity. Standing upright, arms at their sides, hands free of any objects. Same person, identical proportions, hairstyle, and wardrobe in all three panels. Even soft studio lighting, full-length body illumination. Hyper-realistic photoreal 3D character reference model. No text, no labels, no props.
```

## Voice spec
```json
{
  "register": "derived_from_notes",
  "notes": "LA casual; Japanese with grandparents.",
  "performance_style": "Loose body; comic timing in shrug.",
  "prompt_suffix": "LA casual; Japanese with grandparents.",
  "gender": "male"
}
```

## Tags
- **Persona:** cool, playful, sarcastic, Skater rom-com lead, Cool outsider, Unexpected funny
- **Genre:** anime_live_action_adjacent, family_drama, tech_thriller

## Guardrails
- Synthetic-only; do not reference or generate real-person/celebrity likeness.
- Lead every generation prompt with exact age: `25-year-old`.
- SFW wardrobe baseline on casting plates; story wardrobe via `image_edit` from plate.

---
*STUDIO Casting Bible lock card — do not paraphrase appearance_lock_verbatim in production prompts.*
