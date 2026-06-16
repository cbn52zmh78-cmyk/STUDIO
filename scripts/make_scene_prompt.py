# make_scene_prompt.py - v0.8 (Universal Master Constraints)
import sys
import datetime
import json

MASTER_CONSTRAINTS = {
    "clip_length": (
        "Every individual generation must be strictly 6-10 seconds maximum. Never exceed 10 seconds per clip. "
        "Always plan multi-shot stitching for anything longer."
    ),
    "resolution_rules": {
        "first_generation": "Only 480p or 720p available in Generator. No 1080p option on initial generation.",
        "upscaling": "First generation may be upscaled to 1080p after creation.",
        "1080p_limit": "1080p is HARD-CAPPED at 20 seconds maximum. Cannot be used past 20 seconds under any circumstances.",
        "longer_videos": (
            "Any final video longer than 20 seconds must be generated at 720p from the start OR upscaled to 720p early. "
            "1080p will force fallback to 480p or fail beyond 20 seconds."
        ),
        "best_practice": (
            "For stitched multi-shot scenes longer than 20 seconds total, generate every clip at 720p. "
            "Reserve 1080p only for final deliverables 20 seconds or shorter."
        ),
    },
    "stitching": (
        "Design every shot with natural action overlap or held beats for clean J/L-cuts. Maintain strict character, "
        "lighting, and environment continuity across all shots."
    ),
}


def generate_prompt(scene_idea, mode="default"):
    ts = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M')

    pack = {
        "version": "0.8",
        "mode": mode,
        "master_constraints": MASTER_CONSTRAINTS,
        "overall_scene": scene_idea,
        "narrative_arc": (
            "Always interweave strong stage direction with clear narrative beats. "
            "Make each shot description read as living screenplay action."
        ),
        "resolution_rules": "See master_constraints above — these are now universal and non-negotiable.",
        "shot_breakdown": {
            "shot_1": {
                "duration": "6-8 seconds",
                "description": (
                    "HENRY THE SECOND (@1) seated on throne receiving grave news from clerics who unfurl scrolls. "
                    "His hand slowly tightens around the scepter as controlled anger builds behind his eyes. "
                    "The court falls silent as he raises one hand sharply to silence them. Slow push-in on his face."
                ),
            },
            "shot_2": {
                "duration": "6-8 seconds",
                "description": (
                    "Battle-worn Richard Lionheart steps forward one deliberate pace beside the throne, hand resting "
                    "on sword hilt, eyes locked on Henry with intense loyalty and pain. Clerics lean in, scrolls "
                    "rustling. Henry turns to regard him. Motivated camera drift creating negative space between "
                    "father and son."
                ),
            },
            "shot_3": {
                "duration": "6-8 seconds",
                "description": (
                    "Richard delivers his pledge of loyalty with quiet steel. Henry listens, anger softening into "
                    "grim resolve. The two men hold a charged look as the alliance is silently forged. Final "
                    "low-angle two-shot with strong negative space."
                ),
            },
        },
        "style": (
            "Photorealistic historical drama, rich Plantagenet color palette, high production value, "
            "cinematic lighting, emotional realism, motivated camera"
        ),
        "output": {
            "sequence_length": "18-24 seconds total (stitched)",
            "recommended_generation_length_per_clip": "6-8 seconds (strictly within 6-10s Master Rule)",
            "recommended_resolution": "720p for all shots when stitched total exceeds 20 seconds",
        },
    }

    from pathlib import Path

    scene_slug = {
        "multishot_council": "henry_ii_bad_news_council",
    }.get(mode, mode.replace("-", "_"))
    out_dir = Path(__file__).resolve().parents[1] / "projects" / "Test_Scenes" / scene_slug / "packs"
    out_dir.mkdir(parents=True, exist_ok=True)
    filename = out_dir / f"prompt_pack_{mode}_{ts}.json"
    json_output = json.dumps(pack, indent=2, ensure_ascii=False)
    filename.write_text(json_output, encoding="utf-8")
    print(f"✅ v0.8 Master Constraints Pack saved → {filename}")
    print(json_output)


if __name__ == '__main__':
    scene = (
        sys.argv[1]
        if len(sys.argv) > 1
        else 'Henry II receiving news of his sons conspiring, Richard steps forward and pledges loyalty'
    )
    mode = sys.argv[2] if len(sys.argv) > 2 else 'multishot_council'
    generate_prompt(scene, mode)