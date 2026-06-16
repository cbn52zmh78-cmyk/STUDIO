#!/usr/bin/env python3
"""
Actor Profile Generator — STUDIO artifacts
Builds locked director-bible actor profiles (Markdown + PDF).

API:
    from actor_profile_generator import ActorProfile, generate_actor_profile_pdf
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from datetime import date, datetime
from pathlib import Path
from xml.sax.saxutils import escape

ARTIFACTS_ROOT = Path(__file__).resolve().parent
DEFAULT_OUTPUT = ARTIFACTS_ROOT / "output" / "profiles"

COMPLIANCE_FOOTER = (
    "All prompts must begin with exact numerical age. "
    "Intimate work: Cinematic_Intimacy_Safe_Legal_Protocol_v1.3. "
    "Protect the studio above all."
)


@dataclass
class ActorProfile:
    stage_name: str
    full_legal_name: str
    professional_stage_name: str
    age: int
    date_of_birth: str
    ethnicity: str
    nationality: str
    heritage: str
    languages: list[str]
    base_physical_description: str
    archetypes: list[str]
    performance_style: str
    voice_notes: str
    on_screen_comfort: str
    personality: str
    base_reference_images: list[str]
    tattoo_inventory: str
    signature_looks: str
    casting_notes: str
    profile_date: str = field(default_factory=lambda: datetime.now().strftime("%B %d, %Y"))

    def prompt_prefix(self) -> str:
        """Required opening for every generation prompt."""
        return f"{self.age}-year-old {self.ethnicity} woman"

    def _has_tattoos(self) -> bool:
        inv = self.tattoo_inventory.strip().lower()
        return bool(inv) and not inv.startswith("none")

    def build_actor_generation_prompt(
        self,
        *,
        wardrobe: str | None = None,
        scene: str = (
            "casting reference plate, neutral expression, three-quarter portrait, "
            "photorealistic, soft studio lighting, director bible likeness lock"
        ),
    ) -> str:
        """Full copy-paste prompt to generate the actor from physical canon."""
        segments = [
            self.prompt_prefix() + ".",
            self.base_physical_description.strip().rstrip("."),
            f"Heritage: {self.heritage.strip().rstrip('.')}.",
        ]
        if self.signature_looks.strip():
            segments.append(f"Signature look: {self.signature_looks.strip().rstrip('.')}.")
        if self._has_tattoos():
            segments.append(f"Tattoo continuity: {self.tattoo_inventory.strip().rstrip('.')}.")
        else:
            segments.append("No visible tattoos.")
        if wardrobe:
            segments.append(f"Wearing: {wardrobe.strip().rstrip('.')}.")
        segments.append(scene.rstrip(".") + ".")
        return " ".join(segments)

    def build_wardrobe_generation_prompts(self) -> list[tuple[str, str]]:
        """Wardrobe-anchor variant prompts from base_reference_images."""
        return [
            (label, self.build_actor_generation_prompt(wardrobe=label))
            for label in self.base_reference_images
        ]

    def pdf_basename(self) -> str:
        return f"{slugify(self.stage_name)}_Actor_Profile.pdf"

    def markdown_basename(self) -> str:
        return f"{slugify(self.stage_name)}_Actor_Profile.md"


def slugify(name: str) -> str:
    return re.sub(r"[^\w\-]+", "_", name.lower()).strip("_") or "actor"


def _para(text: str) -> str:
    return escape(str(text)).replace("\n", "<br/>")


def _bullet_list(items: list[str]) -> str:
    if not items:
        return "—"
    return "<br/>".join(f"• {_para(item)}" for item in items)


def build_markdown(actor: ActorProfile) -> str:
    langs = "\n".join(f"- {lang}" for lang in actor.languages) or "- —"
    archetypes = "\n".join(f"- {a}" for a in actor.archetypes) or "- —"
    refs = "\n".join(f"- {r}" for r in actor.base_reference_images) or "- —"

    return f"""# {actor.stage_name} — Actor Profile

**Profile date:** {actor.profile_date}  
**Status:** Locked director reference

## Identity
| Field | Value |
|-------|-------|
| Stage name | {actor.stage_name} |
| Full legal name | {actor.full_legal_name} |
| Professional stage name | {actor.professional_stage_name} |
| Age (locked) | **{actor.age}** |
| Date of birth | {actor.date_of_birth} |
| Ethnicity | {actor.ethnicity} |
| Nationality | {actor.nationality} |
| Heritage | {actor.heritage} |

## Languages
{langs}

## Physical Description
{actor.base_physical_description}

## Tattoo Inventory
{actor.tattoo_inventory}

## Signature Looks
{actor.signature_looks}

## Archetypes
{archetypes}

## Performance Style
{actor.performance_style}

## Voice Notes
{actor.voice_notes}

## On-Screen Comfort
{actor.on_screen_comfort}

## Personality
{actor.personality}

## Base Reference Images / Wardrobe Anchors
{refs}

## Casting Notes
{actor.casting_notes}

## Actor Generation Prompt (Copy-Paste)

**Foundation casting prompt:**

```
{actor.build_actor_generation_prompt()}
```

**Wardrobe variant prompts:**

{chr(10).join(f"- **{label}:** `{prompt}`" for label, prompt in actor.build_wardrobe_generation_prompts()) or "- —"}

## Prompting Rules (Non-Negotiable)
1. **Always lead with exact age:** `{actor.prompt_prefix()}...`
2. Reference assets before scene generation.
3. Clinical/neutral language for intimate or sensual beats.
4. Extensions only — no new foundation prompt mid-sequence.
5. Topless: one baked/reference actor + one prompt-generated (Protocol v1.3).

## Compliance
- {COMPLIANCE_FOOTER}

---
*STUDIO Actor Profile — Director Bible*
"""


def generate_actor_profile_pdf(
    actor: ActorProfile,
    output_path: str | Path | None = None,
) -> Path:
    """Render a director-bible PDF for the given actor profile."""
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_CENTER
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
    from reportlab.lib.units import inch
    from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

    out = Path(output_path) if output_path else DEFAULT_OUTPUT / actor.pdf_basename()
    out.parent.mkdir(parents=True, exist_ok=True)

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "Title",
        parent=styles["Title"],
        fontSize=16,
        textColor=colors.HexColor("#1a1a2e"),
        alignment=TA_CENTER,
        spaceAfter=6,
    )
    subtitle_style = ParagraphStyle(
        "Subtitle",
        parent=styles["Normal"],
        fontSize=9,
        textColor=colors.HexColor("#4a4a4a"),
        alignment=TA_CENTER,
        spaceAfter=12,
    )
    heading_style = ParagraphStyle(
        "Heading",
        parent=styles["Heading2"],
        fontSize=11,
        textColor=colors.HexColor("#16213e"),
        spaceBefore=10,
        spaceAfter=4,
    )
    body_style = ParagraphStyle(
        "Body",
        parent=styles["Normal"],
        fontSize=9.5,
        leading=13,
        spaceAfter=5,
    )
    prompt_style = ParagraphStyle(
        "Prompt",
        parent=body_style,
        fontSize=8.5,
        leading=12,
        leftIndent=12,
        rightIndent=8,
        spaceBefore=4,
        spaceAfter=8,
        backColor=colors.HexColor("#f4f4f8"),
        borderColor=colors.HexColor("#c5c5d0"),
        borderWidth=0.5,
        borderPadding=6,
    )
    prompt_label_style = ParagraphStyle(
        "PromptLabel",
        parent=body_style,
        fontSize=9,
        fontName="Helvetica-Bold",
        textColor=colors.HexColor("#16213e"),
        spaceBefore=6,
        spaceAfter=2,
    )

    doc = SimpleDocTemplate(
        str(out),
        pagesize=letter,
        rightMargin=0.65 * inch,
        leftMargin=0.65 * inch,
        topMargin=0.65 * inch,
        bottomMargin=0.65 * inch,
    )
    story: list = []

    story.append(Paragraph(f"{_para(actor.stage_name)} — Actor Profile", title_style))
    story.append(
        Paragraph(
            f"Profile date: {_para(actor.profile_date)} | Age: <b>{actor.age}</b>",
            subtitle_style,
        )
    )
    story.append(Spacer(1, 0.1 * inch))

    identity_rows = [
        ("Full legal name", actor.full_legal_name),
        ("Professional stage name", actor.professional_stage_name),
        ("Date of birth", actor.date_of_birth),
        ("Ethnicity", actor.ethnicity),
        ("Nationality", actor.nationality),
        ("Heritage", actor.heritage),
        ("Prompt prefix (required)", actor.prompt_prefix()),
    ]
    story.append(Paragraph("Identity", heading_style))
    for label, value in identity_rows:
        story.append(Paragraph(f"<b>{_para(label)}:</b> {_para(value)}", body_style))

    list_sections: list[tuple[str, str]] = [
        ("Languages", _bullet_list(actor.languages)),
        ("Physical description", _para(actor.base_physical_description)),
        ("Tattoo inventory", _para(actor.tattoo_inventory)),
        ("Signature looks", _para(actor.signature_looks)),
        ("Archetypes", _bullet_list(actor.archetypes)),
        ("Performance style", _para(actor.performance_style)),
        ("Voice notes", _para(actor.voice_notes)),
        ("On-screen comfort", _para(actor.on_screen_comfort)),
        ("Personality", _para(actor.personality)),
        ("Base reference images", _bullet_list(actor.base_reference_images)),
        ("Casting notes", _para(actor.casting_notes)),
    ]
    for heading, content in list_sections:
        story.append(Paragraph(heading, heading_style))
        story.append(Paragraph(content, body_style))

    story.append(Paragraph("Actor Generation Prompt", heading_style))
    story.append(
        Paragraph(
            "Copy-paste foundation prompt — age-led, built from physical description and "
            "visual continuity fields.",
            body_style,
        )
    )
    story.append(Paragraph("Foundation casting prompt", prompt_label_style))
    story.append(Paragraph(_para(actor.build_actor_generation_prompt()), prompt_style))

    wardrobe_prompts = actor.build_wardrobe_generation_prompts()
    if wardrobe_prompts:
        story.append(Paragraph("Wardrobe variant prompts", prompt_label_style))
        for label, prompt in wardrobe_prompts:
            story.append(Paragraph(f"<b>{_para(label)}</b>", body_style))
            story.append(Paragraph(_para(prompt), prompt_style))

    story.append(Paragraph("Compliance", heading_style))
    story.append(Paragraph(_para(COMPLIANCE_FOOTER), body_style))

    doc.build(story)
    return out.resolve()


def generate_actor_profile_markdown(
    actor: ActorProfile,
    output_path: str | Path | None = None,
) -> Path:
    out = Path(output_path) if output_path else DEFAULT_OUTPUT / actor.markdown_basename()
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(build_markdown(actor), encoding="utf-8")
    return out.resolve()


def generate_actor_profile(
    actor: ActorProfile,
    output_dir: Path | None = None,
    write_pdf: bool = True,
    write_md: bool = True,
) -> tuple[Path | None, Path | None]:
    """Generate markdown and/or PDF for an ActorProfile."""
    base = output_dir or DEFAULT_OUTPUT
    base.mkdir(parents=True, exist_ok=True)
    md_path = pdf_path = None
    if write_md:
        md_path = generate_actor_profile_markdown(actor, base / actor.markdown_basename())
    if write_pdf:
        pdf_path = generate_actor_profile_pdf(actor, base / actor.pdf_basename())
    return md_path, pdf_path


# --- Preset profiles (CLI / quick generation) ---

def _yuna_nakamura_wendy() -> ActorProfile:
    return ActorProfile(
        stage_name="Yuna Nakamura / Wendy",
        full_legal_name="Yuna Nakamura",
        professional_stage_name="Wendy",
        age=27,
        date_of_birth="[Month DD, YYYY]",
        ethnicity="Japanese-American",
        nationality="United States",
        heritage="Japanese (Tokyo-area family roots)",
        languages=[
            "Japanese (conversational)",
            "English (native fluency, West Coast neutral)",
        ],
        base_physical_description=(
            "5'6\", athletic-slim build, shoulder-length dark hair with subtle wave, "
            "expressive eyes, natural makeup baseline, wardrobe range from professional "
            "to noir evening wear."
        ),
        archetypes=[
            "Noir femme adjacent / controlled intelligence",
            "Professional lead under pressure",
            "Reaction-shot specialist",
        ],
        performance_style=(
            "Controlled intensity; micro-expression beats; stillness under pressure. "
            "Strong in reaction shots and power reversals."
        ),
        voice_notes="Measured cadence; warmth under restraint; sharpens under threat.",
        on_screen_comfort=(
            "Story-serving intimacy per Protocol v1.3; clinical language in prompts; "
            "PG-13 baseline unless canon explicitly escalates with compliance review."
        ),
        personality=(
            "Surface composure with emotional depth beneath; reads situations quickly; "
            "dry warmth in safe company; outsider poise in hostile rooms."
        ),
        base_reference_images=[
            "Tailored blazer + silk blouse (PI Story professional)",
            "Noir evening wear (act transitions)",
        ],
        tattoo_inventory="None — continuity: no tattoo additions without canon update.",
        signature_looks="Muted jewel tones, clean lines, practical heels, minimal jewelry.",
        casting_notes=(
            "Lead and co-lead drama; excels in PI Story universe; age must lead every prompt."
        ),
    )


def _blonde_olive_bikini() -> ActorProfile:
    return ActorProfile(
        stage_name="Blonde Olive Bikini (concept)",
        full_legal_name="[Concept reference — not cast]",
        professional_stage_name="Blonde Olive Bikini",
        age=22,
        date_of_birth="N/A (concept)",
        ethnicity="Northern European",
        nationality="N/A",
        heritage="N/A",
        languages=["English"],
        base_physical_description=(
            "Sun-kissed blonde hair, olive-toned bikini casting look, athletic build, "
            "neutral expression for turnaround plates."
        ),
        archetypes=["Casting reference model", "Beach / editorial staging"],
        performance_style="Reference model — consistency over performance variation.",
        voice_notes="N/A — visual reference only.",
        on_screen_comfort="PG-13 staging per Protocol v1.3; likeness lock via canonical casting v2.",
        personality="N/A — concept plate.",
        base_reference_images=[
            "CONCEPTS/BLONDE/CASTING/concept_blonde_olive_bikini_casting_v2.jpg",
            "CONCEPTS/BLONDE/CASTING/casting_turnaround_3view_olive_bikini_v1.jpg",
        ],
        tattoo_inventory="None in canonical casting.",
        signature_looks="Olive bikini, sun-kissed blonde, neutral casting expression.",
        casting_notes="Use image_edit from canonical casting; outfit/scene changes only.",
    )


PRESET_PROFILES: dict[str, ActorProfile] = {
    "yuna_nakamura_wendy": _yuna_nakamura_wendy(),
    "blonde_olive_bikini": _blonde_olive_bikini(),
}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="STUDIO Actor Profile Generator")
    parser.add_argument("--profile", choices=sorted(PRESET_PROFILES.keys()))
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--no-pdf", action="store_true")
    parser.add_argument("--no-md", action="store_true")
    parser.add_argument("--list", action="store_true")
    args = parser.parse_args(argv)

    if args.list:
        for key, actor in sorted(PRESET_PROFILES.items()):
            print(f"  {key}: {actor.stage_name} (age {actor.age})")
        return 0

    if not args.profile and not args.all:
        parser.error("Specify --profile <key> or --all (or --list)")

    targets = PRESET_PROFILES.items() if args.all else [(args.profile, PRESET_PROFILES[args.profile])]
    print(f"\nSTUDIO Actor Profile Generator\nOutput: {args.output_dir.resolve()}\n")

    for _key, actor in targets:
        md_path, pdf_path = generate_actor_profile(
            actor,
            args.output_dir,
            write_pdf=not args.no_pdf,
            write_md=not args.no_md,
        )
        print(f"✅ {actor.stage_name}")
        if md_path:
            print(f"   MD:  {md_path}")
        if pdf_path:
            print(f"   PDF: {pdf_path}")
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())