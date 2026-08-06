#!/usr/bin/env python3
"""
Replay this branch's backtest over the LIVE paper-trading window using the
exact Ujjwal's Portfolio config, to compare against the live paper result.

Reuses run_ujjwal_baseline.py wholesale (same universe, same risk config,
same atr_multiplier=2.5) and only overrides the period to the live window.

Usage:
  PYTHONHASHSEED=0 finance/bin/python3 scripts/run_paper_window.py            # EqW + Adaptive
  PYTHONHASHSEED=0 finance/bin/python3 scripts/run_paper_window.py --eqw      # EqW only (fast)
"""
import sys
from datetime import datetime

import os
import run_ujjwal_baseline as rb

# The live paper period both portfolios traded (see docs/portfolio_analysis_system_diagnosis.md)
rb.PERIODS = {
    "Paper 2026-04-07-07-07": (datetime(2026, 4, 7), datetime(2026, 7, 7)),
}

# Optional risk-profile overrides so the same runner can replay either live
# profile faithfully. Defaults = Ujjwal's Portfolio (10% / 35%).
#   MAX_POS=0.25 PAUSE=0.60  -> Shubham1 profile
if os.environ.get("MAX_POS"):
    rb.MAX_POSITION_PCT = float(os.environ["MAX_POS"])
if os.environ.get("PAUSE"):
    rb.MAX_DOWNTREND_PCT = float(os.environ["PAUSE"])

if __name__ == "__main__":
    eqw_only = "--eqw" in sys.argv
    print(f"  Profile risk: max_pos={rb.MAX_POSITION_PCT:.2f}  CB_pause={rb.MAX_DOWNTREND_PCT:.2f}")
    rb.run_baseline(equal_weight_only=eqw_only)
