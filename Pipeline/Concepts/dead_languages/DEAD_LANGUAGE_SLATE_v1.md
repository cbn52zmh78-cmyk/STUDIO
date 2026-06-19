# DAVID · Dead Language Slate v1

**Status:** Render-ready (validated 2026-06-19)  
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

**Ordering logic:** Latin establishes the Archive formula (attested vs reconstructed). Greek and Old English widen the classical/literary audience. Old Norse adds mainstream Viking interest. Gothic is the “one corpus witness” thriller beat. Sumerian closes as the deepest-time capstone.

---

## Per-episode assets

| Slug | Concept | Brief | Script (intake) | Imagine pack (script-only) |
|------|---------|-------|-----------------|---------------------------|
| `david_latin_corpus_v1` | `david_latin_corpus_v1.concept.json` | `david_latin_corpus_v1_brief.txt` | `DAVID/scripts/longform_scripts/david_latin_corpus_v1_script.json` | `DAVID/productions/david_latin_corpus_v1_longform_v1/` |
| `david_ancient_greek_corpus_v1` | `david_ancient_greek_corpus_v1.concept.json` | `david_ancient_greek_corpus_v1_brief.txt` | `DAVID/scripts/longform_scripts/david_ancient_greek_corpus_v1_script.json` | `DAVID/productions/david_ancient_greek_corpus_v1_longform_v1/` |
| `david_old_english_corpus_v1` | `david_old_english_corpus_v1.concept.json` | `david_old_english_corpus_v1_brief.txt` | `DAVID/scripts/longform_scripts/david_old_english_corpus_v1_script.json` | `DAVID/productions/david_old_english_corpus_v1_longform_v1/` |
| `david_old_norse_corpus_v1` | `david_old_norse_corpus_v1.concept.json` | `david_old_norse_corpus_v1_brief.txt` | `DAVID/scripts/longform_scripts/david_old_norse_corpus_v1_script.json` | `DAVID/productions/david_old_norse_corpus_v1_longform_v1/` |
| `david_gothic_corpus_v1` | `david_gothic_corpus_v1.concept.json` | `david_gothic_corpus_v1_brief.txt` | `DAVID/scripts/longform_scripts/david_gothic_corpus_v1_script.json` | `DAVID/productions/david_gothic_corpus_v1_longform_v1/` |
| `david_sumerian_corpus_v1` | `david_sumerian_corpus_v1.concept.json` | `david_sumerian_corpus_v1_brief.txt` | `DAVID/scripts/longform_scripts/david_sumerian_corpus_v1_script.json` | `DAVID/productions/david_sumerian_corpus_v1_longform_v1/` |

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