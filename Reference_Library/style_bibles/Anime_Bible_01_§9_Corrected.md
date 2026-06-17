# Anime Style Bible 01 — Belladonna of Sadness (1973)
## §9: Advanced Video Production & xAI SDK Integration
**Version:** Corrected v1.1  
**Date:** June 17, 2026  
**Status:** Locked — zero SPIT/GOLDEN bleed

---

### STYLE LOCK

All video output must honor the film's **psychedelic watercolor-burst animation**, fluid linework, Art Nouveau hair and flowing silhouettes, explosive color blooms, hand-painted texture, and erotic-dreamlike pacing.

**Prohibited in this bible:** Oil impasto, Carcosa yellow, heavy brushwork, desaturated palettes, digital glitch effects, concrete aesthetics.

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
1973 Belladonna of Sadness watercolor burst animation, fluid hand-drawn lines explode into 
radiant color blooms, Art Nouveau flowing hair and naked silhouette of Jeanne rising in 
ecstatic torment, swirling gold and crimson ink washes, psychedelic light rays shattering 
across the frame, erotic surreal dream sequence, extreme emotional distortion, masterpiece 
frame, 8-second seamless motion, grok-imagine-video
```

---

### WORKFLOW MODES

**1. One-Shot Headless (rapid ideation)**
```bash
grok -p "Generate an 8-second Belladonna of Sadness style video: [full descriptive prompt] with exact Belladonna directives"
```

**2. Interactive TUI (compare / iterate)**
```bash
grok
```
Inside TUI:
- Activate Plan Mode: `Shift+Tab` or `/plan`
- Paste Belladonna bible directives
- Use `/fork variantA` / `/fork variantB` to branch
- Compare outputs side-by-side with natural language refinement

**3. Batch / Production Scale (agent builds the script)**
```bash
grok -p "Write a Python asyncio batch script that generates 6 Belladonna of Sadness style variations using xAI API, saves to ./tests/belladonna/, produces a JSON comparison report, and includes tqdm progress bar with error retry logic"
```

---

### PRO PRINCIPLE

> The single most powerful move: ask the Grok agent directly:
> "Write me a complete asyncio batch script with seed sweeping, parallel runs, progress bar, output folder organization, and A/B testing between two Belladonna variants."
> It will output production-ready, commented code you can run immediately.

---

*Belladonna of Sadness §9 — Corrected v1.1 — STUDIO Reference Library*
