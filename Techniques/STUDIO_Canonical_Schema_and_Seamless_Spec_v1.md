# STUDIO Canonical Schema and Seamless Spec v1
**Technique v1.0** | June 2026  
**Pairs with:** `STUDIO_LongForm_Video_Assembly_v1.md` · `STUDIO_Seamless_Continuity_Protocol_v1.1.md`  
**Pipeline:** `DAVID/scripts/render_longform.py`

---

## 1. Canonical Script Schema (only)

All long-form scripts **must** use this shape. Legacy fields (`shot_id`, `host_identity`, `closing_card`, top-level `seamless`, `continuity_prefix`, `end_guard`, `scene_id`, `join`, `guardrails`) are accepted at **load time only** — `normalize_script()` maps them in-memory; persisted copies use canonical fields.

```json
{
  "slug": "david_intro_60s_v2",
  "title": "DAVID — Self-Introduction (Channel Intro) v2 Seamless",
  "target_seconds": 69,
  "config": {
    "model_video": "grok-imagine-video-1.5",
    "resolution": "720p",
    "aspect_ratio": "16:9",
    "identity_lock": "productions/host_identity_v1/david_identity_lock.json",
    "avatar_reference": "productions/host_identity_v1/references/david_avatar_reference.jpg",
    "voice_suffix": "mid-low resonant … synthetic host only",
    "compare_v1": "productions/david_intro_60s_longform_v1/output/david_david_intro_60s_longform_v1.mp4",
    "seamless": {
      "primary": "extend",
      "xfade_s": 0.2,
      "match_color": true,
      "cut_on_motion": true
    }
  },
  "shots": [
    {
      "id": "01_cold_open",
      "duration": 8,
      "t_start": 0,
      "t_end": 8,
      "video_prompt": "CONTINUITY LOCK @David-001: … Lip-synced, delivers: \"…\" Finish on gesture peak …",
      "speech_text": "…",
      "on_screen": "DAVID · The Archive",
      "role": "host"
    }
  ],
  "provenance_card": {
    "enabled": true,
    "duration_s": 6,
    "card_type": "closing",
    "title": "DAVID · The Archive",
    "subtitle": "Dead languages, actually pronounced.",
    "footer": "Bring the dead tongues back — one attestation at a time. DAVID."
  },
  "qa_rules": {
    "require_identity_lock": true,
    "require_synthetic_guard": true,
    "min_shots": 1
  }
}
```

### Required fields

| Path | Type | Notes |
|---|---|---|
| `slug` | string | Production folder: `productions/<slug>_longform_v1/` |
| `config` | object | Model, locks, refs, optional `seamless`, optional `compare_v1` |
| `shots[]` | array | Each shot: `id`, `duration`, `video_prompt`, `speech_text`, `t_start`, `t_end` |
| `provenance_card` | object | Closing or provenance still; `enabled`, `duration_s`, text fields |
| `qa_rules` | object | Gates for `qa_report.json` |

### Seamless config (`config.seamless`)

| Key | Default | Meaning |
|---|---|---|
| `primary` | `"extend"` | Grok Imagine EXTEND within scene; frame-chain fallback |
| `xfade_s` | `0.2` | Video xfade + audio acrossfade duration at joins |
| `match_color` | `false` | Histogram/LUT normalize segment B to A before join |
| `cut_on_motion` | `false` | Trim ~0.15s tail stillness on left segment before join |

CLI flags (`--seamless`, `--match-color`, `--cut-on-motion`, `--xfade`) override or enable at run time.

### Per-shot prompt contract (seamless)

Continuity prefix and end-guard are **embedded in `video_prompt`** in the script — not separate top-level fields:

```
CONTINUITY LOCK @David-001: identical host face, charcoal sweater, Archive desk,
brass lamp, same eye-line — seamless continuation of prior take, zero jump cut.
```

```
Finish on gesture peak (hand motion or lean), never hold dead stillness or dead frame.
```

Shot 1 uses `David-001` locked reference image; shots 2..N use frame-chain (last frame → i2v) when EXTEND is unavailable.

---

## 2. Seamless Assembly (`--seamless`)

### Priority stack

| Tier | Method | When |
|---|---|---|
| **PRIMARY** | `client.video.extend()` | Same scene — one growing take, no cut |
| **JOINS** | Frame-chain + **0.2s xfade** + **acrossfade** | Between generated segments; card join |
| **Pre-join** | `--match-color` | Histogram match right segment to left reference |
| **Hard cut** | `--cut-on-motion` only | Trim tail stillness; never cut on dead frame |

### Frame-chain segment assembly

When EXTEND is unavailable, each shot is generated as `chain_<id>.mp4`, then:

```
concat_xfade_chain(chain_01, chain_02, … chain_N)
  → per join: trim tail (cut-on-motion) → match-color → xfade 0.2s + acrossfade 0.2s
  → host_performance_extend.mp4
```

Card join uses the same `concat_xfade_two` path: host performance → provenance/closing card.

---

## 3. Grok Imagine EXTEND — API vs Editor

| Surface | Status (2026-06) |
|---|---|
| **xAI SDK** | `client.video.extend()` is **scriptable** (method exists) |
| **grok-imagine-video-1.5** | Returns `Video extension is not supported for this model` |
| **grok-imagine-video-1.5-preview** | Same rejection in testing |
| **grok-imagine-video** (legacy) | Extend requires xAI-hosted `video_url` from prior `generate` — not local files |
| **Grok Imagine UI** | Editor **Continue/Extend** may work before API parity on 1.5 |

**Pipeline behavior:** `render_longform.py --seamless` attempts EXTEND after first `generate`; on model rejection, auto-falls back to frame-chain i2v with identical prompt contract. Finding is recorded in `extend_state.json` and `qa_report.json` → `extend_api`.

---

## 4. CLI

```powershell
python DAVID/scripts/render_longform.py scripts/longform_scripts/david_intro_60s_v2_script.json --seamless --match-color --cut-on-motion
python DAVID/scripts/render_longform.py <script.json> --seamless --concat-only
```

| Flag | Effect |
|---|---|
| `--seamless` | EXTEND-primary; frame-chain + xfade chain for joins |
| `--match-color` | Histogram match before each join |
| `--cut-on-motion` | Trim tail stillness before each join |
| `--xfade SEC` | Crossfade duration (default **0.2**) |

---

## 5. Deliverables per production

| Artifact | Path |
|---|---|
| Final MP4 | `productions/<slug>_longform_v1/output/david_<slug>_seamless_v1.mp4` |
| v1 comparison | `output/david_<slug>_v1_vs_v2.mp4` (when `config.compare_v1` set) |
| QA report | `qa_report.json` |
| Extend state | `shots/extend_state.json` |
| Manifest | `manifest.json` |

---

## Version History

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-06-19 | Canonical schema + seamless flags + EXTEND API finding |