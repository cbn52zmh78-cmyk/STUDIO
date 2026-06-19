#!/usr/bin/env python3
"""Generate and lock STUDIO Set_Library_v1 environment reference plates.

Produces empty environment plates (no people) for every non-Archive set,
writes sidecar metadata, and updates Set_Library_v1.json with lock status.
"""
from __future__ import annotations

import json
import os
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
PIPELINE = ROOT / "Studio" / "Pipeline"
REFS_DIR = PIPELINE / "references"
LIBRARY_PATH = PIPELINE / "Set_Library_v1.json"

SET_SPECS: dict[str, dict[str, str]] = {
    "@Set-Studio-Interior-001": {
        "filename": "studio_interior_cyclorama_reference.jpg",
        "prompt": (
            "Editorial fashion studio interior — seamless white-to-pale-grey cyclorama curve, "
            "polished white resin floor, minimal props, optional grip stand at frame edge. "
            "16:9 cinematic wide shot, no people, empty set. High-key 5600K even wrap lighting, "
            "pure neutral white backdrop, soft floor-to-wall sweep, fashion editorial prestige "
            "aesthetic, photoreal cinematic lighting, SFW."
        ),
    },
    "@Set-Modern-Apartment-001": {
        "filename": "modern_apartment_reference.jpg",
        "prompt": (
            "Contemporary open-plan apartment interior, 16:9 cinematic wide shot, no people. "
            "Neutral linen sofa, oak hardwood floor, large window camera-left with sheer curtain "
            "diffusion, minimal decor, soft kitchen blur in background, single potted plant. "
            "Soft window daylight 5200K, lifestyle editorial aesthetic, warm white walls, "
            "photoreal cinematic lighting, SFW."
        ),
    },
    "@Set-Outdoor-Golden-001": {
        "filename": "outdoor_golden_hour_reference.jpg",
        "prompt": (
            "Outdoor location at golden hour, 16:9 cinematic wide shot, no people. "
            "Low sun camera-right at 15 degrees elevation, long warm shadows, sky gradient "
            "amber to pale blue, natural tree line background, textured ground path. "
            "Warm 4000K sunlight, fashion editorial location shoot aesthetic, "
            "photoreal cinematic lighting, SFW."
        ),
    },
    "@Set-Outdoor-Overcast-001": {
        "filename": "outdoor_overcast_reference.jpg",
        "prompt": (
            "Outdoor urban park path or quiet tree-lined street, 16:9 cinematic wide shot, "
            "no people. Soft overcast sky with even diffusion, neutral grey clouds, "
            "pavement and natural foliage, gentle ambient 6000K wrap light. "
            "Lifestyle editorial aesthetic, natural neutral tones, photoreal cinematic lighting, SFW."
        ),
    },
    "@Set-Seamless-Neutral-001": {
        "filename": "seamless_neutral_grey_reference.jpg",
        "prompt": (
            "Professional photo studio with medium neutral grey seamless paper backdrop, "
            "infinite curve, no horizon line visible. 16:9 cinematic wide shot, no people. "
            "Bilateral soft 5500K key lighting, mid-grey backdrop, subtle floor sweep falloff. "
            "Fashion catalog aesthetic, photoreal cinematic lighting, SFW."
        ),
    },
    "@Set-Warehouse-Industrial-001": {
        "filename": "warehouse_industrial_reference.jpg",
        "prompt": (
            "Industrial loft interior, 16:9 cinematic wide shot, no people. "
            "Exposed brick wall, concrete floor, large factory window grid camera-left, "
            "metal ceiling beams, subtle dust motes in directional 4800K window light. "
            "Deep shadow pockets, editorial fashion location aesthetic, photoreal cinematic lighting, SFW."
        ),
    },
    "@Set-Rooftop-Urban-001": {
        "filename": "rooftop_urban_dusk_reference.jpg",
        "prompt": (
            "City rooftop at dusk, 16:9 cinematic wide shot, no people. "
            "Concrete parapet line in foreground, soft bokeh city skyline behind, "
            "sky gradient warm amber to deep indigo, dusk ambient 4300K. "
            "Fashion editorial rooftop shoot aesthetic, tungsten city lights as soft bokeh only, "
            "photoreal cinematic lighting, SFW."
        ),
    },
}


def _load_grok_token() -> str:
    auth_path = Path.home() / ".grok" / "auth.json"
    if not auth_path.is_file():
        raise RuntimeError("No ~/.grok/auth.json — run grok login or set XAI_API_KEY")
    data = json.loads(auth_path.read_text(encoding="utf-8"))
    entry = next(iter(data.values()))
    token = entry.get("key") or entry.get("access_token")
    if not token:
        raise RuntimeError("Grok auth.json has no token")
    return token


def _download(url: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": "STUDIO-set-refs/1.0"})
    with urllib.request.urlopen(req, timeout=300) as r:
        dest.write_bytes(r.read())


def _load_ref_meta(path: Path) -> dict[str, Any]:
    meta_path = path.with_suffix(".json")
    if meta_path.is_file():
        return json.loads(meta_path.read_text(encoding="utf-8"))
    return {}


def _save_ref_meta(path: Path, data: dict[str, Any]) -> None:
    meta_path = path.with_suffix(".json")
    meta_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def generate_plate(client: Any, set_id: str, spec: dict[str, str], force: bool = False) -> dict[str, Any]:
    path = REFS_DIR / spec["filename"]
    rel_path = f"Studio/Pipeline/references/{spec['filename']}"

    if not force and path.exists() and path.stat().st_size > 5000:
        meta = _load_ref_meta(path)
        if meta.get("url") and meta.get("reference_status") == "plate_locked":
            print(f"[{set_id}] reusing locked plate")
            return {**meta, "path": str(path), "reference_file": rel_path, "reused": True}

    print(f"[{set_id}] generating environment plate…")
    resp = client.image.sample(prompt=spec["prompt"], model="grok-imagine-image-quality")
    _download(resp.url, path)
    locked_at = datetime.now(timezone.utc).isoformat()
    data = {
        "set_id": set_id,
        "path": str(path),
        "reference_file": rel_path,
        "url": resp.url,
        "prompt": spec["prompt"],
        "model": "grok-imagine-image-quality",
        "aspect_ratio": "16:9",
        "reference_status": "plate_locked",
        "locked_at": locked_at,
        "reuse": "environment plate @1 — locked before first assembly",
        "sfw": True,
        "no_people": True,
        "reused": False,
    }
    _save_ref_meta(path, data)
    return data


def update_set_library(results: dict[str, dict[str, Any]]) -> Path:
    library = json.loads(LIBRARY_PATH.read_text(encoding="utf-8"))
    locked_at = datetime.now(timezone.utc).isoformat()

    for set_id, result in results.items():
        entry = library["sets"][set_id]
        entry["reference_file"] = result["reference_file"]
        entry["reference_status"] = "plate_locked"
        entry["reference_locked_at"] = result["locked_at"]
        entry["reference_prompt"] = result["prompt"]
        entry["reference_url"] = result.get("url")
        entry["reference_model"] = result.get("model", "grok-imagine-image-quality")

    library["reference_plates_locked_at"] = locked_at
    library["reference_plates_status"] = "ALL_NON_ARCHIVE_LOCKED"

    LIBRARY_PATH.write_text(json.dumps(library, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return LIBRARY_PATH


def main() -> int:
    import xai_sdk

    force = "--force" in os.sys.argv
    token = os.environ.get("XAI_API_KEY") or _load_grok_token()
    os.environ["XAI_API_KEY"] = token
    client = xai_sdk.Client(api_key=token)

    REFS_DIR.mkdir(parents=True, exist_ok=True)
    results: dict[str, dict[str, Any]] = {}

    for set_id, spec in SET_SPECS.items():
        results[set_id] = generate_plate(client, set_id, spec, force=force)

    lock_path = update_set_library(results)

    manifest = {
        "completed_at": datetime.now(timezone.utc).isoformat(),
        "library": str(lock_path),
        "plates": {
            sid: {
                "file": r["reference_file"],
                "status": r["reference_status"],
                "locked_at": r["locked_at"],
                "reused": r.get("reused", False),
            }
            for sid, r in results.items()
        },
    }
    manifest_path = REFS_DIR / "set_references_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(manifest, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())