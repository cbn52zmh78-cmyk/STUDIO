# Render Directive v2 — Seamless Transitions
## Upon Tyne Productions / DAVID channel
### Pipeline: STUDIO/Pipeline — effective 2026-06-20

---

## Background: The "Bunch of Clips" Problem

The first test renders of the dead-language slate had a specific feel: abrupt, choppy, like a slide deck rather than a documentary. The root cause was not the content — it was three pipeline defaults that were never tuned for long-form documentary pacing:

1. 0.2-second crossfade (registered as a hard cut, not a dissolve)
2. 7–9 second shot durations (music video pace, not documentary)
3. No motion continuity signal between shots (each shot rendered cold, no visual thread)

This directive documents the fixes and the reasoning behind each.

---

## Fix 1 — xfade: 0.15s / 0.2s → 1.8s

### What changed
`Production_Templates_v1.json` `seamless_defaults.xfade_s`: `0.2` → `1.8`  
`consume_ai_handoff.py` seamless block `xfade_s`: `0.15` → `1.8`  
All 6 launch episode `script.json` files: `seamless.xfade_s` patched to `1.8`

### Why 1.8 seconds

The crossfade is the moment two clips overlap — the outgoing clip fades out as the incoming one fades in. At 0.2 seconds, the overlap is 5 frames (at 24fps). That's not perceptible as a dissolve. The human visual system needs roughly 20–30 frames (0.8–1.3 seconds) to register a transition as intentional rather than a glitch. Below that threshold, the cut reads as abrupt.

Documentary standard is 1.5–2.0 seconds. BBC/Attenborough-style work uses 1.8–2.2s for host-on-camera segments. 1.8s was chosen as the floor — it's the low end of the documentary band, conservative enough not to feel slow but long enough to read as considered.

At 1.8s xfade with 12s shots: approximately 15% of each shot is cross-fading with its neighbors. That ratio is where documentary seamlessness lives.

### When to tune this further

Use `1.2–1.5s` for faster-paced explainer formats (science, technical) where the content moves at a higher words-per-second rate and slower dissolves feel sluggish.

Use `2.0–2.5s` for emotional or lyrical beats — the final shot of a historical figure episode, a silence beat, a wide establishing shot. The longer fade honors the weight of the moment.

Use `0.3–0.5s` only when you intentionally want a near-cut — for a precision reveal, a word-on-screen beat, or a music-sync hit. Never use it as a default.

---

## Fix 2 — Shot Duration Floor: 4s / 7s → 12s

### What changed
`shot_duration.py` `SEAMLESS_LO`: `7` → `12`  
`shot_duration.py` `SEAMLESS_HI`: `9` → `18`  
`consume_ai_handoff.py` `_build_shots()` minimum: `max(4, ...)` → `max(12, ...)`  
All 6 launch episode `script.json` files: shot durations patched from `~8s` to `12s`

### Why 12 seconds

The previous floor of 7–9 seconds came from the Grok API's "seamless extend" clip discipline — an API constraint, not an editorial choice. The pipeline inherited it as a content-pacing decision by accident.

At 8 seconds per shot:
- 8 shots × 8s = 64s of content
- Minus 7 transitions at 1.8s each = 12.6s of overlap budget consumed
- Net unique content per shot: ~6.4s visible before the next shot begins fading in

That's where the "6-second clip" feeling comes from. The shot timer and the xfade timer were fighting each other.

At 12 seconds per shot:
- 8 shots × 12s = 96s of content
- 7 transitions at 1.8s = 12.6s overlap
- Net unique content per shot: ~10.4s visible — enough time for a sentence, a breath, and a moment of visual information to land

Documentary pacing (Attenborough, Ken Burns, PBS Frontline) averages 12–18 seconds per shot. Faster formats (science explainers, news packages) average 8–12 seconds. Music videos average 3–6 seconds. The pipeline was accidentally in music-video territory.

The new range (SEAMLESS_LO=12, SEAMLESS_HI=18) puts DAVID episodes firmly in documentary territory.

### Shot duration vs. speech content

An important distinction: shot duration is the length of the rendered video clip, not the length of the speech. A 12-second shot with 8 seconds of speech will have 4 seconds of post-speech visual — the host settling, looking thoughtful, or the Archive set holding atmosphere. This is intentional documentary breathing room. It also gives the dissolve enough visual tail to work with.

### When to tune this further

Static shots (host at desk, not moving): 12–15s is ideal.  
Action shots (host with props, gestures, movement): can go to 18s to let the motion complete.  
B-roll / insert shots (manuscript close-up, on-screen text): 8–12s is fine — these are visual punctuation, not primary content.

---

## Fix 3 — Motion Continuity Cues

### What changed
`consume_ai_handoff.py` `_build_video_prompt()` now accepts `shot_index` and `total_shots` and appends a continuity cue to every video_prompt. All 6 launch episode `script.json` files: continuity cues appended to prompts where missing.

### The three cue types

**Opening shot (index 0):**  
`"Opening shot, establish environment slowly."`  
Tells the renderer: this is the first clip — take time to settle into the space, do not begin mid-motion.

**Middle shots (index 1 to n-2):**  
`"Continue from previous shot — same camera direction, smooth motion carry."`  
This is the most important cue. Without it, the renderer treats each shot as a fresh scene, possibly changing camera angle, resetting the ambient motion, or starting a new camera move. "Same camera direction, smooth motion carry" keeps the visual thread continuous across the dissolve.

**Final shot (index n-1):**  
`"Final shot — slowly pull back or hold still, let breath settle."`  
Signals the end of the episode. A slow pull or a hold gives the renderer (and the viewer) a landing. Without this, the last shot can feel like it was cut off mid-sequence.

### What "motion carry" means in `config.seamless`

The flag `"motion_carry": true` is a render directive that tells the renderer to:
- Match the direction of ambient motion between outgoing and incoming clips (if the previous clip has a slow left pan, the incoming clip should not start with a right pan)
- Preserve the camera axis (don't cut from a right-angle to a left-angle without a motivated camera move)
- Maintain consistent lighting temperature across the dissolve

This is distinct from the xfade duration — xfade is about time, motion_carry is about spatial coherence.

### `cut_style: "soft"` vs `"hard"`

`"soft"` = dissolve/fade transition. The clips overlap in opacity during the xfade window.  
`"hard"` = straight cut. No overlap, no fade. Used only when a cut is editorially motivated (beat hit, word-on-screen reveal, music sync).

DAVID documentary episodes use `"soft"` exclusively. Switch to `"hard"` only for a deliberate editorial effect.

---

## Resolution — 480p Test vs Production

`consume_ai_handoff.py` line ~35:
```python
RENDER_RESOLUTION: str = "854x480"  # test render resolution
```

This constant overrides `deliverable_spec.resolution` for all new script.json files generated via the AI handoff pipeline. To promote to production:

| Constant value | Resolution | Use case |
|---|---|---|
| `"854x480"` | 480p | Test renders, pipeline validation |
| `"1280x720"` | 720p | Review quality, pre-production |
| `"1920x1080"` | 1080p | Production / upload |

The 6 launch scripts were directly patched to `"854x480"`. To promote them to 720p, change `config.resolution` in each `script.json`, or re-intake from concept with `production_intake.py` after updating `Production_Templates_v1.json`.

---

## Files Changed in This Directive

| File | Change |
|---|---|
| `STUDIO/Pipeline/consume_ai_handoff.py` | `RENDER_RESOLUTION` constant; `xfade_s`=1.8, `primary`=dissolve, `motion_carry`, `cut_style`; min shot 12s; motion continuity cues in `_build_video_prompt()` |
| `STUDIO/Pipeline/shot_duration.py` | `SEAMLESS_LO`=12, `SEAMLESS_HI`=18 |
| `STUDIO/Pipeline/Production_Templates/Production_Templates_v1.json` | `seamless_defaults.xfade_s`=1.8, `primary`=dissolve, `motion_carry`, `cut_style`; guardrail language updated |
| `DAVID/scripts/longform_scripts/david_*_corpus_v1_script.json` (×6) | `config.seamless` patched; shot durations bumped to 12s; `t_start`/`t_end` recomputed; motion continuity cues appended to all `video_prompt` fields |
| `DAVID/batches/T3_dryrun/scripts/david_*_corpus_v1_480p_script.json` (×6) | Same as above |
| `STUDIO/Pipeline/Concepts/templates/documentary-host.concept.template.json` | `target_seconds`: 69 → 120 |
| `STUDIO/Pipeline/Concepts/templates/historical-figure-documentary.concept.template.json` | `target_seconds`: 54 → 60 |
| `STUDIO/Pipeline/Concepts/templates/science-explainer.concept.template.json` | `target_seconds`: 54 → 60 |
| `STUDIO/Pipeline/Concepts/templates/technical-explainer.concept.template.json` | `target_seconds`: 54 → 60 |

---

## Summary Principle

> Seamlessness in AI video is not about hiding the cuts — it's about making the cuts breathe. Long enough that the viewer settles in. Slow enough that the dissolve registers as intention. Continuous enough that each shot feels like it grew out of the last one rather than replacing it.

The 0.2s / 8s defaults were never wrong — they were defaults. This directive makes them editorial choices.
