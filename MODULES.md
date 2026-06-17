# Studio Modules — Full Filmmaking Coverage

Every aspect of production has a home. **Producer owns the map.**

| # | Module | Path | Submodule focus |
|---|--------|------|-----------------|
| 00 | **Producers Office** | `Producers_Office/` | Slate, Legal Gate, call sheets, compliance, release tracker |
| 01 | **Legal** | `Legal/` | AI content, IRL film, replicas, music, E&O |
| 02 | **Development** | `Development/` + `Productions/` | Scripts, story, `actor_profile_generator`, director skills |
| 03 | **Talent** | `Cast/` | `actors_roster/`, `GFE/`, `Talent_Agency/`, `CONCEPTS/` |
| 04 | **Pre-Production** | `Pre_Production/` | Breakdowns, storyboards, shot lists, schedule, budget |
| 05 | **Production** | `Production/` | Daily reports, continuity, on-set notes |
| 06 | **Post-Production** | `Post_Production/` | Edit, color, sound, VFX, deliverables |
| 07 | **Visual Pipeline** | `Pipeline/` | Prompt packs, profiles, multishot, one-take (artifacts/) |
| 08 | **Music & Sound** | `Music_Sound/` | Score, source music, cue sheets, ADR |
| 09 | **Locations** | `Locations/` | Scouting, permits, releases |
| 10 | **Art Department** | `Art_Department/` | Props, sets, graphics |
| 11 | **Crew** | `Crew/` | Camera, lighting, sound, art, costume, HMU, PM, transport |
| 12 | **Reference Library** | `Reference_Library/` | Plates, assets, metadata |
| 13 | **Research** | `Research/` | Technique bibles, slips, age policy |
| 14 | **Canons** | `Canons/` | Locked rules — intimacy, real-world refs, bibles |
| 15 | **MAGAZINE** | `MAGAZINE/` | In-universe showcase by medium |
| 16 | **Distribution** | `Distribution/` | Festival, streaming, theatrical, sales |
| 17 | **Client Services** | `Client_Services/` | Briefs, deliverables, feedback |
| 18 | **Prompt Library** | `Prompt_Library/` | Domain prompt bibles |
| 19 | **Templates** | `Templates/` | Reusable scaffolds |
| 20 | **Renders** | `renders/` | review → approved (Producer QC) |

## Tooling (`artifacts/`)

| Package | Tools |
|---------|-------|
| `legal/` | `legal_gate.py` — **hard stop** |
| `production/` | `slate_manager.py`, `call_sheet_manager.py` |
| `talent/` | `performance_study_manager.py` |
| `compliance/` | CARA guard, version control, auditors |
| `prompts/` | Generation, refinement, negatives |
| `video/` | Multishot, one-take, shot lists |
| `profile/` | Model profiles |
| `catalog/` | Asset catalog, reference index |
| `export/` | Grok video packs |

## Phase Gates

| Gate | Requirement |
|------|-------------|
| **Gate 0 — Legal (FIRST)** | `legal_gate.py` on every scene/video/brief. AI law + mass dissemination + CARA. `--rating` + `--channels` required. ≠ RED |
| **Gate 1 — Slate** | Project on slate, status set |
| **Gate 2 — Talent** | Performers `agency_ready` for hero work |
| **Gate 3 — Pre-Prod** | Shot list + plates in `Reference_Library/` |
| **Gate 4 — Production** | Pipeline pack + call sheet logged |
| **Gate 5 — Delivery** | `renders/approved/` + MAGAZINE if public |