#!/usr/bin/env python3
"""Build a production image prompt pack (setting plates, head composites, etc.)."""
import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from studio.prompting.production_images import (  # noqa: E402
    DEFAULT_ASPECT_RATIO,
    ImageAssetType,
    ProductionImageRequest,
    build_pack,
    save_pack,
)


def parse_asset_type(value: str) -> ImageAssetType:
    try:
        return ImageAssetType(value)
    except ValueError as exc:
        valid = ", ".join(t.value for t in ImageAssetType)
        raise argparse.ArgumentTypeError(f"Unknown type '{value}'. Choose: {valid}") from exc


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate Studio production image prompt pack.")
    parser.add_argument("--project", default="untitled", help="Project name")
    parser.add_argument(
        "--type",
        type=parse_asset_type,
        action="append",
        dest="types",
        help="Asset type (repeatable). Default: setting_plate + head_composite",
    )
    parser.add_argument("--subject", help="Scene or subject description")
    parser.add_argument("--era", default="", help="Period / visual style")
    parser.add_argument("--lighting", default="", help="Lighting direction")
    parser.add_argument("--camera", default="", help="Lens / framing")
    parser.add_argument("--token", default="", help="Character token e.g. HENRY THE SECOND (@1)")
    parser.add_argument("--notes", default="", help="Extra prompt notes")
    parser.add_argument(
        "--aspect-ratio",
        default=DEFAULT_ASPECT_RATIO,
        help=f"Image aspect ratio (default: {DEFAULT_ASPECT_RATIO})",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=ROOT / "renders" / "prompt_packs",
        help="Output directory for JSON pack",
    )
    args = parser.parse_args()

    types = args.types or [ImageAssetType.SETTING_PLATE, ImageAssetType.HEAD_COMPOSITE]
    subject = args.subject or "Medieval royal council chamber, stone arches, torchlight"

    requests = [
        ProductionImageRequest(
            asset_type=asset_type,
            subject=subject,
            project=args.project,
            era_style=args.era,
            lighting=args.lighting,
            camera=args.camera,
            notes=args.notes,
            character_token=args.token if asset_type == ImageAssetType.HEAD_COMPOSITE else "",
            aspect_ratio=args.aspect_ratio,
        )
        for asset_type in types
    ]

    pack = build_pack(requests, project=args.project)
    path = save_pack(pack, args.out)
    print(f"✅ Image pack saved → {path}")
    for asset in pack["assets"]:
        print(f"\n[{asset['asset_type']}] {asset['aspect_ratio']}")
        print(asset["prompt"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())