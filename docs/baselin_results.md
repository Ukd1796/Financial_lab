======================================================================
  Period: Full  2018–2024   (2018-01-01 → 2024-06-01)
  Universe: 150 symbols → DynamicUniverse top 80 → UniverseSelection top 20
  Costs: 0.10% commission + 0.05% slippage per side (all returns net of costs)
======================================================================
  Strategy               Sharpe    Return    MaxDD      PF     WR  #Trades
  --------------------------------------------------------------------  [Medium-term]
  DualMA SMA20/50          0.84    66.75%   13.35%    1.45  43.4%      532
  --------------------------------------------------------------------  [Short-term]
  Breakout 10d             1.10   148.13%   24.83%    1.37  41.6%     2485
  QuietBrk 20d             1.19   168.83%   20.97%    1.52  42.1%     1605
  TrendPB v2 pct=3%        0.61    40.68%   21.42%    1.19  57.9%     1818
  TrendPB v2 pct=5%        0.81    39.33%   11.21%    1.34  58.6%      960
  --------------------------------------------------------------------  [Mean-reversion]
  RSI-MR  os=5  ob=80      0.24    13.74%   20.01%    1.05  54.7%     2545
  --------------------------------------------------------------------  [Multi-strategy baseline — equal weight]
  EqualWeight (5-strat)    1.13    76.87%   12.71%    1.34  46.6%     6554

  --------------------------------------------------------------------  [Strategy PnL Attribution — EqualWeight]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  Breakout         3777       +59561     40.6%        +16    82.0%
  TrendPB           553        +6695     57.3%        +12     9.2%
  DualMA            233        +5098     43.3%        +22     7.0%
  RSI-MR           1991        +1267     55.5%         +1     1.7%
  TOTAL            6554       +72622
  --------------------------------------------------------------------  [EqualWeight — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  pass_thru%
  DualMA          57277   45660      11563         54      138       79.5%
  Breakout        54165   12620      32197       9348     1893       19.8%
  QuietBrk        44686       0      39816       4870        0        0.0%
  TrendPB         48722    3918      22790      22014      327        7.4%
  RSI-MR          52209    5664      30946      15599     1204        8.5%

   Adaptive  (5-strat)      1.22   120.15%   20.62%    1.44  43.5%     4594
                         (LLM calls: 337)

  --------------------------------------------------------------------  [Strategy PnL Attribution — Adaptive]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  Breakout         3616      +107266     40.2%        +30    96.2%
  TrendPB           319        +2789     58.6%         +9     2.5%
  RSI-MR            527         +879     58.1%         +2     0.8%
  DualMA            132         +577     38.6%         +4     0.5%
  TOTAL            4594      +111511
  --------------------------------------------------------------------  [Adaptive — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  pass_thru%
  DualMA          52410   14866      37499         45      122       28.1%
  Breakout        45278   38821       2696       3761     2541       80.1%
  QuietBrk        36694     788      33775       2131        0        2.1%
  TrendPB         28394    1994      11825      14575      303        6.0%
  RSI-MR          25055    2527      14280       8248     1382        4.6%
  --------------------------------------------------------------------  [Multi-strategy adaptive + RegimeContextAgent]
  Adaptive+RCA (5-strat)   1.28   130.69%   23.20%    1.46  43.1%     4535
                         (LLM calls: 337)

  --------------------------------------------------------------------  [Strategy PnL Attribution — Adaptive+RCA]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  Breakout         3623      +116664     40.1%        +32    95.6%
  TrendPB           328        +4980     59.8%        +15     4.1%
  RSI-MR            458         +789     55.9%         +2     0.6%
  DualMA            126         -462     38.1%         -4    -0.4%
  TOTAL            4535      +121971
  --------------------------------------------------------------------  [Adaptive+RCA — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  pass_thru%
  DualMA          52488   14296      38147         45      118       27.0%
  Breakout        45685   39663       2229       3793     2518       81.3%
  QuietBrk        36522     847      33526       2149        0        2.3%
  TrendPB         29127    2130      11813      15184      306        6.3%
  RSI-MR          21648    2026      12426       7196     1069        4.4%
  RCA delta              + 0.06  +  10.54%

  ══════════════════════════════════════════════════════════════════
  OPPORTUNITY QUALITY SUMMARY  [Full  2018–2024]
  ══════════════════════════════════════════════════════════════════
  Trades analyzed  : 15683  (7007 winners / 8676 losers)
  ──────────────────────────────────────────────────────────────────
  Breakout quality:
    Follow-through rate  :   52.4%   (price continued post-exit)
    False breakout rate  :   33.9%   (MFE>2% but final return <0)
    Persistence half-life:    0.0 days (median survival above entry)
    Avg MFE efficiency   : -0.215      (1.00 = exit at peak)
  ──────────────────────────────────────────────────────────────────
  Continuation decay (post-exit drift):
                      1D        3D        5D
    Winners      -0.05%    +0.39%    +0.75%
    Losers       -0.08%    +0.11%    +0.26%
  ──────────────────────────────────────────────────────────────────
  Universe diagnostics (1581 days):
    Avg stability score  : 0.259  (0=fully churning, 1=static)
    Avg daily turnover   : 60.0%
    Avg leader half-life : 1.8 days
    Stability vs PnL corr: -0.030  (>0 = stable universe → better trades)
    Turnover vs success  : +0.004  (<0 = higher churn → fewer successes)
  ──────────────────────────────────────────────────────────────────
  Per-regime breakdown (entry regime):
    Regime                           N  WinRate    AvgRet
    HIGH_VOL_SIDEWAYS             1033    49.0%     0.01%
    HIGH_VOL_UPTREND              6614    45.1%     0.89%
    LOW_VOL_SIDEWAYS              1156    49.0%     1.44%
    LOW_VOL_UPTREND               2524    40.5%     0.43%
    MID_VOL_SIDEWAYS              1025    46.5%     0.33%
    MID_VOL_UPTREND               3331    43.7%     0.91%
  ──────────────────────────────────────────────────────────────────
  ══════════════════════════════════════════════════════════════════

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

======================================================================
  Period: Bull  2019–2020   (2019-01-01 → 2020-02-01)
  Universe: 150 symbols → DynamicUniverse top 80 → UniverseSelection top 20
  Costs: 0.10% commission + 0.05% slippage per side (all returns net of costs)
======================================================================
  Strategy               Sharpe    Return    MaxDD      PF     WR  #Trades
  --------------------------------------------------------------------  [Medium-term]
  DualMA SMA20/50         -0.11    -1.55%    8.53%    0.63  27.6%       87
  --------------------------------------------------------------------  [Short-term]
  Breakout 10d             0.14     1.09%    9.82%    0.99  39.4%      378
  QuietBrk 20d             0.25     2.37%   12.32%    0.92  34.1%      252
  TrendPB v2 pct=3%        0.33     2.27%    5.02%    1.12  54.2%      251
  TrendPB v2 pct=5%        0.90     4.51%    2.85%    1.43  57.3%      124
  --------------------------------------------------------------------  [Mean-reversion]
  RSI-MR  os=5  ob=80      0.23     1.79%   10.55%    1.05  55.1%      412
  --------------------------------------------------------------------  [Multi-strategy baseline — equal weight]
  EqualWeight (5-strat)   -0.63    -4.50%    9.21%    0.84  42.8%     1150

  --------------------------------------------------------------------  [Strategy PnL Attribution — EqualWeight]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  TrendPB            81         +710     55.6%         +9   -13.7%
  RSI-MR            423         -857     52.0%         -2    16.5%
  DualMA             37        -1696     16.2%        -46    32.6%
  Breakout          609        -3353     36.3%         -6    64.5%
  TOTAL            1150        -5195
  --------------------------------------------------------------------  [EqualWeight — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  pass_thru%
  DualMA           8622    6882       1732          8       17       79.6%
  Breakout         8425    1988       4630       1807      162       21.7%
  QuietBrk         6546       0       5651        895        0        0.0%
  TrendPB          7673     806       3764       3103       29       10.1%
  RSI-MR           8350    1107       5051       2192      134       11.7%
  --------------------------------------------------------------------  

  Adaptive  (5-strat)     -0.36    -4.13%   10.57%    0.82  39.2%      716
                         (LLM calls: 58)

  --------------------------------------------------------------------  [Strategy PnL Attribution — Adaptive]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  RSI-MR            104          +71     51.9%         +1    -1.1%
  TrendPB            33          +17     54.5%         +1    -0.3%
  DualMA             28        -1708     25.0%        -61    26.2%
  Breakout          551        -4898     36.7%         -9    75.1%
  TOTAL             716        -6518
  --------------------------------------------------------------------  [Adaptive — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  pass_thru%
  DualMA           7722    2800       4916          6       14       36.1%
  Breakout         6804    5351        696        757      278       74.6%
  QuietBrk         4880     120       4398        362        0        2.5%
  TrendPB          2834     308       1257       1269       14       10.4%
  RSI-MR           2022     335       1203        484       97       11.8%
  --------------------------------------------------------------------  [Multi-strategy adaptive + RegimeContextAgent]
  Adaptive+RCA (5-strat)  -0.50    -5.40%   11.69%    0.80  38.0%      693
                         (LLM calls: 58)

  --------------------------------------------------------------------  [Strategy PnL Attribution — Adaptive+RCA]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  RSI-MR             80          -42     50.0%         -1     0.6%
  TrendPB            32         -146     56.2%         -5     2.0%
  DualMA             25        -1701     24.0%        -68    23.1%
  Breakout          556        -5480     35.8%        -10    74.4%
  TOTAL             693        -7368
  --------------------------------------------------------------------  [Adaptive+RCA — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  pass_thru%
  DualMA           7713    2834       4873          6       16       36.5%
  Breakout         6634    5288        701        645      283       75.4%
  QuietBrk         4906     120       4456        330        0        2.4%
  TrendPB          2644     287       1164       1193       14       10.3%
  RSI-MR           1509     248        896        365       72       11.7%
  RCA delta              -0.14    -1.27%

  ══════════════════════════════════════════════════════════════════
  OPPORTUNITY QUALITY SUMMARY  [Bull  2019–2020]
  ══════════════════════════════════════════════════════════════════
  Trades analyzed  : 2559  (1036 winners / 1523 losers)
  ──────────────────────────────────────────────────────────────────
  Breakout quality:
    Follow-through rate  :   48.6%   (price continued post-exit)
    False breakout rate  :   36.3%   (MFE>2% but final return <0)
    Persistence half-life:    0.0 days (median survival above entry)
    Avg MFE efficiency   : -0.274      (1.00 = exit at peak)
  ──────────────────────────────────────────────────────────────────
  Continuation decay (post-exit drift):
                      1D        3D        5D
    Winners      -0.03%    +0.23%    +0.40%
    Losers       -0.10%    -0.15%    -0.07%
  ──────────────────────────────────────────────────────────────────
  Universe diagnostics (265 days):
    Avg stability score  : 0.258  (0=fully churning, 1=static)
    Avg daily turnover   : 59.8%
    Avg leader half-life : 1.7 days
    Stability vs PnL corr: -0.009  (>0 = stable universe → better trades)
    Turnover vs success  : +0.054  (<0 = higher churn → fewer successes)
  ──────────────────────────────────────────────────────────────────
  Per-regime breakdown (entry regime):
    Regime                           N  WinRate    AvgRet
    HIGH_VOL_SIDEWAYS              148    39.2%    -0.26%
    HIGH_VOL_UPTREND               688    47.1%     0.61%
    LOW_VOL_SIDEWAYS               295    46.1%    -0.21%
    LOW_VOL_UPTREND                618    31.9%    -0.91%
    MID_VOL_SIDEWAYS               169    46.2%    -1.24%
    MID_VOL_UPTREND                641    37.9%    -0.58%
  ──────────────────────────────────────────────────────────────────
  ══════════════════════════════════════════════════════════════════

  //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

  ======================================================================
  Period: Crash 2020        (2020-01-01 → 2020-12-31)
  Universe: 150 symbols → DynamicUniverse top 80 → UniverseSelection top 20
  Costs: 0.10% commission + 0.05% slippage per side (all returns net of costs)
======================================================================
  Strategy               Sharpe    Return    MaxDD      PF     WR  #Trades
  --------------------------------------------------------------------  [Medium-term]
  DualMA SMA20/50          1.86    27.40%    8.61%    2.50  51.6%       95
  --------------------------------------------------------------------  [Short-term]
  Breakout 10d             2.18    37.36%    6.96%    1.70  44.6%      424
  QuietBrk 20d             2.01    32.41%    9.40%    1.75  40.7%      263
  TrendPB v2 pct=3%        1.85    22.33%    5.66%    1.64  61.7%      426
  TrendPB v2 pct=5%        1.85    16.83%    5.42%    1.78  62.8%      253
  --------------------------------------------------------------------  [Mean-reversion]
  RSI-MR  os=5  ob=80      1.01    12.95%   10.23%    1.29  60.8%      429
  --------------------------------------------------------------------  [Multi-strategy baseline — equal weight]
  EqualWeight (5-strat)    2.34    26.34%    5.70%    1.82  51.6%     1096

  --------------------------------------------------------------------  [Strategy PnL Attribution — EqualWeight]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  Breakout          622       +18253     43.1%        +29    76.3%
  RSI-MR            306        +3310     67.3%        +11    13.8%
  TrendPB           138        +1619     57.2%        +12     6.8%
  DualMA             30         +744     43.3%        +25     3.1%
  TOTAL            1096       +23926
  --------------------------------------------------------------------  [EqualWeight — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  pass_thru%
  DualMA           9965    7908       2046         11       28       79.1%
  Breakout         9107    1942       5641       1524      313       17.9%
  QuietBrk         7803       0       6952        851        0        0.0%
  TrendPB          8322     743       3156       4423       85        7.9%
  RSI-MR           8730     798       5186       2746      130        7.7%
  --------------------------------------------------------------------  [Multi-strategy adaptive — LLM weights]

   Adaptive  (5-strat)      2.49    35.51%    7.75%    1.89  48.1%      884
                         (LLM calls: 54)

  --------------------------------------------------------------------  [Strategy PnL Attribution — Adaptive]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  Breakout          608       +30766     42.3%        +51    93.3%
  TrendPB           113        +1389     61.1%        +12     4.2%
  DualMA             20         +652     50.0%        +33     2.0%
  RSI-MR            143         +151     62.2%         +1     0.5%
  TOTAL             884       +32958
  --------------------------------------------------------------------  [Adaptive — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  pass_thru%
  DualMA           9566    2471       7087          8       24       25.6%
  Breakout         8346    6853        461       1032      374       77.6%
  QuietBrk         7176     220       6377        579        0        3.1%
  TrendPB          7154     574       2495       4085      109        6.5%
  RSI-MR           6944     580       4009       2355      267        4.5%
  --------------------------------------------------------------------  [Multi-strategy adaptive + RegimeContextAgent]
  Adaptive+RCA (5-strat)   2.48    35.74%    7.89%    1.90  46.3%      848
                         (LLM calls: 54)

  --------------------------------------------------------------------  [Strategy PnL Attribution — Adaptive+RCA]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  Breakout          610       +30773     41.6%        +50    92.5%
  TrendPB           114        +1738     58.8%        +15     5.2%
  DualMA             16         +602     50.0%        +38     1.8%
  RSI-MR            108         +152     59.3%         +1     0.5%
  TOTAL             848       +33264
  --------------------------------------------------------------------  [Adaptive+RCA — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  pass_thru%
  DualMA           9465    2165       7294          6       21       22.7%
  Breakout         8183    7123        118        942      365       82.6%
  QuietBrk         6867     204       6109        554        0        3.0%
  TrendPB          7258     581       2460       4217      108        6.5%
  RSI-MR           5412     435       3044       1933      199        4.4%
  RCA delta              -0.01  +   0.23%

  ══════════════════════════════════════════════════════════════════
  OPPORTUNITY QUALITY SUMMARY  [Crash 2020]
  ══════════════════════════════════════════════════════════════════
  Trades analyzed  : 2828  (1384 winners / 1444 losers)
  ──────────────────────────────────────────────────────────────────
  Breakout quality:
    Follow-through rate  :   58.0%   (price continued post-exit)
    False breakout rate  :   35.9%   (MFE>2% but final return <0)
    Persistence half-life:    0.0 days (median survival above entry)
    Avg MFE efficiency   : -0.144      (1.00 = exit at peak)
  ──────────────────────────────────────────────────────────────────
  Continuation decay (post-exit drift):
                      1D        3D        5D
    Winners      +0.15%    +0.91%    +1.32%
    Losers       -0.01%    +0.67%    +1.07%
  ──────────────────────────────────────────────────────────────────
  Universe diagnostics (250 days):
    Avg stability score  : 0.282  (0=fully churning, 1=static)
    Avg daily turnover   : 58.4%
    Avg leader half-life : 1.8 days
    Stability vs PnL corr: +0.052  (>0 = stable universe → better trades)
    Turnover vs success  : +0.062  (<0 = higher churn → fewer successes)
  ──────────────────────────────────────────────────────────────────
  Per-regime breakdown (entry regime):
    Regime                           N  WinRate    AvgRet
    HIGH_VOL_SIDEWAYS              115    50.4%    -0.66%
    HIGH_VOL_UPTREND              1001    42.4%     0.99%
    LOW_VOL_SIDEWAYS               281    63.3%     4.41%
    LOW_VOL_UPTREND                612    47.2%     1.28%
    MID_VOL_SIDEWAYS               138    69.6%     2.84%
    MID_VOL_UPTREND                681    49.8%     2.10%
  ──────────────────────────────────────────────────────────────────

  /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

  ======================================================================
  Period: Recov 2020–2021   (2020-04-01 → 2021-12-31)
  Universe: 150 symbols → DynamicUniverse top 80 → UniverseSelection top 20
  Costs: 0.10% commission + 0.05% slippage per side (all returns net of costs)
======================================================================
  Strategy               Sharpe    Return    MaxDD      PF     WR  #Trades
  --------------------------------------------------------------------  [Medium-term]
  DualMA SMA20/50          2.05    58.40%    8.66%    2.63  54.9%      175
  --------------------------------------------------------------------  [Short-term]
  Breakout 10d             3.29   149.57%   10.74%    2.11  46.5%      805
  QuietBrk 20d             2.45    94.49%   11.26%    1.97  44.4%      529
  TrendPB v2 pct=3%        1.27    29.83%   10.11%    1.36  59.7%      785
  TrendPB v2 pct=5%        1.29    23.35%    7.36%    1.49  60.7%      461
  --------------------------------------------------------------------  [Mean-reversion]
  RSI-MR  os=5  ob=80      1.26    29.75%    7.40%    1.32  57.9%      874
  --------------------------------------------------------------------  [Multi-strategy baseline — equal weight]
  EqualWeight (5-strat)    2.80    64.61%    8.02%    1.91  51.0%     2233

  --------------------------------------------------------------------  [Strategy PnL Attribution — EqualWeight]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  Breakout         1268       +48299     45.0%        +38    76.5%
  RSI-MR            639        +7764     60.1%        +12    12.3%
  DualMA             59        +4065     49.2%        +69     6.4%
  TrendPB           267        +2981     58.4%        +11     4.7%
  TOTAL            2233       +63109
  --------------------------------------------------------------------  [EqualWeight — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  pass_thru%
  DualMA          20043   16002       4012         29       37       79.7%
  Breakout        18770    3901      11572       3297      511       18.1%
  QuietBrk        16010       0      14174       1836        0        0.0%
  TrendPB         17215    1444       6980       8791      137        7.6%
  RSI-MR          18040    1619      10820       5601      227        7.7%
  --------------------------------------------------------------------  [Multi-strategy adaptive — LLM weights]

  //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

  Adaptive  (5-strat)      2.88    90.03%   10.26%    1.96  49.5%     1812
                         (LLM calls: 93)

  --------------------------------------------------------------------  [Strategy PnL Attribution — Adaptive]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  Breakout         1255       +83189     44.8%        +66    94.8%
  TrendPB           227        +2214     60.8%        +10     2.5%
  RSI-MR            299        +1254     61.5%         +4     1.4%
  DualMA             31        +1080     41.9%        +35     1.2%
  TOTAL            1812       +87737
  --------------------------------------------------------------------  [Adaptive — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  pass_thru%
  DualMA          19070    4850      14199         21       27       25.3%
  Breakout        16981   13793       1112       2076      616       77.6%
  QuietBrk        14732     432      13083       1217        0        2.9%
  TrendPB         15391    1102       5695       8594      188        5.9%
  RSI-MR          14260    1221       8325       4714      585        4.5%
  --------------------------------------------------------------------  [Multi-strategy adaptive + RegimeContextAgent]
  Adaptive+RCA (5-strat)   2.73    84.97%    9.84%    1.89  48.2%     1715
                         (LLM calls: 93)

  --------------------------------------------------------------------  [Strategy PnL Attribution — Adaptive+RCA]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  Breakout         1273       +76898     43.8%        +60    94.2%
  TrendPB           217        +2914     61.3%        +13     3.6%
  RSI-MR            198        +1454     62.6%         +7     1.8%
  DualMA             27         +332     44.4%        +12     0.4%
  TOTAL            1715       +81599
  --------------------------------------------------------------------  [Adaptive+RCA — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  pass_thru%
  DualMA          18708    4030      14656         22       29       21.4%
  Breakout        16491   14548        247       1696      618       84.5%
  QuietBrk        14308     385      12929        994        0        2.7%
  TrendPB         14859    1072       5276       8511      198        5.9%
  RSI-MR          10260     845       5835       3580      418        4.2%
  RCA delta              -0.15    -5.06%

  ══════════════════════════════════════════════════════════════════
  OPPORTUNITY QUALITY SUMMARY  [Recov 2020–2021]
  ══════════════════════════════════════════════════════════════════
  Trades analyzed  : 5760  (2862 winners / 2898 losers)
  ──────────────────────────────────────────────────────────────────
  Breakout quality:
    Follow-through rate  :   55.1%   (price continued post-exit)
    False breakout rate  :   34.5%   (MFE>2% but final return <0)
    Persistence half-life:    0.0 days (median survival above entry)
    Avg MFE efficiency   : -0.128      (1.00 = exit at peak)
  ──────────────────────────────────────────────────────────────────
  Continuation decay (post-exit drift):
                      1D        3D        5D
    Winners      -0.04%    +0.75%    +1.24%
    Losers       -0.10%    +0.43%    +0.85%
  ──────────────────────────────────────────────────────────────────
  Universe diagnostics (435 days):
    Avg stability score  : 0.276  (0=fully churning, 1=static)
    Avg daily turnover   : 59.1%
    Avg leader half-life : 1.8 days
    Stability vs PnL corr: -0.016  (>0 = stable universe → better trades)
    Turnover vs success  : -0.015  (<0 = higher churn → fewer successes)
  ──────────────────────────────────────────────────────────────────
  Per-regime breakdown (entry regime):
    Regime                           N  WinRate    AvgRet
    HIGH_VOL_SIDEWAYS              347    55.3%     0.89%
    HIGH_VOL_UPTREND              2720    46.5%     1.58%
    LOW_VOL_SIDEWAYS               323    63.2%     4.99%
    LOW_VOL_UPTREND                734    47.5%     1.38%
    MID_VOL_SIDEWAYS               356    57.3%     2.74%
    MID_VOL_UPTREND               1280    50.7%     2.15%
  ──────────────────────────────────────────────────────────────────

  ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

  ======================================================================
  Period: Bear  2022        (2022-01-01 → 2022-12-31)
  Universe: 150 symbols → DynamicUniverse top 80 → UniverseSelection top 20
  Costs: 0.10% commission + 0.05% slippage per side (all returns net of costs)
======================================================================
  Strategy               Sharpe    Return    MaxDD      PF     WR  #Trades
  --------------------------------------------------------------------  [Medium-term]
  DualMA SMA20/50         -0.24    -2.68%   10.83%    0.86  38.5%       78
  --------------------------------------------------------------------  [Short-term]
  Breakout 10d             0.42     4.57%   12.88%    1.11  39.0%      344
  QuietBrk 20d             0.15     0.97%   14.58%    1.03  35.4%      223
  TrendPB v2 pct=3%       -1.11   -10.68%   11.77%    0.71  52.3%      241
  TrendPB v2 pct=5%       -0.40    -2.48%    5.86%    0.87  50.0%      116
  --------------------------------------------------------------------  [Mean-reversion]
  RSI-MR  os=5  ob=80     -0.88   -11.28%   15.15%    0.74  48.0%      342
  --------------------------------------------------------------------  [Multi-strategy baseline — equal weight]
  EqualWeight (5-strat)    0.14     0.71%    7.41%    1.03  42.8%      788

  --------------------------------------------------------------------  [Strategy PnL Attribution — EqualWeight]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  Breakout          464        +2629     40.1%         +6   378.0%
  DualMA             39         +228     43.6%         +6    32.8%
  TrendPB            57          -28     50.9%         -0    -4.0%
  RSI-MR            228        -2133     46.1%         -9  -306.8%
  TOTAL             788         +695
  --------------------------------------------------------------------  [EqualWeight — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  pass_thru%
  DualMA           7247    5658       1583          6       33       77.6%
  Breakout         6769    1958       3738       1073      446       22.3%
  QuietBrk         5318       0       4798        520        0        0.0%
  TrendPB          5887     481       2779       2627       81        6.8%
  RSI-MR           6519     864       3727       1928      334        8.1%
  --------------------------------------------------------------------  [Multi-strategy adaptive — LLM weights]
  Adaptive  (5-strat)      0.71     6.45%    9.96%    1.23  41.3%      600
                         (LLM calls: 52)

  --------------------------------------------------------------------  [Strategy PnL Attribution — Adaptive]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  Breakout          465        +7369     38.9%        +16   113.9%
  RSI-MR             78          +26     52.6%         +0     0.4%
  TrendPB            36         -380     50.0%        -11    -5.9%
  DualMA             21         -544     38.1%        -26    -8.4%
  TOTAL             600        +6471
  --------------------------------------------------------------------  [Adaptive — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  pass_thru%
  DualMA           6744    1718       5020          6       28       25.1%
  Breakout         5914    5361         39        514      507       82.1%
  QuietBrk         3763      94       3442        227        0        2.5%
  TrendPB          4558     304       1909       2345       82        4.9%
  RSI-MR           4025     502       2265       1258      335        4.1%
  --------------------------------------------------------------------  [Multi-strategy adaptive + RegimeContextAgent]
  Adaptive+RCA (5-strat)   0.62     5.70%   10.30%    1.20  40.0%      567
                         (LLM calls: 52)

  --------------------------------------------------------------------  [Strategy PnL Attribution — Adaptive+RCA]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  Breakout          463        +6874     38.9%        +15   120.3%
  RSI-MR             50          -22     54.0%         -0    -0.4%
  TrendPB            33         -561     36.4%        -17    -9.8%
  DualMA             21         -574     38.1%        -27   -10.0%
  TOTAL             567        +5716
  --------------------------------------------------------------------  [Adaptive+RCA — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  pass_thru%
  DualMA           6759    1844       4910          5       27       26.9%
  Breakout         5909    5396         36        477      511       82.7%
  QuietBrk         3728      80       3414        234        0        2.1%
  TrendPB          4197     288       1751       2158       73        5.1%
  RSI-MR           2562     301       1470        791      201        3.9%
  RCA delta              -0.09    -0.75%

  ══════════════════════════════════════════════════════════════════
  OPPORTUNITY QUALITY SUMMARY  [Bear  2022]
  ══════════════════════════════════════════════════════════════════
  Trades analyzed  : 1955  (812 winners / 1143 losers)
  ──────────────────────────────────────────────────────────────────
  Breakout quality:
    Follow-through rate  :   46.3%   (price continued post-exit)
    False breakout rate  :   35.2%   (MFE>2% but final return <0)
    Persistence half-life:    0.0 days (median survival above entry)
    Avg MFE efficiency   : -0.271      (1.00 = exit at peak)
  ──────────────────────────────────────────────────────────────────
  Continuation decay (post-exit drift):
                      1D        3D        5D
    Winners      -0.03%    +0.05%    +0.14%
    Losers       -0.03%    -0.13%    -0.51%
  ──────────────────────────────────────────────────────────────────
  Universe diagnostics (248 days):
    Avg stability score  : 0.261  (0=fully churning, 1=static)
    Avg daily turnover   : 59.3%
    Avg leader half-life : 1.8 days
    Stability vs PnL corr: -0.135  (>0 = stable universe → better trades)
    Turnover vs success  : -0.054  (<0 = higher churn → fewer successes)
  ──────────────────────────────────────────────────────────────────
  Per-regime breakdown (entry regime):
    Regime                           N  WinRate    AvgRet
    HIGH_VOL_SIDEWAYS               70    32.9%    -1.30%
    HIGH_VOL_UPTREND               444    39.9%    -0.19%
    LOW_VOL_SIDEWAYS               290    53.8%     1.68%
    LOW_VOL_UPTREND                515    38.1%    -0.33%
    MID_VOL_SIDEWAYS               158    42.4%    -0.38%
    MID_VOL_UPTREND                478    40.4%     0.14%
  ──────────────────────────────────────────────────────────────────

  //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


  ======================================================================
  Period: Recent2022–2024   (2022-01-01 → 2024-06-01)
  Universe: 150 symbols → DynamicUniverse top 80 → UniverseSelection top 20
  Costs: 0.10% commission + 0.05% slippage per side (all returns net of costs)
======================================================================
  Strategy               Sharpe    Return    MaxDD      PF     WR  #Trades
  --------------------------------------------------------------------  [Medium-term]
  DualMA SMA20/50          0.51    10.89%   11.89%    1.17  42.1%      202
  --------------------------------------------------------------------  [Short-term]
  Breakout 10d             1.02    35.21%   12.88%    1.31  42.3%      877
  QuietBrk 20d             1.20    45.07%   17.79%    1.47  40.1%      564
  TrendPB v2 pct=3%        0.38     7.02%   14.83%    1.12  58.1%      566
  TrendPB v2 pct=5%        0.87    11.19%    7.31%    1.40  59.8%      266
  --------------------------------------------------------------------  [Mean-reversion]
  RSI-MR  os=5  ob=80     -0.03    -2.46%   17.23%    0.98  53.5%      912
  --------------------------------------------------------------------  [Multi-strategy baseline — equal weight]
  EqualWeight (5-strat)    1.08    21.34%    7.41%    1.30  45.9%     2179

  --------------------------------------------------------------------  [Strategy PnL Attribution — EqualWeight]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  Breakout         1326       +18107     41.6%        +14    95.2%
  TrendPB           147        +1558     58.5%        +11     8.2%
  DualMA             88        +1531     44.3%        +17     8.0%
  RSI-MR            618        -2166     52.4%         -4   -11.4%
  TOTAL            2179       +19030
  --------------------------------------------------------------------  [EqualWeight — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  pass_thru%
  DualMA          21417   16909       4495         13       90       78.5%
  Breakout        19567    4892      11853       2822     1118       19.3%
  QuietBrk        16370       0      14937       1433        0        0.0%
  TrendPB         17122    1130       8723       7269      131        5.8%
  RSI-MR          18584    2103      10656       5825      707        7.5%
  --------------------------------------------------------------------  [Multi-strategy adaptive — LLM weights]

   Adaptive  (5-strat)      1.51    42.05%    9.71%    1.47  45.0%     1733
                         (LLM calls: 126)

  --------------------------------------------------------------------  [Strategy PnL Attribution — Adaptive]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  Breakout         1330       +36178     40.8%        +27    97.1%
  TrendPB           110         +552     60.9%         +5     1.5%
  DualMA             44         +381     43.2%         +9     1.0%
  RSI-MR            249         +150     60.2%         +1     0.4%
  TOTAL            1733       +37261
  --------------------------------------------------------------------  [Adaptive — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  pass_thru%
  DualMA          20055    4642      15398         15       68       22.8%
  Breakout        17337   15619        294       1424     1246       82.9%
  QuietBrk        13830     293      12762        775        0        2.1%
  TrendPB         14209     714       6508       6987      145        4.0%
  RSI-MR          13849    1466       7657       4726      929        3.9%
  --------------------------------------------------------------------  [Multi-strategy adaptive + RegimeContextAgent]
  Adaptive+RCA (5-strat)   1.59    44.47%    9.84%    1.49  44.5%     1698
                         (LLM calls: 126)

  --------------------------------------------------------------------  [Strategy PnL Attribution — Adaptive+RCA]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  Breakout         1318       +37587     40.4%        +29    96.3%
  TrendPB           114         +667     59.6%         +6     1.7%
  DualMA             46         +632     43.5%        +14     1.6%
  RSI-MR            220         +132     61.8%         +1     0.3%
  TOTAL            1698       +39018
  --------------------------------------------------------------------  [Adaptive+RCA — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  pass_thru%
  DualMA          20029    4718      15297         14       72       23.2%
  Breakout        17291   15448        477       1366     1257       82.1%
  QuietBrk        13754     291      12707        756        0        2.1%
  TrendPB         14363     913       6439       7011      143        5.4%
  RSI-MR          12123    1292       6752       4079      824        3.9%
  RCA delta              + 0.07  +   2.43%

  ══════════════════════════════════════════════════════════════════
  OPPORTUNITY QUALITY SUMMARY  [Recent2022–2024]
  ══════════════════════════════════════════════════════════════════
  Trades analyzed  : 5610  (2536 winners / 3074 losers)
  ──────────────────────────────────────────────────────────────────
  Breakout quality:
    Follow-through rate  :   54.0%   (price continued post-exit)
    False breakout rate  :   30.7%   (MFE>2% but final return <0)
    Persistence half-life:    0.0 days (median survival above entry)
    Avg MFE efficiency   : -0.210      (1.00 = exit at peak)
  ──────────────────────────────────────────────────────────────────
  Continuation decay (post-exit drift):
                      1D        3D        5D
    Winners      -0.03%    +0.33%    +0.76%
    Losers       +0.01%    +0.14%    +0.26%
  ──────────────────────────────────────────────────────────────────
  Universe diagnostics (594 days):
    Avg stability score  : 0.252  (0=fully churning, 1=static)
    Avg daily turnover   : 60.3%
    Avg leader half-life : 1.7 days
    Stability vs PnL corr: -0.086  (>0 = stable universe → better trades)
    Turnover vs success  : +0.004  (<0 = higher churn → fewer successes)
  ──────────────────────────────────────────────────────────────────
  Per-regime breakdown (entry regime):
    Regime                           N  WinRate    AvgRet
    HIGH_VOL_SIDEWAYS              316    48.4%     0.05%
    HIGH_VOL_UPTREND              2310    45.3%     0.62%
    LOW_VOL_SIDEWAYS               453    51.2%     1.28%
    LOW_VOL_UPTREND               1054    41.4%     0.36%
    MID_VOL_SIDEWAYS               317    47.0%     0.43%
    MID_VOL_UPTREND               1160    44.7%     0.99%
  ──────────────────────────────────────────────────────────────────
  ══════════════════════════════════════════════════════════════════


  ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

======================================================================
  Period: Live  2025–2026   (2025-01-01 → 2026-03-24)
  Universe: 150 symbols → DynamicUniverse top 80 → UniverseSelection top 20
  Costs: 0.10% commission + 0.05% slippage per side (all returns net of costs)
======================================================================
  Strategy               Sharpe    Return    MaxDD      PF     WR  #Trades
  --------------------------------------------------------------------  [Medium-term]
  DualMA SMA20/50         -0.05    -1.11%    8.32%    0.96  33.0%      103
  --------------------------------------------------------------------  [Short-term]
  Breakout 10d            -0.65   -10.14%   11.77%    0.81  37.1%      399
  QuietBrk 20d            -0.40    -7.26%    8.40%    0.81  37.7%      260
  TrendPB v2 pct=3%        0.24     1.54%    3.84%    1.10  53.3%      135
  TrendPB v2 pct=5%        0.96     3.66%    1.97%    1.74  56.6%       53
  --------------------------------------------------------------------  [Mean-reversion]
  RSI-MR  os=5  ob=80      0.16     1.27%    5.52%    1.03  52.7%      351
  --------------------------------------------------------------------  [Multi-strategy baseline — equal weight]
  EqualWeight (5-strat)   -0.50    -3.00%    4.69%    0.86  39.3%      774

  --------------------------------------------------------------------  [Strategy PnL Attribution — EqualWeight]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  TrendPB            30         +422     60.0%        +14   -14.1%
  RSI-MR            227         -435     51.5%         -2    14.5%
  DualMA             21         -790     19.0%        -38    26.4%
  Breakout          496        -2192     33.3%         -4    73.2%
  TOTAL             774        -2995
  --------------------------------------------------------------------  [EqualWeight — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  pass_thru%
  DualMA           7408    5625       1781          2       55       75.2%
  Breakout         6533    2026       3656        851      569       22.3%
  QuietBrk         5222       0       4753        469        0        0.0%
  TrendPB          5392     316       3151       1925       30        5.3%
  RSI-MR           6071     887       3493       1691      375        8.4%
  --------------------------------------------------------------------  [Multi-strategy adaptive — LLM weights]
  Adaptive  (5-strat)     -0.58    -5.84%    9.19%    0.82  35.1%      573
                         (LLM calls: 66)

  --------------------------------------------------------------------  [Strategy PnL Attribution — Adaptive]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  QuietBrk           15         +509     46.7%        +34    -8.9%
  TrendPB            16         +151     68.8%         +9    -2.6%
  RSI-MR             60          -96     55.0%         -2     1.7%
  DualMA             11         -241     27.3%        -22     4.2%
  Breakout          471        -6056     31.2%        -13   105.6%
  TOTAL             573        -5733
  --------------------------------------------------------------------  [Adaptive — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  pass_thru%
  DualMA           5931    1639       4289          3       31       27.1%
  Breakout         6037    5398        178        461      615       79.2%
  QuietBrk         4284     225       3817        242       12        5.0%
  TrendPB          3084     211       1555       1318       29        5.9%
  RSI-MR           2471     373       1414        684      248        5.1%
  --------------------------------------------------------------------  [Multi-strategy adaptive + RegimeContextAgent]
  Adaptive+RCA (5-strat)  -0.56    -5.86%    9.22%    0.82  35.9%      569
                         (LLM calls: 66)

  --------------------------------------------------------------------  [Strategy PnL Attribution — Adaptive+RCA]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  QuietBrk           17         +615     47.1%        +36   -10.5%
  TrendPB            16         +588     75.0%        +37   -10.0%
  DualMA             11          +24     45.5%         +2    -0.4%
  RSI-MR             40           -8     60.0%         -0     0.1%
  Breakout          485        -7078     32.0%        -15   120.8%
  TOTAL             569        -5858
  --------------------------------------------------------------------  [Adaptive+RCA — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  pass_thru%
  DualMA           6775    2052       4716          7       35       29.8%
  Breakout         6286    5406        433        447      564       77.0%
  QuietBrk         4840     333       4286        221       12        6.6%
  TrendPB          2357     151       1160       1046       22        5.5%
  RSI-MR           1432     219        811        402      141        5.4%
  RCA delta              + 0.02    -0.02%

  ══════════════════════════════════════════════════════════════════
  OPPORTUNITY QUALITY SUMMARY  [Live  2025–2026]
  ══════════════════════════════════════════════════════════════════
  Trades analyzed  : 1916  (709 winners / 1207 losers)
  ──────────────────────────────────────────────────────────────────
  Breakout quality:
    Follow-through rate  :   52.9%   (price continued post-exit)
    False breakout rate  :   27.4%   (MFE>2% but final return <0)
    Persistence half-life:    0.0 days (median survival above entry)
    Avg MFE efficiency   : -0.318      (1.00 = exit at peak)
  ──────────────────────────────────────────────────────────────────
  Continuation decay (post-exit drift):
                      1D        3D        5D
    Winners      +0.16%    +0.21%    +0.45%
    Losers       +0.37%    +0.34%    +0.64%
  ──────────────────────────────────────────────────────────────────
  Universe diagnostics (305 days):
    Avg stability score  : 0.226  (0=fully churning, 1=static)
    Avg daily turnover   : 64.3%
    Avg leader half-life : 1.6 days
    Stability vs PnL corr: +0.064  (>0 = stable universe → better trades)
    Turnover vs success  : -0.027  (<0 = higher churn → fewer successes)
  ──────────────────────────────────────────────────────────────────
  Per-regime breakdown (entry regime):
    Regime                           N  WinRate    AvgRet
    HIGH_VOL_SIDEWAYS               53    43.4%    -0.69%
    HIGH_VOL_UPTREND               417    37.6%    -0.12%
    LOW_VOL_SIDEWAYS               245    32.7%    -0.87%
    LOW_VOL_UPTREND                603    35.2%    -0.40%
    MID_VOL_SIDEWAYS               122    45.9%     0.05%
    MID_VOL_UPTREND                476    38.0%    -0.17%
  ──────────────────────────────────────────────────────────────────
  ══════════════════════════════════════════════════════════════════

======================================================================

















