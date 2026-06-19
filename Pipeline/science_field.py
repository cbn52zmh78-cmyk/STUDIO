"""Chemistry / physics (and allied) field routing for science-explainer intake (#179)."""

from __future__ import annotations

import json
import re
from functools import lru_cache
from pathlib import Path
from typing import Any

PIPELINE_DIR = Path(__file__).resolve().parent
ROOT = PIPELINE_DIR.parents[1]
SCIENCE_ROOT = ROOT / "Science"
SELECTOR_PATH = SCIENCE_ROOT / "systems" / "domain_principle_selector.json"

SUPPORTED_FIELDS = frozenset({
    "chemistry",
    "physics",
    "astrophysics",
    "cosmology",
    "astronomy",
    "space_science",
    "biology",
    "biochemistry",
    "biophysics",
    "genetics",
    "atmospheric_physics",
    "planetary_science",
    "earth_science",
})

FIELD_MANIFESTS: dict[str, Path] = {
    "chemistry": SCIENCE_ROOT / "reference_plates" / "chemistry_reference_manifest.json",
    "physics": SCIENCE_ROOT / "reference_plates" / "physics_reference_manifest.json",
}


def _rel_workspace(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path).replace("\\", "/")


def normalize_field(field: str | None, *, domain: str = "") -> str | None:
    if field:
        slug = re.sub(r"[^a-z0-9]+", "_", str(field).lower()).strip("_")
        if slug in SUPPORTED_FIELDS:
            return slug
        if slug.endswith("_physics") or slug == "phys":
            return "physics"
        if slug.startswith("chem"):
            return "chemistry"
        if slug in ("astro", "astronomy", "cosmology"):
            return "astrophysics"
        return slug
    blob = domain.lower()
    if "chemistry" in blob or blob.startswith("chem"):
        return "chemistry"
    if "astro" in blob or "cosmolog" in blob or "astronom" in blob:
        return "astrophysics"
    if "physics" in blob or "atmospheric" in blob:
        return "physics"
    if any(k in blob for k in ("molecular", "protein", "cell", "dna", "immune")):
        return "biology"
    return None


@lru_cache(maxsize=1)
def _load_selector() -> dict[str, Any]:
    return json.loads(SELECTOR_PATH.read_text(encoding="utf-8"))


def _keyword_in_blob(keyword: str, blob: str) -> bool:
    """Word-boundary keyword match — avoids false positives (e.g. agn in electromagnetic)."""
    return bool(re.search(rf"\b{re.escape(keyword.lower())}\b", blob.lower()))


def select_principle_set(
    *,
    field: str | None,
    domain: str,
    phenomenon: str,
    subject_id: str,
    explicit: str | None = None,
) -> dict[str, Any]:
    if explicit:
        return {
            "principle_set": str(explicit).strip(),
            "selection_reason": "explicit",
        }
    cfg = _load_selector()
    norm_field = normalize_field(field, domain=domain)
    if norm_field:
        for set_id in cfg["priority"]:
            spec = cfg["sets"][set_id]
            if spec.get("default"):
                continue
            fields = [f.lower() for f in spec.get("fields", [])]
            if norm_field in fields:
                return {"principle_set": set_id, "selection_reason": f"field:{norm_field}"}
    blob = f"{domain} {phenomenon} {subject_id}".lower()
    for set_id in cfg["priority"]:
        spec = cfg["sets"][set_id]
        if spec.get("default"):
            continue
        for kw in spec.get("keywords", []):
            if _keyword_in_blob(kw, blob):
                return {"principle_set": set_id, "selection_reason": f"keyword:{kw}"}
    return {"principle_set": "general_scientific", "selection_reason": "default"}


@lru_cache(maxsize=8)
def _load_manifest(field: str) -> dict[str, Any] | None:
    path = FIELD_MANIFESTS.get(field)
    if not path or not path.is_file():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def resolve_field_plate(field: str, subject_id: str) -> dict[str, Any] | None:
    """Lookup harvested @2 plate for chemistry/physics subject_id."""
    manifest = _load_manifest(field)
    if not manifest:
        return None
    sid = subject_id.strip().lower()
    for entry in manifest.get("subjects", []):
        if entry.get("status") != "HARVESTED":
            continue
        candidates = {
            str(entry.get("subject_id", "")).lower(),
            str(entry.get("slug", "")).lower(),
        }
        if sid not in candidates:
            continue
        image = entry.get("image_primary") or (entry.get("files") or {}).get("image_harvest")
        if not image:
            continue
        img_path = Path(image)
        if not img_path.is_absolute():
            img_path = ROOT / image
        return {
            "plate_id": entry.get("plate_id"),
            "visualization_ref": _rel_workspace(img_path),
            "principle_set": entry.get("principle_set"),
            "illustrative_note": entry.get("illustrative_note"),
            "primary_citation": entry.get("primary_citation"),
        }
    return None


def enrich_science_subject(ss: dict[str, Any]) -> dict[str, Any]:
    """Normalize field, principle_set, and optional @2 plate wiring."""
    domain = str(ss.get("domain", "")).strip()
    field = normalize_field(ss.get("field"), domain=domain)
    if field and field not in SUPPORTED_FIELDS:
        raise ValueError(
            f"science_subject.field '{field}' not supported — "
            f"use one of: {', '.join(sorted(SUPPORTED_FIELDS))}"
        )

    principle = select_principle_set(
        field=field,
        domain=domain,
        phenomenon=str(ss.get("phenomenon", "")),
        subject_id=str(ss.get("subject_id", "")),
        explicit=ss.get("principle_set"),
    )
    plate: dict[str, Any] | None = None
    if field in FIELD_MANIFESTS and not ss.get("visualization_ref"):
        plate = resolve_field_plate(field, str(ss.get("subject_id", "")))

    out = dict(ss)
    if field:
        out["field"] = field
    out["principle_set"] = principle["principle_set"]
    out["principle_selection_reason"] = principle["selection_reason"]
    if plate:
        if not out.get("visualization_ref"):
            out["visualization_ref"] = plate["visualization_ref"]
        if not out.get("plate_id"):
            out["plate_id"] = plate["plate_id"]
        if plate.get("illustrative_note") and not out.get("illustrative_note"):
            out["illustrative_note"] = plate["illustrative_note"]
    return out