#!/usr/bin/env python3
"""
Fashion Magazine Modeling Prompt Generator v1.3 — Director | Supermodel-Level Editorial Roster Locked
All models now extremely striking/stunning with high-impact attractive features. Single-subject, 16:9, magazine quality only.
"""

from __future__ import annotations

import sys
from datetime import datetime
from pathlib import Path

_SCRIPTS_DIR = Path(__file__).resolve().parent
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))

from magazine_paths import EDITORIAL_MODELS
from supermodel_roster_data import SUPERMODEL_ROSTER_10

MODEL_SUBFOLDERS = (
    "01_casting_shots",
    "02_reference_views",
    "SCENES",
    "VARIATIONS",
    "CLIPS",
    "PROMOTIONAL",
    "STAGED SHOTS",
)

SCENE_FOLDERS = {
    "studio": "01_casting_shots",
    "runway": "02_reference_views",
}


def ensure_model_dirs(model_name: str) -> None:
    base = EDITORIAL_MODELS / model_name
    for sub in MODEL_SUBFOLDERS:
        (base / sub).mkdir(parents=True, exist_ok=True)


class MagazineModelingPromptGenerator:
    def __init__(self):
        self.version = "1.3"
        self.root = EDITORIAL_MODELS
        self.root.mkdir(parents=True, exist_ok=True)
        print(f"✅ Supermodel editorial assets ready: {self.root}")

    def build_prompt(self, name: str, age: int, ethnicity: str, visuals: str, outfit: str, scene: str = "studio") -> str:
        prompt = f"photorealistic high-fidelity 16:9 magazine editorial photograph, single {age}-year-old {ethnicity} woman named {name}, {visuals}, wearing {outfit}, elegant confident pose with intense captivating gaze to camera, dramatic cinematic lighting with soft shadows and high contrast highlights on fabric and flawless skin, ultra-detailed textures, sharp focus, Vogue-level professional fashion photography, expensive avant-garde haute couture aesthetic, natural physics dress drape and movement, commercial-ready high-end magazine cover quality"
        if scene == "runway":
            prompt += ", dynamic mid-stride runway walk on minimalist catwalk with fabric motion, dramatic spot lighting"
        return prompt

    def generate(self, model_data: dict, scene: str = "studio") -> str:
        name = model_data["name"]
        ensure_model_dirs(name)
        subfolder = SCENE_FOLDERS[scene]
        out_dir = self.root / name / subfolder
        filename = out_dir / f"{name}_Supermodel_Magazine_{scene}.txt"
        prompt = self.build_prompt(
            name=name,
            age=int(model_data["age"]),
            ethnicity=str(model_data["ethnicity"]),
            visuals=str(model_data["visuals"]),
            outfit=str(model_data["outfit"]),
            scene=scene,
        )
        filename.write_text(
            f"# {name} — Supermodel Magazine Shot v1.3 ({scene})\n"
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
            f"{prompt}\n\n"
            "Copy-paste into Grok Imagine. Extremely striking/stunning single-model magazine look locked.\n",
            encoding="utf-8",
        )
        print(f"✅ Saved stunning supermodel shot: {filename}")
        return prompt


if __name__ == "__main__":
    gen = MagazineModelingPromptGenerator()
    for m in SUPERMODEL_ROSTER_10:
        gen.generate(m, scene="studio")
        gen.generate(m, scene="runway")
    print(
        f"\n All {len(SUPERMODEL_ROSTER_10)} supermodel folders ready "
        f"({', '.join(MODEL_SUBFOLDERS)}). Prompts in 01_casting_shots / 02_reference_views."
    )