# Music Bed Clearance SOP
**Channel:** DAVID · The Archive  
**Version:** 1.0 · 2026-06-19  
**T-Ticket:** T5 #143  

---

## Purpose

This SOP covers how Benjamin downloads, confirms, and stamps each music bed from `Music_Bed_Manifest.json`. One page. Follow in order.

---

## Step 1 — Find the Track

1. Open `Music_Bed_Manifest.json` and locate the bed by `bed_id`.
2. Copy the `search_query` value.
3. Navigate to the `source_url` listed for that bed.
4. Paste the search query. Browse results. Select a track that matches:
   - Mood/atmosphere described in `mood_tags`
   - Approximate BPM (±10 is fine)
   - Duration at or beyond `duration_target`

---

## Step 2 — Download Checklist

Before downloading, verify all of the following:

- [ ] **License confirmed** — the track's license on the source page matches the `license` field in the manifest (CC0, CC BY 4.0, Public Domain, or YouTube Audio Library Free)
- [ ] **Attribution check** — if `attribution_required: true`, note the exact artist name and track title for the `attribution_line`
- [ ] **File format** — download MP3 or WAV; minimum 128 kbps (320 kbps or WAV preferred)
- [ ] **Duration** — file is at or above `duration_target`
- [ ] **No vocals** — confirm the track is instrumental only

---

## Step 3 — Store the File

Save the downloaded file to:

```
STUDIO/Art_Department/Music/Beds/{bed_id}.mp3
```

**Example:** `STUDIO/Art_Department/Music/Beds/MB-DOC-001.mp3`

Rename the file to the `bed_id` slug exactly. Do not keep the source platform's filename.

---

## Step 4 — Update the Manifest

Open `Music_Bed_Manifest.json`. For the bed you just cleared, update:

```json
{
  "clearance_status": "CLEARED",
  "cleared_date": "YYYY-MM-DD",
  "cleared_by": "Benjamin Cartwright"
}
```

If `attribution_required: true`, also update `attribution_line` with the actual track title filled in:

```json
"attribution_line": "Music: Dystopia by Kevin MacLeod — incompetech.com (CC BY 4.0)"
```

---

## Step 5 — Stamp the Script

Open the episode's `script.json` (path: `DAVID/scripts/longform_scripts/{slug}_script.json`).

Add the `music_bed_id` under `intake`:

```json
{
  "intake": {
    "music_bed_id": "MB-DOC-001",
    "music_attribution": "Music: Dystopia by Kevin MacLeod — incompetech.com (CC BY 4.0)"
  }
}
```

Set `music_attribution` to `null` for CC0, Public Domain, or YouTube Audio Library beds (no attribution required).

This stamp is what the Legal Gate's `row_music_clearance` check reads. A non-null `music_bed_id` in the brief/script text returns GREEN.

---

## Step 6 — Attribution in Upload Kit (CC BY beds only)

For beds where `attribution_required: true` (currently: MB-DOC-001, MB-EXP-001):

When uploading to YouTube Studio, paste the `attribution_line` at the **bottom of the video description**, below the main body and above the CTA. Format:

```
──────────────────────────
Music: [track title] by Kevin MacLeod — incompetech.com (CC BY 4.0)
```

The `music_attribution` field in the episode's `_upload_kit.json` carries this line automatically once stamped into `script.json`.

---

## Gate 0 Integration

The Legal Gate checks `row_music_clearance`. Status:

| Condition | Gate Row Result |
|-----------|-----------------|
| `music_bed_id` is present in the brief/script | GREEN (non-fatal) |
| `music_bed_id` absent | YELLOW — warning, not a hard stop |

YELLOW is not fatal. A missing music bed will not block production. But the bed must be assigned and cleared **before upload**.

---

## Quick Reference — Clearance Status Values

| Status | Meaning |
|--------|---------|
| `PENDING_DOWNLOAD` | Not yet sourced. Benjamin needs to download and confirm. |
| `CLEARED` | Downloaded, confirmed, manifest updated, script stamped. Ready for use. |

---

*STUDIO · Art_Department · Music · DAVID channel · T5 #143*
