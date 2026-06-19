#!/usr/bin/env python3
"""STUDIO non-documentary sample — cast → set/style → script.json → render.

End-to-end proof that STUDIO produces beyond DAVID documentary host format.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

WORKSPACE = Path(__file__).resolve().parents[2]
ARTIFACTS = WORKSPACE / "artifacts"
sys.path.insert(0, str(ARTIFACTS))
sys.path.insert(0, str(WORKSPACE / "tools"))

from production.production_templates import build_longform_script, write_script  # noqa: E402

PROD_SLUG = "flowdesk_explainer_v1"
PROD_DIR = WORKSPACE / "STUDIO" / "Productions" / "Editorial" / f"{PROD_SLUG}_longform_v1"
CASTING_REGISTRY = WORKSPACE / "STUDIO" / "Cast" / "Casting_Bible" / "registry" / "casting_registry.json"
SET_REF_META = WORKSPACE / "STUDIO" / "Pipeline" / "references" / "seamless_neutral_grey_reference.json"

ACTOR_ID = "Amara-001"
FORMAT_ID = "explainer-ad"
SET_ID = "@Set-Seamless-Neutral-001"
STYLE_ID = "@Style-Cool-Clinical-001"

PRESENTER_AVATAR_PROMPT = (
    "Amara Singh — synthetic product presenter, chest-up medium shot, 16:9. "
    "Female, reads age 30, British Indian, athletic build, thick black hair in long braid, "
    "amber-brown eyes, warm brown skin, strong brows. Smart-casual slate grey blazer over "
    "white blouse — fully clothed professional presenter wardrobe, NOT swimwear. "
    "Standing before neutral grey seamless backdrop, cool clinical 5600K even lighting. "
    "Clear confident presenter energy, trustworthy product tone, no real person likeness, "
    "invented face only, synthetic presenter only."
)

BEATS = [
    {
        "id": "01_hook",
        "duration": 7,
        "speech_text": "Still drowning in scattered notes?",
        "action_prompt": "Presenter addresses camera directly, crisp opener, neutral grey seamless backdrop.",
    },
    {
        "id": "02_pain",
        "duration": 7,
        "speech_text": "Every tab steals your focus.",
        "action_prompt": "Presenter names the pain point, empathetic but brisk, same framing.",
    },
    {
        "id": "03_solution",
        "duration": 8,
        "speech_text": "FlowDesk gathers ideas in one calm workspace.",
        "action_prompt": "Solution reveal — open palm gesture, clean clinical lighting, confident smile.",
    },
    {
        "id": "04_benefit_a",
        "duration": 7,
        "speech_text": "Capture thoughts instantly, anywhere.",
        "action_prompt": "First benefit with presentational hand gesture, locked axis.",
    },
    {
        "id": "05_benefit_b",
        "duration": 7,
        "speech_text": "Find what you need in seconds.",
        "action_prompt": "Second benefit, maintain axis and lighting continuity.",
    },
    {
        "id": "06_cta",
        "duration": 7,
        "speech_text": "Try FlowDesk free at flowdesk dot app.",
        "action_prompt": "Clear CTA, open-palm invite, end on gesture peak.",
        "on_screen": "FlowDesk · flowdesk.app",
    },
]

IDENTITY_CONTINUITY = (
    "CONTINUITY LOCK @Amara-001: identical presenter face, slate grey blazer, white blouse, "
    "neutral seamless set, same eye-line — seamless continuation of prior take, zero jump cut."
)


def _load_grok_token() -> str:
    auth_path = Path.home() / ".grok" / "auth.json"
    data = json.loads(auth_path.read_text(encoding="utf-8"))
    entry = next(iter(data.values()))
    token = entry.get("key") or entry.get("access_token")
    if not token:
        raise RuntimeError("No Grok token")
    return token


def _download(url: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": "STUDIO-sample/1.0"})
    with urllib.request.urlopen(req, timeout=300) as r:
        dest.write_bytes(r.read())


def _find_actor(registry: dict[str, Any], actor_id: str) -> dict[str, Any]:
    for entry in registry.get("actors", registry.get("entries", [])):
        if entry.get("actor_id") == actor_id:
            return entry
    raise KeyError(f"Actor not found: {actor_id}")


def generate_presenter_avatar(client: Any, actor: dict[str, Any], set_url: str, refs_dir: Path) -> dict[str, Any]:
    path = refs_dir / "amara_presenter_avatar_reference.jpg"
    meta_path = path.with_suffix(".json")
    if path.exists() and path.stat().st_size > 5000 and meta_path.is_file():
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        if meta.get("url"):
            print("[avatar] reusing locked presenter reference")
            return {**meta, "path": str(path), "reused": True}

    casting_path = WORKSPACE / actor["reference_image_primary"].replace("/", "\\")
    if not casting_path.is_file():
        casting_path = WORKSPACE / actor["reference_image_primary"]

    print("[avatar] generating presenter from casting plate + set…")
    uploaded = client.files.upload(str(casting_path))
    pub = client.files.create_public_url(uploaded.id)
    casting_url = getattr(pub, "public_url", None) or pub.public_url

    resp = client.image.sample(
        prompt=PRESENTER_AVATAR_PROMPT,
        model="grok-imagine-image-quality",
        image_url=set_url,
    )
    _download(resp.url, path)
    locked_at = datetime.now(timezone.utc).isoformat()
    data = {
        "actor_id": actor["actor_id"],
        "stage_name": actor["stage_name"],
        "age_locked": actor["age_locked"],
        "path": str(path),
        "url": resp.url,
        "prompt": PRESENTER_AVATAR_PROMPT,
        "casting_plate": str(casting_path),
        "casting_url": casting_url,
        "set_url": set_url,
        "model": "grok-imagine-image-quality",
        "aspect_ratio": "16:9",
        "reference_status": "plate_locked",
        "locked_at": locked_at,
        "sfw": True,
        "synthetic_only": True,
        "reused": False,
    }
    meta_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    return data


def write_identity_lock(avatar: dict[str, Any], actor: dict[str, Any], set_meta: dict[str, Any]) -> Path:
    lock = {
        "production": PROD_SLUG,
        "format_id": FORMAT_ID,
        "locked_at": datetime.now(timezone.utc).isoformat(),
        "status": "LOCKED",
        "talent": {
            "actor_id": actor["actor_id"],
            "stage_name": actor["stage_name"],
            "age_locked": actor["age_locked"],
            "content_rating": actor.get("content_rating", "SFW"),
            "identity_anchor": "@Amara-001",
            "wardrobe": "slate grey blazer, white blouse — smart-casual presenter",
            "set_name": "Neutral Seamless Backdrop",
        },
        "references": {
            "talent_avatar": {
                "file": avatar["path"],
                "url": avatar["url"],
                "prompt": avatar["prompt"],
                "reuse": "talent reference @2 — image_to_video frame 1 every presenter shot",
            },
            "set_plate": {
                "file": set_meta["path"],
                "url": set_meta.get("url"),
                "reuse": "environment plate @1 — locked seamless neutral",
            },
        },
        "voice": {
            "register": actor["voice_spec"].get("register", "confident"),
            "notes": actor["voice_spec"].get("notes", ""),
            "prompt_suffix": (
                "clear confident presenter voice, brisk diction, trustworthy product tone, "
                "London crisp warmth, synthetic presenter only"
            ),
        },
        "guardrails": [
            "synthetic only — no real-person likeness",
            "SFW mandatory — PG rating",
            "21+ talent age_locked verified",
            f"casting plate locked: {actor['reference_image_status']}",
        ],
        "models": {
            "image": "grok-imagine-image-quality",
            "video": "grok-imagine-video-1.5",
            "resolution": "720p",
            "aspect_ratio": "16:9",
        },
    }
    path = PROD_DIR / "amara_presenter_identity_lock.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(lock, indent=2, ensure_ascii=False), encoding="utf-8")
    return path


def build_script(identity_lock: Path, avatar: dict[str, Any]) -> Path:
    script = build_longform_script(
        FORMAT_ID,
        concept="FlowDesk productivity app explainer — SFW commercial sample",
        slug=PROD_SLUG,
        title="STUDIO Sample — FlowDesk Explainer Ad",
        beats=BEATS,
        set_id=SET_ID,
        style_id=STYLE_ID,
        brand={
            "brand": "FlowDesk",
            "cta": "Try free at flowdesk.app",
            "legal": "Synthetic presenter · demo only",
        },
    )

    for shot in script["shots"]:
        vp = shot["video_prompt"]
        vp = vp.replace(
            "CONTINUITY LOCK @Presenter-001:",
            "CONTINUITY LOCK @Amara-001:",
        )
        if "CONTINUITY LOCK @Amara-001" not in vp:
            vp = f"{IDENTITY_CONTINUITY} {vp}"
        shot["video_prompt"] = vp

    script["production_dir"] = f"Studio/Productions/Editorial/{PROD_SLUG}_longform_v1"
    script["production_meta"]["identity_anchor"] = "@Amara-001"
    script["production_meta"]["talent_id"] = ACTOR_ID
    script["production_meta"]["casting_plate"] = (
        "Studio/Cast/actors_roster/female/south_asia/Amara_Singh/01_casting_shots/casting_turnaround_v1.jpg"
    )
    script["config"]["magenta_clamp"] = False
    script["config"].update({
        "use_identity_lock": False,
        "identity_lock": str(identity_lock),
        "avatar_reference": avatar["path"],
        "avatar_url": avatar["url"],
        "set_reference": "Studio/Pipeline/references/seamless_neutral_grey_reference.jpg",
        "voice_suffix": (
            "clear confident presenter voice, brisk diction, trustworthy product tone, "
            "London crisp warmth, synthetic presenter only"
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
            "reground_interval": 2,
            "magenta_clamp": False,
        },
    })
    script["qa_rules"]["require_audio"] = True

    out = PROD_DIR / f"{PROD_SLUG}_script.json"
    write_script(script, out)
    return out


def render(script_path: Path) -> int:
    cmd = [
        sys.executable,
        str(WORKSPACE / "DAVID" / "scripts" / "render_longform.py"),
        str(script_path),
        "--seamless",
        "--match-color",
        "--cut-on-motion",
    ]
    print("[render]", " ".join(cmd))
    return subprocess.call(cmd, cwd=str(WORKSPACE / "DAVID"))


def main() -> int:
    import xai_sdk

    token = os.environ.get("XAI_API_KEY") or _load_grok_token()
    os.environ["XAI_API_KEY"] = token
    client = xai_sdk.Client(api_key=token)

    registry = json.loads(CASTING_REGISTRY.read_text(encoding="utf-8"))
    actor = _find_actor(registry, ACTOR_ID)
    if actor["age_locked"] < 21:
        raise RuntimeError(f"{ACTOR_ID} fails 21+ compliance")
    if actor["reference_image_status"] != "plate_locked":
        raise RuntimeError(f"{ACTOR_ID} casting plate not locked")

    set_meta = json.loads(SET_REF_META.read_text(encoding="utf-8"))
    refs_dir = PROD_DIR / "references"
    refs_dir.mkdir(parents=True, exist_ok=True)

    avatar = generate_presenter_avatar(client, actor, set_meta["url"], refs_dir)
    lock_path = write_identity_lock(avatar, actor, set_meta)
    script_path = build_script(lock_path, avatar)

    manifest = {
        "built_at": datetime.now(timezone.utc).isoformat(),
        "format_id": FORMAT_ID,
        "talent": ACTOR_ID,
        "set_id": SET_ID,
        "style_id": STYLE_ID,
        "script": str(script_path),
        "identity_lock": str(lock_path),
        "avatar": avatar["path"],
    }
    (PROD_DIR / "build_manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(json.dumps(manifest, indent=2))

    if "--build-only" in sys.argv:
        return 0
    return render(script_path)


if __name__ == "__main__":
    raise SystemExit(main())