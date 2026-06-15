
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
  --------------------------------------------------------------------  [Multi-strategy adaptive — LLM weights]
  Adaptive  (5-strat)      1.21   116.18%   23.20%    1.45  43.9%     4005
                         (LLM calls: 337)

  --------------------------------------------------------------------  [Strategy PnL Attribution — Adaptive]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  Breakout         2794       +85070     41.6%        +30    79.3%
  QuietBrk          449       +15746     36.3%        +35    14.7%
  TrendPB           247        +2977     55.1%        +12     2.8%
  DualMA             76        +1872     43.4%        +25     1.7%
  RSI-MR            439        +1658     60.6%         +4     1.5%
  TOTAL            4005      +107323
  --------------------------------------------------------------------  [Adaptive — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  pass_thru%
  DualMA          42117   10192      31898         27       95       24.0%
  Breakout        41921   36291       1101       4529     2335       81.0%
  QuietBrk        11611    3357       7986        268      467       24.9%
  TrendPB         24537    1933      10505      12099      292        6.7%
  RSI-MR          22016    2239      12776       7001     1137        5.0%

  --------------------------------------------------------------------  [Adaptive — union-filter overlap (per trading day)]
  Filter                              total   max/day   mean/day
  BreakoutUniverseFilter                  0         0       0.00
  ActivityTailFilter                      0         0       0.00
  PullbackUniverseFilter               1814         9       1.15
  MeanReversionUniverseFilter          6747        20       4.27
  DualMAUniverseFilter                 3430        16       2.17
  --------------------------------------------------------------------  [Multi-strategy adaptive + RegimeContextAgent]
  [RCAQualityGate] 2018-01-16 → Breakout WR 30.0% < 40% over last 20 trades — CB relaxation disabled
  Adaptive+RCA (5-strat)   1.22   116.91%   23.76%    1.46  44.0%     4000
                         (LLM calls: 337)

  --------------------------------------------------------------------  [Strategy PnL Attribution — Adaptive+RCA]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  Breakout         2771       +82443     41.6%        +30    76.4%
  QuietBrk          469       +18203     36.5%        +39    16.9%
  TrendPB           241        +4386     56.4%        +18     4.1%
  RSI-MR            444        +1789     60.4%         +4     1.7%
  DualMA             75        +1158     44.0%        +15     1.1%
  TOTAL            4000      +107979
  --------------------------------------------------------------------  [Adaptive+RCA — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  pass_thru%
  DualMA          42122    9418      32673         31       96       22.1%
  Breakout        41957   37013        448       4496     2339       82.6%
  QuietBrk        11845    3468       8119        258      459       25.4%
  TrendPB         24531    1929      10495      12107      310        6.6%
  RSI-MR          23246    2336      13436       7474     1208        4.9%

  --------------------------------------------------------------------  [Adaptive+RCA — union-filter overlap (per trading day)]
  Filter                              total   max/day   mean/day
  BreakoutUniverseFilter                  0         0       0.00
  ActivityTailFilter                      0         0       0.00
  PullbackUniverseFilter               1814         9       1.15
  MeanReversionUniverseFilter          6747        20       4.27
  DualMAUniverseFilter                 3430        16       2.17
  RCA delta              + 0.01  +   0.73%

  ══════════════════════════════════════════════════════════════════
  OPPORTUNITY QUALITY SUMMARY  [Full  2018–2024]
  ══════════════════════════════════════════════════════════════════
  Trades analyzed  : 13649  (6136 winners / 7513 losers)
  ──────────────────────────────────────────────────────────────────
  Breakout quality:
    Follow-through rate  :   52.2%   (price continued post-exit)
    False breakout rate  :   34.6%   (MFE>2% but final return <0)
    Persistence half-life:    0.0 days (median survival above entry)
    Avg MFE efficiency   : -0.214      (1.00 = exit at peak)
  ──────────────────────────────────────────────────────────────────
  Continuation decay (post-exit drift):
                      1D        3D        5D
    Winners      -0.04%    +0.42%    +0.74%
    Losers       -0.10%    +0.07%    +0.21%
  ──────────────────────────────────────────────────────────────────
  Universe diagnostics (1581 days):
    Avg stability score  : 0.331  (0=fully churning, 1=static)
    Avg daily turnover   : 54.0%
    Avg leader half-life : 2.0 days
    Stability vs PnL corr: +0.000  (>0 = stable universe → better trades)
    Turnover vs success  : +0.005  (<0 = higher churn → fewer successes)
  ──────────────────────────────────────────────────────────────────
  Per-regime breakdown (entry regime):
    Regime                           N  WinRate    AvgRet
    HIGH_VOL_SIDEWAYS              764    49.9%     0.24%
    HIGH_VOL_UPTREND              5807    45.5%     1.07%
    LOW_VOL_SIDEWAYS               869    51.0%     1.82%
    LOW_VOL_UPTREND               2422    42.2%     0.63%
    MID_VOL_SIDEWAYS               771    50.2%     0.61%
    MID_VOL_UPTREND               3016    41.8%     0.97%
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
  --------------------------------------------------------------------  [Multi-strategy adaptive — LLM weights]
  Adaptive  (5-strat)     -0.57    -5.83%   11.34%    0.75  38.1%      609
                         (LLM calls: 58)

  --------------------------------------------------------------------  [Strategy PnL Attribution — Adaptive]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  RSI-MR             76         +146     55.3%         +2    -1.7%
  DualMA             17         -492     23.5%        -29     5.8%
  TrendPB            32         -775     40.6%        -24     9.2%
  QuietBrk           62        -2348     24.2%        -38    27.8%
  Breakout          422        -4978     37.4%        -12    58.9%
  TOTAL             609        -8446
  --------------------------------------------------------------------  [Adaptive — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  pass_thru%
  DualMA           6255    1912       4338          5       15       30.3%
  Breakout         6271    5107        253        911      247       77.5%
  QuietBrk         1413     443        940         30       34       28.9%
  TrendPB          2475     361       1056       1058       22       13.7%
  RSI-MR           1469     265        859        345       65       13.6%

  --------------------------------------------------------------------  [Adaptive — union-filter overlap (per trading day)]
  Filter                              total   max/day   mean/day
  BreakoutUniverseFilter                  0         0       0.00
  ActivityTailFilter                      0         0       0.00
  PullbackUniverseFilter                291         8       1.10
  MeanReversionUniverseFilter          1099        16       4.15
  DualMAUniverseFilter                  556        12       2.10
  --------------------------------------------------------------------  [Multi-strategy adaptive + RegimeContextAgent]
  [RCAQualityGate] 2019-01-21 → Breakout WR 20.0% < 40% over last 15 trades — CB relaxation disabled
  Adaptive+RCA (5-strat)  -0.60    -6.07%   11.41%    0.75  37.5%      605
                         (LLM calls: 58)

  --------------------------------------------------------------------  [Strategy PnL Attribution — Adaptive+RCA]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  RSI-MR             75         +121     52.0%         +2    -1.4%
  TrendPB            30         -184     43.3%         -6     2.2%
  DualMA             18         -509     27.8%        -28     6.0%
  QuietBrk           57        -2327     24.6%        -41    27.4%
  Breakout          425        -5592     36.7%        -13    65.9%
  TOTAL             605        -8492
  --------------------------------------------------------------------  [Adaptive+RCA — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  pass_thru%
  DualMA           6241    1919       4317          5       14       30.5%
  Breakout         6282    5111        265        906      248       77.4%
  QuietBrk         1374     431        906         37       34       28.9%
  TrendPB          2230     331        917        982       23       13.8%
  RSI-MR           1338     260        779        299       64       14.6%

  --------------------------------------------------------------------  [Adaptive+RCA — union-filter overlap (per trading day)]
  Filter                              total   max/day   mean/day
  BreakoutUniverseFilter                  0         0       0.00
  ActivityTailFilter                      0         0       0.00
  PullbackUniverseFilter                291         8       1.10
  MeanReversionUniverseFilter          1099        16       4.15
  DualMAUniverseFilter                  556        12       2.10
  RCA delta              -0.03    -0.24%

  ══════════════════════════════════════════════════════════════════
  OPPORTUNITY QUALITY SUMMARY  [Bull  2019–2020]
  ══════════════════════════════════════════════════════════════════
  Trades analyzed  : 2147  (848 winners / 1299 losers)
  ──────────────────────────────────────────────────────────────────
  Breakout quality:
    Follow-through rate  :   48.0%   (price continued post-exit)
    False breakout rate  :   38.1%   (MFE>2% but final return <0)
    Persistence half-life:    0.0 days (median survival above entry)
    Avg MFE efficiency   : -0.284      (1.00 = exit at peak)
  ──────────────────────────────────────────────────────────────────
  Continuation decay (post-exit drift):
                      1D        3D        5D
    Winners      -0.09%    +0.13%    +0.21%
    Losers       -0.08%    -0.18%    -0.11%
  ──────────────────────────────────────────────────────────────────
  Universe diagnostics (265 days):
    Avg stability score  : 0.331  (0=fully churning, 1=static)
    Avg daily turnover   : 54.3%
    Avg leader half-life : 1.9 days
    Stability vs PnL corr: +0.011  (>0 = stable universe → better trades)
    Turnover vs success  : +0.050  (<0 = higher churn → fewer successes)
  ──────────────────────────────────────────────────────────────────
  Per-regime breakdown (entry regime):
    Regime                           N  WinRate    AvgRet
    HIGH_VOL_SIDEWAYS               91    46.2%     1.00%
    HIGH_VOL_UPTREND               594    47.3%     0.61%
    LOW_VOL_SIDEWAYS               217    47.0%    -0.36%
    LOW_VOL_UPTREND                552    31.7%    -0.99%
    MID_VOL_SIDEWAYS               127    48.0%    -0.95%
    MID_VOL_UPTREND                566    33.0%    -1.09%
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
  --------------------------------------------------------------------  [Multi-strategy adaptive — LLM weights]

  Adaptive  (5-strat)      2.21    31.78%    6.40%    1.82  46.3%      795
                         (LLM calls: 54)

  --------------------------------------------------------------------  [Strategy PnL Attribution — Adaptive]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  Breakout          509       +24983     42.2%        +49    85.1%
  QuietBrk           84        +3339     39.3%        +40    11.4%
  TrendPB            78        +1072     57.7%        +14     3.7%
  RSI-MR            114         +164     63.2%         +1     0.6%
  DualMA             10         -206     30.0%        -21    -0.7%
  TOTAL             795       +29352
  --------------------------------------------------------------------  [Adaptive — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  pass_thru%
  DualMA           7760    1609       6143          8       16       20.5%
  Breakout         7720    6745         73        902      350       82.8%
  QuietBrk         2300     600       1646         54       54       23.7%
  TrendPB          5652     423       1996       3233       88        5.9%
  RSI-MR           5573     477       3334       1762      177        5.4%

  --------------------------------------------------------------------  [Adaptive — union-filter overlap (per trading day)]
  Filter                              total   max/day   mean/day
  BreakoutUniverseFilter                  0         0       0.00
  ActivityTailFilter                      0         0       0.00
  PullbackUniverseFilter                305         8       1.22
  MeanReversionUniverseFilter          1171        19       4.68
  DualMAUniverseFilter                  604        13       2.42
  --------------------------------------------------------------------  [Multi-strategy adaptive + RegimeContextAgent]
  [RCAQualityGate] 2020-01-13 → Breakout WR 10.0% < 40% over last 10 trades — CB relaxation disabled
  Adaptive+RCA (5-strat)   2.26    32.41%    6.37%    1.85  45.5%      765
                         (LLM calls: 54)

  --------------------------------------------------------------------  [Strategy PnL Attribution — Adaptive+RCA]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  Breakout          502       +23652     41.4%        +47    78.7%
  QuietBrk           82        +5197     40.2%        +63    17.3%
  TrendPB            66         +820     59.1%        +12     2.7%
  RSI-MR            105         +472     61.9%         +4     1.6%
  DualMA             10          -89     30.0%         -9    -0.3%
  TOTAL             765       +30051
  --------------------------------------------------------------------  [Adaptive+RCA — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  pass_thru%
  DualMA           7622    1600       6013          9       15       20.8%
  Breakout         7472    6592         62        818      360       83.4%
  QuietBrk         2251     579       1616         56       64       22.9%
  TrendPB          5065     412       1681       2972      102        6.1%
  RSI-MR           5095     445       3042       1608      176        5.3%

  --------------------------------------------------------------------  [Adaptive+RCA — union-filter overlap (per trading day)]
  Filter                              total   max/day   mean/day
  BreakoutUniverseFilter                  0         0       0.00
  ActivityTailFilter                      0         0       0.00
  PullbackUniverseFilter                305         8       1.22
  MeanReversionUniverseFilter          1171        19       4.68
  DualMAUniverseFilter                  604        13       2.42
  RCA delta              + 0.05  +   0.64%

  ══════════════════════════════════════════════════════════════════
  OPPORTUNITY QUALITY SUMMARY  [Crash 2020]
  ══════════════════════════════════════════════════════════════════
  Trades analyzed  : 2551  (1212 winners / 1339 losers)
  ──────────────────────────────────────────────────────────────────
  Breakout quality:
    Follow-through rate  :   56.7%   (price continued post-exit)
    False breakout rate  :   37.8%   (MFE>2% but final return <0)
    Persistence half-life:    0.0 days (median survival above entry)
    Avg MFE efficiency   : -0.153      (1.00 = exit at peak)
  ──────────────────────────────────────────────────────────────────
  Continuation decay (post-exit drift):
                      1D        3D        5D
    Winners      +0.05%    +0.94%    +1.29%
    Losers       -0.10%    +0.51%    +0.83%
  ──────────────────────────────────────────────────────────────────
  Universe diagnostics (250 days):
    Avg stability score  : 0.356  (0=fully churning, 1=static)
    Avg daily turnover   : 52.1%
    Avg leader half-life : 2.1 days
    Stability vs PnL corr: +0.047  (>0 = stable universe → better trades)
    Turnover vs success  : +0.058  (<0 = higher churn → fewer successes)
  ──────────────────────────────────────────────────────────────────
  Per-regime breakdown (entry regime):
    Regime                           N  WinRate    AvgRet
    HIGH_VOL_SIDEWAYS               72    55.6%    -0.05%
    HIGH_VOL_UPTREND               875    43.1%     1.39%
    LOW_VOL_SIDEWAYS               234    64.5%     4.91%
    LOW_VOL_UPTREND                629    47.5%     1.53%
    MID_VOL_SIDEWAYS               108    69.4%     2.99%
    MID_VOL_UPTREND                633    42.7%     1.54%
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
  --------------------------------------------------------------------  [Multi-strategy adaptive — LLM weights]
  Adaptive  (5-strat)      2.72    81.99%    8.95%    1.99  48.9%     1661
                         (LLM calls: 93)

  --------------------------------------------------------------------  [Strategy PnL Attribution — Adaptive]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  Breakout         1035       +65228     45.6%        +63    80.2%
  QuietBrk          171       +12080     41.5%        +71    14.9%
  DualMA             20        +1801     50.0%        +90     2.2%
  TrendPB           179        +1227     59.2%         +7     1.5%
  RSI-MR            256         +962     59.8%         +4     1.2%
  TOTAL            1661       +81296
  --------------------------------------------------------------------  [Adaptive — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  pass_thru%
  DualMA          15342    3434      11892         16       20       22.3%
  Breakout        15531   13053        534       1944      564       80.4%
  QuietBrk         4709    1239       3334        136      140       23.3%
  TrendPB         12588     934       4902       6752      152        6.2%
  RSI-MR          12493    1126       7487       3880      484        5.1%

  --------------------------------------------------------------------  [Adaptive — union-filter overlap (per trading day)]
  Filter                              total   max/day   mean/day
  BreakoutUniverseFilter                  0         0       0.00
  ActivityTailFilter                      0         0       0.00
  PullbackUniverseFilter                583         9       1.34
  MeanReversionUniverseFilter          2194        20       5.04
  DualMAUniverseFilter                  983        13       2.26
  --------------------------------------------------------------------  [Multi-strategy adaptive + RegimeContextAgent]
  [RCAQualityGate] 2020-06-10 → Breakout WR 9.1% < 40% over last 11 trades — CB relaxation disabled
  Adaptive+RCA (5-strat)   2.69    81.02%    9.14%    1.97  48.7%     1630
                         (LLM calls: 93)

  --------------------------------------------------------------------  [Strategy PnL Attribution — Adaptive+RCA]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  Breakout         1034       +65474     45.8%        +63    81.6%
  QuietBrk          174       +11870     41.4%        +68    14.8%
  DualMA             20        +1280     45.0%        +64     1.6%
  TrendPB           146         +849     58.9%         +6     1.1%
  RSI-MR            256         +776     59.8%         +3     1.0%
  TOTAL            1630       +80249
  --------------------------------------------------------------------  [Adaptive+RCA — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  pass_thru%
  DualMA          15139    2920      12204         15       20       19.2%
  Breakout        15268   13359        136       1773      577       83.7%
  QuietBrk         4685    1232       3329        124      143       23.2%
  TrendPB         12269     882       4609       6778      195        5.6%
  RSI-MR          12792    1163       7616       4013      508        5.1%

  --------------------------------------------------------------------  [Adaptive+RCA — union-filter overlap (per trading day)]
  Filter                              total   max/day   mean/day
  BreakoutUniverseFilter                  0         0       0.00
  ActivityTailFilter                      0         0       0.00
  PullbackUniverseFilter                583         9       1.34
  MeanReversionUniverseFilter          2194        20       5.04
  DualMAUniverseFilter                  983        13       2.26
  RCA delta              -0.03    -0.97%

  ══════════════════════════════════════════════════════════════════
  OPPORTUNITY QUALITY SUMMARY  [Recov 2020–2021]
  ══════════════════════════════════════════════════════════════════
  Trades analyzed  : 5276  (2625 winners / 2651 losers)
  ──────────────────────────────────────────────────────────────────
  Breakout quality:
    Follow-through rate  :   54.5%   (price continued post-exit)
    False breakout rate  :   35.1%   (MFE>2% but final return <0)
    Persistence half-life:    0.0 days (median survival above entry)
    Avg MFE efficiency   : -0.128      (1.00 = exit at peak)
  ──────────────────────────────────────────────────────────────────
  Continuation decay (post-exit drift):
                      1D        3D        5D
    Winners      -0.05%    +0.77%    +1.18%
    Losers       -0.10%    +0.38%    +0.77%
  ──────────────────────────────────────────────────────────────────
  Universe diagnostics (435 days):
    Avg stability score  : 0.346  (0=fully churning, 1=static)
    Avg daily turnover   : 53.3%
    Avg leader half-life : 2.0 days
    Stability vs PnL corr: +0.013  (>0 = stable universe → better trades)
    Turnover vs success  : -0.017  (<0 = higher churn → fewer successes)
  ──────────────────────────────────────────────────────────────────
  Per-regime breakdown (entry regime):
    Regime                           N  WinRate    AvgRet
    HIGH_VOL_SIDEWAYS              289    53.3%     0.69%
    HIGH_VOL_UPTREND              2434    48.4%     1.96%
    LOW_VOL_SIDEWAYS               256    65.2%     5.50%
    LOW_VOL_UPTREND                784    49.9%     1.73%
    MID_VOL_SIDEWAYS               294    58.8%     2.65%
    MID_VOL_UPTREND               1219    46.1%     1.87%
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
  --------------------------------------------------------------------  [Multi-strategy adaptive — LLM weights]
  Adaptive  (5-strat)      0.35     2.81%    9.65%    1.10  37.4%      519
                         (LLM calls: 52)

  --------------------------------------------------------------------  [Strategy PnL Attribution — Adaptive]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  Breakout          383        +4455     36.8%        +12   156.9%
  TrendPB            34         +223     41.2%         +7     7.8%
  RSI-MR             40          +63     42.5%         +2     2.2%
  DualMA             12         -143     50.0%        -12    -5.0%
  QuietBrk           50        -1757     32.0%        -35   -61.9%
  TOTAL             519        +2840
  --------------------------------------------------------------------  [Adaptive — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  pass_thru%
  DualMA           5311    1512       3797          2       21       28.1%
  Breakout         5360    4657        211        492      431       78.8%
  QuietBrk         1075     336        704         35       42       27.3%
  TrendPB          3425     305       1479       1641       64        7.0%
  RSI-MR           2006     259       1201        546      155        5.2%

  --------------------------------------------------------------------  [Adaptive — union-filter overlap (per trading day)]
  Filter                              total   max/day   mean/day
  BreakoutUniverseFilter                  0         0       0.00
  ActivityTailFilter                      0         0       0.00
  PullbackUniverseFilter                306         7       1.23
  MeanReversionUniverseFilter          1030        17       4.15
  DualMAUniverseFilter                  668        16       2.69
  --------------------------------------------------------------------  [Multi-strategy adaptive + RegimeContextAgent]
  [RCAQualityGate] 2022-01-18 → Breakout WR 35.0% < 40% over last 20 trades — CB relaxation disabled
  Adaptive+RCA (5-strat)   0.62     5.44%    9.65%    1.20  39.8%      525
                         (LLM calls: 52)

  --------------------------------------------------------------------  [Strategy PnL Attribution — Adaptive+RCA]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  Breakout          378        +6200     38.1%        +16   113.3%
  TrendPB            35         +351     45.7%        +10     6.4%
  RSI-MR             54          +72     51.9%         +1     1.3%
  DualMA             12         -143     50.0%        -12    -2.6%
  QuietBrk           46        -1007     32.6%        -22   -18.4%
  TOTAL             525        +5472
  --------------------------------------------------------------------  [Adaptive+RCA — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  pass_thru%
  DualMA           5248    1491       3756          1       21       28.0%
  Breakout         5274    4584        213        477      438       78.6%
  QuietBrk         1049     319        696         34       51       25.5%
  TrendPB          3412     329       1456       1627       66        7.7%
  RSI-MR           2315     338       1342        635      192        6.3%

  --------------------------------------------------------------------  [Adaptive+RCA — union-filter overlap (per trading day)]
  Filter                              total   max/day   mean/day
  BreakoutUniverseFilter                  0         0       0.00
  ActivityTailFilter                      0         0       0.00
  PullbackUniverseFilter                306         7       1.23
  MeanReversionUniverseFilter          1030        17       4.15
  DualMAUniverseFilter                  668        16       2.69
  RCA delta              + 0.27  +   2.63%

  ══════════════════════════════════════════════════════════════════
  OPPORTUNITY QUALITY SUMMARY  [Bear  2022]
  ══════════════════════════════════════════════════════════════════
  Trades analyzed  : 1747  (689 winners / 1058 losers)
  ──────────────────────────────────────────────────────────────────
  Breakout quality:
    Follow-through rate  :   47.3%   (price continued post-exit)
    False breakout rate  :   37.1%   (MFE>2% but final return <0)
    Persistence half-life:    0.0 days (median survival above entry)
    Avg MFE efficiency   : -0.297      (1.00 = exit at peak)
  ──────────────────────────────────────────────────────────────────
  Continuation decay (post-exit drift):
                      1D        3D        5D
    Winners      +0.08%    +0.23%    +0.25%
    Losers       -0.17%    -0.21%    -0.43%
  ──────────────────────────────────────────────────────────────────
  Universe diagnostics (248 days):
    Avg stability score  : 0.327  (0=fully churning, 1=static)
    Avg daily turnover   : 53.7%
    Avg leader half-life : 2.0 days
    Stability vs PnL corr: -0.094  (>0 = stable universe → better trades)
    Turnover vs success  : +0.011  (<0 = higher churn → fewer successes)
  ──────────────────────────────────────────────────────────────────
  Per-regime breakdown (entry regime):
    Regime                           N  WinRate    AvgRet
    HIGH_VOL_SIDEWAYS               53    35.8%    -1.33%
    HIGH_VOL_UPTREND               386    37.0%     0.23%
    LOW_VOL_SIDEWAYS               212    50.5%     1.52%
    LOW_VOL_UPTREND                515    37.5%    -0.38%
    MID_VOL_SIDEWAYS               139    38.1%    -0.52%
    MID_VOL_UPTREND                442    39.4%     0.20%
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
  --------------------------------------------------------------------  [Multi-strategy adaptive — LLM weights]

  Adaptive  (5-strat)      1.40    37.30%    9.65%    1.43  44.1%     1520
                         (LLM calls: 126)

  --------------------------------------------------------------------  [Strategy PnL Attribution — Adaptive]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  Breakout         1041       +23282     40.9%        +22    72.1%
  QuietBrk          191        +7593     39.8%        +40    23.5%
  TrendPB            79         +839     54.4%        +11     2.6%
  RSI-MR            177         +403     62.1%         +2     1.2%
  DualMA             32         +168     46.9%         +5     0.5%
  TOTAL            1520       +32285
  --------------------------------------------------------------------  [Adaptive — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  pass_thru%
  DualMA          16090    3480      12603          7       49       21.3%
  Breakout        15973   14164        350       1459     1082       81.9%
  QuietBrk         4639    1343       3222         74      215       24.3%
  TrendPB         11690     646       5666       5378      131        4.4%
  RSI-MR          10696    1102       6165       3429      668        4.1%

  --------------------------------------------------------------------  [Adaptive — union-filter overlap (per trading day)]
  Filter                              total   max/day   mean/day
  BreakoutUniverseFilter                  0         0       0.00
  ActivityTailFilter                      0         0       0.00
  PullbackUniverseFilter                734         8       1.24
  MeanReversionUniverseFilter          2457        19       4.14
  DualMAUniverseFilter                 1376        16       2.32
  --------------------------------------------------------------------  [Multi-strategy adaptive + RegimeContextAgent]
  [RCAQualityGate] 2022-01-18 → Breakout WR 35.0% < 40% over last 20 trades — CB relaxation disabled
  Adaptive+RCA (5-strat)   1.50    41.54%    9.65%    1.49  45.1%     1515
                         (LLM calls: 126)

  --------------------------------------------------------------------  [Strategy PnL Attribution — Adaptive+RCA]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  Breakout         1028       +27346     41.3%        +27    75.1%
  QuietBrk          182        +7475     39.6%        +41    20.5%
  RSI-MR            201         +665     65.2%         +3     1.8%
  TrendPB            72         +472     55.6%         +7     1.3%
  DualMA             32         +463     50.0%        +14     1.3%
  TOTAL            1515       +36421
  --------------------------------------------------------------------  [Adaptive+RCA — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  pass_thru%
  DualMA          16017    3492      12519          6       48       21.5%
  Breakout        15854   14052        355       1447     1108       81.6%
  QuietBrk         4622    1317       3233         72      229       23.5%
  TrendPB         11630     633       5630       5367      135        4.3%
  RSI-MR          11079    1192       6295       3592      685        4.6%

  --------------------------------------------------------------------  [Adaptive+RCA — union-filter overlap (per trading day)]
  Filter                              total   max/day   mean/day
  BreakoutUniverseFilter                  0         0       0.00
  ActivityTailFilter                      0         0       0.00
  PullbackUniverseFilter                734         8       1.24
  MeanReversionUniverseFilter          2457        19       4.14
  DualMAUniverseFilter                 1376        16       2.32
  RCA delta              + 0.10  +   4.24%

  ══════════════════════════════════════════════════════════════════
  OPPORTUNITY QUALITY SUMMARY  [Recent2022–2024]
  ══════════════════════════════════════════════════════════════════
  Trades analyzed  : 4968  (2233 winners / 2735 losers)
  ──────────────────────────────────────────────────────────────────
  Breakout quality:
    Follow-through rate  :   54.9%   (price continued post-exit)
    False breakout rate  :   31.9%   (MFE>2% but final return <0)
    Persistence half-life:    0.0 days (median survival above entry)
    Avg MFE efficiency   : -0.217      (1.00 = exit at peak)
  ──────────────────────────────────────────────────────────────────
  Continuation decay (post-exit drift):
                      1D        3D        5D
    Winners      +0.02%    +0.42%    +0.81%
    Losers       -0.04%    +0.12%    +0.26%
  ──────────────────────────────────────────────────────────────────
  Universe diagnostics (594 days):
    Avg stability score  : 0.320  (0=fully churning, 1=static)
    Avg daily turnover   : 54.4%
    Avg leader half-life : 2.0 days
    Stability vs PnL corr: -0.043  (>0 = stable universe → better trades)
    Turnover vs success  : -0.003  (<0 = higher churn → fewer successes)
  ──────────────────────────────────────────────────────────────────
  Per-regime breakdown (entry regime):
    Regime                           N  WinRate    AvgRet
    HIGH_VOL_SIDEWAYS              236    50.8%     0.42%
    HIGH_VOL_UPTREND              2062    45.0%     0.74%
    LOW_VOL_SIDEWAYS               340    48.8%     1.26%
    LOW_VOL_UPTREND               1023    41.4%     0.37%
    MID_VOL_SIDEWAYS               263    47.5%     0.20%
    MID_VOL_UPTREND               1044    45.1%     1.33%
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
  --------------------------------------------------------------------  [Multi-strategy adaptive — LLM weights]

  Adaptive  (5-strat)     -0.22    -2.06%    5.93%    0.92  35.5%      541
                         (LLM calls: 66)

  --------------------------------------------------------------------  [Strategy PnL Attribution — Adaptive]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  QuietBrk           81        +1211     34.6%        +15   -59.8%
  RSI-MR             55          +21     49.1%         +0    -1.0%
  TrendPB             7           +2     28.6%         +0    -0.1%
  DualMA             12         -594     16.7%        -49    29.3%
  Breakout          386        -2665     34.5%         -7   131.6%
  TOTAL             541        -2024
  --------------------------------------------------------------------  [Adaptive — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  pass_thru%
  DualMA           5839    1532       4307          0       25       25.8%
  Breakout         5575    4847        225        503      468       78.5%
  QuietBrk         1943     616       1300         27      126       25.2%
  TrendPB          3444     135       2026       1283       35        2.9%
  RSI-MR           3199     426       1840        933      280        4.6%

  --------------------------------------------------------------------  [Adaptive — union-filter overlap (per trading day)]
  Filter                              total   max/day   mean/day
  BreakoutUniverseFilter                  0         0       0.00
  ActivityTailFilter                      0         0       0.00
  PullbackUniverseFilter                249         8       0.82
  MeanReversionUniverseFilter           993        18       3.26
  DualMAUniverseFilter                  565        11       1.85
  --------------------------------------------------------------------  [Multi-strategy adaptive + RegimeContextAgent]
  [RCAQualityGate] 2025-04-01 → Breakout WR 10.0% < 40% over last 10 trades — CB relaxation disabled
  Adaptive+RCA (5-strat)  -0.41    -3.51%    6.27%    0.87  35.3%      541
                         (LLM calls: 66)

  --------------------------------------------------------------------  [Strategy PnL Attribution — Adaptive+RCA]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  QuietBrk           77        +1384     37.7%        +18   -40.7%
  RSI-MR             48           +5     47.9%         +0    -0.2%
  TrendPB            10          -24     40.0%         -2     0.7%
  DualMA             10         -446     20.0%        -45    13.1%
  Breakout          396        -4317     33.6%        -11   127.1%
  TOTAL             541        -3398
  --------------------------------------------------------------------  [Adaptive+RCA — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  pass_thru%
  DualMA           5869    1328       4541          0       25       22.2%
  Breakout         5645    5085         54        506      459       81.9%
  QuietBrk         1776     538       1208         30       91       25.2%
  TrendPB          3445     202       1941       1302       30        5.0%
  RSI-MR           2778     361       1591        826      238        4.4%

  --------------------------------------------------------------------  [Adaptive+RCA — union-filter overlap (per trading day)]
  Filter                              total   max/day   mean/day
  BreakoutUniverseFilter                  0         0       0.00
  ActivityTailFilter                      0         0       0.00
  PullbackUniverseFilter                249         8       0.82
  MeanReversionUniverseFilter           993        18       3.26
  DualMAUniverseFilter                  565        11       1.85
  RCA delta              -0.19    -1.45%

  ══════════════════════════════════════════════════════════════════
  OPPORTUNITY QUALITY SUMMARY  [Live  2025–2026]
  ══════════════════════════════════════════════════════════════════
  Trades analyzed  : 1729  (623 winners / 1106 losers)
  ──────────────────────────────────────────────────────────────────
  Breakout quality:
    Follow-through rate  :   52.5%   (price continued post-exit)
    False breakout rate  :   27.3%   (MFE>2% but final return <0)
    Persistence half-life:    0.0 days (median survival above entry)
    Avg MFE efficiency   : -0.344      (1.00 = exit at peak)
  ──────────────────────────────────────────────────────────────────
  Continuation decay (post-exit drift):
                      1D        3D        5D
    Winners      +0.07%    +0.05%    +0.28%
    Losers       +0.31%    +0.29%    +0.77%
  ──────────────────────────────────────────────────────────────────
  Universe diagnostics (305 days):
    Avg stability score  : 0.299  (0=fully churning, 1=static)
    Avg daily turnover   : 57.9%
    Avg leader half-life : 1.8 days
    Stability vs PnL corr: +0.093  (>0 = stable universe → better trades)
    Turnover vs success  : -0.012  (<0 = higher churn → fewer successes)
  ──────────────────────────────────────────────────────────────────
  Per-regime breakdown (entry regime):
    Regime                           N  WinRate    AvgRet
    HIGH_VOL_SIDEWAYS               43    41.9%    -0.09%
    HIGH_VOL_UPTREND               371    39.6%    -0.23%
    LOW_VOL_SIDEWAYS               201    31.3%    -0.21%
    LOW_VOL_UPTREND                572    33.9%    -0.51%
    MID_VOL_SIDEWAYS                91    31.9%    -1.66%
    MID_VOL_UPTREND                451    38.1%    -0.02%
  ──────────────────────────────────────────────────────────────────
  ══════════════════════════════════════════════════════════════════

======================================================================

  [LLMCache] hits=392 misses=1180 (25% hit rate, 9932 cached entries, file=runs/llm_cache.json)
