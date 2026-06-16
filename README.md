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
├── actors_roster/      ← Cast actors: {gender}/{region}/{Name}/ profiles + casting
├── scripts/            ← CLI tools (casting shot, image packs, actor profiles)
├── projects/           ← Active productions (PI_Story, Test_Scenes, …)
├── prompts/            ← Prompt library (by domain + library/ + system/)
├── references/         ← Visual references & mood material
├── research/           ← Research notes & director session artifacts
├── Canons/             ← Locked production rules & bibles (incl. intimacy protocol)
├── CONCEPTS/           ← Pre-roster concept characters & casting plates
├── GFE/                ← Girlfriend Experience video assets (20 actress folders); code in GFE repo
├── Magazine_Assets/    ← Supermodel editorial assets (10 models); code in MAGAZINE repo
├── assets/             ← Shared 3D models, images, references
├── Templates/          ← Reusable project & prompt scaffolds
├── archive/            ← Deprecated or retired work
├── docs/               ← Getting started & technical notes
├── skills/             ← Grok director workflow skills
├── studio/             ← Python package (techniques, prompting)
├── examples/           ← Handoff patterns & profile examples
├── systems/            ← System architecture extensions
└── renders/            ← Render outputs (gitignored)
```

| Folder | Purpose |
|--------|---------|
| **actors_roster/** | 50 cast actors — `male/` or `female/` → `world_region/` → actor folder |
| **scripts/** | Production CLIs; see `actor_profile_generator.py`, `generate_roster_50.py` |
| **projects/** | Active video productions — briefs, shot plans, Test_Scenes harness |
| **prompts/** | Generation prompts by category; see [prompts/README.md](prompts/README.md) |
| **references/** | Visual refs — frames, palettes, composition, director study |
| **research/** | Technique research, profiles, policy drafts, session artifacts |
| **Canons/** | Locked rules (age policy, intimacy bible, Protocol v1.3, etc.) |
| **CONCEPTS/** | Concept casting turnarounds before roster promotion |
| **GFE/** | Girlfriend Experience video assets — casting JPGs, staged shots, clips; scripts in [GFE repo](https://github.com/cbn52zmh78-cmyk/GFE) |
| **Magazine_Assets/** | Supermodel editorial prompts and images; scripts in [MAGAZINE repo](https://github.com/cbn52zmh78-cmyk/MAGAZINE) |
| **assets/** | Shared production assets — 3D models, images, reference plates |
| **Templates/** | Blank scaffolds — kickoff layouts, shot lists, master templates |
| **archive/** | Superseded prompts, legacy flat roster paths, profile build scratch |
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