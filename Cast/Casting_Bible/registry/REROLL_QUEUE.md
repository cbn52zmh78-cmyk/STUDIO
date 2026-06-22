# Reroll Queue — Magazine Cast
Generated: 2026-06-19

## Ready for Grok Imagine

---

### ValentinaRossiMag-001 — Valentina Rossi
Status: DIRTY_SWAP_CYCLE
Reason: Dirty plate from batch swap cycle (#125). DO NOT CAST until reroll completes.
Prompt:
photorealistic high-fidelity 16:9 magazine editorial photograph, single 25-year-old Italian woman named Valentina Rossi, striking supermodel beauty with sharp defined cheekbones, captivating dark eyes, flawless porcelain skin, perfect symmetrical features, magnetic presence, wearing asymmetric sculptural black wool coat with metallic petal accents and exaggerated shoulders, elegant confident pose with intense captivating gaze to camera, dramatic cinematic lighting with soft shadows and high contrast highlights on fabric and flawless skin, ultra-detailed textures, sharp focus, Vogue-level professional fashion photography, expensive avant-garde haute couture aesthetic, natural physics dress drape and movement, commercial-ready high-end magazine cover quality, clearly adult woman unambiguously 21+, synthetic fictional character only, no real-person likeness

---

### ZaraKhanMag-001 — Zara Khan
Status: DIRTY_SWAP_CYCLE
Reason: Dirty plate from batch swap cycle (#125). DO NOT CAST until reroll completes.
Prompt:
photorealistic high-fidelity 16:9 magazine editorial photograph, single 26-year-old Indian-British woman named Zara Khan, stunning ethereal beauty with long flowing dark hair, delicate yet powerful features, warm glowing golden skin, intense expressive eyes, flawless proportions, wearing flowing emerald silk gown with dramatic cape sleeves and crystal embellishments, elegant confident pose with intense captivating gaze to camera, dramatic cinematic lighting with soft shadows and high contrast highlights on fabric and flawless skin, ultra-detailed textures, sharp focus, Vogue-level professional fashion photography, expensive avant-garde haute couture aesthetic, natural physics dress drape and movement, commercial-ready high-end magazine cover quality, clearly adult woman unambiguously 21+, synthetic fictional character only, no real-person likeness

---

### LioraVossMag-001 — Liora Voss
Status: DIRTY_SWAP_CYCLE
Reason: Dirty plate from batch swap cycle (#125). DO NOT CAST until reroll completes.
Prompt:
photorealistic high-fidelity 16:9 magazine editorial photograph, single 24-year-old Dutch-German woman named Liora Voss, very attractive willowy supermodel with platinum blonde blunt bob, striking blue eyes, pale flawless porcelain skin, high cheekbones, captivating symmetry, wearing deconstructed white architectural dress with geometric cut-outs and structured pleats, elegant confident pose with intense captivating gaze to camera, dramatic cinematic lighting with soft shadows and high contrast highlights on fabric and flawless skin, ultra-detailed textures, sharp focus, Vogue-level professional fashion photography, expensive avant-garde haute couture aesthetic, natural physics dress drape and movement, commercial-ready high-end magazine cover quality, clearly adult woman unambiguously 21+, synthetic fictional character only, no real-person likeness

---

### SofiaAlvarezMag-001 — Sofia Alvarez
Status: DIRTY_SWAP_CYCLE
Reason: Dirty plate from batch swap cycle (#125). DO NOT CAST until reroll completes.
Prompt:
photorealistic high-fidelity 16:9 magazine editorial photograph, single 27-year-old Brazilian woman named Sofia Alvarez, stunning curvy athletic supermodel with warm tan skin, voluminous curly dark hair, radiant smile, flawless glowing complexion, powerful magnetic presence, wearing vibrant red metallic draped gown with high slit and bold shoulder details, elegant confident pose with intense captivating gaze to camera, dramatic cinematic lighting with soft shadows and high contrast highlights on fabric and flawless skin, ultra-detailed textures, sharp focus, Vogue-level professional fashion photography, expensive avant-garde haute couture aesthetic, natural physics dress drape and movement, commercial-ready high-end magazine cover quality, clearly adult woman unambiguously 21+, synthetic fictional character only, no real-person likeness

---

### NadiaOkoroMag-001 — Nadia Okoro
Status: PLATE_SWAP_BATCH_ERROR
Reason: Freya Lind plate deployed in error during batch deploy (#119). DO NOT CAST until correct plate generated.
Prompt:
photorealistic high-fidelity 16:9 magazine editorial photograph, single 28-year-old Nigerian-French woman named Nadia Okoro, clearly adult woman unambiguously 21+, synthetic fictional character only, no real-person likeness, radiant dark-skinned supermodel with intricate braids and gold threads, high cheekbones, flawless glowing skin, powerful striking presence, perfect symmetry, wearing bold gold and saffron African-inspired avant-garde wrap dress with sculptural sleeves, elegant confident pose with intense captivating gaze to camera, dramatic cinematic lighting with soft shadows and high contrast highlights on fabric and flawless skin, ultra-detailed textures, sharp focus, Vogue-level professional fashion photography, expensive avant-garde haute couture aesthetic, natural physics dress drape and movement, commercial-ready high-end magazine cover quality

---

## Post-Reroll Checklist

After generating each plate at the Grok terminal:
1. Save output to the actor's `01_casting_shots/` folder as `casting_turnaround_v1.jpg`
2. Update `reference_image_primary` in `magazine_casting_registry.json` to the correct path
3. Change `reference_image_status` from `needs_reroll` → `plate_locked`
4. Change `agency_status` from `do_not_cast_pending_reroll` → `development`
5. Remove the compliance flag and `reroll_prompt` field (or archive them)
6. Remove the actor from this queue file
