#!/usr/bin/env python3
"""Audit all 100 cast actors for schema compliance + child-safety floor-age review."""

from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

CAST_ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = CAST_ROOT.parents[1]
REGISTRY_DIR = CAST_ROOT / "Casting_Bible" / "registry"
OUT_DIR = CAST_ROOT / "Casting_Bible" / "audit"

AGE_MIN = 21
FLOOR_AGE_MAX = 22
AGE_PATTERN = re.compile(r"(\d{1,2})-year-old", re.IGNORECASE)

REGISTRIES = [
    ("actors_roster", REGISTRY_DIR / "casting_registry.json", 70),
    ("gfe", REGISTRY_DIR / "gfe_casting_registry.json", 20),
    ("magazine_editorial", REGISTRY_DIR / "magazine_casting_registry.json", 10),
]

REQUIRED_BOOL = {
    "synthetic": True,
    "real_person_likeness": False,
    "ai_disclosure_required": True,
}
REQUIRED_STATUS = {
    "reference_image_status": "plate_locked",
    "appearance_lock_status": "LOCKED",
}


def extract_prompt_age(text: str | None) -> int | None:
    if not text:
        return None
    m = AGE_PATTERN.search(text)
    return int(m.group(1)) if m else None


def resolve_image(path_str: str | None) -> Path | None:
    if not path_str:
        return None
    p = WORKSPACE / path_str.replace("/", "\\")
    return p if p.is_file() else None


def audit_actor(actor: dict, lane: str) -> dict:
    """Return per-actor compliance row."""
    actor_id = actor.get("actor_id", "UNKNOWN")
    errors: list[str] = []
    warnings: list[str] = []

    age = actor.get("age_locked")
    if age is None:
        errors.append("missing_age_locked")
    elif age < AGE_MIN:
        errors.append(f"age_below_minimum:{age}")

    for field, expected in REQUIRED_BOOL.items():
        val = actor.get(field)
        if val is None:
            errors.append(f"missing_{field}")
        elif val != expected:
            errors.append(f"{field}_invalid:{val}")

    for field, expected in REQUIRED_STATUS.items():
        val = actor.get(field)
        if val != expected:
            errors.append(f"{field}_not_{expected.lower()}:{val}")

    lock = actor.get("appearance_lock_verbatim")
    if not lock or not str(lock).strip():
        errors.append("missing_appearance_lock_verbatim")
    else:
        prompt_age = extract_prompt_age(str(lock))
        if prompt_age is None:
            errors.append("appearance_lock_missing_numerical_age")
        else:
            if prompt_age < AGE_MIN:
                errors.append(f"prompt_age_below_minimum:{prompt_age}")
            if age is not None and prompt_age != age:
                errors.append(f"age_mismatch:locked={age} prompt={prompt_age}")
        lower = str(lock).lower()
        if "synthetic" not in lower and "fictional" not in lower:
            warnings.append("appearance_lock_missing_synthetic_guard")
        if lane == "actors_roster":
            if "unambiguously 21+" not in lower and "clearly adult" not in lower:
                warnings.append("appearance_lock_missing_adult_assertion")

    img = resolve_image(actor.get("reference_image_primary"))
    if not img:
        errors.append("plate_file_missing")
    elif img.stat().st_size < 10_000:
        errors.append("plate_file_too_small")

    flags = actor.get("compliance_flags") or []
    if flags:
        warnings.extend([f"registry_flag:{f}" for f in flags])

    floor_age = age is not None and AGE_MIN <= age <= FLOOR_AGE_MAX
    child_safety = "n/a"
    if floor_age:
        child_safety = "REQUIRES_VISUAL_REVIEW"

    status = "BLOCKED" if errors else ("FLAG" if warnings or floor_age else "CLEAR")

    return {
        "actor_id": actor_id,
        "stage_name": actor.get("stage_name"),
        "lane": lane,
        "age_locked": age,
        "floor_age_entry": floor_age,
        "synthetic": actor.get("synthetic"),
        "real_person_likeness": actor.get("real_person_likeness"),
        "ai_disclosure_required": actor.get("ai_disclosure_required"),
        "plate_locked": actor.get("reference_image_status") == "plate_locked",
        "appearance_lock_locked": actor.get("appearance_lock_status") == "LOCKED",
        "plate_path": actor.get("reference_image_primary"),
        "plate_exists": img is not None,
        "child_safety_visual": child_safety,
        "errors": errors,
        "warnings": warnings,
        "status": status,
        "use_blocked": bool(errors),
    }


# Manual visual review results (floor-age 21–22) + known plate/lock mismatches.
VISUAL_REVIEWS: dict[str, dict] = {
    "Yuki-001": {
        "verdict": "PASS",
        "reads_adult": True,
        "borderline": False,
        "notes": "Slender petite build; mature bone structure and adult proportions. Unambiguously 21+.",
    },
    "HanaGFE-001": {
        "verdict": "PASS",
        "reads_adult": True,
        "borderline": False,
        "notes": "Petite East Asian; adult facial structure and body. No teen indicators.",
    },
    "LyraGFE-001": {
        "verdict": "PASS",
        "reads_adult": True,
        "borderline": False,
        "notes": "Slim-athletic; smiling adult features, developed proportions.",
    },
    "VioletGFE-001": {
        "verdict": "PASS",
        "reads_adult": True,
        "borderline": False,
        "notes": "Curvy adult physique; mid-20s read. No ambiguous youth markers.",
    },
    "YumeGFE-001": {
        "verdict": "PASS",
        "reads_adult": True,
        "borderline": False,
        "notes": "Floor age 21; voluptuous adult body and mature face. No borderline flags.",
    },
    "FreyaLindMag-001": {
        "verdict": "FAIL",
        "reads_adult": True,
        "borderline": False,
        "notes": "PLATE/LOCK MISMATCH: plate shows dark-skinned African-styled model; lock specifies Swedish strawberry-blonde freckled fair skin. Re-roll required.",
        "plate_lock_mismatch": True,
    },
}

SOFT_BLOCK_WARNINGS = frozenset({
    "appearance_lock_missing_synthetic_guard",
    "appearance_lock_missing_adult_assertion",
})


def apply_visual_review(row: dict) -> dict:
    actor_id = row["actor_id"]
    review = VISUAL_REVIEWS.get(actor_id)
    if not review:
        return row
    row = {**row}
    row["child_safety_visual"] = review["verdict"]
    row["visual_review"] = review
    if review.get("plate_lock_mismatch"):
        row["errors"] = [*row["errors"], "plate_lock_mismatch"]
        row["status"] = "BLOCKED"
        row["use_blocked"] = True
    elif review["verdict"] == "FAIL":
        row["errors"] = [*row["errors"], "child_safety_visual_fail"]
        row["status"] = "BLOCKED"
        row["use_blocked"] = True
    elif review.get("borderline"):
        row["warnings"] = [*row["warnings"], "child_safety_borderline_visual"]
        if row["status"] == "CLEAR":
            row["status"] = "FLAG"
    return row


def run_audit() -> dict:
    rows: list[dict] = []
    counts = {"total": 0, "clear": 0, "flag": 0, "blocked": 0, "floor_age": 0}

    for lane, path, expected in REGISTRIES:
        data = json.loads(path.read_text(encoding="utf-8"))
        actors = data.get("actors", [])
        if len(actors) != expected:
            raise RuntimeError(f"{lane}: expected {expected} actors, got {len(actors)}")
        for actor in actors:
            row = apply_visual_review(audit_actor(actor, lane))
            rows.append(row)
            counts["total"] += 1
            if row["floor_age_entry"]:
                counts["floor_age"] += 1
            if row["status"] == "BLOCKED":
                counts["blocked"] += 1
            elif row["status"] == "FLAG":
                counts["flag"] += 1
            else:
                counts["clear"] += 1

    if counts["total"] != 100:
        raise RuntimeError(f"Expected 100 actors total, got {counts['total']}")

    rows.sort(key=lambda r: (r["lane"], r["actor_id"]))
    blocked = [r["actor_id"] for r in rows if r["use_blocked"]]
    floor_age = [r for r in rows if r["floor_age_entry"]]
    reroll = [
        r["actor_id"]
        for r in rows
        if r.get("visual_review", {}).get("plate_lock_mismatch")
        or "child_safety_borderline_visual" in r.get("warnings", [])
    ]
    prompt_hygiene = [
        r["actor_id"]
        for r in rows
        if r["status"] == "FLAG"
        and not r["use_blocked"]
        and any(w in SOFT_BLOCK_WARNINGS for w in r.get("warnings", []))
    ]

    return {
        "version": "1.0.0",
        "audited_at": datetime.now(timezone.utc).isoformat(),
        "policy": {
            "age_minimum": AGE_MIN,
            "floor_age_review_range": f"{AGE_MIN}-{FLOOR_AGE_MAX}",
            "required_fields": list(REQUIRED_BOOL) + list(REQUIRED_STATUS),
        },
        "summary": counts,
        "blocked_actor_ids": blocked,
        "reroll_actor_ids": reroll,
        "prompt_hygiene_flag_ids": prompt_hygiene,
        "floor_age_actor_ids": [r["actor_id"] for r in floor_age],
        "floor_age_visual_pass": [
            r["actor_id"] for r in floor_age if r.get("child_safety_visual") == "PASS"
        ],
        "matrix": rows,
    }


def write_outputs(report: dict) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "compliance_matrix.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )

    blocked_registry = {
        "version": "1.0.0",
        "updated_at": report["audited_at"],
        "policy": "BLOCKED actors cannot be used in any production until remediated.",
        "blocked": report["blocked_actor_ids"],
        "reroll_required": report["reroll_actor_ids"],
        "prompt_hygiene_flags": report["prompt_hygiene_flag_ids"],
        "floor_age_visual_pass": report["floor_age_visual_pass"],
    }
    (OUT_DIR / "blocked_actors.json").write_text(
        json.dumps(blocked_registry, indent=2) + "\n", encoding="utf-8"
    )

    lines = [
        "# Cast Compliance Audit — 100 Actors",
        f"**Audited:** {report['audited_at']}",
        "",
        "## Summary",
        f"- **Total:** {report['summary']['total']}",
        f"- **CLEAR:** {report['summary']['clear']}",
        f"- **FLAG:** {report['summary']['flag']}",
        f"- **BLOCKED:** {report['summary']['blocked']}",
        f"- **Floor-age (21–22) visual review:** {report['summary']['floor_age']}",
        "",
        "## Blocked (schema non-compliant)",
    ]
    if report["blocked_actor_ids"]:
        for aid in report["blocked_actor_ids"]:
            row = next(r for r in report["matrix"] if r["actor_id"] == aid)
            lines.append(f"- `{aid}` — {', '.join(row['errors'])}")
    else:
        lines.append("- None")

    lines.extend(["", "## Re-roll required", ""])
    if report["reroll_actor_ids"]:
        for aid in report["reroll_actor_ids"]:
            row = next(r for r in report["matrix"] if r["actor_id"] == aid)
            notes = row.get("visual_review", {}).get("notes", "")
            lines.append(f"- `{aid}` — {notes}")
    else:
        lines.append("- None")

    lines.extend(["", "## Floor-age entries (21–22) — visual review", ""])
    for row in report["matrix"]:
        if row["floor_age_entry"]:
            vr = row.get("visual_review", {})
            lines.append(
                f"- `{row['actor_id']}` ({row['lane']}) age={row['age_locked']} "
                f"visual={row['child_safety_visual']} — {vr.get('notes', 'pending')}"
            )

    lines.extend(["", "## Prompt hygiene flags (usable, lock text should be patched)", ""])
    lines.append(f"- Count: {len(report['prompt_hygiene_flag_ids'])}")
    lines.append(f"- Lanes: 35 male roster + 20 GFE + 10 MAGAZINE missing explicit synthetic/adult clauses in appearance_lock_verbatim")

    lines.extend(["", "## Full matrix", ""])
    lines.append(
        "| actor_id | lane | age | synth | likeness | disclosure | plate | lock | status |"
    )
    lines.append("|---|---|---:|:-:|:-:|:-:|:-:|:-:|---|")
    for r in report["matrix"]:
        yn = lambda v: "✓" if v else "✗"
        lines.append(
            f"| {r['actor_id']} | {r['lane']} | {r['age_locked']} | "
            f"{yn(r['synthetic'])} | {yn(r['real_person_likeness'] is False)} | "
            f"{yn(r['ai_disclosure_required'])} | {yn(r['plate_locked'])} | "
            f"{yn(r['appearance_lock_locked'])} | **{r['status']}** |"
        )

    (OUT_DIR / "compliance_matrix.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    report = run_audit()
    write_outputs(report)
    s = report["summary"]
    print(f"Audited {s['total']} actors: CLEAR={s['clear']} FLAG={s['flag']} BLOCKED={s['blocked']}")
    print(f"Floor-age entries: {s['floor_age']}")
    if report["blocked_actor_ids"]:
        print(f"BLOCKED: {', '.join(report['blocked_actor_ids'])}")
    print(f"Wrote {OUT_DIR / 'compliance_matrix.json'}")
    return 1 if s["blocked"] else 0


if __name__ == "__main__":
    sys.exit(main())