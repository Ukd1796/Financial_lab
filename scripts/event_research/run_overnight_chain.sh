#!/bin/zsh
# Wait for the integrated fetch to finish, then run the backwards extension,
# the re-parse and the feature rebuild.
#
# Sequenced rather than parallel: both hit the same NSE endpoints and the same
# SQLite file, and the whole run is paced by a deliberate 1.5s inter-request
# delay -- running two at once would double the request rate against an
# exchange that has already shown it will stall a session.
#
# Every stage is resumable, so an interruption at any point costs elapsed time
# and nothing else. Re-run this script and it picks up where it stopped.
#
# THREE HARDENINGS, all earned on 2026-08-18 when this script reported no error
# and produced nothing:
#
#   1. `pgrep` failing is not `pgrep` finding nothing.  It exits 1 when there is
#      no match but >=2 on error, and a suspended machine returns "Cannot get
#      process list".  The old `while pgrep ...` read that error as "the fetch
#      has finished" and marched into stage 2 while stage 1 was still running.
#   2. A failed stage no longer cascades.  Stages 3 and 4 derive facts and
#      features from whatever the fetch stages left behind; running them on a
#      corpus that failed to load produces a clean-looking empty result, which
#      is worse than an error.
#   3. A fetch stage that ingests zero new filings aborts the chain.  That is
#      not a no-op -- it is the exact shape of the defect that rejected all
#      3,127 filings of the 2025+ era while logging a plausible-sounding
#      reason for each one (fixed 2026-08-22).  Silence is the thing to catch.
#
# Usage:  scripts/event_research/run_overnight_chain.sh
set -u
cd "$(dirname "$0")/../.."

LOG=data/event_research/chain_$(date +%Y%m%d_%H%M%S).log
DB=data/event_research/event_research.sqlite

log() { echo "$@" | tee -a "$LOG" }

# Filings currently in the corpus.  Printed bare so it can be compared; any
# failure to read the DB returns empty and is treated as unknown, not as zero.
filing_count() {
  finance/bin/python3 - "$DB" <<'PY' 2>/dev/null
import sqlite3, sys
try:
    db = sqlite3.connect(sys.argv[1])
    print(db.execute("SELECT COUNT(*) FROM financial_result_events").fetchone()[0])
except Exception:
    pass
PY
}

# Run one stage, tee it, and stop the chain if it failed.  `pipestatus[1]` is
# the command's own status -- `$?` after a pipe is tee's, which is always 0.
run_stage() {
  local name="$1"; shift
  log "\n=== $name ==="
  "$@" 2>&1 | tee -a "$LOG"
  local rc=${pipestatus[1]}
  if [[ $rc -ne 0 ]]; then
    log "\n!! $name FAILED (exit $rc). Chain stopped here."
    log "   Nothing downstream has run, so the corpus is not half-built."
    log "   Fix, then re-run this script -- every stage resumes."
    exit 1
  fi
}

# A fetch stage must have added something.  Zero is not success.
assert_corpus_grew() {
  local name="$1" before="$2" after="$3"
  if [[ -z "$before" || -z "$after" ]]; then
    log "   (corpus size unreadable; skipping the zero-ingest check)"
    return 0
  fi
  log "   corpus: $before -> $after filings (+$((after - before)))"
  if [[ "$after" -le "$before" ]]; then
    log "\n!! $name ingested NOTHING. Chain stopped here."
    log "   A fetch that reports success and stores nothing is a silent"
    log "   rejection, not an empty window. Check the exception table:"
    log "     SELECT exception_type, COUNT(*) FROM event_data_exceptions"
    log "     WHERE created_at >= date('now') GROUP BY 1;"
    exit 1
  fi
}

log "=== Chain started $(date) ==="
log "  log:  $LOG"
log "  base: $(filing_count) filings in the corpus"

# ---------------------------------------------------------------------------
# 1. Wait out an integrated fetch if one is already running.
# ---------------------------------------------------------------------------
# If one IS running we own its outcome: a fetch that stops is not a fetch that
# worked, and stages 2-4 would otherwise build features on top of whatever it
# failed to store.  Only checked when we actually waited -- if no fetch was
# running there is no delta to expect.
PATTERN="scripts.event_research.fetch_cohort_integrated_filings"
WAITED=0
STAGE1_BEFORE=$(filing_count)
while true; do
  pgrep -f "$PATTERN" > /dev/null
  PGREP_STATUS=$?
  case $PGREP_STATUS in
    0) WAITED=1; log "  $(date +%H:%M) waiting for the integrated fetch ..."; sleep 300 ;;
    1) log "  integrated fetch is not running; continuing"; break ;;
    *) log "\n!! pgrep could not read the process list (exit $PGREP_STATUS)."
       log "   That is a broken machine, not an absent process -- most likely"
       log "   the host suspended. Refusing to assume the fetch finished."
       exit 1 ;;
  esac
done

if [[ $WAITED -eq 1 ]]; then
  log "\n=== Stage 1: integrated fetch (waited out) ==="
  assert_corpus_grew "Stage 1 (integrated fetch)" "$STAGE1_BEFORE" "$(filing_count)"
fi

# ---------------------------------------------------------------------------
# 2. Fetch the year-ago comparatives fold A needs.
# ---------------------------------------------------------------------------
BEFORE=$(filing_count)
run_stage "Stage 2: backwards extension" \
    scripts/event_research/extend_backwards.sh --commit
assert_corpus_grew "Stage 2" "$BEFORE" "$(filing_count)"

# ---------------------------------------------------------------------------
# 3. Re-parse the whole corpus under ONE rule.
#    After all fetching, never during, so the corpus is never half parsed under
#    two conventions -- facts are re-derived from the immutable raw documents,
#    which is what `parser_version` exists for.
# ---------------------------------------------------------------------------
run_stage "Stage 3: re-parse with convention recovery" \
    caffeinate -dimsu finance/bin/python3 -u -m scripts.event_research.reparse_corpus \
    --resolve-conventions --commit

# ---------------------------------------------------------------------------
# 4. Rebuild features and report the funnel. Signal-blind: no fold verdict here.
# ---------------------------------------------------------------------------
run_stage "Stage 4: rebuild event features" \
    caffeinate -dimsu finance/bin/python3 -u -m scripts.event_research.build_event_features \
    --commit

log "\n=== Chain finished $(date) ==="
log "  corpus: $(filing_count) filings"
log "Next, by hand: finance/bin/python3 -m scripts.event_research.run_fold --fold A"
