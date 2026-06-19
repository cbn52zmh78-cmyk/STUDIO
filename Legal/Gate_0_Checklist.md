# Gate 0 — Legal Compliance Checklist v1.1

**Status:** Production canon. Non-negotiable.  
**Applies to:** Every scene, video, prompt pack, client brief, and deliverable intent — before generation, shoot, or client promise.  
**Feeds:** `Producers_Office/Pre_Publish_Gate.md` — **Gate 0 GREEN is a hard prerequisite** for Pre-Publish rows 1, 3, and 6.

---

## Required inputs (declare before review)

- [ ] **Project / slate ID** (`Producers_Office/SLATE/slate.json`)
- [ ] **Target rating** — G · PG · PG-13 · R (CARA ceiling; NC-17 = RED)
- [ ] **Distribution channel(s)** — `social` · `streaming` · `theatrical` · `festival` · `client`
- [ ] **Brief text, prompt, script excerpt, or shot list** (source of truth for gate)
- [ ] **Cast list** — `actor_id`(s) from Casting Bible if performers appear
- [ ] **Music plan** — temp track / licensed / original / none

## Gate CLI (run first)

```powershell
python artifacts/legal/legal_gate.py ^
  --project "henry_ii_council" ^
  --rating PG-13 ^
  --channels social,streaming,theatrical ^
  --text "your scene brief or prompt"
```

Machine verdict JSON → `Producers_Office/Legal_Gate/` · human-readable → `Legal/Gate_Reports/`

---

## Gate 0 Checklist

Complete every row before signing **GREEN**. **Any unchecked or FAIL → not GREEN.**

| # | Domain | Requirement | Verify | PASS |
|---|--------|-------------|--------|:----:|
| 1 | **Synthetic-actor consent / ownership** | All on-screen performers are **STUDIO-owned synthetic characters** from Casting Bible registries (`synthetic: true`). Upon Tyne Productions holds creation rights; no third-party performer likeness license required for synthetic-only cast. Cast `actor_id`(s) logged. Talent at `agency_ready` before hero/client delivery (`Talent_Agency/AGENCY_CHARTER.md`). | Casting Bible registries · talent status · `Legal/Talent_Replica/CHARTER.md` | ☐ |
| 2 | **Music / sync rights** | Every audible track is **cleared or replaced** before release intent: sync license (composition/publishing) + master use (recording) where applicable. Temp music flagged; cue sheet path declared. Uncleared chart/licensed music on client deliverable = **RED**. | `Legal/Music_Clearance/CHARTER.md` · `Music_Sound/Cue_Sheets/` | ☐ |
| 3 | **No-real-likeness sign-off** | **No real-person or celebrity likeness** in face, body, voice, or deceptively similar naming. `real_person_likeness: false` on all cast. Living-person likeness, deepfake, or replica prompts → **COUNSEL minimum**; non-consensual = **RED**. | Casting Bible lock cards · `Legal/AI_Content/CHARTER.md` · `Canons/Real_World_Reference_Policy_v1.md` | ☐ |
| 4 | **Target-channel legality** | Declared `--channels` reviewed against **Mass Dissemination** rules: platform ToS, CARA/rating ceiling, broadcast/festival/client contract surface, E&O exposure. Social-only still gates like theatrical. Channel flags from `legal_gate.py` resolved or logged. | `Legal/Mass_Dissemination/CHARTER.md` · Gate JSON `distribution_flags` | ☐ |
| 5 | **2257-style age documentation** | Every performer in the deliverable has **numerical age 21+** documented in: (a) Casting Bible `age_locked` + lock card, (b) production prompt prose (`[age]-year-old [ethnicity] [gender]` per `prompts/MASTER_JSON_Prompt_Template_ACTIVE.json` → `compliance_2257`), (c) Cast Compliance Audit (#110) not **BLOCKED**. Floor-age 21–22 entries require visual adult review before ship. | `Research/Age_Policy_Locked.md` · `Cast/Casting_Bible/audit/compliance_matrix.md` · `python STUDIO/Cast/Scripts/audit_cast_compliance.py` | ☐ |
| 6 | **AI-disclosure obligation** | **Plan** for synthetic-performer / AI-generated disclosure on every declared channel (in-video label, credits, description, platform metadata). Obligation logged at Gate 0; **presence verified** at Pre-Publish row 3. | `Legal/AI_Content/CHARTER.md` · per-channel ToS in Mass Dissemination charter | ☐ |

### Dual-stack machine review (automated via `legal_gate.py` v1.2)

Machine output includes `checklist_domains` (row_1 … row_6) aligned to the table above. Validation harness: `artifacts/legal/test_gate_v11.py`.

| Stack | Question |
|-------|----------|
| **AI Content** | Replica consent? Deepfake? NCIM? Minors? Synthetic performer rights? |
| **Mass Dissemination** | CARA ceiling? Platform AI label? Festival packet? E&O? |
| **Talent Replica** | `agency_ready` for hero/client delivery? |

---

## Verdict scale

| Verdict | Meaning | Pre-Publish Gate |
|---------|---------|------------------|
| **GREEN** | All checklist rows PASS · machine gate clear of hard stops | **Prerequisite met** — may proceed to production and later Pre-Publish |
| **YELLOW** | Warnings or distribution flags — mitigations documented | **Blocked** until re-gated **GREEN** |
| **COUNSEL** | Counsel flags — entertainment lawyer before spend | **Blocked** until counsel sign-off + re-gate **GREEN** |
| **RED** | Hard stop — federal/canon violation, NC-17 target, uncleared music on client deliverable, minors, explicit adult industry | **Blocked** — kill; no generate, shoot, or publish |

---

## After GREEN only

1. Log verdict on call sheet (`Producers_Office/Call_Sheets/`)
2. Archive Gate JSON in `Producers_Office/Legal_Gate/` and MD in `Legal/Gate_Reports/`
3. Run talent sync if new cast (`python artifacts/talent/performance_study_manager.py sync`)
4. Generate prompts / video
5. CARA report archived in `Producers_Office/Compliance_Reports/` when applicable
6. On final master → run **`Producers_Office/Pre_Publish_Gate.md`** (Gate 0 GREEN required)

---

## Producer Sign-Off — Gate 0

```
GATE 0 LEGAL — GREEN / RED

Project / Slate ID: _______________________________
Target rating:      _______________________________
Channel(s):         _______________________________
Gate report file:   _______________________________  (Legal_Gate/GATE_*.json)

Checklist rows 1–6:  ALL PASS ☐   FAIL ☐
Machine verdict:     GREEN ☐   YELLOW ☐   COUNSEL ☐   RED ☐

GREEN certification (check all if GREEN):
  ☐ Synthetic cast ownership confirmed — Upon Tyne / Casting Bible
  ☐ Music/sync rights cleared or temp-only with replacement plan
  ☐ No-real-likeness sign-off — synthetic-only, no celebrity/deepfake likeness
  ☐ Target-channel legality reviewed for declared channels
  ☐ 2257-style age doc — all performers 21+, audit not BLOCKED
  ☐ AI-disclosure obligation planned for declared channels

RED / HOLD reason (if not GREEN): _______________________________________________

Producer: _________________________   Date: __________   Verdict: GREEN / RED
```

**Only GREEN clears the path to Pre-Publish Gate.** RED halts all downstream work.

---

## Cross-References

| Canon | Path |
|-------|------|
| Pre-Publish Gate (downstream) | `Producers_Office/Pre_Publish_Gate.md` |
| Legal Gate CLI v1.2 | `artifacts/legal/legal_gate.py` |
| Gate validation tests | `artifacts/legal/test_gate_v11.py` |
| Mass Dissemination | `Legal/Mass_Dissemination/CHARTER.md` |
| AI Content | `Legal/AI_Content/CHARTER.md` |
| Talent & Replica | `Legal/Talent_Replica/CHARTER.md` |
| Music Clearance | `Legal/Music_Clearance/CHARTER.md` |
| Cast Compliance (#110) | `Cast/Casting_Bible/audit/compliance_matrix.md` |
| Age Policy | `Research/Age_Policy_Locked.md` |
| 2257 prompt schema | `prompts/MASTER_JSON_Prompt_Template_ACTIVE.json` |
| Producer authority | `PRODUCER.md` |

— Upon Tyne Productions / STUDIO · Locked June 2026