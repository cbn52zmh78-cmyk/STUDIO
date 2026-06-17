# Central Anchor Infinite Orbit + Character Sync
**Technique v1.0** | June 2026

---

## Overview

Technique for achieving stable, continuous orbiting shots with persistent character and environment over extended durations. Combines environmental locking via a unified 3D asset, camera anchored to a fixed geometric center, and optional character motion synchronized to the camera's rotational speed.

---

## Core Principles

**1. Unified 3D Asset as Environmental Anchor (@1)**
The entire environment (buildings, platform, set) is treated as one single cohesive 3D model loaded into @1. Not separate elements — one unified asset. This is the primary stability mechanism. Dramatically reduces drift and regeneration compared to multiple separate references.

**2. Fixed Geometric Center Lock (Church Method)**
Camera is anchored to the exact geometric center of the platform or scene using the Church Method — fixed subject lock applied to the center point rather than the character. This produces clean, mechanical circular motion the model can sustain. No drift from a floating or approximate center.

**3. Character + Camera Sync**
When the character moves, their movement speed is timed to match the camera's rotational rate. Keeps the character in consistent compositional relationship to the environment and reduces asset strain during combined locomotion + camera movement.

**4. Periodic Plate Refresh (extended takes)**
For takes beyond ~10 seconds, explicitly instruct re-injection of the @1 background reference every 2–3 seconds. Counteracts cumulative environmental drift on long orbits.

**5. Controlled Environment Complexity**
Clean sky, simple ground plane, minimal moving elements. Fewer tracked variables = better long-term consistency.

---

## Tested Configurations

**Static character, 5s orbit**
Camera orbits platform center. Character fixed in position. Result: clean mechanical rotation, strong dollhouse composition.

**Walking character, 15s orbit**
Camera orbits continuously. Character walks in sync, circling the environment. @1 refreshed periodically. Result: character asset survives combined locomotion + camera movement across extended duration. Environment detail stable.

---

## Strengths
- High asset persistence for both character and environment during continuous motion
- Dollhouse / symmetrical compositional aesthetic
- Reproducible and controllable — consistent across multiple generations
- Strong candidate for seamless infinite loop sequences

## Current Limitations
- Loop seam not yet clean — frame 0 pose, dress folds, and shadow angles do not perfectly match final frame
- Minor perspective drift on curved geometry over very long takes
- Character-camera sync requires precise timing language in prompt

---

## Recommended Use Cases
Establishing shots, hypnotic or atmospheric sequences, title work, circular platform environments, any scene requiring extended continuous camera orbit.

---

## Next Development Steps
- Formalize reusable prompt template
- Engineer true seamless loop: character completes exactly one full circle, final frame engineered to cut cleanly to frame 0
- Test subtle atmospheric additions (fog, moving clouds, light shift) while maintaining loop integrity
