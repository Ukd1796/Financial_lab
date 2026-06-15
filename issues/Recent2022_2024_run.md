# Regime Diagnostic Run — Recent2022–2024 — 2026-05-31 00:29

**Period:** Recent2022–2024  
**Log:** `issues/Recent2022_2024_regime_labels.jsonl`  
**Env:** `PYTHONHASHSEED=0`, `LLM_CACHE_ENABLED=1`, `ADAPTIVE_ONLY=0`

```

  [Cache] Loading 150 symbols from LOCAL SQLite (2014-01-01 → 2026-12-31)...
  [Cache] Local hit: 401,564 records for 150 symbols (no Supabase calls).


[PERIOD filter] Running 1 of 6 periods: Recent2022–2024
[DynamicUniverseAgent] Bulk fetching 150 symbols from 2021-06-15 to 2024-06-01 ...
[DynamicUniverseAgent] Loaded 149 symbols. Skipped 1: TMCV(no data)

======================================================================
  Period: Recent2022–2024   (2022-01-01 → 2024-06-01)
  Universe: 150 symbols → DynamicUniverse top 80 → UniverseSelection top 20
  Costs: 0.10% commission + 0.05% slippage per side (all returns net of costs)
======================================================================
  Strategy               Sharpe    Return    MaxDD      PF     WR  #Trades
  --------------------------------------------------------------------  [Medium-term]
  DualMA SMA20/50          0.49    10.25%   11.79%    1.16  40.5%      205
  --------------------------------------------------------------------  [Short-term]
  Breakout 10d             0.80    26.11%   13.00%    1.19  41.1%      894
  QuietBrk 20d             0.65    20.36%   18.27%    1.18  40.7%      573
  TrendPB v2 pct=3%        0.33     6.01%   15.19%    1.11  57.4%      563
  TrendPB v2 pct=5%        0.87    11.19%    7.31%    1.40  59.8%      266
  --------------------------------------------------------------------  [Mean-reversion]
  RSI-MR  os=5  ob=80     -0.28    -9.19%   18.38%    0.91  52.9%      908
  --------------------------------------------------------------------  [Multi-strategy baseline — equal weight]
  EqualWeight (5-strat)    1.13    22.42%    7.67%    1.35  45.5%     1933

  --------------------------------------------------------------------  [Strategy PnL Attribution — EqualWeight]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  Breakout         1049       +15242     41.8%        +15    77.0%
  QuietBrk          229        +1888     33.2%         +8     9.5%
  TrendPB           117        +1233     56.4%        +11     6.2%
  DualMA             61        +1069     52.5%        +18     5.4%
  RSI-MR            477         +359     55.8%         +1     1.8%
  TOTAL            1933       +19792
  --------------------------------------------------------------------  [EqualWeight — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  pass_thru%
  DualMA          17391   13788       3595          8       67       78.9%
  Breakout        17847    5426       9817       2604      963       25.0%
  QuietBrk         5465    1171       4139        155      235       17.1%
  TrendPB         14233     882       7647       5704      101        5.5%
  RSI-MR          15500    1793       9008       4699      539        8.1%

  --------------------------------------------------------------------  [EqualWeight — union-filter overlap (per trading day)]
  Filter                              total   max/day   mean/day
  BreakoutUniverseFilter                  0         0       0.00
  ActivityTailFilter                      0         0       0.00
  PullbackUniverseFilter                734         8       1.24
  MeanReversionUniverseFilter          2457        19       4.14
  DualMAUniverseFilter                 1376        16       2.32

  --------------------------------------------------------------------  [Exit Attribution — EqualWeight]
  Reason           Trades     %   WinRate    Avg PnL    Total PnL
  atr_stop            190   9.8%    63.7%      +95.0      +18058
  strategy           1743  90.2%    43.5%       +1.0       +1734

  Strategy       ATR%  Strat%   ATR WR   Strat WR   ATR Avg   Strat Avg
  Breakout       6.9%   93.1%    73.6%      39.5%   +154.5       +4.2
  DualMA        86.9%   13.1%    54.7%      37.5%    +22.4      -14.9
  QuietBrk      28.4%   71.6%    60.0%      22.6%    +88.4      -23.5
  RSI-MR         0.0%  100.0%     0.0%      55.8%     +0.0       +0.8
  TrendPB        0.0%  100.0%     0.0%      56.4%     +0.0      +10.5
  --------------------------------------------------------------------  [Multi-strategy adaptive — LLM weights]
  [AdaptiveSelector] 2022-01-02 [MIXED/LOW] → DualMA=0.25  Breakout=0.25  QuietBrk=0.25  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: RECOVERY (1/2 weeks) — holding MIXED
  [AdaptiveSelector] 2022-01-09 [MIXED/LOW] → DualMA=0.25  Breakout=0.25  QuietBrk=0.25  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime transition confirmed: MIXED → RECOVERY (after 2 weeks)
  [AdaptiveSelector] 2022-01-16 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [RCAQualityGate] 2022-01-18 → Breakout WR 35.0% < 40% over last 20 trades — CB relaxation disabled
  [AdaptiveSelector] Regime pending: CRASH_HIGHVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2022-01-23 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime transition confirmed: RECOVERY → CRASH_HIGHVOL (after 2 weeks)
  [AdaptiveSelector] 2022-01-30 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.45  TrendPB=0.10  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2022-02-06 [CRASH_HIGHVOL/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.40  TrendPB=0.00  RSI-MR=0.00
  [AdaptiveSelector] 2022-02-13 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2022-02-20 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2022-02-27 [CRASH_HIGHVOL/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.40  TrendPB=0.00  RSI-MR=0.00
  [AdaptiveSelector] 2022-03-06 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.45  TrendPB=0.10  RSI-MR=0.00
  [AdaptiveSelector] 2022-03-13 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2022-03-20 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2022-03-27 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2022-04-03 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: RECOVERY (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2022-04-10 [CRASH_HIGHVOL/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.25  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2022-04-17 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2022-04-24 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.35  TrendPB=0.20  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2022-05-01 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.35  TrendPB=0.20  RSI-MR=0.00
  [AdaptiveSelector] 2022-05-08 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2022-05-15 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.45  TrendPB=0.10  RSI-MR=0.00
  [AdaptiveSelector] 2022-05-22 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2022-05-29 [CRASH_HIGHVOL/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.25  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2022-06-05 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2022-06-12 [CRASH_HIGHVOL/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.25  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2022-06-19 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2022-06-26 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2022-07-03 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2022-07-10 [CRASH_HIGHVOL/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.25  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: RECOVERY (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2022-07-17 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime transition confirmed: CRASH_HIGHVOL → RECOVERY (after 2 weeks)
  [AdaptiveSelector] 2022-07-24 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2022-07-31 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2022-08-07 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2022-08-15 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2022-08-21 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2022-08-28 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2022-09-04 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2022-09-11 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2022-09-18 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2022-09-25 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2022-10-02 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2022-10-09 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2022-10-16 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2022-10-23 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2022-10-30 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2022-11-06 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2022-11-13 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2022-11-20 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2022-11-27 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2022-12-04 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2022-12-11 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2022-12-18 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2022-12-25 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: CRASH_HIGHVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2023-01-01 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2023-01-08 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2023-01-15 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime transition confirmed: RECOVERY → MIXED (after 2 weeks)
  [AdaptiveSelector] 2023-01-22 [MIXED/LOW] → DualMA=0.25  Breakout=0.25  QuietBrk=0.25  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: CRASH_HIGHVOL (1/2 weeks) — holding MIXED
  [AdaptiveSelector] 2023-01-29 [MIXED/LOW] → DualMA=0.15  Breakout=0.45  QuietBrk=0.25  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime transition confirmed: MIXED → CRASH_HIGHVOL (after 2 weeks)
  [AdaptiveSelector] 2023-02-05 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2023-02-12 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2023-02-19 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2023-02-26 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2023-03-05 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.35  TrendPB=0.20  RSI-MR=0.00
  [AdaptiveSelector] 2023-03-12 [CRASH_HIGHVOL/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.25  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2023-03-19 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2023-03-26 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2023-04-02 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2023-04-09 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2023-04-16 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: RECOVERY (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2023-04-23 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime transition confirmed: CRASH_HIGHVOL → RECOVERY (after 2 weeks)
  [AdaptiveSelector] 2023-05-01 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2023-05-07 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2023-05-14 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2023-05-21 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2023-05-28 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2023-06-04 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2023-06-11 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: BULL_SUSTAINED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2023-06-18 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2023-06-25 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2023-07-02 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2023-07-09 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2023-07-16 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2023-07-23 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2023-07-30 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2023-08-06 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.35  QuietBrk=0.30  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2023-08-13 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2023-08-20 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2023-08-27 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2023-09-03 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2023-09-10 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2023-09-17 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2023-09-24 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2023-10-02 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2023-10-08 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2023-10-15 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2023-10-22 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: CRASH_HIGHVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2023-10-29 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2023-11-05 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2023-11-12 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2023-11-19 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2023-11-27 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2023-12-03 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2023-12-10 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2023-12-17 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2023-12-25 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2023-12-31 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2024-01-07 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2024-01-14 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2024-01-22 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2024-01-28 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2024-02-04 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2024-02-11 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2024-02-18 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2024-02-25 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.35  QuietBrk=0.30  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2024-03-03 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2024-03-10 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2024-03-17 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2024-03-25 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2024-03-31 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2024-04-07 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2024-04-14 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2024-04-21 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2024-04-28 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2024-05-05 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2024-05-12 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2024-05-20 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2024-05-26 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  Adaptive  (5-strat)      1.47    39.23%   10.19%    1.45  44.9%     1536
                         (LLM calls: 126)

  --------------------------------------------------------------------  [Strategy PnL Attribution — Adaptive]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  Breakout         1024       +25900     41.9%        +25    77.4%
  QuietBrk          205        +5684     37.6%        +28    17.0%
  TrendPB           112        +1227     57.1%        +11     3.7%
  RSI-MR            170         +444     62.9%         +3     1.3%
  DualMA             25         +200     52.0%         +8     0.6%
  TOTAL            1536       +33454
  --------------------------------------------------------------------  [Adaptive — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  pass_thru%
  DualMA          12690    2574      10109          7       29       20.1%
  Breakout        16107   14227        309       1571     1093       81.5%
  QuietBrk         5173    1543       3537         93      279       24.4%
  TrendPB         12405     759       5907       5739      108        5.2%
  RSI-MR          10102    1005       5845       3252      584        4.2%

  --------------------------------------------------------------------  [Adaptive — union-filter overlap (per trading day)]
  Filter                              total   max/day   mean/day
  BreakoutUniverseFilter                  0         0       0.00
  ActivityTailFilter                      0         0       0.00
  PullbackUniverseFilter                734         8       1.24
  MeanReversionUniverseFilter          2457        19       4.14
  DualMAUniverseFilter                 1376        16       2.32
  --------------------------------------------------------------------  [Multi-strategy adaptive + RegimeContextAgent]
  [RCAQualityGate] 2022-01-18 → Breakout WR 35.0% < 40% over last 20 trades — CB relaxation disabled
  Adaptive+RCA (5-strat)   1.47    39.25%    9.91%    1.46  44.2%     1532
                         (LLM calls: 126)

  --------------------------------------------------------------------  [Strategy PnL Attribution — Adaptive+RCA]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  Breakout         1019       +25570     41.6%        +25    76.7%
  QuietBrk          207        +6133     35.7%        +30    18.4%
  TrendPB           109         +962     54.1%         +9     2.9%
  RSI-MR            165         +422     63.0%         +3     1.3%
  DualMA             32         +248     50.0%         +8     0.7%
  TOTAL            1532       +33335
  --------------------------------------------------------------------  [Adaptive+RCA — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  pass_thru%
  DualMA          13798    2874      10916          8       39       20.5%
  Breakout        16192   14289        309       1594     1096       81.5%
  QuietBrk         5146    1523       3525         98      272       24.3%
  TrendPB         12141     747       5952       5442      105        5.3%
  RSI-MR          10147     998       5869       3280      588        4.0%

  --------------------------------------------------------------------  [Adaptive+RCA — union-filter overlap (per trading day)]
  Filter                              total   max/day   mean/day
  BreakoutUniverseFilter                  0         0       0.00
  ActivityTailFilter                      0         0       0.00
  PullbackUniverseFilter                734         8       1.24
  MeanReversionUniverseFilter          2457        19       4.14
  DualMAUniverseFilter                 1376        16       2.32
  RCA delta              -0.00  +   0.02%

  ══════════════════════════════════════════════════════════════════
  OPPORTUNITY QUALITY SUMMARY  [Recent2022–2024]
  ══════════════════════════════════════════════════════════════════
  Trades analyzed  : 5001  (2246 winners / 2755 losers)
  ──────────────────────────────────────────────────────────────────
  Breakout quality:
    Follow-through rate  :   54.5%   (price continued post-exit)
    False breakout rate  :   31.8%   (MFE>2% but final return <0)
    Persistence half-life:    0.0 days (median survival above entry)
    Avg MFE efficiency   : -0.216      (1.00 = exit at peak)
  ──────────────────────────────────────────────────────────────────
  Continuation decay (post-exit drift):
                      1D        3D        5D
    Winners      -0.00%    +0.39%    +0.81%
    Losers       -0.04%    +0.06%    +0.22%
  ──────────────────────────────────────────────────────────────────
  Universe diagnostics (594 days):
    Avg stability score  : 0.320  (0=fully churning, 1=static)
    Avg daily turnover   : 54.4%
    Avg leader half-life : 2.0 days
    Stability vs PnL corr: -0.042  (>0 = stable universe → better trades)
    Turnover vs success  : -0.010  (<0 = higher churn → fewer successes)
  ──────────────────────────────────────────────────────────────────
  Per-regime breakdown (entry regime):
    Regime                           N  WinRate    AvgRet
    HIGH_VOL_SIDEWAYS              235    50.6%     0.35%
    HIGH_VOL_UPTREND              2119    44.8%     0.68%
    LOW_VOL_SIDEWAYS               339    48.1%     1.24%
    LOW_VOL_UPTREND               1019    43.1%     0.58%
    MID_VOL_SIDEWAYS               252    50.0%     0.26%
    MID_VOL_UPTREND               1037    43.4%     1.23%
  ──────────────────────────────────────────────────────────────────
  ══════════════════════════════════════════════════════════════════

======================================================================


```
