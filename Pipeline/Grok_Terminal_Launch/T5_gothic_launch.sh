#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# T5 — david_gothic_corpus_v1 — "A Language Saved by One Bible"
# Resolution: 854x480  (test render — seamless transitions v2)
# Estimated: ~8 min at 480p  |  8 shots × 12s = 96s runtime
# Transition: dissolve @ 1.8s xfade  (was 0.2s abrupt cuts)
# ─────────────────────────────────────────────────────────────────────────────
set -e

GROK_ROOT="C:\Users\NCG\Videos\Grok Projects"
cd "$GROK_ROOT"

echo "[T5] Staging david_gothic_corpus_v1 for render..."
python3 STUDIO/Pipeline/batch_runner.py \
    --slate dead_languages \
    --episode david_gothic_corpus_v1

echo ""
echo "[T5] Gothic render queued."
echo "     Output: DAVID/productions/david_gothic_corpus_v1_longform_v1/"
echo "     When done, run T6_COMMIT_after_render.sh from the COMMIT terminal."
