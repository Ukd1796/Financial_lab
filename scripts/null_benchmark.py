"""
Null benchmark: equal-weight buy-and-hold of the traded universe vs. the system,
per period. If a passive hold beats the active machinery, the edge is not in the
machinery. Read-only — no engine, no strategies.
"""
from dotenv import load_dotenv
load_dotenv()

from app.data.repository import MarketDataRepository
from run_ujjwal_baseline import BROAD_UNIVERSE, PERIODS, NIFTY_50

repo = MarketDataRepository()

# System EqW returns (activity baseline, from the deterministic A/B already run).
SYS = {"Bull  2019–2020": -2.09, "Crash 2020": 19.57, "Recov 2020–2021": 49.57,
       "Bear  2022": 1.00, "Recent2022–2024": 21.83, "Live  2025–2026": -2.73}


import math
import pandas as pd

# System risk stats (activity baseline): (Sharpe, MaxDD%) from the A/B run.
SYS_RISK = {"Bull  2019–2020": (-0.37, 5.66), "Crash 2020": (2.21, 4.56),
            "Recov 2020–2021": (2.77, 5.02), "Bear  2022": (0.20, 5.95),
            "Recent2022–2024": (1.25, 5.95), "Live  2025–2026": (-0.57, 3.71)}


def bh_stats(symbols, start, end):
    """Equal-weight buy&hold total return + a daily EW-index Sharpe & MaxDD."""
    data = repo.get_ohlc_bulk(symbols, start, end)
    series = {}
    for s, recs in data.items():
        recs = [r for r in recs if start <= r.timestamp <= end]
        if len(recs) < 2:
            continue
        recs.sort(key=lambda r: r.timestamp)
        c0 = recs[0].close
        if not c0 or c0 <= 0:
            continue
        series[s] = pd.Series({r.timestamp: r.close / c0 for r in recs})  # normalized
    if not series:
        return None, 0, None, None
    idx = pd.DataFrame(series).sort_index().ffill()          # daily EW price index
    ew = idx.mean(axis=1)
    total_ret = 100 * (ew.iloc[-1] - 1)
    daily = ew.pct_change().dropna()
    sharpe = (daily.mean() / daily.std() * math.sqrt(252)) if daily.std() > 0 else 0.0
    maxdd = 100 * (1 - (ew / ew.cummax())).max()
    return total_ret, len(series), sharpe, maxdd


hdr = (f"{'Period':<17}{'Sys%':>7}{'SysShrp':>8}{'SysDD':>7}   "
       f"{'B&H%':>8}{'BHShrp':>8}{'BHDD':>7}{'Capture':>9}")
print(hdr)
print("-" * len(hdr))
for label, (s, e) in PERIODS.items():
    lbl = label.strip()
    bh_all, n, bh_sh, bh_dd = bh_stats(BROAD_UNIVERSE, s, e)
    sysr = SYS.get(label, SYS.get(lbl))
    sh, dd = SYS_RISK.get(label, SYS_RISK.get(lbl, (0, 0)))
    cap = f"{100*sysr/bh_all:>7.0f}%" if bh_all and bh_all > 0 else "   n/a"
    print(f"{lbl:<17}{sysr:>6.1f}%{sh:>8.2f}{dd:>6.1f}%   "
          f"{bh_all:>7.1f}%{bh_sh:>8.2f}{bh_dd:>6.1f}%{cap:>9}")
