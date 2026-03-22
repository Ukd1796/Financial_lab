#!/bin/bash
# Cron wrapper for run_orders.py
# Cron: 45 3 * * 1-5  (9:15 AM IST on weekdays)
# Example cron line:
#   45 3 * * 1-5 /Users/ujjwalkumar/Financial_lab/scripts/run_orders.sh >> /Users/ujjwalkumar/Financial_lab/logs/orders.log 2>&1

set -e
cd /Users/ujjwalkumar/Financial_lab

# Load environment variables
if [ -f .env ]; then
    export $(grep -v '^#' .env | grep -v '^$' | xargs)
fi

/Users/ujjwalkumar/Financial_lab/finance/bin/python3 run_orders.py
