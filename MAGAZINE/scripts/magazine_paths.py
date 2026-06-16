"""Canonical paths — MAGAZINE lives under Studio/MAGAZINE/."""

from __future__ import annotations

from pathlib import Path

MAGAZINE_ROOT = Path(__file__).resolve().parent.parent
STUDIO_ROOT = MAGAZINE_ROOT.parent
EDITORIAL_MODELS = MAGAZINE_ROOT / "Editorial" / "Models"
CATALOG_DIR = MAGAZINE_ROOT / "_Catalog"
PIPELINE_DIR = STUDIO_ROOT / "Pipeline"
SHOT_LISTS_DIR = PIPELINE_DIR / "ShotLists"
VIDEO_PROMPTS_DIR = PIPELINE_DIR / "Video_Prompts"