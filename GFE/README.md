# GFE — Girlfriend Experience Roster

Twenty actress profiles, casting turnarounds, ASMR camera-interaction prompts, and staged-shot assets. Lives inside **STUDIO** at `Studio/GFE/`.

## Layout

```
Studio/GFE/
├── {Aiko,Vesper,...}/     # 20 actress folders
│   ├── 01_casting_shots/
│   ├── 02_reference_views/
│   ├── CLIPS/
│   └── STAGED SHOTS/      # per-actor when present
├── GFE_ASMR_All_Prompts_v1.1.md
└── GFE_ASMR_Camera_Interaction_Library_v1.1.md

Studio/scripts/            # GFE batch tools (run from repo root)
```

## Scripts

Run from the **Studio** repo root:

```bash
cd scripts
python ensure_gfe_folder_structure.py
python GFE_roster_batch.py
python generate_gfe_casting_shots.py
python generate_gfe_asmr_prompts.py
python organize_gfe_folder.py
```

## Parent ecosystem

Part of **STUDIO** — cinematic production layer. Coordinates with `actors_roster/`, `CONCEPTS/`, and `prompts/` for casting and on-screen treatment.