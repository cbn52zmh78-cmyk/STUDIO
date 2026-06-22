# Music Bed Clearance SOP — Upon Tyne Productions / STUDIO
**ID:** T5 #143  
**Date:** 2026-06-20  
**Owner:** T5 (music) → Hub (clearance decisions) → Benjamin (final publish authorization)  
**Applies to:** All productions under DAVID · The Archive, Observable, Companion Lane, Movies Lane, Explainer Lane

---

## Purpose

This SOP governs how music beds are selected, cleared, assigned, and verified for every production. It exists because:

1. Gate 0 row-2 is a **hard stop** — no unlisted or unverified bed may appear in a published video
2. Music copyright is the most operationally dangerous rights exposure in AI video (composition + master)
3. SPEC_ONLY beds require an approved fallback and explicit commissioning/sourcing before publish

---

## The Two Clearance Sources

All cleared beds must appear in `STUDIO/Music_Sound/clearance_manifest.json`. No bed outside the manifest may be used in any production.

**Cleared status:**
- `"license": "owned"` — Upon Tyne Productions internal score library; fully cleared, all channels
- `"license": "royalty-free"` — perpetual RF license on file (Studio RF pack or equivalent); all channels
- `"license": "CC0"` — Creative Commons CC0 1.0 (public domain dedication); no attribution, all channels

**Not cleared:**
- `"license": "SPEC_ONLY"` — instrumentation spec written, not yet sourced or commissioned; use `fallback_bed_id` at publish

**What is NOT permitted:**
- AI-generated music (xAI, Suno, Udio, etc.) — dilution risk on AI-music copyright (per Intel #205 ruling)
- YouTube Audio Library tracks — licensing is "YT only" by default, does not cover streaming/theatrical
- Tracks heard in a YouTube/TikTok video with no verified license — not cleared by osmosis
- Any track not in the manifest, even if it "seems" royalty-free

---

## Gate 0 Row-2 Check (the machine-enforceable rule)

At production intake, `legal_gate.py` checks: **is the assigned `music_bed_id` present in `clearance_manifest.json`?**

- Listed → row-2 = **PASS** → gate can be GREEN
- Unlisted → row-2 = **RED (HARD STOP)** → gate is RED regardless of other rows

This is enforced in `legal_gate.py` (v1.5 post-#154). The check runs against the `tracks` dict in `clearance_manifest.json`. A SPEC_ONLY bed's `fallback_bed_id` must be the bed assigned at intake — not the spec bed ID — until the spec bed is sourced.

**Correct intake practice for SPEC_ONLY beds:**
```json
"music_bed_id": "BED-ANT-001"  // fallback — NOT "BED-VED-001" (spec)
```
Update the intake to the spec bed ID ONLY AFTER the bed is sourced, manifest updated, and row-2 re-verified.

---

## Assignment Decision Tree

When assigning a music bed to a new production:

```
1. What is the production's LANE?
   → documentary-host (DAVID, history): period or prestige lane beds
   → science explainer (Observable): cosmic-awe, clinical, physics, chemistry, how-it-works
   → companion: soft-warm-companion
   → thriller/narrative: cinematic-thriller
   → product/service explainer: upbeat-explainer

2. What is the episode's ERA or CULTURAL CONTEXT?
   → Mediterranean antiquity (Greek, Roman, Egyptian): period-antiquity
   → Near Eastern / Mesopotamian / Anatolian: period-near-east (fallback: period-antiquity)
   → South Asian / Vedic: period-south-asian (fallback: period-antiquity)
   → East Asian: period-east-asian (fallback: documentary-prestige)
   → Medieval European (500–1500 CE): period-medieval
   → Tudor/Elizabethan: period-tudor
   → Fully reconstructed / no script (PIE): documentary-prestige (archival tone)
   → New World / Mesoamerican: period-mesoamerican once sourced (fallback: documentary-prestige)
   → Undeciphered: period-antiquity matching the cultural region

3. Does the episode have a thematic tone that suggests a specific track?
   → Prestige/archival: BED-DOC-001 "Archive Room"
   → Intellectual argument / method: BED-DOC-002 "Corpus Walk"
   → Fragility / tension / single-witness: BED-THR-001 "Pressure Grid"
   → Drama / dark: BED-THR-002 "Night Ledger"
   → Medieval liturgy / scripture: BED-MED-001 "Scriptorium"
   → Norse / Anglo-Norman: BED-MED-002 "Northumbrian Hearth"
   → Bronze Age / ancient Mediterranean: BED-ANT-001 "Aegean Dusk" or BED-ANT-002 "Temple Column"
   → Tudor court: BED-TUD-001 "Consort Air" or BED-TUD-002 "Virginal Room"

4. Is the assigned bed in the manifest?
   → YES + CLEARED → assign, row-2 = PASS
   → YES + SPEC_ONLY → assign FALLBACK bed at intake; note expansion queue item
   → NO → DO NOT USE; add to manifest before assigning

5. Verify: allowed_channels includes the intended publish channel(s)
   → All current cleared beds allow: social, streaming, theatrical, festival, client ✓
```

---

## Adding a New Bed to the Manifest

Before any new bed can be used in production:

1. **Verify the license:** get written confirmation (downloaded receipt, license PDF, or proof of ownership). For CC0: verify the upload source and stated CC0 1.0 designation.
2. **Add the track entry** to `clearance_manifest.json` under `"tracks"`:
   - Assign next sequential ID in the lane (BED-DOC-003, BED-WARM-003, etc.)
   - Fill ALL required fields: title, lane, mood, file, duration_seconds, bpm, source, license, attribution_required, allowed_channels
   - Set `cue_sheet_path` to the path of the license PDF if applicable
3. **Bump the manifest version** (e.g., 1.5 → 1.6) and update `"updated"` date
4. **Add the lane** to the `"lanes"` array if it's a new lane
5. **Run `legal_gate.py`** to confirm the new bed passes row-2 on a test intake
6. **Commit** the updated manifest to version control before using the bed in production

---

## Sourcing New Beds (for SPEC_ONLY items)

SPEC_ONLY beds in the expansion queue need to be sourced or commissioned before publish. Decision tree:

```
Option A — Commission from a musician (PREFERRED for period-instrument beds):
  → Contact period-instrument composer/performer
  → Negotiate: one-time composition fee + "work for hire" or perpetual all-channel license
  → Get a signed license agreement before using
  → Store license PDF in STUDIO/Music_Sound/licenses/<BED-ID>_license.pdf
  → Update manifest: license="owned", cue_sheet_path=that path

Option B — Source from RF library (Epidemic Sound / Artlist):
  → Search the library for the period/instrument profile in the spec
  → Verify the license covers: YouTube, social, streaming, client use (not "content-ID cleared only")
  → Download the track and license receipt
  → Store track in Music_Beds/<lane>/<BED-ID>.mp3
  → Store receipt in STUDIO/Music_Sound/licenses/<BED-ID>_license.pdf
  → Update manifest: license="royalty-free"

Option C — Source from CC0 (MusOpen, OpenGameArt, Pixabay Music):
  → Verify CC0 1.0 designation explicitly stated by the uploader
  → No attribution required, no commercial restrictions
  → Download and store
  → Update manifest: license="CC0"

AVOID:
  → Anything labeled "free for personal use" (not commercial)
  → YouTube Audio Library (YT-only)
  → AI-generated music (any platform)
  → SoundCloud/Bandcamp without explicit license grant
```

---

## Clearance Checklist (per production, at publish-prep)

Run this before the upload kit is finalized:

```
[ ] music_bed_id in script.json matches a track ID in clearance_manifest.json
[ ] Track license = owned / royalty-free / CC0 (NOT SPEC_ONLY)
[ ] Track's allowed_channels includes all intended publish channels
[ ] license receipt or ownership record is on file (if royalty-free — cue_sheet_path filled)
[ ] Gate 0 row-2 = PASS (confirmed in gate JSON)
[ ] If attribution_required = true: attribution line included in video description
[ ] If bed was recently added: manifest version bumped, commit recorded
```

---

## Assignment Status Summary — T5 #143

| Ep | Slug | Bed | License | Status |
|----|------|-----|---------|--------|
| S1 Ep 1 | david_latin_corpus_v1 | BED-DOC-001 | owned | ✅ CLEARED |
| S1 Ep 2 | david_ancient_greek_corpus_v1 | BED-DOC-002 | owned | ✅ CLEARED |
| S1 Ep 3 | david_old_english_corpus_v1 | BED-DOC-001 | owned | ✅ CLEARED |
| S1 Ep 4 | david_old_norse_corpus_v1 | BED-DOC-002 | owned | ✅ CLEARED |
| S1 Ep 5 | david_gothic_corpus_v1 | BED-THR-001 | owned | ✅ CLEARED |
| S1 Ep 6 | david_sumerian_corpus_v1 | BED-DOC-002 | owned | ✅ CLEARED |
| S1 Ep 7 | david_sanskrit_corpus_v1 | BED-VED-001 → fallback BED-ANT-001 | SPEC/owned | ⏳ SPEC (fallback: BED-ANT-001 cleared) |
| S1 Ep 8 | david_biblical_hebrew_corpus_v1 | BED-ANT-001 | owned | ✅ CLEARED |
| S1 Ep 9 | david_akkadian_corpus_v1 | BED-NEAR-001 → fallback BED-ANT-002 | SPEC/RF | ⏳ SPEC (fallback: BED-ANT-002 cleared) |
| S1 Ep 10 | david_middle_egyptian_corpus_v1 | BED-ANT-002 | royalty-free | ✅ CLEARED |
| S1 Ep 11 | david_classical_nahuatl_corpus_v1 | BED-DOC-001 | owned | ✅ CLEARED (BED-MESOAM-001 expansion queued) |
| S1 Ep 12 | david_old_church_slavonic_corpus_v1 | BED-MED-001 | owned | ✅ CLEARED |
| S2 Ep 13 | david_hittite_corpus_v1 | BED-NEAR-001 → fallback BED-ANT-002 | SPEC/RF | ⏳ PROVISIONAL (concept-only; fallback cleared) |
| S2 Ep 14 | david_classical_japanese_corpus_v1 | BED-EAST-001 → fallback BED-DOC-001 | SPEC/owned | ⏳ PROVISIONAL (concept-only; fallback cleared) |
| S2 Ep 15 | david_etruscan_corpus_v1 | BED-ANT-002 | royalty-free | ⏳ PROVISIONAL (concept-only) |
| S2 Ep 16 | david_proto_indo_european_corpus_v1 | BED-DOC-001 | owned | ⏳ PROVISIONAL (concept-only) |
| S2 Ep 17 | david_linear_a_corpus_v1 | BED-ANT-001 | owned | ⏳ PROVISIONAL (concept-only) |
| S2 Ep 18 | david_coptic_corpus_v1 | BED-MED-001 | owned | ⏳ PROVISIONAL (concept-only) |
| Lane: Movies | movies_lane_sample_v1 | BED-THR-002 | royalty-free | ✅ CLEARED |
| Lane: Explainer | julian_flowdesk_explainer_v1 | BED-UP-001 | owned | ✅ CLEARED |
| Lane: Companion | gfe_companion_sage_proof_v1 | BED-WARM-001 | royalty-free | ✅ CLEARED (ep gate = YELLOW, not bed issue) |

**Summary:** 14 CLEARED · 3 SPEC (cleared fallbacks available) · 6 PROVISIONAL (Season 2 concept-only, cleared where applicable)

---

## Music Library Expansion Queue (T5 #143)

| Priority | Bed ID | Spec Title | Needed For | License Target |
|----------|--------|------------|------------|----------------|
| HIGH | BED-NEAR-001 | Euphrates — Reed Flute & Clay Drum | Akkadian (S1), Hittite (S2) | owned or RF perpetual |
| MED | BED-VED-001 | Rishi Pulse — Tanpura Drone | Sanskrit (S1) | owned or RF perpetual |
| MED | BED-EAST-001 | Heian Court — Koto Pulse | Classical Japanese (S2) | owned or RF perpetual |
| MED | BED-MESOAM-001 | Tenochtitlan — Huehuetl Drum | Nahuatl (S1 Ep 11, currently on BED-DOC-001) | owned or RF perpetual |

All four are SPEC_ONLY. Cleared fallbacks exist for all. These become HIGH priority when Benjamin greenlights batch renders for the relevant episodes.

---

*Upon Tyne Productions / STUDIO Music Sound · T5 #143 · Hub 2026-06-20*
