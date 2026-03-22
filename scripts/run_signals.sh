#!/bin/bash
# Cron wrapper for run_signals.py
# Cron: 5 10 * * 1-5  (3:35 PM IST on weekdays)
# Example cron line:
#   5 10 * * 1-5 /Users/ujjwalkumar/Financial_lab/scripts/run_signals.sh >> /Users/ujjwalkumar/Financial_lab/logs/signals.log 2>&1

set -e
cd /Users/ujjwalkumar/Financial_lab

# Load environment variables
if [ -f .env ]; then
    export $(grep -v '^#' .env | grep -v '^$' | xargs)
fi

/Users/ujjwalkumar/Financial_lab/finance/bin/python3 run_signals.py
