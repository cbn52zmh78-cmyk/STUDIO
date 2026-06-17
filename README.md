# STUDIO — Cinematic Video & Visual Production

**Core question:** *How should this look and feel on screen?*

STUDIO owns director technique, prompting, reference libraries, production workflows, and final visual output.

**Producer charter:** [`PRODUCER.md`](PRODUCER.md) — compliance gate for every generation session.

---

## Producer Layout (June 2026)

Full module map: [`MODULES.md`](MODULES.md) · Org chart: [`ORG_CHART.md`](ORG_CHART.md)

```
Studio/
├── PRODUCER.md              ← Chain of command (read first)
├── MODULES.md               ← 00–20 module index
├── ORG_CHART.md
│
├── Producers_Office/        ← Producer authority
│   ├── SLATE/               ← Active titles (max 10)
│   ├── Legal_Gate/          ← Gate verdict JSON
│   ├── Call_Sheets/         ← Daily call sheets
│   ├── Session_Logs/
│   ├── Compliance_Reports/
│   ├── Tool_Logs/
│   └── Release_Tracker/
│
├── Legal/                   ← HARD STOP department
│   ├── AI_Content/ Filmmaking_IRL/ Talent_Replica/
│   ├── Music_Clearance/ Distribution_EO/ Gate_Reports/
│
├── Pre_Production/          ← Script → breakdown → board → schedule
├── Production/              ← Daily reports, continuity, on-set notes
├── Post_Production/         ← Edit, color, sound, VFX, deliverables
├── Distribution/            ← Festival, streaming, theatrical, sales
├── Crew/                    ← Camera through transport
├── Locations/               ← Scout, permits, releases
├── Art_Department/          ← Props, sets, graphics
├── Music_Sound/             ← Score, source, cues, ADR
├── Client_Services/         ← Briefs, deliverables, feedback
├── Modules/                 ← Logical module index
│
├── Cast/                    ← Performers + Talent_Agency/
├── Productions/             ← Active narrative, GFE, History, Editorial
├── MAGAZINE/                ← In-universe showcase by medium
├── Pipeline/                ← Tool outputs (artifacts/)
├── Reference_Library/
├── renders/                 ← review → approved (Producer QC)
├── Canons/ · Research/ · Prompt_Library/ · Development/
└── archive/
```

**Legal RED = hard no.** No generation, no shoot, no publish. Producer does not debate it.

---

## Ecosystem Boundaries

| STUDIO owns | Other layers own |
|-------------|------------------|
| Video & cinematic visual production | Multi-agent routing → **AI** |
| Director styles & prompting | Registry & workflows → **NEXUS** |
| Reference management & visual canon | Client ops → **Stonebridge** |
| Cinematic treatment of validated content | Science principles → **Science / AI** |

---

## Toolchain

Python CLIs live in `../artifacts/`. Outputs land in `Pipeline/`.

```powershell
cd "C:\Users\NCG\Videos\Grok Projects"
pip install -e artifacts/
pip install -e Studio/
python artifacts/core/master_launcher.py
```

---

## Quick Start

| Task | Path / Command |
|------|----------------|
| Producer compliance | `PRODUCER.md` |
| Legal gate (mandatory) | `python artifacts/legal/legal_gate.py --project "Title" --text "..."` |
| Active slate | `Producers_Office/SLATE/` · `python artifacts/production/slate_manager.py list` |
| Talent agency hold | `Cast/Talent_Agency/` — no `renders/approved/` until `agency_ready` |
| Start a scene | `Productions/_Scene_Production_Kit/` |
| Run all tools | `python artifacts/core/master_launcher.py` |
| Ship a render | `renders/approved/` (Producer sign-off only) |
| Client brief | `Client_Services/Briefs/` → Legal Gate first |

---

*STUDIO — cinematic production for the Grok Projects ecosystem.*