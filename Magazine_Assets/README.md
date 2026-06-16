# Magazine Assets (STUDIO)

Supermodel magazine and runway editorial assets for the 10-model roster. All **prompts and images** live here; generators run from the [**MAGAZINE** repo](https://github.com/cbn52zmh78-cmyk/MAGAZINE).

## Layout

```
Studio/Magazine_Assets/
├── {Anya Petrova, Freya Lind, …}/   # 10 model folders
│   ├── 01_casting_shots/            # studio editorial prompt + hero images
│   ├── 02_reference_views/        # runway editorial prompt
│   ├── SCENES/
│   ├── VARIATIONS/
│   └── …
```

## Generate / update

From the **MAGAZINE** repo (`../MAGAZINE/scripts`):

```bash
cd ../MAGAZINE/scripts
python ensure_magazine_folder_structure.py
python fashion_modeling_prompt_generator.py
```