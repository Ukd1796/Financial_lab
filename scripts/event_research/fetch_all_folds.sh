#!/bin/zsh
# Fetch every rolled-cohort filing across folds A, B and C in one pass.
#
# Two source eras, because the legacy result index stops carrying bulk filings
# after ~Feb 2025 and the Integrated Filing endpoint takes over.  The windows
# overlap deliberately: a duplicate source_sha256 is a no-op in
# import_validated_filing, so an overlap costs a redundant download and buys
# certainty that nothing falls between the two eras.
#
# Fetching is signal-blind -- it reads no price and computes no return -- so
# pulling folds B and C now costs none of the pre-registration.  Charter v3 §7
# gates *evaluation*, not ingestion.
#
# Resumable: each fetcher skips filings whose source URL is already ingested,
# so an interrupted run is restarted by re-issuing the same command.  This run
# takes hours, and on 2026-08-17 a closed lid suspended it for most of a day --
# the work was not lost, it simply did not advance while the machine slept.
#
# NOTE: `caffeinate -dimsu` prevents idle and display sleep, but macOS still
# sleeps on lid close unless the machine is in clamshell mode (external display
# + power). Leave the lid OPEN for the duration, or just re-run afterwards --
# resume makes that cheap.
#
# Usage:  scripts/event_research/fetch_all_folds.sh [--commit]
set -u
cd "$(dirname "$0")/../.."

COMMIT="${1:-}"
# An array, not a string: zsh does not word-split an unquoted parameter, so
# PY="caffeinate ... python3" would be looked up as a single command name.
# -u so a crash lands in the log where it happened: block-buffered stdout
# scrambled a traceback into the middle of an unrelated line on 2026-08-18.
PY=(caffeinate -dimsu finance/bin/python3 -u)
FAILURES=0
LOG=data/event_research/fetch_$(date +%Y%m%d_%H%M%S).log

COHORTS=(
  liquid-2023-06-30 liquid-2023-09-30 liquid-2023-12-31 liquid-2024-03-31
  liquid-2024-06-30 liquid-2024-09-30 liquid-2024-12-31 liquid-2025-03-31
  liquid-2025-06-30 liquid-2025-09-30 liquid-2025-12-31 liquid-2026-03-31
  liquid-2026-06-30
)

# Quarterly windows keep each legacy index request small and make the run
# resumable: a window that fails can be re-run without repeating the rest.
LEGACY_WINDOWS=(
  "2023-06-01 2023-09-30" "2023-10-01 2023-12-31"
  "2024-01-01 2024-03-31" "2024-04-01 2024-06-30"
  "2024-07-01 2024-09-30" "2024-10-01 2024-12-31"
  "2025-01-01 2025-03-31"
)

echo "=== Fetch started $(date) ===" | tee -a "$LOG"

for window in "${LEGACY_WINDOWS[@]}"; do
  from="${window%% *}"; to="${window##* }"
  echo "\n--- legacy index $from .. $to ---" | tee -a "$LOG"
  "${PY[@]}" -m scripts.event_research.fetch_cohort_filings \
      --cohort-id "${COHORTS[@]}" --from "$from" --to "$to" $COMMIT 2>&1 | tee -a "$LOG"
  # A pipe through tee reports tee's status, so read the producer's explicitly.
  # Without this the script exited 0 while every single step had failed.
  if [[ ${pipestatus[1]} -ne 0 ]]; then
    echo "  !! window $from .. $to FAILED (exit ${pipestatus[1]})" | tee -a "$LOG"
    FAILURES=$((FAILURES + 1))
  fi
done

echo "\n--- integrated filings 2025-01-01 .. 2026-08-14 ---" | tee -a "$LOG"
"${PY[@]}" -m scripts.event_research.fetch_cohort_integrated_filings \
    --cohort-id "${COHORTS[@]}" --from 2025-01-01 --to 2026-08-14 $COMMIT 2>&1 | tee -a "$LOG"
if [[ ${pipestatus[1]} -ne 0 ]]; then
  echo "  !! integrated fetch FAILED (exit ${pipestatus[1]})" | tee -a "$LOG"
  FAILURES=$((FAILURES + 1))
fi

echo "\n=== Fetch finished $(date), $FAILURES failed step(s) ===" | tee -a "$LOG"
exit $((FAILURES > 0))
