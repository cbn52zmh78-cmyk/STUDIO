# Anime Style Bible 05 — Mind Game (2004, Masaaki Yuasa)
## §9: Advanced Video Production & xAI SDK Integration
**Version:** Corrected v1.1  
**Date:** June 17, 2026  
**Status:** Locked — zero SPIT/GOLDEN bleed

---

### STYLE LOCK

All output must capture the film's **chaotic fluid animation**, rapid style shifts, abstract psychedelic bursts, exaggerated expressions, and wild narrative energy. Pure kinetic freedom.

**Prohibited in this bible:** Slow pacing, monochrome palettes, static camera, realistic proportions held for more than a beat, painterly stillness.

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
2004 Mind Game chaotic abstract animation, wild-eyed protagonist transforming mid-leap through 
exploding manga panels and fluid ink rivers, rapid style shifts from realistic to super-deformed 
to psychedelic vortex, vibrant clashing colors, exaggerated motion lines and speed streaks, pure 
kinetic insanity, masterpiece frame, 8-second explosive sequence, grok-imagine-video
```

---

### WORKFLOW MODES

**1. One-Shot Headless (rapid ideation)**
```bash
grok -p "Generate an 8-second Mind Game / Masaaki Yuasa style video: [full descriptive prompt] with exact Mind Game directives"
```

**2. Interactive TUI (compare / iterate)**
```bash
grok
```
Inside TUI:
- Activate Plan Mode: `Shift+Tab` or `/plan`
- Paste Mind Game bible directives
- Use `/fork variantA` / `/fork variantB` to branch
- Compare outputs side-by-side with natural language refinement

**3. Batch / Production Scale (agent builds the script)**
```bash
grok -p "Write a Python asyncio batch script that generates 6 Mind Game style variations using xAI API, saves to ./tests/mind_game/, produces a JSON comparison report, and includes tqdm progress bar with error retry logic"
```

---

### PRO PRINCIPLE

> The single most powerful move: ask the Grok agent directly:
> "Write me a complete asyncio batch script with seed sweeping, parallel runs, progress bar, output folder organization, and A/B testing between two Mind Game variants."
> It will output production-ready, commented code you can run immediately.

---

*Mind Game §9 — Corrected v1.1 — STUDIO Reference Library*
