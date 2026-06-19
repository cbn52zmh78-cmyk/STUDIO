#!/usr/bin/env python3
"""Patch movies lane sample script with Amara-001 casting + seamless config."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

PROD = Path(__file__).resolve().parent
SCRIPT = PROD / "movies_lane_sample_v1_script.json"
LOCK = PROD / "amara_character_identity_lock.json"
AVATAR = PROD / "references" / "amara_character_avatar_reference.jpg"
CAST_PLATE = (
    Path(__file__).resolve().parents[3]
    / "Cast/actors_roster/female/south_asia/Amara_Singh/01_casting_shots/casting_turnaround_v1.jpg"
)
WAREHOUSE = Path(__file__).resolve().parents[3] / "Pipeline/references/warehouse_industrial_reference.json"

script = json.loads(SCRIPT.read_text(encoding="utf-8"))
wh = json.loads(WAREHOUSE.read_text(encoding="utf-8"))

# Identity anchor: roster actor Amara-001
anchor = "@Amara-001"
lock_line = (
    f"CONTINUITY LOCK {anchor}: identical character face, wardrobe, hair, same eye-line and blocking "
    "— seamless continuation of prior take, zero jump cut."
)

for shot in script["shots"]:
    vp = shot.get("video_prompt", "")
    vp = vp.replace("@Talent-001", anchor)
    vp = vp.replace(
        "CONTINUITY LOCK @Talent-001: identical character face, wardrobe, hair, same eye-line and blocking — seamless continuation of prior take, zero jump cut.",
        lock_line,
    )
    shot["video_prompt"] = vp

script["production_meta"]["identity_anchor"] = anchor
script["production_meta"]["talent_id"] = "amara_singh"
script["production_meta"]["actor_id"] = "Amara-001"
script["production_meta"]["age_locked"] = 30
script["production_meta"]["content_rating"] = "SFW"

avatar_meta = {}
avatar_json = AVATAR.with_suffix(".json")
if avatar_json.is_file():
    avatar_meta = json.loads(avatar_json.read_text(encoding="utf-8"))

script["production_dir"] = "Studio/Productions/Narrative/movies_lane_sample_v1_longform_v1"
script["config"].update({
    "resolution": "480p",
    "use_identity_lock": False,
    "identity_lock": str(LOCK),
    "avatar_reference": str(AVATAR),
    "avatar_url": avatar_meta.get("url"),
    "set_reference": wh["reference_file"],
    "voice_suffix": (
        "naturalistic dialogue delivery, motivated breath, cinematic intimacy, "
        "London crisp warmth, synthetic talent only"
    ),
    "seamless": {
        "primary": "extend",
        "xfade_s": 0.2,
        "match_color": True,
        "cut_on_motion": True,
        "lamp_lock": False,
        "glasses_lock": False,
        "loudnorm": True,
        "pin_audio_sync": True,
        "reground_interval": 1,
        "magenta_clamp": True,
    },
})

script["provenance_card"].update({
    "title": "Warehouse Signal",
    "subtitle": "STUDIO Movies Lane · Sample validation",
    "footer": "Synthetic performer · Amara Singh (Amara-001) · SFW · Upon Tyne Productions",
})

script["guardrails"] = list(script.get("guardrails", [])) + [
    "movies lane validation sample — not mass production",
    "Amara-001 roster casting plate locked",
    "21+ age_locked verified",
]

SCRIPT.write_text(json.dumps(script, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

# Identity lock (written before avatar URL is known — render uploads if missing)
PROD.mkdir(parents=True, exist_ok=True)
(PROD / "references").mkdir(exist_ok=True)
lock_doc = {
    "production": "movies_lane_sample_v1",
    "format_id": "narrative-short-film",
    "lane": "movies",
    "locked_at": datetime.now(timezone.utc).isoformat(),
    "status": "LOCKED",
    "talent": {
        "actor_id": "Amara-001",
        "stage_name": "Amara Singh",
        "age_locked": 30,
        "content_rating": "SFW",
        "identity_anchor": anchor,
        "wardrobe": "dark olive field jacket, black jeans, black boots — SFW thriller",
        "set_name": "Warehouse Industrial Loft",
        "casting_plate": str(CAST_PLATE),
    },
    "references": {
        "talent_avatar": {
            "file": str(AVATAR),
            "prompt": (
                "Amara Singh — synthetic narrative character, medium shot three-quarter, 16:9. "
                "Female, 30-year-old British Indian, athletic build, thick black hair in long braid, "
                "amber-brown eyes, warm brown skin, strong brows. Dark olive field jacket, black jeans, "
                "black boots — fully clothed SFW thriller wardrobe. Industrial loft background soft blur, "
                "4800K window side key, cinematic tension, no real person likeness, synthetic talent only."
            ),
            "reuse": "talent reference @2 — image_to_video frame 1 every character shot",
        },
        "set_plate": {
            "file": wh["path"],
            "url": wh.get("url"),
            "reuse": "environment plate @1 — @Set-Warehouse-Industrial-001",
        },
    },
    "voice": {
        "register": "derived_from_notes",
        "notes": "London crisp; Punjabi warmth with family.",
        "prompt_suffix": (
            "naturalistic dialogue delivery, motivated breath, cinematic intimacy, "
            "London crisp warmth, synthetic talent only"
        ),
    },
    "guardrails": [
        "synthetic only — no real-person likeness",
        "SFW mandatory — PG-13 framing",
        "21+ talent age_locked verified",
        "casting plate locked: plate_locked",
    ],
    "models": {
        "image": "grok-imagine-image-quality",
        "video": "grok-imagine-video-1.5",
        "resolution": "480p",
        "aspect_ratio": "16:9",
    },
}
LOCK.write_text(json.dumps(lock_doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(f"Patched {SCRIPT}")
print(f"Wrote {LOCK}")