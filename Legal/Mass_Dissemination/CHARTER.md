# Mass Dissemination Compliance

AI video is not a sandbox. The moment we make it, we are planning to put it **somewhere** — and every destination has its own law.

## Two legal stacks (both mandatory at Gate 0)

| Stack | Governs |
|-------|---------|
| **AI Content** | Replica consent (AB 2602, SAG), deepfake, synthetic performer, training/likeness, platform AI-label rules |
| **Mass Dissemination** | Rating bodies, broadcast rules, platform ToS, theatrical certification, festival submission, E&O |

**Producer runs both before any generation.** Not after. Not "we'll tag it later."

## Distribution channels we plan for

Declare intent on every gate submission:

| Channel | Compliance surface |
|---------|-------------------|
| **Social** | YouTube, X, TikTok, Instagram — AI disclosure, community guidelines, age-gating, monetization policy |
| **Streaming** | Netflix, Amazon, Apple TV+ — deliverable specs, content ratings (TV-MA etc.), music cue sheets |
| **Theatrical** | CARA/MPA (US), BBFC (UK), regional boards — no self-rating; producer targets ceiling |
| **Festival** | Submission legal packet, short-form ratings, likeness releases |
| **Client** | Work-for-hire, brand safety, indemnity, extra clearance |

## Rating bodies (theatrical ceiling)

Studio mandate: **cinema, not pornography.**

| Rating | Producer use |
|--------|--------------|
| G / PG / PG-13 | Default narrative & editorial |
| R | GFE, mature drama — Intimacy Protocol v1.3 required |
| NC-17 | **Not a production target** — content here is RED or killed |

CARA guard runs inside Legal Gate when `--rating` is supplied.

## Gate 0 workflow (every scene, video, brief)

```
1. Declare: project, target rating, distribution channel(s)
2. Run legal_gate.py (AI + dissemination + CARA)
3. RED → STOP. No prompts. No renders. No client promise.
4. YELLOW → revise and re-gate
5. COUNSEL → lawyer sign-off before spend
6. GREEN → log verdict on call sheet, then pre-prod
```

## Producer note

"I'll only post it on X" does not shrink the legal surface. Social is mass dissemination. Gate it like a theatrical release.