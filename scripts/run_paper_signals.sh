#!/bin/bash
# Cron wrapper for api/run_paper_signals.py
# Cron: 35 10 * * 1-5  (16:05 IST on weekdays — EOD signal generation)
# Example cron line:
#   35 10 * * 1-5 /Users/ujjwalkumar/Financial_lab/scripts/run_paper_signals.sh >> /Users/ujjwalkumar/Financial_lab/logs/paper_signals.log 2>&1

set -e
cd /Users/ujjwalkumar/Financial_lab

if [ -f .env ]; then
    export $(grep -v '^#' .env | grep -v '^$' | xargs)
fi

/Users/ujjwalkumar/Financial_lab/finance/bin/python3 -m api.run_paper_signals
