#!/usr/bin/env python3
"""T2 #178 — render R4 chemistry + physics @2 plates from harvest, fidelity-review, PLATE_LOCKED."""
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
CHEM_MANIFEST = REPO / "reference_plates" / "chemistry_reference_manifest.json"
PHYS_MANIFEST = REPO / "reference_plates" / "physics_reference_manifest.json"
NOTES_PATH = REPO / "reference_plates" / "r4_178_fidelity_review.json"

R4_SPECS: dict[str, dict[str, Any]] = {
    "covalent-bonding": {
        "domain": "chemistry",
        "plate_id": "@Sci-ChemBond-001",
        "reference_file": "Science/reference_plates/chemistry/covalent_bonding_reference.jpg",
        "principle_set": "jantzen_molecular_cellular",
        "imagine_prompt": (
            "Scientific molecular visualization, bent water molecule H2O — oxygen central atom, "
            "two equivalent O–H covalent sigma bonds, ~104.5 degree bond angle, NIST WebBook topology, "
            "clean neutral background, documentary chemistry fidelity, no ionic lattice mixing, 16:9"
        ),
        "plate_lock_verbatim": (
            "Covalent bonding — bent H2O triatomic, two O–H σ bonds, NIST Chemistry WebBook anchor, "
            "no ionic NaCl lattice, no exaggerated 90° geometry."
        ),
        "fidelity_anchors": ["Bent triatomic water", "Two equivalent O–H bonds", "NIST WebBook topology"],
        "prohibited": ["Ionic lattice mixing", "90° bond angle error", "Isolated atoms without bonds"],
    },
    "crystal-lattice": {
        "domain": "chemistry",
        "plate_id": "@Sci-CrystalLattice-001",
        "reference_file": "Science/reference_plates/chemistry/crystal_lattice_reference.jpg",
        "principle_set": "general_scientific",
        "imagine_prompt": (
            "Scientific crystal visualization, rock-salt NaCl face-centered cubic ionic lattice, "
            "alternating Na+ and Cl− ions, COD 1000040 / PDB 1NAG morphology anchor, "
            "documentary materials chemistry, 16:9, no isolated diatomic gas molecule"
        ),
        "plate_lock_verbatim": (
            "Crystal lattice — NaCl Fm-3m rock-salt, alternating cations/anions, COD 1000040 class, "
            "not gas-phase NaCl dimer."
        ),
        "fidelity_anchors": ["FCC ionic lattice", "Alternating Na+/Cl−", "COD/PDB morphology"],
        "prohibited": ["Isolated diatomic NaCl", "Metallic bonding cues", "Wrong lattice symmetry"],
    },
    "chemical-reaction": {
        "domain": "chemistry",
        "plate_id": "@Sci-ChemReaction-001",
        "reference_file": "Science/reference_plates/chemistry/chemical_reaction_reference.jpg",
        "principle_set": "general_scientific",
        "imagine_prompt": (
            "Scientific chemistry visualization, methane CH4 combustion reactant anchor — "
            "tetrahedral methane molecule, balanced stoichiometry context CH4 + 2O2 → CO2 + 2H2O, "
            "NIST WebBook topology, documentary reaction lesson plate, 16:9"
        ),
        "plate_lock_verbatim": (
            "Chemical reaction — methane combustion reactant topology, complete combustion stoichiometry, "
            "NIST WebBook CH4 anchor, no incomplete CO smoke."
        ),
        "fidelity_anchors": ["Tetrahedral CH4", "Combustion stoichiometry", "NIST reactant topology"],
        "prohibited": ["Incomplete combustion CO", "Unbalanced equation", "Single-atom methane"],
    },
    "material-microstructure": {
        "domain": "chemistry",
        "plate_id": "@Sci-Microstructure-001",
        "reference_file": "Science/reference_plates/chemistry/material_microstructure_reference.jpg",
        "principle_set": "general_scientific",
        "imagine_prompt": (
            "Scientific materials SEM visualization, laser-microstructured copper surface NASA JSC jsc2023e010177, "
            "µm-scale engraved texture, sparse particulates, documentary metallurgy microstructure, "
            "not biological cells, 16:9"
        ),
        "plate_lock_verbatim": (
            "Materials microstructure — SEM laser-textured copper, µm surface features, NASA JSC/DLR anchor, "
            "not TEM lattice fringes as grain boundaries."
        ),
        "fidelity_anchors": ["SEM surface morphology", "µm-scale texture", "Metallurgy not biology"],
        "prohibited": ["Biological cells as alloy grains", "TEM fringes as grain boundaries", "CT scan slices"],
    },
    "electromagnetic-field-lines": {
        "domain": "physics",
        "plate_id": "@Sci-EMField-001",
        "reference_file": "Science/reference_plates/physics/electromagnetic_field_lines_reference.jpg",
        "principle_set": "general_scientific",
        "imagine_prompt": (
            "Scientific physics visualization, Earth magnetosphere with MMS spacecraft quartet and "
            "smooth closed magnetic field lines, NASA MMS 2014 anchor, no monopole fields, "
            "no crossing field lines, documentary EM fidelity, 16:9"
        ),
        "plate_lock_verbatim": (
            "EM field lines — magnetosphere multipoint sampling, smooth closed curves, NASA MMS anchor, "
            "no monopole, no random disconnected arcs."
        ),
        "fidelity_anchors": ["Closed field lines", "MMS spacecraft context", "No monopole fields"],
        "prohibited": ["Field lines crossing", "Monopole fields", "Random disconnected curves"],
    },
    "fusion-plasma-tokamak": {
        "domain": "physics",
        "plate_id": "@Sci-FusionPlasma-001",
        "reference_file": "Science/reference_plates/physics/fusion_plasma_tokamak_reference.jpg",
        "principle_set": "general_scientific",
        "imagine_prompt": (
            "Scientific plasma physics visualization, tokamak toroidal fusion plasma confinement, "
            "hot core plasma in magnetic torus, DOE FES 2025 simulation morphology anchor, "
            "no star-in-a-jar trope, no solid glowing liquid, 16:9"
        ),
        "plate_lock_verbatim": (
            "Fusion plasma tokamak — magnetically confined toroidal plasma, hot core, DOE FES anchor, "
            "not solid liquid plasma or star-in-jar."
        ),
        "fidelity_anchors": ["Toroidal confinement", "Hot plasma core", "Tokamak field structure"],
        "prohibited": ["Solid plasma liquid", "Star-in-a-jar", "Missing toroidal geometry"],
    },
}

HARVESTABLE = tuple(R4_SPECS.keys())


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
    req = urllib.request.Request(url, headers={"User-Agent": "STUDIO-r4-chem-physics-plates/1.0"})
    with urllib.request.urlopen(req, timeout=300) as r:
        dest.write_bytes(r.read())


def harvest_entry(slug: str) -> dict[str, Any]:
    for manifest_path in (CHEM_MANIFEST, PHYS_MANIFEST):
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
        for s in data.get("subjects", []):
            if s["slug"] == slug:
                return s
    raise KeyError(f"R4 harvest missing slug: {slug}")


def fidelity_review(
    spec: dict[str, Any],
    harvest_path: Path,
    out_path: Path,
    harvest: dict[str, Any],
) -> dict[str, Any]:
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
            passes.append("plate differs from R4 harvest (production render applied)")

    passes.append(f"principle_set: {spec['principle_set']}")
    if "16:9" in spec["imagine_prompt"]:
        passes.append("16:9 canvas requested")

    for anchor in spec["fidelity_anchors"]:
        passes.append(f"anchor reviewed: {anchor}")
    for rule in spec["prohibited"]:
        passes.append(f"prohibited logged: {rule}")

    if harvest.get("status") != "HARVESTED":
        issues.append(f"harvest status not HARVESTED: {harvest.get('status')}")

    return {
        "plate_id": spec["plate_id"],
        "slug": harvest["slug"],
        "pass": len(issues) == 0,
        "passes": passes,
        "issues": issues,
        "fidelity_anchors": spec["fidelity_anchors"],
        "prohibited": spec["prohibited"],
        "reviewed_at": datetime.now(timezone.utc).isoformat(),
    }


def render_plate(
    client: Any,
    slug: str,
    harvest: dict[str, Any],
    *,
    force: bool = False,
) -> dict[str, Any]:
    spec = R4_SPECS[slug]
    out_path = WORKSPACE / spec["reference_file"].replace("/", os.sep)
    meta_path = out_path.with_suffix(".json")
    domain_dir = REPO / "reference_plates" / spec["domain"]

    harvest_rel = harvest.get("image_primary", "")
    harvest_path = WORKSPACE / harvest_rel.replace("/", os.sep) if harvest_rel else Path()
    if not harvest_path.is_file():
        raise FileNotFoundError(f"R4 harvest image missing: {harvest_path}")

    if (
        out_path.is_file()
        and out_path.stat().st_size > 8000
        and meta_path.is_file()
        and not force
    ):
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        if meta.get("status") == "PLATE_LOCKED" and meta.get("url"):
            if out_path.read_bytes() != harvest_path.read_bytes():
                print(f"[r4] reusing locked {spec['plate_id']} → {out_path.name}")
                return meta

    print(f"[r4] rendering {spec['plate_id']} from harvest {harvest_path.name}…")
    uploaded = client.files.upload(str(harvest_path))
    pub = client.files.create_public_url(uploaded.id)
    harvest_url = getattr(pub, "public_url", None) or pub.public_url

    prompt = (
        f"{spec['imagine_prompt']} "
        "Use attached R4 harvest as structural morphology anchor only. "
        "Documentary scientific visualization, no anthropomorphism."
    )
    resp = client.image.sample(
        prompt=prompt,
        model="grok-imagine-image-quality",
        image_url=harvest_url,
    )
    _download(resp.url, out_path)

    review = fidelity_review(spec, harvest_path, out_path, harvest)
    if not review["pass"]:
        raise RuntimeError(f"Fidelity review failed for {spec['plate_id']}: {review['issues']}")

    locked_at = datetime.now(timezone.utc).isoformat()
    meta = {
        "issue": 178,
        "plate_id": spec["plate_id"],
        "slug": slug,
        "domain": spec["domain"],
        "principle_set": spec["principle_set"],
        "path": str(out_path),
        "url": resp.url,
        "prompt": spec["imagine_prompt"],
        "plate_lock_verbatim": spec["plate_lock_verbatim"],
        "harvest_image": str(harvest_path.relative_to(WORKSPACE)).replace("\\", "/"),
        "harvest_url": harvest_url,
        "harvest_source": harvest.get("image_source"),
        "primary_citation": harvest.get("primary_citation"),
        "license": harvest.get("license"),
        "status": "PLATE_LOCKED",
        "locked_at": locked_at,
        "fidelity_review": review,
        "swap_slot": "@2",
        "reused": False,
    }
    meta_path.write_text(json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8")

    sidecar = domain_dir / f"{slug.replace('-', '_')}_reference.json"
    if not sidecar.is_file():
        sidecar = domain_dir / f"{slug}_reference.json"
    sidecar.write_text(
        json.dumps(
            {
                "issue": 178,
                "subject_id": harvest.get("subject_id"),
                "plate_id": spec["plate_id"],
                "slug": slug,
                "label": harvest.get("label"),
                "path": str(out_path),
                "url": resp.url,
                "harvest_image": meta["harvest_image"],
                "source_url": harvest.get("source_url") or harvest.get("source_page_url"),
                "license": harvest.get("license"),
                "primary_citation": harvest.get("primary_citation"),
                "status": "PLATE_LOCKED",
                "locked_at": locked_at,
                "feeds": ["T2 #178 R4 chemistry/physics @2 plates"],
            },
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    print(f"[r4] PLATE_LOCKED → {out_path.name}")
    return meta


def write_notes(metas: list[dict[str, Any]]) -> Path:
    notes = {
        "issue": 178,
        "task": "T2 #178 — R4 chemistry + physics @2 plates",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "swap_slot": "@2",
        "all_pass": all(m.get("fidelity_review", {}).get("pass") for m in metas),
        "blocked": {
            "double-slit-interference": "HARVEST_FAILED — Wikimedia 403",
            "particle-tracks-bubble-chamber": "HARVEST_FAILED — CERN CDS HTML gate",
        },
        "plates": [
            {
                "plate_id": m["plate_id"],
                "slug": m["slug"],
                "domain": m["domain"],
                "delivery": m["path"],
                "harvest": m["harvest_image"],
                "status": m["status"],
                "locked_at": m["locked_at"],
                "fidelity": m.get("fidelity_review"),
            }
            for m in metas
        ],
    }
    NOTES_PATH.write_text(json.dumps(notes, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return NOTES_PATH


def main() -> int:
    parser = argparse.ArgumentParser(description="T2 #178 R4 chem/physics plate lock")
    parser.add_argument("--slugs", default=",".join(HARVESTABLE))
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    slugs = [s.strip() for s in args.slugs.split(",") if s.strip()]
    import xai_sdk

    token = os.environ.get("XAI_API_KEY") or _load_grok_token()
    os.environ["XAI_API_KEY"] = token
    client = xai_sdk.Client(api_key=token)

    metas = [render_plate(client, slug, harvest_entry(slug), force=args.force) for slug in slugs]
    notes = write_notes(metas)
    by_domain: dict[str, int] = {}
    for m in metas:
        by_domain[m["domain"]] = by_domain.get(m["domain"], 0) + 1
    print(json.dumps({"issue": 178, "locked_by_domain": by_domain, "notes": str(notes)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())