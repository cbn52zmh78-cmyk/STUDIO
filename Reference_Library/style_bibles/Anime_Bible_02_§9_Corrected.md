# Anime Style Bible 02 — Angel's Egg (1985)
## §9: Advanced Video Production & xAI SDK Integration
**Version:** Corrected v1.1  
**Date:** June 17, 2026  
**Status:** Locked — zero SPIT/GOLDEN bleed

---

### STYLE LOCK

All video output must preserve the film's **ultra-slow surreal painterly atmosphere**, religious symbolism, deep chiaroscuro, egg-like fragility, misty cathedral gloom, and motionless dread.

**Prohibited in this bible:** Bright color blooms, digital glitch, psychedelic saturation, rapid cuts, erotic content, impasto brushwork.

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
1985 Angel's Egg dark surreal painterly animation, lone girl in tattered cloak cradling glowing 
egg under endless rainy cathedral spires, soft wet oil-paint textures, deep indigo and amber 
chiaroscuro, religious melancholy, almost static dreamlike drift with faint wind ripples, heavy 
atmosphere, cinematic masterpiece, 8-second subtle motion, grok-imagine-video
```

---

### WORKFLOW MODES

**1. One-Shot Headless (rapid ideation)**
```bash
grok -p "Generate an 8-second Angel's Egg style video: [full descriptive prompt] with exact Angel's Egg directives"
```

**2. Interactive TUI (compare / iterate)**
```bash
grok
```
Inside TUI:
- Activate Plan Mode: `Shift+Tab` or `/plan`
- Paste Angel's Egg bible directives
- Use `/fork variantA` / `/fork variantB` to branch
- Compare outputs side-by-side with natural language refinement

**3. Batch / Production Scale (agent builds the script)**
```bash
grok -p "Write a Python asyncio batch script that generates 6 Angel's Egg style variations using xAI API, saves to ./tests/angels_egg/, produces a JSON comparison report, and includes tqdm progress bar with error retry logic"
```

---

### PRO PRINCIPLE

> The single most powerful move: ask the Grok agent directly:
> "Write me a complete asyncio batch script with seed sweeping, parallel runs, progress bar, output folder organization, and A/B testing between two Angel's Egg variants."
> It will output production-ready, commented code you can run immediately.

---

*Angel's Egg §9 — Corrected v1.1 — STUDIO Reference Library*
