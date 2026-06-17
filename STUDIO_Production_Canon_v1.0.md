# STUDIO — Production Canon v1.0
**Compiled from trial, error, and research** | June 2026  
**Status:** Hard code reference — project-agnostic

---

## 1. JSON PROMPT ARCHITECTURE

Standard structure for all video generation prompts:

```json
{
  "command": "generate video",
  "scene": "[pure stage direction — action, position, concurrent movement]",
  "camera": "[shot size + movement + motivation]",
  "@1": { "description": "see attached render" },
  "@2": { "description": "see attached render" },
  "style": "[cinematic style + lighting + atmosphere + director reference]",
  "output": { "sequence_length": "[seconds]" }
}
```

---

## 2. ASSET SLOT RULES

### @1 — Body Reference
- Describe **clothing physics and movement only**
- Never describe appearance, face, or body
- Correct: fabric weight, drape, how clothing moves with the body
- Wrong: hair color, skin tone, facial features — anything visual about the person

### @2 — Head Reference
- One phrase only: **"see attached render"**
- Nothing else. Over-describing @2 fights the loaded image and degrades output
- @2 drops out when the subject no longer exists in its original form (transformation, destruction, etc.)

### Tone & Mood Modifiers

Any @1 reference — character, animal, or setting — can carry a behavioral descriptor in parentheses:

```
CHARACTER (@1, [behavioral descriptor])
ANIMAL (@1, [behavioral descriptor])
SETTING (@1, [atmosphere / ambient behavior / sound design / energy])
```

**The parentheses direct behavior, not appearance.** The reference image handles appearance. This applies to everything — people, animals, environments.

**For characters and animals:**
- Personality traits, energy, affect
- Speech delivery, rhythm, accent
- How they carry themselves, move, respond
- Emotional register

**For settings:**
- Atmospheric energy and tone (lively, ominous, Disney-warm, Viking-grim)
- Behavior of background elements (cheerful people milling around, vendors calling out, birds moving through)
- Ambient sound design (background music style, crowd noise, nature sounds, wind)
- Overall world feeling — the setting has its own behavioral quality just like a character does

**Examples:**
- Character: `(@1, warm grounded confidence, articulate and natural, delivery slips into warmth when comfortable)`
- Animal: `(@1, alert but calm, ears tracking movement, weight shifting with cautious curiosity)`
- Setting: `(@1, lively town square at midday, cheerful townsfolk moving between market stalls, distant folk music carried on the breeze, warm and animated — think Disney village energy)`
- Setting: `(@1, Norse longhouse interior, firelight flickering, men sharpening weapons in near-silence, low murmur of old language, heavy and purposeful atmosphere)`

The setting plate is a character. Direct it the same way.

---

### Two Asset Actors (@1 + @2)
Both slots occupied = asset actor pair. Permitted for:
- Touching, embracing, caressing
- Kissing including deep/passionate (mouth-closed preferred — tongue swap poorly handled)
- Light to moderate physical closeness
- Pre-intimacy build-up scenes

Two asset actors **cannot** be used for elevated physicality (grinding, dry humping, aggressive from-behind action) — will trigger moderation. See Section 6.

---

## 3. OUTFIT CHANGE RULE

**Exact syntax — non-negotiable:**
```
change her outfit to [garments + layers + footwear + accessories]
change his outfit to [garments + layers + footwear + accessories]
```

**Concise but complete.** Include: main garments, layers, footwear, key accessories.  
**Do not repeat** the character's physical description — the reference image handles that.

| | |
|---|---|
| **Too vague** | `change her outfit to winter clothes with a coat and scarf` |
| **Too bloated** | Repeating the character's age, ethnicity, appearance, lighting notes, etc. |
| **Correct** | `change her outfit to a black turtleneck sweater under a long camel wool coat, dark grey straight-leg trousers, black leather knee-high boots, thick cream scarf, black beanie` |

Same rule as everywhere else: describe the clothing, not the person wearing it.

---

## 4. SCENE WRITING RULES

### Concurrent Action Language
- Use: **whilst / as / while / meanwhile**
- Never: **"and then"** — sequential narration kills simultaneous action
- "And then" = Little Timmy storytelling. It does not belong in a scene line.

### Scene Line = Pure Stage Direction
- What the body does, where it is, how it moves
- No camera language in the scene field — camera goes in the camera field
- No emotional description — convey emotion through action, not adjectives

### General
- One action chain per scene block
- Spatial relationships must be explicit — the model does not infer positioning
- Weight, bracing, and surface contact must be stated — characters float if not grounded

---

## 5. CAMERA RULES

### Shot Size = Distance — Always
Camera distance is expressed in **shot size terminology only**:
- Wide shot / medium wide / medium shot / medium close-up / close-up / extreme close-up
- **Never use physical measurements** (5 feet, 10 meters, etc.)
- Physical measurements cause the actor to walk out of the skybox

### Camera Movement
State: movement type + speed + motivation
- "slow push-in toward her face as realization settles"
- "static locked-off wide, star centered, generous negative space"
- "handheld follow, slight shake, tracking alongside movement"

### Camera as Storyteller
Use camera movement to imply action that should not or cannot be shown directly:
- Slow zoom to reaction shot while physical action moves off-screen
- Cut to environment or object at the moment of impact
- Suggestion is frequently more powerful than explicit depiction

---

## 6. BLOCKING SYSTEM

### Stage Grid (9 Zones — Actor's POV Facing Audience)
```
UR  UC  UL
CR  CC  CL
DR  DC  DL
```
U = Upstage / D = Downstage / R = Right / L = Left / C = Center (actor's perspective)

### Movement Notation
| Code | Meaning |
|------|---------|
| Ent | Enter |
| Ex | Exit |
| X | Cross (move to) |
| p | Pause |
| u | Up (move upstage) |
| d | Down (move downstage) |
| s | Sit |
| Kn | Kneel |
| Lie | Lie down |
| R | Rise |
| t | Turn |
| a | Aside |

Recording format: **Character + Action + Destination/Object**  
Example: `She X DR / Kn / faces UC`

### Blocking Principles
- **Levels**: High / Medium / Low — vary them, don't play everything standing
- **Triangles**: Position characters in triangles, not straight lines — straight lines flatten composition
- **Cheat Out**: Characters angle toward camera even in scenes that would logically play profile

---

## 7. INTIMACY PROTOCOL

### Primary Workflow
1. **Strong foundation prompt** — establish physical relationship, spatial positioning, rhythm, and emotional tone
2. **Clean extensions** — use extend without new prompts; the editor maintains what the foundation set
3. **Fishing** (blank prompt extensions) — only after a solid base scene is locked; lets the editor invent continuations

### Asset Structure by Level

| Level | Method |
|-------|--------|
| Touching, embracing, kissing, build-up | @1 + @2 (two asset actors) |
| Grinding, dry humping, aggressive physical contact | One character **baked into setting plate** (@1) + second character **fully prompt-generated** (no asset image) |
| Explicit genital contact / below-waist intimate touching | **Permanently forbidden. No exceptions.** |

### Language
- Clinical and neutral only: bosom, waist, hips, lower back, shoulder, neck, thigh
- No slang, no crude descriptors
- Spatial relationships must be explicit in the foundation prompt

### Known Technical Weaknesses + Mitigations
- **Neck/head rotation strain**: Most severe in sustained from-behind kissing. Fix: keep rear contact brief, prefer side-entry or front-facing for longer sequences
- **Unsupported weight / floating**: Explicitly prompt bracing and weight transfer
- **Limb clipping**: Precise spatial prompting; accept minor cleanup in post
- **Hand specificity**: "right hand / left hand" resolves correctly ~60% of the time

---

## 8. NUDITY & CLOTHING STATE RULES

- **Nudity cannot begin on frame 1** — must always extend from a clothed initial generation
- **Baking requirement**: Any intended clothing state change later in the sequence requires the character to be integrated (baked) into the scene from frame 1
- Removing clothing layers mid-scene frequently breaks continuity (tattoos, marks, textures)
- Strengthen fabric physics in @1 to resist clothing disappearance during movement

---

## 9. MULTI-PHASE SEQUENCING

For long-form events (transformations, extended sequences, 30s+), break into 10-second segments:

- **Phase 1**: Establish the event — load @1 and @2 if subject exists in original form
- **Phase 2**: Sustained state — drop @2 if subject has transformed; maintain @1 for continuity
- **Phase 3**: Decline/resolution — camera can shift (push-in, slow zoom) to signal conclusion

Key rule: **@2 only applies to a subject in its pre-event state.** Once the subject transforms or is destroyed, @2 is not used in subsequent phases.

For physics realism: **asymmetrical and chaotic structure** consistently outperforms perfect radial symmetry.

---

## 10. CENTRAL ANCHOR INFINITE ORBIT (Dollhouse Orbit Loop)

Technique for stable continuous orbiting shots over extended duration.

**Requirements:**
1. **Unified 3D asset as @1** — entire environment as one model, not separate elements
2. **Church Method lock** — camera anchored to exact geometric center of the platform/scene
3. **Character + camera sync** — character movement speed timed to match camera orbital rate
4. **Periodic plate refresh** (takes over ~10s) — re-inject @1 reference every 2–3 seconds to counter drift
5. **Clean environment** — simple sky, minimal moving elements reduce tracked variables

**Known limitation**: Loop seam not yet clean — frame 0 and final frame do not perfectly match pose/shadow. In development.

**Best use**: Establishing shots, atmospheric sequences, title work, any shot requiring sustained circular camera movement.

---

## 11. CINEMATIC PROSE — PROMPTING LANGUAGE

### Hybrid Formula
**Subject + Action/Movement + Scene/Environment + Cinematic Language + Lighting/Atmosphere + Style Reference**

### Ratio
- Target 30–50% cinematic language woven into narrative description
- Too many technical terms: mechanical, loses story
- Too few: loses camera control

### Sentence Structure = Pacing
- Short sentences / fragments: urgency, impact, fast cuts
- Long flowing sentences: immersion, reflection, slow scenes
- Match sentence rhythm to the scene's emotional register
- Read prompts aloud — aim for musical flow

### Paragraph Breaks = Shot Rhythm
- New paragraph = suggested shot change or significant beat shift
- Use white space to pace the model the way an editor paces a cut

### Prompt Workflow
1. Start with the narrative core (what happens, why it matters)
2. Layer cinematic grammar (shot type, camera move, framing)
3. Add style/director reference
4. Control pacing through sentence and paragraph length
5. Test variants: prose-heavy / technical-heavy / well-blended

---

## 12. PRODUCTION WORKFLOW SEQUENCE

```
Elf Pass → Scene Phase → Video Prompt Phase → Canon Protection
```

**Elf Pass**: Major pictures / flow with simple blocking notation  
**Scene Phase**: Full scene built with stage directions and blocking  
**Video Prompt Phase**: Scene translated into JSON prompt architecture  
**Canon Protection**: Locked output filed; prompt archived

**Legal Gate 0** runs before any generation. RED = hard stop. No generation, no shoot, no publish. No debate.

---

*STUDIO Production Canon v1.0 — project-agnostic, hard code reference*  
*All techniques derived from systematic testing. No story references.*
