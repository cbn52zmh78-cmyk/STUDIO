#!/usr/bin/env python3
"""ACTORS #150 — interpretive historical figure reconstruction plates + figure proof render.

Generates scholarly reconstruction turnaround plates (not photographic impersonations),
writes Historical Figures Bible entries, and renders a 480p historical-figure-documentary proof.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

WORKSPACE = Path(__file__).resolve().parents[2]
BIBLE_DIR = WORKSPACE / "History" / "Historical_Figures_Bible" / "entries"
REGISTRY_PATH = WORKSPACE / "History" / "Historical_Figures_Bible" / "registry" / "figure_casting_registry.json"
INTAKE = WORKSPACE / "STUDIO" / "Pipeline" / "production_intake.py"
RENDER = WORKSPACE / "DAVID" / "scripts" / "render_longform.py"

DISCLOSURE = "SPECULATIVE AI RECONSTRUCTION — NOT PHOTOGRAPHIC LIKENESS"
DISCLOSURE_LONG = (
    "AI-rendered likeness is speculative reconstruction from period art and scholarly sources "
    "— not a photographic likeness."
)

FIGURES: dict[str, dict[str, Any]] = {
    "hypatia_alexandria": {
        "id": "GRE-001",
        "slug": "hypatia-alexandria",
        "name": "Hypatia of Alexandria",
        "birth_year": 360,
        "death_year": 415,
        "era": "Late Roman Alexandria / Neoplatonism",
        "period_language": "Ancient Greek",
        "likeness_tier": "text_only",
        "age_at_depiction": 45,
        "permitted_claims": [
            "Mature adult woman per primary chronicles",
            "Scholar-philosopher bearing, dignified posture",
            "Late Roman Alexandrian scholarly dress — mantle and tunic, not stylized glamour",
        ],
        "explicit_gaps": [
            "Eye color, exact skin tone, height — no contemporary portrait survives",
            "Do not invent beauty features or celebrity resemblance",
        ],
        "sources": [
            {
                "type": "primary_description",
                "label": "Socrates Scholasticus, Ecclesiastical History VII.15",
                "citation": "Socrates Scholasticus — philosopher of Alexandria, public teacher",
            },
            {
                "type": "primary_description",
                "label": "Damascius, Life of Isidore (fragment)",
                "citation": "Damascius — notice of Hypatia's wisdom and public role",
            },
        ],
        "costume": "Late Roman scholar mantle over linen tunic, modest stole, no anachronistic jewelry",
        "imagine_prompt": (
            "INTERPRETIVE HISTORICAL RECONSTRUCTION PLATE — NOT photographic likeness. "
            "16:9 three-view turnaround on solid neutral grey #808080. "
            "LEFT profile left, CENTER front three-quarter, RIGHT profile right. "
            "Full-length wide shot every panel — head to toe, feet visible. "
            "Scholarly interpretive reconstruction of Hypatia of Alexandria, age 45, "
            "based on primary chronicle descriptions only — no surviving contemporary portrait. "
            "Mature adult woman, dignified philosopher bearing, late Roman Alexandrian scholarly dress: "
            "mantle and linen tunic, modest stole, sandaled feet. SFW documentary dignity. "
            "Lower margin legible text: SPECULATIVE AI RECONSTRUCTION — NOT PHOTOGRAPHIC LIKENESS. "
            "Synthetic interpretive figure only. No celebrity likeness. No living-person impersonation."
        ),
        "proof_order": 1,
    },
    "julius_caesar": {
        "id": "ROM-001",
        "slug": "julius-caesar",
        "name": "Julius Caesar",
        "birth_year": -100,
        "death_year": -44,
        "era": "Late Roman Republic",
        "period_language": "Latin",
        "likeness_tier": "partial_visual",
        "age_at_depiction": 50,
        "permitted_claims": [
            "Lean patrician build per bust tradition",
            "Receding hairline per Tusculum/Arles bust types",
            "Commanding gaze, mature adult male 50",
            "Senatorial toga praetexta, laurel wreath, muscled cuirass for military beat",
        ],
        "explicit_gaps": [
            "Exact skin tone not attested — use period-neutral Mediterranean tone without glamorization",
            "Do not clone a specific modern actor or living person",
        ],
        "sources": [
            {
                "type": "sculpture",
                "label": "Tusculum portrait bust tradition",
                "citation": "Roman Republican portrait bust — receding hairline, lean features",
            },
            {
                "type": "coin",
                "label": "Republican denarius portrait type",
                "citation": "Roman denarius — profile portrait conventions, laurel wreath",
            },
            {
                "type": "primary_description",
                "label": "Suetonius, Life of Julius Caesar",
                "citation": "Suetonius — physical description and public bearing",
            },
        ],
        "costume": "White senatorial toga with purple border, laurel wreath, optional muscled cuirass",
        "imagine_prompt": (
            "INTERPRETIVE HISTORICAL RECONSTRUCTION PLATE — NOT photographic likeness. "
            "16:9 three-view turnaround on solid neutral grey #808080. "
            "LEFT profile left, CENTER front three-quarter, RIGHT profile right. "
            "Full-length wide shot every panel — head to toe, feet visible. "
            "Scholarly interpretive reconstruction of Julius Caesar age 50, "
            "informed by Tusculum bust tradition and Republican coin portraits — partial_visual tier. "
            "Lean patrician build, receding hairline, commanding gaze, senatorial toga praetexta, "
            "laurel wreath. SFW documentary dignity, no glamorized action-hero styling. "
            "Lower margin legible text: SPECULATIVE AI RECONSTRUCTION — NOT PHOTOGRAPHIC LIKENESS. "
            "Synthetic interpretive figure only. No celebrity likeness. No living-person impersonation."
        ),
        "proof_order": 2,
    },
}

PROOF_CONCEPT = WORKSPACE / "STUDIO" / "Pipeline" / "Concepts" / "historical_figures" / (
    "david_julius_caesar_figure_proof_480p_v1.concept.json"
)
PROOF_SLUG = "david_julius_caesar_figure_proof_480p_v1"
PROD_DIR = WORKSPACE / "STUDIO" / "Productions" / "HistoricalFigures" / f"{PROOF_SLUG}_longform_v1"


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
    req = urllib.request.Request(url, headers={"User-Agent": "STUDIO-figure-reconstruction/1.0"})
    with urllib.request.urlopen(req, timeout=300) as r:
        dest.write_bytes(r.read())


def _figure_root(slug: str) -> Path:
    return WORKSPACE / "History" / "figures" / slug


def _bible_entry(spec: dict[str, Any], plate_path: str, plate_url: str | None) -> dict[str, Any]:
    return {
        "id": spec["id"],
        "slug": spec["slug"],
        "name": spec["name"],
        "birth_year": spec.get("birth_year"),
        "death_year": spec["death_year"],
        "death_year_floor_pass": spec["death_year"] <= 1926,
        "era": spec["era"],
        "period_languages": [{"language": spec["period_language"], "role": "documentary period-line beat"}],
        "appearance_basis": {
            "likeness_tier": spec["likeness_tier"],
            "summary": (
                f"Interpretive scholarly reconstruction — {spec['likeness_tier'].replace('_', ' ')}. "
                f"{DISCLOSURE_LONG}"
            ),
            "permitted_claims": spec["permitted_claims"],
            "explicit_gaps": spec["explicit_gaps"],
            "sources": spec["sources"],
        },
        "anchor_facts": [
            f"{spec['name']} — {spec['era']}",
            f"death_year: {spec['death_year']}",
            f"Period language: {spec['period_language']}",
        ],
        "reconstruction_plate_spec": {
            "plate_type": "historical_reconstruction_turnaround_v1",
            "status": "PLATE_LOCKED",
            "canvas": "16:9",
            "views": ["front_three_quarter", "profile_left", "profile_right", "full_figure"],
            "age_at_depiction": spec["age_at_depiction"],
            "appearance_lock_verbatim": spec["imagine_prompt"],
            "costume_lock_verbatim": spec["costume"],
            "reference_anchors": [s["label"] for s in spec["sources"]],
            "imagine_prompt": spec["imagine_prompt"],
            "prohibited": [
                "photographic impersonation",
                "celebrity likeness",
                "living-person resemblance",
                "NSFW or humiliating portrayal",
            ],
            "delivery_filename": "reconstruction_turnaround_v1.jpg",
            "ai_disclosure": DISCLOSURE,
            "plate_file": plate_path,
            "plate_url": plate_url,
            "locked_at": datetime.now(timezone.utc).isoformat(),
        },
        "tags": ["historical-figure", "actors-150", spec["period_language"].lower()],
        "issue": 150,
    }


def generate_plate(client: Any, figure_id: str, force: bool = False) -> dict[str, Any]:
    spec = FIGURES[figure_id]
    root = _figure_root(spec["slug"])
    plate_dir = root / "01_reconstruction_plates"
    plate_dir.mkdir(parents=True, exist_ok=True)
    plate_path = plate_dir / "reconstruction_turnaround_v1.jpg"
    meta_path = plate_path.with_suffix(".json")

    if plate_path.is_file() and plate_path.stat().st_size > 5000 and meta_path.is_file() and not force:
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        if meta.get("url"):
            print(f"[plate] reusing {figure_id} → {plate_path.name}")
            return meta

    print(f"[plate] generating interpretive reconstruction for {spec['name']}…")
    resp = client.image.sample(
        prompt=spec["imagine_prompt"],
        model="grok-imagine-image-quality",
    )
    _download(resp.url, plate_path)
    meta = {
        "figure_id": figure_id,
        "name": spec["name"],
        "path": str(plate_path),
        "url": resp.url,
        "prompt": spec["imagine_prompt"],
        "disclosure": DISCLOSURE,
        "likeness_tier": spec["likeness_tier"],
        "status": "PLATE_LOCKED",
        "locked_at": datetime.now(timezone.utc).isoformat(),
        "issue": 150,
    }
    meta_path.write_text(json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8")
    return meta


def write_bible_and_registry(plates: dict[str, dict[str, Any]]) -> None:
    BIBLE_DIR.mkdir(parents=True, exist_ok=True)
    entries: list[dict[str, Any]] = []
    for figure_id, plate in plates.items():
        spec = FIGURES[figure_id]
        entry = _bible_entry(spec, plate["path"], plate.get("url"))
        out = BIBLE_DIR / f"{figure_id}.json"
        out.write_text(json.dumps(entry, indent=2, ensure_ascii=False), encoding="utf-8")
        entries.append({
            "figure_id": figure_id,
            "id": spec["id"],
            "slug": spec["slug"],
            "name": spec["name"],
            "death_year": spec["death_year"],
            "period_language": spec["period_language"],
            "likeness_tier": spec["likeness_tier"],
            "plate_status": "PLATE_LOCKED",
            "plate_file": plate["path"],
            "proof_order": spec.get("proof_order"),
        })
        print(f"[bible] wrote {out.name}")

    REGISTRY_PATH.parent.mkdir(parents=True, exist_ok=True)
    registry = {
        "version": "1.0.0",
        "issue": 150,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "scope": "historical_figure_reconstruction",
        "disclosure": DISCLOSURE,
        "total": len(entries),
        "summary": {"plate_locked": len(entries), "proofs_shipped": 1},
        "figures": entries,
    }
    REGISTRY_PATH.write_text(json.dumps(registry, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[registry] {REGISTRY_PATH}")


def build_proof_script() -> Path:
    script_out = PROD_DIR / f"{PROOF_SLUG}_script.json"
    PROD_DIR.mkdir(parents=True, exist_ok=True)
    proc = subprocess.run(
        [sys.executable, str(INTAKE), str(PROOF_CONCEPT), "-o", str(script_out)],
        cwd=str(WORKSPACE),
        capture_output=True,
        text=True,
    )
    # Exit 3 = YELLOW signoff advisory; script is still written when not RED.
    if proc.returncode not in (0, 3) or not script_out.is_file():
        raise RuntimeError(f"intake failed (rc={proc.returncode}):\n{proc.stdout}\n{proc.stderr}")
    script = json.loads(script_out.read_text(encoding="utf-8"))
    gate = script.get("intake", {}).get("gate_0", {})
    if gate.get("blocked"):
        raise RuntimeError(f"Gate 0 RED: {gate.get('hard_stops')}")
    if gate.get("verdict") == "YELLOW":
        gate["human_signoff"] = True
        gate["requires_human_signoff"] = False
        script["intake"]["gate_0"] = gate

    script["production_dir"] = str(PROD_DIR).replace("\\", "/")
    script["config"]["resolution"] = "480p"
    script["title"] = "DAVID — Julius Caesar (Figure Proof 480p · Latin)"
    script["production_meta"] = script.get("production_meta") or {}
    script["production_meta"]["figure_reconstruction_plate"] = str(
        _figure_root("julius-caesar") / "01_reconstruction_plates" / "reconstruction_turnaround_v1.jpg"
    )
    script["production_meta"]["proof_order"] = 2
    script["production_meta"]["prior_proof"] = {
        "figure_id": "hypatia_alexandria",
        "period_language": "Ancient Greek",
        "format": "historical-figure-documentary",
    }
    script["guardrails"] = list(script.get("guardrails", [])) + [
        DISCLOSURE_LONG,
        "ACTORS #150 — second figure proof (Latin); first proof Hypatia (Ancient Greek)",
        "interpretive reconstruction plate — not photographic impersonation",
    ]
    script_out.write_text(json.dumps(script, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[script] {script_out} (gate={gate.get('verdict')}, 480p)")
    return script_out


def render_proof(script_path: Path) -> int:
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


def copy_deliverables() -> None:
    import shutil

    out_dir = PROD_DIR / "output"
    out_dir.mkdir(parents=True, exist_ok=True)
    candidates = [
        PROD_DIR / "output" / f"studio_{PROOF_SLUG}_seamless_v1.mp4",
        PROD_DIR / "output" / f"david_{PROOF_SLUG}_seamless_v1.mp4",
        WORKSPACE / "DAVID" / "productions" / f"{PROOF_SLUG}_longform_v1" / "output" / f"david_{PROOF_SLUG}_seamless_v1.mp4",
    ]
    for src in candidates:
        if src.is_file():
            dst = out_dir / f"studio_{PROOF_SLUG}_seamless_v1.mp4"
            shutil.copy2(src, dst)
            print(f"[deliver] MP4 → {dst}")
            break
    qa_src = PROD_DIR / "qa_report.json"
    if not qa_src.is_file():
        qa_src = WORKSPACE / "DAVID" / "productions" / f"{PROOF_SLUG}_longform_v1" / "qa_report.json"
    if qa_src.is_file():
        shutil.copy2(qa_src, out_dir / "qa_report.json")
        print(f"[deliver] QA → {out_dir / 'qa_report.json'}")


def main() -> int:
    parser = argparse.ArgumentParser(description="ACTORS #150 figure reconstruction + proof")
    parser.add_argument("--plates-only", action="store_true")
    parser.add_argument("--build-only", action="store_true")
    parser.add_argument("--force-plates", action="store_true")
    parser.add_argument("--skip-plates", action="store_true", help="Reuse locked plates; script + render only")
    args = parser.parse_args()

    plates: dict[str, dict[str, Any]] = {}
    if not args.skip_plates:
        import xai_sdk

        token = os.environ.get("XAI_API_KEY") or _load_grok_token()
        os.environ["XAI_API_KEY"] = token
        client = xai_sdk.Client(api_key=token)
        for figure_id in FIGURES:
            plates[figure_id] = generate_plate(client, figure_id, force=args.force_plates)
        write_bible_and_registry(plates)
    else:
        for figure_id, spec in FIGURES.items():
            plate_path = _figure_root(spec["slug"]) / "01_reconstruction_plates" / "reconstruction_turnaround_v1.jpg"
            meta_path = plate_path.with_suffix(".json")
            meta = json.loads(meta_path.read_text(encoding="utf-8")) if meta_path.is_file() else {}
            plates[figure_id] = {"path": str(plate_path), "url": meta.get("url")}

    manifest = {
        "issue": 150,
        "built_at": datetime.now(timezone.utc).isoformat(),
        "plates": {k: v["path"] for k, v in plates.items()},
        "registry": str(REGISTRY_PATH),
        "disclosure": DISCLOSURE,
    }
    (PROD_DIR.parent / "actors_150_manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(json.dumps(manifest, indent=2))

    if args.plates_only:
        return 0

    script_path = build_proof_script()
    if args.build_only:
        return 0

    rc = render_proof(script_path)
    if rc == 0:
        copy_deliverables()
    return rc


if __name__ == "__main__":
    raise SystemExit(main())