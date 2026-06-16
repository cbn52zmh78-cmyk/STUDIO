# STUDIO Prompts

Cinematic and visual generation prompts organized by domain, technique, and role.

**Parent:** [../README.md](../README.md)

---

## Organization

```
Prompts/
├── README.md           ← You are here
├── library/            ← Reusable, production-ready prompt blocks
├── system/             ← STUDIO session & director system prompts
├── astrophysics/       ← Space, planets, cosmic subjects
├── black_hole/         ← Black hole & extreme gravity visuals
├── blocking/           ← Actor blocking and staging
├── character/          ← Character appearance and performance
├── cinematography/     ← Camera, lens, lighting, composition
├── general/            ← Cross-domain prompts
├── historical/         ← Period and historical figure visuals
├── scene/              ← Full scene compositions
└── science_viz/        ← Styled science visuals (post-AI handoff)
```

| Folder | Purpose |
|--------|---------|
| **library/** | Tested prompts ready to copy into `Projects/` |
| **system/** | Session behavior, director workflow, layer rules |
| **astrophysics/** | Astrophysical subjects and prompt bibles |
| **black_hole/** | Black hole templates and masters |
| **blocking** | Staging and spatial blocking language |
| **character** | Character-focused generation prompts |
| **cinematography** | Shot design, camera movement, lighting |
| **general** | Prompts that span multiple domains |
| **historical** | History-layer visual content |
| **scene** | End-to-end scene prompt packages |
| **science_viz** | Cinematic treatment of validated science base |

---

## Prompts vs other folders

| Location | Contains |
|----------|----------|
| `Prompts/` | Executable generation and session prompts |
| `Research/` | Research notes, bibles in development, session artifacts |
| `Canons/` | Locked production rules promoted from research |
| `Templates/` | Blank scaffolds to fill per project |
| `archive/` | Deprecated prompt versions |

---

## Adding prompts

1. Choose the domain folder (or `library/` when production-ready).
2. Use clear filenames and version suffixes when iterating (`_v1.0`).
3. Promote stable bibles to `Canons/` when rules must not drift.
4. Move superseded files to `archive/`.

---

## Related

| Document | Path |
|----------|------|
| Astrophysics bible (canonical) | `astrophysics/ASTROPHYSICS_PROMPT_BIBLE.md` |
| AI handoff styling | `../examples/consume_ai_handoff.py` |
| Python prompt library | `../studio/prompting/prompt_library.py` |