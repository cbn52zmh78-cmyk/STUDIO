# Model Constraints: Nudity, Timing, Layering & Prompt Language
**Version:** 1.0 | **Date:** 2026-06-14 | **Status:** Locked Reference for All Future Work

## Core Rules (Tested Behavior)

### 1. Nudity Timing — Cannot Start in Frame 1
- The model **will not generate** topless or nude female characters in the initial frame or first generation.
- Straight topless/nude images or videos that begin in a nude state are blocked.
- Topless or nude states can **only** be introduced later in a video, typically after the first 2–3 seconds, via **video extension**.
- Rule: Generate the initial clothed scene first → extend to introduce state change (topless).

### 2. Character Integration Requirement (Baking)
- If a female character is intended to go topless later in the scene, **she must be baked into the initial scene generation** as part of the composition and setting from the very first frame.
- You **cannot** use a clean/neutral plate + separate actor asset approach and then attempt to make her topless in an extension. This triggers moderation.
- The character must exist in the scene as a coherent part of the environment before any clothing removal is attempted.

### 3. Post-Topless Contact & Interaction Rules
- Once a female character becomes topless, she must have **minimal physical contact** with any other person in the scene.
- She effectively must "act like she has the plague" — very limited touching is tolerated.
- Acceptable minimal contact examples: light caress on the leg, touch on the shoulder, brief hand contact.
- Two topless women in the same scene is possible if they maintain distance and relaxed, non-intimate positioning (e.g., sitting across from each other on a couch). Heavy physical interaction is blocked.
- Solo scenes are more forgiving than scenes with other characters present.

### 4. Limits on Nudity Level
- Topless (bosom exposed) is achievable in extensions.
- Full nudity (removing panties, showing genitals/vagina) is **not supported** and will be moderated.
- Allowed intimate actions while topless: caressing breasts/bosom, touching buttocks.
- Never attempt to show or describe genitals.

### 5. Prompt Language Rules (Critical for Editor Compliance)
- Use only **proper, neutral English anatomical terms**.
  - Acceptable: bosom, breasts, buttocks, calf, shin, torso, shoulder, neck, back, hips, waist, thigh, etc.
- **Strictly forbidden** (will trigger immediate moderation):
  - Any crude, lewd, slang, or euphemistic terms for intimate anatomy.
  - Any reference whatsoever to female genitals or what lies between a woman’s legs.
- **Lockbox Rule**: The entire subject of female intimate anatomy below the waist is placed in a sealed lockbox, the key is broken, and the box is thrown into the depths of the Atlantic Ocean. It does not exist in prompts. Never open it. Never reference it. Never describe it. This is non-negotiable.
- After a character becomes topless, **do not repeatedly state "topless"** in every prompt. The model can observe the current state on screen.
- You may describe bosom shape and size in neutral terms for consistency, e.g.:
  - "medium relaxed bosom"
  - "small teardrop bosom"
- Avoid overly graphic descriptors (e.g., avoid "pointy with sharp nipples"). Keep descriptions tasteful and functional.

### 6. Explicit Intimate Action Prompting (Hard Limit)
- **Never explicitly prompt** genital-region touching or intimate contact below the waist, regardless of the gender of the characters involved.
  - Forbidden examples: "she caresses her between the legs", "hand slides down her panties", "reaches for his groin", "oral sex", etc.
- The model sometimes generates such actions organically on its own (emergent behavior). This is only acceptable **if it does not result in actual genital exposure**.
- **Slip Protocol**: If any generation produces visible genitals (vagina, penis, or full genital exposure) due to clothing slip, model error, or emergent behavior:
  - The file must be immediately deleted.
  - The exact prompt must be reported and logged in the dedicated `Slips.md` file.
  - That prompt is permanently banned from future use.
- You **can** block shots so that explicit acts occur off-screen while showing only reactions (e.g., the receiving person's face and upper body).
- Explicitly stating genital-area contact in a prompt will trigger moderation.
- Allowed: embracing, kissing, caressing the body, light touching on legs/shoulders/arms, etc., as long as it stays away from explicit genital prompts.

### 7. General Best Practice
- When working with layered clothing or fabric removal (jackets, sweaters, bikini tops, etc.), generate the initial clothed state with the character properly integrated into the scene.
- Test fabric weight, drape, and removal mechanics in controlled extensions.
- Always prioritize natural, motivated action over forced or abrupt clothing changes.

---

## 8. Asset Actors vs Prompt-Generated Characters for Intimate Physical Scenes (New Rule — June 2026)

### Core Discovery
The video editor treats **asset-based actors** (@1 + @2 compositing) differently from characters generated purely through prompt description when it comes to physical intimacy.

### What Is Allowed With Two Asset Actors (@1 + @2)
- Touching, embracing, and caressing
- Kissing, including deep and passionate kissing (mouth-closed preferred for cleaner results; visible tongue swapping is poorly handled by the model)
- Light to moderate physical closeness

**Two asset actors can safely be used for pre-sex intimacy and build-up scenes.**

### What Requires One Character Baked + One Prompt-Generated
For **elevated physical intimacy** that the editor still permits (dry humping, grinding, more aggressive embracing from behind, etc.), the following structure must be used:

- One character must be **baked into the setting plate** (asset slot 1).
- The second character must be **fully generated via prompt description** — no asset image or reference plate may be used for them.

Attempting to use two asset actors for this level of physicality will trigger moderation.

### Practical Application for Cinematic Work
In narrative filmmaking, the goal is almost always to show the **build-up to intimacy** rather than explicit sex. This includes:
- Heightened caressing
- Hand on cheek / neck
- Slow embracing
- Deep kissing
- Body closeness and tension

These moments can be achieved with two asset actors without issue. The stricter limitations only apply when pushing into dry humping or more overt physical grinding.

### Recommendation
- Use two asset actors (@1 + @2) for most intimate build-up scenes.
- Reserve the baked + prompt-generated method only when the scene specifically requires the higher level of physical contact the editor allows.
- Never prompt explicit genital contact or below-the-waist intimate touching regardless of method.

---

**This document is now the canonical reference for all future scenes involving clothing state changes, topless/nude elements, or intimate physical interaction.**