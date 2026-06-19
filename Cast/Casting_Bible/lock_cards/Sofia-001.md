# Sofia-001 — Sofia Andersson

**Status:** LOCKED  
**Content rating:** SFW  
**Synthetic:** Yes — no real-person likeness  
**AI disclosure required:** Yes

## Identity
| Field | Value |
|-------|-------|
| Actor ID | `Sofia-001` |
| Stage name | Sofia Andersson |
| Talent ID | `sofia_andersson` |
| Age (locked) | **29** |
| Gender | female |
| Ethnicity | Swedish |
| Region | europe_west |
| Roster group | — |

## Reference
- **Primary plate:** `STUDIO/Cast/actors_roster/female/europe_west/Sofia_Andersson/01_casting_shots/casting_turnaround_v1.jpg`
- **Roster path:** `STUDIO/Cast/actors_roster/female/europe_west/Sofia_Andersson`

## Appearance lock (verbatim — reuse every shot)
```
GENERATE 3D MODEL of back, side and front profiles of 29-year-old Swedish woman, 5'10", long-limbed athletic build, straight platinum-blonde bob, ice-blue eyes, fair Nordic skin, minimal brows, wearing a fully covered high-waisted navy bikini top and matching navy bikini bottoms. Single 16:9 turnaround reference sheet on solid pure white background. LEFT panel: side profile. CENTER panel: front view. RIGHT panel: back view. FULL-LENGTH WIDE SHOT in every panel — camera pulled back, entire body head to toe with headroom and footroom, feet visible on the floor. NOT a close-up. NOT a medium close-up. NOT a medium shot. NOT a bust shot. NOT waist-up. NOT knee-up. NOT cropped. Fully covered high-waisted bikini top and matching bikini bottoms in all three views — fully clothed casting wardrobe, NOT topless, NOT nude, NOT implied nudity. Standing upright, arms at their sides, hands free of any objects. Same person, identical proportions, hairstyle, and wardrobe in all three panels. Even soft studio lighting, full-length body illumination. Hyper-realistic photoreal 3D character reference model. No text, no labels, no props.
```

## Voice spec
```json
{
  "register": "derived_from_notes",
  "notes": "Clear, cool timbre; softens one notch in intimacy.",
  "performance_style": "Economy of motion; less-is-more Nordic restraint.",
  "prompt_suffix": "Clear, cool timbre; softens one notch in intimacy.",
  "gender": "female"
}
```

## Tags
- **Persona:** observant, cool, deadpan, Cool investigator, Nordic noir lead, Quiet avenger
- **Genre:** coastal, literary, period_drama, prestige_tv

## Guardrails
- Synthetic-only; do not reference or generate real-person/celebrity likeness.
- Lead every generation prompt with exact age: `29-year-old`.
- SFW wardrobe baseline on casting plates; story wardrobe via `image_edit` from plate.

---
*STUDIO Casting Bible lock card — do not paraphrase appearance_lock_verbatim in production prompts.*
