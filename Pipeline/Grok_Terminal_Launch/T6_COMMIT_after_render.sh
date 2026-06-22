#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# COMMIT terminal — run AFTER all T1–T5 (+ SUMERIAN) renders complete.
#
# Steps:
#   1. Package all completed episodes
#   2. Run Gate 0 verification (must be 27/27 GREEN)
#   3. Git status — OPERATOR REVIEWS before committing
#   4. Git add + commit
#
# DO NOT push without operator sign-off on the render review.
# ─────────────────────────────────────────────────────────────────────────────
set -e

GROK_ROOT="C:\Users\NCG\Videos\Grok Projects"
cd "$GROK_ROOT"

echo "============================================================"
echo "  COMMIT terminal — post-render packaging + verification"
echo "============================================================"

# Step 1: Package all completed episodes
echo ""
echo "[COMMIT 1/4] Packaging completed episodes..."
python3 STUDIO/Pipeline/batch_runner.py --slate dead_languages --package

# Step 2: Gate 0 verification
echo ""
echo "[COMMIT 2/4] Running Gate 0 verification..."
python3 STUDIO/Pipeline/verify_gate_0.py

# Step 3: Git status for operator review
echo ""
echo "[COMMIT 3/4] Git status — REVIEW BEFORE PROCEEDING:"
echo "------------------------------------------------------------"
git status
echo "------------------------------------------------------------"
echo ""
echo "  Review the diff above."
echo "  Type Ctrl-C to abort if anything looks wrong."
echo "  Press Enter to continue with git add + commit..."
read -r

# Step 4: Commit
echo ""
echo "[COMMIT 4/4] Committing..."
git add -A
git commit -m "chore: 480p test renders — launch 6 dead-language eps — seamless transitions v2

- xfade: 0.2s -> 1.8s (dissolve, documentary standard)
- shot duration: 7-9s -> 12s per shot (96s total runtime)
- resolution: 854x480 (test render mode)
- motion_carry + continuity cues added to all video prompts
- consume_ai_handoff.py: RENDER_RESOLUTION constant, min 12s floor
- shot_duration.py: SEAMLESS_LO=12, SEAMLESS_HI=18
- Production_Templates_v1.json: seamless_defaults updated"

echo ""
echo "[COMMIT] Done. Review above and push when ready:"
echo "  git push"
