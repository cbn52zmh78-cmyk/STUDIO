# Legal — Producer Authority

**Gate 0 runs here first.** Every scene, video, and brief. RED is final.

## Two legal stacks (both mandatory)

1. **AI Content** — replica, deepfake, synthetic performer, likeness
2. **Mass Dissemination** — CARA/rating bodies, social, streaming, theatrical, festival, client, E&O

See `Gate_0_Checklist.md` and `Mass_Dissemination/CHARTER.md`.

## Submodules

| Folder | Scope |
|--------|-------|
| `AI_Content/` | Synthetic media, likeness, deepfake, training data |
| `Mass_Dissemination/` | Rating bodies, platform ToS, broadcast, festival, social |
| `Filmmaking_IRL/` | On-set permits, minors, stunts, insurance |
| `Talent_Replica/` | Casting plates, agency status, performance rights |
| `Music_Clearance/` | Sync, master, samples, cue sheets |
| `Distribution_EO/` | E&O, chain-of-title, release binders |
| `Gate_Reports/` | Machine + human verdict archive |

## Gate CLI (run FIRST)

```bash
python artifacts/legal/legal_gate.py --project "Title" --rating PG-13 --channels social,streaming,theatrical --text "brief"
python artifacts/legal/legal_gate.py --project "Title" --rating R --channels client --file path/to/brief.md
```

## Verdicts

- **GREEN** — Proceed
- **YELLOW** — Proceed with documented mitigations
- **COUNSEL** — Outside counsel before spend
- **RED** — **HARD STOP** — no generation, no shoot, no publish

## Producer Rule

Director proposes. Producer gates. Legal RED overrides everything including client revenue.