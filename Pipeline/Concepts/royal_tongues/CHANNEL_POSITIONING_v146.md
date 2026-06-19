# #146 Channel Positioning — Royal Tongues

**Recommendation:** **DAVID sub-series** (not a sibling channel)

---

## Decision

| Option | Verdict | Why |
|--------|---------|-----|
| **DAVID sub-series** `Royal Tongues` | **RECOMMENDED** | Same host, Archive set, attested/reconstructed method, shared audience |
| **Sibling channel** (e.g. Upon Tyne History) | Defer | Splits subscribers, duplicates pipeline, blurs brand before DAVID dead-language runway ships |
| **MAGAZINE narrative reenactment** | Wrong product | Roster talent portraying figures on screen → deceased-likeness YELLOW; different format (`narrative-short-film`) |

---

## Positioning statement

**DAVID · The Archive** owns the corpus-first honesty method. **Dead Languages** is the flagship playlist (Latin → Sumerian). **Royal Tongues** is a sub-series applying the same method to historical figures whose *spoken register* can be sourced or reconstructed — Anglo-Norman, Tudor English, court Latin — without costume drama or synthetic figure impersonation.

**Host rule:** David-001 comments, demonstrates period lines, cites sources. He does not wear period dress or claim to *be* the figure.

**Audience promise:** *What did they actually say — and how do we prove it?* applied to crowns, not only to dead tongues.

---

## Channel architecture (one YouTube channel)

```
DAVID · The Archive
├── Playlist: DAVID · Dead Languages        ← flagship (#146 runway continues)
├── Playlist: DAVID · Royal Tongues         ← Eleanor, Richard, Elizabeth pilots
└── Playlist: DAVID · Intro & Archive       ← intros, method explainers
```

**Banner / About:** Parent Upon Tyne credit unchanged (`DAVID/brand/CHANNEL_ABOUT.md`). Add Royal Tongues line to About when sub-series launches.

---

## Publish order (Royal Tongues)

**Pilots (figures 1–3)**

| # | Episode | Hook | Period line |
|---|---------|------|-------------|
| 1 | Eleanor of Aquitaine | Two crowns, one tongue | RECONSTRUCTED Anglo-Norman petition |
| 2 | Richard I | Lion who spoke Norman French | ATTESTED *Deus le volt!* |
| 3 | Elizabeth I | Tilbury in her own English | ATTESTED Tudor speech excerpt |

**Backlog (figures 4–6, #168)** — each bridges to a Dead Languages episode for cross-playlist pull. Validated (Gate 0 GREEN + intake + `--script-only`), not rendered.

| # | Episode | Hook | Period line | Bridges to |
|---|---------|------|-------------|-----------|
| 4 | Charlemagne | The emperor who named the months | ATTESTED Frankish month-names (Einhard) | Dead Languages — Latin |
| 5 | Alfred the Great | A king in his own English | ATTESTED Old English (Pastoral Care preface) | Dead Languages — Old English |
| 6 | Cnut the Great | The king the skalds praised | ATTESTED Old Norse skaldic epithet | Dead Languages — Old Norse |

**Cross-link:** After Dead Languages #1 (Latin), drop Royal Tongues #1 (Eleanor) — both Plantagenet, bridges language → figure. Then pair each backlog figure with its bridge episode (Charlemagne↔Latin, Alfred↔Old English, Cnut↔Old Norse).

---

## When to spin a sibling channel later

Only if **both** are true after 12+ months:

1. Narrative reenactment demand (roster talent *as* figures, cinematic shorts) exceeds documentary-host capacity
2. Algorithm/brand research shows "Upon Tyne History" search intent separate from "dead languages"

Until then: one channel, two playlists, one Archive host.

---

## Format lock

| Field | Value |
|-------|-------|
| `format_id` | `historical-figure-documentary` |
| `actor_id` | `David-001` |
| Set / style | `@Set-Archive-001` + `@Style-Documentary-Prestige-001` |
| Required block | `historical_figure` with `sources[]` |
| Period beat | `04_period_line` — attestation labels mandatory |
| End card | `card_type: sources` — sources card from intake |

Validate: `python STUDIO/Pipeline/Concepts/royal_tongues/validate_royal_tongues_slate.py`