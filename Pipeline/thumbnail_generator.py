#!/usr/bin/env python3
"""STUDIO thumbnail spec generator — DAVID channel (Upon Tyne Productions / NEXUS).

Generates Grok Imagine prompts + metadata specs for YouTube thumbnails (1280×720).
Does NOT call any API or generate actual images. All outputs are prompt specs for
Benjamin's Grok terminal.

Usage:
    python thumbnail_generator.py --slate dead_languages   # 6 launch eps A+B (12 specs)
    python thumbnail_generator.py --episode david_latin_corpus_v1  # single ep A+B
    python thumbnail_generator.py --sample-lanes           # 3 lane samples A+B (6 specs)
    python thumbnail_generator.py --all                    # episodes + samples (18 specs)

Output files:
    STUDIO/Art_Department/Thumbnails/thumbnail_specs.json
    STUDIO/Art_Department/Thumbnails/THUMBNAIL_QUEUE.md

T2 Priority #140 — Weekend Dispatch Queue
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT         = Path(__file__).resolve().parents[2]
CONCEPTS_DIR = Path(__file__).resolve().parent / "Concepts"
THUMB_DIR    = ROOT / "STUDIO" / "Art_Department" / "Thumbnails"


# ── Episode data ──────────────────────────────────────────────────────────────
# Source: DEAD_LANGUAGE_SLATE_v1.md  (launch six, eps 1-6)

DEAD_LANGUAGES_LAUNCH: list[dict[str, Any]] = [
    {
        "slug":      "david_latin_corpus_v1",
        "title":     "Why Latin Never Really Died",
        "topic":     "Latin — the language that never left the lectern",
        "language":  "Latin",
        "era":       "Classical Rome — medieval continuity — present liturgy",
        "format_id": "documentary-host",
        "artifact_scene": (
            "close-up of weathered stone Latin inscription on crumbling Roman forum "
            "columns, golden hour raking light, fine dust in the air, rich ochre and "
            "shadow colour grade"
        ),
        "writing_bg": (
            "monumental Roman capitalis letters carved in pale travertine stone "
            "filling the background, dramatic side-lighting casting deep shadows "
            "in each letterform"
        ),
        "headline":  "WHY LATIN NEVER REALLY DIED",
        "subline":   "The Language That Refused to Die",
    },
    {
        "slug":      "david_ancient_greek_corpus_v1",
        "title":     "Restoring the Pitch Accent",
        "topic":     "Ancient Greek pitch accent — what Homer actually sounded like",
        "language":  "Ancient Greek",
        "era":       "Archaic and Classical Greece — Homeric oral tradition",
        "format_id": "documentary-host",
        "artifact_scene": (
            "ancient Greek papyrus scroll with pitch accent marks visible under "
            "dramatic raking library light, dark scholarly atmosphere, deep indigo "
            "and gold colour grade"
        ),
        "writing_bg": (
            "monumental ancient Greek uncial letters and diacritical pitch marks "
            "etched into stone, filling frame, deep teal and shadow tones"
        ),
        "headline":  "RESTORING THE PITCH ACCENT",
        "subline":   "What Homer Actually Sounded Like",
    },
    {
        "slug":      "david_old_english_corpus_v1",
        "title":     "Beowulf's Tongue in Manuscript",
        "topic":     "Old English — Beowulf manuscript and alliterative verse",
        "language":  "Old English",
        "era":       "Anglo-Saxon England, 700–1100 CE",
        "format_id": "documentary-host",
        "artifact_scene": (
            "extreme close-up of an illuminated Old English manuscript page, Beowulf "
            "ink script visible, candlelight warm glow, vellum texture, deep amber "
            "and black colour grade"
        ),
        "writing_bg": (
            "Old English insular script characters — angular runic-influenced letters — "
            "filling the background in charcoal on parchment texture, candlelit amber tones"
        ),
        "headline":  "BEOWULF'S TONGUE IN MANUSCRIPT",
        "subline":   "The Speech That Outlasted the Kingdoms",
    },
    {
        "slug":      "david_old_norse_corpus_v1",
        "title":     "Runes Attested, Sagas Reconstructed",
        "topic":     "Old Norse — runestones and Eddic poetry",
        "language":  "Old Norse",
        "era":       "Viking Age Scandinavia, 700–1100 CE",
        "format_id": "documentary-host",
        "artifact_scene": (
            "dramatic low-angle shot of a tall runestone in frozen Nordic landscape, "
            "runic inscriptions carved deep into stone, overcast arctic light, steel "
            "blue and silver colour grade"
        ),
        "writing_bg": (
            "Elder Futhark runic characters carved in relief across rough grey stone "
            "filling the background, cold blue-white dramatic lighting"
        ),
        "headline":  "RUNES ATTESTED, SAGAS RECONSTRUCTED",
        "subline":   "The Language Carved in Stone",
    },
    {
        "slug":      "david_gothic_corpus_v1",
        "title":     "A Language Saved by One Bible",
        "topic":     "Gothic — the Wulfila Bible as sole surviving corpus",
        "language":  "Gothic",
        "era":       "4th–6th century CE, Visigothic Europe",
        "format_id": "documentary-host",
        "artifact_scene": (
            "silver Codex Argenteus manuscript open under dramatic directional light, "
            "purple vellum with silver Gothic script glowing, deep royal purple and "
            "silver colour grade"
        ),
        "writing_bg": (
            "Gothic alphabet letters — angular Wulfila script — filling the background "
            "in silver on deep purple, illuminated manuscript aesthetic"
        ),
        "headline":  "A LANGUAGE SAVED BY ONE BIBLE",
        "subline":   "Gothic: Four Centuries in a Single Manuscript",
    },
    {
        "slug":      "david_sumerian_corpus_v1",
        "title":     "The First Written Language",
        "topic":     "Sumerian cuneiform — the earliest attested writing system",
        "language":  "Sumerian",
        "era":       "Mesopotamia, 3200–500 BCE",
        "format_id": "documentary-host",
        "artifact_scene": (
            "close-up of a Sumerian cuneiform clay tablet with reed impressions, "
            "dramatic raking side-light, ancient museum setting, warm clay and deep "
            "shadow colour grade"
        ),
        "writing_bg": (
            "dense cuneiform wedge-impressions covering clay tablet texture filling "
            "the background, warm terracotta and shadow tones, museum-quality dramatic lighting"
        ),
        "headline":  "THE FIRST WRITTEN LANGUAGE",
        "subline":   "Five Thousand Years in Clay",
    },
]

LANE_SAMPLES: list[dict[str, Any]] = [
    {
        "slug":      "lane_sample_david",
        "title":     "History Documentary Lane Sample",
        "topic":     "History documentary — DAVID Archive channel brand",
        "language":  "N/A (lane sample)",
        "era":       "Pan-historical",
        "format_id": "documentary-host",
        "artifact_scene": (
            "ancient archive room with towering shelves of scrolls and manuscripts, "
            "a single dramatic light beam cutting through dust, deep amber and shadow "
            "colour grade, cinematic depth of field"
        ),
        "writing_bg": (
            "layered text fragments from multiple ancient scripts — Latin, Greek, "
            "cuneiform — overlapping on aged parchment, warm amber tones"
        ),
        "headline":  "THE ARCHIVE",
        "subline":   "Dead Languages, Actually Pronounced",
    },
    {
        "slug":      "lane_sample_observatory",
        "title":     "Astrophysics / Space Lane Sample",
        "topic":     "Astrophysics and space science — observatory documentary style",
        "language":  "N/A (lane sample)",
        "era":       "Contemporary science",
        "format_id": "documentary-host",
        "artifact_scene": (
            "interior of a massive radio telescope dish at night, Milky Way visible "
            "overhead, cold blue and deep space black colour grade, long exposure "
            "star trails in background"
        ),
        "writing_bg": (
            "star field and nebula imagery — deep space blues and purples — filling "
            "the background with observable universe depth, galaxy spiral structures"
        ),
        "headline":  "WHAT THE TELESCOPE HEARS",
        "subline":   "At the Edge of Observable Space",
    },
    {
        "slug":      "lane_sample_science",
        "title":     "Science Explainer Lane Sample",
        "topic":     "Science explainer — clean educational documentary style",
        "language":  "N/A (lane sample)",
        "era":       "Contemporary science",
        "format_id": "documentary-host",
        "artifact_scene": (
            "dramatic close-up of a molecular model or scientific apparatus — glass "
            "beakers, crystalline structures — in a high-contrast laboratory setting, "
            "cool teal and white colour grade"
        ),
        "writing_bg": (
            "scientific diagram elements — atomic structures, formula notation, "
            "periodic table fragments — on deep navy blue background, "
            "clean high-contrast scientific aesthetic"
        ),
        "headline":  "THE SCIENCE BEHIND IT",
        "subline":   "Evidence-First Documentary",
    },
]

SLATES: dict[str, list[dict[str, Any]]] = {
    "dead_languages": DEAD_LANGUAGES_LAUNCH,
}

SYNTHETIC_GUARD = "Synthetic fictional host presenter. No real person depicted."

PROMPT_TEMPLATE_A = (
    "Photorealistic 16:9 thumbnail-style image, 1280x720 composition. {scene_description}. "
    "Dramatic cinematic lighting, deep rich color grade, sharp focus on center subject. "
    "Documentary channel thumbnail aesthetic — bold, striking, educational. "
    "No text. No watermarks. No logos."
)

PROMPT_TEMPLATE_B = (
    "Photorealistic 16:9 thumbnail-style image, 1280x720 composition. {scene_description}. "
    "Dramatic cinematic lighting, deep rich color grade, sharp focus on center subject. "
    "Documentary channel thumbnail aesthetic — bold, striking, educational. "
    "No text. No watermarks. No logos. {synthetic_guard}"
)


# ── Core spec builder ─────────────────────────────────────────────────────────

def generate_thumbnail_spec(episode: dict[str, Any], variant: str = "A") -> dict[str, Any]:
    """Generate a single thumbnail spec dict for the given episode and variant.

    Args:
        episode: Episode dict with keys: slug, title, topic, language, era,
                 format_id, artifact_scene, writing_bg, headline, subline.
        variant: "A" (artifact/environment) or "B" (host-forward).

    Returns:
        Thumbnail spec dict with grok_prompt, text_overlay, design_notes, etc.
    """
    slug    = episode["slug"]
    variant = variant.upper()
    assert variant in ("A", "B"), f"variant must be A or B, got {variant!r}"

    if variant == "A":
        scene = episode["artifact_scene"]
        grok_prompt = PROMPT_TEMPLATE_A.format(scene_description=scene)
        design_notes = (
            f"Variant A — artifact/environment focus. No host in frame. "
            f"Key visual: {episode['language']} artifact or inscription as hero element. "
            f"Era: {episode['era']}. "
            f"Compositing team adds text overlay in post. "
            f"Target feel: museum-quality, weighty, scholarly discovery."
        )
    else:
        scene = (
            f"DAVID documentary presenter (synthetic AI host, male, authoritative, "
            f"40s, clean professional appearance) looking directly into camera with "
            f"confident engaged expression, positioned left-of-centre, "
            f"{episode['writing_bg']} filling the right two-thirds of the background"
        )
        grok_prompt = PROMPT_TEMPLATE_B.format(
            scene_description=scene,
            synthetic_guard=SYNTHETIC_GUARD,
        )
        design_notes = (
            f"Variant B — host-forward. DAVID presenter faces camera, "
            f"{episode['language']} writing system as dramatic background element. "
            f"Host occupies left third, script/writing fills right two-thirds. "
            f"Match David-001 identity lock (same face across all episodes). "
            f"Compositing team adds text overlay in post. "
            f"Target feel: direct, authoritative, personal address to viewer."
        )

    text_overlay = {
        "headline":      episode["headline"],
        "subline":       episode["subline"],
        "channel_badge": "DAVID · The Archive",
        "font_style":    "bold_condensed_serif",
        "text_color":    "#FFFFFF",
        "shadow":        True,
    }

    return {
        "slug":         slug,
        "variant":      variant,
        "filename":     f"{slug}_thumb_{variant}.jpg",
        "dimensions":   "1280x720",
        "episode_title": episode["title"],
        "language":     episode["language"],
        "era":          episode["era"],
        "format_id":    episode["format_id"],
        "grok_prompt":  grok_prompt,
        "text_overlay": text_overlay,
        "design_notes": design_notes,
    }


# ── Output writers ────────────────────────────────────────────────────────────

def _generate_specs(episodes: list[dict[str, Any]]) -> list[dict[str, Any]]:
    specs: list[dict[str, Any]] = []
    for ep in episodes:
        specs.append(generate_thumbnail_spec(ep, "A"))
        specs.append(generate_thumbnail_spec(ep, "B"))
    return specs


def _write_json(specs: list[dict[str, Any]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(specs, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"  → wrote {path.relative_to(ROOT)} ({len(specs)} specs)")


def _write_queue_md(specs: list[dict[str, Any]], path: Path) -> None:
    """Write a human-readable THUMBNAIL_QUEUE.md with copy-paste-ready Grok prompts."""
    path.parent.mkdir(parents=True, exist_ok=True)

    # Group by slug
    by_slug: dict[str, list[dict[str, Any]]] = {}
    for s in specs:
        by_slug.setdefault(s["slug"], []).append(s)

    lines: list[str] = [
        "# THUMBNAIL QUEUE — DAVID · The Archive",
        "",
        "**Generated by:** `STUDIO/Pipeline/thumbnail_generator.py`  ",
        "**Format:** 1280×720 · Grok Imagine prompts · No API calls made here  ",
        "**Compositing:** Text overlays added in post — NOT in Grok prompt  ",
        "",
        "---",
        "",
        "## How to use",
        "",
        "1. Copy the **Grok Prompt** block for the variant you want",
        "2. Paste into your Grok Imagine terminal",
        "3. Save output as `<filename>` listed under each variant",
        "4. Hand to compositing team with the **Text Overlay** values",
        "",
        "---",
        "",
    ]

    ep_num = 0
    for slug, slug_specs in by_slug.items():
        # Detect if this is a lane sample
        is_lane = slug.startswith("lane_sample_")
        if not is_lane:
            ep_num += 1
            ep_label = f"Episode {ep_num}"
        else:
            ep_label = "Lane Sample"

        title = slug_specs[0]["episode_title"]
        lang  = slug_specs[0]["language"]
        era   = slug_specs[0]["era"]

        lines += [
            f"## {ep_label}: {title}",
            "",
            f"**Slug:** `{slug}`  ",
            f"**Language:** {lang}  ",
            f"**Era:** {era}  ",
            "",
        ]

        for spec in slug_specs:
            v = spec["variant"]
            focus = "Artifact / Environment focus (no host)" if v == "A" else "Host-forward (DAVID presenter)"
            lines += [
                f"### Variant {v} — {focus}",
                "",
                f"**Output filename:** `{spec['filename']}`  ",
                f"**Dimensions:** {spec['dimensions']}  ",
                "",
                "**Grok Prompt:**",
                "```",
                spec["grok_prompt"],
                "```",
                "",
                "**Text Overlay (compositing):**",
                f"- Headline: `{spec['text_overlay']['headline']}`",
                f"- Subline: `{spec['text_overlay']['subline']}`",
                f"- Channel badge: `{spec['text_overlay']['channel_badge']}`",
                f"- Font: `{spec['text_overlay']['font_style']}`",
                f"- Color: `{spec['text_overlay']['text_color']}` with shadow",
                "",
                "**Art Direction:**",
                f"> {spec['design_notes']}",
                "",
                "---",
                "",
            ]

    path.write_text("\n".join(lines), encoding="utf-8")
    print(f"  → wrote {path.relative_to(ROOT)}")


def _write_single_spec_json(spec: dict[str, Any], out_dir: Path) -> None:
    """Write individual <slug>_thumb_spec.json for batch_runner THUMB column."""
    slug = spec["slug"]
    path = out_dir / f"{slug}_thumb_spec.json"
    # Load existing or start fresh
    existing: list[dict] = []
    if path.is_file():
        try:
            existing = json.loads(path.read_text(encoding="utf-8"))
            if not isinstance(existing, list):
                existing = [existing]
        except Exception:
            existing = []
    # Replace or append
    existing = [s for s in existing if s.get("variant") != spec["variant"]]
    existing.append(spec)
    path.write_text(json.dumps(existing, indent=2, ensure_ascii=False), encoding="utf-8")


# ── CLI ───────────────────────────────────────────────────────────────────────

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="DAVID thumbnail spec generator — Grok prompts + metadata",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--slate", choices=list(SLATES),
        help="Generate specs for all launch episodes in a slate (A+B per episode)",
    )
    group.add_argument(
        "--episode", metavar="SLUG",
        help="Generate specs for a single episode slug (A+B variants)",
    )
    group.add_argument(
        "--sample-lanes", dest="sample_lanes", action="store_true",
        help="Generate specs for the 3 lane samples (A+B each)",
    )
    group.add_argument(
        "--all", dest="all_specs", action="store_true",
        help="Generate all 18 specs: 6 launch episodes + 3 lane samples (A+B each)",
    )
    args = parser.parse_args(argv)

    episodes_to_run: list[dict[str, Any]] = []
    samples_to_run:  list[dict[str, Any]] = []

    if args.slate:
        episodes_to_run = list(SLATES[args.slate])
        print(f"[thumbnail_generator] slate={args.slate}  episodes={len(episodes_to_run)}")
    elif args.episode:
        all_eps = [ep for slate in SLATES.values() for ep in slate]
        all_eps += LANE_SAMPLES
        matches = [e for e in all_eps if e["slug"] == args.episode]
        if not matches:
            print(
                f"[thumbnail_generator] ERROR: '{args.episode}' not found in any slate",
                file=sys.stderr,
            )
            return 1
        episodes_to_run = matches
        print(f"[thumbnail_generator] single episode={args.episode}")
    elif args.sample_lanes:
        samples_to_run = list(LANE_SAMPLES)
        print(f"[thumbnail_generator] generating {len(samples_to_run)} lane samples")
    elif args.all_specs:
        episodes_to_run = list(SLATES["dead_languages"])
        samples_to_run  = list(LANE_SAMPLES)
        print(
            f"[thumbnail_generator] --all: "
            f"{len(episodes_to_run)} episodes + {len(samples_to_run)} lane samples"
        )

    all_episodes = episodes_to_run + samples_to_run
    total_specs = len(all_episodes) * 2
    print(f"[thumbnail_generator] generating {total_specs} specs ({len(all_episodes)} episodes × A+B)")

    specs = _generate_specs(all_episodes)

    # Write combined JSON
    json_path = THUMB_DIR / "thumbnail_specs.json"
    _write_json(specs, json_path)

    # Write human-readable queue
    queue_path = THUMB_DIR / "THUMBNAIL_QUEUE.md"
    _write_queue_md(specs, queue_path)

    # Write per-slug spec files (for batch_runner THUMB column)
    for spec in specs:
        _write_single_spec_json(spec, THUMB_DIR)

    print(f"[thumbnail_generator] ✓ done — {total_specs} specs written to Art_Department/Thumbnails/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
