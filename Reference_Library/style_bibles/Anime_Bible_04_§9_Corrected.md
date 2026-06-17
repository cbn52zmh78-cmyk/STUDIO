# Anime Style Bible 04 — Texhnolyze (2003)
## §9: Advanced Video Production & xAI SDK Integration
**Version:** Corrected v1.1  
**Date:** June 17, 2026  
**Status:** Locked — zero SPIT/GOLDEN bleed

---

### STYLE LOCK

All video output locked to the show's **bleak dystopian realism**, desaturated palette, brutal existential violence, underground concrete gloom, and slow-burn despair.

**Prohibited in this bible:** Bright colors, psychedelic effects, warm tones, painterly softness, rapid cuts, CRT/digital aesthetics.

---

### CONFIRMED SDK SYNTAX (Verified June 2026 — xAI SDK)

```python
from xai_sdk import Client

client = Client()  # api_key loaded from XAI_API_KEY env var

response = client.video.generate(
    prompt="...[style-specific prompt below]...",
    model="grok-imagine-video",
    duration=8,
    aspect_ratio="16:9",
    resolution="720p"
)

print(response.url)  # auto-polls to completion
```

> **Note:** `client.video.generate` (singular) is the canonical xAI SDK call per official docs (docs.x.ai + github.com/xai-org/xai-sdk-python, current as of June 2026). Do not use plural `.videos.generate`.

---

### STYLE-SPECIFIC EXAMPLE PROMPT

```
2003 Texhnolyze bleak dystopian animation, scarred fighter in dim underground arena, desaturated 
greys and blood-red accents, heavy shadows, concrete decay and flickering fluorescent tubes, slow 
brutal movement, existential emptiness in eyes, raw realistic motion, masterpiece frame, 
8-second sequence, grok-imagine-video
```

---

### WORKFLOW MODES

**1. One-Shot Headless (rapid ideation)**
```bash
grok -p "Generate an 8-second Texhnolyze style video: [full descriptive prompt] with exact Texhnolyze directives"
```

**2. Interactive TUI (compare / iterate)**
```bash
grok
```
Inside TUI:
- Activate Plan Mode: `Shift+Tab` or `/plan`
- Paste Texhnolyze bible directives
- Use `/fork variantA` / `/fork variantB` to branch
- Compare outputs side-by-side with natural language refinement

**3. Batch / Production Scale (agent builds the script)**
```bash
grok -p "Write a Python asyncio batch script that generates 6 Texhnolyze style variations using xAI API, saves to ./tests/texhnolyze/, produces a JSON comparison report, and includes tqdm progress bar with error retry logic"
```

---

### CROSS-REFERENCE NOTE

**Confirmed SPIT Act II visual match.** Texhnolyze's Hopper-influenced concrete noir, prosthetic biomechanics, and industrial brutalism align with SPIT Act II tone requirements. Priority test candidate for cross-bible Lain x Texhnolyze hybrid render.

---

### PRO PRINCIPLE

> The single most powerful move: ask the Grok agent directly:
> "Write me a complete asyncio batch script with seed sweeping, parallel runs, progress bar, output folder organization, and A/B testing between two Texhnolyze variants."
> It will output production-ready, commented code you can run immediately.

---

*Texhnolyze §9 — Corrected v1.1 — STUDIO Reference Library*
