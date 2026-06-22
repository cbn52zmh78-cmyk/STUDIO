#!/usr/bin/env python3
"""ZhangYutongLang-001 — OG casting plate generator.

Generates the canonical identity reference for Zhang Yutong (张雨桐),
LANG_TUTOR_001 Mandarin tutor host for DAVID · The Archive.

Usage (run from any working dir on Benjamin's machine):
    python "STUDIO/Cast/Casting_Bible/lock_plates/gen_zhang_yutong_plate.py"

Outputs (all in same folder as this script):
    ZhangYutongLang-001_OG_v1.jpg   ← canonical OG (use this)
    ZhangYutongLang-001_OG_v2.jpg   ← variant 2
    ZhangYutongLang-001_OG_v3.jpg   ← variant 3
    ZhangYutongLang-001_OG_v4.jpg   ← variant 4
    ZhangYutongLang-001_3view.jpg   ← 3-panel turnaround (requires OG first)
    ZhangYutongLang-001_plates.json ← metadata sidecar

After script completes:
    1. Review v1–v4; rename best one to ZhangYutongLang-001_OG.jpg
    2. Run legal_gate.py (Gate 0 must be GREEN before scripting)
    3. Report back to hub
"""
from __future__ import annotations

import json
import os
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

# ── paths ────────────────────────────────────────────────────────────────────
HERE = Path(__file__).resolve().parent
LOCK_CARD = HERE.parent / "lock_cards" / "ZhangYutongLang-001.md"

# ── auth ─────────────────────────────────────────────────────────────────────

def _load_token() -> str:
    env = os.environ.get("XAI_API_KEY")
    if env:
        return env
    auth_path = Path.home() / ".grok" / "auth.json"
    if not auth_path.is_file():
        raise RuntimeError(
            "No XAI_API_KEY env var and no ~/.grok/auth.json found.\n"
            "Run: grok login   OR   set XAI_API_KEY=<your key>"
        )
    data = json.loads(auth_path.read_text(encoding="utf-8"))
    entry = next(iter(data.values()))
    token = entry.get("key") or entry.get("access_token")
    if not token:
        raise RuntimeError("~/.grok/auth.json found but contains no token key")
    return token


# ── download helper ───────────────────────────────────────────────────────────

def _download(url: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": "NEXUS-CastingPlate/1.0"})
    with urllib.request.urlopen(req, timeout=120) as r:
        dest.write_bytes(r.read())
    print(f"  saved → {dest.name}  ({dest.stat().st_size // 1024} KB)")


# ── prompts ───────────────────────────────────────────────────────────────────

OG_PLATE_PROMPT = """\
CONTINUITY LOCK @ZhangYutongLang-001 + @SET-LANG-BRIGHT-001 STYLE LOCK @STYLE-LANG-TUTOR-001

OG CASTING PLATE — Zhang Yutong (张雨桐) — ZhangYutongLang-001
PRIMARY IDENTITY REFERENCE — language tutor host, DAVID · The Archive

Portrait, chest-up, facing camera slightly angled (3/4 left), natural direct gaze into lens.

SUBJECT:
Chinese woman, age 27–29 [age_locked: 21+ mandatory], Han Chinese, educational tutor.
Face: oval "goose-egg" shape (鹅蛋脸) with softly tapered chin — natural, not angular or sharp.
Eyes: almond-shaped, double eyelids (双眼皮), warm dark brown irises, natural lashes.
Hair: long, straight, black — worn down naturally past shoulders, smooth and healthy.
Skin: natural warm-ivory to light-medium; healthy, clear, even tone. NOT chalky pale. \
NOT desaturated. Warm undertones.
Features: soft nose, natural mouth, gentle expression — approachable, composed, intelligent.
Build: slim; chest-up frame; relaxed natural posture, slight forward lean toward camera.
Expression: warm, professional, genuine — a teacher who is glad you are here. \
Slight natural smile, eyes engaged.

WARDROBE:
Simple solid-colour blouse — soft sage green or warm white. Clean neckline. \
No patterns. No distracting jewellery. Hair worn naturally down.

SET (@SET-LANG-BRIGHT-001):
Clean off-white or light warm-grey backdrop. Optional: very shallow suggestion of \
light wood desk edge at lower frame. Airy, spacious. No props. No clutter.

LIGHTING (@STYLE-LANG-TUTOR-001):
Natural daylight simulation. Neutral-warm white balance (~5500K). \
Soft diffused key light from camera-left. Gentle fill from right. \
No dramatic shadows. No warm amber. Bright and open — classroom feel, not bedroom feel.

TECHNICAL:
Photorealistic. 2:3 portrait preferred. High resolution. \
Soft depth of field (subject sharp, background gently defocused). \
Natural skin texture — no over-smoothing. No stylisation, no illustration.

NOT: ASMR aesthetic. NOT fashion model. NOT dramatic lighting. \
NOT pale/porcelain/chalky skin. NOT heavy makeup.

PROVENANCE NOTE (do not render in frame):
AI-generated · ZhangYutongLang-001 · OG plate · Upon Tyne Productions · 2026-06-21"""

TURNAROUND_PROMPT_TEMPLATE = """\
CONTINUITY LOCK @ZhangYutongLang-001 + @SET-LANG-BRIGHT-001 STYLE LOCK @STYLE-LANG-TUTOR-001

3-VIEW TURNAROUND — ZhangYutongLang-001
Reference: OG plate image attached.

Three-panel reference sheet. Same subject, same lighting, same wardrobe as OG plate.
Panel left: profile left (90°). Panel centre: front-facing (0°). Panel right: profile right (90°).
Head and shoulders, neutral expression, hair down.
Consistent skin tone, features, and lighting across all three panels.
Purpose: production reference for shot-to-shot consistency across all 5 lesson videos.

PROVENANCE NOTE:
AI-generated · ZhangYutongLang-001 · 3-view turnaround · Upon Tyne Productions · 2026-06-21"""


# ── main generation ───────────────────────────────────────────────────────────

def main() -> None:
    print("=" * 64)
    print("ZhangYutongLang-001 — OG Casting Plate Generator")
    print("DAVID · The Archive — Language Tutor lane")
    print("=" * 64)

    token = _load_token()
    print(f"[auth] token loaded (len={len(token)})")

    import xai_sdk  # noqa: PLC0415
    client = xai_sdk.Client(api_key=token)
    print("[sdk] xai_sdk.Client ready")

    results: list[dict] = []
    og_path: Path | None = None

    # ── OG plate — 4 variants ─────────────────────────────────────────────────
    print("\n[plate] Generating OG plate variants (4x)…")
    for v in range(1, 5):
        out = HERE / f"ZhangYutongLang-001_OG_v{v}.jpg"
        if out.exists() and out.stat().st_size > 5_000:
            print(f"  v{v}: already exists — skipping")
            if v == 1:
                og_path = out
            results.append({"variant": v, "path": str(out), "status": "reused"})
            continue

        print(f"  v{v}: requesting generation…")
        resp = client.image.sample(
            prompt=OG_PLATE_PROMPT,
            model="grok-imagine-image-quality",
        )
        _download(resp.url, out)
        if v == 1:
            og_path = out
        results.append({
            "variant": v,
            "path": str(out),
            "url": resp.url,
            "model": "grok-imagine-image-quality",
            "prompt": OG_PLATE_PROMPT,
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "status": "generated",
        })
        if v < 4:
            time.sleep(1.5)  # pace — xAI image rate limit

    # ── 3-view turnaround (using OG plate as reference) ───────────────────────
    tv_out = HERE / "ZhangYutongLang-001_3view.jpg"
    if tv_out.exists() and tv_out.stat().st_size > 5_000:
        print("\n[3view] already exists — skipping")
        results.append({"variant": "3view", "path": str(tv_out), "status": "reused"})
    elif og_path and og_path.exists():
        print("\n[3view] Generating 3-panel turnaround (OG as reference)…")
        try:
            # Upload OG as reference image if API supports it
            og_url = next(
                (r.get("url") for r in results if r.get("variant") == 1 and r.get("url")),
                None,
            )
            if og_url:
                resp3 = client.image.sample(
                    prompt=TURNAROUND_PROMPT_TEMPLATE,
                    model="grok-imagine-image-quality",
                    image_url=og_url,
                )
            else:
                resp3 = client.image.sample(
                    prompt=TURNAROUND_PROMPT_TEMPLATE,
                    model="grok-imagine-image-quality",
                )
            _download(resp3.url, tv_out)
            results.append({
                "variant": "3view",
                "path": str(tv_out),
                "url": resp3.url,
                "model": "grok-imagine-image-quality",
                "prompt": TURNAROUND_PROMPT_TEMPLATE,
                "generated_at": datetime.now(timezone.utc).isoformat(),
                "status": "generated",
            })
        except Exception as exc:
            print(f"  [3view] WARN: generation failed — {exc}")
            print("  [3view] Re-run manually after reviewing OG variants.")
    else:
        print("\n[3view] No OG plate available — skipping turnaround (run again after OG is saved)")

    # ── sidecar JSON ─────────────────────────────────────────────────────────
    sidecar = HERE / "ZhangYutongLang-001_plates.json"
    payload = {
        "actor_id": "ZhangYutongLang-001",
        "working_name": "Zhang Yutong (张雨桐)",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "plates": results,
        "canonical_og": "ZhangYutongLang-001_OG_v1.jpg",
        "next_steps": [
            "Review v1–v4; rename best to ZhangYutongLang-001_OG.jpg",
            "Run legal_gate.py — Gate 0 must be GREEN",
            "Update lock card plate status to APPROVED",
            "Open LANG_TUTOR_001 script drafting",
        ],
    }
    sidecar.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\n[meta] sidecar saved → {sidecar.name}")

    # ── summary ───────────────────────────────────────────────────────────────
    print("\n" + "=" * 64)
    print("DONE — review outputs in:")
    print(f"  {HERE}")
    print()
    print("Files generated:")
    for r in results:
        icon = "✅" if r.get("status") in ("generated", "reused") else "✗"
        label = r.get("variant", "?")
        print(f"  {icon} v{label}: {Path(r['path']).name}")
    print()
    print("NEXT:")
    print("  1. Inspect v1–v4 in Windows Explorer")
    print("  2. Rename best to: ZhangYutongLang-001_OG.jpg")
    print("  3. python DAVID/scripts/legal_gate.py  (Gate 0)")
    print("  4. Tell hub: 'OG plate approved' → hub opens script drafting")
    print("=" * 64)


if __name__ == "__main__":
    main()
