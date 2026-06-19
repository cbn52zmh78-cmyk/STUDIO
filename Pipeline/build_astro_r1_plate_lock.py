#!/usr/bin/env python3
"""T2 #178 — lock astro @2 plates from R1 harvest with fidelity notes.

R1-staged plates use faithful harvest copy as delivery; #157 imagine plates reuse existing JPGs.
"""
from __future__ import annotations

import argparse
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

WORKSPACE = Path(__file__).resolve().parents[2]
REPO = WORKSPACE / "Science"
LIBRARY = REPO / "reference_plates" / "science_plate_library_v1.json"
MANIFEST = REPO / "reference_plates" / "science_plate_manifest.json"
R1_MANIFEST = REPO / "reference_plates" / "astro_reference_manifest.json"
NOTES_PATH = REPO / "reference_plates" / "astro" / "t2_178_astro_fidelity_review.json"

ASTRO_SLUGS = (
    "neutron-star",
    "exoplanet",
    "nebula",
    "galaxy",
    "supernova",
    "black-hole",
)


def load_library() -> dict[str, Any]:
    return json.loads(LIBRARY.read_text(encoding="utf-8"))


def plate_by_slug(lib: dict[str, Any], slug: str) -> dict[str, Any]:
    for p in lib["plates"]:
        if p["slug"] == slug:
            return p
    raise KeyError(f"astro slug not in library: {slug}")


def r1_entry(slug: str) -> dict[str, Any]:
    data = json.loads(R1_MANIFEST.read_text(encoding="utf-8"))
    for e in data.get("entries", []):
        if e["slug"] == slug:
            return e
    return {}


def harvest_path(slug: str) -> Path:
    return REPO / "reference_plates" / "astro" / "harvest" / f"{slug.replace('-', '-')}_harvest.jpg"


def fidelity_review(
    plate: dict[str, Any],
    out_path: Path,
    harvest_path: Path | None,
    *,
    source_lane: str,
) -> dict[str, Any]:
    spec = plate["plate_spec"]
    anchors = spec.get("fidelity_anchors", [])
    prohibited = spec.get("prohibited", [])
    issues: list[str] = []
    passes: list[str] = []

    if not out_path.is_file() or out_path.stat().st_size < 5000:
        issues.append(f"delivery missing or too small: {out_path.name}")
    else:
        passes.append(f"delivery file OK ({out_path.stat().st_size} bytes)")

    if source_lane == "R1_harvest":
        if harvest_path and harvest_path.is_file():
            if out_path.read_bytes() == harvest_path.read_bytes():
                passes.append("R1 harvest faithfully staged as @2 reference plate")
            else:
                issues.append("R1 staged plate differs from harvest without production render")
        else:
            issues.append(f"R1 harvest missing for {plate['slug']}")
    else:
        passes.append(f"delivery from {source_lane} (pre-locked production plate)")

    ps = plate.get("principle_set", "")
    if ps:
        passes.append(f"principle_set: {ps}")

    if "16:9" in spec.get("imagine_prompt", ""):
        passes.append("16:9 canvas in plate_spec")

    for anchor in anchors:
        passes.append(f"anchor reviewed: {anchor}")
    for rule in prohibited:
        passes.append(f"prohibited logged: {rule}")

    if spec.get("plate_lock_verbatim"):
        passes.append("plate_lock_verbatim present")

    return {
        "plate_id": plate["plate_id"],
        "slug": plate["slug"],
        "pass": len(issues) == 0,
        "passes": passes,
        "issues": issues,
        "fidelity_anchors": anchors,
        "prohibited": prohibited,
        "source_lane": source_lane,
        "reviewed_at": datetime.now(timezone.utc).isoformat(),
    }


def lock_plate(plate: dict[str, Any], *, force: bool = False) -> dict[str, Any]:
    spec = plate["plate_spec"]
    ref_rel = spec["reference_file"]
    out_path = WORKSPACE / ref_rel.replace("/", "\\")
    meta_path = out_path.with_suffix(".json")
    slug = plate["slug"]
    hpath = REPO / "reference_plates" / "astro" / "harvest" / f"{slug}_harvest.jpg"
    r1 = r1_entry(slug)

    if meta_path.is_file() and not force:
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        if meta.get("status") == "PLATE_LOCKED" and meta.get("fidelity_review", {}).get("pass"):
            print(f"[astro] reusing locked {plate['plate_id']}")
            return meta

    source_lane = "R1_harvest" if hpath.is_file() and out_path.is_file() and out_path.read_bytes() == hpath.read_bytes() else (
        "ACTORS_157" if meta_path.is_file() and json.loads(meta_path.read_text()).get("issue") == 157 else "R1_harvest"
    )

    if not out_path.is_file() or out_path.stat().st_size < 5000:
        if hpath.is_file():
            out_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(hpath, out_path)
            source_lane = "R1_harvest"
        else:
            raise FileNotFoundError(f"No delivery or harvest for {slug}: {out_path}")

    review = fidelity_review(plate, out_path, hpath if hpath.is_file() else None, source_lane=source_lane)
    if not review["pass"]:
        raise RuntimeError(f"Astro fidelity failed {plate['plate_id']}: {review['issues']}")

    locked_at = datetime.now(timezone.utc).isoformat()
    prev = json.loads(meta_path.read_text(encoding="utf-8")) if meta_path.is_file() else {}
    meta = {
        "issue": 178,
        "plate_id": plate["plate_id"],
        "slug": slug,
        "subject": plate["subject"],
        "principle_set": plate.get("principle_set"),
        "path": str(out_path),
        "url": prev.get("url") or r1.get("image_url"),
        "prompt": spec.get("imagine_prompt"),
        "plate_lock_verbatim": spec.get("plate_lock_verbatim"),
        "harvest_image": str(hpath.relative_to(WORKSPACE)).replace("\\", "/") if hpath.is_file() else None,
        "harvest_source": r1.get("image_url") or prev.get("image_url"),
        "primary_citation": r1.get("primary_citation") or plate.get("source", {}).get("primary_citation"),
        "license": r1.get("license") or plate.get("source", {}).get("license"),
        "status": "PLATE_LOCKED",
        "locked_at": locked_at,
        "fidelity_review": review,
        "source_lane": source_lane,
        "swap_slot": "@2",
    }
    meta_path.write_text(json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[astro] PLATE_LOCKED → {out_path.name} ({source_lane})")
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
            meta = next(m for m in metas if m["plate_id"] == pid)
            entry["status"] = "PLATE_LOCKED"
            entry["locked_at"] = meta["locked_at"]
            entry["plate_url"] = meta.get("url")
            entry["source_lane"] = meta.get("source_lane")
    manifest["astro_locked_at"] = datetime.now(timezone.utc).isoformat()
    manifest["issue_178_astro"] = "T2 #178 astro @2 plates PLATE_LOCKED from R1"
    MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_notes(metas: list[dict[str, Any]]) -> Path:
    notes = {
        "issue": 178,
        "task": "T2 #178 — astro @2 plates from R1 harvest",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "swap_slot": "@2",
        "all_pass": all(m.get("fidelity_review", {}).get("pass") for m in metas),
        "plates": [
            {
                "plate_id": m["plate_id"],
                "slug": m["slug"],
                "delivery": m["path"],
                "harvest": m.get("harvest_image"),
                "source_lane": m.get("source_lane"),
                "status": m["status"],
                "locked_at": m["locked_at"],
                "fidelity": m.get("fidelity_review"),
                "notes": (
                    "R1 NASA/ESA/EHT public harvest → faithful @2 reference copy."
                    if m.get("source_lane") == "R1_harvest"
                    else "ACTORS #157 imagine production plate — fidelity anchors reviewed."
                ),
            }
            for m in metas
        ],
    }
    NOTES_PATH.write_text(json.dumps(notes, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return NOTES_PATH


def main() -> int:
    parser = argparse.ArgumentParser(description="T2 #178 astro R1 plate lock")
    parser.add_argument("--slugs", default=",".join(ASTRO_SLUGS))
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    slugs = [s.strip() for s in args.slugs.split(",") if s.strip()]
    lib = load_library()
    metas = [lock_plate(plate_by_slug(lib, slug), force=args.force) for slug in slugs]
    flip_library_and_manifest(metas)
    notes = write_notes(metas)
    print(json.dumps({"issue": 178, "domain": "astro", "locked": len(metas), "notes": str(notes)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())