# DAVID · Royal Tongues Slate v1

**Status:** Render-ready (validated 2026-06-19) — 6 episodes (3 pilots + backlog figures 4–6, #168)
**Format:** `historical-figure-documentary` · David-001 · 54s · PG
**Validation:** Gate 0 (GREEN/COUNSEL, none RED) + `production_intake` exit 0 + `render_longform --script-only` exit 0
**Not rendered:** No API spend — launch decision pending.
**Positioning:** DAVID sub-series, not a sibling channel (`CHANNEL_POSITIONING_v146.md`).

Smoke-test: `python STUDIO/Pipeline/Concepts/royal_tongues/validate_royal_tongues_slate.py`

---

## Publish order

| # | Slug | Figure | Title | Period line | Attestation | Bridges to (Dead Languages) |
|---|------|--------|-------|-------------|-------------|-----------------------------|
| 1 | `david_eleanor_aquitaine_v1` | Eleanor of Aquitaine | Two Crowns, One Tongue | Anglo-Norman petition register | RECONSTRUCTED | — (Plantagenet opener) |
| 2 | `david_richard_lionheart_v1` | Richard I | The Lion Who Spoke Norman French | *Deus le volt!* | ATTESTED | — |
| 3 | `david_elizabeth_tudor_v1` | Elizabeth I | The Tilbury Speech in Her Own English | Tilbury 1588 excerpt | ATTESTED | — |
| 4 | `david_charlemagne_v1` | Charlemagne | The Emperor Who Named the Months | Frankish month-names (Einhard, *Vita Karoli* ch. 29) | ATTESTED | Latin |
| 5 | `david_alfred_great_v1` | Alfred the Great | A King in His Own English | Old English — *Pastoral Care* preface greeting | ATTESTED | Old English |
| 6 | `david_cnut_great_v1` | Cnut the Great | The King the Skalds Praised | Old Norse — *Knútr inn ríki* skaldic epithet | ATTESTED | Old Norse |

**Ordering logic (pilots 1–3):** Eleanor opens on the Plantagenet/Anglo-Norman court and is the natural cross-link after Dead Languages #1 (Latin). Richard widens it with a short, attested battle-cry hook. Elizabeth lands the most recognizable attested royal speech (Tilbury) to anchor the sub-series.

**Backlog logic (figures 4–6, #168):** Each expansion is chosen to *bridge* a Dead Languages episode for cross-playlist pull — Charlemagne↔Latin (the Carolingian renaissance restoring Latin, with attested Germanic month-names), Alfred↔Old English (a king whose own West-Saxon prose survives), Cnut↔Old Norse (a king remembered in his skalds' attested court verse). All three carry an ATTESTED period line and 3 primary sources.

**Attestation honesty:** Charlemagne's and Cnut's period lines are attested *about/around* the figure (Einhard's record of the month-names; skaldic verse composed for Cnut, not by him) — the provenance card states this explicitly. Alfred's line is the king's own attested prose. Eleanor's Anglo-Norman is labeled RECONSTRUCTED.

---

## Per-episode assets

| Slug | Concept | Brief | Script (intake) | Script-only output |
|------|---------|-------|-----------------|--------------------|
| `david_eleanor_aquitaine_v1` | `david_eleanor_aquitaine_v1.concept.json` | `david_eleanor_aquitaine_v1_brief.txt` | `DAVID/scripts/longform_scripts/david_eleanor_aquitaine_v1_script.json` | `STUDIO/Productions/Editorial/david_eleanor_aquitaine_v1_longform_v1/` |
| `david_richard_lionheart_v1` | `david_richard_lionheart_v1.concept.json` | `david_richard_lionheart_v1_brief.txt` | `DAVID/scripts/longform_scripts/david_richard_lionheart_v1_script.json` | `STUDIO/Productions/Editorial/david_richard_lionheart_v1_longform_v1/` |
| `david_elizabeth_tudor_v1` | `david_elizabeth_tudor_v1.concept.json` | `david_elizabeth_tudor_v1_brief.txt` | `DAVID/scripts/longform_scripts/david_elizabeth_tudor_v1_script.json` | `STUDIO/Productions/Editorial/david_elizabeth_tudor_v1_longform_v1/` |
| `david_charlemagne_v1` | `david_charlemagne_v1.concept.json` | `david_charlemagne_v1_brief.txt` | `DAVID/scripts/longform_scripts/david_charlemagne_v1_script.json` | `STUDIO/Productions/Editorial/david_charlemagne_v1_longform_v1/` |
| `david_alfred_great_v1` | `david_alfred_great_v1.concept.json` | `david_alfred_great_v1_brief.txt` | `DAVID/scripts/longform_scripts/david_alfred_great_v1_script.json` | `STUDIO/Productions/Editorial/david_alfred_great_v1_longform_v1/` |
| `david_cnut_great_v1` | `david_cnut_great_v1.concept.json` | `david_cnut_great_v1_brief.txt` | `DAVID/scripts/longform_scripts/david_cnut_great_v1_script.json` | `STUDIO/Productions/Editorial/david_cnut_great_v1_longform_v1/` |

All concepts and briefs live under `STUDIO/Pipeline/Concepts/royal_tongues/`. Latest run → `validation_report.json`.

---

## Shared structure (every episode)

| Beat | Role |
|------|------|
| `01_cold_open` | "I am DAVID" hook + DAVID · The Archive · Royal Tongues |
| `02_who_they_were` | Figure biography — dates, reign, defining act |
| `03_their_world` | Language environment of the court (vernacular + Latin) |
| `04_period_line` | Attested/reconstructed period line + on-screen **ATTESTED** / **RECONSTRUCTED** + **PERIOD LANGUAGE** labels |
| `05_legacy` | Death + what survives, and how we know it |

**End card:** `card_type: sources` (sources card from intake — 3 primary sources per figure).

**Host rule:** David-001 comments, demonstrates the period line, and cites sources. He does **not** wear period dress or claim to *be* the figure (no deceased-likeness impersonation).

**Host lock:** `actor_id: David-001` · `@Set-Archive-001` · `@Style-Documentary-Prestige-001` · `format_id: historical-figure-documentary`.

---

## Fill and run (any episode)

```powershell
$env:PYTHONIOENCODING='utf-8'
python STUDIO/Pipeline/production_intake.py STUDIO/Pipeline/Concepts/royal_tongues/<slug>.concept.json -o DAVID/scripts/longform_scripts/<slug>_script.json
python DAVID/scripts/render_longform.py DAVID/scripts/longform_scripts/<slug>_script.json --script-only
```

**Render when approved** (spend decision):

```powershell
python DAVID/scripts/render_longform.py DAVID/scripts/longform_scripts/<slug>_script.json --seamless --match-color --cut-on-motion
```

---

## Validation snapshot (2026-06-19)

| Slug | Gate 0 | Intake | `--script-only` | Sources |
|------|--------|--------|-----------------|---------|
| `david_eleanor_aquitaine_v1` | GREEN | OK | OK | 3 |
| `david_richard_lionheart_v1` | COUNSEL | OK | OK | 3 |
| `david_elizabeth_tudor_v1` | GREEN | OK | OK | 3 |
| `david_charlemagne_v1` | GREEN | OK | OK | 3 |
| `david_alfred_great_v1` | GREEN | OK | OK | 3 |
| `david_cnut_great_v1` | GREEN | OK | OK | 3 |

Validator exit 0 (no RED). Richard I returns **COUNSEL** (legal counsel review, not a block) — crusade-era *Deus le volt!* battle-cry flagged for human sign-off before publish; passes the gate.
