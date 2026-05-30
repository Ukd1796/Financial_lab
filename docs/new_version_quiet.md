
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
  EqualWeight (5-strat)    1.23    82.35%   11.94%    1.40  46.4%     5662

  --------------------------------------------------------------------  [Strategy PnL Attribution — EqualWeight]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  Breakout         2969       +52531     41.6%        +18    67.8%
  QuietBrk          591       +12926     37.1%        +22    16.7%
  RSI-MR           1527        +4412     56.6%         +3     5.7%
  TrendPB           428        +4386     56.5%        +10     5.7%
  DualMA            147        +3282     44.9%        +22     4.2%
  TOTAL            5662       +77536
  --------------------------------------------------------------------  [EqualWeight — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  pass_thru%
  DualMA          46120   36875       9207         38      123       79.7%
  Breakout        48002   14024      26179       7799     1754       25.6%
  QuietBrk        14724    2872      11410        442      407       16.7%
  TrendPB         39140    2837      19138      17165      276        6.5%
  RSI-MR          42329    4873      25229      12227     1041        9.1%

  --------------------------------------------------------------------  [EqualWeight — union-filter overlap (per trading day)]
  Filter                              total   max/day   mean/day
  BreakoutUniverseFilter                  0         0       0.00
  ActivityTailFilter                      0         0       0.00
  PullbackUniverseFilter               1814         9       1.15
  MeanReversionUniverseFilter          6747        20       4.27
  DualMAUniverseFilter                 3430        16       2.17
  --------------------------------------------------------------------  

   Adaptive  (5-strat)      1.27   125.63%   22.24%    1.48  44.1%     4081
                         (LLM calls: 337)

  --------------------------------------------------------------------  [Strategy PnL Attribution — Adaptive]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  Breakout         2831       +93185     41.7%        +33    80.3%
  QuietBrk          457       +16057     36.5%        +35    13.8%
  TrendPB           252        +3984     55.6%        +16     3.4%
  DualMA             86        +1931     46.5%        +22     1.7%
  RSI-MR            455         +946     60.0%         +2     0.8%
  TOTAL            4081      +116102
  --------------------------------------------------------------------  [Adaptive — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  pass_thru%
  DualMA          41593   10254      31317         22       95       24.4%
  Breakout        40954   35784       1266       3904     2328       81.7%
  QuietBrk        11756    3313       8216        227      476       24.1%
  TrendPB         23727    1718      10236      11773      282        6.1%
  RSI-MR          22017    2206      12820       6991     1122        4.9%

  --------------------------------------------------------------------  [Adaptive — union-filter overlap (per trading day)]
  Filter                              total   max/day   mean/day
  BreakoutUniverseFilter                  0         0       0.00
  ActivityTailFilter                      0         0       0.00
  PullbackUniverseFilter               1814         9       1.15
  MeanReversionUniverseFilter          6747        20       4.27
  DualMAUniverseFilter                 3430        16       2.17
  -------------------------------------------------------------------- 
   --------------------------------------------------------------------  [Multi-strategy adaptive + RegimeContextAgent]
  [RCAQualityGate] 2018-01-16 → Breakout WR 30.0% < 40% over last 20 trades — CB relaxation disabled
  Adaptive+RCA (5-strat)   1.21   117.02%   23.74%    1.46  43.7%     4061
                         (LLM calls: 337)

  --------------------------------------------------------------------  [Strategy PnL Attribution — Adaptive+RCA]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  Breakout         2817       +84442     41.3%        +30    78.1%
  QuietBrk          477       +19254     37.5%        +40    17.8%
  TrendPB           226        +2181     54.4%        +10     2.0%
  DualMA             77        +1462     45.5%        +19     1.4%
  RSI-MR            464         +733     59.3%         +2     0.7%
  TOTAL            4061      +108073
  --------------------------------------------------------------------  [Adaptive+RCA — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  pass_thru%
  DualMA          41303    9166      32114         23       98       22.0%
  Breakout        40596   36476        396       3724     2362       84.0%
  QuietBrk        11910    3331       8363        216      451       24.2%
  TrendPB         23686    1674      10107      11905      325        5.7%
  RSI-MR          23361    2343      13518       7500     1219        4.8%

  --------------------------------------------------------------------  [Adaptive+RCA — union-filter overlap (per trading day)]
  Filter                              total   max/day   mean/day
  BreakoutUniverseFilter                  0         0       0.00
  ActivityTailFilter                      0         0       0.00
  PullbackUniverseFilter               1814         9       1.15
  MeanReversionUniverseFilter          6747        20       4.27
  DualMAUniverseFilter                 3430        16       2.17
  RCA delta              -0.06    -8.62%

  ══════════════════════════════════════════════════════════════════
  OPPORTUNITY QUALITY SUMMARY  [Full  2018–2024]
  ══════════════════════════════════════════════════════════════════
  Trades analyzed  : 13804  (6202 winners / 7602 losers)
  ──────────────────────────────────────────────────────────────────
  Breakout quality:
    Follow-through rate  :   52.2%   (price continued post-exit)
    False breakout rate  :   34.5%   (MFE>2% but final return <0)
    Persistence half-life:    0.0 days (median survival above entry)
    Avg MFE efficiency   : -0.215      (1.00 = exit at peak)
  ──────────────────────────────────────────────────────────────────
  Continuation decay (post-exit drift):
                      1D        3D        5D
    Winners      -0.04%    +0.42%    +0.74%
    Losers       -0.10%    +0.09%    +0.22%
  ──────────────────────────────────────────────────────────────────
  Universe diagnostics (1581 days):
    Avg stability score  : 0.331  (0=fully churning, 1=static)
    Avg daily turnover   : 54.0%
    Avg leader half-life : 2.0 days
    Stability vs PnL corr: +0.000  (>0 = stable universe → better trades)
    Turnover vs success  : +0.003  (<0 = higher churn → fewer successes)
  ──────────────────────────────────────────────────────────────────
  Per-regime breakdown (entry regime):
    Regime                           N  WinRate    AvgRet
    HIGH_VOL_SIDEWAYS              785    49.7%     0.30%
    HIGH_VOL_UPTREND              5847    45.4%     0.97%
    LOW_VOL_SIDEWAYS               875    51.0%     1.83%
    LOW_VOL_UPTREND               2456    42.1%     0.51%
    MID_VOL_SIDEWAYS               790    49.6%     0.48%
    MID_VOL_UPTREND               3051    42.0%     0.98%
  ──────────────────────────────────────────────────────────────────
  ══════════════════════════════════════════════════════════════════

  //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


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
  EqualWeight (5-strat)   -0.59    -3.84%    7.74%    0.82  41.6%      935

  --------------------------------------------------------------------  [Strategy PnL Attribution — EqualWeight]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  RSI-MR            317         +207     52.1%         +1    -4.4%
  TrendPB            55          -83     43.6%         -2     1.8%
  DualMA             25        -1262     20.0%        -50    26.7%
  QuietBrk           88        -1707     25.0%        -19    36.1%
  Breakout          450        -1885     38.4%         -4    39.8%
  TOTAL             935        -4732
  --------------------------------------------------------------------  [EqualWeight — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  pass_thru%
  DualMA           6766    5408       1354          4       18       79.7%
  Breakout         7111    2058       3642       1411      187       26.3%
  QuietBrk         2051     412       1570         69       51       17.6%
  TrendPB          5884     532       2991       2361       32        8.5%
  RSI-MR           6559     975       3917       1667      149       12.6%

  --------------------------------------------------------------------  [EqualWeight — union-filter overlap (per trading day)]
  Filter                              total   max/day   mean/day
  BreakoutUniverseFilter                  0         0       0.00
  ActivityTailFilter                      0         0       0.00
  PullbackUniverseFilter                291         8       1.10
  MeanReversionUniverseFilter          1099        16       4.15
  DualMAUniverseFilter                  556        12       2.10
  -------------------------------------------------------------------- 
  Adaptive  (5-strat)     -0.61    -6.24%   11.32%    0.76  37.7%      616
                         (LLM calls: 58)

  --------------------------------------------------------------------  [Strategy PnL Attribution — Adaptive]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  RSI-MR             89          +95     50.6%         +1    -1.2%
  DualMA             16         -337     31.2%        -21     4.2%
  TrendPB            32         -453     46.9%        -14     5.6%
  QuietBrk           61        -2672     23.0%        -44    33.1%
  Breakout          418        -4717     36.6%        -11    58.4%
  TOTAL             616        -8083
  --------------------------------------------------------------------  [Adaptive — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  pass_thru%
  DualMA           6013    1873       4136          4       19       30.8%
  Breakout         5856    4862        257        737      268       78.4%
  QuietBrk         1414     429        958         27       34       27.9%
  TrendPB          2312     276       1005       1031       27       10.8%
  RSI-MR           1530     292        910        328       69       14.6%

  --------------------------------------------------------------------  [Adaptive — union-filter overlap (per trading day)]
  Filter                              total   max/day   mean/day
  BreakoutUniverseFilter                  0         0       0.00
  ActivityTailFilter                      0         0       0.00
  PullbackUniverseFilter                291         8       1.10
  MeanReversionUniverseFilter          1099        16       4.15
  DualMAUniverseFilter                  556        12       2.10
  --------------------------------------------------------------------  [Multi-strategy adaptive + RegimeContextAgent]
  [RCAQualityGate] 2019-01-21 → Breakout WR 20.0% < 40% over last 15 trades — CB relaxation disabled
  Adaptive+RCA (5-strat)  -0.59    -6.06%   11.02%    0.76  38.1%      611
                         (LLM calls: 58)

  --------------------------------------------------------------------  [Strategy PnL Attribution — Adaptive+RCA]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  RSI-MR             79          +70     53.2%         +1    -0.9%
  DualMA             16         -233     37.5%        -15     2.9%
  TrendPB            31         -368     45.2%        -12     4.6%
  QuietBrk           67        -2532     23.9%        -38    31.5%
  Breakout          418        -4963     37.1%        -12    61.8%
  TOTAL             611        -8026
  --------------------------------------------------------------------  [Adaptive+RCA — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  pass_thru%
  DualMA           6042    1861       4177          4       19       30.5%
  Breakout         5906    4919        256        731      268       78.8%
  QuietBrk         1490     451       1011         28       33       28.1%
  TrendPB          2188     256        907       1025       24       10.6%
  RSI-MR           1497     255        881        361       66       12.6%

  --------------------------------------------------------------------  [Adaptive+RCA — union-filter overlap (per trading day)]
  Filter                              total   max/day   mean/day
  BreakoutUniverseFilter                  0         0       0.00
  ActivityTailFilter                      0         0       0.00
  PullbackUniverseFilter                291         8       1.10
  MeanReversionUniverseFilter          1099        16       4.15
  DualMAUniverseFilter                  556        12       2.10
  RCA delta              + 0.02  +   0.18%

  ══════════════════════════════════════════════════════════════════
  OPPORTUNITY QUALITY SUMMARY  [Bull  2019–2020]
  ══════════════════════════════════════════════════════════════════
  Trades analyzed  : 2162  (854 winners / 1308 losers)
  ──────────────────────────────────────────────────────────────────
  Breakout quality:
    Follow-through rate  :   47.4%   (price continued post-exit)
    False breakout rate  :   38.2%   (MFE>2% but final return <0)
    Persistence half-life:    0.0 days (median survival above entry)
    Avg MFE efficiency   : -0.284      (1.00 = exit at peak)
  ──────────────────────────────────────────────────────────────────
  Continuation decay (post-exit drift):
                      1D        3D        5D
    Winners      -0.05%    +0.15%    +0.16%
    Losers       -0.05%    -0.16%    -0.18%
  ──────────────────────────────────────────────────────────────────
  Universe diagnostics (265 days):
    Avg stability score  : 0.331  (0=fully churning, 1=static)
    Avg daily turnover   : 54.3%
    Avg leader half-life : 1.9 days
    Stability vs PnL corr: +0.011  (>0 = stable universe → better trades)
    Turnover vs success  : +0.053  (<0 = higher churn → fewer successes)
  ──────────────────────────────────────────────────────────────────
  Per-regime breakdown (entry regime):
    Regime                           N  WinRate    AvgRet
    HIGH_VOL_SIDEWAYS               93    46.2%     0.87%
    HIGH_VOL_UPTREND               599    46.9%     0.60%
    LOW_VOL_SIDEWAYS               220    46.8%    -0.15%
    LOW_VOL_UPTREND                554    31.8%    -1.02%
    MID_VOL_SIDEWAYS               126    48.4%    -0.85%
    MID_VOL_UPTREND                570    33.3%    -0.95%
  ──────────────────────────────────────────────────────────────────
  ══════════════════════════════════════════════════════════════════


///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

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
  EqualWeight (5-strat)    2.51    27.52%    5.29%    1.95  50.2%      990

  --------------------------------------------------------------------  [Strategy PnL Attribution — EqualWeight]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  Breakout          520       +17355     43.3%        +33    69.7%
  QuietBrk           96        +3399     41.7%        +35    13.6%
  RSI-MR            248        +2505     65.7%        +10    10.1%
  TrendPB           106        +1522     58.5%        +14     6.1%
  DualMA             20         +127     35.0%         +6     0.5%
  TOTAL             990       +24907
  --------------------------------------------------------------------  [EqualWeight — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  pass_thru%
  DualMA           8331    6683       1638         10       22       80.0%
  Breakout         8533    2359       4803       1371      261       24.6%
  QuietBrk         2688     497       2114         77       50       16.6%
  TrendPB          7082     564       2833       3685       71        7.0%
  RSI-MR           7478     714       4508       2256      100        8.2%

  --------------------------------------------------------------------  [EqualWeight — union-filter overlap (per trading day)]
  Filter                              total   max/day   mean/day
  BreakoutUniverseFilter                  0         0       0.00
  ActivityTailFilter                      0         0       0.00
  PullbackUniverseFilter                305         8       1.22
  MeanReversionUniverseFilter          1171        19       4.68
  DualMAUniverseFilter                  604        13       2.42
  -------------------------------------------------------------------- 
   Adaptive  (5-strat)      2.24    31.90%    6.86%    1.83  46.8%      789
                         (LLM calls: 54)


  --------------------------------------------------------------------  [Strategy PnL Attribution — Adaptive]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  Breakout          515       +23305     42.3%        +45    78.5%
  QuietBrk           78        +4569     39.7%        +59    15.4%
  TrendPB            78        +1783     57.7%        +23     6.0%
  RSI-MR            108         +119     66.7%         +1     0.4%
  DualMA             10         -104     30.0%        -10    -0.4%
  TOTAL             789       +29672
  --------------------------------------------------------------------  [Adaptive — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  pass_thru%
  DualMA           7665    1608       6049          8       16       20.8%
  Breakout         7530    6645         65        820      346       83.7%
  QuietBrk         2222     573       1591         58       60       23.1%
  TrendPB          5398     420       1879       3099       96        6.0%
  RSI-MR           5285     455       3120       1710      177        5.3%

  --------------------------------------------------------------------  [Adaptive — union-filter overlap (per trading day)]
  Filter                              total   max/day   mean/day
  BreakoutUniverseFilter                  0         0       0.00
  ActivityTailFilter                      0         0       0.00
  PullbackUniverseFilter                305         8       1.22
  MeanReversionUniverseFilter          1171        19       4.68
  DualMAUniverseFilter                  604        13       2.42
  --------------------------------------------------------------------  [Multi-strategy adaptive + RegimeContextAgent]
  [RCAQualityGate] 2020-01-13 → Breakout WR 10.0% < 40% over last 10 trades — CB relaxation disabled
  Adaptive+RCA (5-strat)   2.31    33.26%    6.52%    1.87  45.4%      762
                           (LLM calls: 54)

  --------------------------------------------------------------------  [Strategy PnL Attribution — Adaptive+RCA]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  Breakout          502       +24892     41.6%        +50    80.6%
  QuietBrk           81        +5109     39.5%        +63    16.5%
  TrendPB            62         +752     59.7%        +12     2.4%
  RSI-MR            107         +246     60.7%         +2     0.8%
  DualMA             10         -103     30.0%        -10    -0.3%
  TOTAL             762       +30896
  --------------------------------------------------------------------  [Adaptive+RCA — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  pass_thru%
  DualMA           7595    1593       5993          9       16       20.8%
  Breakout         7429    6576         61        792      367       83.6%
  QuietBrk         2209     578       1575         56       58       23.5%
  TrendPB          5010     386       1671       2953      105        5.6%
  RSI-MR           5087     442       3028       1617      174        5.3%

  --------------------------------------------------------------------  [Adaptive+RCA — union-filter overlap (per trading day)]
  Filter                              total   max/day   mean/day
  BreakoutUniverseFilter                  0         0       0.00
  ActivityTailFilter                      0         0       0.00
  PullbackUniverseFilter                305         8       1.22
  MeanReversionUniverseFilter          1171        19       4.68
  DualMAUniverseFilter                  604        13       2.42
  RCA delta              + 0.07  +   1.36%

  ══════════════════════════════════════════════════════════════════
  OPPORTUNITY QUALITY SUMMARY  [Crash 2020]
  ══════════════════════════════════════════════════════════════════
  Trades analyzed  : 2541  (1212 winners / 1329 losers)
  ──────────────────────────────────────────────────────────────────
  Breakout quality:
    Follow-through rate  :   56.9%   (price continued post-exit)
    False breakout rate  :   37.9%   (MFE>2% but final return <0)
    Persistence half-life:    0.0 days (median survival above entry)
    Avg MFE efficiency   : -0.151      (1.00 = exit at peak)
  ──────────────────────────────────────────────────────────────────
  Continuation decay (post-exit drift):
                      1D        3D        5D
    Winners      +0.06%    +0.91%    +1.28%
    Losers       -0.07%    +0.61%    +0.99%
  ──────────────────────────────────────────────────────────────────
  Universe diagnostics (250 days):
    Avg stability score  : 0.356  (0=fully churning, 1=static)
    Avg daily turnover   : 52.1%
    Avg leader half-life : 2.1 days
    Stability vs PnL corr: +0.053  (>0 = stable universe → better trades)
    Turnover vs success  : +0.059  (<0 = higher churn → fewer successes)
  ──────────────────────────────────────────────────────────────────
  Per-regime breakdown (entry regime):
    Regime                           N  WinRate    AvgRet
    HIGH_VOL_SIDEWAYS               71    54.9%    -0.21%
    HIGH_VOL_UPTREND               875    43.0%     1.39%
    LOW_VOL_SIDEWAYS               232    64.7%     4.71%
    LOW_VOL_UPTREND                631    48.0%     1.51%
    MID_VOL_SIDEWAYS               108    68.5%     2.88%
    MID_VOL_UPTREND                624    43.3%     1.56%
  ──────────────────────────────────────────────────────────────────
  ══════════════════════════════════════════════════════════════════

  //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

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
  EqualWeight (5-strat)    2.97    67.25%    6.29%    2.10  51.3%     1989

  --------------------------------------------------------------------  [Strategy PnL Attribution — EqualWeight]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  Breakout         1037       +44089     46.3%        +43    65.9%
  QuietBrk          193       +10952     44.6%        +57    16.4%
  RSI-MR            505        +6290     60.8%        +12     9.4%
  DualMA             41        +3800     53.7%        +93     5.7%
  TrendPB           213        +1741     59.2%         +8     2.6%
  TOTAL            1989       +66872
  --------------------------------------------------------------------  [EqualWeight — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  pass_thru%
  DualMA          16461   13277       3160         24       29       80.5%
  Breakout        17171    4711       9640       2820      437       24.9%
  QuietBrk         5285     947       4165        173       98       16.1%
  TrendPB         14284    1119       5997       7168      113        7.0%
  RSI-MR          15028    1426       9112       4490      177        8.3%

  --------------------------------------------------------------------  [EqualWeight — union-filter overlap (per trading day)]
  Filter                              total   max/day   mean/day
  BreakoutUniverseFilter                  0         0       0.00
  ActivityTailFilter                      0         0       0.00
  PullbackUniverseFilter                583         9       1.34
  MeanReversionUniverseFilter          2194        20       5.04
  DualMAUniverseFilter                  983        13       2.26
  -------------------------------------------------------------------- 
  Adaptive  (5-strat)      2.80    85.78%    9.17%    2.04  49.3%     1649
                         (LLM calls: 93)

  --------------------------------------------------------------------  [Strategy PnL Attribution — Adaptive]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  Breakout         1035       +67473     46.2%        +65    79.3%
  QuietBrk          171       +13715     42.1%        +80    16.1%
  TrendPB           166        +1576     60.2%         +9     1.9%
  DualMA             18        +1485     50.0%        +83     1.7%
  RSI-MR            259         +869     59.5%         +3     1.0%
  TOTAL            1649       +85117
  --------------------------------------------------------------------  [Adaptive — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  pass_thru%
  DualMA          15314    3369      11930         15       21       21.9%
  Breakout        15476   13109        517       1850      555       81.1%
  QuietBrk         4704    1241       3343        120      132       23.6%
  TrendPB         12518     876       4814       6828      167        5.7%
  RSI-MR          12478    1128       7453       3897      489        5.1%

  --------------------------------------------------------------------  [Adaptive — union-filter overlap (per trading day)]
  Filter                              total   max/day   mean/day
  BreakoutUniverseFilter                  0         0       0.00
  ActivityTailFilter                      0         0       0.00
  PullbackUniverseFilter                583         9       1.34
  MeanReversionUniverseFilter          2194        20       5.04
  DualMAUniverseFilter                  983        13       2.26
  --------------------------------------------------------------------  [Multi-strategy adaptive + RegimeContextAgent]
  [RCAQualityGate] 2020-06-10 → Breakout WR 9.1% < 40% over last 11 trades — CB relaxation disabled
  Adaptive+RCA (5-strat)   2.66    80.56%    8.94%    1.97  48.3%     1643
                         (LLM calls: 93)

  --------------------------------------------------------------------  [Strategy PnL Attribution — Adaptive+RCA]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  Breakout         1050       +65273     45.5%        +62    81.8%
  QuietBrk          166       +11915     41.6%        +72    14.9%
  DualMA             18        +1274     44.4%        +71     1.6%
  TrendPB           149         +731     57.0%         +5     0.9%
  RSI-MR            260         +600     59.2%         +2     0.8%
  TOTAL            1643       +79793
  --------------------------------------------------------------------  [Adaptive+RCA — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  pass_thru%
  DualMA          15170    2945      12211         14       22       19.3%
  Breakout        15299   13427        129       1743      562       84.1%
  QuietBrk         4586    1194       3269        123      150       22.8%
  TrendPB         12276     836       4628       6812      192        5.2%
  RSI-MR          12807    1161       7618       4028      509        5.1%

  --------------------------------------------------------------------  [Adaptive+RCA — union-filter overlap (per trading day)]
  Filter                              total   max/day   mean/day
  BreakoutUniverseFilter                  0         0       0.00
  ActivityTailFilter                      0         0       0.00
  PullbackUniverseFilter                583         9       1.34
  MeanReversionUniverseFilter          2194        20       5.04
  DualMAUniverseFilter                  983        13       2.26
  RCA delta              -0.14    -5.22%

  ══════════════════════════════════════════════════════════════════
  OPPORTUNITY QUALITY SUMMARY  [Recov 2020–2021]
  ══════════════════════════════════════════════════════════════════
  Trades analyzed  : 5281  (2628 winners / 2653 losers)
  ──────────────────────────────────────────────────────────────────
  Breakout quality:
    Follow-through rate  :   54.6%   (price continued post-exit)
    False breakout rate  :   35.3%   (MFE>2% but final return <0)
    Persistence half-life:    0.0 days (median survival above entry)
    Avg MFE efficiency   : -0.128      (1.00 = exit at peak)
  ──────────────────────────────────────────────────────────────────
  Continuation decay (post-exit drift):
                      1D        3D        5D
    Winners      -0.04%    +0.80%    +1.21%
    Losers       -0.10%    +0.41%    +0.78%
  ──────────────────────────────────────────────────────────────────
  Universe diagnostics (435 days):
    Avg stability score  : 0.346  (0=fully churning, 1=static)
    Avg daily turnover   : 53.3%
    Avg leader half-life : 2.0 days
    Stability vs PnL corr: +0.014  (>0 = stable universe → better trades)
    Turnover vs success  : -0.020  (<0 = higher churn → fewer successes)
  ──────────────────────────────────────────────────────────────────
  Per-regime breakdown (entry regime):
    Regime                           N  WinRate    AvgRet
    HIGH_VOL_SIDEWAYS              286    53.5%     0.74%
    HIGH_VOL_UPTREND              2433    48.1%     1.90%
    LOW_VOL_SIDEWAYS               259    65.6%     5.53%
    LOW_VOL_UPTREND                791    49.7%     1.73%
    MID_VOL_SIDEWAYS               296    59.1%     2.69%
    MID_VOL_UPTREND               1216    46.6%     1.89%
  ──────────────────────────────────────────────────────────────────
  ══════════════════════════════════════════════════════════════════

  /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

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
  EqualWeight (5-strat)    0.02    -0.09%    7.55%    1.00  40.9%      709

  --------------------------------------------------------------------  [Strategy PnL Attribution — EqualWeight]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  Breakout          376        +2351     38.8%         +6 -2234.9%
  DualMA             28         +177     50.0%         +6  -168.3%
  TrendPB            50         -356     46.0%         -7   338.4%
  QuietBrk           72         -895     26.4%        -12   850.7%
  RSI-MR            183        -1382     48.1%         -8  1314.0%
  TOTAL             709         -105
  --------------------------------------------------------------------  [EqualWeight — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  pass_thru%
  DualMA           5812    4519       1291          2       27       77.3%
  Breakout         6015    2093       2984        938      396       28.2%
  QuietBrk         1659     379       1213         67       79       18.1%
  TrendPB          4740     373       2356       2011       63        6.5%
  RSI-MR           5266     726       3059       1481      245        9.1%

  --------------------------------------------------------------------  [EqualWeight — union-filter overlap (per trading day)]
  Filter                              total   max/day   mean/day
  BreakoutUniverseFilter                  0         0       0.00
  ActivityTailFilter                      0         0       0.00
  PullbackUniverseFilter                306         7       1.23
  MeanReversionUniverseFilter          1030        17       4.15
  DualMAUniverseFilter                  668        16       2.69
  --------------------------------------------------------------------  
  Adaptive  (5-strat)      0.39     3.19%    9.94%    1.11  38.3%      515
                         (LLM calls: 52)

  --------------------------------------------------------------------  [Strategy PnL Attribution — Adaptive]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  Breakout          382        +5293     37.7%        +14   164.2%
  RSI-MR             42          +54     45.2%         +1     1.7%
  DualMA             13         -155     46.2%        -12    -4.8%
  TrendPB            31         -554     38.7%        -18   -17.2%
  QuietBrk           47        -1416     34.0%        -30   -43.9%
  TOTAL             515        +3223
  --------------------------------------------------------------------  [Adaptive — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  pass_thru%
  DualMA           5252    1534       3716          2       20       28.8%
  Breakout         5275    4625        208        442      440       79.3%
  QuietBrk         1084     347        707         30       58       26.7%
  TrendPB          3003     245       1321       1437       62        6.1%
  RSI-MR           1963     256       1176        531      155        5.1%

  --------------------------------------------------------------------  [Adaptive — union-filter overlap (per trading day)]
  Filter                              total   max/day   mean/day
  BreakoutUniverseFilter                  0         0       0.00
  ActivityTailFilter                      0         0       0.00
  PullbackUniverseFilter                306         7       1.23
  MeanReversionUniverseFilter          1030        17       4.15
  DualMAUniverseFilter                  668        16       2.69
  --------------------------------------------------------------------  [Multi-strategy adaptive + RegimeContextAgent]
  [RCAQualityGate] 2022-01-18 → Breakout WR 35.0% < 40% over last 20 trades — CB relaxation disabled
  Adaptive+RCA (5-strat)   0.36     2.92%    9.93%    1.11  37.3%      509
                         (LLM calls: 52)

  --------------------------------------------------------------------  [Strategy PnL Attribution — Adaptive+RCA]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  Breakout          385        +5253     38.2%        +14   177.8%
  RSI-MR             35          -86     40.0%         -2    -2.9%
  DualMA             13         -155     46.2%        -12    -5.2%
  TrendPB            27         -703     33.3%        -26   -23.8%
  QuietBrk           49        -1355     28.6%        -28   -45.9%
  TOTAL             509        +2954
  --------------------------------------------------------------------  [Adaptive+RCA — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  pass_thru%
  DualMA           5203    1520       3681          2       20       28.8%
  Breakout         5229    4626        198        405      443       80.0%
  QuietBrk         1111     338        745         28       59       25.1%
  TrendPB          2868     235       1262       1371       59        6.1%
  RSI-MR           1796     235       1076        485      148        4.8%

  --------------------------------------------------------------------  [Adaptive+RCA — union-filter overlap (per trading day)]
  Filter                              total   max/day   mean/day
  BreakoutUniverseFilter                  0         0       0.00
  ActivityTailFilter                      0         0       0.00
  PullbackUniverseFilter                306         7       1.23
  MeanReversionUniverseFilter          1030        17       4.15
  DualMAUniverseFilter                  668        16       2.69
  RCA delta              -0.03    -0.27%

  ══════════════════════════════════════════════════════════════════
  OPPORTUNITY QUALITY SUMMARY  [Bear  2022]
  ══════════════════════════════════════════════════════════════════
  Trades analyzed  : 1733  (677 winners / 1056 losers)
  ──────────────────────────────────────────────────────────────────
  Breakout quality:
    Follow-through rate  :   46.2%   (price continued post-exit)
    False breakout rate  :   37.2%   (MFE>2% but final return <0)
    Persistence half-life:    0.0 days (median survival above entry)
    Avg MFE efficiency   : -0.309      (1.00 = exit at peak)
  ──────────────────────────────────────────────────────────────────
  Continuation decay (post-exit drift):
                      1D        3D        5D
    Winners      +0.06%    +0.16%    +0.15%
    Losers       -0.12%    -0.17%    -0.42%
  ──────────────────────────────────────────────────────────────────
  Universe diagnostics (248 days):
    Avg stability score  : 0.327  (0=fully churning, 1=static)
    Avg daily turnover   : 53.7%
    Avg leader half-life : 2.0 days
    Stability vs PnL corr: -0.101  (>0 = stable universe → better trades)
    Turnover vs success  : +0.001  (<0 = higher churn → fewer successes)
  ──────────────────────────────────────────────────────────────────
  Per-regime breakdown (entry regime):
    Regime                           N  WinRate    AvgRet
    HIGH_VOL_SIDEWAYS               59    39.0%    -1.20%
    HIGH_VOL_UPTREND               379    36.1%    -0.38%
    LOW_VOL_SIDEWAYS               216    50.0%     1.68%
    LOW_VOL_UPTREND                506    37.2%    -0.42%
    MID_VOL_SIDEWAYS               138    39.9%    -0.71%
    MID_VOL_UPTREND                435    38.2%     0.12%
  ──────────────────────────────────────────────────────────────────

  //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


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
  EqualWeight (5-strat)    1.12    21.87%    7.55%    1.34  45.5%     1939

  --------------------------------------------------------------------  [Strategy PnL Attribution — EqualWeight]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  Breakout         1051       +15324     41.8%        +15    79.6%
  QuietBrk          226        +2091     33.6%         +9    10.9%
  DualMA             61        +1079     52.5%        +18     5.6%
  TrendPB           117         +879     55.6%         +8     4.6%
  RSI-MR            484         -129     55.8%         -0    -0.7%
  TOTAL            1939       +19244
  --------------------------------------------------------------------  [EqualWeight — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  pass_thru%
  DualMA          17341   13753       3580          8       67       78.9%
  Breakout        17753    5429       9784       2540      961       25.2%
  QuietBrk         5426    1164       4114        148      236       17.1%
  TrendPB         14127     844       7576       5707      101        5.3%
  RSI-MR          15377    1746       8955       4676      541        7.8%

  --------------------------------------------------------------------  [EqualWeight — union-filter overlap (per trading day)]
  Filter                              total   max/day   mean/day
  BreakoutUniverseFilter                  0         0       0.00
  ActivityTailFilter                      0         0       0.00
  PullbackUniverseFilter                734         8       1.24
  MeanReversionUniverseFilter          2457        19       4.14
  DualMAUniverseFilter                 1376        16       2.32
  -------------------------------------------------------------------- 
Adaptive  (5-strat)      1.47    40.22%    9.94%    1.46  44.5%     1504
                         (LLM calls: 126)

  --------------------------------------------------------------------  [Strategy PnL Attribution — Adaptive]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  Breakout         1038       +25668     41.3%        +25    73.5%
  QuietBrk          180        +8548     41.7%        +47    24.5%
  DualMA             31         +676     48.4%        +22     1.9%
  RSI-MR            182         +373     63.2%         +2     1.1%
  TrendPB            73         -359     49.3%         -5    -1.0%
  TOTAL            1504       +34907
  --------------------------------------------------------------------  [Adaptive — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  pass_thru%
  DualMA          15931    3503      12420          8       49       21.7%
  Breakout        15781   14076        342       1363     1091       82.3%
  QuietBrk         4610    1331       3206         73      227       23.9%
  TrendPB         11151     571       5396       5184      128        4.0%
  RSI-MR          10529    1086       6047       3396      664        4.0%

  --------------------------------------------------------------------  [Adaptive — union-filter overlap (per trading day)]
  Filter                              total   max/day   mean/day
  BreakoutUniverseFilter                  0         0       0.00
  ActivityTailFilter                      0         0       0.00
  PullbackUniverseFilter                734         8       1.24
  MeanReversionUniverseFilter          2457        19       4.14
  DualMAUniverseFilter                 1376        16       2.32
  --------------------------------------------------------------------  [Multi-strategy adaptive + RegimeContextAgent]
  [RCAQualityGate] 2022-01-18 → Breakout WR 35.0% < 40% over last 20 trades — CB relaxation disabled
  Adaptive+RCA (5-strat)   1.42    38.97%    9.93%    1.45  44.3%     1491
                         (LLM calls: 126)

  --------------------------------------------------------------------  [Strategy PnL Attribution — Adaptive+RCA]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  Breakout         1031       +25185     41.4%        +24    74.3%
  QuietBrk          186        +8371     38.7%        +45    24.7%
  DualMA             31         +646     51.6%        +21     1.9%
  RSI-MR            178         +389     63.5%         +2     1.1%
  TrendPB            65         -672     50.8%        -10    -2.0%
  TOTAL            1491       +33918
  --------------------------------------------------------------------  [Adaptive+RCA — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  pass_thru%
  DualMA          15941    3516      12416          9       52       21.7%
  Breakout        15745   14055        342       1348     1117       82.2%
  QuietBrk         4715    1353       3298         64      237       23.7%
  TrendPB         10857     545       5315       4997      129        3.8%
  RSI-MR          10519    1072       6032       3415      650        4.0%

  --------------------------------------------------------------------  [Adaptive+RCA — union-filter overlap (per trading day)]
  Filter                              total   max/day   mean/day
  BreakoutUniverseFilter                  0         0       0.00
  ActivityTailFilter                      0         0       0.00
  PullbackUniverseFilter                734         8       1.24
  MeanReversionUniverseFilter          2457        19       4.14
  DualMAUniverseFilter                 1376        16       2.32
  RCA delta              -0.05    -1.25%

  ══════════════════════════════════════════════════════════════════
  OPPORTUNITY QUALITY SUMMARY  [Recent2022–2024]
  ══════════════════════════════════════════════════════════════════
  Trades analyzed  : 4934  (2213 winners / 2721 losers)
  ──────────────────────────────────────────────────────────────────
  Breakout quality:
    Follow-through rate  :   54.5%   (price continued post-exit)
    False breakout rate  :   31.8%   (MFE>2% but final return <0)
    Persistence half-life:    0.0 days (median survival above entry)
    Avg MFE efficiency   : -0.222      (1.00 = exit at peak)
  ──────────────────────────────────────────────────────────────────
  Continuation decay (post-exit drift):
                      1D        3D        5D
    Winners      +0.01%    +0.40%    +0.79%
    Losers       -0.01%    +0.15%    +0.26%
  ──────────────────────────────────────────────────────────────────
  Universe diagnostics (594 days):
    Avg stability score  : 0.320  (0=fully churning, 1=static)
    Avg daily turnover   : 54.4%
    Avg leader half-life : 2.0 days
    Stability vs PnL corr: -0.044  (>0 = stable universe → better trades)
    Turnover vs success  : -0.006  (<0 = higher churn → fewer successes)
  ──────────────────────────────────────────────────────────────────
  Per-regime breakdown (entry regime):
    Regime                           N  WinRate    AvgRet
    HIGH_VOL_SIDEWAYS              242    51.7%     0.43%
    HIGH_VOL_UPTREND              2046    44.5%     0.61%
    LOW_VOL_SIDEWAYS               344    48.0%     1.30%
    LOW_VOL_UPTREND               1007    41.2%     0.37%
    MID_VOL_SIDEWAYS               262    49.2%     0.10%
    MID_VOL_UPTREND               1033    45.3%     1.32%
  ──────────────────────────────────────────────────────────────────

  ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

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
  EqualWeight (5-strat)   -0.65    -3.66%    4.59%    0.81  36.9%      647

  --------------------------------------------------------------------  [Strategy PnL Attribution — EqualWeight]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  QuietBrk           87         +365     31.0%         +4   -10.0%
  TrendPB            18          -42     50.0%         -2     1.2%
  RSI-MR            164         -419     50.0%         -3    11.5%
  DualMA             14         -751     14.3%        -54    20.5%
  Breakout          364        -2809     32.7%         -8    76.8%
  TOTAL             647        -3656
  --------------------------------------------------------------------  [EqualWeight — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  pass_thru%
  DualMA           5805    4439       1364          2       41       75.8%
  Breakout         5682    1949       2960        773      484       25.8%
  QuietBrk         1995     474       1473         48      134       17.0%
  TrendPB          4283     229       2575       1479       30        4.6%
  RSI-MR           4870     726       2814       1330      303        8.7%

  --------------------------------------------------------------------  [EqualWeight — union-filter overlap (per trading day)]
  Filter                              total   max/day   mean/day
  BreakoutUniverseFilter                  0         0       0.00
  ActivityTailFilter                      0         0       0.00
  PullbackUniverseFilter                249         8       0.82
  MeanReversionUniverseFilter           993        18       3.26
  DualMAUniverseFilter                  565        11       1.85
  -------------------------------------------------------------------- 
   Adaptive  (5-strat)     -0.33    -3.00%    6.39%    0.89  35.5%      538
                         (LLM calls: 66)

  --------------------------------------------------------------------  [Strategy PnL Attribution — Adaptive]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  QuietBrk           86         +770     33.7%         +9   -25.6%
  RSI-MR             52          +64     51.9%         +1    -2.1%
  TrendPB             9           +5     44.4%         +1    -0.2%
  DualMA             11         -561     18.2%        -51    18.7%
  Breakout          380        -3282     33.9%         -9   109.3%
  TOTAL             538        -3004
  --------------------------------------------------------------------  [Adaptive — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  pass_thru%
  DualMA           5878    1506       4372          0       26       25.2%
  Breakout         5598    4905        167        526      480       79.0%
  QuietBrk         1928     624       1283         21      100       27.2%
  TrendPB          2941     116       1684       1141       28        3.0%
  RSI-MR           2795     373       1643        779      244        4.6%

  --------------------------------------------------------------------  [Adaptive — union-filter overlap (per trading day)]
  Filter                              total   max/day   mean/day
  BreakoutUniverseFilter                  0         0       0.00
  ActivityTailFilter                      0         0       0.00
  PullbackUniverseFilter                249         8       0.82
  MeanReversionUniverseFilter           993        18       3.26
  DualMAUniverseFilter                  565        11       1.85
  --------------------------------------------------------------------  [Multi-strategy adaptive + RegimeContextAgent]

  Adaptive  (5-strat)     -0.33    -3.00%    6.39%    0.89  35.5%      538
                         (LLM calls: 66)

  --------------------------------------------------------------------  [Strategy PnL Attribution — Adaptive]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  QuietBrk           86         +770     33.7%         +9   -25.6%
  RSI-MR             52          +64     51.9%         +1    -2.1%
  TrendPB             9           +5     44.4%         +1    -0.2%
  DualMA             11         -561     18.2%        -51    18.7%
  Breakout          380        -3282     33.9%         -9   109.3%
  TOTAL             538        -3004
  --------------------------------------------------------------------  [Adaptive — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  pass_thru%
  DualMA           5878    1506       4372          0       26       25.2%
  Breakout         5598    4905        167        526      480       79.0%
  QuietBrk         1928     624       1283         21      100       27.2%
  TrendPB          2941     116       1684       1141       28        3.0%
  RSI-MR           2795     373       1643        779      244        4.6%

  --------------------------------------------------------------------  [Adaptive — union-filter overlap (per trading day)]
  Filter                              total   max/day   mean/day
  BreakoutUniverseFilter                  0         0       0.00
  ActivityTailFilter                      0         0       0.00
  PullbackUniverseFilter                249         8       0.82
  MeanReversionUniverseFilter           993        18       3.26
  DualMAUniverseFilter                  565        11       1.85
  --------------------------------------------------------------------  [Multi-strategy adaptive + RegimeContextAgent]
  [RCAQualityGate] 2025-04-01 → Breakout WR 10.0% < 40% over last 10 trades — CB relaxation disabled
  Adaptive+RCA (5-strat)  -0.27    -2.45%    5.67%    0.91  33.9%      545
                         (LLM calls: 66)

  --------------------------------------------------------------------  [Strategy PnL Attribution — Adaptive+RCA]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  QuietBrk           84        +1445     32.1%        +17   -60.7%
  RSI-MR             53          -54     43.4%         -1     2.3%
  TrendPB             7          -82     28.6%        -12     3.4%
  DualMA             11         -468     18.2%        -43    19.7%
  Breakout          390        -3221     33.6%         -8   135.4%
  TOTAL             545        -2379
  --------------------------------------------------------------------  [Adaptive+RCA — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  pass_thru%
  DualMA           5906    1479       4427          0       25       24.6%
  Breakout         5639    4958        164        517      462       79.7%
  QuietBrk         1936     613       1295         28      100       26.5%
  TrendPB          3316     127       1920       1269       35        2.8%
  RSI-MR           3131     389       1803        939      262        4.1%

  --------------------------------------------------------------------  [Adaptive+RCA — union-filter overlap (per trading day)]
  Filter                              total   max/day   mean/day
  BreakoutUniverseFilter                  0         0       0.00
  ActivityTailFilter                      0         0       0.00
  PullbackUniverseFilter                249         8       0.82
  MeanReversionUniverseFilter           993        18       3.26
  DualMAUniverseFilter                  565        11       1.85
  RCA delta              + 0.06  +   0.56%

  ══════════════════════════════════════════════════════════════════
  OPPORTUNITY QUALITY SUMMARY  [Live  2025–2026]
  ══════════════════════════════════════════════════════════════════
  Trades analyzed  : 1730  (615 winners / 1115 losers)
  ──────────────────────────────────────────────────────────────────
  Breakout quality:
    Follow-through rate  :   53.0%   (price continued post-exit)
    False breakout rate  :   27.7%   (MFE>2% but final return <0)
    Persistence half-life:    0.0 days (median survival above entry)
    Avg MFE efficiency   : -0.350      (1.00 = exit at peak)
  ──────────────────────────────────────────────────────────────────
  Continuation decay (post-exit drift):
                      1D        3D        5D
    Winners      +0.08%    +0.05%    +0.30%
    Losers       +0.32%    +0.34%    +0.84%
  ──────────────────────────────────────────────────────────────────
  Universe diagnostics (305 days):
    Avg stability score  : 0.299  (0=fully churning, 1=static)
    Avg daily turnover   : 57.9%
    Avg leader half-life : 1.8 days
    Stability vs PnL corr: +0.096  (>0 = stable universe → better trades)
    Turnover vs success  : -0.012  (<0 = higher churn → fewer successes)
  ──────────────────────────────────────────────────────────────────
  Per-regime breakdown (entry regime):
    Regime                           N  WinRate    AvgRet
    HIGH_VOL_SIDEWAYS               44    40.9%    -0.20%
    HIGH_VOL_UPTREND               369    39.3%    -0.25%
    LOW_VOL_SIDEWAYS               193    32.1%    -0.10%
    LOW_VOL_UPTREND                577    33.3%    -0.53%
    MID_VOL_SIDEWAYS                89    29.2%    -1.91%
    MID_VOL_UPTREND                458    37.6%    -0.06%
  ──────────────────────────────────────────────────────────────────
  ══════════════════════════════════════════════════════════════════

======================================================================













