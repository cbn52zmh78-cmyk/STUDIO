#!/usr/bin/env python3
"""Channel Export — bundle upload kits from a batch into one ready-to-upload folder.

Reads a manifest_package.json (output of `batch_runner.py package`) and assembles
a single `channel_export/` directory that contains all upload-ready episode kits
plus a batch-level upload index.

Usage:
    python STUDIO/Pipeline/channel_export.py DAVID/batches/<id>/manifest_package.json
    python STUDIO/Pipeline/channel_export.py DAVID/batches/<id>/manifest_package.json --out my_export
"""
from __future__ import annotations

import argparse
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _sanitize(s: str) -> str:
    """Safe directory name from slug."""
    return "".join(c if (c.isalnum() or c in "_-") else "_" for c in s)


def build_channel_export(
    pkg_manifest_path: Path,
    *,
    out_dir: Path | None = None,
    overwrite: bool = False,
) -> dict[str, Any]:
    """Assemble channel export bundle from a package manifest.

    Returns a summary dict with the export path and per-episode status.
    """
    if not pkg_manifest_path.is_file():
        raise FileNotFoundError(f"Package manifest not found: {pkg_manifest_path}")

    pkg_manifest = json.loads(pkg_manifest_path.read_text(encoding="utf-8"))
    batch_id = pkg_manifest.get("batch_id", pkg_manifest_path.parent.name)
    items = pkg_manifest.get("items", [])

    if out_dir is None:
        out_dir = pkg_manifest_path.parent / "channel_export"

    if out_dir.exists():
        if overwrite:
            shutil.rmtree(out_dir)
        else:
            raise FileExistsError(
                f"Export dir already exists: {out_dir}. Use --overwrite to replace."
            )
    out_dir.mkdir(parents=True)

    episodes: list[dict[str, Any]] = []
    for item in items:
        slug = item.get("slug", "unknown")
        status = item.get("status", "?")
        upload_kit_path = item.get("upload_kit")

        if status != "ok" or not upload_kit_path:
            print(f"  - {slug}: status={status} → skipped")
            episodes.append({"slug": slug, "status": status, "exported": False})
            continue

        kit_src = Path(upload_kit_path)
        if not kit_src.is_dir():
            print(f"  ✗ {slug}: upload_kit dir not found ({kit_src})")
            episodes.append({"slug": slug, "status": "missing_kit", "exported": False})
            continue

        ep_dir = out_dir / _sanitize(slug)
        shutil.copytree(kit_src, ep_dir)
        print(f"  ✅ {slug}: → {ep_dir.name}/")
        episodes.append({
            "slug": slug,
            "status": "exported",
            "exported": True,
            "export_dir": str(ep_dir.relative_to(ROOT)).replace("\\", "/"),
        })

    # Build batch upload index
    index_rows: list[str] = [
        "# Channel Upload Index",
        f"",
        f"Batch: {batch_id}",
        f"Exported: {_utc_now()}",
        f"Episodes: {sum(1 for e in episodes if e['exported'])} / {len(episodes)}",
        "",
        "| # | Slug | Dir | Title | Duration |",
        "|---|------|-----|-------|----------|",
    ]
    for i, ep in enumerate(episodes, 1):
        if not ep["exported"]:
            index_rows.append(f"| {i} | {ep['slug']} | — | *skipped ({ep['status']})* | — |")
            continue
        ep_dir = out_dir / _sanitize(ep["slug"])
        seo_path = ep_dir / "seo" / "seo.json"
        kit_path = ep_dir / "manifest.json"
        title = ep["slug"]
        duration = "?"
        try:
            seo = json.loads(seo_path.read_text(encoding="utf-8"))
            title = seo.get("title", title)
        except Exception:
            pass
        try:
            kit_manifest = json.loads(kit_path.read_text(encoding="utf-8"))
            dur_s = kit_manifest.get("video_duration_s", 0)
            m, s = divmod(int(dur_s), 60)
            duration = f"{m}:{s:02d}"
        except Exception:
            pass
        index_rows.append(f"| {i} | `{ep['slug']}` | `{_sanitize(ep['slug'])}/` | {title} | {duration} |")

    (out_dir / "UPLOAD_INDEX.md").write_text("\n".join(index_rows) + "\n", encoding="utf-8")

    # Operator checklist
    checklist_lines = [
        "# Channel Export — Upload Checklist",
        "",
        "Work through each episode folder in order:",
        "",
    ]
    for i, ep in enumerate(episodes, 1):
        if not ep["exported"]:
            checklist_lines.append(f"- [ ] {ep['slug']} *(skipped — {ep['status']})*")
            continue
        ep_dir_name = _sanitize(ep["slug"])
        checklist_lines += [
            f"### {i}. {ep['slug']}",
            f"  - [ ] Review `{ep_dir_name}/seo/title.txt` and `description.txt`",
            f"  - [ ] Finalize thumbnail from `{ep_dir_name}/thumbnail/THUMBNAIL_BRIEF.json`",
            f"  - [ ] Upload `{ep_dir_name}/video/*.mp4` to YouTube Studio",
            f"  - [ ] Paste description (chapters pre-embedded)",
            f"  - [ ] Configure end screen per `{ep_dir_name}/end_screen/end_screen.json`",
            f"  - [ ] Set playlist, category, language per seo.json",
            f"  - [ ] Confirm AI disclosure line visible in description",
            f"  - [ ] Publish (or schedule)",
            "",
        ]
    (out_dir / "UPLOAD_CHECKLIST.md").write_text("\n".join(checklist_lines) + "\n", encoding="utf-8")

    # Export manifest
    export_manifest = {
        "batch_id": batch_id,
        "phase": "channel_export",
        "generated_at": _utc_now(),
        "source_manifest": str(pkg_manifest_path.relative_to(ROOT)).replace("\\", "/"),
        "export_dir": str(out_dir.relative_to(ROOT)).replace("\\", "/"),
        "episodes": episodes,
        "summary": {
            "total": len(episodes),
            "exported": sum(1 for e in episodes if e["exported"]),
            "skipped": sum(1 for e in episodes if not e["exported"]),
        },
    }
    (out_dir / "export_manifest.json").write_text(
        json.dumps(export_manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )

    print(f"\n[channel_export] → {out_dir}")
    print(f"[channel_export] summary: {export_manifest['summary']}")
    return export_manifest


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Bundle upload kits from a batch into one channel export folder"
    )
    parser.add_argument("manifest", type=Path, help="Path to manifest_package.json")
    parser.add_argument("--out", type=Path, default=None, help="Output dir (default: <batch>/channel_export)")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing export dir")
    args = parser.parse_args(argv)

    manifest_path = Path(args.manifest)
    if not manifest_path.is_absolute():
        manifest_path = (ROOT / manifest_path).resolve()

    result = build_channel_export(manifest_path, out_dir=args.out, overwrite=args.overwrite)
    return 0 if result["summary"]["exported"] > 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
