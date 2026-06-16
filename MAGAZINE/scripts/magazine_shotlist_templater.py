#!/usr/bin/env python3
"""
Magazine Shot-List Templater v1.0 — Director | Idea 1
Generates versioned, continuity-locked shot lists from master templates + model data.
Single-subject, 16:9, high-fidelity magazine/editorial only.
"""

import json
from datetime import datetime
from pathlib import Path

import sys

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from magazine_paths import SHOT_LISTS_DIR


class ShotListTemplater:
    def __init__(self):
        self.version = "1.0"
        self.output_dir = SHOT_LISTS_DIR
        self.output_dir.mkdir(parents=True, exist_ok=True)
        print(f"✅ ShotLists folder ready: {self.output_dir}")

    # Locked supermodel roster (from v1.3 — can be loaded from JSON later)
    SUPERMODELS = {
        "Valentina Rossi": {
            "age": 25,
            "ethnicity": "Italian",
            "visuals": "striking supermodel beauty with sharp defined cheekbones, captivating dark eyes, flawless porcelain skin, perfect symmetrical features, magnetic presence",
        },
        # Add others as needed; for v1 we demonstrate with Valentina
    }

    def build_base_description(self, model_key: str) -> str:
        m = self.SUPERMODELS[model_key]
        return (
            f"photorealistic high-fidelity 16:9 magazine editorial photograph, "
            f"single {m['age']}-year-old {m['ethnicity']} woman named {model_key}, {m['visuals']}"
        )

    def generate_shot_list(
        self, model_key: str, scene_name: str, base_outfit: str, num_shots: int = 5
    ):
        base = self.build_base_description(model_key)
        shots = []

        variations = [
            {
                "move": "static hero pose, elegant confident stance with intense direct gaze to camera",
                "lighting": "dramatic cinematic side lighting with soft shadows and high contrast highlights on fabric and skin",
            },
            {
                "move": "slow subtle push-in, fabric drape and movement visible",
                "lighting": "same dramatic cinematic side lighting, slightly warmer highlights",
            },
            {
                "move": "gentle 3/4 turn with sustained eye contact, natural head movement",
                "lighting": "dramatic cinematic side lighting, soft rim light on hair and shoulders",
            },
            {
                "move": "slow walk toward camera, mid-stride, fabric physics and motion",
                "lighting": "dramatic cinematic side lighting with motion-appropriate highlight roll-off",
            },
            {
                "move": "final hero pose, slight head tilt, powerful direct gaze",
                "lighting": "dramatic cinematic side lighting, final high-contrast key light",
            },
        ]

        for i, var in enumerate(variations[:num_shots], 1):
            prompt = (
                f"{base}, wearing {base_outfit}, {var['move']}, "
                f"{var['lighting']}, ultra-detailed textures, sharp focus, "
                "Vogue-level professional fashion photography, expensive avant-garde haute couture aesthetic, "
                "natural physics dress drape and movement, commercial-ready high-end magazine cover quality, "
                "single subject only, clean composition, no extra figures or distractions"
            )
            shots.append(
                {
                    "shot": f"Shot {i:02d}",
                    "intent": var["move"].split(",")[0],
                    "prompt": prompt,
                }
            )

        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        seq_dir = self.output_dir / f"{model_key.replace(' ', '_')}_{scene_name}_{timestamp}"
        seq_dir.mkdir(parents=True, exist_ok=True)

        for s in shots:
            fname = seq_dir / f"{s['shot'].replace(' ', '_')}.txt"
            fname.write_text(
                f"# {s['shot']} — {model_key} | {scene_name}\n"
                f"Version: {self.version} | Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
                f"{s['prompt']}\n",
                encoding="utf-8",
            )

        master = {
            "version": self.version,
            "model": model_key,
            "scene": scene_name,
            "generated": datetime.now().isoformat(),
            "shots": shots,
        }
        (seq_dir / "_MASTER_SEQUENCE.json").write_text(
            json.dumps(master, indent=2), encoding="utf-8"
        )

        print(f"✅ Generated {num_shots}-shot sequence for {model_key} → {seq_dir}")
        return seq_dir


if __name__ == "__main__":
    t = ShotListTemplater()
    t.generate_shot_list(
        model_key="Valentina Rossi",
        scene_name="Sculptural_Black_Coat_Editorial",
        base_outfit="asymmetric sculptural black wool coat with metallic petal accents and exaggerated shoulders",
        num_shots=5,
    )
    print("\n Shot list complete. Open the folder and copy any .txt into Grok Imagine.")