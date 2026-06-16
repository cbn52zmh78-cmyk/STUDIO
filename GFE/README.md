# GFE — Video & Visual Assets (STUDIO)

All **video content, images, casting plates, staged shots, and clip prompts** for the 20 GFE actresses live here.

Roster **code and batch scripts** are in the standalone [**GFE** repo](https://github.com/cbn52zmh78-cmyk/GFE) (`../GFE/` sibling folder). Scripts write outputs into this directory.

## Layout

```
Studio/GFE/
├── {Aiko,Vesper,...}/     # 20 actress asset folders
│   ├── 01_casting_shots/  # casting_prompt.txt, casting_turnaround_v1.jpg
│   ├── 02_reference_views/
│   ├── CLIPS/             # asmr_camera_interaction_v1.txt
│   ├── STAGED SHOTS/
│   ├── SCENES/
│   └── …
├── GFE_ASMR_All_Prompts_v1.1.md
└── GFE_ASMR_Camera_Interaction_Library_v1.1.md
```

## Generate / update assets

From the **GFE** repo (requires `Studio/` as sibling):

```bash
cd ../GFE/scripts
python ensure_gfe_folder_structure.py
python GFE_roster_batch.py
python generate_gfe_casting_shots.py
python generate_gfe_asmr_prompts.py
```

Or from **Studio** (same paths, local scripts):

```bash
cd scripts
python ensure_gfe_folder_structure.py
```

## Parent ecosystem

Part of **STUDIO** cinematic production. Coordinates with `actors_roster/`, `CONCEPTS/`, and `prompts/`.