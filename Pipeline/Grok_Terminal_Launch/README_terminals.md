# Grok Terminal Launch — Dead Languages Slate v1
## 480p Test Renders — Seamless Transitions v2

---

## Terminal Assignment

| Terminal | Script | Episode | Title |
|---|---|---|---|
| **T1** | `T1_latin_launch.sh` | `david_latin_corpus_v1` | Why Latin Never Really Died |
| **T2** | `T2_ancient_greek_launch.sh` | `david_ancient_greek_corpus_v1` | Restoring the Pitch Accent |
| **T3** | `T3_old_english_launch.sh` | `david_old_english_corpus_v1` | Beowulf's Tongue in Manuscript |
| **T4** | `T4_old_norse_launch.sh` | `david_old_norse_corpus_v1` | Runes Attested, Sagas Reconstructed |
| **T5** | `T5_gothic_launch.sh` | `david_gothic_corpus_v1` | A Language Saved by One Bible |
| **T1–T5 (first free)** | `SUMERIAN_queue.sh` | `david_sumerian_corpus_v1` | The First Written Language |
| **COMMIT** | `T6_COMMIT_after_render.sh` | — | Package + gate verify + commit |

Run Sumerian on whichever of T1–T5 finishes first. All 6 must complete before running the COMMIT terminal.

---

## How to Run

Open 5 terminal windows (or Grok terminal sessions). In each, run the appropriate script:

```bash
# Example — T1
bash "C:\Users\NCG\Videos\Grok Projects\STUDIO\Pipeline\Grok_Terminal_Launch\T1_latin_launch.sh"
```

When any terminal finishes, immediately queue Sumerian in that window:
```bash
bash "C:\Users\NCG\Videos\Grok Projects\STUDIO\Pipeline\Grok_Terminal_Launch\SUMERIAN_queue.sh"
```

When all 6 are complete, run the COMMIT terminal:
```bash
bash "C:\Users\NCG\Videos\Grok Projects\STUDIO\Pipeline\Grok_Terminal_Launch\T6_COMMIT_after_render.sh"
```

---

## How to Check Render Status

```bash
# Dry-run status table — shows all 6 episodes and their current state
cd "C:\Users\NCG\Videos\Grok Projects"
python3 STUDIO/Pipeline/batch_runner.py --slate dead_languages --dry-run
```

Output will show: `PACKAGED` / `READY_TO_PACKAGE` / `MISSING_SCRIPT` / `MISSING_MP4` for each episode.

Render output lands in: `DAVID/productions/<slug>_longform_v1/`

---

## What Changed — Seamless Transitions v2

This batch resolves the "bunch of 6-second clips" problem. Three root causes were fixed:

**1. xfade duration: 0.2s → 1.8s (dissolve)**
Previously: 0.2-second crossfade — so fast it reads as a hard cut. The human eye needs ~1s minimum to register a dissolve as intentional. Documentary standard is 1.5–2.0s. Changed to 1.8s in all 6 script.json files, `Production_Templates_v1.json` seamless_defaults, and `consume_ai_handoff.py`.

**2. Shot duration: 8s → 12s per shot**
Previously: 7–9s shots (the Grok API's "seamless extend" clip discipline). At 8s/shot, 8 shots = 64s of staccato cuts. Documentary pacing is 10–18s per shot — slow enough for information to breathe. Changed `shot_duration.py` SEAMLESS_LO=12, SEAMLESS_HI=18. All 6 scripts patched to 12s/shot (96s total runtime).

**3. Motion continuity cues in video prompts**
Each shot prompt now carries an explicit cue telling the renderer how to connect to the previous shot. Shot 0 says "Opening shot, establish environment slowly." Middle shots say "Continue from previous shot — same camera direction, smooth motion carry." Final shot says "Final shot — slowly pull back or hold still, let breath settle." This prevents the renderer from treating each shot as a fresh scene.

---

## Render Mode — 480p vs Production

The constant `RENDER_RESOLUTION` in `consume_ai_handoff.py` controls output resolution for new script.json files generated via the AI handoff pipeline:

```python
# Line ~35 of consume_ai_handoff.py
RENDER_RESOLUTION: str = "854x480"   # test
# Change to:
RENDER_RESOLUTION: str = "1280x720"  # 720p
RENDER_RESOLUTION: str = "1920x1080" # production
```

The existing 6 launch scripts were directly patched to `"resolution": "854x480"` in their config blocks. To switch them to 720p before a production run, update that value in each script.json (or re-intake from concept via `production_intake.py` after flipping the constant in `Production_Templates_v1.json`).

---

## Gate 0 Verification

Before committing, the COMMIT script runs `verify_gate_0.py` — must return 27/27 GREEN. If it returns anything less, do not commit. Check the output for which test failed.

---

## Episode Specs (all 6)

- Resolution: 854×480 (test)
- Runtime: 96s (8 shots × 12s)
- Transition: dissolve, 1.8s xfade
- render_mode: test
- Gate 0: GREEN (all pre-verified)
