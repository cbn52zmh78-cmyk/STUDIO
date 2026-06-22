# DAVID · The Archive — Music Bed Library
**Version:** 1.0  
**Created:** 2026-06-19  
**Scope:** DAVID channel dead-language slate · Upon Tyne Productions  
**T-Ticket:** T5 #143

---

## Overview

This library specifies 9 cleared music beds for the DAVID channel — 3 lanes × 3 beds. All beds are sourced from royalty-free or public-domain libraries only (CC0, CC BY 4.0, Public Domain, or YouTube Audio Library free tier). No copyrighted music. No sync licenses required.

**Channel aesthetic:** Atmospheric, scholarly, cinematic. Parchment. Candlelight. Ancient stone. Not pop. Not upbeat. Think: a manuscript in a cold room.

**Source directories authorised for this slate:**
- [Pixabay Music](https://pixabay.com/music/) — CC0, no attribution required
- [Free Music Archive](https://freemusicarchive.org/) — filter to CC0 only
- [YouTube Audio Library](https://studio.youtube.com/channel/music) — free tier, no attribution required
- [Incompetech](https://incompetech.filmmusic.io/) — CC BY 4.0, attribution required (line provided below)
- [Musopen](https://musopen.org/) — public domain classical recordings, no attribution required

**Clearance status on creation:** All beds are `PENDING_DOWNLOAD` — Benjamin must download, confirm the track, and update `Music_Bed_Manifest.json` to `CLEARED`.

---

## Lane Definitions

| Lane Code | Lane Name | Use Case | Sonic Profile |
|-----------|-----------|----------|---------------|
| DOC | `lane_documentary` | Main dead-language episodes (launch + backlog) | Slow orchestral/ambient, minimal percussion, 55–70 BPM |
| EXP | `lane_explainer` | Science/history crossover, linguistics deep-dives | Clean piano or string quartet, slightly more structured, 65–80 BPM |
| CMP | `lane_companion` | Companion content, lighter tone | Gentle, conversational, acoustic warmth, 55–65 BPM |

---

## Lane 1 — `lane_documentary` (DOC)

*Slow, orchestral, ambient. Works under narration without fighting it. Think manuscript libraries and stone corridors.*

---

### MB-DOC-001 — "Parchment Vault — Slow Strings"

| Field | Value |
|-------|-------|
| **bed_id** | `MB-DOC-001` |
| **title** | Parchment Vault — Slow Strings |
| **lane** | `lane_documentary` |
| **source** | Incompetech (Kevin MacLeod) |
| **search_query** | `dark ambient strings orchestral slow documentary` |
| **license** | CC BY 4.0 |
| **attribution_required** | true |
| **attribution_line** | `Music: [track title] by Kevin MacLeod — incompetech.com (CC BY 4.0)` |
| **mood_tags** | dark, orchestral, slow, atmospheric, scholarly, cinematic |
| **bpm_approx** | 62 |
| **duration_target** | loopable |
| **clearance_status** | PENDING_DOWNLOAD |

**Notes:** Incompetech has a strong catalogue of slow documentary strings. Search the genre "Documentary" + mood "Dark". Typical match: "Dystopia" or "Invariance" (verify title before use; use whatever matches the query above).

---

### MB-DOC-002 — "Clay Tablet — Ambient Drone"

| Field | Value |
|-------|-------|
| **bed_id** | `MB-DOC-002` |
| **title** | Clay Tablet — Ambient Drone |
| **lane** | `lane_documentary` |
| **source** | Pixabay Music |
| **search_query** | `ambient dark documentary atmospheric orchestral` |
| **license** | CC0 |
| **attribution_required** | false |
| **attribution_line** | null |
| **mood_tags** | dark, ambient, drone, atmospheric, ancient, cinematic |
| **bpm_approx** | 58 |
| **duration_target** | loopable |
| **clearance_status** | PENDING_DOWNLOAD |

**Notes:** Pixabay Music category "Cinematic" → subcategory "Ambient" or "Dramatic". Filter results by "Documentary" keyword. Look for slow, pad-heavy tracks with minimal beats, 2:00+ duration. CC0 confirmed at point of download.

---

### MB-DOC-003 — "Stone Archive — Minimal Orchestra"

| Field | Value |
|-------|-------|
| **bed_id** | `MB-DOC-003` |
| **title** | Stone Archive — Minimal Orchestra |
| **lane** | `lane_documentary` |
| **source** | Free Music Archive (CC0 only) |
| **search_query** | `ambient orchestral slow documentary CC0` |
| **license** | CC0 |
| **attribution_required** | false |
| **attribution_line** | null |
| **mood_tags** | orchestral, minimal, slow, scholarly, archive, atmospheric |
| **bpm_approx** | 65 |
| **duration_target** | loopable |
| **clearance_status** | PENDING_DOWNLOAD |

**Notes:** On FMA, set filter "License: CC0". Search genre "Classical/Ambient". Look for tracks under the artists Kai Engel, Dee Yan-Key, or similar FMA CC0 specialists. Confirm CC0 on the track page before downloading.

---

## Lane 2 — `lane_explainer` (EXP)

*More structured than documentary lane — clean piano or string quartet. Supports analytical narration and visual comparisons. Still scholarly; never pop.*

---

### MB-EXP-001 — "Scholar's Desk — Piano & Strings"

| Field | Value |
|-------|-------|
| **bed_id** | `MB-EXP-001` |
| **title** | Scholar's Desk — Piano & Strings |
| **lane** | `lane_explainer` |
| **source** | Incompetech (Kevin MacLeod) |
| **search_query** | `piano strings quartet gentle scholarly educational documentary` |
| **license** | CC BY 4.0 |
| **attribution_required** | true |
| **attribution_line** | `Music: [track title] by Kevin MacLeod — incompetech.com (CC BY 4.0)` |
| **mood_tags** | piano, strings, gentle, scholarly, educational, clean |
| **bpm_approx** | 72 |
| **duration_target** | loopable |
| **clearance_status** | PENDING_DOWNLOAD |

**Notes:** Incompetech genre "Documentary" + mood "Peaceful" or "Hopeful". Good Incompetech matches: "Ossuary 6 — Air" or "Prelude and Action" (verify). Piano-led with light string accompaniment preferred.

---

### MB-EXP-002 — "Archive Keys — Solo Piano"

| Field | Value |
|-------|-------|
| **bed_id** | `MB-EXP-002` |
| **title** | Archive Keys — Solo Piano |
| **lane** | `lane_explainer` |
| **source** | Musopen |
| **search_query** | `solo piano nocturne calm classical public domain` |
| **license** | Public Domain |
| **attribution_required** | false |
| **attribution_line** | null |
| **mood_tags** | piano, solo, classical, nocturne, calm, reflective |
| **bpm_approx** | 68 |
| **duration_target** | 2:00+ |
| **clearance_status** | PENDING_DOWNLOAD |

**Notes:** Musopen hosts public-domain recordings of classical works. Search for Chopin nocturnes, Debussy preludes, or Satie Gymnopédies (all public domain). Confirm the *recording* is also public domain (Musopen recordings are, by default). Download MP3 at highest quality available.

---

### MB-EXP-003 — "Inquiry — String Quartet"

| Field | Value |
|-------|-------|
| **bed_id** | `MB-EXP-003` |
| **title** | Inquiry — String Quartet |
| **lane** | `lane_explainer` |
| **source** | YouTube Audio Library |
| **search_query** | `string quartet gentle light documentary` |
| **license** | YouTube Audio Library Free |
| **attribution_required** | false |
| **attribution_line** | null |
| **mood_tags** | string quartet, gentle, light, documentary, classical |
| **bpm_approx** | 75 |
| **duration_target** | loopable |
| **clearance_status** | PENDING_DOWNLOAD |

**Notes:** In YouTube Studio → Audio Library → filter Genre: "Classical" + Mood: "Calm" or "Inspirational". Download directly from YouTube Studio. Note: YouTube Audio Library tracks are free to use in YouTube-uploaded content; usage outside YouTube may require additional licensing — use only for DAVID YouTube uploads.

---

## Lane 3 — `lane_companion` (CMP)

*Gentle, conversational, understated. Supports a quieter register — not cinematic, not academic. Feels like sitting with someone thoughtful.*

---

### MB-CMP-001 — "Study Light — Acoustic Warmth"

| Field | Value |
|-------|-------|
| **bed_id** | `MB-CMP-001` |
| **title** | Study Light — Acoustic Warmth |
| **lane** | `lane_companion` |
| **source** | Pixabay Music |
| **search_query** | `acoustic guitar soft gentle calm warm background` |
| **license** | CC0 |
| **attribution_required** | false |
| **attribution_line** | null |
| **mood_tags** | acoustic, guitar, warm, gentle, calm, conversational |
| **bpm_approx** | 62 |
| **duration_target** | loopable |
| **clearance_status** | PENDING_DOWNLOAD |

**Notes:** Pixabay category "Acoustic" or "Folk/Acoustic". Avoid anything with singing, percussion kit, or synth bass. Fingerpicked acoustic guitar with light pad or piano preferred. 2:00+ preferred for loop use.

---

### MB-CMP-002 — "Evening Notes — Minimal Piano"

| Field | Value |
|-------|-------|
| **bed_id** | `MB-CMP-002` |
| **title** | Evening Notes — Minimal Piano |
| **lane** | `lane_companion` |
| **source** | Free Music Archive (CC0 only) |
| **search_query** | `minimal piano gentle ambient warm CC0` |
| **license** | CC0 |
| **attribution_required** | false |
| **attribution_line** | null |
| **mood_tags** | piano, minimal, gentle, warm, ambient, evening |
| **bpm_approx** | 58 |
| **duration_target** | loopable |
| **clearance_status** | PENDING_DOWNLOAD |

**Notes:** FMA CC0 filter, genre "Classical" or "Ambient". Artists like Kai Engel produce exactly this — minimal solo piano beds. Confirm CC0 on track page. Prefer tracks 2:30+ so they loop comfortably under 60–90s companion segments.

---

### MB-CMP-003 — "Quiet Reading — Understated Pad"

| Field | Value |
|-------|-------|
| **bed_id** | `MB-CMP-003` |
| **title** | Quiet Reading — Understated Pad |
| **lane** | `lane_companion` |
| **source** | YouTube Audio Library |
| **search_query** | `ambient pad gentle calm understated background` |
| **license** | YouTube Audio Library Free |
| **attribution_required** | false |
| **attribution_line** | null |
| **mood_tags** | ambient, pad, gentle, calm, understated, background |
| **bpm_approx** | 60 |
| **duration_target** | loopable |
| **clearance_status** | PENDING_DOWNLOAD |

**Notes:** YouTube Studio Audio Library → Genre: "Ambient" → Mood: "Calm". Select tracks with no percussion and no melodic hooks — pure background pad is ideal. Same YouTube-only usage restriction as MB-EXP-003.

---

## Summary Table

| bed_id | Title | Lane | Source | License | Attribution |
|--------|-------|------|--------|---------|-------------|
| MB-DOC-001 | Parchment Vault — Slow Strings | lane_documentary | Incompetech | CC BY 4.0 | Required |
| MB-DOC-002 | Clay Tablet — Ambient Drone | lane_documentary | Pixabay Music | CC0 | No |
| MB-DOC-003 | Stone Archive — Minimal Orchestra | lane_documentary | Free Music Archive | CC0 | No |
| MB-EXP-001 | Scholar's Desk — Piano & Strings | lane_explainer | Incompetech | CC BY 4.0 | Required |
| MB-EXP-002 | Archive Keys — Solo Piano | lane_explainer | Musopen | Public Domain | No |
| MB-EXP-003 | Inquiry — String Quartet | lane_explainer | YouTube Audio Library | YT Free | No |
| MB-CMP-001 | Study Light — Acoustic Warmth | lane_companion | Pixabay Music | CC0 | No |
| MB-CMP-002 | Evening Notes — Minimal Piano | lane_companion | Free Music Archive | CC0 | No |
| MB-CMP-003 | Quiet Reading — Understated Pad | lane_companion | YouTube Audio Library | YT Free | No |

---

*STUDIO · Art_Department · Music · DAVID channel — T5 #143*  
*Clearance SOP: see `Clearance_SOP.md` in this directory*  
*Machine manifest: see `Music_Bed_Manifest.json` in this directory*  
*Episode assignments: see `Episode_Music_Assignments.md` in this directory*
