# Worked Example — Explainer Ad (§0 Quickstart)

**Status:** Executed 2026-06-19  
**Format:** `explainer-ad` (non-DAVID)  
**Talent:** `Julian-001` (Julian Cross, 31, plate_locked)  
**Set / Style:** `@Set-Seamless-Neutral-001` + `@Style-Cool-Clinical-001`  
**Purpose:** Prove `STUDIO_Master_Prompt_Bible_v1.0.md` §0 is followable without tribal knowledge.

---

## What we built

A 30-second fictional SaaS explainer (**FlowDesk**) with 6 presenter beats, composed `video_prompt`s, render-ready `imagine_pack.json`, and pre-render QA pass. Video generation was **not** run (no API spend); all steps through compose + validate are complete.

---

## Operator checklist (§0 mapped)

| Step | Bible §0 | Action taken | Artifact |
|------|----------|--------------|----------|
| 1 LEGAL GATE | §3.4 | Ran Gate 0 on brief; **YELLOW** (proceed; client clearance flag) | `Studio/Producers_Office/Legal_Gate/GATE_YELLOW_julian_flowdesk_explainer_v1_20260618_222013.json` |
| 2 CAST | §1 | Selected `Julian-001`; verified registry + lock card | `STUDIO/Cast/Casting_Bible/lock_cards/Julian-001.md` |
| 3 SET + STYLE | §7–§8 | Format defaults: Seamless Neutral + Cool Clinical | `Set_Library_v1.json`, `Style_Library_v1.json` |
| 4 FORMAT | §9 | Explicit `format_id: explainer-ad` in concept | `Production_Templates_v1.json` |
| 5 SCRIPT | §5 | `production_intake.py` → canonical script | `DAVID/scripts/longform_scripts/julian_flowdesk_explainer_v1_script.json` |
| 6 COMPOSE | §10 | Intake auto-composes every `video_prompt` (compose contract) | Same script — see shot `01_hook` |
| 7 GENERATE | §0 step 7 | **Skipped** (optional; needs `XAI_API_KEY`) | — |
| 8 QA | §0 step 8 | Registry build + pre-render `qa_check` | `qa_report_pre_render.json` (see QA section) |

---

## Step-by-step commands

Run from repo root: `C:\Users\NCG\Videos\Grok Projects`

### Step 1 — LEGAL GATE

Write a one-page brief (rating, channels, performer age, synthetic disclosure). **Do not write the word `minors`** in briefs — CARA guard false-positives on that substring (see Ambiguities).

```powershell
python artifacts/legal/legal_gate.py `
  --project julian_flowdesk_explainer_v1 `
  --file STUDIO/Pipeline/Concepts/julian_flowdesk_explainer_v1_brief.txt `
  --rating PG `
  --channels social,streaming,client
```

**Result:** YELLOW (exit 0). RED would be exit 2 — hard stop.

**Brief input:** `STUDIO/Pipeline/Concepts/julian_flowdesk_explainer_v1_brief.txt`

### Step 2 — CAST

1. Open registry or lock card; confirm:
   - `actor_id`: `Julian-001`
   - `age_locked`: **31** (≥ 21)
   - `reference_image_status`: `plate_locked`
   - `appearance_lock_status`: `LOCKED`

```powershell
python STUDIO/Cast/Scripts/build_casting_bible.py
```

**Result:** `age_compliant_21plus: 70/70` — registry QA pass.

**Plate path:** `STUDIO/Cast/actors_roster/male/north_america/Julian_Cross/01_casting_shots/casting_turnaround_v1.jpg`

**Identity mapping:** Format anchor is `@Presenter-001`; set `actor_id: Julian-001` in concept. Intake replaces anchor with roster continuity lock (`CONTINUITY LOCK @Julian-001: …`).

### Step 2b — OUTFIT (recommended before video)

Casting plate wardrobe is gym shorts + tank (§1.2). Commercial presenter needs §2 outfit plate:

```
change his outfit to navy blazer over light blue Oxford shirt, no tie, dark chinos, brown leather loafers
```

`image_edit` from casting plate → save as e.g. `presenter_commercial_plate.jpg` → set `avatar_reference` in concept. **This example skipped outfit plate** and used the casting plate directly to prove intake wiring; see Ambiguity #3.

### Step 3 — SET + STYLE

Omitted in concept → intake takes format defaults:

| ID | Name |
|----|------|
| `@Set-Seamless-Neutral-001` | Neutral grey seamless |
| `@Style-Cool-Clinical-001` | Cool clinical product grade |

Set reference plate: `STUDIO/Pipeline/references/seamless_neutral_grey_reference.jpg`

### Step 4–6 — FORMAT + SCRIPT + COMPOSE

Single command via intake flow (`STUDIO/Pipeline/INTAKE_FLOW.md`):

```powershell
python STUDIO/Pipeline/production_intake.py STUDIO/Pipeline/Concepts/julian_flowdesk_explainer_v1.concept.json
```

**Concept input:** `STUDIO/Pipeline/Concepts/julian_flowdesk_explainer_v1.concept.json`

**Emitted script highlights:**
- `format_id`: `explainer-ad`
- `config.use_identity_lock`: `false` (roster talent — not David lock)
- `config.avatar_reference`: Julian casting plate path
- `intake.actor_id`: `Julian-001`
- 6 shots, all with `speech_text` + lip-sync in `video_prompt`

**Sample composed prompt (truncated):**

```
CONTINUITY LOCK @Julian-001: identical 31-year-old White American male performer (Julian Cross)…
CONTINUITY LOCK @Set-Seamless-Neutral-001: identical neutral grey seamless…
STYLE LOCK @Style-Cool-Clinical-001: cool-clinical grade…
Presenter addresses camera directly, crisp opener, neutral backdrop. Camera: locked medium, snap attention.
… Lip-synced, delivers: "Still drowning in scattered notes?" Warm mid-Atlantic baritone… synthetic talent only.
Finish on presentational gesture peak…
```

### Step 7 — VALIDATE (pre-render; no API)

```powershell
$env:PYTHONIOENCODING = 'utf-8'
python DAVID/scripts/render_longform.py DAVID/scripts/longform_scripts/julian_flowdesk_explainer_v1_script.json --script-only
```

**Outputs:**
- `DAVID/productions/julian_flowdesk_explainer_v1_longform_v1/julian_flowdesk_explainer_v1_script.json` (normalized)
- `DAVID/productions/julian_flowdesk_explainer_v1_longform_v1/julian_flowdesk_explainer_v1_imagine_pack.json`

### Step 8 — QA

**A. Registry QA** — `build_casting_bible.py` (step 2).

**B. Pre-render script QA** (no video files yet):

```powershell
python -c "
import json, sys
from pathlib import Path
sys.path.insert(0, 'DAVID/scripts')
from render_longform import normalize_script, resolve_refs, qa_check
p = Path('DAVID/scripts/longform_scripts/julian_flowdesk_explainer_v1_script.json')
script = normalize_script(json.loads(p.read_text(encoding='utf-8')), p)
qa = qa_check(script, resolve_refs(script), [])
Path('DAVID/productions/julian_flowdesk_explainer_v1_longform_v1/qa_report_pre_render.json').write_text(json.dumps(qa, indent=2))
print('pass:', qa['pass'])
"
```

**Result:** `pass: true` — 6 shots ≥ min 4, synthetic guard on all prompts.

**C. Post-render QA** — `qa_report.json` is written only after full `render_longform.py` (with or without `--seamless`). Checks segment files on disk.

### Step 7 (optional) — GENERATE

```powershell
python DAVID/scripts/render_longform.py DAVID/scripts/longform_scripts/julian_flowdesk_explainer_v1_script.json --seamless --match-color --cut-on-motion
```

Requires `XAI_API_KEY`. Writes `output/*.mp4`, `qa_report.json`, `manifest.json`.

---

## Full artifact manifest

| Artifact | Path |
|----------|------|
| Brief | `STUDIO/Pipeline/Concepts/julian_flowdesk_explainer_v1_brief.txt` |
| Concept | `STUDIO/Pipeline/Concepts/julian_flowdesk_explainer_v1.concept.json` |
| Legal gate JSON | `Studio/Producers_Office/Legal_Gate/GATE_YELLOW_julian_flowdesk_explainer_v1_20260618_222013.json` |
| CARA report | `Studio/Producers_Office/Compliance_Reports/CARA_Compliance_Report_julian_flowdesk_explainer_v1_20260618_222013.txt` |
| Lock card | `STUDIO/Cast/Casting_Bible/lock_cards/Julian-001.md` |
| Casting plate | `STUDIO/Cast/actors_roster/male/north_america/Julian_Cross/01_casting_shots/casting_turnaround_v1.jpg` |
| Intake script (source) | `DAVID/scripts/longform_scripts/julian_flowdesk_explainer_v1_script.json` |
| Normalized script | `DAVID/productions/julian_flowdesk_explainer_v1_longform_v1/julian_flowdesk_explainer_v1_script.json` |
| Imagine pack | `DAVID/productions/julian_flowdesk_explainer_v1_longform_v1/julian_flowdesk_explainer_v1_imagine_pack.json` |
| Pre-render QA | `DAVID/productions/julian_flowdesk_explainer_v1_longform_v1/qa_report_pre_render.json` |

---

## Bible ambiguities found (patch list)

| # | Step | Ambiguity | Resolution / patch |
|---|------|-----------|-------------------|
| 1 | §0 / §11 | Quickstart pointed only to `production_templates.py`; intake path undocumented | **Patched:** §0 + §11 now reference `production_intake.py` + `INTAKE_FLOW.md` |
| 2 | §9 / CAST | `@Presenter-001` → roster `ActorID` mapping not explicit | **Patched:** §0 step 2 — set `actor_id` in concept; intake synthesizes `@ActorID` continuity lock |
| 3 | §1 / §2 | When to `image_edit` presenter wardrobe vs use casting plate as `avatar_reference` | **Patched:** §0 step 2b — outfit plate before video for non-casting wardrobe |
| 4 | §5 | `use_identity_lock: false` for roster talent not documented | **Patched:** §5.1 config table |
| 5 | §5.4 | Production output path only showed `productions/<slug>/` (DAVID-centric) | **Patched:** §5.4 — Editorial vs DAVID paths + `normalize_script` strips `format_id` |
| 6 | §3.4 / §11 | Legal Gate CLI missing | **Patched:** §3.4 + §11 command table |
| 7 | §0 step 8 | `qa_report.json` implied at script-only time | **Patched:** §0 — pre-render vs post-render QA split |
| 8 | LEGAL | Brief phrase "No minors" triggers CARA false RED | **Documented here;** avoid substring `minor` in gate briefs |
| 9 | CODE | `production_intake.py` omitted `presenter` from speaking roles (no lip-sync) | **Fixed** in `production_intake.py` — aligned with §10 speaking roles |

---

## Verdict

**Bible is followable** for a non-DAVID explainer-ad when the operator:

1. Uses `production_intake.py` (not manual template copy-paste)
2. Sets `actor_id` to a registry handle
3. Avoids `minor` in legal briefs
4. Runs `--script-only` before API spend
5. Generates presenter outfit plate before video (recommended; was the one manual gap)

Patches applied to `STUDIO_Master_Prompt_Bible_v1.0.md` (§0, §3.4, §5, §9.6, §11, §12).