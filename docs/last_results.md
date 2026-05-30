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
  --------------------------------------------------------------------  [Multi-strategy adaptive — LLM weights]
  Adaptive  (5-strat)      0.71     6.40%    9.80%    1.24  40.0%      538
                         (LLM calls: 52)

  --------------------------------------------------------------------  [Strategy PnL Attribution — Adaptive]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  Breakout          384        +7000     38.5%        +18   108.9%
  RSI-MR             55         +103     54.5%         +2     1.6%
  DualMA             15         -183     46.7%        -12    -2.8%
  QuietBrk           46         -192     32.6%         -4    -3.0%
  TrendPB            38         -300     39.5%         -8    -4.7%
  TOTAL             538        +6429
  --------------------------------------------------------------------  [Adaptive — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  pass_thru%
  DualMA           5256    1566       3689          1       18       29.5%
  Breakout         5272    4554        261        457      424       78.3%
  QuietBrk         1119     333        758         28       60       24.4%
  TrendPB          3277     290       1444       1543       56        7.1%
  RSI-MR           2310     322       1317        671      181        6.1%

  --------------------------------------------------------------------  [Adaptive — union-filter overlap (per trading day)]
  Filter                              total   max/day   mean/day
  BreakoutUniverseFilter                  0         0       0.00
  ActivityTailFilter                      0         0       0.00
  PullbackUniverseFilter                306         7       1.23
  MeanReversionUniverseFilter          1030        17       4.15
  DualMAUniverseFilter                  668        16       2.69
  --------------------------------------------------------------------  [Multi-strategy adaptive + RegimeContextAgent]
  Adaptive+RCA (5-strat)   0.44     3.73%   10.02%    1.14  37.5%      515
                         (LLM calls: 52)

  --------------------------------------------------------------------  [Strategy PnL Attribution — Adaptive+RCA]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  Breakout          388        +4860     37.9%        +13   129.1%
  RSI-MR             37          +35     40.5%         +1     0.9%
  QuietBrk           45         -233     33.3%         -5    -6.2%
  DualMA             13         -290     38.5%        -22    -7.7%
  TrendPB            32         -607     34.4%        -19   -16.1%
  TOTAL             515        +3765
  --------------------------------------------------------------------  [Adaptive+RCA — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  pass_thru%
  DualMA           4938    1543       3395          0       19       30.9%
  Breakout         5256    4576        256        424      430       78.9%
  QuietBrk         1055     323        706         26       55       25.4%
  TrendPB          2910     242       1249       1419       58        6.3%
  RSI-MR           1469     207        883        379      122        5.8%

  --------------------------------------------------------------------  [Adaptive+RCA — union-filter overlap (per trading day)]
  Filter                              total   max/day   mean/day
  BreakoutUniverseFilter                  0         0       0.00
  ActivityTailFilter                      0         0       0.00
  PullbackUniverseFilter                306         7       1.23
  MeanReversionUniverseFilter          1030        17       4.15
  DualMAUniverseFilter                  668        16       2.69
  RCA delta              -0.27    -2.66%

  ══════════════════════════════════════════════════════════════════
  OPPORTUNITY QUALITY SUMMARY  [Bear  2022]
  ══════════════════════════════════════════════════════════════════
  Trades analyzed  : 1762  (698 winners / 1064 losers)
  ──────────────────────────────────────────────────────────────────
  Breakout quality:
    Follow-through rate  :   46.8%   (price continued post-exit)
    False breakout rate  :   37.0%   (MFE>2% but final return <0)
    Persistence half-life:    0.0 days (median survival above entry)
    Avg MFE efficiency   : -0.298      (1.00 = exit at peak)
  ──────────────────────────────────────────────────────────────────
  Continuation decay (post-exit drift):
                      1D        3D        5D
    Winners      +0.06%    +0.19%    +0.21%
    Losers       -0.11%    -0.14%    -0.42%
  ──────────────────────────────────────────────────────────────────
  Universe diagnostics (248 days):
    Avg stability score  : 0.327  (0=fully churning, 1=static)
    Avg daily turnover   : 53.7%
    Avg leader half-life : 2.0 days
    Stability vs PnL corr: -0.101  (>0 = stable universe → better trades)
    Turnover vs success  : +0.022  (<0 = higher churn → fewer successes)
  ──────────────────────────────────────────────────────────────────
  Per-regime breakdown (entry regime):
    Regime                           N  WinRate    AvgRet
    HIGH_VOL_SIDEWAYS               59    39.0%    -1.10%
    HIGH_VOL_UPTREND               399    37.8%    -0.18%
    LOW_VOL_SIDEWAYS               219    51.1%     1.70%
    LOW_VOL_UPTREND                509    36.0%    -0.47%
    MID_VOL_SIDEWAYS               141    41.1%    -0.61%
    MID_VOL_UPTREND                435    39.3%     0.30%
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
  --------------------------------------------------------------------  [Multi-strategy adaptive — LLM weights]
  Adaptive  (5-strat)      1.57    43.53%    9.93%    1.50  45.3%     1549
                         (LLM calls: 126)

  --------------------------------------------------------------------  [Strategy PnL Attribution — Adaptive]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  Breakout         1057       +29249     41.7%        +28    78.0%
  QuietBrk          180        +6254     41.1%        +35    16.7%
  TrendPB            98         +782     54.1%         +8     2.1%
  DualMA             34         +713     50.0%        +21     1.9%
  RSI-MR            180         +479     64.4%         +3     1.3%
  TOTAL            1549       +37477
  --------------------------------------------------------------------  [Adaptive — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  pass_thru%
  DualMA          16201    3625      12567          9       47       22.1%
  Breakout        16105   14188        492       1425     1052       81.6%
  QuietBrk         4673    1313       3285         75      228       23.2%
  TrendPB         11733     725       5675       5333      106        5.3%
  RSI-MR          10196    1029       5904       3263      607        4.1%

  --------------------------------------------------------------------  [Adaptive — union-filter overlap (per trading day)]
  Filter                              total   max/day   mean/day
  BreakoutUniverseFilter                  0         0       0.00
  ActivityTailFilter                      0         0       0.00
  PullbackUniverseFilter                734         8       1.24
  MeanReversionUniverseFilter          2457        19       4.14
  DualMAUniverseFilter                 1376        16       2.32
  --------------------------------------------------------------------  [Multi-strategy adaptive + RegimeContextAgent]
  Adaptive+RCA (5-strat)   1.54    42.40%   10.02%    1.49  44.8%     1517
                         (LLM calls: 126)

  --------------------------------------------------------------------  [Strategy PnL Attribution — Adaptive+RCA]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  Breakout         1044       +28325     41.7%        +27    76.8%
  QuietBrk          182        +7277     41.8%        +40    19.7%
  DualMA             33         +592     45.5%        +18     1.6%
  RSI-MR            163         +445     63.2%         +3     1.2%
  TrendPB            95         +224     53.7%         +2     0.6%
  TOTAL            1517       +36864
  --------------------------------------------------------------------  [Adaptive+RCA — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  pass_thru%
  DualMA          15703    3627      12068          8       47       22.8%
  Breakout        16037   14160        447       1430     1074       81.6%
  QuietBrk         4641    1327       3242         72      224       23.8%
  TrendPB         11207     635       5456       5116      100        4.8%
  RSI-MR           9204     880       5206       3118      502        4.1%

  --------------------------------------------------------------------  [Adaptive+RCA — union-filter overlap (per trading day)]
  Filter                              total   max/day   mean/day
  BreakoutUniverseFilter                  0         0       0.00
  ActivityTailFilter                      0         0       0.00
  PullbackUniverseFilter                734         8       1.24
  MeanReversionUniverseFilter          2457        19       4.14
  DualMAUniverseFilter                 1376        16       2.32
  RCA delta              -0.04    -1.13%

  ══════════════════════════════════════════════════════════════════
  OPPORTUNITY QUALITY SUMMARY  [Recent2022–2024]
  ══════════════════════════════════════════════════════════════════
  Trades analyzed  : 5005  (2263 winners / 2742 losers)
  ──────────────────────────────────────────────────────────────────
  Breakout quality:
    Follow-through rate  :   54.4%   (price continued post-exit)
    False breakout rate  :   31.4%   (MFE>2% but final return <0)
    Persistence half-life:    0.0 days (median survival above entry)
    Avg MFE efficiency   : -0.216      (1.00 = exit at peak)
  ──────────────────────────────────────────────────────────────────
  Continuation decay (post-exit drift):
                      1D        3D        5D
    Winners      -0.01%    +0.38%    +0.80%
    Losers       +0.00%    +0.13%    +0.25%
  ──────────────────────────────────────────────────────────────────
  Universe diagnostics (594 days):
    Avg stability score  : 0.320  (0=fully churning, 1=static)
    Avg daily turnover   : 54.4%
    Avg leader half-life : 2.0 days
    Stability vs PnL corr: -0.054  (>0 = stable universe → better trades)
    Turnover vs success  : +0.006  (<0 = higher churn → fewer successes)
  ──────────────────────────────────────────────────────────────────
  Per-regime breakdown (entry regime):
    Regime                           N  WinRate    AvgRet
    HIGH_VOL_SIDEWAYS              248    52.0%     0.52%
    HIGH_VOL_UPTREND              2093    45.2%     0.65%
    LOW_VOL_SIDEWAYS               344    47.7%     1.29%
    LOW_VOL_UPTREND               1012    41.7%     0.39%
    MID_VOL_SIDEWAYS               265    48.7%     0.09%
    MID_VOL_UPTREND               1043    45.3%     1.35%
  ──────────────────────────────────────────────────────────────────



  ///////////////////////////////////////////////////////////////////////////
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


  Adaptive  (5-strat)     -0.19    -1.87%    5.85%    0.93  35.1%      539
                         (LLM calls: 66)

  --------------------------------------------------------------------  [Strategy PnL Attribution — Adaptive]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  QuietBrk           82        +2083     30.5%        +25  -115.6%
  RSI-MR             56          +69     50.0%         +1    -3.8%
  TrendPB            13          +38     61.5%         +3    -2.1%
  DualMA             12         -434     25.0%        -36    24.1%
  Breakout          376        -3559     33.2%         -9   197.5%
  TOTAL             539        -1802
  --------------------------------------------------------------------  [Adaptive — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  pass_thru%
  DualMA           5408    1393       4015          0       21       25.4%
  Breakout         5571    4783        255        533      483       77.2%
  QuietBrk         1926     622       1276         28      129       25.6%
  TrendPB          3452     208       1948       1296       26        5.3%
  RSI-MR           3087     380       1809        898      243        4.4%

  --------------------------------------------------------------------  [Adaptive — union-filter overlap (per trading day)]
  Filter                              total   max/day   mean/day
  BreakoutUniverseFilter                  0         0       0.00
  ActivityTailFilter                      0         0       0.00
  PullbackUniverseFilter                249         8       0.82
  MeanReversionUniverseFilter           993        18       3.26
  DualMAUniverseFilter                  565        11       1.85
  --------------------------------------------------------------------  [Multi-strategy adaptive + RegimeContextAgent]
  Adaptive+RCA (5-strat)  -0.18    -1.75%    5.65%    0.93  35.4%      540
                         (LLM calls: 66)

  --------------------------------------------------------------------  [Strategy PnL Attribution — Adaptive+RCA]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  QuietBrk           84        +1723     28.6%        +21  -102.6%
  TrendPB            13          +76     61.5%         +6    -4.5%
  RSI-MR             52          +61     50.0%         +1    -3.6%
  DualMA             11         -349     27.3%        -32    20.8%
  Breakout          380        -3190     34.2%         -8   189.9%
  TOTAL             540        -1679
  --------------------------------------------------------------------  [Adaptive+RCA — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  pass_thru%
  DualMA           5572    1514       4058          0       25       26.7%
  Breakout         5594    4725        346        523      467       76.1%
  QuietBrk         1921     623       1268         30      128       25.8%
  TrendPB          3625     250       2019       1356       26        6.2%
  RSI-MR           2436     332       1420        684      205        5.2%

  --------------------------------------------------------------------  [Adaptive+RCA — union-filter overlap (per trading day)]
  Filter                              total   max/day   mean/day
  BreakoutUniverseFilter                  0         0       0.00
  ActivityTailFilter                      0         0       0.00
  PullbackUniverseFilter                249         8       0.82
  MeanReversionUniverseFilter           993        18       3.26
  DualMAUniverseFilter                  565        11       1.85
  RCA delta              + 0.01  +   0.12%

  ══════════════════════════════════════════════════════════════════
  OPPORTUNITY QUALITY SUMMARY  [Live  2025–2026]
  ══════════════════════════════════════════════════════════════════
  Trades analyzed  : 1726  (619 winners / 1107 losers)
  ──────────────────────────────────────────────────────────────────
  Breakout quality:
    Follow-through rate  :   52.5%   (price continued post-exit)
    False breakout rate  :   28.0%   (MFE>2% but final return <0)
    Persistence half-life:    0.0 days (median survival above entry)
    Avg MFE efficiency   : -0.343      (1.00 = exit at peak)
  ──────────────────────────────────────────────────────────────────
  Continuation decay (post-exit drift):
                      1D        3D        5D
    Winners      +0.09%    +0.07%    +0.33%
    Losers       +0.33%    +0.34%    +0.80%
  ──────────────────────────────────────────────────────────────────
  Universe diagnostics (305 days):
    Avg stability score  : 0.299  (0=fully churning, 1=static)
    Avg daily turnover   : 57.9%
    Avg leader half-life : 1.8 days
    Stability vs PnL corr: +0.120  (>0 = stable universe → better trades)
    Turnover vs success  : -0.005  (<0 = higher churn → fewer successes)
  ──────────────────────────────────────────────────────────────────
  Per-regime breakdown (entry regime):
    Regime                           N  WinRate    AvgRet
    HIGH_VOL_SIDEWAYS               46    39.1%    -0.16%
    HIGH_VOL_UPTREND               369    41.2%    -0.01%
    LOW_VOL_SIDEWAYS               202    32.2%    -0.13%
    LOW_VOL_UPTREND                579    33.0%    -0.55%
    MID_VOL_SIDEWAYS                79    31.6%    -1.65%
    MID_VOL_UPTREND                451    37.3%    -0.11%
  ──────────────────────────────────────────────────────────────────
  ══════════════════════════════════════════════════════════════════

======================================================================
