# Scientific Source of Truth (SoT) Standard v1.0

**Status:** Production canon. Non-negotiable for science explainers, astrophysics, molecular, and data-visualization episodes.  
**Applies to:** `science-explainer` format · Stonebridge science handoffs · any episode with measurement claims or @2 visualization payoffs.  
**Feeds:** `concept.science_subject.sources` · visualization on-screen labels · closing **science sources card** · Pre-Publish row 3 (AI + illustrative disclosure).

---

## 1. Claim classes

| Class | Definition | On-screen label | Script rule |
|-------|------------|-----------------|-------------|
| **Observed measurement** | Quantity from instrument, survey, or archived dataset | Optional unit callout | Must cite mission/archive primary in `science_subject.sources` |
| **Peer-reviewed inference** | Interpretation of data in published literature | Verbal hedge (“researchers found…”) | Secondary source required |
| **Observed imagery** | Frame from mission pipeline (JWST, Hubble, EHT, etc.) | `OBSERVED` + mission tag | Primary citation with dataset/release ID |
| **Illustrative visualization** | Schematic, artist conception, or didactic graphic — **not** numerical output | `ILLUSTRATIVE` · `NOT A SIMULATION` | Required on `04_visualization_payoff` when `viz_class: illustrative` |
| **Simulation output** | Numerical model render with defined code/params | `SIMULATION` + model name | Primary = paper/repo + params; never mislabel illustrative as simulation |
| **Forbidden** | Presenting illustrative/AI viz as telescope truth; unsourced constants; medical/legal advice as counsel | — | **RED** at editorial review |

### Illustrative — not simulation (hard rule)

When a frame is **didactic, schematic, or AI-generated** and is **not** direct mission pixels or validated simulation output:

1. `beats[04_visualization_payoff].viz_class` **must** be `"illustrative"`.
2. On-screen labels **must** include **`ILLUSTRATIVE`** and **`NOT A SIMULATION`**.
3. Add **`NOT TO SCALE`** when spatial or temporal compression is used.
4. Host copy **must not** imply the frame is a recording (“this is what JWST saw”) unless `viz_class: observed`.
5. Sources card **must** list the illustrative basis (secondary methods paper or internal viz brief) if no mission primary applies to the frame itself.

**Never** ship illustrative viz with only a simulation label, or simulation output without model citation.

---

## 2. Citation tiers

### Primary — mission & archive data (`type: "primary"`)

Authoritative **instrument, survey, or structural archive** outputs. Preferred agencies:

| Agency key | Examples | Citation minimum |
|------------|----------|----------------|
| `NASA` | Hubble, Chandra, Roman archives; NASA SVS releases | Mission + program + release ID or DOI |
| `JWST` | MAST / Webb program IDs; ERS/GO proposal imagery | `JWST Program ID` or `MAST dataset` + filter/band |
| `EHT` | Event Horizon Telescope M87*/Sgr A* releases | Paper DOI + data release version |
| `PDB` | RCSB Protein Data Bank entries | PDB ID (e.g. `PDB: 1CRN`) + resolution note |
| `ESA` | Gaia, Euclid, XMM archives | Mission + data release |
| `LIGO` | GWTC event catalogs | Event name + catalog version |

Other mission primaries allowed when named with stable dataset ID (ALMA, Vera Rubin, etc.).

### Secondary — peer interpretation (`type: "secondary"`)

- Peer-reviewed journal articles (Nature, Science, ApJ, Cell, etc.)
- Official mission science summaries **interpreting** data (not raw FITS alone)
- Textbooks and review articles for established theory only — not sole source for contested claims

**Minimum:** authors + year + journal OR DOI.

### Not acceptable as sole source

- Unsourced explainer blogs, social clips, AI image galleries presented as data
- Wikipedia alone for numeric claims
- Stock “space” footage without mission attribution

---

## 3. Citation string format (concept JSON)

Each entry in `science_subject.sources[]`:

```json
{
  "citation": "NASA/JWST — Program 2734, NGC 628 MIRI mosaic (2024 release)",
  "type": "primary",
  "agency": "JWST",
  "dataset_id": "10.17909/xxxxx",
  "url": "https://mast.stsci.edu/...",
  "supports": ["03_how_we_know", "04_visualization_payoff"],
  "notes": "Optional producer note"
}
```

| Field | Required | Rule |
|-------|----------|------|
| `citation` | **Yes** | Human-readable; appears on sources card |
| `type` | **Yes** | `primary` or `secondary` only |
| `agency` | Recommended for primary | `NASA` · `JWST` · `EHT` · `PDB` · `ESA` · `LIGO` · other |
| `dataset_id` | Recommended for primary | Program ID, PDB ID, GW event, DOI |
| `url` | No | Stable archive link |
| `supports` | Recommended | Beat IDs this source backs |

### Per-episode minimums (`science-explainer`)

| Requirement | Minimum |
|-------------|---------|
| Mission/archive primaries | ≥1 (≥2 when mixing domains) |
| Peer-reviewed secondary | ≥1 |
| `04_visualization_payoff` viz_class declared | **Required** |
| Primary tied to viz beat | **Required** when `viz_class: observed` |

---

## 4. Visualization workflow

1. Declare `science_subject.viz_class_default` (`illustrative` | `observed` | `simulation`).
2. Override per beat on `04_visualization_payoff` with `viz_class` + `on_screen_labels`.
3. Attach `@2` reference path in concept when using pre-rendered science plate.
4. Intake validates labels for illustrative class (see `science_sources_card.template.json`).
5. Sources card auto-built from `science_subject.sources` (`card_type: sources`).
6. Pre-Publish: producer confirms labels on master match concept JSON.

---

## 5. Science music pairing

Declare `gate_0.music_bed_id` from science lanes in `Music_Sound/clearance_manifest.json`:

| Tone | Lane | Example beds | Use |
|------|------|--------------|-----|
| Wonder, scale, cosmos | `cosmic-awe` | `BED-COS-001`, `BED-COS-002` | Astrophysics, JWST, EHT, deep-time |
| Precision, lab, molecular | `clinical-precision` | `BED-CLI-001`, `BED-CLI-002` | PDB, structural biology, immune/molecular |
| Measurement, fields, atmosphere | `physics-precision` | `BED-PHY-001`, `BED-PHY-002` | Classical & atmospheric physics explainers |
| Reaction, bonding, stoichiometry | `chemistry-lab` | `BED-CHE-001`, `BED-CHE-002` | Chemistry explainers (reserve until chem slate ships) |

Gate 0 row 2: manifest track → **PASS**.

---

## 6. Producer sign-off line

> I confirm every measurement and imagery claim maps to a listed primary or secondary source; `04_visualization_payoff` viz_class and on-screen labels correctly distinguish observed, illustrative, and simulation content; illustrative frames are **not** presented as simulations or direct recordings; the rendered sources card matches the concept JSON.

---

**Cross-refs:** `Historical_SoT_Standard_v1.md` (parallel citation shape) · `science-explainer` (#98) · `science_sources_card.template.json` · `Music_Sound/clearance_manifest.json` · `Style-Cool-Clinical-001`