#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# T1 — david_latin_corpus_v1 — "Why Latin Never Really Died"
# Resolution: 854x480  (test render — seamless transitions v2)
# Estimated: ~8 min at 480p  |  8 shots × 12s = 96s runtime
# Transition: dissolve @ 1.8s xfade  (was 0.2s abrupt cuts)
# ─────────────────────────────────────────────────────────────────────────────
set -e

GROK_ROOT="C:\Users\NCG\Videos\Grok Projects"
cd "$GROK_ROOT"

echo "[T1] Staging david_latin_corpus_v1 for render..."
python3 STUDIO/Pipeline/batch_runner.py \
    --slate dead_languages \
    --episode david_latin_corpus_v1

echo ""
echo "[T1] Latin render queued."
echo "     Output: DAVID/productions/david_latin_corpus_v1_longform_v1/"
echo "     When done, run T6_COMMIT_after_render.sh from the COMMIT terminal."
