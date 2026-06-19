# Proof #214 — Rough Draft → Pro Screenplay

**The undeniable demo:** hand the studio a deliberately amateur original draft;
get back a professional screenplay, professional coverage, and a line-by-line
account of every change. Same story. Same ending. Better in every measurable way.

## The package

| Stage | File | What it is |
|-------|------|-----------|
| Before | [`01_rough_draft.txt`](01_rough_draft.txt) | The original draft as a client would write it — prose blocks, on-the-nose dialogue, feelings in parentheticals, a narrated flashback, spelling slips |
| After | [`02_pro_screenplay.txt`](02_pro_screenplay.txt) | Standard screenplay format; subtext-driven; ~23% shorter; the keys carry the scene |
| Analysis | [`03_coverage.md`](03_coverage.md) | Industry script coverage — logline, synopsis, comments, craft grid, verdict |
| Diff | [`04_what_we_changed.md`](04_what_we_changed.md) | 10 itemized changes, each tied to a craft principle, plus what we deliberately kept |

## Scene

*THE KEYS* — a nurse drives out to take her widowed father's car keys after a
minor accident. A two-hander, one location, no effects. Universal, castable at
any budget.

## Pipeline verification

The developed screenplay was run through the studio's **Gate 0 — Legal**
(`artifacts/legal/legal_gate.py`), the same first gate every scene, brief, and
video passes:

- **Verdict: ✅ GREEN** · CARA: COMPLIANT · ceiling PG · channels festival/streaming/client
- Report: `Studio/Producers_Office/Legal_Gate/GATE_GREEN_proof_214_the_keys_20260619_025919.json`

Reproduce:

```powershell
$env:PYTHONIOENCODING='utf-8'
python artifacts/legal/legal_gate.py --project proof_214_the_keys `
  --file "STUDIO/Development/Proofs/proof_214/02_pro_screenplay.txt" `
  --rating PG --channels festival,streaming,client
```

## The claim, proven

1. **Format** — prose in, shootable screenplay out.
2. **Craft** — exposition becomes subtext; stated theme becomes staged image.
3. **Honesty** — every edit is documented and reversible; the writer's intent is preserved, not overwritten.
4. **Pipeline-ready** — the output clears Gate 0 on the first pass.

*STUDIO Development / Story Department · 2026-06-19 · #214.*
