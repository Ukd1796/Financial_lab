PYTHONHASHSEED=0 CROSS_EXIT_TRENDPB=1 PERIODS_FILTER=Live finance/bin/python3 run_experiments.py

  [Cache] Loading 150 symbols from LOCAL SQLite (2014-01-01 → 2026-12-31)...
  [Cache] Local hit: 400,968 records for 150 symbols (no Supabase calls).


######################################################################
  VARIANT 1 — Selective cross-strategy exit ENABLED
  cross_exit_strategies = {'TrendPB'} on EqW / Adaptive / Adaptive+RCA routers
######################################################################

[PERIODS_FILTER active] running 1 of 7: Live  2025–2026
[DynamicUniverseAgent] Bulk fetching 150 symbols from 2024-06-15 to 2026-03-24 ...
[DynamicUniverseAgent] Loaded 150 symbols. Skipped 0: none

======================================================================
  Period: Live  2025–2026   (2025-01-01 → 2026-03-24)
  Universe: 150 symbols → DynamicUniverse top 80 → UniverseSelection top 20
  Costs: 0.10% commission + 0.05% slippage per side (all returns net of costs)
======================================================================
  Strategy               Sharpe    Return    MaxDD      PF     WR  #Trades
  --------------------------------------------------------------------  [Medium-term]
  DualMA SMA20/50         -0.00    -0.55%    7.80%    0.98  33.7%      104
  --------------------------------------------------------------------  [Short-term]
  Breakout 10d            -0.69   -10.61%   12.90%    0.80  37.4%      409
  QuietBrk 20d             0.05    -0.27%    8.43%    0.99  38.8%      263
  TrendPB v2 pct=3%        0.23     1.50%    3.84%    1.09  53.3%      135
  TrendPB v2 pct=5%        0.96     3.66%    1.97%    1.74  56.6%       53
  --------------------------------------------------------------------  [Mean-reversion]
  RSI-MR  os=5  ob=80      0.36     3.82%    5.86%    1.10  53.6%      351
  --------------------------------------------------------------------  [Multi-strategy baseline — equal weight]
  EqualWeight (5-strat)   -1.25    -4.11%    4.74%    0.79  46.8%      935

  --------------------------------------------------------------------  [Strategy PnL Attribution — EqualWeight]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  TrendPB            26         +315     57.7%        +12    -7.7%
  RSI-MR            254         -571     54.7%         -2    13.9%
  DualMA             38        -1110     31.6%        -29    27.0%
  Breakout          617        -2745     44.1%         -4    66.8%
  TOTAL             935        -4111
  --------------------------------------------------------------------  [EqualWeight — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  cross_ex  pass_thru%
  DualMA           5697    3490       2205          2       65         0       60.1%
  Breakout         4239    1703       1653        883      628         0       25.4%
  QuietBrk         3156       0       2715        441        0         0        0.0%
  TrendPB          3144     860       2284          0       51       459       25.7%
  RSI-MR           3667     862       2000        805      404         0       12.5%
  --------------------------------------------------------------------  [Multi-strategy adaptive — LLM weights]
  [AdaptiveSelector] 2025-01-01 [CRASH_HIGHVOL/HIGH] → DualMA=0.26  Breakout=0.32  QuietBrk=0.05  TrendPB=0.32  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2025-01-06 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.30  QuietBrk=0.10  TrendPB=0.40  RSI-MR=0.00
  [AdaptiveSelector] 2025-01-12 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.45  QuietBrk=0.00  TrendPB=0.35  RSI-MR=0.00
  [AdaptiveSelector] 2025-01-19 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.45  QuietBrk=0.00  TrendPB=0.35  RSI-MR=0.00
  [AdaptiveSelector] 2025-01-26 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.45  QuietBrk=0.00  TrendPB=0.35  RSI-MR=0.00
  [AdaptiveSelector] 2025-01-31 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.45  QuietBrk=0.00  TrendPB=0.35  RSI-MR=0.00
  [AdaptiveSelector] 2025-02-05 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.45  QuietBrk=0.00  TrendPB=0.35  RSI-MR=0.00
  [AdaptiveSelector] 2025-02-10 [CRASH_HIGHVOL/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.00  TrendPB=0.40  RSI-MR=0.00
  [AdaptiveSelector] 2025-02-16 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.45  QuietBrk=0.00  TrendPB=0.35  RSI-MR=0.00
  [AdaptiveSelector] 2025-02-23 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.45  QuietBrk=0.00  TrendPB=0.35  RSI-MR=0.00
  [AdaptiveSelector] 2025-03-02 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.55  QuietBrk=0.00  TrendPB=0.45  RSI-MR=0.00
  [AdaptiveSelector] 2025-03-09 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.45  QuietBrk=0.00  TrendPB=0.35  RSI-MR=0.00
  [AdaptiveSelector] 2025-03-16 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.45  QuietBrk=0.00  TrendPB=0.35  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2025-03-23 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.30  QuietBrk=0.10  TrendPB=0.40  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2025-03-31 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.30  QuietBrk=0.10  TrendPB=0.40  RSI-MR=0.00
  [AdaptiveSelector] 2025-04-06 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.45  QuietBrk=0.00  TrendPB=0.35  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: RECOVERY (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2025-04-14 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.45  QuietBrk=0.00  TrendPB=0.35  RSI-MR=0.00
  [AdaptiveSelector] Regime transition confirmed: CRASH_HIGHVOL → RECOVERY (after 2 weeks)
  [AdaptiveSelector] 2025-04-20 [RECOVERY/HIGH] → DualMA=0.21  Breakout=0.37  QuietBrk=0.26  TrendPB=0.11  RSI-MR=0.05
  [AdaptiveSelector] 2025-04-27 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.40  TrendPB=0.00  RSI-MR=0.00
  [AdaptiveSelector] 2025-05-04 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.40  TrendPB=0.00  RSI-MR=0.00
  [AdaptiveSelector] 2025-05-11 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.40  TrendPB=0.00  RSI-MR=0.00
  [AdaptiveSelector] 2025-05-18 [RECOVERY/HIGH] → DualMA=0.20  Breakout=0.40  QuietBrk=0.25  TrendPB=0.10  RSI-MR=0.05
  [AdaptiveSelector] 2025-05-25 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.40  TrendPB=0.00  RSI-MR=0.00
  [AdaptiveSelector] 2025-06-01 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.55  QuietBrk=0.30  TrendPB=0.00  RSI-MR=0.00
  [AdaptiveSelector] 2025-06-08 [RECOVERY/HIGH] → DualMA=0.20  Breakout=0.40  QuietBrk=0.30  TrendPB=0.05  RSI-MR=0.05
  [AdaptiveSelector] 2025-06-15 [RECOVERY/HIGH] → DualMA=0.20  Breakout=0.40  QuietBrk=0.30  TrendPB=0.05  RSI-MR=0.05
  [AdaptiveSelector] 2025-06-22 [RECOVERY/HIGH] → DualMA=0.21  Breakout=0.37  QuietBrk=0.26  TrendPB=0.11  RSI-MR=0.05
  [AdaptiveSelector] 2025-06-29 [RECOVERY/HIGH] → DualMA=0.21  Breakout=0.37  QuietBrk=0.26  TrendPB=0.11  RSI-MR=0.05
  [AdaptiveSelector] 2025-07-06 [RECOVERY/HIGH] → DualMA=0.21  Breakout=0.37  QuietBrk=0.26  TrendPB=0.11  RSI-MR=0.05
  [AdaptiveSelector] 2025-07-13 [RECOVERY/HIGH] → DualMA=0.21  Breakout=0.37  QuietBrk=0.26  TrendPB=0.11  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: BULL_SUSTAINED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2025-07-20 [RECOVERY/HIGH] → DualMA=0.21  Breakout=0.37  QuietBrk=0.26  TrendPB=0.11  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: CRASH_HIGHVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2025-07-27 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.40  TrendPB=0.00  RSI-MR=0.00
  [AdaptiveSelector] Regime transition confirmed: RECOVERY → CRASH_HIGHVOL (after 2 weeks)
  [AdaptiveSelector] 2025-08-03 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.45  QuietBrk=0.00  TrendPB=0.35  RSI-MR=0.00
  [AdaptiveSelector] 2025-08-10 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.45  QuietBrk=0.00  TrendPB=0.35  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: RECOVERY (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2025-08-17 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.45  QuietBrk=0.00  TrendPB=0.35  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2025-08-24 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.45  QuietBrk=0.00  TrendPB=0.35  RSI-MR=0.00
  [AdaptiveSelector] 2025-08-31 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.45  QuietBrk=0.00  TrendPB=0.35  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: RECOVERY (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2025-09-07 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.45  QuietBrk=0.00  TrendPB=0.35  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2025-09-14 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.45  QuietBrk=0.00  TrendPB=0.35  RSI-MR=0.00
  [AdaptiveSelector] Regime transition confirmed: CRASH_HIGHVOL → MIXED (after 2 weeks)
  [AdaptiveSelector] 2025-09-21 [MIXED/LOW] → DualMA=0.45  Breakout=0.30  QuietBrk=0.25  TrendPB=0.00  RSI-MR=0.00
  [AdaptiveSelector] 2025-09-28 [MIXED/LOW] → DualMA=0.45  Breakout=0.30  QuietBrk=0.25  TrendPB=0.00  RSI-MR=0.00
  [AdaptiveSelector] 2025-10-05 [MIXED/LOW] → DualMA=0.45  Breakout=0.30  QuietBrk=0.25  TrendPB=0.00  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: RECOVERY (1/2 weeks) — holding MIXED
  [AdaptiveSelector] 2025-10-12 [MIXED/LOW] → DualMA=0.45  Breakout=0.30  QuietBrk=0.25  TrendPB=0.00  RSI-MR=0.00
  [AdaptiveSelector] Regime transition confirmed: MIXED → RECOVERY (after 2 weeks)
  [AdaptiveSelector] 2025-10-19 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.40  TrendPB=0.00  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: BULL_SUSTAINED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2025-10-26 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.55  QuietBrk=0.30  TrendPB=0.00  RSI-MR=0.00
  [AdaptiveSelector] 2025-11-02 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.40  TrendPB=0.00  RSI-MR=0.00
  [AdaptiveSelector] 2025-11-09 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.40  TrendPB=0.00  RSI-MR=0.00
  [AdaptiveSelector] 2025-11-16 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.40  TrendPB=0.00  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2025-11-23 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.40  TrendPB=0.00  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: BULL_SUSTAINED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2025-11-30 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.55  QuietBrk=0.30  TrendPB=0.00  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: BEAR_EARLY (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2025-12-07 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.40  TrendPB=0.00  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: BULL_SUSTAINED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2025-12-14 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.55  QuietBrk=0.30  TrendPB=0.00  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2025-12-21 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.40  TrendPB=0.00  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2025-12-28 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.40  TrendPB=0.00  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: BULL_SUSTAINED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2026-01-04 [RECOVERY/HIGH] → DualMA=0.21  Breakout=0.37  QuietBrk=0.26  TrendPB=0.11  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2026-01-11 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.40  TrendPB=0.00  RSI-MR=0.00
  [AdaptiveSelector] 2026-01-18 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.55  QuietBrk=0.30  TrendPB=0.00  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: CRASH_HIGHVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2026-01-26 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.40  TrendPB=0.00  RSI-MR=0.00
  [AdaptiveSelector] Regime transition confirmed: RECOVERY → CRASH_HIGHVOL (after 2 weeks)
  [AdaptiveSelector] 2026-02-01 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.45  QuietBrk=0.00  TrendPB=0.35  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2026-02-08 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.45  QuietBrk=0.00  TrendPB=0.35  RSI-MR=0.00
  [AdaptiveSelector] 2026-02-15 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.45  QuietBrk=0.00  TrendPB=0.35  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: RECOVERY (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2026-02-22 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.45  QuietBrk=0.00  TrendPB=0.35  RSI-MR=0.00
  [AdaptiveSelector] 2026-03-01 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.45  QuietBrk=0.00  TrendPB=0.35  RSI-MR=0.00
  [AdaptiveSelector] 2026-03-08 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.45  QuietBrk=0.00  TrendPB=0.35  RSI-MR=0.00
  [AdaptiveSelector] 2026-03-15 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.45  QuietBrk=0.00  TrendPB=0.35  RSI-MR=0.00
  [AdaptiveSelector] 2026-03-22 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.45  QuietBrk=0.00  TrendPB=0.35  RSI-MR=0.00
  Adaptive  (5-strat)     -0.57    -3.78%    6.49%    0.88  42.4%      715
                         (LLM calls: 66)

  --------------------------------------------------------------------  [Strategy PnL Attribution — Adaptive]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  DualMA             19         +186     36.8%        +10    -4.9%
  TrendPB            11          +13     63.6%         +1    -0.3%
  RSI-MR             46         -126     45.7%         -3     3.3%
  Breakout          639        -3849     41.9%         -6   101.9%
  TOTAL             715        -3776
  --------------------------------------------------------------------  [Adaptive — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  cross_ex  pass_thru%
  DualMA           6265    2505       3756          4       45         0       39.3%
  Breakout         4745    3801        652        292      536         0       68.8%
  QuietBrk         3147      35       2953        159        0         0        1.1%
  TrendPB          1445     520        925          0       39       318       33.3%
  RSI-MR           1043     256        568        219      184         0        6.9%
  --------------------------------------------------------------------  [Multi-strategy adaptive + RegimeContextAgent]
  Adaptive+RCA (5-strat)  -0.53    -3.48%    6.42%    0.89  41.5%      715
                         (LLM calls: 66)

  --------------------------------------------------------------------  [Strategy PnL Attribution — Adaptive+RCA]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  DualMA             19         +214     36.8%        +11    -6.2%
  TrendPB            19         +133     52.6%         +7    -3.8%
  RSI-MR             35         -154     42.9%         -4     4.4%
  Breakout          642        -3674     41.3%         -6   105.5%
  TOTAL             715        -3481
  --------------------------------------------------------------------  [Adaptive+RCA — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  cross_ex  pass_thru%
  DualMA           6226    2549       3673          4       45         0       40.2%
  Breakout         4663    3680        688        295      537         0       67.4%
  QuietBrk         3089      32       2893        164        0         0        1.0%
  TrendPB          1524     585        939          0       39       326       35.8%
  RSI-MR            766     185        406        175      130         0        7.2%
  RCA delta              + 0.04  +   0.29%

  ══════════════════════════════════════════════════════════════════
  OPPORTUNITY QUALITY SUMMARY  [Live  2025–2026]
  ══════════════════════════════════════════════════════════════════
  Trades analyzed  : 2365  (1038 winners / 1327 losers)
  ──────────────────────────────────────────────────────────────────
  Breakout quality:
    Follow-through rate  :   49.0%   (price continued post-exit)
    False breakout rate  :   13.4%   (MFE>2% but final return <0)
    Persistence half-life:    0.0 days (median survival above entry)
    Avg MFE efficiency   : -0.209      (1.00 = exit at peak)
  ──────────────────────────────────────────────────────────────────
  Continuation decay (post-exit drift):
                      1D        3D        5D
    Winners      +0.01%    -0.17%    -0.40%
    Losers       +0.15%    +0.22%    +0.45%
  ──────────────────────────────────────────────────────────────────
  Universe diagnostics (305 days):
    Avg stability score  : 0.226  (0=fully churning, 1=static)
    Avg daily turnover   : 64.3%
    Avg leader half-life : 1.6 days
    Stability vs PnL corr: +0.022  (>0 = stable universe → better trades)
    Turnover vs success  : -0.001  (<0 = higher churn → fewer successes)
  ──────────────────────────────────────────────────────────────────
  Per-regime breakdown (entry regime):
    Regime                           N  WinRate    AvgRet
    HIGH_VOL_SIDEWAYS               63    47.6%    -0.21%
    HIGH_VOL_UPTREND               503    47.7%    -0.33%
    LOW_VOL_SIDEWAYS               282    37.6%    -0.12%
    LOW_VOL_UPTREND                735    40.0%    -0.43%
    MID_VOL_SIDEWAYS               129    46.5%    -0.07%
    MID_VOL_UPTREND                653    47.2%    -0.01%
  ──────────────────────────────────────────────────────────────────
  ══════════════════════════════════════════════════════════════════

======================================================================


///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

ujjwalkumar@Ujjwals-Laptop Financial_lab % PYTHONHASHSEED=0 CROSS_EXIT_TRENDPB=1 PERIODS_FILTER=Live finance/bin/python3 run_experiments.py

  [Cache] Loading 150 symbols from LOCAL SQLite (2014-01-01 → 2026-12-31)...
  [Cache] Local hit: 400,968 records for 150 symbols (no Supabase calls).


######################################################################
  VARIANT 1 — Selective cross-strategy exit ENABLED
  cross_exit_strategies = {'TrendPB'} on EqW / Adaptive / Adaptive+RCA routers
######################################################################

[PERIODS_FILTER active] running 1 of 7: Live  2025–2026
[DynamicUniverseAgent] Bulk fetching 150 symbols from 2024-06-15 to 2026-03-24 ...
[DynamicUniverseAgent] Loaded 150 symbols. Skipped 0: none

======================================================================
  Period: Live  2025–2026   (2025-01-01 → 2026-03-24)
  Universe: 150 symbols → DynamicUniverse top 80 → UniverseSelection top 20
  Costs: 0.10% commission + 0.05% slippage per side (all returns net of costs)
======================================================================
  Strategy               Sharpe    Return    MaxDD      PF     WR  #Trades
  --------------------------------------------------------------------  [Medium-term]
  DualMA SMA20/50         -0.00    -0.55%    7.80%    0.98  33.7%      104
  --------------------------------------------------------------------  [Short-term]
  Breakout 10d            -0.69   -10.61%   12.90%    0.80  37.4%      409
  QuietBrk 20d             0.05    -0.27%    8.43%    0.99  38.8%      263
  TrendPB v2 pct=3%        0.23     1.50%    3.84%    1.09  53.3%      135
  TrendPB v2 pct=5%        0.96     3.66%    1.97%    1.74  56.6%       53
  --------------------------------------------------------------------  [Mean-reversion]
  RSI-MR  os=5  ob=80      0.36     3.82%    5.86%    1.10  53.6%      351
  --------------------------------------------------------------------  [Multi-strategy baseline — equal weight]
  EqualWeight (5-strat)   -1.25    -4.11%    4.74%    0.79  46.8%      935

  --------------------------------------------------------------------  [Strategy PnL Attribution — EqualWeight]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  TrendPB            26         +315     57.7%        +12    -7.7%
  RSI-MR            254         -571     54.7%         -2    13.9%
  DualMA             38        -1110     31.6%        -29    27.0%
  Breakout          617        -2745     44.1%         -4    66.8%
  TOTAL             935        -4111
  --------------------------------------------------------------------  [EqualWeight — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  cross_ex  pass_thru%
  DualMA           5697    3490       2205          2       65         0       60.1%
  Breakout         4239    1703       1653        883      628         0       25.4%
  QuietBrk         3156       0       2715        441        0         0        0.0%
  TrendPB          3144     860       2284          0       51       459       25.7%
  RSI-MR           3667     862       2000        805      404         0       12.5%
  --------------------------------------------------------------------  [Multi-strategy adaptive — LLM weights]
  [AdaptiveSelector] 2025-01-01 [CRASH_HIGHVOL/HIGH] → DualMA=0.26  Breakout=0.32  QuietBrk=0.05  TrendPB=0.32  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2025-01-06 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.30  QuietBrk=0.10  TrendPB=0.40  RSI-MR=0.00
  [AdaptiveSelector] 2025-01-12 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.45  QuietBrk=0.00  TrendPB=0.35  RSI-MR=0.00
  [AdaptiveSelector] 2025-01-19 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.45  QuietBrk=0.00  TrendPB=0.35  RSI-MR=0.00
  [AdaptiveSelector] 2025-01-26 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.45  QuietBrk=0.00  TrendPB=0.35  RSI-MR=0.00
  [AdaptiveSelector] 2025-01-31 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.45  QuietBrk=0.00  TrendPB=0.35  RSI-MR=0.00
  [AdaptiveSelector] 2025-02-05 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.45  QuietBrk=0.00  TrendPB=0.35  RSI-MR=0.00
  [AdaptiveSelector] 2025-02-10 [CRASH_HIGHVOL/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.00  TrendPB=0.40  RSI-MR=0.00
  [AdaptiveSelector] 2025-02-16 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.45  QuietBrk=0.00  TrendPB=0.35  RSI-MR=0.00
  [AdaptiveSelector] 2025-02-23 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.45  QuietBrk=0.00  TrendPB=0.35  RSI-MR=0.00
  [AdaptiveSelector] 2025-03-02 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.45  QuietBrk=0.00  TrendPB=0.35  RSI-MR=0.00
  [AdaptiveSelector] 2025-03-09 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.45  QuietBrk=0.00  TrendPB=0.35  RSI-MR=0.00
  [AdaptiveSelector] 2025-03-16 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.45  QuietBrk=0.00  TrendPB=0.35  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2025-03-23 [CRASH_HIGHVOL/HIGH] → DualMA=0.21  Breakout=0.32  QuietBrk=0.10  TrendPB=0.32  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2025-03-31 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.30  QuietBrk=0.10  TrendPB=0.40  RSI-MR=0.00
  [AdaptiveSelector] 2025-04-06 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.45  QuietBrk=0.00  TrendPB=0.35  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: RECOVERY (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2025-04-14 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.45  QuietBrk=0.00  TrendPB=0.35  RSI-MR=0.00
  [AdaptiveSelector] Regime transition confirmed: CRASH_HIGHVOL → RECOVERY (after 2 weeks)
  [AdaptiveSelector] 2025-04-20 [RECOVERY/HIGH] → DualMA=0.21  Breakout=0.37  QuietBrk=0.26  TrendPB=0.11  RSI-MR=0.05
  [AdaptiveSelector] 2025-04-27 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.40  TrendPB=0.00  RSI-MR=0.00
  [AdaptiveSelector] 2025-05-04 [RECOVERY/HIGH] → DualMA=0.21  Breakout=0.37  QuietBrk=0.26  TrendPB=0.11  RSI-MR=0.05
  [AdaptiveSelector] 2025-05-11 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.40  TrendPB=0.00  RSI-MR=0.00
  [AdaptiveSelector] 2025-05-18 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.40  TrendPB=0.00  RSI-MR=0.00
  [AdaptiveSelector] 2025-05-25 [RECOVERY/HIGH] → DualMA=0.21  Breakout=0.37  QuietBrk=0.26  TrendPB=0.11  RSI-MR=0.05
  [AdaptiveSelector] 2025-06-01 [RECOVERY/HIGH] → DualMA=0.17  Breakout=0.39  QuietBrk=0.28  TrendPB=0.11  RSI-MR=0.05
  [AdaptiveSelector] 2025-06-08 [RECOVERY/HIGH] → DualMA=0.21  Breakout=0.37  QuietBrk=0.26  TrendPB=0.11  RSI-MR=0.05
  [AdaptiveSelector] 2025-06-15 [RECOVERY/HIGH] → DualMA=0.21  Breakout=0.37  QuietBrk=0.26  TrendPB=0.11  RSI-MR=0.05
  [AdaptiveSelector] 2025-06-22 [RECOVERY/HIGH] → DualMA=0.21  Breakout=0.37  QuietBrk=0.26  TrendPB=0.11  RSI-MR=0.05
  [AdaptiveSelector] 2025-06-29 [RECOVERY/HIGH] → DualMA=0.21  Breakout=0.37  QuietBrk=0.26  TrendPB=0.11  RSI-MR=0.05
  [AdaptiveSelector] 2025-07-06 [RECOVERY/HIGH] → DualMA=0.20  Breakout=0.40  QuietBrk=0.30  TrendPB=0.05  RSI-MR=0.05
  [AdaptiveSelector] 2025-07-13 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.40  TrendPB=0.00  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: BULL_SUSTAINED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2025-07-20 [RECOVERY/HIGH] → DualMA=0.20  Breakout=0.45  QuietBrk=0.35  TrendPB=0.00  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: CRASH_HIGHVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2025-07-27 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.40  TrendPB=0.00  RSI-MR=0.00
  [AdaptiveSelector] Regime transition confirmed: RECOVERY → CRASH_HIGHVOL (after 2 weeks)
  [AdaptiveSelector] 2025-08-03 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.45  QuietBrk=0.00  TrendPB=0.35  RSI-MR=0.00
  [AdaptiveSelector] 2025-08-10 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.45  QuietBrk=0.00  TrendPB=0.35  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: RECOVERY (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2025-08-17 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.45  QuietBrk=0.00  TrendPB=0.35  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2025-08-24 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.45  QuietBrk=0.00  TrendPB=0.35  RSI-MR=0.00
  [AdaptiveSelector] 2025-08-31 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.45  QuietBrk=0.00  TrendPB=0.35  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: RECOVERY (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2025-09-07 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.45  QuietBrk=0.00  TrendPB=0.35  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2025-09-14 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.45  QuietBrk=0.00  TrendPB=0.35  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2025-09-21 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.45  QuietBrk=0.00  TrendPB=0.35  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2025-09-28 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.45  QuietBrk=0.00  TrendPB=0.35  RSI-MR=0.00
  [AdaptiveSelector] Regime transition confirmed: CRASH_HIGHVOL → MIXED (after 2 weeks)
  [AdaptiveSelector] 2025-10-05 [MIXED/LOW] → DualMA=0.45  Breakout=0.30  QuietBrk=0.25  TrendPB=0.00  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: RECOVERY (1/2 weeks) — holding MIXED
  [AdaptiveSelector] 2025-10-12 [MIXED/LOW] → DualMA=0.45  Breakout=0.30  QuietBrk=0.25  TrendPB=0.00  RSI-MR=0.00
  [AdaptiveSelector] Regime transition confirmed: MIXED → RECOVERY (after 2 weeks)
  [AdaptiveSelector] 2025-10-19 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.40  TrendPB=0.00  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: BULL_SUSTAINED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2025-10-26 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.40  TrendPB=0.00  RSI-MR=0.00
  [AdaptiveSelector] 2025-11-02 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.40  TrendPB=0.00  RSI-MR=0.00
  [AdaptiveSelector] 2025-11-09 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.55  QuietBrk=0.30  TrendPB=0.00  RSI-MR=0.00
  [AdaptiveSelector] 2025-11-16 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.40  TrendPB=0.00  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2025-11-23 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.40  TrendPB=0.00  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: BULL_SUSTAINED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2025-11-30 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.55  QuietBrk=0.30  TrendPB=0.00  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: BEAR_EARLY (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2025-12-07 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.40  TrendPB=0.00  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: BULL_SUSTAINED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2025-12-14 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.40  TrendPB=0.00  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2025-12-21 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.40  TrendPB=0.00  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2025-12-28 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.55  QuietBrk=0.30  TrendPB=0.00  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: BULL_SUSTAINED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2026-01-04 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.40  TrendPB=0.00  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2026-01-11 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.40  TrendPB=0.00  RSI-MR=0.00
  [AdaptiveSelector] 2026-01-18 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.55  QuietBrk=0.30  TrendPB=0.00  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: CRASH_HIGHVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2026-01-26 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.40  TrendPB=0.00  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2026-02-01 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.55  QuietBrk=0.30  TrendPB=0.00  RSI-MR=0.00
  [AdaptiveSelector] 2026-02-08 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.40  TrendPB=0.00  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2026-02-15 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.40  TrendPB=0.00  RSI-MR=0.00
  [AdaptiveSelector] 2026-02-22 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.40  TrendPB=0.00  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: CRASH_HIGHVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2026-03-01 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.55  QuietBrk=0.30  TrendPB=0.00  RSI-MR=0.00
  [AdaptiveSelector] Regime transition confirmed: RECOVERY → CRASH_HIGHVOL (after 2 weeks)
  [AdaptiveSelector] 2026-03-08 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.45  QuietBrk=0.00  TrendPB=0.35  RSI-MR=0.00
  [AdaptiveSelector] 2026-03-15 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.45  QuietBrk=0.00  TrendPB=0.35  RSI-MR=0.00
  [AdaptiveSelector] 2026-03-22 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.45  QuietBrk=0.00  TrendPB=0.35  RSI-MR=0.00
  Adaptive  (5-strat)     -1.02    -7.73%    9.54%    0.78  41.4%      756
                         (LLM calls: 66)

  --------------------------------------------------------------------  [Strategy PnL Attribution — Adaptive]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  TrendPB            12           +7     33.3%         +1    -0.1%
  RSI-MR             41         -143     51.2%         -3     1.8%
  DualMA             14         -285     42.9%        -20     3.7%
  Breakout          689        -7314     40.9%        -11    94.6%
  TOTAL             756        -7734
  --------------------------------------------------------------------  [Adaptive — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  cross_ex  pass_thru%
  DualMA           6451    2313       4133          5       44         0       35.2%
  Breakout         4988    4247        475        266      466         0       75.8%
  QuietBrk         3417      39       3199        179        0         0        1.1%
  TrendPB          1323     469        854          0       29       320       33.3%
  RSI-MR            969     252        467        250      188         0        6.6%
  --------------------------------------------------------------------  [Multi-strategy adaptive + RegimeContextAgent]
  Adaptive+RCA (5-strat)  -0.59    -4.00%    6.40%    0.87  41.6%      707
                         (LLM calls: 66)

  --------------------------------------------------------------------  [Strategy PnL Attribution — Adaptive+RCA]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  DualMA             20         +113     35.0%         +6    -2.8%
  TrendPB            19          +99     52.6%         +5    -2.5%
  RSI-MR             26          -49     42.3%         -2     1.2%
  Breakout          642        -4159     41.4%         -6   104.1%
  TOTAL             707        -3997
  --------------------------------------------------------------------  [Adaptive+RCA — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  cross_ex  pass_thru%
  DualMA           6229    2580       3645          4       44         0       40.7%
  Breakout         4635    3679        682        274      536         0       67.8%
  QuietBrk         3082      30       2893        159        0         0        1.0%
  TrendPB          1489     560        929          0       39       325       35.0%
  RSI-MR            540     138        284        118       95         0        8.0%
  RCA delta              + 0.42  +   3.74%

  ══════════════════════════════════════════════════════════════════
  OPPORTUNITY QUALITY SUMMARY  [Live  2025–2026]
  ══════════════════════════════════════════════════════════════════
  Trades analyzed  : 2398  (1045 winners / 1353 losers)
  ──────────────────────────────────────────────────────────────────
  Breakout quality:
    Follow-through rate  :   49.2%   (price continued post-exit)
    False breakout rate  :   14.3%   (MFE>2% but final return <0)
    Persistence half-life:    0.0 days (median survival above entry)
    Avg MFE efficiency   : -0.210      (1.00 = exit at peak)
  ──────────────────────────────────────────────────────────────────
  Continuation decay (post-exit drift):
                      1D        3D        5D
    Winners      -0.00%    -0.15%    -0.25%
    Losers       +0.13%    +0.14%    +0.36%
  ──────────────────────────────────────────────────────────────────
  Universe diagnostics (305 days):
    Avg stability score  : 0.226  (0=fully churning, 1=static)
    Avg daily turnover   : 64.3%
    Avg leader half-life : 1.6 days
    Stability vs PnL corr: +0.028  (>0 = stable universe → better trades)
    Turnover vs success  : +0.012  (<0 = higher churn → fewer successes)
  ──────────────────────────────────────────────────────────────────
  Per-regime breakdown (entry regime):
    Regime                           N  WinRate    AvgRet
    HIGH_VOL_SIDEWAYS               66    47.0%    -0.32%
    HIGH_VOL_UPTREND               517    46.4%    -0.41%
    LOW_VOL_SIDEWAYS               283    38.9%    -0.13%
    LOW_VOL_UPTREND                749    39.8%    -0.47%
    MID_VOL_SIDEWAYS               129    45.7%    -0.11%
    MID_VOL_UPTREND                654    46.9%    -0.05%
  ──────────────────────────────────────────────────────────────────
  ══════════════════════════════════════════════════════════════════

======================================================================



PYTHONHASHSEED=0 CROSS_EXIT_TRENDPB=1 CROSS_EXIT_GATE=1 PERIODS_FILTER=Live,Crash,Recov finance/bin/python3 run_experiments.py

  [Cache] Loading 150 symbols from LOCAL SQLite (2014-01-01 → 2026-12-31)...
  [Cache] Local hit: 400,968 records for 150 symbols (no Supabase calls).


######################################################################
  VARIANT C — Cross-exit with PERFORMANCE GATE
  cross_exit_strategies = {'TrendPB'}
  gate: allow cross-exit only when rolling-20-trade WR(Breakout) < 0.40
  warmup: gate stays CLOSED until 20 fills accrue
######################################################################

[PERIODS_FILTER active] running 3 of 7: Crash 2020, Recov 2020–2021, Live  2025–2026
[DynamicUniverseAgent] Bulk fetching 150 symbols from 2019-06-15 to 2020-12-31 ...
[DynamicUniverseAgent] Loaded 148 symbols. Skipped 2: TMCV(no data), ETERNAL(no data)

======================================================================
  Period: Crash 2020        (2020-01-01 → 2020-12-31)
  Universe: 150 symbols → DynamicUniverse top 80 → UniverseSelection top 20
  Costs: 0.10% commission + 0.05% slippage per side (all returns net of costs)
======================================================================
  Strategy               Sharpe    Return    MaxDD      PF     WR  #Trades
  --------------------------------------------------------------------  [Medium-term]
  DualMA SMA20/50          1.67    23.80%    9.00%    2.27  49.5%       93
  --------------------------------------------------------------------  [Short-term]
  Breakout 10d             1.72    29.08%    7.25%    1.49  41.3%      426
  QuietBrk 20d             1.95    31.64%   12.71%    1.70  39.0%      287
  TrendPB v2 pct=3%        1.62    19.51%    5.84%    1.53  60.9%      425
  TrendPB v2 pct=5%        1.83    16.68%    5.42%    1.78  62.8%      253
  --------------------------------------------------------------------  [Mean-reversion]
  RSI-MR  os=5  ob=80      1.05    13.63%   10.08%    1.31  61.6%      435
  --------------------------------------------------------------------  [Multi-strategy baseline — equal weight]
  EqualWeight (5-strat)    2.62    25.21%    5.30%    1.85  55.5%     1235

  --------------------------------------------------------------------  [Strategy PnL Attribution — EqualWeight]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  Breakout          706       +17686     50.1%        +25    71.3%
  RSI-MR            327        +3291     66.1%        +10    13.3%
  TrendPB           159        +2465     61.0%        +16     9.9%
  DualMA             43        +1371     44.2%        +32     5.5%
  TOTAL            1235       +24813
  --------------------------------------------------------------------  [EqualWeight — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  cross_ex  gated_off  pass_thru%
  DualMA           9065    6729       2325         11       28         0          0       73.9%
  Breakout         7936    1745       4589       1602      314         0          0       18.0%
  QuietBrk         6703       0       5847        856        0         0          0        0.0%
  TrendPB          7257    1183       2994          0       84       335       3080       15.1%
  RSI-MR           7523     754       4493       2276      130         0          0        8.3%
  gate: open 89/250 days (35.6%) — closed 161/250 days
  --------------------------------------------------------------------  [Multi-strategy adaptive — LLM weights]
  [AdaptiveSelector] 2020-01-01 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2020-01-06 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.40  TrendPB=0.00  RSI-MR=0.00
  [AdaptiveSelector] 2020-01-12 [RECOVERY/HIGH] → DualMA=0.21  Breakout=0.37  QuietBrk=0.26  TrendPB=0.11  RSI-MR=0.05
  [AdaptiveSelector] 2020-01-19 [RECOVERY/HIGH] → DualMA=0.21  Breakout=0.37  QuietBrk=0.26  TrendPB=0.11  RSI-MR=0.05
  [AdaptiveSelector] 2020-01-26 [RECOVERY/HIGH] → DualMA=0.17  Breakout=0.39  QuietBrk=0.28  TrendPB=0.11  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: CRASH_HIGHVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2020-02-02 [RECOVERY/HIGH] → DualMA=0.20  Breakout=0.40  QuietBrk=0.25  TrendPB=0.10  RSI-MR=0.05
  [AdaptiveSelector] 2020-02-09 [RECOVERY/HIGH] → DualMA=0.17  Breakout=0.39  QuietBrk=0.28  TrendPB=0.11  RSI-MR=0.05
  [AdaptiveSelector] 2020-02-16 [RECOVERY/HIGH] → DualMA=0.20  Breakout=0.40  QuietBrk=0.25  TrendPB=0.10  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2020-02-23 [RECOVERY/HIGH] → DualMA=0.22  Breakout=0.39  QuietBrk=0.28  TrendPB=0.11  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: CRASH_HIGHVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2020-03-01 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.40  TrendPB=0.00  RSI-MR=0.00
  [AdaptiveSelector] Regime transition confirmed: RECOVERY → CRASH_HIGHVOL (after 2 weeks)
  [AdaptiveSelector] 2020-03-08 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.45  QuietBrk=0.00  TrendPB=0.35  RSI-MR=0.00
  [AdaptiveSelector] 2020-03-15 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.45  QuietBrk=0.00  TrendPB=0.35  RSI-MR=0.00
  [AdaptiveSelector] 2020-03-22 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.45  QuietBrk=0.00  TrendPB=0.35  RSI-MR=0.00
  [AdaptiveSelector] 2020-03-29 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.45  QuietBrk=0.00  TrendPB=0.35  RSI-MR=0.00
  [AdaptiveSelector] 2020-04-06 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.45  QuietBrk=0.00  TrendPB=0.35  RSI-MR=0.00
  [AdaptiveSelector] 2020-04-12 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.45  QuietBrk=0.00  TrendPB=0.35  RSI-MR=0.00
  [AdaptiveSelector] 2020-04-19 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.45  QuietBrk=0.00  TrendPB=0.35  RSI-MR=0.00
  [AdaptiveSelector] 2020-04-26 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.45  QuietBrk=0.00  TrendPB=0.35  RSI-MR=0.00
  [AdaptiveSelector] 2020-05-03 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.45  QuietBrk=0.00  TrendPB=0.35  RSI-MR=0.00
  [AdaptiveSelector] 2020-05-10 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.45  QuietBrk=0.00  TrendPB=0.35  RSI-MR=0.00
  [AdaptiveSelector] 2020-05-17 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.45  QuietBrk=0.00  TrendPB=0.35  RSI-MR=0.00
  [AdaptiveSelector] 2020-05-25 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.45  QuietBrk=0.00  TrendPB=0.35  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2020-05-31 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.45  QuietBrk=0.00  TrendPB=0.35  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: RECOVERY (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2020-06-07 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.30  QuietBrk=0.10  TrendPB=0.40  RSI-MR=0.00
  [AdaptiveSelector] Regime transition confirmed: CRASH_HIGHVOL → RECOVERY (after 2 weeks)
  [AdaptiveSelector] 2020-06-14 [RECOVERY/HIGH] → DualMA=0.21  Breakout=0.37  QuietBrk=0.26  TrendPB=0.11  RSI-MR=0.05
  [AdaptiveSelector] 2020-06-21 [RECOVERY/HIGH] → DualMA=0.21  Breakout=0.37  QuietBrk=0.26  TrendPB=0.11  RSI-MR=0.05
  [AdaptiveSelector] 2020-06-28 [RECOVERY/HIGH] → DualMA=0.21  Breakout=0.37  QuietBrk=0.26  TrendPB=0.11  RSI-MR=0.05
  [AdaptiveSelector] 2020-07-05 [RECOVERY/HIGH] → DualMA=0.17  Breakout=0.40  QuietBrk=0.28  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2020-07-12 [RECOVERY/HIGH] → DualMA=0.21  Breakout=0.37  QuietBrk=0.26  TrendPB=0.11  RSI-MR=0.05
  [AdaptiveSelector] 2020-07-19 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-07-26 [RECOVERY/HIGH] → DualMA=0.21  Breakout=0.37  QuietBrk=0.26  TrendPB=0.11  RSI-MR=0.05
  [AdaptiveSelector] 2020-08-02 [RECOVERY/HIGH] → DualMA=0.20  Breakout=0.40  QuietBrk=0.25  TrendPB=0.10  RSI-MR=0.05
  [AdaptiveSelector] 2020-08-09 [RECOVERY/HIGH] → DualMA=0.21  Breakout=0.37  QuietBrk=0.26  TrendPB=0.11  RSI-MR=0.05
  [AdaptiveSelector] 2020-08-16 [RECOVERY/HIGH] → DualMA=0.20  Breakout=0.40  QuietBrk=0.30  TrendPB=0.05  RSI-MR=0.05
  [AdaptiveSelector] 2020-08-23 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-08-30 [RECOVERY/HIGH] → DualMA=0.20  Breakout=0.40  QuietBrk=0.30  TrendPB=0.05  RSI-MR=0.05
  [AdaptiveSelector] 2020-09-06 [RECOVERY/HIGH] → DualMA=0.21  Breakout=0.37  QuietBrk=0.26  TrendPB=0.11  RSI-MR=0.05
  [AdaptiveSelector] 2020-09-13 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-09-20 [RECOVERY/HIGH] → DualMA=0.21  Breakout=0.37  QuietBrk=0.26  TrendPB=0.11  RSI-MR=0.05
  [AdaptiveSelector] 2020-09-27 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-10-04 [RECOVERY/HIGH] → DualMA=0.21  Breakout=0.37  QuietBrk=0.26  TrendPB=0.11  RSI-MR=0.05
  [AdaptiveSelector] 2020-10-11 [RECOVERY/HIGH] → DualMA=0.21  Breakout=0.37  QuietBrk=0.26  TrendPB=0.11  RSI-MR=0.05
  [AdaptiveSelector] 2020-10-18 [RECOVERY/HIGH] → DualMA=0.21  Breakout=0.37  QuietBrk=0.26  TrendPB=0.11  RSI-MR=0.05
  [AdaptiveSelector] 2020-10-25 [RECOVERY/HIGH] → DualMA=0.20  Breakout=0.40  QuietBrk=0.30  TrendPB=0.05  RSI-MR=0.05
  [AdaptiveSelector] 2020-11-01 [RECOVERY/HIGH] → DualMA=0.17  Breakout=0.39  QuietBrk=0.28  TrendPB=0.11  RSI-MR=0.05
  [AdaptiveSelector] 2020-11-08 [RECOVERY/HIGH] → DualMA=0.17  Breakout=0.39  QuietBrk=0.28  TrendPB=0.11  RSI-MR=0.05
  [AdaptiveSelector] 2020-11-13 [RECOVERY/HIGH] → DualMA=0.21  Breakout=0.37  QuietBrk=0.26  TrendPB=0.11  RSI-MR=0.05
  [AdaptiveSelector] 2020-11-18 [RECOVERY/HIGH] → DualMA=0.21  Breakout=0.37  QuietBrk=0.26  TrendPB=0.11  RSI-MR=0.05
  [AdaptiveSelector] 2020-11-23 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-11-30 [RECOVERY/HIGH] → DualMA=0.21  Breakout=0.37  QuietBrk=0.26  TrendPB=0.11  RSI-MR=0.05
  [AdaptiveSelector] 2020-12-06 [RECOVERY/HIGH] → DualMA=0.20  Breakout=0.40  QuietBrk=0.30  TrendPB=0.05  RSI-MR=0.05
  [AdaptiveSelector] 2020-12-13 [RECOVERY/HIGH] → DualMA=0.20  Breakout=0.40  QuietBrk=0.30  TrendPB=0.05  RSI-MR=0.05
  [AdaptiveSelector] 2020-12-20 [RECOVERY/HIGH] → DualMA=0.21  Breakout=0.37  QuietBrk=0.26  TrendPB=0.11  RSI-MR=0.05
  [AdaptiveSelector] 2020-12-27 [RECOVERY/HIGH] → DualMA=0.20  Breakout=0.40  QuietBrk=0.30  TrendPB=0.05  RSI-MR=0.05
  Adaptive  (5-strat)      2.28    28.50%    5.57%    1.71  52.4%     1044
                         (LLM calls: 54)

  --------------------------------------------------------------------  [Strategy PnL Attribution — Adaptive]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  Breakout          745       +24028     47.1%        +32    85.7%
  TrendPB           126        +2088     65.1%        +17     7.4%
  DualMA             25        +1532     56.0%        +61     5.5%
  RSI-MR            148         +382     67.6%         +3     1.4%
  TOTAL            1044       +28030
  --------------------------------------------------------------------  [Adaptive — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  cross_ex  gated_off  pass_thru%
  DualMA           8629    2209       6411          9       21         0          0       25.4%
  Breakout         7195    5746        474        975      337         0          0       75.2%
  QuietBrk         5973     208       5223        542        0         0          0        3.5%
  TrendPB          6281     999       2269          0      117       346       3013       14.0%
  RSI-MR           5923     541       3364       2018      256         0          0        4.8%
  gate: open 79/250 days (31.6%) — closed 171/250 days
  --------------------------------------------------------------------  [Multi-strategy adaptive + RegimeContextAgent]
  Adaptive+RCA (5-strat)   1.56    19.01%    7.74%    1.46  50.4%     1026
                         (LLM calls: 54)

  --------------------------------------------------------------------  [Strategy PnL Attribution — Adaptive+RCA]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  Breakout          755       +15662     45.7%        +21    84.2%
  TrendPB           120        +1864     60.0%        +16    10.0%
  DualMA             25         +719     60.0%        +29     3.9%
  RSI-MR            126         +356     67.5%         +3     1.9%
  TOTAL            1026       +18601
  --------------------------------------------------------------------  [Adaptive+RCA — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  cross_ex  gated_off  pass_thru%
  DualMA           8387    2276       6101         10       22         0          0       26.9%
  Breakout         6926    5545        465        916      364         0          0       74.8%
  QuietBrk         5836     184       5145        507        0         0          0        3.2%
  TrendPB          5910     969       2197          0      115       345       2744       14.5%
  RSI-MR           4336     448       2469       1419      205         0          0        5.6%
  gate: open 80/250 days (32.0%) — closed 170/250 days
  RCA delta              -0.73    -9.48%

  ══════════════════════════════════════════════════════════════════
  OPPORTUNITY QUALITY SUMMARY  [Crash 2020]
  ══════════════════════════════════════════════════════════════════
  Trades analyzed  : 3305  (1750 winners / 1555 losers)
  ──────────────────────────────────────────────────────────────────
  Breakout quality:
    Follow-through rate  :   56.2%   (price continued post-exit)
    False breakout rate  :   31.5%   (MFE>2% but final return <0)
    Persistence half-life:    0.0 days (median survival above entry)
    Avg MFE efficiency   : -0.063      (1.00 = exit at peak)
  ──────────────────────────────────────────────────────────────────
  Continuation decay (post-exit drift):
                      1D        3D        5D
    Winners      -0.08%    +0.61%    +1.34%
    Losers       -0.15%    +0.42%    +0.90%
  ──────────────────────────────────────────────────────────────────
  Universe diagnostics (250 days):
    Avg stability score  : 0.282  (0=fully churning, 1=static)
    Avg daily turnover   : 58.4%
    Avg leader half-life : 1.8 days
    Stability vs PnL corr: +0.058  (>0 = stable universe → better trades)
    Turnover vs success  : +0.009  (<0 = higher churn → fewer successes)
  ──────────────────────────────────────────────────────────────────
  Per-regime breakdown (entry regime):
    Regime                           N  WinRate    AvgRet
    HIGH_VOL_SIDEWAYS              111    60.4%    -0.16%
    HIGH_VOL_UPTREND              1245    49.0%     0.68%
    LOW_VOL_SIDEWAYS               292    65.1%     3.61%
    LOW_VOL_UPTREND                696    51.7%     1.28%
    MID_VOL_SIDEWAYS               155    65.8%     2.35%
    MID_VOL_UPTREND                806    52.2%     1.10%
  ──────────────────────────────────────────────────────────────────
  ══════════════════════════════════════════════════════════════════
[DynamicUniverseAgent] Bulk fetching 150 symbols from 2019-09-14 to 2021-12-31 ...
[DynamicUniverseAgent] Loaded 149 symbols. Skipped 1: TMCV(no data)

======================================================================
  Period: Recov 2020–2021   (2020-04-01 → 2021-12-31)
  Universe: 150 symbols → DynamicUniverse top 80 → UniverseSelection top 20
  Costs: 0.10% commission + 0.05% slippage per side (all returns net of costs)
======================================================================
  Strategy               Sharpe    Return    MaxDD      PF     WR  #Trades
  --------------------------------------------------------------------  [Medium-term]
  DualMA SMA20/50          1.87    51.22%    9.01%    2.40  52.7%      169
  --------------------------------------------------------------------  [Short-term]
  Breakout 10d             2.62   105.97%   11.72%    1.79  44.6%      822
  QuietBrk 20d             2.42    92.87%   14.52%    1.91  43.6%      546
  TrendPB v2 pct=3%        1.24    29.13%    9.93%    1.36  60.2%      782
  TrendPB v2 pct=5%        1.30    23.55%    6.96%    1.49  60.9%      460
  --------------------------------------------------------------------  [Mean-reversion]
  RSI-MR  os=5  ob=80      1.31    32.35%    7.52%    1.34  58.8%      873
  --------------------------------------------------------------------  [Multi-strategy baseline — equal weight]
  EqualWeight (5-strat)    2.59    50.00%    6.14%    1.75  54.0%     2502

  --------------------------------------------------------------------  [Strategy PnL Attribution — EqualWeight]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  Breakout         1452       +32237     49.3%        +22    65.9%
  RSI-MR            674        +8896     60.7%        +13    18.2%
  TrendPB           293        +4325     62.5%        +15     8.8%
  DualMA             83        +3464     53.0%        +42     7.1%
  TOTAL            2502       +48922
  --------------------------------------------------------------------  [EqualWeight — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  cross_ex  gated_off  pass_thru%
  DualMA          17847   13155       4667         25       39         0          0       73.5%
  Breakout        15894    3574       9028       3292      551         0          0       19.0%
  QuietBrk        13307       0      11521       1786        0         0          0        0.0%
  TrendPB         14520    2293       6390          0      150       694       5837       14.8%
  RSI-MR          15020    1559       8977       4484      249         0          0        8.7%
  gate: open 76/435 days (17.5%) — closed 359/435 days
  --------------------------------------------------------------------  [Multi-strategy adaptive — LLM weights]
  [AdaptiveSelector] 2020-04-02 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.30  QuietBrk=0.10  TrendPB=0.40  RSI-MR=0.00
  [AdaptiveSelector] 2020-04-07 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.30  QuietBrk=0.10  TrendPB=0.40  RSI-MR=0.00
  [AdaptiveSelector] 2020-04-12 [CRASH_HIGHVOL/HIGH] → DualMA=0.25  Breakout=0.30  QuietBrk=0.05  TrendPB=0.40  RSI-MR=0.00
  [AdaptiveSelector] 2020-04-19 [CRASH_HIGHVOL/HIGH] → DualMA=0.25  Breakout=0.30  QuietBrk=0.05  TrendPB=0.40  RSI-MR=0.00
  [AdaptiveSelector] 2020-04-26 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.30  QuietBrk=0.05  TrendPB=0.45  RSI-MR=0.00
  [AdaptiveSelector] 2020-05-03 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.30  QuietBrk=0.10  TrendPB=0.40  RSI-MR=0.00
  [AdaptiveSelector] 2020-05-10 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.30  QuietBrk=0.10  TrendPB=0.40  RSI-MR=0.00
  [AdaptiveSelector] 2020-05-17 [CRASH_HIGHVOL/HIGH] → DualMA=0.25  Breakout=0.30  QuietBrk=0.05  TrendPB=0.40  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2020-05-25 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.30  QuietBrk=0.10  TrendPB=0.40  RSI-MR=0.00
  [AdaptiveSelector] Regime transition confirmed: CRASH_HIGHVOL → MIXED (after 2 weeks)
  [AdaptiveSelector] 2020-05-31 [MIXED/LOW] → DualMA=0.25  Breakout=0.25  QuietBrk=0.25  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: RECOVERY (1/2 weeks) — holding MIXED
  [AdaptiveSelector] 2020-06-07 [MIXED/LOW] → DualMA=0.25  Breakout=0.25  QuietBrk=0.25  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime transition confirmed: MIXED → RECOVERY (after 2 weeks)
  [AdaptiveSelector] 2020-06-14 [RECOVERY/HIGH] → DualMA=0.21  Breakout=0.37  QuietBrk=0.26  TrendPB=0.11  RSI-MR=0.05
  [AdaptiveSelector] 2020-06-21 [RECOVERY/HIGH] → DualMA=0.21  Breakout=0.37  QuietBrk=0.26  TrendPB=0.11  RSI-MR=0.05
  [AdaptiveSelector] 2020-06-28 [RECOVERY/HIGH] → DualMA=0.21  Breakout=0.37  QuietBrk=0.26  TrendPB=0.11  RSI-MR=0.05
  [AdaptiveSelector] 2020-07-05 [RECOVERY/HIGH] → DualMA=0.22  Breakout=0.39  QuietBrk=0.28  TrendPB=0.11  RSI-MR=0.00
  [AdaptiveSelector] 2020-07-12 [RECOVERY/HIGH] → DualMA=0.21  Breakout=0.37  QuietBrk=0.26  TrendPB=0.11  RSI-MR=0.05
  [AdaptiveSelector] 2020-07-19 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-07-26 [RECOVERY/HIGH] → DualMA=0.21  Breakout=0.37  QuietBrk=0.26  TrendPB=0.11  RSI-MR=0.05
  [AdaptiveSelector] 2020-08-02 [RECOVERY/HIGH] → DualMA=0.20  Breakout=0.40  QuietBrk=0.25  TrendPB=0.10  RSI-MR=0.05
  [AdaptiveSelector] 2020-08-09 [RECOVERY/HIGH] → DualMA=0.21  Breakout=0.37  QuietBrk=0.26  TrendPB=0.11  RSI-MR=0.05
  [AdaptiveSelector] 2020-08-16 [RECOVERY/HIGH] → DualMA=0.21  Breakout=0.37  QuietBrk=0.26  TrendPB=0.11  RSI-MR=0.05
  [AdaptiveSelector] 2020-08-23 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-08-30 [RECOVERY/HIGH] → DualMA=0.22  Breakout=0.39  QuietBrk=0.28  TrendPB=0.11  RSI-MR=0.00
  [AdaptiveSelector] 2020-09-06 [RECOVERY/HIGH] → DualMA=0.21  Breakout=0.37  QuietBrk=0.26  TrendPB=0.11  RSI-MR=0.05
  [AdaptiveSelector] 2020-09-13 [RECOVERY/HIGH] → DualMA=0.17  Breakout=0.39  QuietBrk=0.28  TrendPB=0.11  RSI-MR=0.05
  [AdaptiveSelector] 2020-09-20 [RECOVERY/HIGH] → DualMA=0.21  Breakout=0.37  QuietBrk=0.26  TrendPB=0.11  RSI-MR=0.05
  [AdaptiveSelector] 2020-09-27 [RECOVERY/HIGH] → DualMA=0.17  Breakout=0.39  QuietBrk=0.28  TrendPB=0.11  RSI-MR=0.05
  [AdaptiveSelector] 2020-10-04 [RECOVERY/HIGH] → DualMA=0.21  Breakout=0.37  QuietBrk=0.26  TrendPB=0.11  RSI-MR=0.05
  [AdaptiveSelector] 2020-10-11 [RECOVERY/HIGH] → DualMA=0.21  Breakout=0.37  QuietBrk=0.26  TrendPB=0.11  RSI-MR=0.05
  [AdaptiveSelector] 2020-10-18 [RECOVERY/HIGH] → DualMA=0.21  Breakout=0.37  QuietBrk=0.26  TrendPB=0.11  RSI-MR=0.05
  [AdaptiveSelector] 2020-10-25 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-11-01 [RECOVERY/HIGH] → DualMA=0.17  Breakout=0.39  QuietBrk=0.28  TrendPB=0.11  RSI-MR=0.05
  [AdaptiveSelector] 2020-11-08 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-11-13 [RECOVERY/HIGH] → DualMA=0.21  Breakout=0.37  QuietBrk=0.26  TrendPB=0.11  RSI-MR=0.05
  [AdaptiveSelector] 2020-11-18 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-11-23 [RECOVERY/HIGH] → DualMA=0.17  Breakout=0.39  QuietBrk=0.28  TrendPB=0.11  RSI-MR=0.05
  [AdaptiveSelector] 2020-11-30 [RECOVERY/HIGH] → DualMA=0.21  Breakout=0.37  QuietBrk=0.26  TrendPB=0.11  RSI-MR=0.05
  [AdaptiveSelector] 2020-12-06 [RECOVERY/HIGH] → DualMA=0.20  Breakout=0.40  QuietBrk=0.30  TrendPB=0.05  RSI-MR=0.05
  [AdaptiveSelector] 2020-12-13 [RECOVERY/HIGH] → DualMA=0.20  Breakout=0.40  QuietBrk=0.30  TrendPB=0.05  RSI-MR=0.05
  [AdaptiveSelector] 2020-12-20 [RECOVERY/HIGH] → DualMA=0.20  Breakout=0.40  QuietBrk=0.30  TrendPB=0.05  RSI-MR=0.05
  [AdaptiveSelector] 2020-12-27 [RECOVERY/HIGH] → DualMA=0.20  Breakout=0.40  QuietBrk=0.30  TrendPB=0.05  RSI-MR=0.05
  [AdaptiveSelector] 2021-01-03 [RECOVERY/HIGH] → DualMA=0.21  Breakout=0.37  QuietBrk=0.26  TrendPB=0.11  RSI-MR=0.05
  [AdaptiveSelector] 2021-01-10 [RECOVERY/HIGH] → DualMA=0.21  Breakout=0.37  QuietBrk=0.26  TrendPB=0.11  RSI-MR=0.05
  [AdaptiveSelector] 2021-01-17 [RECOVERY/HIGH] → DualMA=0.21  Breakout=0.37  QuietBrk=0.26  TrendPB=0.11  RSI-MR=0.05
  [AdaptiveSelector] 2021-01-24 [RECOVERY/HIGH] → DualMA=0.21  Breakout=0.37  QuietBrk=0.26  TrendPB=0.11  RSI-MR=0.05
  [AdaptiveSelector] 2021-01-31 [RECOVERY/HIGH] → DualMA=0.21  Breakout=0.37  QuietBrk=0.26  TrendPB=0.11  RSI-MR=0.05
  [AdaptiveSelector] 2021-02-07 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2021-02-14 [RECOVERY/HIGH] → DualMA=0.21  Breakout=0.37  QuietBrk=0.26  TrendPB=0.11  RSI-MR=0.05
  [AdaptiveSelector] 2021-02-21 [RECOVERY/HIGH] → DualMA=0.21  Breakout=0.37  QuietBrk=0.26  TrendPB=0.11  RSI-MR=0.05
  [AdaptiveSelector] 2021-02-28 [RECOVERY/HIGH] → DualMA=0.17  Breakout=0.39  QuietBrk=0.28  TrendPB=0.11  RSI-MR=0.05
  [AdaptiveSelector] 2021-03-07 [RECOVERY/HIGH] → DualMA=0.21  Breakout=0.37  QuietBrk=0.26  TrendPB=0.11  RSI-MR=0.05
  [AdaptiveSelector] 2021-03-14 [RECOVERY/HIGH] → DualMA=0.21  Breakout=0.37  QuietBrk=0.26  TrendPB=0.11  RSI-MR=0.05
  [AdaptiveSelector] 2021-03-21 [RECOVERY/HIGH] → DualMA=0.21  Breakout=0.37  QuietBrk=0.26  TrendPB=0.11  RSI-MR=0.05
  [AdaptiveSelector] 2021-03-29 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2021-04-04 [RECOVERY/HIGH] → DualMA=0.20  Breakout=0.40  QuietBrk=0.25  TrendPB=0.10  RSI-MR=0.05
  [AdaptiveSelector] Regime transition confirmed: RECOVERY → MIXED (after 2 weeks)
  [AdaptiveSelector] 2021-04-11 [MIXED/LOW] → DualMA=0.25  Breakout=0.25  QuietBrk=0.25  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: CRASH_HIGHVOL (1/2 weeks) — holding MIXED
  [AdaptiveSelector] 2021-04-18 [MIXED/LOW] → DualMA=0.25  Breakout=0.25  QuietBrk=0.25  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding MIXED
  [AdaptiveSelector] 2021-04-25 [MIXED/LOW] → DualMA=0.25  Breakout=0.25  QuietBrk=0.25  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2021-05-02 [MIXED/LOW] → DualMA=0.25  Breakout=0.25  QuietBrk=0.25  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: RECOVERY (1/2 weeks) — holding MIXED
  [AdaptiveSelector] 2021-05-09 [MIXED/LOW] → DualMA=0.25  Breakout=0.25  QuietBrk=0.25  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime transition confirmed: MIXED → RECOVERY (after 2 weeks)
  [AdaptiveSelector] 2021-05-16 [RECOVERY/HIGH] → DualMA=0.21  Breakout=0.37  QuietBrk=0.26  TrendPB=0.11  RSI-MR=0.05
  [AdaptiveSelector] 2021-05-23 [RECOVERY/HIGH] → DualMA=0.21  Breakout=0.37  QuietBrk=0.26  TrendPB=0.11  RSI-MR=0.05
  [AdaptiveSelector] 2021-05-30 [RECOVERY/HIGH] → DualMA=0.21  Breakout=0.37  QuietBrk=0.26  TrendPB=0.11  RSI-MR=0.05
  [AdaptiveSelector] 2021-06-06 [RECOVERY/HIGH] → DualMA=0.21  Breakout=0.37  QuietBrk=0.26  TrendPB=0.11  RSI-MR=0.05
  [AdaptiveSelector] 2021-06-13 [RECOVERY/HIGH] → DualMA=0.20  Breakout=0.40  QuietBrk=0.30  TrendPB=0.05  RSI-MR=0.05
  [AdaptiveSelector] 2021-06-20 [RECOVERY/HIGH] → DualMA=0.21  Breakout=0.37  QuietBrk=0.26  TrendPB=0.11  RSI-MR=0.05
  [AdaptiveSelector] 2021-06-27 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2021-07-04 [RECOVERY/HIGH] → DualMA=0.21  Breakout=0.37  QuietBrk=0.26  TrendPB=0.11  RSI-MR=0.05
  [AdaptiveSelector] 2021-07-11 [RECOVERY/HIGH] → DualMA=0.20  Breakout=0.40  QuietBrk=0.25  TrendPB=0.10  RSI-MR=0.05
  [AdaptiveSelector] 2021-07-18 [RECOVERY/HIGH] → DualMA=0.21  Breakout=0.37  QuietBrk=0.26  TrendPB=0.11  RSI-MR=0.05
  [AdaptiveSelector] 2021-07-25 [RECOVERY/HIGH] → DualMA=0.21  Breakout=0.37  QuietBrk=0.26  TrendPB=0.11  RSI-MR=0.05
  [AdaptiveSelector] 2021-08-01 [RECOVERY/HIGH] → DualMA=0.21  Breakout=0.37  QuietBrk=0.26  TrendPB=0.11  RSI-MR=0.05
  [AdaptiveSelector] 2021-08-08 [RECOVERY/HIGH] → DualMA=0.21  Breakout=0.37  QuietBrk=0.26  TrendPB=0.11  RSI-MR=0.05
  [AdaptiveSelector] 2021-08-15 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2021-08-22 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2021-08-29 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2021-09-05 [RECOVERY/HIGH] → DualMA=0.21  Breakout=0.37  QuietBrk=0.26  TrendPB=0.11  RSI-MR=0.05
  [AdaptiveSelector] 2021-09-12 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2021-09-19 [RECOVERY/HIGH] → DualMA=0.21  Breakout=0.37  QuietBrk=0.26  TrendPB=0.11  RSI-MR=0.05
  [AdaptiveSelector] 2021-09-26 [RECOVERY/HIGH] → DualMA=0.17  Breakout=0.39  QuietBrk=0.28  TrendPB=0.11  RSI-MR=0.05
  [AdaptiveSelector] 2021-10-03 [RECOVERY/HIGH] → DualMA=0.21  Breakout=0.37  QuietBrk=0.26  TrendPB=0.11  RSI-MR=0.05
  [AdaptiveSelector] 2021-10-10 [RECOVERY/HIGH] → DualMA=0.21  Breakout=0.37  QuietBrk=0.26  TrendPB=0.11  RSI-MR=0.05
  [AdaptiveSelector] 2021-10-17 [RECOVERY/HIGH] → DualMA=0.21  Breakout=0.37  QuietBrk=0.26  TrendPB=0.11  RSI-MR=0.05
  [AdaptiveSelector] 2021-10-24 [RECOVERY/HIGH] → DualMA=0.20  Breakout=0.40  QuietBrk=0.25  TrendPB=0.10  RSI-MR=0.05
  [AdaptiveSelector] 2021-10-31 [RECOVERY/HIGH] → DualMA=0.17  Breakout=0.39  QuietBrk=0.28  TrendPB=0.11  RSI-MR=0.05
  [AdaptiveSelector] 2021-11-07 [RECOVERY/HIGH] → DualMA=0.17  Breakout=0.39  QuietBrk=0.28  TrendPB=0.11  RSI-MR=0.05
  [AdaptiveSelector] 2021-11-14 [RECOVERY/HIGH] → DualMA=0.21  Breakout=0.37  QuietBrk=0.26  TrendPB=0.11  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2021-11-21 [RECOVERY/HIGH] → DualMA=0.17  Breakout=0.39  QuietBrk=0.28  TrendPB=0.11  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: CRASH_HIGHVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2021-11-28 [RECOVERY/HIGH] → DualMA=0.21  Breakout=0.37  QuietBrk=0.26  TrendPB=0.11  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2021-12-05 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime transition confirmed: RECOVERY → BULL_MEDVOL (after 2 weeks)
  [AdaptiveSelector] 2021-12-12 [BULL_MEDVOL/MEDIUM] → DualMA=0.21  Breakout=0.26  QuietBrk=0.21  TrendPB=0.26  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: CRASH_HIGHVOL (1/2 weeks) — holding BULL_MEDVOL
  [AdaptiveSelector] 2021-12-19 [BULL_MEDVOL/MEDIUM] → DualMA=0.21  Breakout=0.26  QuietBrk=0.21  TrendPB=0.26  RSI-MR=0.05
  [AdaptiveSelector] 2021-12-26 [BULL_MEDVOL/MEDIUM] → DualMA=0.22  Breakout=0.28  QuietBrk=0.22  TrendPB=0.22  RSI-MR=0.05
  Adaptive  (5-strat)      2.53    60.65%    8.15%    1.67  53.2%     2142
                         (LLM calls: 93)

  --------------------------------------------------------------------  [Strategy PnL Attribution — Adaptive]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  Breakout         1533       +52981     49.5%        +35    87.7%
  DualMA             47        +3816     68.1%        +81     6.3%
  TrendPB           244        +2392     61.9%        +10     4.0%
  RSI-MR            318        +1201     62.3%         +4     2.0%
  TOTAL            2142       +60390
  --------------------------------------------------------------------  [Adaptive — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  cross_ex  gated_off  pass_thru%
  DualMA          17040    4790      12229         21       27         0          0       28.0%
  Breakout        14398   10826       1545       2027      560         0          0       71.3%
  QuietBrk        12311     452      10707       1152        0         0          0        3.7%
  TrendPB         12886    1943       5188          0      216       752       5755       13.4%
  RSI-MR          12138    1232       6918       3988      629         0          0        5.0%
  gate: open 74/435 days (17.0%) — closed 361/435 days
  --------------------------------------------------------------------  [Multi-strategy adaptive + RegimeContextAgent]
  Adaptive+RCA (5-strat)   2.16    53.89%    9.10%    1.58  51.4%     2146
                         (LLM calls: 93)

  --------------------------------------------------------------------  [Strategy PnL Attribution — Adaptive+RCA]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  Breakout         1559       +47696     48.0%        +31    89.1%
  TrendPB           253        +3143     60.9%        +12     5.9%
  DualMA             45        +1699     48.9%        +38     3.2%
  RSI-MR            289        +1019     61.6%         +4     1.9%
  TOTAL            2146       +53557
  --------------------------------------------------------------------  [Adaptive+RCA — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  cross_ex  gated_off  pass_thru%
  DualMA          16996    4269      12708         19       24         0          0       25.0%
  Breakout        14321   11332       1006       1983      542         0          0       75.3%
  QuietBrk        12231     478      10597       1156        0         0          0        3.9%
  TrendPB         12808    1935       5199          0      215       734       5674       13.4%
  RSI-MR          11218    1131       6362       3725      582         0          0        4.9%
  gate: open 70/435 days (16.1%) — closed 365/435 days
  RCA delta              -0.37    -6.75%

  ══════════════════════════════════════════════════════════════════
  OPPORTUNITY QUALITY SUMMARY  [Recov 2020–2021]
  ══════════════════════════════════════════════════════════════════
  Trades analyzed  : 6790  (3595 winners / 3195 losers)
  ──────────────────────────────────────────────────────────────────
  Breakout quality:
    Follow-through rate  :   53.5%   (price continued post-exit)
    False breakout rate  :   31.1%   (MFE>2% but final return <0)
    Persistence half-life:    0.0 days (median survival above entry)
    Avg MFE efficiency   : -0.056      (1.00 = exit at peak)
  ──────────────────────────────────────────────────────────────────
  Continuation decay (post-exit drift):
                      1D        3D        5D
    Winners      -0.21%    +0.53%    +1.07%
    Losers       -0.06%    +0.32%    +0.76%
  ──────────────────────────────────────────────────────────────────
  Universe diagnostics (435 days):
    Avg stability score  : 0.276  (0=fully churning, 1=static)
    Avg daily turnover   : 59.1%
    Avg leader half-life : 1.8 days
    Stability vs PnL corr: +0.010  (>0 = stable universe → better trades)
    Turnover vs success  : -0.038  (<0 = higher churn → fewer successes)
  ──────────────────────────────────────────────────────────────────
  Per-regime breakdown (entry regime):
    Regime                           N  WinRate    AvgRet
    HIGH_VOL_SIDEWAYS              351    57.8%     0.79%
    HIGH_VOL_UPTREND              3416    51.6%     0.96%
    LOW_VOL_SIDEWAYS               341    65.1%     4.16%
    LOW_VOL_UPTREND                835    50.8%     1.30%
    MID_VOL_SIDEWAYS               373    57.6%     1.84%
    MID_VOL_UPTREND               1474    52.1%     1.29%
  ──────────────────────────────────────────────────────────────────
  ══════════════════════════════════════════════════════════════════


  


  ######################################################################
  VARIANT C — Cross-exit with PERFORMANCE GATE
  cross_exit_strategies = {'TrendPB'}
  gate: allow cross-exit only when rolling-20-trade WR(Breakout) < 0.40
  override: gate CLOSED if recent-5-trade WR(Breakout) ≥ 0.60  (positive-momentum)
  warmup: gate stays CLOSED until 20 fills accrue
######################################################################

[PERIODS_FILTER active] running 1 of 7: Recov 2020–2021
[DynamicUniverseAgent] Bulk fetching 150 symbols from 2019-09-14 to 2021-12-31 ...
[DynamicUniverseAgent] Loaded 149 symbols. Skipped 1: TMCV(no data)

======================================================================
  Period: Recov 2020–2021   (2020-04-01 → 2021-12-31)
  Universe: 150 symbols → DynamicUniverse top 80 → UniverseSelection top 20
  Costs: 0.10% commission + 0.05% slippage per side (all returns net of costs)
======================================================================
  Strategy               Sharpe    Return    MaxDD      PF     WR  #Trades
  --------------------------------------------------------------------  [Medium-term]
  DualMA SMA20/50          1.87    51.22%    9.01%    2.40  52.7%      169
  --------------------------------------------------------------------  [Short-term]
  Breakout 10d             2.62   105.97%   11.72%    1.79  44.6%      822
  QuietBrk 20d             2.42    92.87%   14.52%    1.91  43.6%      546
  TrendPB v2 pct=3%        1.24    29.13%    9.93%    1.36  60.2%      782
  TrendPB v2 pct=5%        1.30    23.55%    6.96%    1.49  60.9%      460
  --------------------------------------------------------------------  [Mean-reversion]
  RSI-MR  os=5  ob=80      1.31    32.35%    7.52%    1.34  58.8%      873
  --------------------------------------------------------------------  [Multi-strategy baseline — equal weight]
  EqualWeight (5-strat)    2.16    39.49%    6.19%    1.61  53.5%     2497

  --------------------------------------------------------------------  [Strategy PnL Attribution — EqualWeight]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  Breakout         1470       +24882     48.7%        +17    63.3%
  RSI-MR            662        +7752     60.4%        +12    19.7%
  TrendPB           283        +3802     62.2%        +13     9.7%
  DualMA             82        +2875     53.7%        +35     7.3%
  TOTAL            2497       +39312
  --------------------------------------------------------------------  [EqualWeight — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  cross_ex  gated_off  pass_thru%
  DualMA          17938   13224       4688         26       39         0          0       73.5%
  Breakout        15985    3635       9096       3254      566         0          0       19.2%
  QuietBrk        13428       0      11653       1775        0         0          0        0.0%
  TrendPB         14572    2237       6484          0      156       671       5851       14.3%
  RSI-MR          15076    1549       9071       4456      262         0          0        8.5%
  gate: open 75/435 days (17.2%) — closed 360/435 days
  --------------------------------------------------------------------  [Multi-strategy adaptive — LLM weights]
  [AdaptiveSelector] 2020-04-02 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.30  QuietBrk=0.10  TrendPB=0.40  RSI-MR=0.00
  [AdaptiveSelector] 2020-04-07 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.30  QuietBrk=0.10  TrendPB=0.40  RSI-MR=0.00
  [AdaptiveSelector] 2020-04-12 [CRASH_HIGHVOL/HIGH] → DualMA=0.25  Breakout=0.30  QuietBrk=0.05  TrendPB=0.40  RSI-MR=0.00
  [AdaptiveSelector] 2020-04-19 [CRASH_HIGHVOL/HIGH] → DualMA=0.25  Breakout=0.30  QuietBrk=0.05  TrendPB=0.40  RSI-MR=0.00
  [AdaptiveSelector] 2020-04-26 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.30  QuietBrk=0.05  TrendPB=0.45  RSI-MR=0.00
  [AdaptiveSelector] 2020-05-03 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.30  QuietBrk=0.10  TrendPB=0.40  RSI-MR=0.00
  [AdaptiveSelector] 2020-05-10 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.30  QuietBrk=0.05  TrendPB=0.45  RSI-MR=0.00
  [AdaptiveSelector] 2020-05-17 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.30  QuietBrk=0.10  TrendPB=0.40  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2020-05-25 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.30  QuietBrk=0.10  TrendPB=0.40  RSI-MR=0.00
  [AdaptiveSelector] Regime transition confirmed: CRASH_HIGHVOL → MIXED (after 2 weeks)
  [AdaptiveSelector] 2020-05-31 [MIXED/LOW] → DualMA=0.25  Breakout=0.25  QuietBrk=0.25  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: RECOVERY (1/2 weeks) — holding MIXED
  [AdaptiveSelector] 2020-06-07 [MIXED/LOW] → DualMA=0.25  Breakout=0.25  QuietBrk=0.25  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime transition confirmed: MIXED → RECOVERY (after 2 weeks)
  [AdaptiveSelector] 2020-06-14 [RECOVERY/HIGH] → DualMA=0.21  Breakout=0.37  QuietBrk=0.26  TrendPB=0.11  RSI-MR=0.05
  [AdaptiveSelector] 2020-06-21 [RECOVERY/HIGH] → DualMA=0.21  Breakout=0.37  QuietBrk=0.26  TrendPB=0.11  RSI-MR=0.05
  [AdaptiveSelector] 2020-06-28 [RECOVERY/HIGH] → DualMA=0.21  Breakout=0.37  QuietBrk=0.26  TrendPB=0.11  RSI-MR=0.05
  [AdaptiveSelector] 2020-07-05 [RECOVERY/HIGH] → DualMA=0.22  Breakout=0.39  QuietBrk=0.28  TrendPB=0.11  RSI-MR=0.00
  [AdaptiveSelector] 2020-07-12 [RECOVERY/HIGH] → DualMA=0.21  Breakout=0.37  QuietBrk=0.26  TrendPB=0.11  RSI-MR=0.05
  [AdaptiveSelector] 2020-07-19 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-07-26 [RECOVERY/HIGH] → DualMA=0.21  Breakout=0.37  QuietBrk=0.26  TrendPB=0.11  RSI-MR=0.05
  [AdaptiveSelector] 2020-08-02 [RECOVERY/HIGH] → DualMA=0.20  Breakout=0.40  QuietBrk=0.25  TrendPB=0.10  RSI-MR=0.05
  [AdaptiveSelector] 2020-08-09 [RECOVERY/HIGH] → DualMA=0.21  Breakout=0.37  QuietBrk=0.26  TrendPB=0.11  RSI-MR=0.05
  [AdaptiveSelector] 2020-08-16 [RECOVERY/HIGH] → DualMA=0.21  Breakout=0.37  QuietBrk=0.26  TrendPB=0.11  RSI-MR=0.05
  [AdaptiveSelector] 2020-08-23 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-08-30 [RECOVERY/HIGH] → DualMA=0.22  Breakout=0.39  QuietBrk=0.28  TrendPB=0.11  RSI-MR=0.00
  [AdaptiveSelector] 2020-09-06 [RECOVERY/HIGH] → DualMA=0.21  Breakout=0.37  QuietBrk=0.26  TrendPB=0.11  RSI-MR=0.05
  [AdaptiveSelector] 2020-09-13 [RECOVERY/HIGH] → DualMA=0.17  Breakout=0.39  QuietBrk=0.28  TrendPB=0.11  RSI-MR=0.05
  [AdaptiveSelector] 2020-09-20 [RECOVERY/HIGH] → DualMA=0.21  Breakout=0.37  QuietBrk=0.26  TrendPB=0.11  RSI-MR=0.05
  [AdaptiveSelector] 2020-09-27 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-10-04 [RECOVERY/HIGH] → DualMA=0.20  Breakout=0.40  QuietBrk=0.30  TrendPB=0.05  RSI-MR=0.05
  [AdaptiveSelector] 2020-10-11 [RECOVERY/HIGH] → DualMA=0.21  Breakout=0.37  QuietBrk=0.26  TrendPB=0.11  RSI-MR=0.05
  [AdaptiveSelector] 2020-10-18 [RECOVERY/HIGH] → DualMA=0.20  Breakout=0.40  QuietBrk=0.30  TrendPB=0.05  RSI-MR=0.05
  [AdaptiveSelector] 2020-10-25 [RECOVERY/HIGH] → DualMA=0.21  Breakout=0.37  QuietBrk=0.26  TrendPB=0.11  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2020-11-01 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-11-08 [RECOVERY/HIGH] → DualMA=0.17  Breakout=0.39  QuietBrk=0.28  TrendPB=0.11  RSI-MR=0.05
  [AdaptiveSelector] 2020-11-13 [RECOVERY/HIGH] → DualMA=0.21  Breakout=0.37  QuietBrk=0.26  TrendPB=0.11  RSI-MR=0.05
  [AdaptiveSelector] 2020-11-18 [RECOVERY/HIGH] → DualMA=0.21  Breakout=0.37  QuietBrk=0.26  TrendPB=0.11  RSI-MR=0.05
  [AdaptiveSelector] 2020-11-23 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-11-30 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-12-06 [RECOVERY/HIGH] → DualMA=0.22  Breakout=0.39  QuietBrk=0.28  TrendPB=0.11  RSI-MR=0.00
  [AdaptiveSelector] 2020-12-13 [RECOVERY/HIGH] → DualMA=0.21  Breakout=0.37  QuietBrk=0.26  TrendPB=0.11  RSI-MR=0.05
  [AdaptiveSelector] 2020-12-20 [RECOVERY/HIGH] → DualMA=0.21  Breakout=0.37  QuietBrk=0.26  TrendPB=0.11  RSI-MR=0.05
  [AdaptiveSelector] 2020-12-27 [RECOVERY/HIGH] → DualMA=0.20  Breakout=0.40  QuietBrk=0.30  TrendPB=0.05  RSI-MR=0.05
  [AdaptiveSelector] 2021-01-03 [RECOVERY/HIGH] → DualMA=0.21  Breakout=0.37  QuietBrk=0.26  TrendPB=0.11  RSI-MR=0.05
  [AdaptiveSelector] 2021-01-10 [RECOVERY/HIGH] → DualMA=0.21  Breakout=0.37  QuietBrk=0.26  TrendPB=0.11  RSI-MR=0.05
  [AdaptiveSelector] 2021-01-17 [RECOVERY/HIGH] → DualMA=0.20  Breakout=0.40  QuietBrk=0.30  TrendPB=0.05  RSI-MR=0.05
  [AdaptiveSelector] 2021-01-24 [RECOVERY/HIGH] → DualMA=0.21  Breakout=0.37  QuietBrk=0.26  TrendPB=0.11  RSI-MR=0.05
  [AdaptiveSelector] 2021-01-31 [RECOVERY/HIGH] → DualMA=0.21  Breakout=0.37  QuietBrk=0.26  TrendPB=0.11  RSI-MR=0.05
  [AdaptiveSelector] 2021-02-07 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2021-02-14 [RECOVERY/HIGH] → DualMA=0.21  Breakout=0.37  QuietBrk=0.26  TrendPB=0.11  RSI-MR=0.05
  [AdaptiveSelector] 2021-02-21 [RECOVERY/HIGH] → DualMA=0.21  Breakout=0.37  QuietBrk=0.26  TrendPB=0.11  RSI-MR=0.05
  [AdaptiveSelector] 2021-02-28 [RECOVERY/HIGH] → DualMA=0.17  Breakout=0.39  QuietBrk=0.28  TrendPB=0.11  RSI-MR=0.05
  [AdaptiveSelector] 2021-03-07 [RECOVERY/HIGH] → DualMA=0.21  Breakout=0.37  QuietBrk=0.26  TrendPB=0.11  RSI-MR=0.05
  [AdaptiveSelector] 2021-03-14 [RECOVERY/HIGH] → DualMA=0.21  Breakout=0.37  QuietBrk=0.26  TrendPB=0.11  RSI-MR=0.05
  [AdaptiveSelector] 2021-03-21 [RECOVERY/HIGH] → DualMA=0.21  Breakout=0.37  QuietBrk=0.26  TrendPB=0.11  RSI-MR=0.05
  [AdaptiveSelector] 2021-03-29 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2021-04-04 [RECOVERY/HIGH] → DualMA=0.21  Breakout=0.37  QuietBrk=0.26  TrendPB=0.11  RSI-MR=0.05
  [AdaptiveSelector] Regime transition confirmed: RECOVERY → MIXED (after 2 weeks)
  [AdaptiveSelector] 2021-04-11 [MIXED/LOW] → DualMA=0.25  Breakout=0.25  QuietBrk=0.25  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: CRASH_HIGHVOL (1/2 weeks) — holding MIXED
  [AdaptiveSelector] 2021-04-18 [MIXED/LOW] → DualMA=0.25  Breakout=0.25  QuietBrk=0.25  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2021-04-25 [MIXED/LOW] → DualMA=0.25  Breakout=0.25  QuietBrk=0.25  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2021-05-02 [MIXED/LOW] → DualMA=0.25  Breakout=0.25  QuietBrk=0.25  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: RECOVERY (1/2 weeks) — holding MIXED
  [AdaptiveSelector] 2021-05-09 [MIXED/LOW] → DualMA=0.25  Breakout=0.25  QuietBrk=0.25  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime transition confirmed: MIXED → RECOVERY (after 2 weeks)
  [AdaptiveSelector] 2021-05-16 [RECOVERY/HIGH] → DualMA=0.21  Breakout=0.37  QuietBrk=0.26  TrendPB=0.11  RSI-MR=0.05
  [AdaptiveSelector] 2021-05-23 [RECOVERY/HIGH] → DualMA=0.21  Breakout=0.37  QuietBrk=0.26  TrendPB=0.11  RSI-MR=0.05
  [AdaptiveSelector] 2021-05-30 [RECOVERY/HIGH] → DualMA=0.21  Breakout=0.37  QuietBrk=0.26  TrendPB=0.11  RSI-MR=0.05
  [AdaptiveSelector] 2021-06-06 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2021-06-13 [RECOVERY/HIGH] → DualMA=0.21  Breakout=0.37  QuietBrk=0.26  TrendPB=0.11  RSI-MR=0.05
  [AdaptiveSelector] 2021-06-20 [RECOVERY/HIGH] → DualMA=0.21  Breakout=0.37  QuietBrk=0.26  TrendPB=0.11  RSI-MR=0.05
  [AdaptiveSelector] 2021-06-27 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2021-07-04 [RECOVERY/HIGH] → DualMA=0.21  Breakout=0.37  QuietBrk=0.26  TrendPB=0.11  RSI-MR=0.05
  [AdaptiveSelector] 2021-07-11 [RECOVERY/HIGH] → DualMA=0.21  Breakout=0.37  QuietBrk=0.26  TrendPB=0.11  RSI-MR=0.05
  [AdaptiveSelector] 2021-07-18 [RECOVERY/HIGH] → DualMA=0.20  Breakout=0.40  QuietBrk=0.25  TrendPB=0.10  RSI-MR=0.05
  [AdaptiveSelector] 2021-07-25 [RECOVERY/HIGH] → DualMA=0.21  Breakout=0.37  QuietBrk=0.26  TrendPB=0.11  RSI-MR=0.05
  [AdaptiveSelector] 2021-08-01 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2021-08-08 [RECOVERY/HIGH] → DualMA=0.21  Breakout=0.37  QuietBrk=0.26  TrendPB=0.11  RSI-MR=0.05
  [AdaptiveSelector] 2021-08-15 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2021-08-22 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2021-08-29 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2021-09-05 [RECOVERY/HIGH] → DualMA=0.21  Breakout=0.37  QuietBrk=0.26  TrendPB=0.11  RSI-MR=0.05
  [AdaptiveSelector] 2021-09-12 [RECOVERY/HIGH] → DualMA=0.21  Breakout=0.37  QuietBrk=0.26  TrendPB=0.11  RSI-MR=0.05
  [AdaptiveSelector] 2021-09-19 [RECOVERY/HIGH] → DualMA=0.21  Breakout=0.37  QuietBrk=0.26  TrendPB=0.11  RSI-MR=0.05
  [AdaptiveSelector] 2021-09-26 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2021-10-03 [RECOVERY/HIGH] → DualMA=0.21  Breakout=0.37  QuietBrk=0.26  TrendPB=0.11  RSI-MR=0.05
  [AdaptiveSelector] 2021-10-10 [RECOVERY/HIGH] → DualMA=0.21  Breakout=0.37  QuietBrk=0.26  TrendPB=0.11  RSI-MR=0.05
  [AdaptiveSelector] 2021-10-17 [RECOVERY/HIGH] → DualMA=0.21  Breakout=0.37  QuietBrk=0.26  TrendPB=0.11  RSI-MR=0.05
  [AdaptiveSelector] 2021-10-24 [RECOVERY/HIGH] → DualMA=0.21  Breakout=0.37  QuietBrk=0.26  TrendPB=0.11  RSI-MR=0.05
  [AdaptiveSelector] 2021-10-31 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2021-11-07 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2021-11-14 [RECOVERY/HIGH] → DualMA=0.21  Breakout=0.37  QuietBrk=0.26  TrendPB=0.11  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2021-11-21 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: CRASH_HIGHVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2021-11-28 [RECOVERY/HIGH] → DualMA=0.21  Breakout=0.37  QuietBrk=0.26  TrendPB=0.11  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2021-12-05 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime transition confirmed: RECOVERY → BULL_MEDVOL (after 2 weeks)
  [AdaptiveSelector] 2021-12-12 [BULL_MEDVOL/MEDIUM] → DualMA=0.21  Breakout=0.26  QuietBrk=0.21  TrendPB=0.26  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: CRASH_HIGHVOL (1/2 weeks) — holding BULL_MEDVOL
  [AdaptiveSelector] 2021-12-19 [BULL_MEDVOL/MEDIUM] → DualMA=0.21  Breakout=0.26  QuietBrk=0.21  TrendPB=0.26  RSI-MR=0.05
  [AdaptiveSelector] 2021-12-26 [BULL_MEDVOL/MEDIUM] → DualMA=0.22  Breakout=0.28  QuietBrk=0.22  TrendPB=0.22  RSI-MR=0.05
  Adaptive  (5-strat)      2.53    60.65%    8.38%    1.65  53.2%     2156
                         (LLM calls: 93)

  --------------------------------------------------------------------  [Strategy PnL Attribution — Adaptive]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  Breakout         1534       +51994     49.3%        +34    86.2%
  DualMA             52        +4373     69.2%        +84     7.3%
  TrendPB           254        +2621     63.4%        +10     4.3%
  RSI-MR            316        +1311     61.4%         +4     2.2%
  TOTAL            2156       +60299
  --------------------------------------------------------------------  [Adaptive — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  cross_ex  gated_off  pass_thru%
  DualMA          17122    4841      12262         19       27         0          0       28.1%
  Breakout        14517   10907       1569       2041      540         0          0       71.4%
  QuietBrk        12367     455      10748       1164        0         0          0        3.7%
  TrendPB         13029    1958       5285          0      208       746       5786       13.4%
  RSI-MR          11986    1228       6772       3986      618         0          0        5.1%
  gate: open 56/435 days (12.9%) — closed 379/435 days
  --------------------------------------------------------------------  [Multi-strategy adaptive + RegimeContextAgent]
  Adaptive+RCA (5-strat)   2.26    58.00%    8.11%    1.64  51.7%     2087
                         (LLM calls: 93)

  --------------------------------------------------------------------  [Strategy PnL Attribution — Adaptive+RCA]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  Breakout         1531       +51434     48.8%        +34    89.4%
  DualMA             43        +2865     58.1%        +67     5.0%
  TrendPB           242        +2252     61.6%         +9     3.9%
  RSI-MR            271         +979     58.7%         +4     1.7%
  TOTAL            2087       +57530
  --------------------------------------------------------------------  [Adaptive+RCA — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  cross_ex  gated_off  pass_thru%
  DualMA          17026    4221      12784         21       26         0          0       24.6%
  Breakout        14393   11562        957       1874      541         0          0       76.6%
  QuietBrk        12259     427      10764       1068        0         0          0        3.5%
  TrendPB         12914    1913       5082          0      225       694       5919       13.1%
  RSI-MR          11300    1113       6375       3812      596         0          0        4.6%
  gate: open 62/435 days (14.3%) — closed 373/435 days
  RCA delta              -0.27    -2.65%

  ══════════════════════════════════════════════════════════════════
  OPPORTUNITY QUALITY SUMMARY  [Recov 2020–2021]
  ══════════════════════════════════════════════════════════════════
  Trades analyzed  : 6740  (3563 winners / 3177 losers)
  ──────────────────────────────────────────────────────────────────
  Breakout quality:
    Follow-through rate  :   53.7%   (price continued post-exit)
    False breakout rate  :   31.4%   (MFE>2% but final return <0)
    Persistence half-life:    0.0 days (median survival above entry)
    Avg MFE efficiency   : -0.059      (1.00 = exit at peak)
  ──────────────────────────────────────────────────────────────────
  Continuation decay (post-exit drift):
                      1D        3D        5D
    Winners      -0.14%    +0.50%    +1.24%
    Losers       -0.07%    +0.30%    +0.73%
  ──────────────────────────────────────────────────────────────────
  Universe diagnostics (435 days):
    Avg stability score  : 0.276  (0=fully churning, 1=static)
    Avg daily turnover   : 59.1%
    Avg leader half-life : 1.8 days
    Stability vs PnL corr: +0.013  (>0 = stable universe → better trades)
    Turnover vs success  : -0.028  (<0 = higher churn → fewer successes)
  ──────────────────────────────────────────────────────────────────
  Per-regime breakdown (entry regime):
    Regime                           N  WinRate    AvgRet
    HIGH_VOL_SIDEWAYS              350    56.0%     0.68%
    HIGH_VOL_UPTREND              3360    52.2%     1.02%
    LOW_VOL_SIDEWAYS               338    62.1%     3.78%
    LOW_VOL_UPTREND                835    48.4%     1.15%
    MID_VOL_SIDEWAYS               371    59.0%     1.82%
    MID_VOL_UPTREND               1486    52.4%     1.23%
  ──────────────────────────────────────────────────────────────────
  ══════════════════════════════════════════════════════════════════

======================================================================
