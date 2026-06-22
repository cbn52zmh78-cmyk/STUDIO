#!/usr/bin/env python3
"""Pre-fill GFE ASMR camera-interaction prompts for all roster actresses."""

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
import sys
from pathlib import Path

# --- qa_gate wiring ---
_AI_FED = Path(__file__).resolve().parents[4] / "AI" / "federation"
if str(_AI_FED) not in sys.path:
    sys.path.insert(0, str(_AI_FED))
try:
    from qa_gate import qa_check as _qa_gate_check
    _QA_GATE_AVAILABLE = True
except ImportError:
    _QA_GATE_AVAILABLE = False
# --- end qa_gate wiring ---

from actor_profile_generator import ActorProfile, STUDIO_ROOT
from ensure_gfe_folder_structure import ensure_actor_dirs
from gfe_roster_data import GFE_ROSTER_20

GFE_DIR = STUDIO_ROOT / "GFE"
OUT_NAME = "asmr_camera_interaction_v1.txt"
INDEX_NAME = "GFE_ASMR_All_Prompts_v1.1.md"

_TAIL = (
    "extreme close-up personal attention POV in low light bedroom, sustained eye contact "
    "directly into camera as if speaking only to viewer, soft-spoken breathy whispering "
    "with ear-to-ear intimacy and warm teasing affirmations, slow deliberate leaning in "
    "and hand gestures brushing toward lens, {performance}, static camera with subtle "
    "motivated leans for intimacy, natural physics realistic skin detail and tattoo "
    "visibility, soft directional lighting highlighting eyes, lips and ink"
)


def _tattoo_label(actor: ActorProfile) -> str:
    inv = actor.tattoo_inventory
    if inv.startswith("Heavy"):
        return "full irezumi sleeves floral choker band and thigh panels"
    if inv.startswith("Moderate"):
        return "botanical half-sleeve sternum and ankle tattoos"
    if inv.startswith("Light"):
        return "subtle wrist collarbone and thigh script tattoos"
    return "no visible tattoos"


def _physical_compact(actor: ActorProfile) -> str:
    text = actor.base_physical_description.strip().rstrip(".")
    text = re.sub(r"^5'[\d.]+\"\s*,?\s*", "", text)
    return text


def _signature_hook(actor: ActorProfile) -> str:
    raw = actor.signature_looks.replace(";", ",").split(",")[0].strip().lower()
    return raw.rstrip(".")


def _pick_outfit(actor: ActorProfile) -> str:
    if _tattoo_label(actor).startswith("full") or _tattoo_label(actor).startswith("botanical"):
        return "red string bikini"
    sig = actor.signature_looks.lower()
    if "satin" in sig or "slip" in sig or "ivory" in actor.casting_wardrobe_color:
        return "white satin slip with black lace trim"
    return "white string bikini"


def _archetype_performance(actor: ActorProfile) -> str:
    mood = actor.on_screen_mood.strip().rstrip(".")
    archetype = actor.archetypes[0].lower() if actor.archetypes else "intimate girlfriend"
    return f"{mood}, {archetype} energy with micro-expressions and teasing winks"


def build_asmr_prompt(actor: ActorProfile) -> str:
    visuals = (
        f"{_tattoo_label(actor)}, {_signature_hook(actor)}, {_physical_compact(actor)}"
    )
    head = (
        f"{actor.age}-year-old woman named {actor.stage_name}, {actor.ethnicity} with "
        f"{visuals}, wearing {_pick_outfit(actor)}, "
    )
    return head + _TAIL.format(performance=_archetype_performance(actor))


def write_prompt(actor: ActorProfile) -> Path:
    ensure_actor_dirs(actor.stage_name)
    clips_dir = GFE_DIR / actor.stage_name / "CLIPS"
    out = clips_dir / OUT_NAME
    prompt = build_asmr_prompt(actor)
    # --- qa_gate: QA narration prompt before write ---
    if _QA_GATE_AVAILABLE and prompt.strip():
        try:
            _qa_asmr = _qa_gate_check(
                content=prompt,
                content_type="narration",
                subject=actor.stage_name,
            )
            if _qa_asmr["gate"] == "RED":
                print(
                    f"[QA HOLD] generate_gfe_asmr_prompts.py: {_qa_asmr['summary']} | Issues: {_qa_asmr['issues']}",
                    file=sys.stderr,
                )
                return out  # skip write on RED
            elif _qa_asmr["gate"] == "YELLOW":
                print(
                    f"[QA WARN] generate_gfe_asmr_prompts.py: {_qa_asmr['summary']}",
                    file=sys.stderr,
                )
        except Exception as _exc:
            print(f"[QA WARN] generate_gfe_asmr_prompts.py: qa_gate error: {_exc}", file=sys.stderr)
    # --- end qa_gate ---
    body = (
        f"# ASMR Camera Interaction — {actor.stage_name}\n"
        f"# Library: GFE_ASMR_Camera_Interaction_Library_v1.1.md\n"
        f"# Casting ref: 01_casting_shots/casting_turnaround_v1.jpg\n\n"
        f"{prompt}\n"
    )
    out.write_text(body, encoding="utf-8")
    return out


def write_index(paths: list[tuple[ActorProfile, Path]]) -> Path:
    lines = [
        "# GFE ASMR Camera Interaction — All Prompts v1.1",
        "",
        "Pre-filled from roster canon. One file per actress in `{Name}/CLIPS/asmr_camera_interaction_v1.txt`.",
        "",
    ]
    for actor, rel in paths:
        prompt = build_asmr_prompt(actor)
        lines.extend(
            [
                f"## {actor.stage_name} ({actor.age})",
                f"**File:** `{rel}`",
                "",
                "```",
                prompt,
                "```",
                "",
            ]
        )
    index = GFE_DIR / INDEX_NAME
    index.write_text("\n".join(lines), encoding="utf-8")
    return index


def main() -> int:
    print("\nGFE ASMR prompt generator\n")
    entries: list[tuple[ActorProfile, str]] = []
    for actor in GFE_ROSTER_20:
        path = write_prompt(actor)
        rel = str(path.relative_to(STUDIO_ROOT)).replace("\\", "/")
        entries.append((actor, rel))
        print(f"  ✅ {actor.stage_name} → {rel}")

    index = write_index(entries)
    print(f"\nIndex: {index.relative_to(STUDIO_ROOT)}")
    print(f"Done: {len(entries)}/20 prompts")
    return 0 if len(entries) == 20 else 1


if __name__ == "__main__":
    sys.exit(main())