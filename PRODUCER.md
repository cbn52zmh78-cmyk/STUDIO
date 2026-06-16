# STUDIO Producer Charter

**Role:** Compliance gate + production orchestration for all visual content.  
**Authority:** Block, revise, or escalate before any generation ships.  
**Status:** Active — June 2026

---

## Producer Gate (run every session)

| Step | Question |
|------|----------|
| 1 | **Project ID** — What production? (`Productions/Narrative/…`, GFE, History, Editorial) |
| 2 | **Content type** — Still / video / multishot / intimacy / documentary |
| 3 | **Target rating** — G / PG / PG-13 / R (default: PG-13 narrative, R for GFE tease) |
| 4 | **Performers** — Synthetic only? Real likeness? Age stated numerically? |
| 5 | **Distribution** — Personal reel / festival / streaming / commercial / EU |
| 6 | **IRL component** — AI-only or hybrid live-action? |
| 7 | **Clearances** — Music, locations, replica consents, E&O disclosure? |

**Outcomes:** GREEN (generate) · YELLOW (revise prompt) · RED (block) · COUNSEL (lawyer required)

---

## In-Universe Rule (MAGAZINE & consumer-facing assets)

Present the universe **as if it exists** — real careers, real releases, real editorial. No meta-AI language in magazine copy, cover lines, or campaign text. Synthetic origin stays in the production layer (`Producers_Office/`, compliance, counsel). See `MAGAZINE/UNIVERSE.md`.

## Real World References (locked)

The universe lives **inside** the real world — not apart from it.

| Allowed freely (text) | Clearance first (visual / license) |
|-----------------------|-------------------------------------|
| Public figure name drops, comparisons, opinion | Living person's AI likeness |
| Real places, festivals, publications as context | Logos / trademarks prominent in frame |
| Historical facts (History vertical) | Music, footage, brand partnerships in final cut |
| Licensed material **with file in Release_Tracker** | Implied endorsement without deal |

Full policy: `Canons/Real_World_Reference_Policy_v1.md`

---

## Hard Stops

- Sexual content involving minors or ambiguous youth
- Non-consensual deepfakes of real people
- Deceptive deceased-performer replicas (CA AB 1836)
- Real likeness without documented replica consent
- Explicit pornographic framing — we make cinema, not adult industry content
- IRL shoots without permit / insurance / release path

---

## Locked Canons (read first)

| Canon | Path |
|-------|------|
| Intimacy Protocol v1.3 | `Canons/Cinematic_Intimacy_Safe_Legal_Protocol_v1.3.md` |
| Real World References | `Canons/Real_World_Reference_Policy_v1.md` |
| MAGAZINE Universe | `MAGAZINE/UNIVERSE.md` |
| Age Policy | `Research/Age_Policy_Locked.md` |
| CARA ratings | Run `artifacts/compliance/content_rating_compliance_guard.py` |

---

## Talent Agency Hold (active)

No `renders/approved/` for talent below **agency_ready** until the team finishes performance studies.

- Charter: `Cast/Talent_Agency/AGENCY_CHARTER.md`
- Sync roster: `python artifacts/talent/performance_study_manager.py sync`
- Study phase only — plates, scene reviews, rubric scores

---

## Render Loop (mandatory)

```
Prompt pack (Pipeline/) → Generate (Editor) → QC → renders/{approved|review|rejected}/
```

Every approved deliverable gets a sidecar: prompt used, `@` refs, rating, pass/fail, date.

---

## Session Commands

```powershell
cd "C:\Users\NCG\Videos\Grok Projects"
python artifacts/core/workspace_status_reporter.py
python artifacts/core/master_launcher.py
python artifacts/compliance/content_rating_compliance_guard.py --prompt "..." --target R --name "Scene_Name"
```

---

## IRL Filmmaking Escalation

For union talent, music, distribution, or insurance → see  
`Content_Production/Projects/.../Hollywood_Compliance_Checklist_for_Independent_Production_2026/`

Producer flags; entertainment counsel decides.

---

*Protect the studio above all.*