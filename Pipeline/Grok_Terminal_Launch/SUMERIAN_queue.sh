#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# Ep 6 — david_sumerian_corpus_v1 — "The First Written Language"
# Resolution: 854x480  (test render — seamless transitions v2)
# Queue this on WHICHEVER T1–T5 terminal finishes first.
# Estimated: ~8 min at 480p  |  8 shots × 12s = 96s runtime
# Transition: dissolve @ 1.8s xfade
# ─────────────────────────────────────────────────────────────────────────────
set -e

GROK_ROOT="C:\Users\NCG\Videos\Grok Projects"
cd "$GROK_ROOT"

echo "[SUMERIAN] Staging david_sumerian_corpus_v1 for render..."
python3 STUDIO/Pipeline/batch_runner.py \
    --slate dead_languages \
    --episode david_sumerian_corpus_v1

echo ""
echo "[SUMERIAN] Sumerian render queued."
echo "     Output: DAVID/productions/david_sumerian_corpus_v1_longform_v1/"
echo "     When done, this terminal is free. Notify COMMIT terminal to finalize."
