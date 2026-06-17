# Anime Style Bible 03 — Serial Experiments Lain (1998)
## §9: Advanced Video Production & xAI SDK Integration
**Version:** Corrected v1.1  
**Date:** June 17, 2026  
**Status:** Locked — zero SPIT/GOLDEN bleed

---

### STYLE LOCK

All video output must replicate the series' **glitch-cyber minimalism**, wireframe overlays, static interference, psychological dissociation, low-res CRT feel, and haunting digital loneliness.

**Prohibited in this bible:** Watercolor washes, painterly softness, warm palettes, saturated blooms, religious symbolism, erotic content.

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
1998 Serial Experiments Lain glitch cyber minimal animation, pale girl with straight black hair 
standing in empty wired room, CRT scanlines and digital noise flickering, floating wireframe bears 
and "Present day, present time" text overlay, cold blue monochrome palette, psychological 
dissociation, static camera with subtle frame jitter, haunting atmosphere, 8-second motion, 
grok-imagine-video
```

---

### WORKFLOW MODES

**1. One-Shot Headless (rapid ideation)**
```bash
grok -p "Generate an 8-second Serial Experiments Lain style video: [full descriptive prompt] with exact Lain directives"
```

**2. Interactive TUI (compare / iterate)**
```bash
grok
```
Inside TUI:
- Activate Plan Mode: `Shift+Tab` or `/plan`
- Paste Lain bible directives
- Use `/fork variantA` / `/fork variantB` to branch
- Compare outputs side-by-side with natural language refinement

**3. Batch / Production Scale (agent builds the script)**
```bash
grok -p "Write a Python asyncio batch script that generates 6 Serial Experiments Lain style variations using xAI API, saves to ./tests/lain/, produces a JSON comparison report, and includes tqdm progress bar with error retry logic"
```

---

### CROSS-REFERENCE NOTE

This bible has confirmed visual alignment with SPIT Act II aesthetic (suburban void, digital alienation, isolation). See STUDIO Canon for cross-bible integration rules.

---

### PRO PRINCIPLE

> The single most powerful move: ask the Grok agent directly:
> "Write me a complete asyncio batch script with seed sweeping, parallel runs, progress bar, output folder organization, and A/B testing between two Lain variants."
> It will output production-ready, commented code you can run immediately.

---

*Serial Experiments Lain §9 — Corrected v1.1 — STUDIO Reference Library*
