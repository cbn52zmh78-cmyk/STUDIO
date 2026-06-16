# Queen Rowhouse Orbit Technique — Technical Note v1.0

**Date**: June 12, 2026  
**Project**: SPIT  
**Status**: Locked for reference

## Overview
This note documents the successful "Central Anchor Infinite Orbit + Character Sync" tests using Queen in front of a stylized multi-colored rowhouse on a circular cobblestone platform. The technique combines environmental locking, single-asset architecture, and synchronized camera/character motion to achieve stable orbiting shots with strong potential for seamless looping.

## Key Technical Insight (User Clarification)
The exceptional environmental stability comes from treating **the entire collection of rowhouses as one single unified 3D asset** rather than separate buildings. This unified model serves as the primary environmental reference (@1), dramatically reducing drift and regeneration issues during continuous camera movement.

## Test Breakdown

### Video 1 (5s Orbit — Static Queen)
- **Camera Behavior**: Slow, smooth orbit locked to the exact geometric center of the circular cobblestone platform.
- **Anchor**: Center point of the platform + the unified rowhouse 3D asset as @1.
- **Character**: Queen static on the left side of the platform.
- **Result**: Clean mechanical rotation. Queen remains in consistent screen position relative to the building. Strong dollhouse/symmetrical composition.

### Video 2 (15s Orbit — Walking Queen)
- **Camera Behavior**: Continuous orbiting camera locked to platform center.
- **Character Motion**: Queen walking in rotational sync with the camera orbit, circling the building.
- **Environment Handling**: Unified 3D rowhouse asset + periodic background plate refresh to maintain architectural consistency (color sections, windows, rooflines).
- **Result**: Queen’s asset survives the combined locomotion + camera movement without regeneration. Building details remain highly stable across 16 frames. This is the more advanced test and demonstrates the core power of the technique.

## Core Principles of the Technique

1. **Single Unified 3D Asset as Environmental Anchor (@1)**  
   The entire curved rowhouse block is one cohesive 3D model. This is the primary lock point and reference. It provides far greater stability than multiple separate assets.

2. **Central Geometric Lock (Church Method Variant)**  
   Camera is locked to the exact center of the circular platform. This creates repeatable, mechanical orbiting motion that the model can sustain.

3. **Character + Camera Sync**  
   When the character walks, her movement is timed to match the camera’s rotational speed. This keeps her in pleasing compositional relationship to the building and reduces asset strain.

4. **Periodic Plate Refresh (for longer takes)**  
   Explicit instruction to re-inject or duplicate the background reference (@1) at regular intervals (every 2–3 seconds) to combat cumulative environmental drift during extended orbits.

5. **Stylized / Low-Detail Environment**  
   Clean sky, simple ground plane, and controlled lighting reduce the number of elements the model must track, improving long-term consistency.

## Strengths Observed
- Excellent asset persistence for both environment and character during continuous motion.
- Strong symmetrical / dollhouse aesthetic that aligns with project visual language.
- High potential for true seamless infinite loops (once loop-point matching is refined).
- Reproducible and controllable — ideal for establishing shots, hypnotic sequences, or title work.

## Current Limitations
- Loop seam not yet perfect (pose, dress folds, and shadow angles at frame 0 vs final frame do not perfectly match).
- Minor perspective drift on the curved facade over very long takes.
- Requires precise timing language in prompts for character-camera synchronization.

## Recommended Module Name
**"Central Anchor Infinite Orbit + Character Sync"** (also referred to as "Dollhouse Orbit Loop")

## Next Steps (Proposed)
- Formalize reusable prompt template based on these tests.
- Test a true seamless loop version where Queen completes exactly one full circle and the final frame is engineered to cut cleanly back to frame 0.
- Explore adding subtle atmospheric elements (fog, moving clouds, shifting light) while maintaining the loop.
- Integrate into SPIT scenes that benefit from hypnotic or symmetrical establishing shots.

---

**Locked by Director**  
This technique is now part of the active technical canon for SPIT visual development. All future orbiting or circular platform shots should reference this note.