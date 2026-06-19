# STUDIO Long-Form Video Assembly
**Technique v1.0** | June 2026  
**Home:** STUDIO/Techniques (cinematic technique + production method)  
**Pipeline owner:** DAVID (`DAVID/scripts/render_longform.py`)  
**Canon cross-ref:** STUDIO Production Canon §9 (multi-phase sequencing)

---

## 1. Principle — No Real Length Limit

The **30-second cap applies per Grok Imagine clip**, not per finished video.

Every DAVID video shipped so far was already long-form assembly:

| Deliverable | Shots | Per-shot duration | Concat total |
|---|---|---|---|
| Latin sample (#41) | 6 + provenance | 6–10s | ~41s |
| Gothic sample (#41) | 6 + provenance | 6–10s | ~41s |
| Post 1 PIE hybrid (#70) | 5 + provenance | 5–15s | ~49s |
| Host identity test (#69) | 2 | 8–10s | ~18s |

**Method:** generate many short clips → stitch with **ffmpeg concat** → one MP4.

Want **3 minutes**? Generate ~18–30 short shots (6–10s each) and concatenate.  
The real costs are **generation time** and **QA**, not a technical wall.

---

## 2. Production Method

```
script.json (shots[] + config + provenance)
    │
    ├─► Lock refs: avatar @2, set @1, voice suffix (identity_lock.json)
    │
    ├─► FOR each shot in shots[]:
    │       image_url = locked avatar (or per-shot override)
    │       grok-imagine-video-1.5 @ duration, 720p, 16:9
    │       cache → productions/<slug>/shots/<id>.mp4
    │
    ├─► Render provenance card (PIL PNG → ffmpeg still video)
    │
    └─► ffmpeg concat demuxer → output/<slug>_longform_v1.mp4
            + imagine_pack.json + qa_report.json + manifest.json
```

**One command:**

```powershell
python DAVID/scripts/render_longform.py DAVID/scripts/longform_scripts/<script>.json
```

**Reuse cached shots on re-run** (skip generation if `shots/<id>.mp4` exists and size > 10 KB).

**Concat-only reassembly** (no API):

```powershell
python DAVID/scripts/render_longform.py <script.json> --concat-only
```

---

## 3. Consistency Rules — One Piece, Many Shots

Long videos only look coherent when references are locked **before** shot generation.

| Lock | Source | Reuse rule |
|---|---|---|
| **Avatar @2** | `david_identity_lock.json` → `david_avatar_reference.jpg` + URL | Every host shot uses same `image_url` as frame-1 reference |
| **Set @1** | `archive_set_reference.jpg` | Prompt every host shot with Archive desk, brass lamp, codex — same environment plate |
| **Voice suffix** | `identity_lock.voice.prompt_suffix` | Append to every `video_prompt`; never change mid-video |
| **Synthetic only** | Character spec | `synthetic host only`, `no real person likeness` in every prompt |
| **Honesty labels** | Per-shot `on_screen_labels` | RECONSTRUCTED / ATTESTED / NOT ATTESTED carried per shot; provenance card at end |

**Do not** swap avatar references mid-assembly. **Do not** change voice register between shots.  
If a shot drifts, regenerate **that shot only** (`--force-shot <id>`), then re-concat.

---

## 4. Script JSON Schema (imagine-pack compatible)

```json
{
  "slug": "proto-indo-european-deep-dive",
  "title": "DAVID — The Mother Tongue (deep dive)",
  "production_dir": "optional/override/path",
  "config": {
    "model_video": "grok-imagine-video-1.5",
    "resolution": "720p",
    "aspect_ratio": "16:9",
    "identity_lock": "productions/host_identity_v1/david_identity_lock.json",
    "voice_suffix": "mid-low resonant unhurried voice, precise diction, documentary gravitas, synthetic host only"
  },
  "shots": [
    {
      "id": "01_host_hook",
      "duration": 8,
      "video_prompt": "…",
      "speech_text": "…",
      "on_screen": "…",
      "on_screen_labels": ["RECONSTRUCTED language"],
      "role": "host"
    }
  ],
  "provenance_card": {
    "enabled": true,
    "duration_s": 7,
    "banner": "RECONSTRUCTED — NOT ATTESTED",
    "title": "DAVID · PROVENANCE",
    "subtitle": "…",
    "lines": ["TEXT [reconstructed]: …", "CITATION: …"],
    "footer": "reconstructed text · reconstructed pronunciation"
  },
  "provenance": { "text": "…", "citation": "…" },
  "qa_rules": {
    "require_identity_lock": true,
    "require_synthetic_guard": true,
    "min_shots": 1
  }
}
```

Legacy scripts (`post01_pie_script_final.json` format) are auto-normalized by `render_longform.py`.

---

## 5. Two- to Three-Minute Recipe

| Target | Shots | Avg duration | Provenance | Total |
|---|---|---|---|---|
| **2 min** | 14–16 | 7–8s | 7s | ~115–135s |
| **2.5 min** | 16–18 | 7–8s | 7s | ~125–150s |
| **3 min** | 18–22 | 7–8s | 7s | ~135–180s |

**Beat structure (documentary / DAVID):**

1. Cold open hook (1 shot, 6–8s)
2. Problem statement — signature beat (1 shot, 5–8s)
3. Core content blocks (8–14 shots, 6–10s each) — one idea per shot
4. Method / honesty beat (1–2 shots) — comparative method, uncertainty
5. Tagline close (1 shot, 6s)
6. Provenance card (code-rendered, 7s)

**Prompt discipline:** one spoken idea per shot; lip-synced delivery in `video_prompt`;  
never stack two teaching beats in one generation call.

---

## 6. ffmpeg Concat Reference

Concat demuxer (stream copy — fast, lossless join):

```bash
# concat_list.txt — one absolute path per line:
file 'C:/path/to/shots/01_host_hook.mp4'
file 'C:/path/to/shots/02_host_question.mp4'
file 'C:/path/to/shots/provenance.mp4'

ffmpeg -y -f concat -safe 0 -i concat_list.txt -c copy output.mp4
```

Provenance still → video:

```bash
ffmpeg -y -loop 1 -i provenance_card.png -c:v libx264 -t 7 \
  -pix_fmt yuv420p -vf scale=1280:720 provenance.mp4
```

`render_longform.py` uses `imageio-ffmpeg` when system `ffmpeg` is not on PATH.

---

## 7. QA Checklist (per assembly)

- [ ] Identity lock status = `LOCKED`
- [ ] Every host shot prompt contains voice suffix + `synthetic host only`
- [ ] Reconstructed content shots carry `RECONSTRUCTED` + `NOT ATTESTED` labels where required
- [ ] All `shots/<id>.mp4` present before concat
- [ ] Provenance card lines match script `provenance` block
- [ ] Final duration ≈ sum(shots) + provenance (±2s)
- [ ] Re-run reuses cache; only `--force-shot` regenerates

---

## 8. Downstream Reuse

Same pipeline serves:

- **DAVID** language episodes (attested + reconstructed)
- **Stonebridge** client explainers (host + provenance card pattern)
- **STUDIO** narrative pieces (swap avatar lock for actor @2; keep concat method)

---

## Version History

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-06-18 | Initial technique doc; pairs with `render_longform.py` |