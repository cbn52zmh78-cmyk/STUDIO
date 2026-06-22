# Gate 0 — DAVID Channel Launch Checklist
**Channel:** DAVID · The Archive | Upon Tyne Productions  
**Task:** T4 #142  
**Date:** 2026-06-19  
**Status:** Pre-launch verification — complete every section before first upload

Run `python STUDIO/Pipeline/verify_gate_0.py` to auto-check sections A and B.  
Sections C–E are manual (Benjamin at the terminal / browser).

---

## A. Legal / Compliance Gate (codebase — verify without YouTube)

### A1. § 2257 Statement in legal_gate.py
- [ ] `SECTION_2257_STATEMENT` constant exists in `artifacts/legal/legal_gate.py` and is non-empty  
      *(confirmed at line 158 — "18 U.S.C. § 2257 Record-Keeping Requirements Compliance Statement…")*
- [ ] `get_2257_statement()` helper function is present in `artifacts/legal/legal_gate.py`  
      *(confirmed at line 168)*
- [ ] `GateResult.section_2257` field is populated when `has_performers=True`  
      *(confirmed at line 199 of GateResult dataclass; set in `review()` at line 502)*

### A2. Gate 0 Hard Stop in consume_ai_handoff.py
- [ ] `raise ValueError` block gated on `"blocked"` / `"RED"` verdict exists in `STUDIO/Pipeline/consume_ai_handoff.py`  
      *(confirmed lines 317–323: `if _gate_result.get("blocked") or _gate_result.get("verdict") == "RED": raise ValueError(…)`)*
- [ ] The raise is unconditional — pipeline does NOT silently continue on RED  
      *(confirmed: no fallback, no `continue`, no flag suppression)*

### A3. Age Policy
- [ ] `Age_Policy_Locked.md` exists  
      **Actual path:** `STUDIO/research/Age_Policy_Locked.md`  
      *(Note: NOT under Cast/Casting_Bible — it lives in research/)*

### A4. Reroll Queue — Actor Registry Status
All 5 actors in `STUDIO/Cast/Casting_Bible/registry/REROLL_QUEUE.md` must have `agency_status: "do_not_cast_pending_reroll"` in `magazine_casting_registry.json`.

| Actor ID | Status in Registry | OK? |
|---|---|---|
| ValentinaRossiMag-001 | `do_not_cast_pending_reroll` | ✅ |
| LioraVossMag-001 | `do_not_cast_pending_reroll` | ✅ |
| SofiaAlvarezMag-001 | `do_not_cast_pending_reroll` | ✅ |
| NadiaOkoroMag-001 | `do_not_cast_pending_reroll` | ✅ |
| ZaraKhanMag-001 | **NOT FOUND in magazine_casting_registry.json** | ⚠️ |

- [ ] All 4 present actors confirm `do_not_cast_pending_reroll`
- [ ] **ACTION REQUIRED:** `ZaraKhanMag-001` (Zara Khan) is in `REROLL_QUEUE.md` but absent from `magazine_casting_registry.json` (the file has a JSON parse error at line 394, col 24 — likely an unterminated string truncating the file). Add Zara Khan to the registry with `agency_status: "do_not_cast_pending_reroll"` and fix the JSON.
- [ ] No actor with `agency_status: "do_not_cast_pending_reroll"` appears in any active production script in `STUDIO/Productions/` or `DAVID/productions/`  
      *(scan returned zero matches — currently clean)*

---

## B. Channel Identity / Upload Kit (verify before going live)

### B1. channel_identity.json
File: `STUDIO/Art_Department/Brand_Kit/channel_identity.json`

- [ ] `company` — non-empty  
      *(value: "Upon Tyne Productions")*
- [ ] `channel_name` — non-empty  
      *(value: "DAVID")*
- [ ] `channel_badge` — non-empty  
      *(value: "DAVID · The Archive")*
- [ ] `ai_disclosure` — non-empty  
      *(value: "DAVID is a synthetic AI host. No real persons depicted. Produced by Upon Tyne Productions.")*
- [ ] `section_2257` — non-empty  
      *(value: "18 U.S.C. § 2257: All performers are synthetic AI characters, unambiguously 21+…")*

### B2. Latin Launch Episode Upload Kit
File: `DAVID/productions/david_latin_corpus_v1_longform_v1/upload_kit/david_latin_corpus_v1_upload_kit.json`

- [ ] File exists
- [ ] `youtube_title` present and non-empty  
      *(value: "DAVID — Why Latin Never Really Died")*
- [ ] `youtube_description` present and non-empty
- [ ] `chapters` present and non-empty (9 chapter entries confirmed)
- [ ] `youtube_tags` (field name in file: `youtube_tags`) present and non-empty
- [ ] `ai_disclosure_card` present and non-empty
- [ ] `section_2257_note` present and non-empty
- [ ] `youtube_description` contains "AI" or "synthetic" — **YES** ("AI-generated synthetic performers")
- [ ] Gate summary: `verdict: "GREEN"`, `blocked: false`

### B3. Thumbnail Specs
File: `STUDIO/Art_Department/Thumbnails/thumbnail_specs.json`

- [ ] File exists
- [ ] Contains ≥ 12 specs  
      *(current count: **18** entries — 6 DAVID dead-language eps + 3 lane samples × 2 variants + individual episode spec files also present in Thumbnails/)*

---

## C. YouTube Studio Steps (Benjamin — at browser)

Work through YouTube Studio at [studio.youtube.com](https://studio.youtube.com).

### C1. Channel Identity
- [ ] Channel name set to **DAVID** (or "DAVID · The Archive" if handle is separate)
- [ ] Channel handle set — e.g. `@DAVIDtheArchive` or `@DAVIDArchive` (your choice; check availability first)
- [ ] About section: paste the **Short Version** from `STUDIO/Art_Department/Brand_Kit/About_Copy.md`  
      *(~620 chars — well within YouTube's 1,000-char limit; count before pasting)*

### C2. Channel Art
- [ ] **Banner:** generate from Prompt 1 in `STUDIO/Art_Department/Brand_Kit/Grok_Imagine_Prompts.md`, upload at 2560 × 1440 px (YouTube recommended)
- [ ] **Profile logo:** generate from Prompt 2 in `Grok_Imagine_Prompts.md`, upload as 800 × 800 px square
- [ ] **Branding watermark:** check `STUDIO/Art_Department/Brand_Kit/Asset_Spec_Sheet.md` — add if a watermark spec is defined there

### C3. Default Upload Settings
In YouTube Studio → Settings → Upload defaults:
- [ ] Category: **Education**
- [ ] Language: **English**
- [ ] License: **Standard YouTube License**
- [ ] Comments: your choice (recommended: enabled, hold for review)

### C4. AI-Generated Content Disclosure (per video)
For every uploaded DAVID episode:
- [ ] In the upload flow → "Details" step → tick **"Contains AI-generated content"** toggle
- [ ] Confirm the disclosure label appears on the published video's page

### C5. § 2257 Compliance Statement Placement
The `section_2257_note` from the upload kit must be visible to viewers. Two approaches — pick one and apply consistently:
- **Option A (recommended):** Paste the § 2257 statement as a **pinned comment** on each video immediately after publishing. This keeps the description cleaner.
- **Option B:** Append to the bottom of the YouTube description (below the CTA and separator line). Confirm the full description still renders without truncation (YouTube shows ~280 chars before "Show more").

- [ ] Chosen approach: _________________________ (fill in)
- [ ] Applied consistently to all uploads

### C6. Cards & End Screens
For each episode:
- [ ] Configure end screen per `end_screen` block in the upload kit (`cta_text`, `subscribe_prompt`, `timestamp_s: 47.0` for the Latin ep)
- [ ] Add a Subscribe card at minimum; add video/playlist card if later episodes are live

### C7. Monetization Gate
- [ ] **DO NOT** enable monetization until the channel reaches **1,000 subscribers** and **4,000 watch-hours** (YouTube Partner Programme threshold)
- [ ] Note: monetization application also requires a linked AdSense account — set this up in advance if not already done

---

## D. Gate 0 Smoke Test (run before any real upload)

Run these from the project root (`C:\Users\NCG\Videos\Grok Projects\`).

### D1. Automated Verification
```
python STUDIO/Pipeline/verify_gate_0.py
```
Expected: all checks PASS or expected FAILs noted (e.g. upload kits for unrendered episodes). Exit code 0 = all pass.

```
python STUDIO/Pipeline/verify_gate_0.py --verbose
```
Shows full detail on each check.

### D2. Batch Dry-Run
```
python STUDIO/Pipeline/batch_runner.py --slate dead_languages --dry-run
```
Expected: prints planned run, exits 0, emits no real renders.

### D3. Upload Kit Generation
Upload kits are produced by `package_episode.py`, invoked automatically by `batch_runner.py --package` after render:
```
python STUDIO/Pipeline/package_episode.py --help
```
Confirm the script is present and importable before render day.

### D4. Handoff Smoke Test
To verify Gate 0 blocks correctly on a RED package, run consume_ai_handoff with a synthetic RED test package (do not use a real episode package for this):
```
# Confirm Gate 0 raises ValueError on RED:
python -c "
from STUDIO.Pipeline.consume_ai_handoff import consume_ai_handoff
import json
bad = {'handoff_id':'test','lane':'test','cinematic_style':'test',
       'concept_hint':{'slug':'test','beats':[{}]},
       'provenance':{'source_repo':'x','citations':[],'gate_status':'RED blocked'}}
try:
    consume_ai_handoff(bad)
    print('FAIL — did not block')
except ValueError as e:
    print('PASS — blocked:', str(e)[:80])
"
```

---

## E. Final Gate Sign-Off (Benjamin fills in — date and initials each item)

- [ ] **LLC / entity registered** — Upon Tyne Productions legal entity confirmed and registered in jurisdiction of operation  
      Date confirmed: _______________ / Initials: ___

- [ ] **Monetization policy reviewed** — channel is pre-revenue; YouTube Partner Programme review deferred until thresholds met. Counsel review of revenue policy: _______________

- [ ] **RDP credentials rotated** — `CHANGEME#123!` is **compromised and must be changed before any channel launch**. New credentials set, old credentials invalidated.  
      Date rotated: _______________ / Initials: ___

- [ ] **Git repo private** — FLASH/STUDIO GitHub repository confirmed private; no credentials, API keys, or session tokens committed to history  
      Confirmed: _______________ / Initials: ___

- [ ] **DAVID channel live date confirmed** — gated on:
  - [ ] Issue #218 fix (verify what #218 is and confirm closed)
  - [ ] Latin episode render complete and QC passed
  - [ ] At least one upload kit generated and smoke-tested  
  Target live date: _______________

---

## Quick Reference — Key Paths

| Item | Path |
|---|---|
| Legal gate | `artifacts/legal/legal_gate.py` |
| Gate 0 consumer | `STUDIO/Pipeline/consume_ai_handoff.py` |
| Age policy | `STUDIO/research/Age_Policy_Locked.md` |
| Channel identity | `STUDIO/Art_Department/Brand_Kit/channel_identity.json` |
| About copy | `STUDIO/Art_Department/Brand_Kit/About_Copy.md` |
| Brand prompts | `STUDIO/Art_Department/Brand_Kit/Grok_Imagine_Prompts.md` |
| Thumbnail specs | `STUDIO/Art_Department/Thumbnails/thumbnail_specs.json` |
| Reroll queue | `STUDIO/Cast/Casting_Bible/registry/REROLL_QUEUE.md` |
| Casting registry | `STUDIO/Cast/Casting_Bible/registry/magazine_casting_registry.json` |
| Latin upload kit | `DAVID/productions/david_latin_corpus_v1_longform_v1/upload_kit/david_latin_corpus_v1_upload_kit.json` |
| Verify script | `STUDIO/Pipeline/verify_gate_0.py` |

---

*Generated by NEXUS AI — T4 #142 · Gate 0 verify · 2026-06-19*
