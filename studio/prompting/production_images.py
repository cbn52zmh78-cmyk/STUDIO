"""Production image prompt templates — setting plates, head composites, and VFX-ready assets."""
from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any


class ImageAssetType(str, Enum):
    SETTING_PLATE = "setting_plate"
    HEAD_COMPOSITE = "head_composite"
    COSTUME_PLATE = "costume_plate"
    PROP_PLATE = "prop_plate"
    ENVIRONMENT_ESTABLISHING = "environment_establishing"
    LIGHTING_REFERENCE = "lighting_reference"
    CROWD_PLATE = "crowd_plate"
    MATTE_EXTENSION = "matte_extension"
    TEXTURE_SURFACE = "texture_surface"
    CHARACTER_TURNAROUND = "character_turnaround"
    TURNAROUND_SHEET_3VIEW = "turnaround_sheet_3view"


# Studio defaults — non-negotiable unless user overrides in prompt.
DEFAULT_ASPECT_RATIO = "16:9"
CASTING_STANCE = (
    "Standing upright, arms at their sides, hands free of any objects."
)

CASTING_SHOT_OPENER = "GENERATE 3D renders of back, side and front profiles of"

CASTING_SHOT_FRAMING_TAIL = (
    "Single 16:9 turnaround reference sheet on solid pure white background. "
    "LEFT panel: side profile. CENTER panel: front view. RIGHT panel: back view. "
    "FULL-LENGTH WIDE SHOT in every panel — camera pulled back, entire body head to toe "
    "with headroom and footroom, feet visible on the floor. "
    "NOT a close-up. NOT a medium close-up. NOT a medium shot. NOT a bust shot. "
    "NOT waist-up. NOT knee-up. NOT cropped. "
    "Fully covered high-waisted bikini top and matching bikini bottoms in all three views — "
    "fully clothed casting wardrobe, NOT topless, NOT nude, NOT implied nudity. "
    "Standing upright, arms at their sides, hands free of any objects. "
    "Same person, identical proportions, hairstyle, and wardrobe in all three panels. "
    "Even soft studio lighting, full-length body illumination. "
    "Hyper-realistic photoreal 3D character reference render. No text, no labels, no props."
)

# Casting / profile shots always use CASTING_STANCE in every view.
CASTING_PROFILE_TYPES: frozenset[ImageAssetType] = frozenset(
    {
        ImageAssetType.CHARACTER_TURNAROUND,
        ImageAssetType.TURNAROUND_SHEET_3VIEW,
        ImageAssetType.HEAD_COMPOSITE,
        ImageAssetType.COSTUME_PLATE,
    }
)


def aspect_ratio_for(
    asset_type: ImageAssetType, override: str | None = None
) -> str:
    return override or DEFAULT_ASPECT_RATIO


TEMPLATE_SUFFIXES: dict[ImageAssetType, str] = {
    ImageAssetType.SETTING_PLATE: (
        "Empty environment plate for compositing. No people, no animals, no text, no logos. "
        "Clean sightlines, stable geometry, neutral depth cues, production-ready for VFX plate replacement. "
        "Photoreal cinematic lighting, high detail, subtle atmospheric haze."
    ),
    ImageAssetType.HEAD_COMPOSITE: (
        "Casting composite plate. Neutral expression, eyes to camera, even key light with soft fill, "
        "minimal shadows on face, plain muted background, sharp focus on eyes and skin texture, "
        "no jewelry clutter unless specified, no text, identity-consistent features for later compositing."
    ),
    ImageAssetType.COSTUME_PLATE: (
        "Casting costume reference plate. Garment shown clearly on live model, even studio lighting, "
        "fabric weave and trim visible, neutral background, no text, catalog clarity."
    ),
    ImageAssetType.PROP_PLATE: (
        "Isolated prop on neutral surface. Object centered, soft shadow, macro detail on materials, "
        "no hands, no text, product-style clarity for compositing."
    ),
    ImageAssetType.ENVIRONMENT_ESTABLISHING: (
        "Establishing environment shot with full atmosphere and depth. Cinematic composition, motivated lighting, "
        "layered foreground midground background, production value, photoreal."
    ),
    ImageAssetType.LIGHTING_REFERENCE: (
        "Same location and camera position as setting plate, lighting-only variation. "
        "Document light direction, color temperature, and shadow behavior for match-back."
    ),
    ImageAssetType.CROWD_PLATE: (
        "Background crowd plate. Figures small or mid-distance, soft detail, no hero faces, "
        "repeatable extras, depth layering, no readable text."
    ),
    ImageAssetType.MATTE_EXTENSION: (
        "Matte painting extension plate. Sky, horizon, distant architecture or landscape, "
        "seam-friendly edges, atmospheric perspective, no foreground talent."
    ),
    ImageAssetType.TEXTURE_SURFACE: (
        "Macro texture surface plate. Fill frame with material detail, even lighting, "
        "tileable impression, no text, high micro-contrast."
    ),
    ImageAssetType.CHARACTER_TURNAROUND: (
        "Casting character turnaround. Full body, clear silhouette, costume and proportions readable, "
        "solid white background, photoreal."
    ),
    ImageAssetType.TURNAROUND_SHEET_3VIEW: (
        "Casting turnaround sheet on one 16:9 canvas. Left: side profile. Center: front view. "
        "Right: back view. Same person, identical proportions, hairstyle, and wardrobe in all three. "
        "MANDATORY full body head-to-toe in every view — feet, legs, hips, torso, arms, and head "
        "fully visible; wide framing; no close-ups, no bust shots, no cropping. "
        "Solid white background, even spacing, no text labels, VFX/editor 360 reference for compositing."
    ),
}


@dataclass
class ProductionImageRequest:
    asset_type: ImageAssetType
    subject: str
    project: str = "untitled"
    era_style: str = ""
    lighting: str = ""
    camera: str = ""
    notes: str = ""
    reference_images: list[str] = field(default_factory=list)
    character_token: str = ""
    aspect_ratio: str | None = None  # None → DEFAULT_ASPECT_RATIO (16:9)


def build_casting_shot_prompt(person_description: str) -> str:
    """One-call 3-view casting turnaround from a person description."""
    person = person_description.strip().rstrip(".")
    return f"{CASTING_SHOT_OPENER} {person}. {CASTING_SHOT_FRAMING_TAIL}"


def build_prompt(req: ProductionImageRequest) -> str:
    parts: list[str] = []
    if req.character_token:
        parts.append(f"{req.character_token} -")
    parts.append(req.subject.strip())
    if req.era_style:
        parts.append(req.era_style.strip())
    if req.lighting:
        parts.append(f"Lighting: {req.lighting.strip()}")
    if req.camera:
        parts.append(f"Camera: {req.camera.strip()}")
    if req.asset_type in CASTING_PROFILE_TYPES:
        parts.append(CASTING_STANCE)
    parts.append(TEMPLATE_SUFFIXES[req.asset_type])
    if req.notes:
        parts.append(req.notes.strip())
    return " ".join(parts)


def build_pack(
    requests: list[ProductionImageRequest],
    *,
    project: str | None = None,
) -> dict[str, Any]:
    generated = datetime.now().strftime("%Y-%m-%d_%H-%M")
    assets = []
    for i, req in enumerate(requests, start=1):
        prompt = build_prompt(req)
        assets.append(
            {
                "id": f"asset_{i:02d}",
                "asset_type": req.asset_type.value,
                "aspect_ratio": aspect_ratio_for(req.asset_type, req.aspect_ratio),
                "project": project or req.project,
                "character_token": req.character_token,
                "reference_images": req.reference_images,
                "prompt": prompt,
                "compositing_notes": _compositing_notes(req.asset_type),
            }
        )
    return {
        "version": "1.0",
        "generated": generated,
        "project": project or (requests[0].project if requests else "untitled"),
        "master_constraints": {
            "aspect_ratio": DEFAULT_ASPECT_RATIO,
            "casting_stance": CASTING_STANCE,
        },
        "workflow": "Studio production image pack — generate base with image_gen; iterate with image_edit; animate with image_to_video",
        "assets": assets,
    }


def _compositing_notes(asset_type: ImageAssetType) -> str:
    notes = {
        ImageAssetType.SETTING_PLATE: "Use as background plate; match lens height and horizon to talent comp.",
        ImageAssetType.HEAD_COMPOSITE: "Extract head; match key/fill direction to scene lighting; preserve eye line.",
        ImageAssetType.COSTUME_PLATE: "Reference for wardrobe continuity; not a final comp element.",
        ImageAssetType.PROP_PLATE: "Cut out prop; match scene grade and shadow direction.",
        ImageAssetType.ENVIRONMENT_ESTABLISHING: "Hero environment; may include talent in frame.",
        ImageAssetType.LIGHTING_REFERENCE: "Do not comp directly — use to match talent lighting.",
        ImageAssetType.CROWD_PLATE: "Place behind hero action; defocus if needed.",
        ImageAssetType.MATTE_EXTENSION: "Blend at horizon or architecture seam.",
        ImageAssetType.TEXTURE_SURFACE: "Overlay or projection map for set extension.",
        ImageAssetType.CHARACTER_TURNAROUND: "Lock proportions before head/body composite workflow.",
        ImageAssetType.TURNAROUND_SHEET_3VIEW: "Editor uses all three views to reconstruct 360 model in video comp.",
    }
    return notes[asset_type]


def save_pack(pack: dict[str, Any], output_dir: Path, stem: str | None = None) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    name = stem or f"image_pack_{pack['project'].replace(' ', '_')}_{pack['generated']}"
    path = output_dir / f"{name}.json"
    path.write_text(json.dumps(pack, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return path