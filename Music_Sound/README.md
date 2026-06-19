# Music & Sound

| Subfolder | Purpose |
|-----------|---------|
| `Music_Beds/` | **Owned / royalty-free / CC0 beds** by lane-mood (Gate 0 row 2) |
| `clearance_manifest.json` | Per-track source, license, attribution, allowed-channels |
| `Score/` | Composer agreements, stems, sessions |
| `Source_Music/` | Licensed tracks, temp music log |
| `Cue_Sheets/` | ASCAP/BMI/SESAC submission prep |
| `ADR/` | Looping sessions, replacement dialogue |

## Music bed lanes (`Music_Beds/`)

| Lane | Use |
|------|-----|
| `documentary-prestige` | Host-led documentary, archive, prestige explainers |
| `cinematic-thriller` | Stakes, investigation, tension narrative |
| `soft-warm-companion` | Warm companion tone, gentle intimacy-safe beds |
| `upbeat-explainer` | Product explainers, tutorials, social-first cuts |
| `period-antiquity` | Ancient / classical / late-antique / Bronze Age biography |
| `period-medieval` | Medieval, Anglo-Norman, Gothic, Norse biography |
| `period-tudor` | Tudor / Elizabethan / Henrician court biography |

Declare `gate_0.music_bed_id` (e.g. `BED-DOC-001`, `BED-TUD-001`) in concept JSON. Intake emits a manifest-backed brief line; `legal_gate.py` reads `clearance_manifest.json` for row 2 PASS.

Period pairing guide: `Canons/Historical_SoT_Standard_v1.md` §5.

See `Legal/Music_Clearance/` before any **non-manifest** licensed track hits picture lock.