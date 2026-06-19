# Historical Source of Truth (SoT) Standard v1.0

**Status:** Production canon. Non-negotiable for biography, historical-figure, and corpus-first DAVID episodes.  
**Applies to:** `historical-figure-documentary` format · dead-language corpus episodes with biographical claims · any on-screen life-dates or attributed speech.  
**Feeds:** `concept.historical_figure.sources` · Gate 0 brief · closing **sources card** · Pre-Publish row 3 (disclosure) where period-language lines appear.

---

## 1. Claim classes

| Class | Definition | On-screen label | Script rule |
|-------|------------|-----------------|-------------|
| **Biographical fact** | Birth, death, office held, documented event with date | None required if sourced | Must map to ≥1 source in `historical_figure.sources` |
| **Attested period language** | Words surviving in a primary witness (manuscript, inscription, contemporary account) | `ATTESTED` + language tag | `beats[04_period_line].attestation: "ATTESTED"` + primary citation naming witness |
| **Reconstructed period language** | Scholarly pronunciation or wording rebuilt from corpus/meter/grammar | `RECONSTRUCTED` + language tag | `attestation: "RECONSTRUCTED"` — never imply a recording exists |
| **Scholarly synthesis** | Modern interpretation of sparse evidence | Verbal hedge in host copy (“scholars argue…”) | Secondary source required |
| **Forbidden** | Invented dialogue attributed to a real figure; dramatic scenes presented as fact; unsourced death-cause gossip | — | **RED** at editorial review |

---

## 2. Source tiers

### Primary (`type: "primary"`)

A source **contemporary with or directly quoting** the figure or event:

- Ancient/medieval chronicles, letters, legal rolls, inscriptions
- Manuscript witnesses of texts the figure wrote or owned
- Archaeological corpora (coins, tablets) with catalogue IDs
- Period charters, council records, diplomatic documents

**Minimum:** author/collection + work title + book/chapter/roll/folio or catalogue ID when available.

### Secondary (`type: "secondary"`)

Modern scholarship **interpreting** primary evidence:

- Peer-reviewed monographs and Oxford/Cambridge/Cambridge UP–class university press works
- Established reference works (ODNB, Britannica academic, Pauly-Wissowa class)
- Critical editions with editorial apparatus

**Minimum:** author + title + publisher/year OR stable URL to a scholarly edition.

### Not acceptable as sole source

- Unsourced social posts, fan wikis, AI summaries, tourist plaques, film/TV, historical fiction
- Single tertiary web articles without traceable primary chain

---

## 3. Citation string format (concept JSON)

Each entry in `historical_figure.sources[]`:

```json
{
  "citation": "Author, Work Title, book.chapter or roll/date (specific passage)",
  "type": "primary",
  "url": "https://optional-stable-link",
  "notes": "Optional — what claim this supports",
  "supports": ["birth_year", "04_period_line", "legacy_beat"]
}
```

| Field | Required | Rule |
|-------|----------|------|
| `citation` | **Yes** | Human-readable; appears on sources card |
| `type` | **Yes** | `primary` or `secondary` only |
| `url` | No | Prefer stable editions (Wikisource, Internet Archive, museum catalogue) |
| `notes` | No | Internal producer note — not rendered unless `render_notes: true` |
| `supports` | Recommended | Beat IDs or claim keys this source backs |

### Per-episode minimums

| Episode type | Primary | Secondary | Period-line primary |
|--------------|---------|-----------|---------------------|
| `historical-figure-documentary` | ≥2 | ≥1 | **Required** if `attestation: ATTESTED`; recommended if `RECONSTRUCTED` |
| Dead-language corpus (no biography) | ≥1 corpus witness | ≥1 reference grammar/edition | Required for attested lines only |

---

## 4. Biographical claim workflow

1. **Draft beats** — mark each factual sentence with intended source key in producer notes.
2. **Fill `historical_figure.sources`** — every death date, title, and place name in speech must trace to a listed citation.
3. **Period line** — one line only; attestation explicit; IPA optional in `speech_ipa`.
4. **Intake** — `production_intake.py` validates non-empty `sources[]` and `citation` on each entry.
5. **Sources card** — auto-built from `provenance_card` (`card_type: sources`) at render.
6. **Pre-Publish** — producer confirms on-card text matches concept JSON (no drift).

---

## 5. Period music pairing

Historical biography and era-staked episodes declare `gate_0.music_bed_id` from **period lanes** in `Music_Sound/clearance_manifest.json`:

| Era keyword | Period lane | Example beds |
|-------------|-------------|--------------|
| antiquity, ancient, Greek, Roman, Late Antique, Sumerian | `period-antiquity` | `BED-ANT-001`, `BED-ANT-002` |
| medieval, Anglo-Norman, Gothic, Old English, Norse, crusades | `period-medieval` | `BED-MED-001`, `BED-MED-002` |
| Tudor, Elizabethan, Henrician, 16th-century English court | `period-tudor` | `BED-TUD-001`, `BED-TUD-002` |

Gate 0 row 2: manifest track → **PASS** (same as mood lanes).

---

## 6. Producer sign-off line

> I confirm every biographical claim in this episode maps to a primary or secondary source listed in `historical_figure.sources`, period-language lines are correctly labeled ATTESTED or RECONSTRUCTED, and the rendered sources card matches the concept JSON.

---

**Cross-refs:** `Real_World_Reference_Policy_v1.md` · `historical-figure-documentary` (#98) · `sources_card.template.json` · `Music_Sound/clearance_manifest.json`