# Cast Compliance Audit — 100 Actors
**Audited:** 2026-06-19T03:02:59.494334+00:00

## Summary
- **Total:** 100
- **CLEAR:** 35
- **FLAG:** 64
- **BLOCKED:** 1
- **Floor-age (21–22) visual review:** 6

## Blocked (schema non-compliant)
- `FreyaLindMag-001` — plate_lock_mismatch

## Re-roll required

- `FreyaLindMag-001` — PLATE/LOCK MISMATCH: plate shows dark-skinned African-styled model; lock specifies Swedish strawberry-blonde freckled fair skin. Re-roll required.

## Floor-age entries (21–22) — visual review

- `Yuki-001` (actors_roster) age=22 visual=PASS — Slender petite build; mature bone structure and adult proportions. Unambiguously 21+.
- `HanaGFE-001` (gfe) age=22 visual=PASS — Petite East Asian; adult facial structure and body. No teen indicators.
- `LyraGFE-001` (gfe) age=22 visual=PASS — Slim-athletic; smiling adult features, developed proportions.
- `VioletGFE-001` (gfe) age=22 visual=PASS — Curvy adult physique; mid-20s read. No ambiguous youth markers.
- `YumeGFE-001` (gfe) age=21 visual=PASS — Floor age 21; voluptuous adult body and mature face. No borderline flags.
- `FreyaLindMag-001` (magazine_editorial) age=22 visual=FAIL — PLATE/LOCK MISMATCH: plate shows dark-skinned African-styled model; lock specifies Swedish strawberry-blonde freckled fair skin. Re-roll required.

## Prompt hygiene flags (usable, lock text should be patched)

- Count: 64
- Lanes: 35 male roster + 20 GFE + 10 MAGAZINE missing explicit synthetic/adult clauses in appearance_lock_verbatim

## Full matrix

| actor_id | lane | age | synth | likeness | disclosure | plate | lock | status |
|---|---|---:|:-:|:-:|:-:|:-:|:-:|---|
| Aiko-001 | actors_roster | 26 | ✓ | ✓ | ✓ | ✓ | ✓ | **CLEAR** |
| Amahle-001 | actors_roster | 25 | ✓ | ✓ | ✓ | ✓ | ✓ | **CLEAR** |
| Amara-001 | actors_roster | 30 | ✓ | ✓ | ✓ | ✓ | ✓ | **CLEAR** |
| Amir-001 | actors_roster | 32 | ✓ | ✓ | ✓ | ✓ | ✓ | **CLEAR** |
| Ananya-001 | actors_roster | 29 | ✓ | ✓ | ✓ | ✓ | ✓ | **CLEAR** |
| Anastasia-001 | actors_roster | 33 | ✓ | ✓ | ✓ | ✓ | ✓ | **CLEAR** |
| Andre-001 | actors_roster | 27 | ✓ | ✓ | ✓ | ✓ | ✓ | **CLEAR** |
| Arjun-001 | actors_roster | 30 | ✓ | ✓ | ✓ | ✓ | ✓ | **CLEAR** |
| BridgetOkafor-001 | actors_roster | 35 | ✓ | ✓ | ✓ | ✓ | ✓ | **CLEAR** |
| BridgetWalsh-001 | actors_roster | 39 | ✓ | ✓ | ✓ | ✓ | ✓ | **CLEAR** |
| Camille-001 | actors_roster | 26 | ✓ | ✓ | ✓ | ✓ | ✓ | **CLEAR** |
| Carlos-001 | actors_roster | 42 | ✓ | ✓ | ✓ | ✓ | ✓ | **CLEAR** |
| Carmen-001 | actors_roster | 32 | ✓ | ✓ | ✓ | ✓ | ✓ | **CLEAR** |
| Chiara-001 | actors_roster | 34 | ✓ | ✓ | ✓ | ✓ | ✓ | **CLEAR** |
| Connor-001 | actors_roster | 29 | ✓ | ✓ | ✓ | ✓ | ✓ | **CLEAR** |
| Dante-001 | actors_roster | 26 | ✓ | ✓ | ✓ | ✓ | ✓ | **CLEAR** |
| Diego-001 | actors_roster | 28 | ✓ | ✓ | ✓ | ✓ | ✓ | **CLEAR** |
| Dmitri-001 | actors_roster | 40 | ✓ | ✓ | ✓ | ✓ | ✓ | **CLEAR** |
| Elijah-001 | actors_roster | 37 | ✓ | ✓ | ✓ | ✓ | ✓ | **CLEAR** |
| Elinor-001 | actors_roster | 26 | ✓ | ✓ | ✓ | ✓ | ✓ | **CLEAR** |
| Emma-001 | actors_roster | 31 | ✓ | ✓ | ✓ | ✓ | ✓ | **CLEAR** |
| Ethan-001 | actors_roster | 29 | ✓ | ✓ | ✓ | ✓ | ✓ | **CLEAR** |
| Fatima-001 | actors_roster | 28 | ✓ | ✓ | ✓ | ✓ | ✓ | **CLEAR** |
| Finn-001 | actors_roster | 33 | ✓ | ✓ | ✓ | ✓ | ✓ | **CLEAR** |
| Grace-001 | actors_roster | 23 | ✓ | ✓ | ✓ | ✓ | ✓ | **CLEAR** |
| Hana-001 | actors_roster | 24 | ✓ | ✓ | ✓ | ✓ | ✓ | **CLEAR** |
| Hassan-001 | actors_roster | 36 | ✓ | ✓ | ✓ | ✓ | ✓ | **CLEAR** |
| Inés-001 | actors_roster | 31 | ✓ | ✓ | ✓ | ✓ | ✓ | **CLEAR** |
| Isabella-001 | actors_roster | 29 | ✓ | ✓ | ✓ | ✓ | ✓ | **CLEAR** |
| James-001 | actors_roster | 38 | ✓ | ✓ | ✓ | ✓ | ✓ | **CLEAR** |
| Jayden-001 | actors_roster | 24 | ✓ | ✓ | ✓ | ✓ | ✓ | **CLEAR** |
| JiYeon-001 | actors_roster | 23 | ✓ | ✓ | ✓ | ✓ | ✓ | **CLEAR** |
| Julian-001 | actors_roster | 31 | ✓ | ✓ | ✓ | ✓ | ✓ | **CLEAR** |
| Katya-001 | actors_roster | 24 | ✓ | ✓ | ✓ | ✓ | ✓ | **CLEAR** |
| Kenji-001 | actors_roster | 34 | ✓ | ✓ | ✓ | ✓ | ✓ | **CLEAR** |
| Khalid-001 | actors_roster | 30 | ✓ | ✓ | ✓ | ✓ | ✓ | **FLAG** |
| Kofi-001 | actors_roster | 28 | ✓ | ✓ | ✓ | ✓ | ✓ | **FLAG** |
| Lars-001 | actors_roster | 34 | ✓ | ✓ | ✓ | ✓ | ✓ | **FLAG** |
| Layla-001 | actors_roster | 31 | ✓ | ✓ | ✓ | ✓ | ✓ | **FLAG** |
| Linh-001 | actors_roster | 25 | ✓ | ✓ | ✓ | ✓ | ✓ | **FLAG** |
| Luca-001 | actors_roster | 29 | ✓ | ✓ | ✓ | ✓ | ✓ | **FLAG** |
| Maeve-001 | actors_roster | 28 | ✓ | ✓ | ✓ | ✓ | ✓ | **FLAG** |
| Malik-001 | actors_roster | 29 | ✓ | ✓ | ✓ | ✓ | ✓ | **FLAG** |
| Marco-001 | actors_roster | 36 | ✓ | ✓ | ✓ | ✓ | ✓ | **FLAG** |
| Marcus-001 | actors_roster | 32 | ✓ | ✓ | ✓ | ✓ | ✓ | **FLAG** |
| MeiLing-001 | actors_roster | 27 | ✓ | ✓ | ✓ | ✓ | ✓ | **FLAG** |
| Nadia-001 | actors_roster | 42 | ✓ | ✓ | ✓ | ✓ | ✓ | **FLAG** |
| Nikolai-001 | actors_roster | 27 | ✓ | ✓ | ✓ | ✓ | ✓ | **FLAG** |
| Noor-001 | actors_roster | 27 | ✓ | ✓ | ✓ | ✓ | ✓ | **FLAG** |
| Olivia-001 | actors_roster | 27 | ✓ | ✓ | ✓ | ✓ | ✓ | **FLAG** |
| Oluwaseun-001 | actors_roster | 33 | ✓ | ✓ | ✓ | ✓ | ✓ | **FLAG** |
| Pierre-001 | actors_roster | 41 | ✓ | ✓ | ✓ | ✓ | ✓ | **FLAG** |
| Priya-001 | actors_roster | 37 | ✓ | ✓ | ✓ | ✓ | ✓ | **FLAG** |
| Rachel-001 | actors_roster | 36 | ✓ | ✓ | ✓ | ✓ | ✓ | **FLAG** |
| Rafael-001 | actors_roster | 35 | ✓ | ✓ | ✓ | ✓ | ✓ | **FLAG** |
| Ravi-001 | actors_roster | 38 | ✓ | ✓ | ✓ | ✓ | ✓ | **FLAG** |
| Ren-001 | actors_roster | 25 | ✓ | ✓ | ✓ | ✓ | ✓ | **FLAG** |
| Sam-001 | actors_roster | 27 | ✓ | ✓ | ✓ | ✓ | ✓ | **FLAG** |
| Serena-001 | actors_roster | 30 | ✓ | ✓ | ✓ | ✓ | ✓ | **FLAG** |
| Sienna-001 | actors_roster | 28 | ✓ | ✓ | ✓ | ✓ | ✓ | **FLAG** |
| Sofia-001 | actors_roster | 29 | ✓ | ✓ | ✓ | ✓ | ✓ | **FLAG** |
| Tessa-001 | actors_roster | 27 | ✓ | ✓ | ✓ | ✓ | ✓ | **FLAG** |
| Theo-001 | actors_roster | 25 | ✓ | ✓ | ✓ | ✓ | ✓ | **FLAG** |
| Tomas-001 | actors_roster | 26 | ✓ | ✓ | ✓ | ✓ | ✓ | **FLAG** |
| Valentina-001 | actors_roster | 47 | ✓ | ✓ | ✓ | ✓ | ✓ | **FLAG** |
| Vikram-001 | actors_roster | 32 | ✓ | ✓ | ✓ | ✓ | ✓ | **FLAG** |
| Viktor-001 | actors_roster | 35 | ✓ | ✓ | ✓ | ✓ | ✓ | **FLAG** |
| Wei-001 | actors_roster | 31 | ✓ | ✓ | ✓ | ✓ | ✓ | **FLAG** |
| Yuki-001 | actors_roster | 22 | ✓ | ✓ | ✓ | ✓ | ✓ | **FLAG** |
| Zara-001 | actors_roster | 28 | ✓ | ✓ | ✓ | ✓ | ✓ | **FLAG** |
| AikoGFE-001 | gfe | 24 | ✓ | ✓ | ✓ | ✓ | ✓ | **FLAG** |
| EmberGFE-001 | gfe | 26 | ✓ | ✓ | ✓ | ✓ | ✓ | **FLAG** |
| HanaGFE-001 | gfe | 22 | ✓ | ✓ | ✓ | ✓ | ✓ | **FLAG** |
| IrisGFE-001 | gfe | 25 | ✓ | ✓ | ✓ | ✓ | ✓ | **FLAG** |
| JadeGFE-001 | gfe | 25 | ✓ | ✓ | ✓ | ✓ | ✓ | **FLAG** |
| KiraGFE-001 | gfe | 27 | ✓ | ✓ | ✓ | ✓ | ✓ | **FLAG** |
| LunaGFE-001 | gfe | 24 | ✓ | ✓ | ✓ | ✓ | ✓ | **FLAG** |
| LyraGFE-001 | gfe | 22 | ✓ | ✓ | ✓ | ✓ | ✓ | **FLAG** |
| MikaGFE-001 | gfe | 24 | ✓ | ✓ | ✓ | ✓ | ✓ | **FLAG** |
| NikoGFE-001 | gfe | 27 | ✓ | ✓ | ✓ | ✓ | ✓ | **FLAG** |
| NovaGFE-001 | gfe | 23 | ✓ | ✓ | ✓ | ✓ | ✓ | **FLAG** |
| RavenGFE-001 | gfe | 24 | ✓ | ✓ | ✓ | ✓ | ✓ | **FLAG** |
| RinGFE-001 | gfe | 25 | ✓ | ✓ | ✓ | ✓ | ✓ | **FLAG** |
| SageGFE-001 | gfe | 26 | ✓ | ✓ | ✓ | ✓ | ✓ | **FLAG** |
| ScarletGFE-001 | gfe | 28 | ✓ | ✓ | ✓ | ✓ | ✓ | **FLAG** |
| SoraGFE-001 | gfe | 23 | ✓ | ✓ | ✓ | ✓ | ✓ | **FLAG** |
| VesperGFE-001 | gfe | 26 | ✓ | ✓ | ✓ | ✓ | ✓ | **FLAG** |
| VioletGFE-001 | gfe | 22 | ✓ | ✓ | ✓ | ✓ | ✓ | **FLAG** |
| WillowGFE-001 | gfe | 23 | ✓ | ✓ | ✓ | ✓ | ✓ | **FLAG** |
| YumeGFE-001 | gfe | 21 | ✓ | ✓ | ✓ | ✓ | ✓ | **FLAG** |
| AnyaPetrovaMag-001 | magazine_editorial | 23 | ✓ | ✓ | ✓ | ✓ | ✓ | **FLAG** |
| FreyaLindMag-001 | magazine_editorial | 22 | ✓ | ✓ | ✓ | ✓ | ✓ | **BLOCKED** |
| IsoldeMoreauMag-001 | magazine_editorial | 26 | ✓ | ✓ | ✓ | ✓ | ✓ | **FLAG** |
| LioraVossMag-001 | magazine_editorial | 24 | ✓ | ✓ | ✓ | ✓ | ✓ | **FLAG** |
| MeiLinChenMag-001 | magazine_editorial | 25 | ✓ | ✓ | ✓ | ✓ | ✓ | **FLAG** |
| NadiaOkoroMag-001 | magazine_editorial | 28 | ✓ | ✓ | ✓ | ✓ | ✓ | **FLAG** |
| PriyaSinghMag-001 | magazine_editorial | 24 | ✓ | ✓ | ✓ | ✓ | ✓ | **FLAG** |
| SofiaAlvarezMag-001 | magazine_editorial | 27 | ✓ | ✓ | ✓ | ✓ | ✓ | **FLAG** |
| ValentinaRossiMag-001 | magazine_editorial | 25 | ✓ | ✓ | ✓ | ✓ | ✓ | **FLAG** |
| ZaraKhanMag-001 | magazine_editorial | 26 | ✓ | ✓ | ✓ | ✓ | ✓ | **FLAG** |
