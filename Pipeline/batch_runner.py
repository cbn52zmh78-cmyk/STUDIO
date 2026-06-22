#!/usr/bin/env python3
"""STUDIO batch runner — MP4 → upload kit pipeline for the DAVID slate.

Usage:
    python batch_runner.py --slate dead_languages [--package] [--thumbnails] [--dry-run] [--episode SLUG]

Flags:
    --slate       Slate to process. Currently supported: dead_languages
    --package     Run package_episode() for episodes that have script + MP4.
    --thumbnails  Generate thumbnail specs for PACKAGED or READY_TO_PACKAGE episodes.
    --dry-run     Report status only; do not write any files.
    --episode     Limit to a single episode slug.

Exit codes:
    0  All episodes in scope are PACKAGED or CONCEPT_ONLY.
    1  One or more episodes have missing dependencies.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any

ROOT         = Path(__file__).resolve().parents[2]
SCRIPTS_DIR  = ROOT / "DAVID" / "scripts" / "longform_scripts"
PRODS_DIR    = ROOT / "DAVID" / "productions"
PIPELINE_DIR = Path(__file__).resolve().parent
THUMB_DIR    = ROOT / "STUDIO" / "Art_Department" / "Thumbnails"


# ── Slate definitions ─────────────────────────────────────────────────────────
# Source: STUDIO/Pipeline/Concepts/dead_languages/DEAD_LANGUAGE_SLATE_v1.md
# Tiers: launch (eps 1-6), backlog (eps 7-12, #168), extension (eps 13-18, T3 #141)

DEAD_LANGUAGES_SLATE: list[dict[str, Any]] = [
    # ── Launch six ────────────────────────────────────────────────────────────
    {"ep":  1, "slug": "david_latin_corpus_v1",
     "title": "Why Latin Never Really Died",                       "tier": "launch"},
    {"ep":  2, "slug": "david_ancient_greek_corpus_v1",
     "title": "Restoring the Pitch Accent",                        "tier": "launch"},
    {"ep":  3, "slug": "david_old_english_corpus_v1",
     "title": "Beowulf's Tongue in Manuscript",                    "tier": "launch"},
    {"ep":  4, "slug": "david_old_norse_corpus_v1",
     "title": "Runes Attested, Sagas Reconstructed",               "tier": "launch"},
    {"ep":  5, "slug": "david_gothic_corpus_v1",
     "title": "A Language Saved by One Bible",                     "tier": "launch"},
    {"ep":  6, "slug": "david_sumerian_corpus_v1",
     "title": "The First Written Language",                        "tier": "launch"},
    # ── Backlog (eps 7-12, #168) ──────────────────────────────────────────────
    {"ep":  7, "slug": "david_sanskrit_corpus_v1",
     "title": "The Language Memory Kept Alive",                    "tier": "backlog"},
    {"ep":  8, "slug": "david_biblical_hebrew_corpus_v1",
     "title": "The Language That Came Back",                       "tier": "backlog"},
    {"ep":  9, "slug": "david_akkadian_corpus_v1",
     "title": "The Voice Inside the Clay",                         "tier": "backlog"},
    {"ep": 10, "slug": "david_middle_egyptian_corpus_v1",
     "title": "The Sound Behind the Hieroglyphs",                  "tier": "backlog"},
    {"ep": 11, "slug": "david_classical_nahuatl_corpus_v1",
     "title": "The Tongue the Conquest Wrote Down",                "tier": "backlog"},
    {"ep": 12, "slug": "david_old_church_slavonic_corpus_v1",
     "title": "The Bible That Built an Alphabet",                  "tier": "backlog"},
    # ── Slate extension (eps 13-18, T3 #141 · concept/brief only) ────────────
    {"ep": 13, "slug": "david_hittite_corpus_v1",
     "title": "The Language That Rewrote the Family Tree",         "tier": "extension"},
    {"ep": 14, "slug": "david_classical_japanese_corpus_v1",
     "title": "The Court Language Hidden in Plain Sight",          "tier": "extension"},
    {"ep": 15, "slug": "david_etruscan_corpus_v1",
     "title": "The Tongue Rome Learned Its Alphabet From",         "tier": "extension"},
    {"ep": 16, "slug": "david_proto_indo_european_corpus_v1",
     "title": "The Language No One Wrote Down",                    "tier": "extension"},
    {"ep": 17, "slug": "david_linear_a_corpus_v1",
     "title": "The Script We Can Read but Cannot Understand",      "tier": "extension"},
    {"ep": 18, "slug": "david_coptic_corpus_v1",
     "title": "The Vowels Egyptian Never Wrote",                   "tier": "extension"},
]

SLATES: dict[str, list[dict[str, Any]]] = {
    "dead_languages": DEAD_LANGUAGES_SLATE,
}


# ── Path helpers ──────────────────────────────────────────────────────────────

def _script_path(slug: str) -> Path:
    return SCRIPTS_DIR / f"{slug}_script.json"


def _prod_dir(slug: str) -> Path:
    return PRODS_DIR / f"{slug}_longform_v1"


def _find_mp4(slug: str) -> Path | None:
    out = _prod_dir(slug) / "output"
    if not out.is_dir():
        return None
    for pattern in (
        f"*_{slug}_seamless_v1.mp4",
        f"*_{slug}_longform_v1.mp4",
        "*.mp4",
    ):
        hits = sorted(out.glob(pattern), key=lambda p: p.stat().st_mtime, reverse=True)
        if hits:
            return hits[0]
    return None


def _kit_json_path(slug: str) -> Path:
    return _prod_dir(slug) / "upload_kit" / f"{slug}_upload_kit.json"


def _thumb_spec_path(slug: str) -> Path:
    return THUMB_DIR / f"{slug}_thumb_spec.json"


def _has_thumb_spec(slug: str) -> bool:
    return _thumb_spec_path(slug).is_file()


# ── Status logic ──────────────────────────────────────────────────────────────

def _episode_status(slug: str, tier: str) -> dict[str, Any]:
    has_script = _script_path(slug).is_file()
    mp4        = _find_mp4(slug)
    has_mp4    = mp4 is not None
    has_kit    = _kit_json_path(slug).is_file()

    if not has_script and tier == "extension":
        state = "CONCEPT_ONLY"
    elif not has_script:
        state = "NEEDS_INTAKE"
    elif has_kit:
        state = "PACKAGED"
    elif has_mp4:
        state = "READY_TO_PACKAGE"
    else:
        state = "READY_TO_RENDER"

    return {
        "slug":     slug,
        "script":   has_script,
        "mp4":      has_mp4,
        "mp4_path": str(mp4) if mp4 else None,
        "kit":      has_kit,
        "thumb":    _has_thumb_spec(slug),
        "state":    state,
    }


# ── Package action ────────────────────────────────────────────────────────────

def _load_package_module() -> Any:
    """Import package_episode.py fresh (bypasses sys.modules cache)."""
    import types as _types
    mod_path = PIPELINE_DIR / "package_episode.py"
    src = mod_path.read_text(encoding="utf-8")
    mod = _types.ModuleType("_package_episode_fresh")
    mod.__file__ = str(mod_path)
    exec(compile(src, str(mod_path), "exec"), mod.__dict__)  # noqa: S102
    return mod


def _run_package(
    slug: str,
    info: dict[str, Any],
    *,
    dry_run: bool,
) -> str:
    if not info["script"]:
        return "SKIP — no script.json"
    if not info["mp4"]:
        return "SKIP — no MP4 (render first)"
    if dry_run:
        return "DRY-RUN — would call package_episode()"

    try:
        mod = _load_package_module()
        out_dir = _prod_dir(slug) / "upload_kit"
        out_dir.mkdir(parents=True, exist_ok=True)
        _, kit_json, brief_txt = mod.package_episode(
            script_json_path=_script_path(slug),
            mp4_path=Path(info["mp4_path"]),
            out_dir=out_dir,
        )
        return f"OK → {kit_json.name}"
    except Exception as exc:
        return f"ERROR — {exc}"


# ── Thumbnail action ──────────────────────────────────────────────────────────

def _run_thumbnails(slug: str, ep_meta: dict[str, Any], *, dry_run: bool) -> str:
    """Generate thumbnail specs (A+B) for a single episode via thumbnail_generator."""
    if dry_run:
        return "DRY-RUN — would call thumbnail_generator"
    if _has_thumb_spec(slug):
        return "SKIP — spec already exists"
    try:
        import importlib.util as _ilu
        spec_mod = _ilu.spec_from_file_location(
            "thumbnail_generator",
            PIPELINE_DIR / "thumbnail_generator.py",
        )
        assert spec_mod and spec_mod.loader
        mod = _ilu.module_from_spec(spec_mod)
        spec_mod.loader.exec_module(mod)  # type: ignore[attr-defined]
        # Find the episode dict from the generator's internal slate
        all_eps = [e for slate in mod.SLATES.values() for e in slate]
        matches = [e for e in all_eps if e["slug"] == slug]
        if not matches:
            return f"SKIP — slug not found in thumbnail_generator slate"
        ep = matches[0]
        for variant in ("A", "B"):
            thumb_spec = mod.generate_thumbnail_spec(ep, variant)
            mod._write_single_spec_json(thumb_spec, THUMB_DIR)
        return f"OK → {slug}_thumb_spec.json (A+B)"
    except Exception as exc:
        return f"ERROR — {exc}"


# ── Table printer ─────────────────────────────────────────────────────────────

def _print_table(rows: list[dict[str, Any]]) -> None:
    col_slug = max(len(r["slug"]) for r in rows) + 2

    header = (
        f"{'EP':>3}  {'TIER':<10}  "
        f"{'SLUG':<{col_slug}}  "
        f"{'SCRIPT':<7}  {'MP4':<7}  {'KIT':<7}  {'THUMB':<7}  STATUS"
    )
    sep = "─" * (len(header) + 4)

    print()
    print(header)
    print(sep)
    for r in rows:
        s_mark = "✓" if r["script"] else "✗"
        m_mark = "✓" if r["mp4"]    else "✗"
        k_mark = "✓" if r["kit"]    else "✗"
        t_mark = "✓" if r.get("thumb") else "✗"
        print(
            f"{r['ep']:>3}  {r['tier']:<10}  "
            f"{r['slug']:<{col_slug}}  "
            f"{s_mark:<7}  {m_mark:<7}  {k_mark:<7}  {t_mark:<7}  {r['state']}"
        )
    print(sep)

    total   = len(rows)
    by_state: dict[str, int] = {}
    for r in rows:
        by_state[r["state"]] = by_state.get(r["state"], 0) + 1

    parts = [f"Total: {total}"]
    for state in ("PACKAGED", "READY_TO_PACKAGE", "READY_TO_RENDER",
                  "CONCEPT_ONLY", "NEEDS_INTAKE"):
        n = by_state.get(state, 0)
        if n:
            label = state.replace("_", "-").lower()
            parts.append(f"{label}: {n}")
    print("  " + "  |  ".join(parts))
    print()


# ── Main ──────────────────────────────────────────────────────────────────────

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="STUDIO batch runner — MP4 → upload kit pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--slate", required=True, choices=list(SLATES),
        help="Slate to process",
    )
    parser.add_argument(
        "--package", action="store_true",
        help="Run package_episode() for episodes with script + MP4",
    )
    parser.add_argument(
        "--dry-run", dest="dry_run", action="store_true",
        help="Report status only; write nothing",
    )
    parser.add_argument(
        "--episode", default=None, metavar="SLUG",
        help="Process a single episode slug",
    )
    parser.add_argument(
        "--thumbnails", action="store_true",
        help=(
            "Generate thumbnail specs (A+B) for any episode that is "
            "PACKAGED or READY_TO_PACKAGE. Calls thumbnail_generator.py."
        ),
    )
    args = parser.parse_args(argv)

    slate = SLATES[args.slate]

    # Filter to single episode if requested
    if args.episode:
        matching = [e for e in slate if e["slug"] == args.episode]
        if not matching:
            print(
                f"ERROR: episode '{args.episode}' not in slate '{args.slate}'",
                file=sys.stderr,
            )
            return 1
        slate = matching

    # Build status for all episodes in scope
    rows: list[dict[str, Any]] = []
    for ep in slate:
        info = _episode_status(ep["slug"], ep["tier"])
        info["ep"]   = ep["ep"]
        info["tier"] = ep["tier"]
        rows.append(info)

    _print_table(rows)

    any_failed = False

    # ── Package action ─────────────────────────────────────────────────────
    if args.package:
        print("\n── Packaging ─────────────────────────────────────────────")
        for row in rows:
            if row["state"] in ("CONCEPT_ONLY",):
                continue
            result = _run_package(row["slug"], row, dry_run=args.dry_run)
            status = "✓" if result.startswith("OK") else ("⟳" if result.startswith("DRY") else "✗")
            print(f"  {status}  {row['slug']:<40}  {result}")
            if result.startswith("ERROR"):
                any_failed = True

    # ── Thumbnail action ───────────────────────────────────────────────────
    if args.thumbnails:
        print("\n── Thumbnails ────────────────────────────────────────────")
        THUMB_DIR.mkdir(parents=True, exist_ok=True)
        eligible_states = ("PACKAGED", "READY_TO_PACKAGE")
        for ep, row in zip(slate, rows):
            if row["state"] not in eligible_states:
                continue
            result = _run_thumbnails(row["slug"], ep, dry_run=args.dry_run)
            status = "✓" if result.startswith("OK") else ("⟳" if result.startswith("DRY") else "✗")
            print(f"  {status}  {row['slug']:<40}  {result}")
            if result.startswith("ERROR"):
                any_failed = True

    # ── Exit code ──────────────────────────────────────────────────────────
    # Exit 1 if any episode is in a non-terminal blocking state (excluding
    # CONCEPT_ONLY which is expected for extension-tier episodes).
    blocking = [r for r in rows if r["state"] in ("NEEDS_INTAKE",)]
    if blocking or any_failed:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
