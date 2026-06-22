# NEXUS AI Production Pipeline — Code Audit Report
**Date:** 2026-06-19 / 2026-06-20  
**Auditor:** Claude (automated sweep, no human override)  
**Scope:** All `.py` files under `Grok Projects/` (720 files total)  
**Commissioned by:** Upon Tyne Productions — weekend sweep while Benjamin is away

---

## Summary

| Category | Count | Status |
|---|---|---|
| Files compiled | 720 | ✓ |
| Compile failures (pre-fix) | 8 | All fixed |
| Truncated pipeline files | 5 | All completed |
| Other syntax/indentation errors | 3 | Fixed |
| verify_gate_0.py (pre-fix) | BLOCKED (null bytes) | — |
| verify_gate_0.py (post-fix) | **27/27 ALL PASS** | ✓ |

---

## Step 1 — Compile Check Results (Pre-Fix)

Eight files failed `python3 -m py_compile`:

| File | Error | Root Cause |
|---|---|---|
| `STUDIO/Pipeline/consume_ai_handoff.py` | `SyntaxError: '(' was never closed` (line 334) | File truncated mid-expression |
| `STUDIO/Pipeline/verify_gate_0.py` | `ValueError: source code string cannot contain null bytes` | ~1,259 null bytes appended to file |
| `AI/federation/science_integration.py` | `SyntaxError: '{' was never closed` (line 45) | File truncated mid-return dict |
| `Science/scripts/gather_groundtruth_solar_system.py` | `SyntaxError: f-string expression part cannot include a backslash` (line 389) | Backslash escape (`r'\[…\]'`) used inside f-string — illegal before Python 3.12 |
| `Stonebridge/examples/generate_compliance_checklist.py` | `SyntaxError: unterminated string literal` (line 7) | Bare CRLF newline inside a double-quoted string |
| `Stonebridge/examples/generate_sample_roster.py` | `IndentationError` (line 24) | `f.write(output)` had same indent as parent `with` statement |
| `Stonebridge/stonebridge.py` | `IndentationError` (line 35) | Entire file used 1-space indentation; nested blocks were at the same level |
| `artifacts/legal/legal_gate.py` | `SyntaxError: unterminated string literal` (line 603) | File truncated mid-string inside `save_report()` |

---

## Step 2 — Problem Pattern Grep

Patterns found **within pipeline-critical files**: none.

Non-critical hits (not in pipeline path):
- `Nexus/Labs/nexus_pgh_tax_calendar/fill_map.py` — 2× `TODO` comments (visual verification notes, not stubs)
- `Stonebridge/connectors/evidence_collector_sdk/verticals/{food_safety,real_estate,security}.py` — `raise NotImplementedError` (vertical SDK stubs; **NEEDS BENJAMIN** — out of pipeline scope)
- Various Stonebridge `Operations/Scripts/` files — `XXX` appears in NH RSA URL fragments as a placeholder chapter number in the state law URL scheme (not code stubs — these are real URLs where `XXX` is the chapter; **NEEDS BENJAMIN** to verify correct chapter numbers)
- `STUDIO/Pipeline/build_companion_proof.py` line 428 — `pass  #` (backward-compatible default; benign)
- `STUDIO/Pipeline/package_episode.py` line 492 — `pass  #` (fallback to `target_seconds` on probe failure; intentional)
- `STUDIO/Pipeline/production_intake.py` line 1250 — ellipsis stub body (out of weekend sweep scope)

---

## Step 3 — Specific Pipeline File Audit

### `batch_runner.py`
- ✓ `--package` flag correctly calls `package_episode.py` via `_load_package_module()` (exec/compile workaround — no sys.modules cache collision)
- ✓ `--thumbnails` flag correctly calls `thumbnail_generator.py` via `importlib.util`
- ✓ All 18 episodes present with correct slugs and tiers (launch 1–6, backlog 7–12, extension 13–18)
- ✗ **TRUNCATED** — `main()` body was entirely absent (file ended at `args = parser.parse_args(argv)`)
- **Fixed:** Completed `main()` with full episode iteration, table printing, package/thumbnail dispatch, and `if __name__` entry point

### `package_episode.py`
- ✓ `music_bed_id` present in kit dict (line 555: `intake.get("music_bed_id")`)
- ✓ `music_attribution` present in kit dict (line 556: `intake.get("music_attribution")`)
- ✓ `build_youtube_description()` includes mandatory AI disclosure paragraph ("AI-generated synthetic performers. No real persons depicted.")
- ✓ `build_thumbnail_brief()` has `channel_badge: "DAVID · The Archive"`
- ✗ **TRUNCATED** — `package_production()` ended at `.writ` (missing `write_text()` call and return)
- **Fixed:** Completed `write_text()` for `manifest.json`, added `return kit_manifest`, and added CLI `main()` + entry point

### `thumbnail_generator.py`
- ✓ `generate_thumbnail_spec()` is fully implemented and importable
- ✓ `--all` flag generates specs for 6 launch episodes + 3 lane samples × A+B = 18 specs
- ✓ `_write_single_spec_json()` present (used by `batch_runner._run_thumbnails()`)
- ✓ No truncation — file is complete

### `consume_ai_handoff.py`
- ✓ Gate 0 hard stop IS wired — raises `ValueError` on `blocked=True` or `verdict=="RED"` (lines 317–323)
- ✓ `legal_gate.py` loaded via `importlib.util.spec_from_file_location` resolving `ROOT_DIR / "artifacts" / "legal" / "legal_gate.py"`
- ✗ **TRUNCATED** — `consume_ai_handoff()` ended mid-expression at `duration_s = float(`
- **Fixed:** Completed duration resolution, shot-building via `_build_shots()`, config assembly, `intake` block with gate_0 fields, canonical `script.json` assembly, `write_text()`, and CLI `main()` + entry point

### `verify_gate_0.py`
- ✓ Logic fully intact after null-byte stripping
- ✗ **NULL BYTES** — ~1,259 null bytes appended to file (binary garbage after final `sys.exit(main())`)
- **Fixed:** Stripped null bytes in-place; file reduced from 16,089 → 14,830 bytes; compiles and runs

### `artifacts/legal/legal_gate.py`
- ✓ `SECTION_2257_STATEMENT` constant present with correct 18 U.S.C. § 2257 language
- ✓ `get_2257_statement()` helper present
- ✓ `GateResult.section_2257: str` field present in dataclass
- ✓ `row_music_clearance` present in `_evaluate_checklist_domains()`
- ✓ `row_2257_compliance` present in `_evaluate_checklist_domains()`
- ✗ **TRUNCATED** — `save_report()` ended mid-string inside the checklist domains iteration
- **Fixed:** Completed the `for key in (...)` tuple with all 8 domain keys, finished the markdown write, and added CLI `main()` + entry point

### `AI/federation/science_integration.py`
- ✗ **TRUNCATED** — `load_science_context()` ended at `"gate_status": p` mid-return dict
- **Fixed:** Completed `"gate_status": packet.gate_status,` and closing `}`

### `AI/Federations/` Python files
- All federation `.py` files in `AI/federation/` compile cleanly (post-fix)
- No `NotImplementedError` stubs in federation files
- `historical_figure_gate.py`, `music_clearance.py`, `science_gate.py` — all compile OK

---

## Step 4 — Cross-File Reference Check

| Reference | Status |
|---|---|
| `batch_runner.py` → `package_episode.py` (import) | ✓ Uses `exec(compile(...))` workaround — sys.modules cache bypassed correctly |
| `batch_runner.py` → `thumbnail_generator.py` (import) | ✓ Uses `importlib.util.spec_from_file_location` |
| `consume_ai_handoff.py` → `legal_gate.py` | ✓ `importlib.util` load from `ROOT_DIR / "artifacts" / "legal" / "legal_gate.py"` — path resolves correctly |
| `legal_gate.py` → `lib.bootstrap`, `lib.studio_paths` | ✓ Both exist at `artifacts/lib/`; `bootstrap.py` adds `artifacts/` subtrees to `sys.path` |
| `legal_gate.py` → `historical_figure_gate`, `music_clearance`, `science_gate` | ✓ All present in `artifacts/legal/`; all compile cleanly |
| `package_episode.py` imports (`argparse`, `json`, `re`, `shutil`, `subprocess`, `sys`, `datetime`, `pathlib`) | ✓ All stdlib — no missing dependencies |

---

## Step 5 — Fixes Applied

| # | File | Fix |
|---|---|---|
| 1 | `STUDIO/Pipeline/verify_gate_0.py` | Stripped 1,259 null bytes — file now 14,830 bytes, compiles OK |
| 2 | `Science/scripts/gather_groundtruth_solar_system.py` | Extracted f-string backslash expression to concatenation: `"..." + re.sub(r'\[...\]', '', orb).strip() + "..."` |
| 3 | `Stonebridge/examples/generate_compliance_checklist.py` | Replaced bare CRLF inside string literal with `\n` escape |
| 4 | `Stonebridge/examples/generate_sample_roster.py` | Added one additional space of indent to `f.write(output)` to place it inside the `with` block |
| 5 | `Stonebridge/stonebridge.py` | Rewrote with consistent 4-space indentation throughout |
| 6 | `artifacts/legal/legal_gate.py` | Completed truncated `save_report()`: full checklist domain iteration (8 keys), markdown write, CLI `main()` |
| 7 | `AI/federation/science_integration.py` | Completed truncated `load_science_context()` return dict: `"gate_status": packet.gate_status,` + closing `}` |
| 8 | `STUDIO/Pipeline/consume_ai_handoff.py` | Completed truncated `consume_ai_handoff()`: duration resolution, shot-building, config, intake block, script.json assembly + write, CLI `main()` |
| 9 | `STUDIO/Pipeline/package_episode.py` | Completed truncated `package_production()`: `manifest.json` write + return, CLI `main()` |
| 10 | `STUDIO/Pipeline/batch_runner.py` | Completed truncated `main()`: episode iteration, status table, package/thumbnail dispatch, exit code logic, `if __name__` entry point |

---

## Needs Benjamin

The following require decisions, credentials, or content that cannot be inferred from code context:

1. **Stonebridge `Operations/Scripts/` — NH RSA `XXX` URL chapter numbers** (`state_regulatory_urls.py`, `harvest_groundtruth_r1b_construction_trades_gaps.py`, `regulatory_research_scraper.py`, `run_t5_food_re_nz.py`, and archive scripts): Multiple URLs use `/XXX/` as a placeholder RSA chapter number. These are real NH General Court URLs where `XXX` must be the correct chapter number (e.g. 331-A, 319-C). Verify the correct chapter numbers and replace `XXX` with the real value.

2. **Stonebridge SDK vertical stubs** (`connectors/evidence_collector_sdk/verticals/food_safety.py`, `real_estate.py`, `security.py`): All three raise `NotImplementedError` — these need actual implementation or a decision to leave as abstract base.

3. **`production_intake.py` line 1250 — ellipsis stub**: One function has `...` as its body. Needs content decision.

4. **Music bed IDs** (`kit["music_bed_id"]`, `kit["music_attribution"]`): Both fields are present in the upload kit but will be `null` until clearance is assigned. Stamp via `intake.music_bed_id` in each `script.json` per `Music_Bed_Manifest.json` after clearance is complete.

5. **`Nexus/Labs/nexus_pgh_tax_calendar/fill_map.py`** — two `TODO` comments: one asks for visual confirmation of PDF field order (Text6–Text29), one for a visual pass on page 2 exemption labels. Requires Benjamin to open the actual ET-2025 PDF in Acrobat.

6. **Remaining 17 DAVID episodes** (eps 2–18): no MP4s present — render pipeline must be run to move episodes from `READY_TO_RENDER` to `READY_TO_PACKAGE`. Ep 1 (`david_latin_corpus_v1`) has a kit and is `PACKAGED`.

7. **magazine_casting_registry.json was valid JSON** at audit time — the hardcoded warning string in `verify_gate_0.py` (line 270) referencing "JSONDecodeError at line 394 col 24" is a stale in-code message from a previous broken state. No action needed unless the JSON breaks again.

---

## Step 6 — verify_gate_0.py Final Output

```
Gate 0 Channel Launch — Verification Report
============================================================
[PASS] § 2257 statement constant (SECTION_2257_STATEMENT) in legal_gate.py
[PASS] get_2257_statement() helper in legal_gate.py
[PASS] GateResult.section_2257 field present in legal_gate.py
[PASS] Gate 0 hard stop (raise ValueError on RED) in consume_ai_handoff.py
[PASS] Age_Policy_Locked.md exists (STUDIO/research/Age_Policy_Locked.md)
[PASS] REROLL_QUEUE.md — file exists and actor IDs parseable
[PASS] magazine_casting_registry.json — valid JSON
[PASS] Reroll actor ValentinaRossiMag-001: agency_status = do_not_cast_pending_reroll
[PASS] Reroll actor ZaraKhanMag-001: agency_status = do_not_cast_pending_reroll
[PASS] Reroll actor LioraVossMag-001: agency_status = do_not_cast_pending_reroll
[PASS] Reroll actor SofiaAlvarezMag-001: agency_status = do_not_cast_pending_reroll
[PASS] Reroll actor NadiaOkoroMag-001: agency_status = do_not_cast_pending_reroll
[PASS] channel_identity.json — file exists and is valid JSON
[PASS] channel_identity.json: 'company' non-empty
[PASS] channel_identity.json: 'channel_name' non-empty
[PASS] channel_identity.json: 'channel_badge' non-empty
[PASS] channel_identity.json: 'ai_disclosure' non-empty
[PASS] channel_identity.json: 'section_2257' non-empty
[PASS] Upload kit(s) found in DAVID/productions
[PASS] upload_kit david_latin_corpus_v1_upload_kit.json: 'youtube_title' present and non-empty
[PASS] upload_kit david_latin_corpus_v1_upload_kit.json: 'youtube_description' present and non-empty
[PASS] upload_kit david_latin_corpus_v1_upload_kit.json: 'chapters' present and non-empty
[PASS] upload_kit david_latin_corpus_v1_upload_kit.json: 'youtube_tags' present and non-empty
[PASS] upload_kit david_latin_corpus_v1_upload_kit.json: 'ai_disclosure_card' present and non-empty
[PASS] upload_kit david_latin_corpus_v1_upload_kit.json: 'section_2257_note' present and non-empty
[PASS] upload_kit david_latin_corpus_v1_upload_kit.json: youtube_description contains AI/synthetic disclosure
[PASS] thumbnail_specs.json has >= 12 specs
============================================================
Result: 27/27 checks passed. ALL PASS.
```

---

*Generated by automated audit sweep · Upon Tyne Productions / NEXUS AI · 2026-06-19*
