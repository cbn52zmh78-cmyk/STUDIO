# Companion Lane — Series Structure v1
**ID:** T3 #141 · Companion Lane Series Structure  
**Date:** 2026-06-19  
**Format:** `conversational-companion` · SFW mandatory · Upon Tyne Productions  
**Status:** DRAFT — Hub compilation, not yet intake-run

---

## 1. Concept

The companion lane produces short-form check-in videos (30–45s) featuring a recurring synthetic companion persona delivering low-pressure, supportive content — affirmations, micro-moments of calm, light reflection prompts. The content registers as a supportive friend, not a romantic partner or therapist.

**Core guardrail (non-negotiable):** Every frame, line, and set choice must clear PG at theatrical CARA standard. No suggestive framing, no bedroom staging, no roleplay. The companion is *present and warm*, not *romantic or intimate*.

---

## 2. Recurring Persona

Each companion series anchors to **one actor per series run** (e.g., Sage, Willow, Sora). The actor holds identity lock across all episodes in that series run. Series can be retired and replaced with a new actor on a new series run without disrupting the format.

**Recommended launch persona: Willow (WillowGFE-001)**  
- Age lock: 23 · content_rating: SFW_SUGGESTIVE_CLOTHED (SFW mode only)
- Tags: Wellness girlfriend fantasy · Morning ritual intimacy · Breath-led romance
- Why: "Wellness" and "morning ritual" tags align naturally with check-in/affirmation content; the persona archetype is calm and grounded rather than high-energy or night-club adjacent

**Alternative personas:**
- Sora (SoraGFE-001, 23): "Soft girlfriend fantasy · Slice-of-life romance" — best for low-key daily-life tone
- Sage (SageGFE-001, 26): "Intellectual · Quote-heavy" — best for reflection-prompt episodes (proved in gfe_companion_sage_proof_v1)
- Willow or Sora for wellness series; Sage for journaling / depth series

**Identity lock requirement:** A `sage_companion_identity_lock.json`-style lock card must exist for each series persona before first episode enters intake. Reference: `STUDIO/Productions/Companion/gfe_companion_sage_proof_v1_longform_v1/sage_companion_identity_lock.json`

---

## 3. Episode Beat Structure (6-Beat Template)

| Beat | ID | Role | Duration | SFW Notes |
|------|----|------|----------|-----------|
| 1 | `01_greeting` | Warm camera address — "glad you're here" energy | 6–8s | Fully clothed, medium-close, no suggestive angle |
| 2 | `02_check_in` | Open question to viewer | 6–8s | Attentive listen pose, no physical contact staging |
| 3 | `03_core_message` | Single calm thought or affirmation | 7–9s | Static or slow push, hands at neutral or open gesture |
| 4 | `04_reflective_pause` | Invited pause / breath beat | 5–7s | No cutaway; companion holds eye contact or soft down-look |
| 5 | `05_encouragement` | Affirmation ("you're doing fine") | 5–7s | Warm, not effusive; no physical proximity escalation |
| 6 | `06_soft_close` | Goodbye + CTA ("I'll be here") | 5–7s | Low-key, no hard sell; companion exits on calm note |

**Target runtime:** 34–46s (provenance card adds 5s if enabled)  
**Provenance card:** RECOMMENDED ON (label: "Synthetic companion · AI generated performer · [Series name] · Upon Tyne Productions"). Proof `gfe_companion_sage_proof_v1` had it OFF — enable for any non-proof publish.

---

## 4. Episode Cadence

**Series run:** 6 episodes per persona, released weekly  
**Thematic arc across a 6-episode run:**

| Ep | Theme | Sample hook |
|----|-------|-------------|
| 1 | Arrival / welcome | "No catch-up needed — you're already here." |
| 2 | Permission to be slow | "Nothing needs to get fixed today." |
| 3 | One small win | "What's one thing that went okay this week?" |
| 4 | Recharge | "When did you last do something just for you?" |
| 5 | Forward lean | "What are you quietly looking forward to?" |
| 6 | Goodbye / see-you-next-week | "Same time next week? I'll be here." |

**Thematic series options (future runs):**
- Morning check-in series (early light aesthetic, soft AM set dressing)
- End-of-week wind-down series (golden hour, slower pacing)
- Seasonal tie-in series (no holiday branding — affect tone only, no dates)
- Journaling companion series (Sage persona; prompts, not answers)

---

## 5. Set & Style Locks

| Lock | Value |
|------|-------|
| Set ID | `@Set-Modern-Apartment-001` |
| Style ID | `@Style-Soft-Warm-001` |
| Set description | Modern apartment — oak floor, linen sofa, window camera-left, kitchen blur bg |
| Wardrobe | Smart-casual or lifestyle casual — fully clothed; no cropped tops, no sleepwear, no swimwear |
| Camera | Gentle float or static medium-close; micro-push on encouragement beats only |
| Forbidden angles | Explicit framing, suggestive angles, lingerie or bedroom staging, clinical flatness |
| Lighting | Soft warm key — daylight or soft diffused fill; no noir or dramatic shadow |
| Music bed | `BED-WARM-001` (cleared per clearance_manifest.json) |

---

## 6. SFW Content Rails (Hard, All Episodes)

1. **PG mandatory** — no sexual content, no nudity, no suggestive framing, no intimate staging
2. **No medical, legal, or financial advice** presented as professional counsel
3. **No romantic roleplay** — companion energy is "supportive friend," not "girlfriend fantasy"
4. **No physical contact** between companion and viewer implied or staged
5. **No bedroom or intimate settings** — modern apartment SFW set only
6. **Synthetic disclosure** — AI disclosure must appear in every publish surface (provenance card + upload description)
7. **No real-person likeness** — persona is invented; no celebrity reference in appearance or voice spec
8. **Gate 0 required before any publish** — YELLOW cleared to GREEN; human_signoff=true

---

## 7. Gate 0 Channel Map

| Channel | Rating | AI Disclosure Surface | Notes |
|---------|--------|-----------------------|-------|
| Social (short-form) | PG | Provenance card burn-in + platform AI label | Must re-gate GREEN from YELLOW before first publish |
| Streaming | PG | Provenance card + upload description | Same re-gate requirement |
| Client deliverable | PG | Description + separate disclosure card | Frame companion as "AI companion demo" in all client comms |

---

## 8. Production Path

```powershell
# 1. Build identity lock for persona (first time per series)
python STUDIO/Pipeline/build_companion_proof.py --actor WillowGFE-001 --series-id willow_s1 --lock-only

# 2. Author episode concept + brief
# Concept template: format_id=conversational-companion, 6 beats, gate_0 per §6 above

# 3. Intake
python STUDIO/Pipeline/production_intake.py STUDIO/Pipeline/Concepts/companion/<slug>.concept.json

# 4. Script-only validation
python DAVID/scripts/render_longform.py DAVID/scripts/longform_scripts/<slug>_script.json --script-only

# 5. Render (on Benjamin's approval)
python STUDIO/Pipeline/build_companion_proof.py --script <slug>_script.json --seamless

# 6. Pre-publish C4 gate (run after render)
# D1: render check · D2: Gate 0 GREEN · D3: N/A (honesty rail not applicable to companion) · D4: brand check
```

---

## 9. Deliverables (Series v1 Launch)

| Item | Status |
|------|--------|
| 6-beat episode template | ✅ Established (Sage proof validated) |
| Persona recommendation (Willow) | ✅ This document |
| Identity lock (Willow) | ⏳ Pending — build at series kickoff |
| 6 episode concepts (Willow S1) | ⏳ Pending — author when Benjamin greenlit series |
| Gate 0 re-gate (Sage proof → GREEN) | ⏳ Pending — requires Benjamin's signoff at publish |
| Thumbnail specs (companion lane) | ⏳ Pending — T2 #140 deliverable (see thumbnail generator) |

---

*Upon Tyne Productions / STUDIO Companion Lane · T3 #141 · Hub 2026-06-19*
