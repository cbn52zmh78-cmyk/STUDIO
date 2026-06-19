# Music & Sound

| Subfolder | Purpose |
|-----------|---------|
| `Music_Beds/` | **Owned / royalty-free / CC0 beds** by lane-mood (Gate 0 row 2) |
| `clearance_manifest.json` | Per-track source, license, attribution, allowed-channels |
| `science_music_assignments.json` | T5-182 science slate bed stamps |
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
| `cosmic-awe` | Astrophysics, JWST/EHT, cosmology wonder-tone |
| `clinical-precision` | Molecular, PDB, lab-measurement explainers |
| `physics-precision` | Classical & atmospheric physics explainers |
| `chemistry-lab` | Chemical reaction & bonding explainers |

Declare `gate_0.music_bed_id` (e.g. `BED-COS-001`, `BED-CLI-001`, `BED-PHY-001`) in concept JSON. Intake emits a manifest-backed brief line; `legal_gate.py` reads `clearance_manifest.json` for row 2 PASS.

Period pairing: `Canons/Historical_SoT_Standard_v1.md` §5 · Science pairing: `Canons/Scientific_SoT_Standard_v1.md` §5.

See `Legal/Music_Clearance/` before any **non-manifest** licensed track hits picture lock.