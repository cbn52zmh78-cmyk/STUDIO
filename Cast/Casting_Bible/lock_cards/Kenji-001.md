# Kenji-001 — Kenji Sato

**Status:** LOCKED  
**Content rating:** SFW  
**Synthetic:** Yes — no real-person likeness  
**AI disclosure required:** Yes

## Identity
| Field | Value |
|-------|-------|
| Actor ID | `Kenji-001` |
| Stage name | Kenji Sato |
| Talent ID | `kenji_sato` |
| Age (locked) | **34** |
| Gender | male |
| Ethnicity | Japanese |
| Region | east_asia |
| Roster group | — |

## Reference
- **Primary plate:** `STUDIO/Cast/actors_roster/male/east_asia/Kenji_Sato/01_casting_shots/casting_turnaround_v1.jpg`
- **Roster path:** `STUDIO/Cast/actors_roster/male/east_asia/Kenji_Sato`

## Appearance lock (verbatim — reuse every shot)
```
GENERATE 3D MODEL of back, side and front profiles of 34-year-old Japanese man, 5'10", lean martial-arts build, black hair medium length swept back, dark brown eyes, fair skin, calm face, wearing loose athletic gym shorts in black and a fitted black tank top (not speedo, not swim briefs, not tight swim trunks). Single 16:9 turnaround reference sheet on solid pure white background. LEFT panel: side profile. CENTER panel: front view. RIGHT panel: back view. FULL-LENGTH WIDE SHOT in every panel — camera pulled back, entire body head to toe with headroom and footroom, feet visible on the floor. NOT a close-up. NOT a medium close-up. NOT a medium shot. NOT a bust shot. NOT waist-up. NOT knee-up. NOT cropped. Loose athletic gym shorts and a fitted tank top in all three views — fully clothed casting wardrobe, NOT speedo, NOT swim briefs, NOT tight swim trunks, NOT topless, NOT nude, NOT implied nudity. Standing upright, arms at their sides, hands free of any objects. Same person, identical proportions, hairstyle, and wardrobe in all three panels. Even soft studio lighting, full-length body illumination. Hyper-realistic photoreal 3D character reference model. No text, no labels, no props. Synthetic fictional character only. No real person or celebrity likeness. Clearly adult with mature facial features and adult bone structure — unambiguously 21+ adult, not teen, not school-age.
```

## Voice spec
```json
{
  "register": "derived_from_notes",
  "notes": "Calm baritone; Japanese formality levels.",
  "performance_style": "Economy; honor in posture.",
  "prompt_suffix": "Calm baritone; Japanese formality levels.",
  "gender": "male"
}
```

## Tags
- **Persona:** disciplined, subtle, honorable, Samurai-modern lead, Disciplined partner, Subtle humor
- **Genre:** anime_live_action_adjacent, family_drama, tech_thriller

## Guardrails
- Synthetic-only; do not reference or generate real-person/celebrity likeness.
- Lead every generation prompt with exact age: `34-year-old`.
- SFW wardrobe baseline on casting plates; story wardrobe via `image_edit` from plate.

## Compliance flags
- prompt_pattern:\bcelebrity\b

---
*STUDIO Casting Bible lock card — do not paraphrase appearance_lock_verbatim in production prompts.*
