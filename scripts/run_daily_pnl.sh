#!/bin/bash
# Cron wrapper for api/run_daily_pnl.py
# Cron: 15 10 * * 1-5  (15:45 IST on weekdays — daily P&L summary push)
# Example cron line:
#   15 10 * * 1-5 /Users/ujjwalkumar/Financial_lab/scripts/run_daily_pnl.sh >> /Users/ujjwalkumar/Financial_lab/logs/daily_pnl.log 2>&1

set -e
cd /Users/ujjwalkumar/Financial_lab

if [ -f .env ]; then
    export $(grep -v '^#' .env | grep -v '^$' | xargs)
fi

/Users/ujjwalkumar/Financial_lab/finance/bin/python3 -m api.run_daily_pnl
