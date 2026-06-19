#!/usr/bin/env python3
"""Companion lane proof — one GFE actor → conversational-companion (#98) → Modern-Apartment + Soft-Warm (#99)."""
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

PROD_SLUG = "gfe_companion_sage_proof_v1"
PROD_DIR = WORKSPACE / "STUDIO" / "Productions" / "Companion" / f"{PROD_SLUG}_longform_v1"
CASTING_REGISTRY = WORKSPACE / "STUDIO" / "Cast" / "Casting_Bible" / "registry" / "gfe_casting_registry.json"
SET_REF_META = WORKSPACE / "STUDIO" / "Pipeline" / "references" / "modern_apartment_reference.json"

ACTOR_ID = "SageGFE-001"
FORMAT_ID = "conversational-companion"
SET_ID = "@Set-Modern-Apartment-001"
STYLE_ID = "@Style-Soft-Warm-001"
IDENTITY_ANCHOR = "@SageGFE-001"

AI_DISCLOSURE = "Synthetic companion — AI generated performer"

COMPANION_AVATAR_PROMPT = (
    "Sage — synthetic companion, chest-up medium shot, 16:9. "
    "Clearly adult 26-year-old Japanese woman, bookish slim build, straight black hair, "
    "thoughtful dark eyes, pale skin. Fully clothed smart-casual — cream knit sweater over "
    "high-neck blouse, relaxed on linen sofa in modern apartment living room. "
    "Warm friendly check-in energy, supportive friend not romantic, PG editorial framing, "
    "no suggestive angles, no swimwear, no lingerie, no bedroom intimacy staging. "
    "Soft window daylight 5200K, lifestyle SFW, no real person likeness, synthetic companion only."
)

BEATS = [
    {
        "id": "01_greeting",
        "duration": 7,
        "speech_text": "Hey — glad you dropped in today.",
        "action_prompt": (
            "Companion greets viewer warmly, relaxed posture on linen sofa, soft window daylight, "
            "fully clothed cream sweater, friendly eye-line to camera, PG medium-close framing."
        ),
    },
    {
        "id": "02_check_in",
        "duration": 7,
        "speech_text": "How has your week been feeling so far?",
        "action_prompt": (
            "Companion listens attentively, gentle nod, empathetic micro-expressions, "
            "same apartment sofa, supportive friend energy, no romantic staging."
        ),
    },
    {
        "id": "03_core_message",
        "duration": 8,
        "speech_text": "Small pauses count — you do not have to sprint through everything.",
        "action_prompt": (
            "Companion shares calm thought, open hand gesture at chest level, trustworthy tone, "
            "fully clothed, static medium-close, soft-warm grade."
        ),
    },
    {
        "id": "04_reflective_pause",
        "duration": 7,
        "speech_text": "Take one slow breath with me.",
        "action_prompt": (
            "Brief reflective pause, soft inhale, inviting viewer reflection, "
            "hold medium-close, no suggestive framing."
        ),
    },
    {
        "id": "05_encouragement",
        "duration": 7,
        "speech_text": "You're doing better than you think.",
        "action_prompt": (
            "Encouraging close, genuine warm smile, supportive hand gesture, "
            "same wardrobe and set continuity."
        ),
    },
    {
        "id": "06_soft_close",
        "duration": 7,
        "speech_text": "I'll be here when you need a calm check-in.",
        "action_prompt": (
            "Soft sign-off, small wave, warm eye contact, gesture peak for seamless join, "
            "fully clothed companion, PG SFW close."
        ),
        "on_screen": AI_DISCLOSURE,
    },
]

IDENTITY_CONTINUITY = (
    "CONTINUITY LOCK @SageGFE-001: identical companion face, cream knit sweater, "
    "modern apartment sofa set, same eye-line to camera — seamless continuation of prior take, zero jump cut."
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
    req = urllib.request.Request(url, headers={"User-Agent": "STUDIO-companion-proof/1.0"})
    with urllib.request.urlopen(req, timeout=300) as r:
        dest.write_bytes(r.read())


def _find_actor(registry: dict[str, Any], actor_id: str) -> dict[str, Any]:
    for entry in registry.get("actors", []):
        if entry.get("actor_id") == actor_id:
            return entry
    raise KeyError(f"Actor not found: {actor_id}")


def generate_companion_avatar(client: Any, actor: dict[str, Any], set_url: str, refs_dir: Path) -> dict[str, Any]:
    path = refs_dir / "sage_companion_avatar_reference.jpg"
    meta_path = path.with_suffix(".json")
    if path.exists() and path.stat().st_size > 5000 and meta_path.is_file():
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        if meta.get("url"):
            print("[avatar] reusing locked companion reference")
            return {**meta, "path": str(path), "reused": True}

    casting_path = WORKSPACE / actor["reference_image_primary"].replace("STUDIO/", "STUDIO").replace("/", "\\")
    if not casting_path.is_file():
        casting_path = WORKSPACE / actor["reference_image_primary"]

    print("[avatar] generating companion avatar from casting plate + apartment set…")
    uploaded = client.files.upload(str(casting_path))
    pub = client.files.create_public_url(uploaded.id)
    casting_url = getattr(pub, "public_url", None) or pub.public_url

    resp = client.image.sample(
        prompt=COMPANION_AVATAR_PROMPT,
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
        "prompt": COMPANION_AVATAR_PROMPT,
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
    voice = actor.get("voice_spec", {})
    lock = {
        "production": PROD_SLUG,
        "format_id": FORMAT_ID,
        "template_ref": "#98 conversational-companion",
        "set_style_ref": "#99 @Set-Modern-Apartment-001 + @Style-Soft-Warm-001",
        "locked_at": datetime.now(timezone.utc).isoformat(),
        "status": "LOCKED",
        "talent": {
            "actor_id": actor["actor_id"],
            "stage_name": actor["stage_name"],
            "age_locked": actor["age_locked"],
            "content_rating": "SFW",
            "identity_anchor": IDENTITY_ANCHOR,
            "wardrobe": "cream knit sweater, high-neck blouse — fully clothed smart-casual",
            "set_name": "Modern Apartment (Lifestyle)",
        },
        "references": {
            "talent_avatar": {
                "file": avatar["path"],
                "url": avatar["url"],
                "prompt": avatar["prompt"],
                "reuse": "talent reference @2 — image_to_video frame 1 every companion shot",
            },
            "set_plate": {
                "file": set_meta["path"],
                "url": set_meta.get("url"),
                "reuse": "environment plate @1 — locked modern apartment",
            },
        },
        "voice": {
            "register": voice.get("register", "warm"),
            "notes": voice.get("notes", ""),
            "prompt_suffix": (
                "warm approachable conversational voice, attentive listener energy, natural breath, "
                "synthetic companion only"
            ),
        },
        "guardrails": [
            "synthetic only — no real-person likeness",
            "SFW mandatory — PG rating, no suggestive framing",
            "21+ talent age_locked verified",
            "fully clothed wardrobe only",
            AI_DISCLOSURE,
            f"casting plate locked: {actor['reference_image_status']}",
        ],
        "models": {
            "image": "grok-imagine-image-quality",
            "video": "grok-imagine-video-1.5",
            "resolution": "720p",
            "aspect_ratio": "16:9",
        },
    }
    path = PROD_DIR / "sage_companion_identity_lock.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(lock, indent=2, ensure_ascii=False), encoding="utf-8")
    return path


def build_script(identity_lock: Path, avatar: dict[str, Any], actor: dict[str, Any]) -> Path:
    script = build_longform_script(
        FORMAT_ID,
        concept="Warm SFW companion check-in proof — Sage GFE lane validation",
        slug=PROD_SLUG,
        title="STUDIO Companion Proof — Sage SFW Check-In",
        beats=BEATS,
        set_id=SET_ID,
        style_id=STYLE_ID,
    )

    for shot in script["shots"]:
        vp = shot["video_prompt"]
        vp = vp.replace("CONTINUITY LOCK @Companion-001:", f"CONTINUITY LOCK {IDENTITY_ANCHOR}:")
        if IDENTITY_ANCHOR not in vp:
            vp = f"{IDENTITY_CONTINUITY} {vp}"
        vp += " SFW PG only — fully clothed, no suggestive framing, no lingerie, supportive friend energy."
        shot["video_prompt"] = vp

    script["production_dir"] = f"STUDIO/Productions/Companion/{PROD_SLUG}_longform_v1"
    script["production_meta"]["identity_anchor"] = IDENTITY_ANCHOR
    script["production_meta"]["talent_id"] = ACTOR_ID
    script["production_meta"]["casting_plate"] = actor["reference_image_primary"]
    script["production_meta"]["ai_disclosure"] = AI_DISCLOSURE
    script["config"].update({
        "use_identity_lock": False,
        "identity_lock": str(identity_lock),
        "avatar_reference": avatar["path"],
        "avatar_url": avatar["url"],
        "set_reference": "STUDIO/Pipeline/references/modern_apartment_reference.jpg",
        "voice_suffix": (
            "warm approachable conversational voice, attentive listener energy, natural breath, "
            "synthetic companion only"
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
    script["qa_rules"]["require_identity_lock"] = False
    script["qa_rules"]["require_sfw_companion"] = True
    script["qa_rules"]["require_audio"] = True
    script["guardrails"] = list(script.get("guardrails", [])) + [
        AI_DISCLOSURE,
        "companion lane proof — single sample only",
    ]

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

    avatar = generate_companion_avatar(client, actor, set_meta["url"], refs_dir)
    lock_path = write_identity_lock(avatar, actor, set_meta)
    script_path = build_script(lock_path, avatar, actor)

    manifest = {
        "built_at": datetime.now(timezone.utc).isoformat(),
        "lane": "companion",
        "format_id": FORMAT_ID,
        "template_ref": "#98",
        "set_style_ref": "#99",
        "talent": ACTOR_ID,
        "set_id": SET_ID,
        "style_id": STYLE_ID,
        "script": str(script_path),
        "identity_lock": str(lock_path),
        "avatar": avatar["path"],
        "ai_disclosure": AI_DISCLOSURE,
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