# DAVID · Dead Language Slate v1

**Status:** Render-ready (validated 2026-06-19) — 12 episodes (launch six + backlog eps 7–12, #168) · Slate extension eps 13–18 authored 2026-06-19 (T3 #141, concept/brief only — not yet intake-run)  
**Format:** `documentary-host` · David-001 · 69s · PG  
**Validation:** Gate 0 GREEN + `production_intake` exit 0 + `render_longform --script-only` exit 0  
**Not rendered:** No API spend — launch decision pending.

Smoke-test: `python STUDIO/Pipeline/Concepts/dead_languages/validate_dead_language_slate.py`

---

## Publish order

| # | Slug | Title | Hook (cold open) | Corpus anchor |
|---|------|-------|------------------|---------------|
| 1 | `david_latin_corpus_v1` | Why Latin Never Really Died | Textbooks call Latin dead — yet priests, jurists, and scientists still read it aloud every week | Liturgy + law + science continuity; Caesar *Gallia* line |
| 2 | `david_ancient_greek_corpus_v1` | Restoring the Pitch Accent | Homer and Plato read for millennia — rarely with the pitch accent poets counted | Homeric meter + Dionysius Thrax; Muse invocation |
| 3 | `david_old_english_corpus_v1` | Beowulf's Tongue in Manuscript | Speech of Beowulf and Alfred — ink that outlasted the kingdoms where it was spoken | Beowulf MS + West Saxon alliteration; *Hwæt* opening |
| 4 | `david_old_norse_corpus_v1` | Runes Attested, Sagas Reconstructed | Sagas and runestones — carved stone attests forms, manuscript poetry demands reconstruction | Jelling stones + Poetic Edda meter |
| 5 | `david_gothic_corpus_v1` | A Language Saved by One Bible | Gothic vanished from daily life — survived because Wulfila translated scripture in the fourth century | Codex Argenteus / Wulfila alphabet; *Atta unsar* |
| 6 | `david_sumerian_corpus_v1` | The First Written Language | Not Indo-European, not Semitic — the first language we meet written in clay, five millennia ago | Cuneiform syllabaries + bilingual lists; Ningirsu name |
| 7 | `david_sanskrit_corpus_v1` | The Language Memory Kept Alive | Preserved not first by ink but by memory — recited so carefully we hear it near its origin | Pāṇini + Prātiśākhyas; Rigveda 1.1.1 *agním īḷe* |
| 8 | `david_biblical_hebrew_corpus_v1` | The Language That Came Back | Stopped being spoken at home for centuries, guarded in worship — then revived | Dead Sea Scrolls + Masoretic pointing; *Shemaʿ Yisraʾel* |
| 9 | `david_akkadian_corpus_v1` | The Voice Inside the Clay | Babylon and Assyria's tongue, its cuneiform so forgotten travellers thought it decoration | Gilgamesh + Sumerian-Akkadian lists; *ša naqba īmuru* |
| 10 | `david_middle_egyptian_corpus_v1` | The Sound Behind the Hieroglyphs | Hieroglyphs we read with confidence — whose vowels the script almost never wrote | Rosetta Stone / Champollion + Coptic; *ḥotep-di-nesu* |
| 11 | `david_classical_nahuatl_corpus_v1` | The Tongue the Conquest Wrote Down | Aztec language written down by conquered and conquerors alike — descendants speak it still | Florentine Codex + friar grammars; *in xochitl in cuicatl* |
| 12 | `david_old_church_slavonic_corpus_v1` | The Bible That Built an Alphabet | First written Slavic, built in the ninth century so scripture could be read | Cyril & Methodius / Glagolitic; *Otĭče našĭ* |

**Ordering logic (launch six):** Latin establishes the Archive formula (attested vs reconstructed). Greek and Old English widen the classical/literary audience. Old Norse adds mainstream Viking interest. Gothic is the “one corpus witness” thriller beat. Sumerian closes as the deepest-time capstone.

**Backlog logic (eps 7–12, #168):** Sanskrit is the oral-tradition counterpoint to Latin's written one. Hebrew is the revival success story. Akkadian pairs with Sumerian (cuneiform deep-time, bilingual bridge). Egyptian is the honest hard case (consonants attested, vowels reconstructed via Coptic). Nahuatl opens the New World with living descendants. Old Church Slavonic mirrors Gothic/Latin's scripture-translation + liturgical-continuity strand.

---

## Slate extension — eps 13–18 (T3 #141 · authored 2026-06-19 · concept-only)

| # | Slug | Title | Hook (cold open) | Corpus anchor |
|---|------|-------|------------------|---------------|
| 13 | `david_hittite_corpus_v1` | The Language That Rewrote the Family Tree | Linguists had PIE reconstructed — then Hattusa was excavated and the whole family tree had to be redrawn | ~30,000 cuneiform tablets; Treaty of Kadesh; laryngeal confirmation |
| 14 | `david_classical_japanese_corpus_v1` | The Court Language Hidden in Plain Sight | Modern Japanese speakers read the characters — but the grammar and sounds of the Nara and Heian courts are a foreign language underneath | Man'yōshū (759 CE); Man'yōgana 8-vowel system; Genji |
| 15 | `david_etruscan_corpus_v1` | The Tongue Rome Learned Its Alphabet From | We can read it aloud — the alphabet is recoverable — but much of the vocabulary still resists translation | ~13,000 inscriptions; Liber Linteus (only pre-Roman book); Pyrgi Tablets |
| 16 | `david_proto_indo_european_corpus_v1` | The Language No One Wrote Down | No tablet, no inscription, no manuscript — every sound reconstructed from the descendants | Comparative evidence: Sanskrit, Greek, Latin, Hittite; laryngeal hypothesis |
| 17 | `david_linear_a_corpus_v1` | The Script We Can Read but Cannot Understand | We can vocalise the signs — borrowed from Linear B — but the language they record is unknown | ~1,500 Minoan documents; GORILA corpus; libation formula *i-da-ma-te* |
| 18 | `david_coptic_corpus_v1` | The Vowels Egyptian Never Wrote | For 3,500 years hieroglyphics omitted the vowels — Coptic finally wrote them, and Champollion used that to crack the Rosetta Stone | Nag Hammadi Library; Bohairic liturgy (living); Sahidic NT |

**Slate extension logic (eps 13–18):** Hittite is the IE "shock discovery" paired with ep 2 (Greek, IE family) and ep 16 (PIE). Classical Japanese opens East Asia and is the "hidden in plain sight" arc. Etruscan is the honest partial-decipherment case (contrasts with Linear A's full non-decipherment). PIE is the capstone of the reconstruction methodology arc — the only episode with no corpus at all. Linear A is the Archive's most honest episode: we can read, we cannot understand. Coptic closes the extension as the Egyptian sequel (ep 10), revealing the vowels the hieroglyphics never wrote and tying back to Champollion.

**Intake status:** Concepts and briefs authored; not yet run through `production_intake.py`. Gate 0 human signoff required per concept before intake.

---

## Per-episode assets

| Slug | Concept | Brief | Script (intake) | Imagine pack (script-only) |
|------|---------|-------|-----------------|---------------------------|
| `david_latin_corpus_v1` | `david_latin_corpus_v1.concept.json` | `david_latin_corpus_v1_brief.txt` | `DAVID/scripts/longform_scripts/david_latin_corpus_v1_script.json` | `DAVID/productions/david_latin_corpus_v1_longform_v1/` |
| `david_ancient_greek_corpus_v1` | `david_ancient_greek_corpus_v1.concept.json` | `david_ancient_greek_corpus_v1_brief.txt` | `DAVID/scripts/longform_scripts/david_ancient_greek_corpus_v1_script.json` | `DAVID/productions/david_ancient_greek_corpus_v1_longform_v1/` |
| `david_old_english_corpus_v1` | `david_old_english_corpus_v1.concept.json` | `david_old_english_corpus_v1_brief.txt` | `DAVID/scripts/longform_scripts/david_old_english_corpus_v1_script.json` | `DAVID/productions/david_old_english_corpus_v1_longform_v1/` |
| `david_old_norse_corpus_v1` | `david_old_norse_corpus_v1.concept.json` | `david_old_norse_corpus_v1_brief.txt` | `DAVID/scripts/longform_scripts/david_old_norse_corpus_v1_script.json` | `DAVID/productions/david_old_norse_corpus_v1_longform_v1/` |
| `david_gothic_corpus_v1` | `david_gothic_corpus_v1.concept.json` | `david_gothic_corpus_v1_brief.txt` | `DAVID/scripts/longform_scripts/david_gothic_corpus_v1_script.json` | `DAVID/productions/david_gothic_corpus_v1_longform_v1/` |
| `david_sanskrit_corpus_v1` | `david_sanskrit_corpus_v1.concept.json` | `david_sanskrit_corpus_v1_brief.txt` | `DAVID/scripts/longform_scripts/david_sanskrit_corpus_v1_script.json` | `DAVID/productions/david_sanskrit_corpus_v1_longform_v1/` |
| `david_biblical_hebrew_corpus_v1` | `david_biblical_hebrew_corpus_v1.concept.json` | `david_biblical_hebrew_corpus_v1_brief.txt` | `DAVID/scripts/longform_scripts/david_biblical_hebrew_corpus_v1_script.json` | `DAVID/productions/david_biblical_hebrew_corpus_v1_longform_v1/` |
| `david_akkadian_corpus_v1` | `david_akkadian_corpus_v1.concept.json` | `david_akkadian_corpus_v1_brief.txt` | `DAVID/scripts/longform_scripts/david_akkadian_corpus_v1_script.json` | `DAVID/productions/david_akkadian_corpus_v1_longform_v1/` |
| `david_middle_egyptian_corpus_v1` | `david_middle_egyptian_corpus_v1.concept.json` | `david_middle_egyptian_corpus_v1_brief.txt` | `DAVID/scripts/longform_scripts/david_middle_egyptian_corpus_v1_script.json` | `DAVID/productions/david_middle_egyptian_corpus_v1_longform_v1/` |
| `david_classical_nahuatl_corpus_v1` | `david_classical_nahuatl_corpus_v1.concept.json` | `david_classical_nahuatl_corpus_v1_brief.txt` | `DAVID/scripts/longform_scripts/david_classical_nahuatl_corpus_v1_script.json` | `DAVID/productions/david_classical_nahuatl_corpus_v1_longform_v1/` |
| `david_old_church_slavonic_corpus_v1` | `david_old_church_slavonic_corpus_v1.concept.json` | `david_old_church_slavonic_corpus_v1_brief.txt` | `DAVID/scripts/longform_scripts/david_old_church_slavonic_corpus_v1_script.json` | `DAVID/productions/david_old_church_slavonic_corpus_v1_longform_v1/` |
| `david_sumerian_corpus_v1` | `david_sumerian_corpus_v1.concept.json` | `david_sumerian_corpus_v1_brief.txt` | `DAVID/scripts/longform_scripts/david_sumerian_corpus_v1_script.json` | `DAVID/productions/david_sumerian_corpus_v1_longform_v1/` |
| `david_hittite_corpus_v1` | `david_hittite_corpus_v1.concept.json` | `david_hittite_corpus_v1_brief.txt` | *(not yet run)* | *(not yet run)* |
| `david_classical_japanese_corpus_v1` | `david_classical_japanese_corpus_v1.concept.json` | `david_classical_japanese_corpus_v1_brief.txt` | *(not yet run)* | *(not yet run)* |
| `david_etruscan_corpus_v1` | `david_etruscan_corpus_v1.concept.json` | `david_etruscan_corpus_v1_brief.txt` | *(not yet run)* | *(not yet run)* |
| `david_proto_indo_european_corpus_v1` | `david_proto_indo_european_corpus_v1.concept.json` | `david_proto_indo_european_corpus_v1_brief.txt` | *(not yet run)* | *(not yet run)* |
| `david_linear_a_corpus_v1` | `david_linear_a_corpus_v1.concept.json` | `david_linear_a_corpus_v1_brief.txt` | *(not yet run)* | *(not yet run)* |
| `david_coptic_corpus_v1` | `david_coptic_corpus_v1.concept.json` | `david_coptic_corpus_v1_brief.txt` | *(not yet run)* | *(not yet run)* |

All concepts live under `STUDIO/Pipeline/Concepts/dead_languages/`.

---

## Shared structure (every episode)

| Beat | Role |
|------|------|
| `01_cold_open` | Corpus-grounded hook + DAVID · The Archive |
| `02_stakes` | What silence / loss cost |
| `03_signature_question` | Archive signature question (on-screen) |
| `04_proof_beat` | Corpus evidence named |
| `05_method` | Corpus-first reconstruction method |
| `06_honesty` | Attested vs reconstructed honesty principle |
| `07_demonstration` | Spoken line + **RECONSTRUCTED** / **ATTESTED** on-screen label |
| `08_invitation` | Follow / subscribe CTA |

**Host lock:** `actor_id: David-001` · `@Set-Archive-001` · `@Style-Documentary-Prestige-001` · `david_identity_lock.json` (§4)

---

## Fill and run (any episode)

```powershell
python STUDIO/Pipeline/production_intake.py STUDIO/Pipeline/Concepts/dead_languages/<slug>.concept.json
$env:PYTHONIOENCODING='utf-8'
python DAVID/scripts/render_longform.py DAVID/scripts/longform_scripts/<slug>_script.json --script-only
```

**Render when approved** (spend decision):

```powershell
python DAVID/scripts/render_longform.py DAVID/scripts/longform_scripts/<slug>_script.json --seamless --match-color --cut-on-motion
```