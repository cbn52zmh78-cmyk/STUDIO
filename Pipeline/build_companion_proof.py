#!/usr/bin/env python3
"""Companion lane proof — GFE actor → conversational-companion (#98) → Modern-Apartment + Soft-Warm (#99)."""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

WORKSPACE = Path(__file__).resolve().parents[2]
ARTIFACTS = WORKSPACE / "artifacts"
sys.path.insert(0, str(ARTIFACTS))
sys.path.insert(0, str(WORKSPACE / "tools"))

from production.production_templates import build_longform_script, write_script  # noqa: E402

CASTING_REGISTRY = WORKSPACE / "STUDIO" / "Cast" / "Casting_Bible" / "registry" / "gfe_casting_registry.json"
SET_REF_META = WORKSPACE / "STUDIO" / "Pipeline" / "references" / "modern_apartment_reference.json"

FORMAT_ID = "conversational-companion"
SET_ID = "@Set-Modern-Apartment-001"
STYLE_ID = "@Style-Soft-Warm-001"
AI_DISCLOSURE = "Synthetic companion — AI generated performer"

BEATS = [
    {
        "id": "01_greeting",
        "duration": 7,
        "speech_text": "Hey — glad you dropped in today.",
        "action_prompt": (
            "Companion greets viewer warmly, relaxed posture on linen sofa, soft window daylight, "
            "fully clothed smart-casual, friendly eye-line to camera, PG medium-close framing."
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
            "fully clothed companion, PG SFW close. "
            f"Lower-third on-screen text overlay, legible white text on semi-transparent bar: {AI_DISCLOSURE}"
        ),
        "on_screen": AI_DISCLOSURE,
    },
]

PERSONA_WARDROBE: dict[str, dict[str, str]] = {
    "SageGFE-001": {
        "wardrobe": "cream knit sweater, high-neck blouse — fully clothed smart-casual",
        "avatar_prompt": (
            "Sage — synthetic companion, chest-up medium shot, 16:9. "
            "Clearly adult 26-year-old Japanese woman, bookish slim build, straight black hair, "
            "thoughtful dark eyes, pale skin. Fully clothed smart-casual — cream knit sweater over "
            "high-neck blouse, relaxed on linen sofa in modern apartment living room. "
            "Warm friendly check-in energy, supportive friend not romantic, PG editorial framing, "
            "no suggestive angles, no swimwear, no lingerie, no bedroom intimacy staging. "
            "Soft window daylight 5200K, lifestyle SFW, no real person likeness, synthetic companion only."
        ),
        "continuity_extra": "cream knit sweater",
    },
    "VioletGFE-001": {
        "wardrobe": "dusty rose cardigan, white crew-neck tee, high-waist jeans — fully clothed smart-casual",
        "avatar_prompt": (
            "Violet — synthetic companion, chest-up medium shot, 16:9. "
            "Clearly adult 22-year-old Japanese-Brazilian woman, dancer build, violet-tinted black curls, "
            "lilac-brown eyes, warm caramel skin, wide friendly smile. Fully clothed smart-casual — "
            "dusty rose cardigan over white crew-neck tee, high-waist jeans, relaxed on linen sofa "
            "in modern apartment living room. Warm joyful check-in energy, supportive friend not romantic, "
            "PG editorial framing, no suggestive angles, no swimwear, no lingerie, no bedroom intimacy staging. "
            "Soft window daylight 5200K, lifestyle SFW, no real person likeness, synthetic companion only."
        ),
        "continuity_extra": "dusty rose cardigan, white tee",
    },
}


@dataclass
class PersonaConfig:
    actor_id: str
    stage_name: str
    identity_anchor: str
    slug: str
    prod_dir: Path
    resolution: str
    wardrobe: str
    avatar_prompt: str
    continuity_extra: str
    voice_suffix: str


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


def resolve_persona(actor_id: str, resolution: str = "720p") -> PersonaConfig:
    registry = json.loads(CASTING_REGISTRY.read_text(encoding="utf-8"))
    actor = _find_actor(registry, actor_id)
    if actor["age_locked"] < 21:
        raise RuntimeError(f"{actor_id} fails 21+ compliance")
    if actor["reference_image_status"] != "plate_locked":
        raise RuntimeError(f"{actor_id} casting plate not locked")

    stage = actor["stage_name"].lower()
    res_tag = resolution.replace("p", "p") if resolution != "720p" else ""
    slug = f"gfe_companion_{stage}_proof_{res_tag}_v1" if res_tag else f"gfe_companion_{stage}_proof_v1"
    slug = slug.replace("__", "_")

    wardrobe_info = PERSONA_WARDROBE.get(actor_id, {
        "wardrobe": "smart-casual sweater and blouse — fully clothed",
        "avatar_prompt": (
            f"{actor['stage_name']} — synthetic companion, chest-up medium shot, 16:9. "
            f"Clearly adult {actor['age_locked']}-year-old woman, fully clothed smart-casual on linen sofa "
            f"in modern apartment. Warm friendly check-in, PG SFW, no suggestive framing, "
            f"synthetic companion only."
        ),
        "continuity_extra": "smart-casual wardrobe",
    })

    voice_notes = actor.get("voice_spec", {}).get("prompt_suffix") or actor.get("voice_spec", {}).get("notes", "")
    voice_suffix = (
        f"{voice_notes}, warm approachable conversational voice, attentive listener energy, "
        "natural breath, synthetic companion only"
    )

    return PersonaConfig(
        actor_id=actor_id,
        stage_name=actor["stage_name"],
        identity_anchor=f"@{actor_id}",
        slug=slug,
        prod_dir=WORKSPACE / "STUDIO" / "Productions" / "Companion" / f"{slug}_longform_v1",
        resolution=resolution,
        wardrobe=wardrobe_info["wardrobe"],
        avatar_prompt=wardrobe_info["avatar_prompt"],
        continuity_extra=wardrobe_info["continuity_extra"],
        voice_suffix=voice_suffix,
    )


def generate_companion_avatar(
    client: Any,
    actor: dict[str, Any],
    persona: PersonaConfig,
    set_url: str,
    refs_dir: Path,
) -> dict[str, Any]:
    slug = persona.stage_name.lower()
    path = refs_dir / f"{slug}_companion_avatar_reference.jpg"
    meta_path = path.with_suffix(".json")
    if path.exists() and path.stat().st_size > 5000 and meta_path.is_file():
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        if meta.get("url"):
            print("[avatar] reusing locked companion reference")
            return {**meta, "path": str(path), "reused": True}

    casting_path = WORKSPACE / actor["reference_image_primary"]
    if not casting_path.is_file():
        casting_path = WORKSPACE / actor["reference_image_primary"].replace("/", "\\")

    print("[avatar] generating companion avatar from casting plate + apartment set…")
    uploaded = client.files.upload(str(casting_path))
    pub = client.files.create_public_url(uploaded.id)
    casting_url = getattr(pub, "public_url", None) or pub.public_url

    resp = client.image.sample(
        prompt=persona.avatar_prompt,
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
        "prompt": persona.avatar_prompt,
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


def write_identity_lock(
    persona: PersonaConfig,
    avatar: dict[str, Any],
    actor: dict[str, Any],
    set_meta: dict[str, Any],
) -> Path:
    voice = actor.get("voice_spec", {})
    lock = {
        "production": persona.slug,
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
            "identity_anchor": persona.identity_anchor,
            "wardrobe": persona.wardrobe,
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
            "prompt_suffix": persona.voice_suffix,
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
            "resolution": persona.resolution,
            "aspect_ratio": "16:9",
        },
    }
    path = persona.prod_dir / f"{persona.stage_name.lower()}_companion_identity_lock.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(lock, indent=2, ensure_ascii=False), encoding="utf-8")
    return path


def build_script(
    persona: PersonaConfig,
    identity_lock: Path,
    avatar: dict[str, Any],
    actor: dict[str, Any],
) -> Path:
    identity_continuity = (
        f"CONTINUITY LOCK {persona.identity_anchor}: identical companion face, {persona.continuity_extra}, "
        "modern apartment sofa set, same eye-line to camera — seamless continuation of prior take, zero jump cut."
    )

    script = build_longform_script(
        FORMAT_ID,
        concept=f"Warm SFW companion check-in proof — {persona.stage_name} persona lane validation ({persona.resolution})",
        slug=persona.slug,
        title=f"STUDIO Companion Proof — {persona.stage_name} SFW Check-In ({persona.resolution})",
        beats=BEATS,
        set_id=SET_ID,
        style_id=STYLE_ID,
    )

    for shot in script["shots"]:
        vp = shot["video_prompt"]
        vp = vp.replace("CONTINUITY LOCK @Companion-001:", f"CONTINUITY LOCK {persona.identity_anchor}:")
        if persona.identity_anchor not in vp:
            vp = f"{identity_continuity} {vp}"
        vp += " SFW PG only — fully clothed, no suggestive framing, no lingerie, supportive friend energy."
        if shot.get("on_screen"):
            vp += f" On-screen lower-third overlay text: {shot['on_screen']}"
        shot["video_prompt"] = vp

    script["production_dir"] = f"Studio/Productions/Companion/{persona.slug}_longform_v1"
    script["production_meta"]["identity_anchor"] = persona.identity_anchor
    script["production_meta"]["talent_id"] = persona.actor_id
    script["production_meta"]["age_locked"] = actor["age_locked"]
    script["production_meta"]["casting_plate"] = actor["reference_image_primary"]
    script["production_meta"]["ai_disclosure"] = AI_DISCLOSURE
    script["config"]["resolution"] = persona.resolution
    script["config"].update({
        "use_identity_lock": False,
        "identity_lock": str(identity_lock),
        "avatar_reference": avatar["path"],
        "avatar_url": avatar["url"],
        "set_reference": "Studio/Pipeline/references/modern_apartment_reference.jpg",
        "voice_suffix": persona.voice_suffix,
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
        f"companion lane proof — {persona.stage_name} persona validation",
        f"resolution test: {persona.resolution}",
    ]

    out = persona.prod_dir / f"{persona.slug}_script.json"
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
    return subprocess.call(cmd, cwd=str(WORKSPACE))


def copy_deliverables(persona: PersonaConfig) -> None:
    david_out = WORKSPACE / "DAVID" / "productions" / f"{persona.slug}_longform_v1"
    studio_out = persona.prod_dir / "output"
    studio_out.mkdir(parents=True, exist_ok=True)
    mp4_src = david_out / "output" / f"david_{persona.slug}_seamless_v1.mp4"
    qa_src = david_out / "qa_report.json"
    if mp4_src.is_file():
        shutil_target = studio_out / f"studio_{persona.slug}_seamless_v1.mp4"
        import shutil
        shutil.copy2(mp4_src, shutil_target)
        print(f"[deliver] MP4 → {shutil_target}")
    if qa_src.is_file():
        import shutil
        shutil.copy2(qa_src, studio_out / "qa_report.json")
        print(f"[deliver] QA → {studio_out / 'qa_report.json'}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Build + render companion lane proof")
    parser.add_argument("--actor", default="SageGFE-001", help="GFE roster actor_id (plate_locked, 21+)")
    parser.add_argument("--resolution", default="720p", choices=["480p", "720p"], help="Video resolution")
    parser.add_argument("--build-only", action="store_true", help="Build script/avatar only, no render")
    args = parser.parse_args()

    if args.actor == "SageGFE-001" and args.resolution == "720p" and len(sys.argv) == 1:
        pass  # backward-compatible default: Sage 720p

    import xai_sdk

    persona = resolve_persona(args.actor, args.resolution)
    if persona.actor_id == "SageGFE-001" and args.resolution == "720p":
        persona = resolve_persona("SageGFE-001", "720p")
        persona.slug = "gfe_companion_sage_proof_v1"
        persona.prod_dir = WORKSPACE / "STUDIO" / "Productions" / "Companion" / "gfe_companion_sage_proof_v1_longform_v1"

    token = os.environ.get("XAI_API_KEY") or _load_grok_token()
    os.environ["XAI_API_KEY"] = token
    client = xai_sdk.Client(api_key=token)

    registry = json.loads(CASTING_REGISTRY.read_text(encoding="utf-8"))
    actor = _find_actor(registry, persona.actor_id)

    set_meta = json.loads(SET_REF_META.read_text(encoding="utf-8"))
    refs_dir = persona.prod_dir / "references"
    refs_dir.mkdir(parents=True, exist_ok=True)

    avatar = generate_companion_avatar(client, actor, persona, set_meta["url"], refs_dir)
    lock_path = write_identity_lock(persona, avatar, actor, set_meta)
    script_path = build_script(persona, lock_path, avatar, actor)

    manifest = {
        "built_at": datetime.now(timezone.utc).isoformat(),
        "lane": "companion",
        "format_id": FORMAT_ID,
        "template_ref": "#98",
        "set_style_ref": "#99",
        "talent": persona.actor_id,
        "resolution": persona.resolution,
        "set_id": SET_ID,
        "style_id": STYLE_ID,
        "script": str(script_path),
        "identity_lock": str(lock_path),
        "avatar": avatar["path"],
        "ai_disclosure": AI_DISCLOSURE,
    }
    (persona.prod_dir / "build_manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(json.dumps(manifest, indent=2))

    if args.build_only:
        return 0

    rc = render(script_path)
    if rc == 0:
        copy_deliverables(persona)
    return rc


if __name__ == "__main__":
    raise SystemExit(main())