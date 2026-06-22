# DAVID · The Archive — Episode Music Assignments
**Slate:** Dead-Language Slate (18 episodes)  
**Version:** 1.0  
**Created:** 2026-06-19  
**T-Ticket:** T5 #143

---

## Assignment Logic

| Tier | Episodes | Lane | Beds Available |
|------|----------|------|----------------|
| Launch (eps 1–6) | Latin, Greek, Old English, Norse, Gothic, Sumerian | `lane_documentary` | MB-DOC-001 · 002 · 003 |
| Backlog (eps 7–12) | Sanskrit, Biblical Hebrew, Akkadian, Egyptian, Nahuatl, OCS | `lane_explainer` | MB-EXP-001 · 002 · 003 |
| Extension (eps 13–18) | Hittite, Cl. Japanese, Etruscan, PIE, Linear A, Coptic | `lane_companion` | MB-CMP-001 · 002 · 003 |

**Rotation rule:** Primary beds rotate DOC-001 → 002 → 003 → 001 → 002 → 003. Fallback is always the next bed in the same lane (wraps).

---

## Full Assignment Table

| EP | SLUG | EPISODE TITLE | TIER | LANE | PRIMARY BED | FALLBACK BED |
|----|------|---------------|------|------|-------------|--------------|
| 01 | david_latin_corpus_v1 | Why Latin Never Really Died | launch | lane_documentary | MB-DOC-001 | MB-DOC-002 |
| 02 | david_ancient_greek_corpus_v1 | Restoring the Pitch Accent | launch | lane_documentary | MB-DOC-002 | MB-DOC-003 |
| 03 | david_old_english_corpus_v1 | Beowulf's Tongue in Manuscript | launch | lane_documentary | MB-DOC-003 | MB-DOC-001 |
| 04 | david_old_norse_corpus_v1 | Runes Attested, Sagas Reconstructed | launch | lane_documentary | MB-DOC-001 | MB-DOC-002 |
| 05 | david_gothic_corpus_v1 | A Language Saved by One Bible | launch | lane_documentary | MB-DOC-002 | MB-DOC-001 |
| 06 | david_sumerian_corpus_v1 | The First Written Language | launch | lane_documentary | MB-DOC-003 | MB-DOC-002 |
| 07 | david_sanskrit_corpus_v1 | The Language Memory Kept Alive | backlog | lane_explainer | MB-EXP-001 | MB-EXP-002 |
| 08 | david_biblical_hebrew_corpus_v1 | The Language That Came Back | backlog | lane_explainer | MB-EXP-002 | MB-EXP-003 |
| 09 | david_akkadian_corpus_v1 | The Voice Inside the Clay | backlog | lane_explainer | MB-EXP-001 | MB-EXP-003 |
| 10 | david_middle_egyptian_corpus_v1 | The Sound Behind the Hieroglyphs | backlog | lane_explainer | MB-EXP-003 | MB-EXP-001 |
| 11 | david_classical_nahuatl_corpus_v1 | The Tongue the Conquest Wrote Down | backlog | lane_explainer | MB-EXP-002 | MB-EXP-001 |
| 12 | david_old_church_slavonic_corpus_v1 | The Bible That Built an Alphabet | backlog | lane_explainer | MB-EXP-001 | MB-EXP-002 |
| 13 | david_hittite_corpus_v1 | The Language That Rewrote the Family Tree | extension | lane_companion | MB-CMP-001 | MB-CMP-002 |
| 14 | david_classical_japanese_corpus_v1 | The Court Language Hidden in Plain Sight | extension | lane_companion | MB-CMP-002 | MB-CMP-003 |
| 15 | david_etruscan_corpus_v1 | The Tongue Rome Learned Its Alphabet From | extension | lane_companion | MB-CMP-001 | MB-CMP-003 |
| 16 | david_proto_indo_european_corpus_v1 | The Language No One Wrote Down | extension | lane_companion | MB-CMP-003 | MB-CMP-001 |
| 17 | david_linear_a_corpus_v1 | The Script We Can Read but Cannot Understand | extension | lane_companion | MB-CMP-002 | MB-CMP-001 |
| 18 | david_coptic_corpus_v1 | The Vowels Egyptian Never Wrote | extension | lane_companion | MB-CMP-001 | MB-CMP-002 |

---

## Period Alignment Notes

For the dead-language launch slate specifically, the STUDIO clearance_manifest.json (`STUDIO/Music_Sound/clearance_manifest.json`) has existing period beds that can serve as temporary fallbacks while PENDING_DOWNLOAD beds are being sourced:

| Launch Episode | Language Era | clearance_manifest.json fallback |
|----------------|-------------|----------------------------------|
| Ep 1 Latin | Classical Roman | `BED-ANT-001` (Aegean Dusk) or `BED-ANT-002` (Temple Column) |
| Ep 2 Ancient Greek | Classical / Hellenistic | `BED-ANT-001` or `BED-ANT-002` |
| Ep 3 Old English | Medieval Anglo-Saxon | `BED-MED-001` (Scriptorium) or `BED-MED-002` (Northumbrian Hearth) |
| Ep 4 Old Norse | Medieval Norse | `BED-MED-002` (Northumbrian Hearth) |
| Ep 5 Gothic | Late Antique / Migration Period | `BED-DOC-001` (Archive Room) |
| Ep 6 Sumerian | Ancient Near East | `BED-NEAR-001` (Euphrates — SPEC_ONLY; fallback `BED-ANT-002`) |

These are **interim only** — the MB-DOC-* beds from this library should replace them once cleared.

---

## Stamping Instructions

Once a bed is CLEARED (see `Clearance_SOP.md`), stamp the `bed_id` into the episode's `script.json`:

```json
{
  "intake": {
    "music_bed_id": "MB-DOC-001",
    "music_attribution": "Music: [track title] by Kevin MacLeod — incompetech.com (CC BY 4.0)"
  }
}
```

`music_attribution` is `null` for CC0/Public Domain/YT-Free beds.

---

*Bed specs: see `Music_Bed_Library.md` · Machine manifest: `Music_Bed_Manifest.json` · SOP: `Clearance_SOP.md`*  
*STUDIO · Art_Department · Music · T5 #143*
