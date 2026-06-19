# STUDIO Pre-Publish Gate v1.0

**Status:** Production canon. Non-negotiable.  
**Applies to:** Every STUDIO video before shipping — social cut, streaming master, MAGAZINE feature, GFE clip, client deliverable, festival packet.  
**Prerequisite:** Gate 0 Legal **GREEN** already logged (`Legal/Gate_0_Checklist.md`).  
**Blocks:** `renders/approved/`, public upload, client handoff, MAGAZINE publish.

---

## Pre-Publish Checklist

Complete every row. **Any FAIL = HOLD.** No ship until all PASS.

| # | Gate | Requirement | Verify | PASS |
|---|------|-------------|--------|:----:|
| 1 | **Cast — 21+ & compliant (#110)** | Every on-screen synthetic performer is **21+** with numerical age stated in production prompts and final output metadata. Each cast `actor_id` is **CLEAR** or **FLAG-cleared** in the Cast Compliance Audit — **never BLOCKED** (`blocked_actors.json` empty for this deliverable). Floor-age entries (21–22) require completed visual adult review on plate. | `Cast/Casting_Bible/audit/compliance_matrix.json` · `blocked_actors.json` · `python STUDIO/Cast/Scripts/audit_cast_compliance.py` | ☐ |
| 2 | **Synthetic-only** | No real-person or celebrity likeness in face, body, voice, or naming intent. Performers match Casting Bible `synthetic: true`, `real_person_likeness: false`. | Casting Bible registries · `appearance_lock_verbatim` on every performer | ☐ |
| 3 | **AI disclosure on output** | Shipped file carries AI/synthetic-performer disclosure in **all required surfaces** for the target platform: in-video label and/or credits, description/caption, and platform metadata field where available. Minimum wording: *Synthetic performer — label in credits/description per Upon Tyne Productions policy.* | Final export + upload draft reviewed side-by-side | ☐ |
| 4 | **SFW boundary** | No nudity, topless, explicit sexual content, or implied nudity in any frame. Wardrobe stays SFW or suggestive-clothed per lane (`SFW` / `SFW_SUGGESTIVE_CLOTHED`). CARA/target-rating ceiling not exceeded. | Full timeline + hero frames · `artifacts/compliance/content_rating_compliance_guard.py` | ☐ |
| 5 | **No minors depicted** | Zero minors in frame — foreground, background, insert, flashback, photo-in-scene, or implied. No school-setting sensuality. No ambiguous youth framing. | Frame-by-frame review of all performer appearances | ☐ |
| 6 | **Target-platform policy** | Destination platform ToS satisfied: AI-label rules, age-gating, content restrictions, music/sync rights, branded-content flags, regional rules. Gate 0 `--channels` matches actual publish target. | Platform policy check logged · Gate 0 JSON in `Producers_Office/Legal_Gate/` | ☐ |
| 7 | **Audio / sync / color QA** | Final master passes technical QC: dialogue intelligible; loudness within spec (pipeline target **−16 LUFS** integrated, spread ≤ **1.5 LU** shot-to-shot); no dropouts/clipping; lip-sync and action-sync acceptable; color consistent shot-to-shot (magenta score ≤ **0.42**, no uncorrected cast/grade drift); correct aspect ratio and frame rate for deliverable. Production `qa_report.json` shows **`pass: true`** with zero blocking `issues`. | `qa_report.json` · Post sign-off · `Post_Production/Deliverables/` spec | ☐ |

---

## FAIL Actions

| Result | Producer action |
|--------|-----------------|
| **HOLD** | Do not move to `renders/approved/`. Do not publish. Log reason in `Release_Tracker/`. |
| **REVISE** | Return to Post or Production. Re-run affected gate rows after fix. |
| **KILL** | Gate 0 RED, BLOCKED cast, or minor depiction → hard stop. Rebuild from legal review. |

---

## Cross-References

| Canon | Path |
|-------|------|
| Cast Compliance Audit (#110) | `Cast/Casting_Bible/audit/compliance_matrix.json` |
| Casting Bible registries | `Cast/Casting_Bible/registry/` |
| Age Policy (21+ floor) | `research/Age_Policy_Locked.md` |
| Blocked cast list | `Cast/Casting_Bible/audit/blocked_actors.json` |
| Gate 0 Legal | `Legal/Gate_0_Checklist.md` |
| Intimacy Protocol | `Canons/Cinematic_Intimacy_Safe_Legal_Protocol_v1.3.md` |
| Mass Dissemination | `Legal/Mass_Dissemination/CHARTER.md` |
| Producer chain of command | `PRODUCER.md` |

---

## Producer Sign-Off

```
PRE-PUBLISH GATE — PASS

Project / Slate ID: _______________________________
Deliverable title:  _______________________________
Target platform(s): _______________________________
File / asset ID:    _______________________________

I certify that checklist rows 1–7 are PASS for the deliverable named above.
Cast is 21+ and compliant per #110. Synthetic-only. AI disclosure is present
on the output. Content is within SFW boundary. No minors are depicted. Platform
policy is satisfied. Audio, sync, and color QA are complete.

Cleared for: renders/approved/  ·  distribution  ·  MAGAZINE publish (if applicable)

Producer: _________________________   Date: __________   Verdict: PASS / HOLD
```

— Upon Tyne Productions / STUDIO · Locked June 2026