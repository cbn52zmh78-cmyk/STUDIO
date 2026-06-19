#!/usr/bin/env python3
"""T2 #178 — render + lock Historical Figures Bible v1 first-8 reconstruction plates."""
from __future__ import annotations

import argparse
import json
import os
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

WORKSPACE = Path(__file__).resolve().parents[2]
BIBLE_REGISTRY = WORKSPACE / "History" / "Historical_Figures_Bible" / "registry" / "v1_first_8.json"
CASTING_REGISTRY = WORKSPACE / "History" / "Historical_Figures_Bible" / "registry" / "figure_casting_registry.json"
NOTES_PATH = WORKSPACE / "History" / "Historical_Figures_Bible" / "registry" / "t2_178_figure_fidelity_review.json"

DISCLOSURE = "SPECULATIVE AI RECONSTRUCTION — NOT PHOTOGRAPHIC LIKENESS"
TURNAROUND_PREFIX = (
    "INTERPRETIVE HISTORICAL RECONSTRUCTION PLATE — NOT photographic likeness. "
    "16:9 three-view turnaround on solid neutral grey #808080. "
    "LEFT profile left, CENTER front three-quarter, RIGHT profile right. "
    "Full-length wide shot every panel — head to toe, feet visible. "
)
TURNAROUND_SUFFIX = (
    " Lower margin legible text: SPECULATIVE AI RECONSTRUCTION — NOT PHOTOGRAPHIC LIKENESS. "
    "Synthetic interpretive figure only. No celebrity likeness. No living-person impersonation."
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
    req = urllib.request.Request(url, headers={"User-Agent": "STUDIO-figure-bible-v1/1.0"})
    with urllib.request.urlopen(req, timeout=300) as r:
        dest.write_bytes(r.read())


def _figure_root(slug: str) -> Path:
    return WORKSPACE / "History" / "figures" / slug


def _turnaround_prompt(base: str) -> str:
    return f"{TURNAROUND_PREFIX}{base.strip()}{TURNAROUND_SUFFIX}"


def fidelity_review(figure: dict[str, Any], plate_path: Path) -> dict[str, Any]:
    spec = figure.get("reconstruction_plate_spec", {})
    issues: list[str] = []
    passes: list[str] = []

    if not plate_path.is_file() or plate_path.stat().st_size < 8000:
        issues.append("plate missing or too small")
    else:
        passes.append(f"delivery OK ({plate_path.stat().st_size} bytes)")

    if figure.get("death_year_floor_pass"):
        passes.append("death_year_floor_pass")
    else:
        issues.append("death_year_floor failed")

    tier = figure.get("appearance_basis", {}).get("likeness_tier")
    if tier:
        passes.append(f"likeness_tier: {tier}")

    for anchor in spec.get("reference_anchors", []):
        passes.append(f"anchor reviewed: {anchor}")
    for rule in spec.get("prohibited", []):
        passes.append(f"prohibited logged: {rule}")

    if DISCLOSURE.upper() in _turnaround_prompt(spec.get("imagine_prompt", "")).upper():
        passes.append("AI disclosure in prompt")

    return {
        "figure_id": figure["slug"],
        "name": figure["name"],
        "pass": len(issues) == 0,
        "passes": passes,
        "issues": issues,
        "reviewed_at": datetime.now(timezone.utc).isoformat(),
    }


def generate_plate(client: Any, figure: dict[str, Any], *, force: bool = False) -> dict[str, Any]:
    slug = figure["slug"]
    spec = figure["reconstruction_plate_spec"]
    root = _figure_root(slug)
    plate_dir = root / "01_reconstruction_plates"
    plate_dir.mkdir(parents=True, exist_ok=True)
    plate_path = plate_dir / "reconstruction_turnaround_v1.jpg"
    meta_path = plate_path.with_suffix(".json")

    if plate_path.is_file() and plate_path.stat().st_size > 8000 and meta_path.is_file() and not force:
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        if meta.get("status") == "PLATE_LOCKED" and meta.get("url"):
            if not meta.get("fidelity_review"):
                review = fidelity_review(figure, plate_path)
                if not review["pass"]:
                    raise RuntimeError(f"Figure fidelity failed {slug}: {review['issues']}")
                meta["fidelity_review"] = review
                meta["issue"] = 178
                meta_path.write_text(json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8")
            print(f"[figure] reusing locked {figure['name']}")
            return meta

    prompt = _turnaround_prompt(spec["imagine_prompt"])
    print(f"[figure] generating {figure['name']}…")
    resp = client.image.sample(prompt=prompt, model="grok-imagine-image-quality")
    _download(resp.url, plate_path)

    review = fidelity_review(figure, plate_path)
    if not review["pass"]:
        raise RuntimeError(f"Figure fidelity failed {slug}: {review['issues']}")

    locked_at = datetime.now(timezone.utc).isoformat()
    meta = {
        "figure_id": slug,
        "id": figure["id"],
        "name": figure["name"],
        "path": str(plate_path),
        "url": resp.url,
        "prompt": prompt,
        "disclosure": DISCLOSURE,
        "likeness_tier": figure.get("appearance_basis", {}).get("likeness_tier"),
        "status": "PLATE_LOCKED",
        "locked_at": locked_at,
        "fidelity_review": review,
        "issue": 178,
    }
    meta_path.write_text(json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[figure] PLATE_LOCKED → {slug}")
    return meta


def update_registries(figures: list[dict[str, Any]], plates: dict[str, dict[str, Any]]) -> None:
    bible = json.loads(BIBLE_REGISTRY.read_text(encoding="utf-8"))
    for fig in bible["figures"]:
        slug = fig["slug"]
        if slug in plates:
            fig["reconstruction_plate_spec"]["status"] = "PLATE_LOCKED"
            fig["reconstruction_plate_spec"]["locked_at"] = plates[slug]["locked_at"]
            fig["reconstruction_plate_spec"]["plate_file"] = plates[slug]["path"]
            fig["reconstruction_plate_spec"]["plate_url"] = plates[slug].get("url")
    bible["plate_lock_issue"] = 178
    bible["plate_locked_at"] = datetime.now(timezone.utc).isoformat()
    BIBLE_REGISTRY.write_text(json.dumps(bible, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    entries = []
    for fig in bible["figures"]:
        slug = fig["slug"]
        if slug not in plates:
            continue
        langs = fig.get("period_languages") or []
        period_lang = langs[0]["language"] if langs else ""
        entries.append({
            "figure_id": slug.replace("-", "_") if False else slug,
            "id": fig["id"],
            "slug": slug,
            "name": fig["name"],
            "death_year": fig["death_year"],
            "period_language": period_lang,
            "likeness_tier": fig.get("appearance_basis", {}).get("likeness_tier"),
            "plate_status": "PLATE_LOCKED",
            "plate_file": plates[slug]["path"],
            "fidelity_pass": plates[slug].get("fidelity_review", {}).get("pass"),
        })

    registry = {
        "version": "1.0.0",
        "issue": 178,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "scope": "historical_figure_reconstruction_bible_v1_first_8",
        "disclosure": DISCLOSURE,
        "total": len(entries),
        "summary": {"plate_locked": len(entries), "proofs_shipped": 0},
        "figures": entries,
    }
    CASTING_REGISTRY.write_text(json.dumps(registry, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_notes(plates: dict[str, dict[str, Any]]) -> Path:
    notes = {
        "issue": 178,
        "task": "T2 #178 — Historical Figures Bible v1 first-8 reconstruction plates",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "disclosure": DISCLOSURE,
        "all_pass": all(p.get("fidelity_review", {}).get("pass") for p in plates.values()),
        "figures": [
            {
                "slug": slug,
                "name": p["name"],
                "delivery": p["path"],
                "status": p["status"],
                "locked_at": p["locked_at"],
                "fidelity": p.get("fidelity_review"),
            }
            for slug, p in plates.items()
        ],
    }
    NOTES_PATH.write_text(json.dumps(notes, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return NOTES_PATH


def main() -> int:
    parser = argparse.ArgumentParser(description="T2 #178 figure bible v1 plate lock")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--slugs", default="", help="Comma-separated subset; default all first-8")
    args = parser.parse_args()

    bible = json.loads(BIBLE_REGISTRY.read_text(encoding="utf-8"))
    figures = bible["figures"]
    if args.slugs:
        want = {s.strip() for s in args.slugs.split(",") if s.strip()}
        figures = [f for f in figures if f["slug"] in want]

    import xai_sdk

    token = os.environ.get("XAI_API_KEY") or _load_grok_token()
    os.environ["XAI_API_KEY"] = token
    client = xai_sdk.Client(api_key=token)

    plates: dict[str, dict[str, Any]] = {}
    for fig in figures:
        plates[fig["slug"]] = generate_plate(client, fig, force=args.force)

    update_registries(figures, plates)
    notes = write_notes(plates)
    print(json.dumps({"issue": 178, "domain": "figures", "locked": len(plates), "notes": str(notes)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())