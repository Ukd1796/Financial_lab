#!/bin/zsh
# Wait for the integrated fetch to finish, then run the backwards extension.
#
# Sequenced rather than parallel: both hit the same NSE endpoints and the same
# SQLite file, and the whole run is paced by a deliberate 1.5s inter-request
# delay -- running two at once would double the request rate against an
# exchange that has already shown it will stall a session.
#
# Every stage is resumable, so an interruption at any point costs elapsed time
# and nothing else. Re-run this script and it picks up where it stopped.
#
# Usage:  scripts/event_research/run_overnight_chain.sh
set -u
cd "$(dirname "$0")/../.."
LOG=data/event_research/chain_$(date +%Y%m%d_%H%M%S).log

echo "=== Chain started $(date) ===" | tee -a "$LOG"

# 1. Wait out the integrated fetch if one is running.
while pgrep -f "scripts.event_research.fetch_cohort_integrated_filings" > /dev/null; do
  echo "  $(date +%H:%M) waiting for the integrated fetch ..." | tee -a "$LOG"
  sleep 300
done
echo "  integrated fetch is not running; continuing" | tee -a "$LOG"

# 2. Fetch the year-ago comparatives fold A needs.
echo "\n=== Stage 2: backwards extension ===" | tee -a "$LOG"
scripts/event_research/extend_backwards.sh --commit 2>&1 | tee -a "$LOG"

# 3. Re-parse the whole corpus under ONE rule.
#    Doing this after all fetching, never during, so the corpus is never half
#    parsed under two conventions -- facts are re-derived from the immutable
#    raw documents, which is what `parser_version` exists for.
echo "\n=== Stage 3: re-parse with convention recovery ===" | tee -a "$LOG"
caffeinate -dimsu finance/bin/python3 -u -m scripts.event_research.reparse_corpus \
    --resolve-conventions --commit 2>&1 | tee -a "$LOG"

# 4. Rebuild features and report the funnel. Signal-blind: no fold verdict here.
echo "\n=== Stage 4: rebuild event features ===" | tee -a "$LOG"
caffeinate -dimsu finance/bin/python3 -u -m scripts.event_research.build_event_features \
    --commit 2>&1 | tee -a "$LOG"

echo "\n=== Chain finished $(date) ===" | tee -a "$LOG"
echo "Next, by hand: finance/bin/python3 -m scripts.event_research.run_fold --fold A" | tee -a "$LOG"
