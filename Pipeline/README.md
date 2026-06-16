# Pipeline

Machine-generated prompts, packs, and profiles. **Do not hand-edit without version control.**

Produced by `../artifacts/` tools. Run via:

```powershell
python artifacts/core/master_launcher.py
```

| Folder | Tool |
|--------|------|
| Model_Profiles | model_profile_manager.py |
| ShotLists | magazine_shotlist_templater.py |
| Video_Prompts | multishot_video_compiler.py |
| OneTake_Prompts | onetake_choreography_builder.py |
| Refined_Prompts | prompt_refinement_pipeline.py |
| Negative_Prompts | negative_prompt_builder.py |
| Compliance inputs | content_rating_compliance_guard.py |

**Rule:** Pipeline outputs are drafts until Producer QC approves a render in `renders/approved/`.