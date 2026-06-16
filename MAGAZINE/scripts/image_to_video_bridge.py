#!/usr/bin/env python3
"""
Image-to-Video Continuity Bridge v1.0 — Director | Idea 3
Takes a reference still/prompt + motion instruction and generates locked video prompts.
Maintains supermodel identity, lighting, single-subject 16:9 framing, and natural physics.
"""

from datetime import datetime
from pathlib import Path

import sys

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from magazine_paths import VIDEO_PROMPTS_DIR


class ImageToVideoBridge:
    def __init__(self):
        self.version = "1.0"
        self.output_dir = VIDEO_PROMPTS_DIR
        self.output_dir.mkdir(parents=True, exist_ok=True)
        print(f"✅ Video Prompts folder ready: {self.output_dir}")

    SUPERMODELS = {
        "Valentina Rossi": {
            "age": 25,
            "ethnicity": "Italian",
            "visuals": "striking supermodel beauty with sharp defined cheekbones, captivating dark eyes, flawless porcelain skin, perfect symmetrical features, magnetic presence",
        }
    }

    def build_video_prompt(
        self,
        model_key: str,
        reference_description: str,
        motion_instruction: str,
        duration: str = "6-8 seconds",
        camera_move: str = "slow motivated push-in",
    ):
        m = self.SUPERMODELS[model_key]
        return (
            f"photorealistic high-fidelity 16:9 video frame, single {m['age']}-year-old {m['ethnicity']} woman named {model_key}, "
            f"{m['visuals']}, {reference_description}, "
            f"exact same woman, exact same lighting direction and intensity, exact same framing and composition as reference still, "
            f"{motion_instruction}, natural fabric physics and drape continuing from previous pose, "
            f"{camera_move}, consistent skin texture and hair movement, no extra figures, clean single-subject composition, "
            f"duration {duration}, Vogue-level professional fashion video, expensive avant-garde haute couture, sharp focus, natural motion, "
            "commercial-ready high-end magazine editorial quality"
        )

    def generate_video_variations(
        self,
        model_key: str,
        reference_description: str,
        base_motion: str,
        num_variations: int = 3,
    ):
        variations = [
            "slow elegant walk forward with subtle fabric movement and sustained eye contact",
            "gentle 3/4 turn while maintaining direct gaze, natural head and shoulder movement",
            "slow push-in on face and upper body with delicate fabric shift and micro-expression change",
        ]

        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        out_dir = self.output_dir / f"{model_key.replace(' ', '_')}_Video_{timestamp}"
        out_dir.mkdir(parents=True, exist_ok=True)

        for i, motion in enumerate(variations[:num_variations], 1):
            prompt = self.build_video_prompt(
                model_key=model_key,
                reference_description=reference_description,
                motion_instruction=motion,
                camera_move=base_motion if i == 1 else "subtle motivated camera adjustment",
            )
            fname = out_dir / f"Video_Variation_{i:02d}.txt"
            fname.write_text(
                f"# Video Variation {i} — {model_key} | Continuing from reference still\n"
                f"Version: {self.version} | Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
                f"{prompt}\n",
                encoding="utf-8",
            )
            print(f"✅ Generated Video Variation {i}")

        print(f"\n Video prompt pack saved to: {out_dir}")
        return out_dir


if __name__ == "__main__":
    bridge = ImageToVideoBridge()

    bridge.generate_video_variations(
        model_key="Valentina Rossi",
        reference_description="wearing asymmetric sculptural black wool coat with metallic petal accents and exaggerated shoulders, elegant confident hero pose with intense direct gaze",
        base_motion="slow motivated camera push-in",
        num_variations=3,
    )