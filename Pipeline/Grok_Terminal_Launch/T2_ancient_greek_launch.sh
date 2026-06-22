#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# T2 — david_ancient_greek_corpus_v1 — "Restoring the Pitch Accent"
# Resolution: 854x480  (test render — seamless transitions v2)
# Estimated: ~8 min at 480p  |  8 shots × 12s = 96s runtime
# Transition: dissolve @ 1.8s xfade  (was 0.2s abrupt cuts)
# ─────────────────────────────────────────────────────────────────────────────
set -e

GROK_ROOT="C:\Users\NCG\Videos\Grok Projects"
cd "$GROK_ROOT"

echo "[T2] Staging david_ancient_greek_corpus_v1 for render..."
python3 STUDIO/Pipeline/batch_runner.py \
    --slate dead_languages \
    --episode david_ancient_greek_corpus_v1

echo ""
echo "[T2] Ancient Greek render queued."
echo "     Output: DAVID/productions/david_ancient_greek_corpus_v1_longform_v1/"
echo "     When done, run T6_COMMIT_after_render.sh from the COMMIT terminal."
