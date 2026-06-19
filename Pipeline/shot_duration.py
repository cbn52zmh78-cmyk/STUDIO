"""Seamless shot duration policy — intake pre-clamp + render/QA single source (#177)."""

from __future__ import annotations

from typing import Any

SEAMLESS_LO = 7
SEAMLESS_HI = 9
AV_SYNC_TOLERANCE_S = 0.12


def clamp_shot_duration(
    duration: int | float,
    lo: int = SEAMLESS_LO,
    hi: int = SEAMLESS_HI,
) -> int:
    return max(lo, min(hi, int(duration)))


def seamless_chain_enabled(seamless_cfg: dict[str, Any] | None) -> bool:
    seam = seamless_cfg or {}
    return seam.get("primary") in ("extend", "extend_chain", True)


def should_clamp_shot_durations(seamless_cfg: dict[str, Any] | None) -> bool:
    """Intake + seamless render paths clamp blueprint durations into API band."""
    return seamless_chain_enabled(seamless_cfg)


def effective_shot_duration(shot: dict[str, Any], *, seamless: bool) -> int:
    """Duration render, pin, and QA should target (idempotent after intake clamp)."""
    d = int(shot.get("duration", 8))
    return clamp_shot_duration(d) if seamless else d


def apply_duration_clamp_to_shots(
    shots: list[dict[str, Any]],
    *,
    lo: int = SEAMLESS_LO,
    hi: int = SEAMLESS_HI,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Clamp shot durations and recompute contiguous t_start/t_end."""
    out: list[dict[str, Any]] = []
    t = 0
    changed = 0
    for shot in shots:
        s = dict(shot)
        raw = int(s.get("duration", 8))
        clamped = clamp_shot_duration(raw, lo, hi)
        if raw != clamped:
            s["duration_raw"] = raw
            changed += 1
        s["duration"] = clamped
        s["t_start"] = t
        s["t_end"] = t + clamped
        t += clamped
        out.append(s)
    return out, {"lo": lo, "hi": hi, "shots_clamped": changed}


def check_shot_duration_band(
    shot: dict[str, Any],
    *,
    seamless: bool,
    lo: int = SEAMLESS_LO,
    hi: int = SEAMLESS_HI,
) -> str | None:
    if not seamless:
        return None
    dur = int(shot.get("duration", 0))
    if dur < lo or dur > hi:
        return f"{shot['id']}: duration {dur}s outside {lo}–{hi}s seamless band"
    return None


def av_sync_drift_label(
    shot: dict[str, Any],
    video_duration: float,
    *,
    seamless: bool,
    tolerance_s: float = AV_SYNC_TOLERANCE_S,
) -> str | None:
    if not seamless:
        return None
    expected = float(effective_shot_duration(shot, seamless=True))
    delta = abs(video_duration - expected)
    if delta > tolerance_s:
        return f"{shot['id']}:{delta:.3f}s"
    return None