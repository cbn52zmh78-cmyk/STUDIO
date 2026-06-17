# Gate 0 — Legal Compliance Checklist

**First action on every scene, video, prompt pack, or client brief. No exceptions.**

## Required inputs

- [ ] Project / slate ID
- [ ] Target rating (G / PG / PG-13 / R)
- [ ] Distribution channel(s): `social` · `streaming` · `theatrical` · `festival` · `client`
- [ ] Brief text, prompt, or script excerpt
- [ ] Performer ages stated (numerical) if intimacy or cast involved
- [ ] Real-person references flagged (name-drop vs likeness)

## Command

```powershell
python artifacts/legal/legal_gate.py ^
  --project "henry_ii_council" ^
  --rating PG-13 ^
  --channels social,streaming,theatrical ^
  --text "your scene brief or prompt"
```

## Dual-stack review

| Stack | Question |
|-------|----------|
| AI Content | Replica consent? Deepfake? Synthetic performer rights? |
| Mass Dissemination | CARA ceiling? Platform AI label? Festival packet? E&O exposure? |
| Talent Replica | `agency_ready` for hero delivery? |

## Verdict actions

| Verdict | Producer |
|---------|----------|
| RED | Kill. Tell Director. Tell client if applicable. |
| COUNSEL | Freeze spend until counsel signs. |
| YELLOW | Send revision notes. Re-gate. |
| GREEN | Log on call sheet. Proceed to pre-prod / pipeline. |

## After GREEN only

- Open call sheet
- Run talent sync if new cast
- Generate prompts / video
- CARA report archived in `Producers_Office/Compliance_Reports/`