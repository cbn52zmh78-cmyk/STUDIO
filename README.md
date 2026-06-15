# STUDIO — Cinematic Video & Visual Production

The **STUDIO layer** is the creative and production home for all video and cinematic visual work in the Grok Projects ecosystem.

**Core question:** *How should this look and feel on screen?*

STUDIO owns director technique, prompting, reference libraries, production workflows, and final visual output. It does **not** own multi-agent routing (AI), ecosystem governance (NEXUS), or scientific principle enforcement (Science / AI Federation).

---

## Purpose

| STUDIO owns | Other layers own |
|-------------|------------------|
| All video production — cinematic, narrative, general visual | Scientifically valuable viz base → **AI** (with Jantzen) |
| Director styles & techniques | Multi-agent orchestration → **AI** |
| Prompt libraries & production research | Registry & workflows → **NEXUS** |
| Reference management & visual canon | Client deliverable ops → **Stonebridge** |
| Cinematic treatment of validated upstream content | Data integrity → **AI / Science** |

**Hybrid workflow:** AI produces a validated base → STUDIO applies cinematic styling without altering scientific logic.

```
User / NEXUS request
        ↓
   AI Orchestrator (when validation needed)
        ↓
   STUDIO — Projects · Prompts · References · Research · Canons
        ↓
   Final cinematic / video output
```

---

## Top-Level Structure

```
Studio/
├── README.md           ← You are here
├── Projects/           ← Active productions & session work
├── Prompts/            ← Prompt library (by domain + library/ + system/)
├── References/         ← Visual references & mood material
├── Research/           ← Research notes & director session artifacts
├── Canons/             ← Locked production rules & bibles
├── Templates/          ← Reusable project & prompt scaffolds
├── archive/            ← Deprecated or retired work
├── docs/               ← Getting started & technical notes
├── skills/             ← Grok director workflow skills
├── studio/             ← Python package (techniques, prompting)
├── examples/           ← AI Federation handoff patterns
├── systems/            ← System architecture extensions
└── renders/            ← Render outputs (per project as needed)
```

| Folder | Purpose |
|--------|---------|
| **Projects/** | Active video productions — briefs, shot plans, deliverables per title |
| **Prompts/** | Generation prompts by category; see [Prompts/README.md](Prompts/README.md) |
| **References/** | Visual refs — frames, palettes, composition, director study |
| **Research/** | Technique research, profiles, policy drafts, session artifacts |
| **Canons/** | Locked rules promoted from research (age policy, intimacy bible, etc.) |
| **Templates/** | Blank scaffolds — kickoff layouts, shot lists, master templates |
| **archive/** | Superseded prompts, old projects, retired experiments |
| **docs/** | Installation, handoff integration, technical notes |
| **skills/** | Grok skills for STUDIO production workflows |

---

## Connection to AI

| Direction | What happens |
|-----------|--------------|
| **AI → STUDIO** | Orchestrator hands off validated content for cinematic treatment |
| **STUDIO → AI** | Request re-validation if source science material changes |

See `examples/consume_ai_handoff.py` and `docs/getting_started.md`.

---

## Connection to NEXUS

Material milestones and integration changes are noted in `Nexus/Nexus_Project_Registry.md` and `Nexus/Workflows/`.

---

## Package

```bash
pip install -e .
```

---

## Quick Start

| Task | Path |
|------|------|
| Start a production | `Projects/` |
| Find or add prompts | `Prompts/README.md` |
| Research & session notes | `Research/` |
| Lock a rule set | `Canons/` |
| Retire old work | `archive/` |
| AI handoff | `examples/consume_ai_handoff.py` |

---

*STUDIO — cinematic video and visual production for the Grok Projects ecosystem.*