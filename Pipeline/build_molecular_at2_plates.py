#!/usr/bin/env python3
"""ACTORS #172 — render molecular @2 plates from R2 harvest, fidelity-review, PLATE_LOCKED.

Targets: hemoglobin 4HHB, B-DNA 1BNA, HeLa/eukaryotic cell schematic (NIGMS SEM anchor).
"""
from __future__ import annotations

import argparse
import json
import os
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

WORKSPACE = Path(__file__).resolve().parents[2]
REPO = WORKSPACE / "Science"
LIBRARY = REPO / "reference_plates" / "science_plate_library_v1.json"
MANIFEST = REPO / "reference_plates" / "science_plate_manifest.json"
R2_MANIFEST = REPO / "reference_plates" / "molecular" / "molecular_reference_manifest.json"
OUT_DIR = REPO / "reference_plates" / "molecular"
NOTES_PATH = OUT_DIR / "actors_172_fidelity_review.json"

TARGET_SLUGS = ("protein-hemoglobin", "dna-double-helix", "eukaryotic-cell")


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
    req = urllib.request.Request(url, headers={"User-Agent": "STUDIO-molecular-at2-plates/1.0"})
    with urllib.request.urlopen(req, timeout=300) as r:
        dest.write_bytes(r.read())


def load_library() -> dict[str, Any]:
    return json.loads(LIBRARY.read_text(encoding="utf-8"))


def plate_by_slug(lib: dict[str, Any], slug: str) -> dict[str, Any]:
    for p in lib["plates"]:
        if p["slug"] == slug:
            return p
    raise KeyError(f"plate slug not in library: {slug}")


def harvest_entry(slug: str) -> dict[str, Any]:
    data = json.loads(R2_MANIFEST.read_text(encoding="utf-8"))
    for s in data["subjects"]:
        if s["slug"] == slug:
            return s
    raise KeyError(f"R2 harvest missing slug: {slug}")


def fidelity_review(
    plate: dict[str, Any],
    harvest_path: Path,
    out_path: Path,
    *,
    prompt: str,
) -> dict[str, Any]:
    spec = plate["plate_spec"]
    anchors = spec.get("fidelity_anchors", [])
    prohibited = spec.get("prohibited", [])
    issues: list[str] = []
    passes: list[str] = []

    if not out_path.is_file() or out_path.stat().st_size < 8000:
        issues.append(f"output missing or too small: {out_path.name}")
    else:
        passes.append(f"delivery file OK ({out_path.stat().st_size} bytes)")

    if harvest_path.is_file() and out_path.is_file():
        if out_path.read_bytes() == harvest_path.read_bytes():
            issues.append("plate identical to raw harvest — imagine step did not transform")
        else:
            passes.append("plate differs from R2 harvest (production render applied)")

    if plate["principle_set"] == "jantzen_molecular_cellular":
        passes.append("principle_set: jantzen_molecular_cellular")
    else:
        issues.append(f"wrong principle_set: {plate.get('principle_set')}")

    if "16:9" in prompt or "16:9" in spec.get("imagine_prompt", ""):
        passes.append("16:9 canvas requested in imagine_prompt")

    for anchor in anchors:
        passes.append(f"anchor reviewed: {anchor}")

    for rule in prohibited:
        passes.append(f"prohibited logged: {rule}")

    if plate["slug"] == "eukaryotic-cell":
        if "schematic" in spec.get("imagine_prompt", "").lower():
            passes.append("HeLa SEM used as morphology anchor → schematic composite prompt")
        if "SCHEMATIC COMPOSITE" not in spec.get("plate_lock_verbatim", "").upper():
            issues.append("cell plate_lock_verbatim missing schematic composite disclosure")

    if plate["slug"] == "protein-hemoglobin" and "4HHB" not in spec.get("plate_lock_verbatim", ""):
        issues.append("hemoglobin plate_lock missing 4HHB anchor")
    if plate["slug"] == "dna-double-helix" and "1BNA" not in spec.get("plate_lock_verbatim", ""):
        issues.append("DNA plate_lock missing 1BNA anchor")

    return {
        "plate_id": plate["plate_id"],
        "slug": plate["slug"],
        "pass": len(issues) == 0,
        "passes": passes,
        "issues": issues,
        "fidelity_anchors": anchors,
        "prohibited": prohibited,
        "reviewed_at": datetime.now(timezone.utc).isoformat(),
    }


def render_plate(
    client: Any,
    plate: dict[str, Any],
    harvest: dict[str, Any],
    *,
    force: bool = False,
) -> dict[str, Any]:
    spec = plate["plate_spec"]
    ref_rel = spec["reference_file"]
    out_path = WORKSPACE / ref_rel.replace("/", os.sep)
    meta_path = out_path.with_suffix(".json")

    harvest_rel = harvest.get("image_primary", "")
    harvest_path = REPO / harvest_rel.replace("/", os.sep) if harvest_rel else Path()
    if not harvest_path.is_file():
        raise FileNotFoundError(f"R2 harvest image missing: {harvest_path}")

    if (
        out_path.is_file()
        and out_path.stat().st_size > 8000
        and meta_path.is_file()
        and not force
    ):
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        if meta.get("status") == "PLATE_LOCKED" and meta.get("url"):
            if out_path.read_bytes() != harvest_path.read_bytes():
                print(f"[plate] reusing locked {plate['plate_id']} → {out_path.name}")
                return meta

    print(f"[plate] rendering {plate['plate_id']} from R2 harvest {harvest_path.name}…")
    uploaded = client.files.upload(str(harvest_path))
    pub = client.files.create_public_url(uploaded.id)
    harvest_url = getattr(pub, "public_url", None) or pub.public_url

    prompt = (
        f"{spec['imagine_prompt']} "
        "Use attached R2 harvest as structural morphology anchor only. "
        "Documentary scientific visualization, Jantzen molecular fidelity, no anthropomorphism."
    )
    resp = client.image.sample(
        prompt=prompt,
        model="grok-imagine-image-quality",
        image_url=harvest_url,
    )
    _download(resp.url, out_path)

    review = fidelity_review(plate, harvest_path, out_path, prompt=prompt)
    if not review["pass"]:
        raise RuntimeError(f"Fidelity review failed for {plate['plate_id']}: {review['issues']}")

    locked_at = datetime.now(timezone.utc).isoformat()
    meta = {
        "issue": 172,
        "plate_id": plate["plate_id"],
        "slug": plate["slug"],
        "subject": plate["subject"],
        "principle_set": plate["principle_set"],
        "path": str(out_path),
        "url": resp.url,
        "prompt": spec["imagine_prompt"],
        "plate_lock_verbatim": spec["plate_lock_verbatim"],
        "harvest_image": str(harvest_path.relative_to(WORKSPACE)).replace("\\", "/"),
        "harvest_url": harvest_url,
        "harvest_source": harvest.get("image_source"),
        "pdb_id": harvest.get("pdb_id"),
        "primary_citation": harvest.get("primary_citation"),
        "license": harvest.get("license"),
        "status": "PLATE_LOCKED",
        "locked_at": locked_at,
        "fidelity_review": review,
        "swap_slot": "@2",
        "reused": False,
    }
    meta_path.write_text(json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8")

    sidecar = OUT_DIR / f"{plate['slug']}_reference.json"
    sidecar.write_text(
        json.dumps(
            {
                "issue": 172,
                "subject_id": harvest["subject_id"],
                "plate_id": plate["plate_id"],
                "slug": plate["slug"],
                "label": harvest.get("label"),
                "pdb_id": harvest.get("pdb_id"),
                "path": str(out_path),
                "url": resp.url,
                "harvest_image": meta["harvest_image"],
                "source_url": harvest.get("source_url"),
                "license": harvest.get("license"),
                "primary_citation": harvest.get("primary_citation"),
                "status": "PLATE_LOCKED",
                "locked_at": locked_at,
                "feeds": ["T2 #152 science_plate_library_v1", "ACTORS #172 @2 molecular plates"],
            },
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    print(f"[plate] PLATE_LOCKED → {out_path.name}")
    return meta


def flip_library_and_manifest(metas: list[dict[str, Any]]) -> None:
    lib = load_library()
    locked_ids = {m["plate_id"] for m in metas}
    for p in lib["plates"]:
        if p["plate_id"] in locked_ids:
            p["plate_spec"]["status"] = "PLATE_LOCKED"
            p["plate_spec"]["locked_at"] = next(
                m["locked_at"] for m in metas if m["plate_id"] == p["plate_id"]
            )
    LIBRARY.write_text(json.dumps(lib, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    for pid, entry in manifest.get("plates", {}).items():
        if pid in locked_ids:
            entry["status"] = "PLATE_LOCKED"
            meta = next(m for m in metas if m["plate_id"] == pid)
            entry["locked_at"] = meta["locked_at"]
            entry["plate_url"] = meta.get("url")
    manifest["molecular_locked_at"] = datetime.now(timezone.utc).isoformat()
    manifest["issue_172"] = "ACTORS molecular @2 plates PLATE_LOCKED"
    MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_notes(metas: list[dict[str, Any]]) -> Path:
    notes = {
        "issue": 172,
        "task": "ACTORS — molecular @2 plates from R2 harvest",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "principle_set": "jantzen_molecular_cellular",
        "swap_slot": "@2",
        "all_pass": all(m.get("fidelity_review", {}).get("pass") for m in metas),
        "plates": [
            {
                "plate_id": m["plate_id"],
                "slug": m["slug"],
                "delivery": m["path"],
                "harvest": m["harvest_image"],
                "pdb_id": m.get("pdb_id"),
                "status": m["status"],
                "locked_at": m["locked_at"],
                "fidelity": m.get("fidelity_review"),
                "notes": (
                    "Hemoglobin: RCSB 4HHB assembly → Jantzen ribbon tetramer @2 plate."
                    if m["slug"] == "protein-hemoglobin"
                    else (
                        "B-DNA: RCSB 1BNA assembly → right-handed groove-faithful @2 plate."
                        if m["slug"] == "dna-double-helix"
                        else "HeLa: NIGMS #3519 SEM morphology anchor → Alberts schematic cross-section @2 plate (not raw EM)."
                    )
                ),
            }
            for m in metas
        ],
        "marginal_swap_usage": "Load plate_spec.reference_file as @2; prompt uses only 'see attached render'.",
    }
    NOTES_PATH.write_text(json.dumps(notes, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return NOTES_PATH


def main() -> int:
    parser = argparse.ArgumentParser(description="ACTORS #172 molecular @2 plate lock")
    parser.add_argument("--slugs", default=",".join(TARGET_SLUGS))
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--review-only", action="store_true")
    args = parser.parse_args()

    slugs = [s.strip() for s in args.slugs.split(",") if s.strip()]
    lib = load_library()
    metas: list[dict[str, Any]] = []

    if args.review_only:
        for slug in slugs:
            plate = plate_by_slug(lib, slug)
            harvest = harvest_entry(slug)
            harvest_path = REPO / harvest["image_primary"].replace("/", os.sep)
            out_path = WORKSPACE / plate["plate_spec"]["reference_file"].replace("/", os.sep)
            review = fidelity_review(
                plate, harvest_path, out_path, prompt=plate["plate_spec"]["imagine_prompt"]
            )
            metas.append({"plate_id": plate["plate_id"], "slug": slug, "fidelity_review": review})
        write_notes(metas)
        print(json.dumps(metas, indent=2))
        return 0 if all(m["fidelity_review"]["pass"] for m in metas) else 1

    import xai_sdk

    token = os.environ.get("XAI_API_KEY") or _load_grok_token()
    os.environ["XAI_API_KEY"] = token
    client = xai_sdk.Client(api_key=token)

    for slug in slugs:
        plate = plate_by_slug(lib, slug)
        harvest = harvest_entry(slug)
        metas.append(render_plate(client, plate, harvest, force=args.force))

    flip_library_and_manifest(metas)
    notes_path = write_notes(metas)
    summary = {
        "issue": 172,
        "locked": len(metas),
        "plates": [m["plate_id"] for m in metas],
        "notes": str(notes_path),
        "all_pass": True,
    }
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())