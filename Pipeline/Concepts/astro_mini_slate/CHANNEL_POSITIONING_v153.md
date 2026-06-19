# #153 Channel Positioning — Observable (Science)

**Recommendation:** **Own channel / brand** (not a DAVID sub-series)

---

## Decision

| Option | Verdict | Why |
|--------|---------|-----|
| **Own channel — Observable (Upon Tyne Science)** | **RECOMMENDED** | Different audience, host, set, method, and downstream product |
| **DAVID sub-series** (e.g. "DAVID · Cosmos") | **Reject** | Breaks DAVID brand lock (dead languages, Archive desk, David-001); forces science curiosity into language-history funnel |
| **Sibling under DAVID without sub-brand** | **Reject** | Same subscriber confusion as Royal Tongues *would* have caused if audience diverged — here it genuinely diverges |

---

## Why audience differs

| Dimension | DAVID · The Archive | Observable (Science) |
|-----------|---------------------|----------------------|
| **Core question** | *What did they actually say — and how do we prove it?* | *What does the universe do — and how do we measure it?* |
| **Evidence type** | Primary texts, attestation, reconstruction | Observations, experiments, simulations with fidelity rules |
| **Host** | David-001 — documentary archivist | Julian-001 — science communicator (roster) |
| **Set / style** | Archive desk + Documentary Prestige | Seamless Neutral + Cool Clinical |
| **Viewer intent** | Language, history, philology, royal registers | Physics curiosity, space, cosmology, STEM |
| **Retention hook** | Period-language payoff beat | @2 visualization payoff + measurement beats |

Royal Tongues worked as a DAVID sub-series because it reuses the **same host, set, and corpus-first method** on a adjacent topic (historical figures). Astro does not share that method surface — it shares only the Upon Tyne production pipeline.

---

## Scientist-facing product (future)

The `Science/` repo is not a DAVID accessory. It is a parallel product line:

- **Domain fidelity** — `Science/systems/domain_principle_selector.json`, astrophysics visualization principles, Jantzen/molecular routing where applicable
- **Viz pipeline** — `Science/scripts/science_viz_pipeline.py`, `prompt_assembler.py`, `visualization_validator.py`
- **Super Heavy mode** — sand-to-stars research queue, Studio handoff packs, simulation-parameter validation

Observable episodes are **consumer-facing entry points** that must:

1. Label OBSERVED vs SIMULATION vs MODEL on viz payoffs
2. Emit `science_subject` blocks with citable sources at intake
3. Hand off visualization prompts that pass Science fidelity checks before render

A DAVID sub-series would bury this under language-brand SEO and prevent a clean **B2B / educator / creator** lane for the Science viz product later (API exports, fidelity-certified assets, classroom packs).

**Architecture:**

```
Upon Tyne (parent)
├── DAVID · The Archive          ← language / history / attestation
│   ├── Dead Languages
│   └── Royal Tongues
└── Observable                     ← measurement / phenomenon / viz fidelity
    ├── Astrophysics (pilot slate #153)
    └── [future domains via Science/ fields/]
```

---

## Positioning statement

**Observable** is Upon Tyne's science channel: short, sourced explainers where wonder follows evidence. Julian-001 presents on seamless neutral; the payoff is a fidelity-governed visualization — not an Archive period line.

**Audience promise:** *See what we know, how we know it, and what the simulation actually shows — labeled honestly.*

**Parent credit:** "An Upon Tyne production" in About and end cards — same corporate parent as DAVID, distinct brand face.

---

## Channel architecture (separate YouTube channel)

```
Observable (Upon Tyne Science)
├── Playlist: Black Holes & Extreme Gravity   ← Anatomy pilot
├── Playlist: Stars & Stellar Evolution       ← Life & Death pilot
├── Playlist: Galaxies & Cosmology            ← How Galaxies Form pilot
└── Playlist: How We Know                     ← method explainers, viz literacy
```

**Do not** list Observable episodes in DAVID playlists. Cross-promote in community posts only after both channels have flagship episodes live.

---

## Publish order (astro mini-slate pilots)

| # | Episode | Hook | Viz payoff |
|---|---------|------|------------|
| 1 | Anatomy of a Black Hole | Boundary where light cannot escape | Kerr shadow + accretion disk (SIMULATION) |
| 2 | Life & Death of a Star | Atoms forged in dead stars | Stellar evolution MODEL |
| 3 | How Galaxies Form | Islands of trillions of stars | ΛCDM merger SIMULATION |

**Rationale:** Black hole → star → galaxy is the intuitive cosmic zoom-out; each episode introduces a heavier evidence chain (EHT/LIGO → spectroscopy/SN 1987A → Planck/JWST).

---

## Format lock

| Field | Value |
|-------|-------|
| `format_id` | `science-explainer` |
| `actor_id` | `Julian-001` |
| Set / style | `@Set-Seamless-Neutral-001` + `@Style-Cool-Clinical-001` |
| Required block | `science_subject` with `sources[]` |
| Viz beat | `04_visualization_payoff` — `NOT TO SCALE` + SIMULATION/MODEL labels |
| End card | `card_type: sources` — from intake provenance |
| Science handoff | `visualization_prompt` → `Science/scripts/` fidelity path before final render |

Validate: `python STUDIO/Pipeline/Concepts/astro_mini_slate/validate_astro_mini_slate.py`

---

## When a DAVID crossover makes sense (limited)

Only for **language-of-science** episodes (Latin species names, historical astronomers' primary texts) — still `documentary-host` or `historical-figure-documentary` on DAVID, not `science-explainer`. Example: "How Kepler Wrote the Laws" on DAVID; "How Orbits Work" on Observable.

---

## Brand working title

| Element | Value |
|---------|-------|
| Channel name | **Observable** |
| Legal / parent | Upon Tyne Science |
| Host | Julian-001 (Julian Cross) |
| Tagline | Evidence before wonder |
| Category | Science & Technology (YouTube) |

Banner, logo, and About copy — separate brand kit task (not #153 scope).