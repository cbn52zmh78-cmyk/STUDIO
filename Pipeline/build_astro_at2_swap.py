#!/usr/bin/env python3
"""ACTORS #157 — prove @2 plug-and-play on fixed black-hole scaffold.

Swap only the science visualization plate (@2) across astro subjects; render each at 480p.
Marginal work per swap: plate path + slug/title metadata — scaffold shots/prompts unchanged.
"""
from __future__ import annotations

import argparse
import copy
import json
import os
import subprocess
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

WORKSPACE = Path(__file__).resolve().parents[2]
SCAFFOLD = WORKSPACE / "STUDIO" / "Pipeline" / "scaffolds" / "black_hole_at2_swap_scaffold.json"
PLATE_LIBRARY = WORKSPACE / "Science" / "reference_plates" / "science_plate_library_v1.json"
RENDER = WORKSPACE / "DAVID" / "scripts" / "render_longform.py"
SCRIPTS_OUT = WORKSPACE / "DAVID" / "scripts" / "longform_scripts"
PROD_ROOT = WORKSPACE / "STUDIO" / "Productions" / "Science" / "actors_157_at2_swap"

DEFAULT_SWAPS = ["neutron-star", "nebula", "galaxy"]
BASELINE_SLUG = "black-hole"


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
    req = urllib.request.Request(url, headers={"User-Agent": "STUDIO-astro-at2-swap/1.0"})
    with urllib.request.urlopen(req, timeout=300) as r:
        dest.write_bytes(r.read())


def load_plate_by_slug(slug: str) -> dict[str, Any]:
    lib = json.loads(PLATE_LIBRARY.read_text(encoding="utf-8"))
    for plate in lib["plates"]:
        if plate["slug"] == slug:
            return plate
    astro = [p["slug"] for p in lib["plates"] if p.get("domain") == "astro"]
    raise KeyError(f"Unknown astro plate slug '{slug}'. Available: {', '.join(astro)}")


def ensure_plate(client: Any, plate: dict[str, Any], force: bool = False) -> dict[str, Any]:
    spec = plate["plate_spec"]
    ref_rel = spec["reference_file"]
    ref_path = WORKSPACE / ref_rel.replace("/", os.sep)
    meta_path = ref_path.with_suffix(".json")

    if ref_path.is_file() and ref_path.stat().st_size > 5000 and meta_path.is_file() and not force:
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        if meta.get("url"):
            print(f"[plate] reusing {plate['plate_id']} → {ref_path.name}")
            return {**meta, "path": str(ref_path), "reused": True}

    print(f"[plate] generating {plate['plate_id']} ({plate['subject']})…")
    resp = client.image.sample(
        prompt=spec["imagine_prompt"],
        model="grok-imagine-image-quality",
    )
    _download(resp.url, ref_path)
    locked_at = datetime.now(timezone.utc).isoformat()
    meta = {
        "plate_id": plate["plate_id"],
        "slug": plate["slug"],
        "subject": plate["subject"],
        "path": str(ref_path),
        "url": resp.url,
        "prompt": spec["imagine_prompt"],
        "plate_lock_verbatim": spec["plate_lock_verbatim"],
        "status": "PLATE_LOCKED",
        "locked_at": locked_at,
        "issue": 157,
        "reused": False,
    }
    meta_path.write_text(json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8")
    return meta


def build_swap_script(
    scaffold: dict[str, Any],
    plate: dict[str, Any],
    plate_meta: dict[str, Any],
) -> tuple[dict[str, Any], Path]:
    slug = f"actors_157_at2_swap_{plate['slug']}_480p_v1"
    prod_dir = PROD_ROOT / f"{slug}_longform_v1"

    script: dict[str, Any] = {
        "slug": slug,
        "title": f"ACTORS #157 — @2 Swap Demo ({plate['subject']}) 480p",
        "format_id": scaffold["format_id"],
        "target_seconds": sum(s["duration"] for s in scaffold["shots"]),
        "production_dir": str(prod_dir).replace("\\", "/"),
        "config": {
            "model_video": "grok-imagine-video-1.5",
            "resolution": scaffold["resolution"],
            "aspect_ratio": "16:9",
            "voice_suffix": (
                "clear enthusiastic science communicator voice, precise but accessible diction, "
                "synthetic presenter only"
            ),
            "use_identity_lock": False,
            "avatar_reference": (
                "STUDIO/Cast/actors_roster/male/north_america/Julian_Cross/"
                "01_casting_shots/casting_turnaround_v1.jpg"
            ),
            "set_reference": "STUDIO/Pipeline/references/seamless_neutral_grey_reference.jpg",
            "visualization_reference": plate_meta["path"].replace("\\", "/"),
            "visualization_url": plate_meta.get("url"),
            "seamless": {
                "primary": "extend",
                "xfade_s": 0.2,
                "match_color": True,
                "cut_on_motion": True,
                "loudnorm": True,
                "pin_audio_sync": True,
                "reground_interval": 2,
                "magenta_clamp": False,
            },
        },
        "shots": copy.deepcopy(scaffold["shots"]),
        "provenance_card": {
            **scaffold["provenance_card"],
            "title": f"Sources — {plate['subject']}",
            "subtitle": plate["domain"],
            "sources": [
                {
                    "citation": plate["source"]["primary_citation"],
                    "url": plate["source"].get("url"),
                    "type": "primary",
                }
            ],
        },
        "qa_rules": copy.deepcopy(scaffold["qa_rules"]),
        "production_meta": {
            "issue": 157,
            "scaffold_id": scaffold["scaffold_id"],
            "swap_slot": scaffold["swap_slot"],
            "plate_id": plate["plate_id"],
            "plate_slug": plate["slug"],
            "plate_subject": plate["subject"],
            "plate_lock_verbatim": plate["plate_spec"]["plate_lock_verbatim"],
            "principle_set": plate.get("principle_set"),
            "swap_delta_fields": scaffold["swap_fields_only"],
            "unchanged_fields": scaffold["unchanged_across_swaps"],
            "baseline_plate_slug": scaffold["default_plate_slug"],
        },
        "guardrails": [
            "ACTORS #157 — @2 plug-and-play proof on fixed black-hole scaffold",
            f"@2 plate swap only: {plate['plate_id']}",
            "prompt uses 'see attached render' only for @2 per STUDIO_Production_Canon_v1.0 §2",
            "illustrative visualization — NOT TO SCALE",
        ],
    }

    script_path = prod_dir / f"{slug}_script.json"
    script_path.parent.mkdir(parents=True, exist_ok=True)
    script_path.write_text(json.dumps(script, indent=2, ensure_ascii=False), encoding="utf-8")

    dav_script = SCRIPTS_OUT / f"{slug}_script.json"
    dav_script.write_text(json.dumps(script, indent=2, ensure_ascii=False), encoding="utf-8")
    return script, script_path


def render_script(script_path: Path) -> int:
    cmd = [
        sys.executable,
        str(RENDER),
        str(script_path),
        "--seamless",
        "--match-color",
        "--cut-on-motion",
    ]
    print("[render]", " ".join(cmd))
    return subprocess.call(cmd, cwd=str(WORKSPACE))


def copy_deliverables(slug: str) -> None:
    import shutil

    prod_dir = PROD_ROOT / f"{slug}_longform_v1"
    studio_out = prod_dir / "output"
    studio_out.mkdir(parents=True, exist_ok=True)

    candidates = [
        prod_dir / "output" / f"studio_{slug}_seamless_v1.mp4",
        prod_dir / "output" / f"david_{slug}_seamless_v1.mp4",
        WORKSPACE / "DAVID" / "productions" / f"{slug}_longform_v1" / "output" / f"david_{slug}_seamless_v1.mp4",
    ]
    for src in candidates:
        if src.is_file():
            dst = studio_out / f"studio_{slug}_seamless_v1.mp4"
            if src.resolve() != dst.resolve():
                shutil.copy2(src, dst)
            print(f"[deliver] MP4 → {dst}")
            break

    for qa_src in (
        prod_dir / "qa_report.json",
        WORKSPACE / "DAVID" / "productions" / f"{slug}_longform_v1" / "qa_report.json",
    ):
        if qa_src.is_file():
            qa_dst = studio_out / "qa_report.json"
            if qa_src.resolve() != qa_dst.resolve():
                shutil.copy2(qa_src, qa_dst)
            print(f"[deliver] QA → {qa_dst}")
            break


def write_swap_manifest(results: list[dict[str, Any]]) -> Path:
    scaffold_data = json.loads(SCAFFOLD.read_text(encoding="utf-8"))
    out = PROD_ROOT / "actors_157_at2_swap_manifest.json"
    out.parent.mkdir(parents=True, exist_ok=True)

    existing: dict[str, Any] = {}
    if out.is_file():
        existing = json.loads(out.read_text(encoding="utf-8"))
    demos_by_slug = {d["slug"]: d for d in existing.get("demos", []) if d.get("slug")}
    for row in results:
        if row.get("slug"):
            demos_by_slug[row["slug"]] = {**demos_by_slug.get(row["slug"], {}), **row}

    demos = sorted(demos_by_slug.values(), key=lambda d: d.get("plate_slug", ""))
    manifest = {
        "issue": 157,
        "task": "ACTORS @2 plug-and-play — fixed black-hole scaffold",
        "scaffold": str(SCAFFOLD),
        "built_at": datetime.now(timezone.utc).isoformat(),
        "resolution": "480p",
        "swap_count": len(demos),
        "all_qa_pass": all(d.get("qa_pass") for d in demos if d.get("qa_pass") is not None),
        "marginal_work_per_swap": scaffold_data["swap_fields_only"],
        "demos": demos,
    }
    out.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description="ACTORS #157 — @2 astro plate swap demos")
    parser.add_argument(
        "--plates",
        default=",".join(DEFAULT_SWAPS),
        help="Comma-separated astro plate slugs to swap (default: neutron-star,nebula,galaxy)",
    )
    parser.add_argument("--resolution", default="480p", choices=["480p", "720p"])
    parser.add_argument("--plates-only", action="store_true", help="Generate @2 plates only")
    parser.add_argument("--build-only", action="store_true", help="Build scripts only, no render")
    parser.add_argument("--skip-plates", action="store_true", help="Reuse existing plate JPGs")
    parser.add_argument("--force-plates", action="store_true")
    parser.add_argument("--include-baseline", action="store_true", help="Also render baseline black-hole @2")
    args = parser.parse_args()

    scaffold = json.loads(SCAFFOLD.read_text(encoding="utf-8"))
    scaffold["resolution"] = args.resolution

    slugs = [s.strip() for s in args.plates.split(",") if s.strip()]
    if args.include_baseline and BASELINE_SLUG not in slugs:
        slugs.insert(0, BASELINE_SLUG)

    import xai_sdk

    token = os.environ.get("XAI_API_KEY") or _load_grok_token()
    os.environ["XAI_API_KEY"] = token
    client = xai_sdk.Client(api_key=token)

    results: list[dict[str, Any]] = []
    exit_code = 0

    for slug in slugs:
        plate = load_plate_by_slug(slug)
        if args.skip_plates:
            ref_path = WORKSPACE / plate["plate_spec"]["reference_file"].replace("/", os.sep)
            meta_path = ref_path.with_suffix(".json")
            meta = json.loads(meta_path.read_text(encoding="utf-8")) if meta_path.is_file() else {}
            plate_meta = {"path": str(ref_path), "url": meta.get("url"), "reused": True}
            if not ref_path.is_file():
                plate_meta = ensure_plate(client, plate, force=args.force_plates)
        else:
            plate_meta = ensure_plate(client, plate, force=args.force_plates)

        if args.plates_only:
            results.append({"plate_slug": slug, "plate_id": plate["plate_id"], "plate_path": plate_meta["path"]})
            continue

        script, script_path = build_swap_script(scaffold, plate, plate_meta)
        demo_slug = script["slug"]
        result: dict[str, Any] = {
            "plate_slug": slug,
            "plate_id": plate["plate_id"],
            "plate_subject": plate["subject"],
            "plate_path": plate_meta["path"],
            "script": str(script_path),
            "slug": demo_slug,
        }

        if args.build_only:
            results.append(result)
            continue

        rc = render_script(script_path)
        result["render_exit_code"] = rc
        if rc == 0:
            copy_deliverables(demo_slug)
            qa_path = PROD_ROOT / f"{demo_slug}_longform_v1" / "output" / "qa_report.json"
            if qa_path.is_file():
                qa = json.loads(qa_path.read_text(encoding="utf-8"))
                result["qa_pass"] = qa.get("pass")
                result["qa_issues"] = qa.get("issues", [])
            else:
                result["qa_pass"] = None
        else:
            exit_code = rc
        results.append(result)

    manifest_path = write_swap_manifest(results)
    print(json.dumps({"manifest": str(manifest_path), "demos": results}, indent=2))
    if any(r.get("qa_pass") is False for r in results):
        return 1
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())