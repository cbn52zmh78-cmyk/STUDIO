# Tomas-001 — Tomas Novak

**Status:** LOCKED  
**Content rating:** SFW  
**Synthetic:** Yes — no real-person likeness  
**AI disclosure required:** Yes

## Identity
| Field | Value |
|-------|-------|
| Actor ID | `Tomas-001` |
| Stage name | Tomas Novak |
| Talent ID | `tomas_novak` |
| Age (locked) | **26** |
| Gender | male |
| Ethnicity | Czech |
| Region | europe_east |
| Roster group | — |

## Reference
- **Primary plate:** `STUDIO/Cast/actors_roster/male/europe_east/Tomas_Novak/01_casting_shots/casting_turnaround_v1.jpg`
- **Roster path:** `STUDIO/Cast/actors_roster/male/europe_east/Tomas_Novak`

## Appearance lock (verbatim — reuse every shot)
```
GENERATE 3D MODEL of back, side and front profiles of 26-year-old Czech man, 5'11", lanky build, messy brown hair, hazel eyes, pale skin, angular features, wire-frame glasses off-duty, wearing loose athletic gym shorts in grey and a fitted grey tank top (not speedo, not swim briefs, not tight swim trunks). Single 16:9 turnaround reference sheet on solid pure white background. LEFT panel: side profile. CENTER panel: front view. RIGHT panel: back view. FULL-LENGTH WIDE SHOT in every panel — camera pulled back, entire body head to toe with headroom and footroom, feet visible on the floor. NOT a close-up. NOT a medium close-up. NOT a medium shot. NOT a bust shot. NOT waist-up. NOT knee-up. NOT cropped. Loose athletic gym shorts and a fitted tank top in all three views — fully clothed casting wardrobe, NOT speedo, NOT swim briefs, NOT tight swim trunks, NOT topless, NOT nude, NOT implied nudity. Standing upright, arms at their sides, hands free of any objects. Same person, identical proportions, hairstyle, and wardrobe in all three panels. Even soft studio lighting, full-length body illumination. Hyper-realistic photoreal 3D character reference model. No text, no labels, no props.
```

## Voice spec
```json
{
  "register": "derived_from_notes",
  "notes": "Soft tenor; rapid Czech-English code-switch.",
  "performance_style": "Naturalistic fidget; honesty in pause.",
  "prompt_suffix": "Soft tenor; rapid Czech-English code-switch.",
  "gender": "male"
}
```

## Tags
- **Persona:** quirky, earnest, anxious, Quirky indie lead, Coder sidekick, Earnest romantic
- **Genre:** cold_war, noir, prestige_tv, thriller

## Guardrails
- Synthetic-only; do not reference or generate real-person/celebrity likeness.
- Lead every generation prompt with exact age: `26-year-old`.
- SFW wardrobe baseline on casting plates; story wardrobe via `image_edit` from plate.

---
*STUDIO Casting Bible lock card — do not paraphrase appearance_lock_verbatim in production prompts.*
