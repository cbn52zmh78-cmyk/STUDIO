#!/usr/bin/env python3
"""Print (or save) the canonical casting-shot prompt for a person description."""
import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from studio.prompting.production_images import build_casting_shot_prompt  # noqa: E402


def slugify(text: str) -> str:
    return re.sub(r"[^\w\-]+", "_", text.lower()).strip("_")[:48] or "subject"


def main() -> int:
    parser = argparse.ArgumentParser(
        description='Build casting-shot prompt from person description.'
    )
    parser.add_argument(
        "description",
        nargs="*",
        help='Person description (words after "casting shot")',
    )
    args = parser.parse_args()
    desc = " ".join(args.description).strip()
    if not desc:
        print("Usage: casting_shot.py <person description>", file=sys.stderr)
        return 1

    prompt = build_casting_shot_prompt(desc)
    out = ROOT / "renders" / "casting_plates" / f"casting_prompt_{slugify(desc)}.txt"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(prompt + "\n", encoding="utf-8")
    print(prompt)
    print(f"\n✅ Prompt saved → {out}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())