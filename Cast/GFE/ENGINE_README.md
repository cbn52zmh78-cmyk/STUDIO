# GFE — Girlfriend Experience

**GFE** = **Girlfriend Experience** — intimate, direct-to-camera romantic fantasy line with 20 actress profiles. This repo holds **code and scripts**; video assets live in **STUDIO**.

## Split architecture

| Layer | Repo / path | Contents |
|-------|-------------|----------|
| **GFE** (this repo) | `GFE/` | Roster data, batch scripts, profile generator lib |
| **STUDIO** | `Studio/GFE/` | All video content — casting JPGs, staged shots, clips, ASMR outputs |

Sibling layout under `Grok Projects/`:

```
Grok Projects/
├── GFE/              ← you are here (scripts + lib)
└── Studio/
    └── GFE/          ← Aiko/, Vesper/, … actress asset folders
```

## Layout (this repo)

```
scripts/             # Batch generators → write into ../Studio/GFE/
lib/                 # actor_profile_generator + studio prompting stubs
```

## Scripts

Requires `Studio/` as a sibling folder. Run from this repo:

```bash
cd scripts
python ensure_gfe_folder_structure.py
python GFE_roster_batch.py
python generate_gfe_casting_shots.py
python generate_gfe_asmr_prompts.py
python organize_gfe_folder.py
```

All outputs land in `../Studio/GFE/{Name}/`.

## Parent ecosystem

- **STUDIO** — cinematic production, all visual assets
- **NEXUS** — ecosystem registry
