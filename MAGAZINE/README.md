# MAGAZINE — In-Universe Showcase

Our trade publication layer: actors, films, campaigns, and performances presented **as if this universe already exists.**

**Creative canon:** [`UNIVERSE.md`](UNIVERSE.md)  
**Real-world refs:** [`../Canons/Real_World_Reference_Policy_v1.md`](../Canons/Real_World_Reference_Policy_v1.md)  
**Scripts:** [`scripts/`](scripts/)

---

## Layout

```
Studio/MAGAZINE/
├── scripts/               ← generators, catalog, shot-list tools
├── Editorial/Models/      ← 10 supermodel roster
├── Film/ Video/ Runway/ Television/ Promos/
├── Profiles/ History/ Audio/
└── _Catalog/              ← db, prompt packs
```

| Medium | Purpose |
|--------|---------|
| **Editorial/** | Still photography — covers, hero shoots (`Models/` = roster) |
| **Film/** | Feature coverage — reviews, stills, festival write-ups |
| **Video/** | Motion editorial — clip packages, motion covers |
| **Runway/** | Fashion week — shows, backstage |
| **Television/** | Series & streaming coverage |
| **Promos/** | Trailers, key art, campaigns |
| **Profiles/** | Long-form actor & director pieces |
| **History/** | Documentary magazine features |
| **Audio/** | Podcast / voice editorial |
| **_Catalog/** | Cross-medium indexes |

---

## Scripts

```bash
cd scripts
python ensure_magazine_folder_structure.py
python fashion_modeling_prompt_generator.py
```

- Model outputs → `Editorial/Models/{Name}/`
- Shot lists → `../Pipeline/ShotLists/` (Studio root)
- Video packs → `../Pipeline/Video_Prompts/`

---

## Workflow

```
Productions/ (the work) → MAGAZINE/{medium}/ (the showcase) → renders/approved/ (the release)
```