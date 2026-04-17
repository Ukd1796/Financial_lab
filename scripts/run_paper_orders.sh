#!/bin/bash
# Cron wrapper for api/run_paper_orders.py
# Cron: 45 10 * * 1-5  (16:15 IST on weekdays — EOD order fills)
# Example cron line:
#   45 10 * * 1-5 /Users/ujjwalkumar/Financial_lab/scripts/run_paper_orders.sh >> /Users/ujjwalkumar/Financial_lab/logs/paper_orders.log 2>&1

set -e
cd /Users/ujjwalkumar/Financial_lab

if [ -f .env ]; then
    export $(grep -v '^#' .env | grep -v '^$' | xargs)
fi

/Users/ujjwalkumar/Financial_lab/finance/bin/python3 -m api.run_paper_orders
