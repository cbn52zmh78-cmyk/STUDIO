# STUDIO Anime Style Bibles — §9 Corrected Extracts
**Version:** v1.1 Corrected  
**Date:** June 17, 2026  
**Scope:** §9 CLI & Automation Toolkit sections only — extracted from living STUDIO Grok project bibles

---

## Files

| File | Bible | Year | Director |
|------|-------|------|----------|
| `Anime_Bible_01_§9_Corrected.md` | Belladonna of Sadness | 1973 | Eiichi Yamamoto |
| `Anime_Bible_02_§9_Corrected.md` | Angel's Egg | 1985 | Yoshiyuki Oshii + Yoshitaka Amano |
| `Anime_Bible_03_§9_Corrected.md` | Serial Experiments Lain | 1998 | Yoshitoshi Abe |
| `Anime_Bible_04_§9_Corrected.md` | Texhnolyze | 2003 | Madhouse |
| `Anime_Bible_05_§9_Corrected.md` | Mind Game | 2004 | Masaaki Yuasa |

---

## What Changed in v1.1 Correction

The original §9 sections (v1.1 initial) contained speculative CLI commands that do not exist:
- `grok video generate` — does not exist
- `grok image generate` — does not exist
- `grok batch run` — does not exist
- Flags: `--style`, `--duration` (CLI), `--seed` (CLI), `--parallel`, `--compare`, `--iterate` — do not exist

**Grok Build is a coding/agent CLI, not a media generation CLI.**

Corrected §9 uses only confirmed real syntax:
- `grok -p "..."` — headless one-shot
- `grok` — interactive TUI with Plan Mode + `/fork`
- `client.video.generate(...)` — xAI Python SDK (singular, canonical)
- Agent-delegated script generation via natural language prompt

---

## SDK Note

`client.video.generate` (singular `.video`) is confirmed canonical per official xAI SDK docs as of June 2026.  
Model: `"grok-imagine-video"` (confirm latest model string against xAI docs before production runs).

---

## SPIT Cross-Reference

- **Bible 03 (Lain)** — suburban void / digital alienation — SPIT Act II alignment
- **Bible 04 (Texhnolyze)** — concrete noir / industrial brutalism — **confirmed SPIT Act II match**
- Priority hybrid test: Lain × Texhnolyze blend for SPIT Act II reference render
