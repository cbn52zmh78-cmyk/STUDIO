# STUDIO — Cinematic Video & Visual Production

**Core question:** *How should this look and feel on screen?*

STUDIO owns director technique, prompting, reference libraries, production workflows, and final visual output.

**Producer charter:** [`PRODUCER.md`](PRODUCER.md) — compliance gate for every generation session.

---

## Producer Layout (June 2026)

```
Studio/
├── PRODUCER.md              ← Compliance charter (read first)
├── README.md                ← You are here
│
├── Producers_Office/        ← Compliance, logs, release tracking
│   ├── Compliance_Reports/
│   ├── Tool_Logs/
│   └── Release_Tracker/     ← E&O / clearance binder scaffold
│
├── Canons/                  ← Locked production rules
│   └── Bibles/              ← Versioned story & technique bibles
│
├── Cast/                    ← All performers & character assets
│   ├── actors_roster/       ← 50+ cast actors (profiles + casting)
│   ├── CONCEPTS/            ← Pre-roster concept characters
│   ├── GFE/                 ← 20 GFE actress asset folders
│
├── MAGAZINE/                ← In-universe showcase (parent — by medium)
│   ├── Editorial/Models/    ← 10 supermodel roster
│   ├── Film/ Video/ Runway/ Television/ Promos/
│   ├── Profiles/ History/ Audio/
│   └── _Catalog/
│
├── Productions/             ← Active shows, scenes, deliverables
│   ├── Narrative/           ← PI_Story, Test_Scenes (Plantagenet, etc.)
│   ├── History/             ← History-layer handoff productions
│   ├── GFE/                 ← Per-actress scene productions
│   ├── Editorial/           ← Magazine runway / hero campaigns
│   └── _Scene_Production_Kit/  ← Clone for every new scene
│
├── Pipeline/                ← Tool-generated prompts & packs (artifacts/)
│   ├── Model_Profiles/
│   ├── ShotLists/
│   ├── Video_Prompts/
│   ├── OneTake_Prompts/
│   ├── Refined_Prompts/
│   ├── Negative_Prompts/
│   ├── Grok_Video_Packs/
│   └── …
│
├── Reference_Library/       ← Plates, 3D assets, metadata, index
│   ├── plates/
│   ├── assets/
│   ├── Asset_Metadata/
│   └── references_index.json
│
├── renders/                 ← Final outputs (gitignored)
│   ├── approved/
│   ├── review/
│   └── rejected/
│
├── Research/                ← Technique research, session artifacts
├── Prompt_Library/          ← Curated prompt bibles by domain
├── Templates/               ← Blank scaffolds
├── Development/             ← Python package, scripts, docs, skills
│   ├── studio/              ← `pip install -e .` package root
│   ├── scripts/
│   └── docs/
│
└── archive/                 ← Retired work
```

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

| Task | Path |
|------|------|
| Producer compliance | `PRODUCER.md` |
| Start a scene | `Productions/_Scene_Production_Kit/` |
| Cast & characters | `Cast/` |
| Run prompt tools | `Pipeline/` (via master launcher) |
| Ship a render | `renders/approved/` |
| Lock a rule | `Canons/` |
| GFE assets | `Cast/GFE/` (scripts in sibling `GFE/` repo) |
| MAGAZINE showcase | `MAGAZINE/` (assets + `MAGAZINE/scripts/`) |

---

*STUDIO — cinematic production for the Grok Projects ecosystem.*