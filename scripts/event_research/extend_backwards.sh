#!/bin/zsh
# Fetch the year-ago comparatives fold A needs, then rebuild and report.
#
# WHY THIS EXISTS
# ---------------
# A seasonal surprise needs TWO filings: the quarter, and the same quarter one
# year earlier.  The main fetch starts at 2023-06-01, so every fold-A quarter
# before mid-2024 has no comparative and cannot be chained.  Measured
# 2026-08-18: only 2 of fold A's 6 quarters are chainable, against charter v3
# §4's floor of 4.  Fold A therefore returns INCONCLUSIVE-on-sufficiency before
# a single return is computed -- not because the hypothesis is weak, but
# because the download window starts twelve months too late.
#
# This fetches dissemination windows 2022-07-01 .. 2023-05-31, which carry the
# reported quarters 2022-06-30 through 2023-03-31 -- exactly the four
# comparatives that are missing.
#
# NO PRICE BACKFILL IS NEEDED.  A year-ago filing contributes only an EPS
# number (`build_event_features.py` reads `prior["eps"]` and nothing else);
# prices are fetched only for the current event.  The price panel starting
# 2023-03-15 is therefore not a constraint here.
#
# Those filings sit in the broken-XBRL era, so they are re-parsed with
# `--resolve-conventions`, which proves the OneD/FourD convention from each
# document's own values rather than assuming it.  Recovered filings carry the
# distinct status RECOVERED_CONVENTION so any result can be re-run without them.
#
# Usage:  scripts/event_research/extend_backwards.sh [--commit]
set -u
cd "$(dirname "$0")/../.."

COMMIT="${1:-}"
PY=(caffeinate -dimsu finance/bin/python3 -u)
LOG=data/event_research/extend_$(date +%Y%m%d_%H%M%S).log
FAILURES=0

COHORTS=(
  liquid-2023-06-30 liquid-2023-09-30 liquid-2023-12-31 liquid-2024-03-31
  liquid-2024-06-30 liquid-2024-09-30 liquid-2024-12-31 liquid-2025-03-31
  liquid-2025-06-30 liquid-2025-09-30 liquid-2025-12-31 liquid-2026-03-31
  liquid-2026-06-30
)

# One window per reporting season, so a failure costs one window not the run.
WINDOWS=(
  "2022-07-01 2022-09-30"   # reports quarter ending 2022-06-30
  "2022-10-01 2022-12-31"   # ... 2022-09-30
  "2023-01-01 2023-03-31"   # ... 2022-12-31
  "2023-04-01 2023-05-31"   # ... 2023-03-31
)

echo "=== Backwards extension started $(date) ===" | tee -a "$LOG"

for window in "${WINDOWS[@]}"; do
  from="${window%% *}"; to="${window##* }"
  echo "\n--- legacy index $from .. $to ---" | tee -a "$LOG"
  "${PY[@]}" -m scripts.event_research.fetch_cohort_filings \
      --cohort-id "${COHORTS[@]}" --from "$from" --to "$to" $COMMIT 2>&1 | tee -a "$LOG"
  if [[ ${pipestatus[1]} -ne 0 ]]; then
    echo "  !! window $from .. $to FAILED (exit ${pipestatus[1]})" | tee -a "$LOG"
    FAILURES=$((FAILURES + 1))
  fi
done

echo "\n=== Backwards extension finished $(date), $FAILURES failed step(s) ===" | tee -a "$LOG"
exit $((FAILURES > 0))
