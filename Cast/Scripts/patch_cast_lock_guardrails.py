#!/usr/bin/env python3
"""Append standard synthetic + adult guard clauses to appearance locks (source files only)."""

from __future__ import annotations

import re
import sys
from pathlib import Path

CAST_ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = CAST_ROOT.parent.parent
MAG_MODELS = WORKSPACE / "STUDIO" / "MAGAZINE" / "Editorial" / "Models"

TURNAROUND_SUFFIX = (
    " Synthetic fictional character only. No real person or celebrity likeness. "
    "Clearly adult with mature facial features and adult bone structure — "
    "unambiguously 21+ adult, not teen, not school-age."
)
MAGAZINE_INLINE = (
    ", clearly adult woman unambiguously 21+, synthetic fictional character only, "
    "no real-person likeness"
)


def has_synthetic(text: str) -> bool:
    lower = text.lower()
    return "synthetic" in lower or "fictional" in lower


def has_adult_assertion(text: str) -> bool:
    lower = text.lower()
    return "unambiguously 21+" in lower or "clearly adult" in lower


def patch_turnaround(text: str, *, require_adult: bool) -> tuple[str, bool]:
    original = text.strip()
    if not original:
        return original, False
    changed = False
    out = original
    if not has_synthetic(out):
        out = out.rstrip(".") + TURNAROUND_SUFFIX
        changed = True
    elif require_adult and not has_adult_assertion(out):
        out = (
            out.rstrip(".")
            + " Clearly adult with mature facial features and adult bone structure — "
            "unambiguously 21+ adult, not teen, not school-age."
        )
        changed = True
    return out, changed


def patch_magazine_studio(path: Path) -> bool:
    raw = path.read_text(encoding="utf-8")
    lines = raw.splitlines()
    changed = False
    new_lines: list[str] = []
    for line in lines:
        stripped = line.strip()
        if (
            not stripped.startswith("#")
            and stripped
            and (stripped.lower().startswith("photorealistic") or "year-old" in stripped)
        ):
            if not has_synthetic(stripped):
                if MAGAZINE_INLINE.strip(", ") not in stripped:
                    stripped = stripped.rstrip(".") + MAGAZINE_INLINE
                    changed = True
            new_lines.append(stripped)
        else:
            new_lines.append(line)
    if changed:
        path.write_text("\n".join(new_lines) + ("\n" if raw.endswith("\n") else ""), encoding="utf-8")
    return changed


def main() -> int:
    patched = 0
    for prompt_path in sorted(CAST_ROOT.glob("actors_roster/**/01_casting_shots/casting_prompt.txt")):
        text = prompt_path.read_text(encoding="utf-8")
        new_text, changed = patch_turnaround(text, require_adult=True)
        if changed:
            prompt_path.write_text(new_text + ("\n" if text.endswith("\n") else ""), encoding="utf-8")
            patched += 1
            print(f"  roster: {prompt_path.parent.parent.name}")

    for prompt_path in sorted((CAST_ROOT / "GFE").glob("*/01_casting_shots/casting_prompt.txt")):
        text = prompt_path.read_text(encoding="utf-8")
        new_text, changed = patch_turnaround(text, require_adult=False)
        if changed:
            prompt_path.write_text(new_text + ("\n" if text.endswith("\n") else ""), encoding="utf-8")
            patched += 1
            print(f"  gfe: {prompt_path.parent.parent.name}")

    if MAG_MODELS.is_dir():
        for studio_path in sorted(MAG_MODELS.glob("*/01_casting_shots/*_Supermodel_Magazine_studio.txt")):
            if patch_magazine_studio(studio_path):
                patched += 1
                print(f"  magazine: {studio_path.parent.parent.name}")

    print(f"Patched {patched} source lock file(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())