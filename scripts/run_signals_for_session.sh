#!/bin/bash
# Run paper signals for a single session only.
# Usage: ./scripts/run_signals_for_session.sh <session_id>
# Example: ./scripts/run_signals_for_session.sh pt_17f9c1

set -e
SESSION_ID="${1:?Usage: $0 <session_id>}"
cd "$(dirname "$0")/.."

if [ -f .env ]; then
    export $(grep -v '^#' .env | grep -v '^$' | xargs)
fi

finance/bin/python3 -m api.run_paper_signals --session "$SESSION_ID"
