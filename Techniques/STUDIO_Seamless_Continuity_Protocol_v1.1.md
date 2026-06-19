# STUDIO Seamless Continuity Protocol v1.1
**Technique v1.1** | June 2026  
**Pairs with:** `STUDIO_LongForm_Video_Assembly_v1.md` · `DAVID/scripts/render_longform.py --seamless`

---

## 1. Priority Stack

| Tier | Method | When |
|---|---|---|
| **PRIMARY** | Grok Imagine **EXTEND** (`client.video.extend`) | Same scene / same take — host continues speaking; no cut to mask |
| **JOINS** | Frame-chain + **0.2s xfade** + **acrossfade** | Scene change or non-video insert (closing/provenance card) |
| **Pre-join** | **`--match-color`** histogram match | Always before a frame-chain join |
| **Hard cut** | **`--cut-on-motion` only** | Gesture peak — never on stillness / dead frame |

---

## 2. Per-Shot Prompt Contract

Every generated segment carries:

**Continuity prefix (locked ref):**
```
CONTINUITY LOCK @David-001: identical host face, charcoal sweater, Archive desk,
brass lamp, same eye-line — seamless continuation of prior take, zero jump cut.
```

**End guard:**
```
Finish on gesture peak (hand motion or lean), never hold dead stillness or dead frame.
```

**Duration:** 7–9s per segment (API clip cap discipline).

**Reference:** `David-001` = `productions/host_identity_v1/david_identity_lock.json` avatar + Archive set.

---

## 3. Extend Chain (PRIMARY)

```
Segment 1: video.generate(image_url=@David-001, duration=7–9s)
Segment 2..N (same scene): video.extend(video_url=prior.url, duration=7–9s)
```

Each extend appends to the **same take** — output is one growing `host_performance.mp4`.

> **API note (2026-06):** `grok-imagine-video-1.5` does not yet expose EXTEND via API.
> `render_longform.py --seamless` auto-falls back to **frame-chain i2v** (last-frame → next
> start-image) with the same continuity-prefix / end-guard contract. Re-test EXTEND when
> xAI enables it on 1.5.

---

## 4. Frame-Chain Join (scene change / card only)

```
1. ffmpeg extract last frame of segment A  →  chain_frame.jpg
2. optional: --match-color segment B to A
3. video.generate(image_url=upload(chain_frame), prompt=segment B)
   OR xfade A + B if B is non-generated (PNG card)
4. xfade=0.2s + acrossfade=0.2s at join
```

**Never** hard-cut on a held still. Use `--cut-on-motion` to trim ~0.15s tail before join when needed.

---

## 5. CLI (`render_longform.py`)

```powershell
python DAVID/scripts/render_longform.py scripts/longform_scripts/david_intro_60s_v2_script.json --seamless
python DAVID/scripts/render_longform.py <script.json> --seamless --match-color --cut-on-motion
python DAVID/scripts/render_longform.py <script.json> --seamless --concat-only
```

| Flag | Effect |
|---|---|
| `--seamless` | Extend chain within scene; frame-chain + xfade for card |
| `--match-color` | Histogram match before frame-chain joins |
| `--cut-on-motion` | Trim tail stillness before joins |
| `--xfade SEC` | Crossfade duration (default **0.2**) |

---

## Version History

| Version | Date | Change |
|---|---|---|
| 1.1 | 2026-06-19 | Extend-primary + frame-chain joins + ffmpeg xfade pipeline |