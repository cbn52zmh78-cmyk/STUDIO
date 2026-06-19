#!/usr/bin/env python3
"""Move loose GFE root files into per-actress folders."""

from __future__ import annotations

import sys
from pathlib import Path

GFE_ROOT = Path(__file__).resolve().parent.parent
STUDIO_ROOT = GFE_ROOT.parent / "Studio"
_SCRIPTS_DIR = Path(__file__).resolve().parent
for p in (_SCRIPTS_DIR, _SCRIPTS_DIR.parent / "lib", STUDIO_ROOT):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

import re
import shutil
from pathlib import Path

from actor_profile_generator import STUDIO_ROOT

GFE_DIR = STUDIO_ROOT / "GFE"

_PDF = re.compile(r"^(.+)_Actor_Profile\.pdf$", re.I)
_TXT = re.compile(r"^(.+)_Casting_Shot_3View\.txt$", re.I)
_JPG = re.compile(r"^(.+)_Casting_Composite_v1\.jpg$", re.I)


def organize() -> list[str]:
    moves: list[str] = []
    for path in sorted(GFE_DIR.iterdir()):
        if not path.is_file():
            continue
        name = path.name
        actor_name = None
        dest: Path | None = None

        if m := _PDF.match(name):
            actor_name = m.group(1)
            dest = GFE_DIR / actor_name / "actor_profile.pdf"
        elif m := _TXT.match(name):
            actor_name = m.group(1)
            dest = GFE_DIR / actor_name / "02_reference_views" / "casting_shot_3view.txt"
        elif m := _JPG.match(name):
            actor_name = m.group(1)
            dest = GFE_DIR / actor_name / "02_reference_views" / "casting_composite_v1.jpg"

        if actor_name and dest:
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(path), str(dest))
            moves.append(f"{name} → {dest.relative_to(STUDIO_ROOT)}")

    return moves


def main() -> int:
    moves = organize()
    if not moves:
        print("No loose files to move.")
        return 0
    print(f"Organized {len(moves)} file(s):\n")
    for line in moves:
        print(f"  {line}")
    remaining = [p.name for p in GFE_DIR.iterdir() if p.is_file()]
    if remaining:
        print(f"\nWarning: {len(remaining)} file(s) still at GFE root: {remaining}")
        return 1
    print("\nGFE root is clean (directories only).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())