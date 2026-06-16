# Talent Agency Charter v1.0

**Mission:** Study actor **performance** before the studio commits them to slate, MAGAZINE, or approved renders.

**Producer hold:** No `renders/approved/` for talent below `agency_ready` unless explicit override logged in `Producers_Office/Tool_Logs/`.

---

## Agency Status Ladder

| Status | Meaning | Cleared for |
|--------|---------|-------------|
| **development** | Profile only; plate not locked | Research, profile work |
| **plate_locked** | Casting turnaround / hero plate exists | Performance studies, test scenes |
| **performance_review** | Scene studies logged; rubric in progress | Team review sessions |
| **agency_ready** | Rubric passed (≥7.0 avg, 4+ dimensions) | Slate casting, hero production |
| **represented** | Active on producer slate | Priority packaging, MAGAZINE features |

---

## Performance Rubric (0–10)

1. **Emotional range** — believability, modulation, stakes  
2. **Physical continuity** — face, body, wardrobe across takes  
3. **Camera presence** — eye line, stillness, reaction timing  
4. **Voice / direct address** — GFE and dialogue delivery  
5. **Archetype clarity** — reads on first frame  
6. **Movement physics** — gesture, fabric, weight  

---

## Team Workflow

1. `sync` — scan all Cast rosters → create study stubs  
2. Lock casting plates (no hero until plate_locked)  
3. Run performance studies — log scenes + scores (no approved render required)  
4. Agency meeting — review `Reports/`  
5. Promote to `agency_ready` → then slate + MAGAZINE  

---

## Commands

```powershell
cd "C:\Users\NCG\Videos\Grok Projects"
python artifacts/talent/performance_study_manager.py sync
python artifacts/talent/performance_study_manager.py report
python artifacts/talent/performance_study_manager.py show --talent valentina_moreau
python artifacts/talent/performance_study_manager.py scene --talent gfe_vesper --project GFE --scene "morning direct-address" --medium video --notes "Warm eye line, subtle smile drift on take 3" --scores "{\"camera_presence\": 8, \"voice_direct_address\": 7}"
```

---

*Performance first. Packaging second. Renders when the agency says go.*