
  [Cache] Loading 150 symbols from LOCAL SQLite (2014-01-01 → 2026-12-31)...
  [Cache] Local hit: 400,968 records for 150 symbols (no Supabase calls).

[DynamicUniverseAgent] Bulk fetching 150 symbols from 2017-06-15 to 2024-06-01 ...
[DynamicUniverseAgent] Loaded 149 symbols. Skipped 1: TMCV(no data)

======================================================================
  Period: Full  2018–2024   (2018-01-01 → 2024-06-01)
  Universe: 150 symbols → DynamicUniverse top 80 → UniverseSelection top 20
  Costs: 0.10% commission + 0.05% slippage per side (all returns net of costs)
======================================================================
  Strategy               Sharpe    Return    MaxDD      PF     WR  #Trades
  --------------------------------------------------------------------  [Medium-term]
  DualMA SMA20/50          0.79    61.81%   13.53%    1.43  42.8%      537
  --------------------------------------------------------------------  [Short-term]
  Breakout 10d             0.92   110.54%   28.60%    1.26  40.4%     2503
  QuietBrk 20d             0.97   120.64%   25.73%    1.35  39.9%     1614
  TrendPB v2 pct=3%        0.60    40.19%   20.41%    1.18  57.9%     1823
  TrendPB v2 pct=5%        0.80    39.15%   10.73%    1.34  58.7%      958
  --------------------------------------------------------------------  [Mean-reversion]
  RSI-MR  os=5  ob=80      0.16     8.01%   20.56%    1.03  54.8%     2553
  --------------------------------------------------------------------  [Multi-strategy baseline — equal weight]
  EqualWeight (5-strat)    1.25    85.36%   12.11%    1.42  46.3%     5644

  --------------------------------------------------------------------  [Strategy PnL Attribution — EqualWeight]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  Breakout         2960       +53107     41.6%        +18    66.0%
  QuietBrk          596       +13464     36.9%        +23    16.7%
  RSI-MR           1512        +5585     56.3%         +4     6.9%
  TrendPB           430        +5139     56.7%        +12     6.4%
  DualMA            146        +3154     45.2%        +22     3.9%
  TOTAL            5644       +80448
  --------------------------------------------------------------------  [EqualWeight — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  pass_thru%
  DualMA          46168   36913       9217         38      126       79.7%
  Breakout        48132   13999      26229       7904     1762       25.4%
  QuietBrk        14815    2886      11474        455      410       16.7%
  TrendPB         39318    2943      19230      17145      275        6.8%
  RSI-MR          42547    4981      25307      12259     1042        9.3%

  --------------------------------------------------------------------  [EqualWeight — union-filter overlap (per trading day)]
  Filter                              total   max/day   mean/day
  BreakoutUniverseFilter                  0         0       0.00
  ActivityTailFilter                      0         0       0.00
  PullbackUniverseFilter               1814         9       1.15
  MeanReversionUniverseFilter          6747        20       4.27
  DualMAUniverseFilter                 3430        16       2.17

  --------------------------------------------------------------------  [Exit Attribution — EqualWeight]
  Reason           Trades     %   WinRate    Avg PnL    Total PnL
  atr_stop            503   8.9%    64.4%     +127.5      +64136
  strategy           5141  91.1%    44.5%       +3.2      +16313

  Strategy       ATR%  Strat%   ATR WR   Strat WR   ATR Avg   Strat Avg
  Breakout       7.1%   92.9%    76.2%      39.0%   +191.1       +4.7
  DualMA        91.1%    8.9%    46.6%      30.8%    +26.4      -27.4
  QuietBrk      26.8%   73.2%    63.7%      27.1%   +128.1      -16.1
  RSI-MR         0.0%  100.0%     0.0%      56.3%     +0.0       +3.7
  TrendPB        0.0%  100.0%     0.0%      56.7%     +0.0      +12.0

  ══════════════════════════════════════════════════════════════════
  OPPORTUNITY QUALITY SUMMARY  [Full  2018–2024]
  ══════════════════════════════════════════════════════════════════
  Trades analyzed  : 5644  (2614 winners / 3030 losers)
  ──────────────────────────────────────────────────────────────────
  Breakout quality:
    Follow-through rate  :   52.1%   (price continued post-exit)
    False breakout rate  :   34.4%   (MFE>2% but final return <0)
    Persistence half-life:    0.0 days (median survival above entry)
    Avg MFE efficiency   : -0.183      (1.00 = exit at peak)
  ──────────────────────────────────────────────────────────────────
  Continuation decay (post-exit drift):
                      1D        3D        5D
    Winners      -0.03%    +0.40%    +0.69%
    Losers       -0.10%    +0.08%    +0.24%
  ──────────────────────────────────────────────────────────────────
  Universe diagnostics (1581 days):
    Avg stability score  : 0.331  (0=fully churning, 1=static)
    Avg daily turnover   : 54.0%
    Avg leader half-life : 2.0 days
    Stability vs PnL corr: -0.002  (>0 = stable universe → better trades)
    Turnover vs success  : +0.012  (<0 = higher churn → fewer successes)
  ──────────────────────────────────────────────────────────────────
  Per-regime breakdown (entry regime):
    Regime                           N  WinRate    AvgRet
    HIGH_VOL_SIDEWAYS              384    50.5%     0.07%
    HIGH_VOL_UPTREND              2256    47.2%     0.94%
    LOW_VOL_SIDEWAYS               415    50.4%     1.44%
    LOW_VOL_UPTREND               1023    43.5%     0.55%
    MID_VOL_SIDEWAYS               354    52.5%     0.66%
    MID_VOL_UPTREND               1212    42.5%     0.88%
  ──────────────────────────────────────────────────────────────────
  ══════════════════════════════════════════════════════════════════
[DynamicUniverseAgent] Bulk fetching 150 symbols from 2018-06-15 to 2020-02-01 ...
[DynamicUniverseAgent] Loaded 146 symbols. Skipped 4: TMCV(no data), ETERNAL(no data), SBICARD(no data), MAXHEALTH(no data)

======================================================================
  Period: Bull  2019–2020   (2019-01-01 → 2020-02-01)
  Universe: 150 symbols → DynamicUniverse top 80 → UniverseSelection top 20
  Costs: 0.10% commission + 0.05% slippage per side (all returns net of costs)
======================================================================
  Strategy               Sharpe    Return    MaxDD      PF     WR  #Trades
  --------------------------------------------------------------------  [Medium-term]
  DualMA SMA20/50         -0.10    -1.46%    8.43%    0.62  27.4%       84
  --------------------------------------------------------------------  [Short-term]
  Breakout 10d             0.27     2.77%   11.03%    1.03  39.8%      387
  QuietBrk 20d             0.47     5.34%   10.96%    0.95  35.8%      243
  TrendPB v2 pct=3%        0.39     2.79%    4.94%    1.14  54.5%      253
  TrendPB v2 pct=5%        0.90     4.51%    2.85%    1.43  57.3%      124
  --------------------------------------------------------------------  [Mean-reversion]
  RSI-MR  os=5  ob=80     -0.08    -1.18%   10.86%    0.98  54.8%      416
  --------------------------------------------------------------------  [Multi-strategy baseline — equal weight]
  EqualWeight (5-strat)   -0.56    -3.69%    7.85%    0.83  41.7%      933

  --------------------------------------------------------------------  [Strategy PnL Attribution — EqualWeight]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  RSI-MR            315         +308     52.4%         +1    -6.8%
  TrendPB            55          +17     43.6%         +0    -0.4%
  DualMA             25        -1262     20.0%        -50    27.7%
  QuietBrk           88        -1717     25.0%        -20    37.7%
  Breakout          450        -1904     38.4%         -4    41.8%
  TOTAL             933        -4558
  --------------------------------------------------------------------  [EqualWeight — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  pass_thru%
  DualMA           6765    5405       1356          4       18       79.6%
  Breakout         7118    2058       3645       1415      187       26.3%
  QuietBrk         2052     412       1570         70       51       17.6%
  TrendPB          5897     541       2996       2360       32        8.6%
  RSI-MR           6588    1002       3917       1669      149       12.9%

  --------------------------------------------------------------------  [EqualWeight — union-filter overlap (per trading day)]
  Filter                              total   max/day   mean/day
  BreakoutUniverseFilter                  0         0       0.00
  ActivityTailFilter                      0         0       0.00
  PullbackUniverseFilter                291         8       1.10
  MeanReversionUniverseFilter          1099        16       4.15
  DualMAUniverseFilter                  556        12       2.10

  --------------------------------------------------------------------  [Exit Attribution — EqualWeight]
  Reason           Trades     %   WinRate    Avg PnL    Total PnL
  atr_stop             62   6.6%    43.5%       -2.3        -141
  strategy            871  93.4%    41.6%       -5.1       -4417

  Strategy       ATR%  Strat%   ATR WR   Strat WR   ATR Avg   Strat Avg
  Breakout       4.7%   95.3%    71.4%      36.8%    +43.6       -6.6
  DualMA        92.0%    8.0%    21.7%       0.0%    -49.4      -63.1
  QuietBrk      20.5%   79.5%    38.9%      21.4%     +4.4      -25.7
  RSI-MR         0.0%  100.0%     0.0%      52.4%     +0.0       +1.0
  TrendPB        0.0%  100.0%     0.0%      43.6%     +0.0       +0.3

  ══════════════════════════════════════════════════════════════════
  OPPORTUNITY QUALITY SUMMARY  [Bull  2019–2020]
  ══════════════════════════════════════════════════════════════════
  Trades analyzed  : 933  (389 winners / 544 losers)
  ──────────────────────────────────────────────────────────────────
  Breakout quality:
    Follow-through rate  :   49.4%   (price continued post-exit)
    False breakout rate  :   37.2%   (MFE>2% but final return <0)
    Persistence half-life:    0.0 days (median survival above entry)
    Avg MFE efficiency   : -0.237      (1.00 = exit at peak)
  ──────────────────────────────────────────────────────────────────
  Continuation decay (post-exit drift):
                      1D        3D        5D
    Winners      +0.03%    +0.13%    +0.27%
    Losers       -0.11%    -0.06%    +0.07%
  ──────────────────────────────────────────────────────────────────
  Universe diagnostics (265 days):
    Avg stability score  : 0.331  (0=fully churning, 1=static)
    Avg daily turnover   : 54.3%
    Avg leader half-life : 1.9 days
    Stability vs PnL corr: +0.024  (>0 = stable universe → better trades)
    Turnover vs success  : +0.053  (<0 = higher churn → fewer successes)
  ──────────────────────────────────────────────────────────────────
  Per-regime breakdown (entry regime):
    Regime                           N  WinRate    AvgRet
    HIGH_VOL_SIDEWAYS               49    49.0%     1.03%
    HIGH_VOL_UPTREND               255    49.0%     0.64%
    LOW_VOL_SIDEWAYS               116    44.8%    -0.56%
    LOW_VOL_UPTREND                227    34.4%    -0.85%
    MID_VOL_SIDEWAYS                63    54.0%    -0.58%
    MID_VOL_UPTREND                223    34.1%    -0.74%
  ──────────────────────────────────────────────────────────────────
  ══════════════════════════════════════════════════════════════════
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
  EqualWeight (5-strat)    2.53    27.91%    5.21%    1.98  50.1%      991

  --------------------------------------------------------------------  [Strategy PnL Attribution — EqualWeight]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  Breakout          520       +17301     43.3%        +33    68.4%
  QuietBrk           99        +3216     40.4%        +32    12.7%
  RSI-MR            246        +2976     65.4%        +12    11.8%
  TrendPB           106        +1679     59.4%        +16     6.6%
  DualMA             20         +127     35.0%         +6     0.5%
  TOTAL             991       +25299
  --------------------------------------------------------------------  [EqualWeight — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  pass_thru%
  DualMA           8346    6692       1644         10       22       79.9%
  Breakout         8558    2359       4812       1387      261       24.5%
  QuietBrk         2698     501       2119         78       47       16.8%
  TrendPB          7116     579       2849       3688       72        7.1%
  RSI-MR           7514     728       4525       2261       98        8.4%

  --------------------------------------------------------------------  [EqualWeight — union-filter overlap (per trading day)]
  Filter                              total   max/day   mean/day
  BreakoutUniverseFilter                  0         0       0.00
  ActivityTailFilter                      0         0       0.00
  PullbackUniverseFilter                305         8       1.22
  MeanReversionUniverseFilter          1171        19       4.68
  DualMAUniverseFilter                  604        13       2.42

  --------------------------------------------------------------------  [Exit Attribution — EqualWeight]
  Reason           Trades     %   WinRate    Avg PnL    Total PnL
  atr_stop             97   9.8%    69.1%     +139.5      +13535
  strategy            894  90.2%    48.0%      +13.2      +11764

  Strategy       ATR%  Strat%   ATR WR   Strat WR   ATR Avg   Strat Avg
  Breakout       9.6%   90.4%    82.0%      39.1%   +181.8      +17.5
  DualMA        90.0%   10.0%    38.9%       0.0%    +18.4     -101.9
  QuietBrk      29.3%   70.7%    65.5%      30.0%   +141.9      -12.9
  RSI-MR         0.0%  100.0%     0.0%      65.4%     +0.0      +12.1
  TrendPB        0.0%  100.0%     0.0%      59.4%     +0.0      +15.8

  ══════════════════════════════════════════════════════════════════
  OPPORTUNITY QUALITY SUMMARY  [Crash 2020]
  ══════════════════════════════════════════════════════════════════
  Trades analyzed  : 991  (496 winners / 495 losers)
  ──────────────────────────────────────────────────────────────────
  Breakout quality:
    Follow-through rate  :   56.6%   (price continued post-exit)
    False breakout rate  :   36.5%   (MFE>2% but final return <0)
    Persistence half-life:    0.0 days (median survival above entry)
    Avg MFE efficiency   : -0.118      (1.00 = exit at peak)
  ──────────────────────────────────────────────────────────────────
  Continuation decay (post-exit drift):
                      1D        3D        5D
    Winners      +0.14%    +0.93%    +1.32%
    Losers       -0.02%    +0.59%    +0.92%
  ──────────────────────────────────────────────────────────────────
  Universe diagnostics (250 days):
    Avg stability score  : 0.356  (0=fully churning, 1=static)
    Avg daily turnover   : 52.1%
    Avg leader half-life : 2.1 days
    Stability vs PnL corr: +0.053  (>0 = stable universe → better trades)
    Turnover vs success  : +0.061  (<0 = higher churn → fewer successes)
  ──────────────────────────────────────────────────────────────────
  Per-regime breakdown (entry regime):
    Regime                           N  WinRate    AvgRet
    HIGH_VOL_SIDEWAYS               38    60.5%     0.50%
    HIGH_VOL_UPTREND               332    46.1%     1.45%
    LOW_VOL_SIDEWAYS                93    64.5%     4.57%
    LOW_VOL_UPTREND                242    47.9%     1.48%
    MID_VOL_SIDEWAYS                49    71.4%     2.75%
    MID_VOL_UPTREND                237    46.0%     1.68%
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
  EqualWeight (5-strat)    3.00    68.25%    6.28%    2.12  51.3%     1985

  --------------------------------------------------------------------  [Strategy PnL Attribution — EqualWeight]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  Breakout         1036       +44120     46.3%        +43    65.0%
  QuietBrk          192       +11193     44.8%        +58    16.5%
  RSI-MR            503        +6718     60.6%        +13     9.9%
  DualMA             41        +3873     53.7%        +94     5.7%
  TrendPB           213        +1966     59.2%         +9     2.9%
  TOTAL            1985       +67869
  --------------------------------------------------------------------  [EqualWeight — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  pass_thru%
  DualMA          16452   13264       3164         24       29       80.4%
  Breakout        17177    4707       9629       2841      439       24.8%
  QuietBrk         5273     945       4150        178       99       16.0%
  TrendPB         14309    1152       6003       7154      113        7.3%
  RSI-MR          15042    1436       9119       4487      176        8.4%

  --------------------------------------------------------------------  [EqualWeight — union-filter overlap (per trading day)]
  Filter                              total   max/day   mean/day
  BreakoutUniverseFilter                  0         0       0.00
  ActivityTailFilter                      0         0       0.00
  PullbackUniverseFilter                583         9       1.34
  MeanReversionUniverseFilter          2194        20       5.04
  DualMAUniverseFilter                  983        13       2.26

  --------------------------------------------------------------------  [Exit Attribution — EqualWeight]
  Reason           Trades     %   WinRate    Avg PnL    Total PnL
  atr_stop            186   9.4%    74.2%     +216.7      +40306
  strategy           1799  90.6%    49.0%      +15.3      +27564

  Strategy       ATR%  Strat%   ATR WR   Strat WR   ATR Avg   Strat Avg
  Breakout       8.9%   91.1%    81.5%      42.9%   +268.5      +20.6
  DualMA        90.2%    9.8%    56.8%      25.0%   +110.7      -56.1
  QuietBrk      29.7%   70.3%    73.7%      32.6%   +201.9       -2.3
  RSI-MR         0.0%  100.0%     0.0%      60.6%     +0.0      +13.4
  TrendPB        0.0%  100.0%     0.0%      59.2%     +0.0       +9.2

  ══════════════════════════════════════════════════════════════════
  OPPORTUNITY QUALITY SUMMARY  [Recov 2020–2021]
  ══════════════════════════════════════════════════════════════════
  Trades analyzed  : 1985  (1019 winners / 966 losers)
  ──────────────────────────────────────────────────────────────────
  Breakout quality:
    Follow-through rate  :   54.4%   (price continued post-exit)
    False breakout rate  :   34.1%   (MFE>2% but final return <0)
    Persistence half-life:    0.0 days (median survival above entry)
    Avg MFE efficiency   : -0.103      (1.00 = exit at peak)
  ──────────────────────────────────────────────────────────────────
  Continuation decay (post-exit drift):
                      1D        3D        5D
    Winners      -0.06%    +0.74%    +1.19%
    Losers       -0.11%    +0.34%    +0.76%
  ──────────────────────────────────────────────────────────────────
  Universe diagnostics (435 days):
    Avg stability score  : 0.346  (0=fully churning, 1=static)
    Avg daily turnover   : 53.3%
    Avg leader half-life : 2.0 days
    Stability vs PnL corr: +0.001  (>0 = stable universe → better trades)
    Turnover vs success  : -0.007  (<0 = higher churn → fewer successes)
  ──────────────────────────────────────────────────────────────────
  Per-regime breakdown (entry regime):
    Regime                           N  WinRate    AvgRet
    HIGH_VOL_SIDEWAYS              134    56.7%     0.72%
    HIGH_VOL_UPTREND               895    49.6%     1.94%
    LOW_VOL_SIDEWAYS               102    64.7%     5.19%
    LOW_VOL_UPTREND                292    50.0%     1.80%
    MID_VOL_SIDEWAYS               116    61.2%     2.85%
    MID_VOL_UPTREND                446    48.4%     2.05%
  ──────────────────────────────────────────────────────────────────
  ══════════════════════════════════════════════════════════════════
[DynamicUniverseAgent] Bulk fetching 150 symbols from 2021-06-15 to 2022-12-31 ...
[DynamicUniverseAgent] Loaded 149 symbols. Skipped 1: TMCV(no data)

======================================================================
  Period: Bear  2022        (2022-01-01 → 2022-12-31)
  Universe: 150 symbols → DynamicUniverse top 80 → UniverseSelection top 20
  Costs: 0.10% commission + 0.05% slippage per side (all returns net of costs)
======================================================================
  Strategy               Sharpe    Return    MaxDD      PF     WR  #Trades
  --------------------------------------------------------------------  [Medium-term]
  DualMA SMA20/50         -0.20    -2.29%   10.37%    0.88  38.3%       81
  --------------------------------------------------------------------  [Short-term]
  Breakout 10d             0.26     2.42%   11.98%    1.06  41.7%      343
  QuietBrk 20d            -0.22    -3.81%   16.98%    0.90  37.3%      220
  TrendPB v2 pct=3%       -1.09   -10.64%   12.14%    0.71  52.3%      241
  TrendPB v2 pct=5%       -0.40    -2.48%    5.86%    0.87  50.0%      116
  --------------------------------------------------------------------  [Mean-reversion]
  RSI-MR  os=5  ob=80     -0.97   -12.12%   15.78%    0.72  48.5%      344
  --------------------------------------------------------------------  [Multi-strategy baseline — equal weight]
  EqualWeight (5-strat)    0.05     0.07%    7.67%    1.00  40.7%      703

  --------------------------------------------------------------------  [Strategy PnL Attribution — EqualWeight]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  Breakout          376        +2360     38.8%         +6  4016.7%
  DualMA             28         +177     50.0%         +6   301.3%
  TrendPB            50          -89     46.0%         -2  -151.7%
  QuietBrk           72         -895     26.4%        -12 -1523.4%
  RSI-MR            177        -1494     47.5%         -8 -2543.0%
  TOTAL             703          +59
  --------------------------------------------------------------------  [EqualWeight — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  pass_thru%
  DualMA           5822    4523       1297          2       27       77.2%
  Breakout         6042    2093       2989        960      396       28.1%
  QuietBrk         1664     379       1214         71       79       18.0%
  TrendPB          4774     396       2371       2007       63        7.0%
  RSI-MR           5304     741       3075       1488      244        9.4%

  --------------------------------------------------------------------  [EqualWeight — union-filter overlap (per trading day)]
  Filter                              total   max/day   mean/day
  BreakoutUniverseFilter                  0         0       0.00
  ActivityTailFilter                      0         0       0.00
  PullbackUniverseFilter                306         7       1.23
  MeanReversionUniverseFilter          1030        17       4.15
  DualMAUniverseFilter                  668        16       2.69

  --------------------------------------------------------------------  [Exit Attribution — EqualWeight]
  Reason           Trades     %   WinRate    Avg PnL    Total PnL
  atr_stop             64   9.1%    56.2%      +59.4       +3804
  strategy            639  90.9%    39.1%       -5.9       -3745

  Strategy       ATR%  Strat%   ATR WR   Strat WR   ATR Avg   Strat Avg
  Breakout       4.3%   95.7%    81.2%      36.9%   +174.6       -1.2
  DualMA        96.4%    3.6%    48.1%     100.0%     +6.1      +13.1
  QuietBrk      29.2%   70.8%    47.6%      17.6%    +40.3      -34.1
  RSI-MR         0.0%  100.0%     0.0%      47.5%     +0.0       -8.4
  TrendPB        0.0%  100.0%     0.0%      46.0%     +0.0       -1.8

  ══════════════════════════════════════════════════════════════════
  OPPORTUNITY QUALITY SUMMARY  [Bear  2022]
  ══════════════════════════════════════════════════════════════════
  Trades analyzed  : 703  (286 winners / 417 losers)
  ──────────────────────────────────────────────────────────────────
  Breakout quality:
    Follow-through rate  :   46.9%   (price continued post-exit)
    False breakout rate  :   37.3%   (MFE>2% but final return <0)
    Persistence half-life:    0.0 days (median survival above entry)
    Avg MFE efficiency   : -0.276      (1.00 = exit at peak)
  ──────────────────────────────────────────────────────────────────
  Continuation decay (post-exit drift):
                      1D        3D        5D
    Winners      +0.02%    +0.10%    +0.13%
    Losers       -0.18%    -0.12%    -0.35%
  ──────────────────────────────────────────────────────────────────
  Universe diagnostics (248 days):
    Avg stability score  : 0.327  (0=fully churning, 1=static)
    Avg daily turnover   : 53.7%
    Avg leader half-life : 2.0 days
    Stability vs PnL corr: -0.093  (>0 = stable universe → better trades)
    Turnover vs success  : -0.007  (<0 = higher churn → fewer successes)
  ──────────────────────────────────────────────────────────────────
  Per-regime breakdown (entry regime):
    Regime                           N  WinRate    AvgRet
    HIGH_VOL_SIDEWAYS               24    37.5%    -2.32%
    HIGH_VOL_UPTREND               149    40.3%    -0.33%
    LOW_VOL_SIDEWAYS                96    52.1%     1.27%
    LOW_VOL_UPTREND                212    37.3%    -0.37%
    MID_VOL_SIDEWAYS                58    39.7%    -0.81%
    MID_VOL_UPTREND                164    39.6%     0.18%
  ──────────────────────────────────────────────────────────────────
  ══════════════════════════════════════════════════════════════════
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

  ══════════════════════════════════════════════════════════════════
  OPPORTUNITY QUALITY SUMMARY  [Recent2022–2024]
  ══════════════════════════════════════════════════════════════════
  Trades analyzed  : 1933  (879 winners / 1054 losers)
  ──────────────────────────────────────────────────────────────────
  Breakout quality:
    Follow-through rate  :   54.9%   (price continued post-exit)
    False breakout rate  :   32.7%   (MFE>2% but final return <0)
    Persistence half-life:    0.0 days (median survival above entry)
    Avg MFE efficiency   : -0.199      (1.00 = exit at peak)
  ──────────────────────────────────────────────────────────────────
  Continuation decay (post-exit drift):
                      1D        3D        5D
    Winners      -0.02%    +0.39%    +0.79%
    Losers       -0.06%    +0.14%    +0.36%
  ──────────────────────────────────────────────────────────────────
  Universe diagnostics (594 days):
    Avg stability score  : 0.320  (0=fully churning, 1=static)
    Avg daily turnover   : 54.4%
    Avg leader half-life : 2.0 days
    Stability vs PnL corr: -0.048  (>0 = stable universe → better trades)
    Turnover vs success  : -0.011  (<0 = higher churn → fewer successes)
  ──────────────────────────────────────────────────────────────────
  Per-regime breakdown (entry regime):
    Regime                           N  WinRate    AvgRet
    HIGH_VOL_SIDEWAYS              114    49.1%    -0.25%
    HIGH_VOL_UPTREND               766    47.3%     0.64%
    LOW_VOL_SIDEWAYS               144    50.0%     1.07%
    LOW_VOL_UPTREND                406    41.9%     0.41%
    MID_VOL_SIDEWAYS               110    48.2%    -0.15%
    MID_VOL_UPTREND                393    42.2%     0.96%
  ──────────────────────────────────────────────────────────────────
  ══════════════════════════════════════════════════════════════════
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
  EqualWeight (5-strat)   -0.62    -3.56%    4.31%    0.81  37.1%      647

  --------------------------------------------------------------------  [Strategy PnL Attribution — EqualWeight]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  QuietBrk           87         +365     31.0%         +4   -10.3%
  TrendPB            18          -37     50.0%         -2     1.0%
  RSI-MR            164         -329     50.6%         -2     9.2%
  DualMA             14         -751     14.3%        -54    21.1%
  Breakout          364        -2809     32.7%         -8    78.9%
  TOTAL             647        -3561
  --------------------------------------------------------------------  [EqualWeight — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  pass_thru%
  DualMA           5807    4437       1368          2       41       75.7%
  Breakout         5694    1949       2960        785      484       25.7%
  QuietBrk         1996     474       1473         49      134       17.0%
  TrendPB          4297     237       2582       1478       30        4.8%
  RSI-MR           4908     758       2820       1330      302        9.3%

  --------------------------------------------------------------------  [EqualWeight — union-filter overlap (per trading day)]
  Filter                              total   max/day   mean/day
  BreakoutUniverseFilter                  0         0       0.00
  ActivityTailFilter                      0         0       0.00
  PullbackUniverseFilter                249         8       0.82
  MeanReversionUniverseFilter           993        18       3.26
  DualMAUniverseFilter                  565        11       1.85

  --------------------------------------------------------------------  [Exit Attribution — EqualWeight]
  Reason           Trades     %   WinRate    Avg PnL    Total PnL
  atr_stop             39   6.0%    51.3%      +25.5        +995
  strategy            608  94.0%    36.2%       -7.5       -4556

  Strategy       ATR%  Strat%   ATR WR   Strat WR   ATR Avg   Strat Avg
  Breakout       3.3%   96.7%    58.3%      31.8%    +35.8       -9.2
  DualMA        85.7%   14.3%    16.7%       0.0%    -54.2      -50.2
  QuietBrk      17.2%   82.8%    73.3%      22.2%    +81.1      -11.8
  RSI-MR         0.0%  100.0%     0.0%      50.6%     +0.0       -2.0
  TrendPB        0.0%  100.0%     0.0%      50.0%     +0.0       -2.0

  ══════════════════════════════════════════════════════════════════
  OPPORTUNITY QUALITY SUMMARY  [Live  2025–2026]
  ══════════════════════════════════════════════════════════════════
  Trades analyzed  : 647  (240 winners / 407 losers)
  ──────────────────────────────────────────────────────────────────
  Breakout quality:
    Follow-through rate  :   51.9%   (price continued post-exit)
    False breakout rate  :   27.0%   (MFE>2% but final return <0)
    Persistence half-life:    0.0 days (median survival above entry)
    Avg MFE efficiency   : -0.322      (1.00 = exit at peak)
  ──────────────────────────────────────────────────────────────────
  Continuation decay (post-exit drift):
                      1D        3D        5D
    Winners      +0.02%    -0.02%    +0.19%
    Losers       +0.34%    +0.26%    +0.79%
  ──────────────────────────────────────────────────────────────────
  Universe diagnostics (305 days):
    Avg stability score  : 0.299  (0=fully churning, 1=static)
    Avg daily turnover   : 57.9%
    Avg leader half-life : 1.8 days
    Stability vs PnL corr: +0.109  (>0 = stable universe → better trades)
    Turnover vs success  : +0.019  (<0 = higher churn → fewer successes)
  ──────────────────────────────────────────────────────────────────
  Per-regime breakdown (entry regime):
    Regime                           N  WinRate    AvgRet
    HIGH_VOL_SIDEWAYS               27    51.9%     0.55%
    HIGH_VOL_UPTREND               131    38.9%    -0.43%
    LOW_VOL_SIDEWAYS                87    33.3%    -0.28%
    LOW_VOL_UPTREND                207    33.8%    -0.70%
    MID_VOL_SIDEWAYS                35    40.0%    -0.83%
    MID_VOL_UPTREND                160    38.8%    -0.03%
  ──────────────────────────────────────────────────────────────────
  ══════════════════════════════════════════════════════════════════

======================================================================

