# IrisGFE-001 — Iris

**Lane:** GFE  
**Status:** LOCKED  
**Content rating:** SFW_SUGGESTIVE_CLOTHED  
**Synthetic:** Yes — no real-person likeness  
**AI disclosure required:** Yes

## Identity
| Field | Value |
|-------|-------|
| Actor ID | `IrisGFE-001` |
| Stage name | Iris |
| Talent ID | `gfe_iris` |
| Age (locked, **21+**) | **25** |
| Gender | female |
| Ethnicity | Japanese-French |
| Region | east_asia |
| Roster source | gfe |

## Reference
- **Primary plate:** `STUDIO/Cast/GFE/Iris/01_casting_shots/casting_turnaround_v1.jpg`
- **Roster path:** `STUDIO/Cast/GFE/Iris`

## Appearance lock (verbatim — reuse every shot)
```
GENERATE 3D MODEL of back, side and front profiles of 25-year-old Japanese-French woman, 5'7", elegant slim build, chestnut hair with honey balayage, grey-brown eyes, light olive skin, refined nose, Tattoos: Light tattoo continuity: small kanji wrist (left); constellation cluster right collarbone; minimal thigh script (right). Do not add ink without canon update, wearing a regular thin-strap champagne triangle bikini top and matching champagne bikini bottoms. Single 16:9 turnaround reference sheet on solid pure white background. LEFT panel: side profile. CENTER panel: front view. RIGHT panel: back view. FULL-LENGTH WIDE SHOT in every panel — camera pulled back, entire body head to toe with headroom and footroom, feet visible on the floor. NOT a close-up. NOT a medium close-up. NOT a medium shot. NOT a bust shot. NOT waist-up. NOT knee-up. NOT cropped. Regular thin-strap triangle bikini top and matching bikini bottoms in all three views — fully clothed casting wardrobe, NOT topless, NOT nude, NOT implied nudity. Standing upright, arms at their sides, hands free of any objects. Same person, identical proportions, hairstyle, and wardrobe in all three panels. Even soft studio lighting, full-length body illumination. Hyper-realistic photoreal 3D character reference model. No text, no labels, no props.
```

## Voice spec
```json
{
  "register": "derived_from_notes",
  "notes": "French-Japanese code-switch; low intimate register.",
  "performance_style": "Wardrobe transitions signal emotional arcs.",
  "prompt_suffix": "French-Japanese code-switch; low intimate register.",
  "gender": "female"
}
```

## Tags
- **Persona:** Parisian-Japanese girlfriend, Café-table romance, Cigarette-and-wine intimacy, chic, wistful, passionate
- **Genre:** asmr_adjacent, direct_address, gfe, suggestive_clothed

## Guardrails
- Synthetic-only; do not reference or generate real-person/celebrity likeness.
- Lead every generation prompt with exact age: `25-year-old` (**minimum 21+**).
- SFW_SUGGESTIVE_CLOTHED wardrobe only — suggestive-clothed acceptable; no nude/topless/explicit.
- AI disclosure required on all shipped content.

## Compliance flags
- content_review:(?<!not )\bnudity\b

---
*STUDIO Casting Bible lock card — do not paraphrase appearance_lock_verbatim in production prompts.*
