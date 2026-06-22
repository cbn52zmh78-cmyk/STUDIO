# STUDIO: Concept → Upload-Ready Kit — Operator Flow

**Status:** COMPLETE pipeline. All stages wired as of 2026-06-19.  
**Author:** T1 #139  

---

## Overview

```
concept.json
    ↓  batch_runner.py run
intake (Gate 0)
    ↓  render_longform.py  [480p draft]
production dir / manifest.json
    ↓  batch_runner.py promote
720p final render
    ↓  package_episode.py  (via --package or `batch package` subcommand)
upload_kit/
    ├── video/        ← final MP4 copy
    ├── seo/          ← title, description, tags (YouTube-ready)
    ├── chapters/     ← timestamp chapter markers
    ├── end_screen/   ← end-screen element config
    ├── thumbnail/    ← candidate frames + THUMBNAIL_BRIEF.json
    └── CHECKLIST.md  ← step-by-step upload checklist
```

---

## Stage 1 — Concept → Draft (480p)

```bash
# Dry-run: intake only, no render, manifest written
python DAVID/scripts/batch_runner.py run STUDIO/Pipeline/Concepts/dead_languages --dry-run

# Real draft render with immediate packaging:
python DAVID/scripts/batch_runner.py run STUDIO/Pipeline/Concepts/dead_languages --package
```

**What happens:**
1. Each `*.concept.json` → Gate 0 (legal/compliance check)
2. RED gate = skipped; GREEN/signoff-required = continues
3. Script JSON written to `DAVID/batches/<batch-id>/scripts/<slug>_480p_script.json`
4. `render_longform.py` called at 480p (draft quality)
5. QA report auto-read from production dir
6. `--package` flag: `package_episode.package_production()` called per passing episode → `upload_kit/` built in production dir

**Output:** `DAVID/batches/<batch-id>/manifest.json`

---

## Stage 2 — Draft Approval → 720p Final

```bash
# Promote all passing drafts to 720p (Benjamin greenlight required for API spend)
python DAVID/scripts/batch_runner.py promote DAVID/batches/<batch-id>/manifest.json

# Promote with packaging:
python DAVID/scripts/batch_runner.py promote DAVID/batches/<batch-id>/manifest.json --package
```

**What happens:**
1. Reads `manifest.json` for `promote_eligible=true` items
2. Writes `<slug>_720p_script.json` (resolution patched)
3. Full render at 720p with `--seamless --match-color --cut-on-motion`
4. QA gate re-confirmed
5. `--package` flag: upload kit built from 720p output

**Output:** `DAVID/batches/<batch-id>/manifest_final_720p.json`

---

## Stage 3 — Package (standalone, post-render)

Run packaging after the fact on any completed batch:

```bash
# Package all pass/promoted items in a manifest
python DAVID/scripts/batch_runner.py package DAVID/batches/<batch-id>/manifest.json

# Package even without QA pass (for manual override)
python DAVID/scripts/batch_runner.py package DAVID/batches/<batch-id>/manifest.json --allow-fail-qa

# Package a single known production dir directly
python STUDIO/Pipeline/package_episode.py DAVID/productions/<slug>_longform_v1/
```

**Output:** `DAVID/batches/<batch-id>/manifest_package.json` listing each episode's upload kit path.

---

## Upload Kit Structure

Each `<production_dir>/upload_kit/` contains:

| Path | Contents |
|------|----------|
| `video/<slug>.mp4` | Final MP4 (copy of render output) |
| `seo/title.txt` | YouTube title (≤100 chars) |
| `seo/description.txt` | Full description with chapters + disclosure embedded |
| `seo/tags.txt` | Comma-separated tags (≤30) |
| `seo/seo.json` | Full SEO object (title, description, tags, category, playlist) |
| `chapters/youtube_chapters.txt` | `MM:SS Label` lines, paste into description |
| `chapters/chapters.json` | Chapter objects with shot IDs and start times |
| `end_screen/end_screen.json` | End-screen element config for YouTube Studio |
| `thumbnail/THUMBNAIL_BRIEF.json` | T2 thumbnail spec: prompt, overlays, design notes |
| `thumbnail/candidate_peak_frame.jpg` | Extracted peak-moment frame (primary thumbnail candidate) |
| `thumbnail/candidate_establishing_frame.jpg` | Alternate candidate |
| `CHECKLIST.md` | ☑ step-by-step upload checklist |
| `manifest.json` | Machine-readable kit manifest |

---

## Channel Export Bundle

To bundle all upload kits from a batch into one ready-to-upload folder:

```bash
# Creates: DAVID/batches/<batch-id>/channel_export/
python STUDIO/Pipeline/channel_export.py DAVID/batches/<batch-id>/manifest_package.json
```

*(See `channel_export.py` — T1 #139 second deliverable.)*

---

## Key Flags Reference

| Flag | Stage | Effect |
|------|-------|--------|
| `--dry-run` | run | Intake + manifest only; no API render |
| `--package` | run, promote | Package each episode after successful render |
| `--allow-fail-qa` | run, promote, package | Package even if QA=FAIL (manual override) |
| `--no-seamless` | run, promote | Skip seamless/color-match flags (faster) |
| `--slug <slug>` | promote | Promote a single episode only |

---

## Hard Rails (always enforced)

- `--seamless` render slate = **Benjamin's spend call only**. Dry-run and script-only passes are always safe.
- `--package` without a prior render = gracefully skipped (no MP4 = `skipped_no_mp4`).
- QA gate required before packaging by default; `--allow-fail-qa` is a named override.
- Upload kit = local artifact only. **Nothing leaves the machine** without explicit publish approval.

---

*Last updated: 2026-06-19 (T1 #139)*
