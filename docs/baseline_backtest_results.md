# Ujjwal Portfolio — Baseline Backtest Results

**Strategy config:** `f786f5cc-09f7-43b2-afbb-4f0b688f55d2` — Ujjwal's Portfolio  
**Capital:** ₹1,00,000  
**Universe:** broad150 (Nifty50 + NiftyNext50 + NiftyMidcap50 = 150 symbols)  
**Strategies:** TrendFollow + Breakout + QuietBreakout + TrendPullback + RSI-MR (all 5 enabled)  
**Risk params:** max_position=10% · risk/trade=0.5% · breadth CB=35% · ATR ratio≥3×

---

## Part A — Stored Runs (from web UI backtest history)

> **Important:** These runs used **different risk params** than Ujjwal's production config.
> The CB threshold (`pause_threshold_pct`) ranged from 5–13%, vs Ujjwal's current **35%**.
> A higher threshold means the CB triggers less often → more trades, more market exposure.
> These runs are included for reference but are **not a valid baseline for Ujjwal's config**.

| Run ID | Date | Universe | Strategies | Period | Capital | MaxPos | CB% | Risk% | Return | Sharpe | MaxDD | Trades | WinRate |
|--------|------|----------|-----------|--------|---------|--------|-----|-------|--------|--------|-------|--------|---------|
| bt_c1102a | 2026-04-03 | broad150 | All 5 | 2020-01 → 2021-03 | ₹10L | 12% | 7% | 0.75% | **+55.45%** | **2.40** | -8.96% | 1523 | 51.0% |
| bt_ee9a3d | 2026-04-03 | broad150 | All 5 | 2021-01 → 2022-03 | ₹10L | 12% | 7% | 0.75% | **+28.89%** | **1.56** | -15.33% | 1522 | 47.2% |
| bt_d83d16 | 2026-04-03 | broad150 | All 5 | 2023-04 → 2026-03 | ₹10L | 12% | 7% | 0.75% | +29.42% | 0.76 | -17.18% | 3293 | 46.2% |
| bt_9d2fb3 | 2026-04-02 | broad150 | All 5 | 2023-01 → 2026-03 | ₹10L | 12% | 7% | 0.75% | +25.33% | 0.64 | -18.32% | 3500 | 45.3% |
| bt_963d92 | 2026-04-03 | broad150 | All 5 | 2024-01 → 2026-03 | ₹10L | 12% | 7% | 0.75% | -6.09% | -0.16 | -17.84% | 2462 | 43.4% |
| bt_2b011f | 2026-04-03 | broad150 | All 5 | 2025-01 → 2026-03 | ₹10L | 12% | 7% | 0.75% | -4.75% | -0.38 | -9.43% | 1037 | 41.5% |
| bt_8003c8 | 2026-04-04 | broad150 | All 5 | 2024-01 → 2026-04 | ₹10L | 10% | 5% | 0.5% | -5.36% | -0.20 | -14.66% | 487 | 39.2% |
| bt_2aff2e | 2026-04-04 | broad150 | All 5 | 2025-01 → 2026-04 | ₹1L | 13% | 6% | 0.5% | -1.07% | -0.26 | -4.21% | 141 | 39.7% |
| bt_ca99bc | 2026-04-03 | broad150 | 3 strats* | 2019-01 → 2024-08 | ₹10L | 12% | 7% | 0.75% | +185.47% | 1.40 | -22.79% | 2233 | 43.4% |
| bt_71a105 | 2026-04-03 | broad150 | 3 strats* | 2023-01 → 2024-08 | ₹10L | 12% | 7% | 0.75% | +63.73% | 2.23 | -9.56% | 604 | 46.7% |

*3-strat runs: TrendFollow + QuietBreakout + TrendPullback (no Breakout or RSI-MR)

### Key observations from stored runs

1. **Bull/recovery periods (2020-2022) are the system's sweet spot** — Sharpe 1.5–2.4, returns 29–55%
2. **Recent 2024-2026 is consistently negative** across all configs. This is a regime problem: the market has been in a choppier, more volatile bear-sideways regime where trend strategies struggle.
3. **Higher CB threshold (7%) + higher risk/trade (0.75%)** in the 2020-2022 runs partially explains the stronger results — more trades captured more of the rally.
4. **Win rates cluster at 39-51%** — typical for trend-following. Profits come from letting winners run (profit factor > 1), not from being right more often.
5. **3 strategies (TF+QBK+TPB) beat all-5 over 2019-2024** with 185% return — RSI-MR and Breakout may be diluting returns in trending markets.

---

## Part B — Ujjwal's Exact Config Baseline (EqualWeight, 5-strat)

> Config: broad150 · max_pos=10% · CB=35% · risk/trade=0.5% · ATR≥3× · commission=0.10% · slippage=0.05%  
> These results use the **exact production parameters** from Ujjwal's live session.

**Generated:** 2026-05-09 00:37  
**Costs:** 0.10% commission + 0.05% slippage per side

```

========================================================================
  Period: Full  2018–2024   (2018-01-01 → 2024-06-01)
  Universe: 150 symbols → DynamicUniverse top 80 → UnionFilter
  Risk: capital=₹100,000  max_pos=10%  risk/trade=0.5%  CB=35%
  Costs: 0.10% commission + 0.05% slippage per side
========================================================================
  Config                   Sharpe    Return    MaxDD      PF     WR  #Trades
  ----------------------------------------------------------------------  [A] Equal Weight — 5 strategies × 0.20 each (no LLM)
  EqualWeight (5-strat)      1.21    97.77%   15.15%    1.42  46.5%     6269

========================================================================
  Period: Bull  2019–2020   (2019-01-01 → 2020-02-01)
  Universe: 150 symbols → DynamicUniverse top 80 → UnionFilter
  Risk: capital=₹100,000  max_pos=10%  risk/trade=0.5%  CB=35%
  Costs: 0.10% commission + 0.05% slippage per side
========================================================================
  Config                   Sharpe    Return    MaxDD      PF     WR  #Trades
  ----------------------------------------------------------------------  [A] Equal Weight — 5 strategies × 0.20 each (no LLM)
  EqualWeight (5-strat)     -0.56    -4.28%    9.44%    0.83  42.5%     1127

========================================================================
  Period: Crash 2020   (2020-01-01 → 2020-12-31)
  Universe: 150 symbols → DynamicUniverse top 80 → UnionFilter
  Risk: capital=₹100,000  max_pos=10%  risk/trade=0.5%  CB=35%
  Costs: 0.10% commission + 0.05% slippage per side
========================================================================
  Config                   Sharpe    Return    MaxDD      PF     WR  #Trades
  ----------------------------------------------------------------------  [A] Equal Weight — 5 strategies × 0.20 each (no LLM)
  EqualWeight (5-strat)      2.46    28.90%    6.23%    1.81  51.7%     1049

========================================================================
  Period: Recov 2020–2021   (2020-04-01 → 2021-12-31)
  Universe: 150 symbols → DynamicUniverse top 80 → UnionFilter
  Risk: capital=₹100,000  max_pos=10%  risk/trade=0.5%  CB=35%
  Costs: 0.10% commission + 0.05% slippage per side
========================================================================
  Config                   Sharpe    Return    MaxDD      PF     WR  #Trades
  ----------------------------------------------------------------------  [A] Equal Weight — 5 strategies × 0.20 each (no LLM)
  EqualWeight (5-strat)      2.88    77.57%    8.88%    2.13  51.5%     2088

========================================================================
  Period: Bear  2022   (2022-01-01 → 2022-12-31)
  Universe: 150 symbols → DynamicUniverse top 80 → UnionFilter
  Risk: capital=₹100,000  max_pos=10%  risk/trade=0.5%  CB=35%
  Costs: 0.10% commission + 0.05% slippage per side
========================================================================
  Config                   Sharpe    Return    MaxDD      PF     WR  #Trades
  ----------------------------------------------------------------------  [A] Equal Weight — 5 strategies × 0.20 each (no LLM)
  EqualWeight (5-strat)      0.32     2.29%    8.25%    0.95  41.6%      762

========================================================================
  Period: Recent2022–2024   (2022-01-01 → 2024-06-01)
  Universe: 150 symbols → DynamicUniverse top 80 → UnionFilter
  Risk: capital=₹100,000  max_pos=10%  risk/trade=0.5%  CB=35%
  Costs: 0.10% commission + 0.05% slippage per side
========================================================================
  Config                   Sharpe    Return    MaxDD      PF     WR  #Trades
  ----------------------------------------------------------------------  [A] Equal Weight — 5 strategies × 0.20 each (no LLM)
  EqualWeight (5-strat)      1.27    29.15%    8.25%    1.38  46.3%     2078

========================================================================
  Period: Live  2025–2026   (2025-01-01 → 2026-03-24)
  Universe: 150 symbols → DynamicUniverse top 80 → UnionFilter
  Risk: capital=₹100,000  max_pos=10%  risk/trade=0.5%  CB=35%
  Costs: 0.10% commission + 0.05% slippage per side
========================================================================
  Config                   Sharpe    Return    MaxDD      PF     WR  #Trades
  ----------------------------------------------------------------------  [A] Equal Weight — 5 strategies × 0.20 each (no LLM)
  EqualWeight (5-strat)     -0.43    -2.79%    4.94%    0.87  39.1%      757

========================================================================
  SUMMARY — Sharpe ratio across all periods
========================================================================
  Period                   EqW Sharpe   EqW Return   EqW MaxDD     WR  #Trades
  ---------------------------------------------------------------------------
  Full  2018–2024                1.21       97.77%      15.15%  46.5%     6269
  Bull  2019–2020               -0.56       -4.28%       9.44%  42.5%     1127
  Crash 2020                     2.46       28.90%       6.23%  51.7%     1049
  Recov 2020–2021                2.88       77.57%       8.88%  51.5%     2088
  Bear  2022                     0.32        2.29%       8.25%  41.6%      762
  Recent2022–2024                1.27       29.15%       8.25%  46.3%     2078
  Live  2025–2026               -0.43       -2.79%       4.94%  39.1%      757

  Generated: 2026-05-09 00:37
  Config ID: f786f5cc-09f7-43b2-afbb-4f0b688f55d2 (Ujjwal's Portfolio)
========================================================================
```

---

## Part C — After Bug #1 Fix (entry ATR stop)

> **Change:** `app/risk/agent.py:95` — ATR stop now uses `position.atr_at_entry` (locked at BUY time) instead of today's ATR.  
> **Generated:** 2026-05-09 00:50

```
  Period                   EqW Sharpe   EqW Return   EqW MaxDD     WR  #Trades
  ---------------------------------------------------------------------------
  Full  2018–2024                1.16       90.25%      15.56%  46.4%     6326
  Bull  2019–2020               -0.64       -4.84%       9.84%  42.2%     1131
  Crash 2020                     2.38       27.80%       6.32%  51.7%     1053
  Recov 2020–2021                2.80       73.41%       9.04%  51.1%     2109
  Bear  2022                     0.28        1.98%       8.26%  41.2%      770
  Recent2022–2024                1.30       29.91%       8.26%  46.5%     2083
  Live  2025–2026               -0.45       -2.91%       5.05%  38.9%      758
```

## Part D — After Bug #1 + Improvement #3 (trailing ATR stop)

> **Additional change:** `app/risk/agent.py` — stop now trails the high-watermark (max price since entry) downward.  
> All three fields now in play: `atr_at_entry`, `high_watermark`, trailing stop = `watermark − 2×entry_ATR`.  
> **Generated:** 2026-05-09 00:57

```
  Period                   EqW Sharpe   EqW Return   EqW MaxDD     WR  #Trades
  ---------------------------------------------------------------------------
  Full  2018–2024                1.13       76.63%      12.86%  46.4%     6580
  Bull  2019–2020               -0.67       -4.73%       9.29%  42.4%     1156
  Crash 2020                     2.33       26.32%       5.70%  51.7%     1097
  Recov 2020–2021                2.78       64.24%       7.95%  50.9%     2231
  Bear  2022                     0.15        0.81%       7.54%  42.3%      796
  Recent2022–2024                1.10       21.92%       7.54%  46.0%     2194
  Live  2025–2026               -0.52       -3.12%       4.73%  39.1%      780
```

---

## Three-way comparison — v1 (bug) → v2 (entry ATR) → v3 (trailing stop)

| Period | v1 MaxDD | v2 MaxDD | v3 MaxDD | MaxDD Δ (v1→v3) |
|--------|----------|----------|----------|-----------------|
| Full 2018–2024 | 15.15% | 15.56% | **12.86%** | **−2.3pp** |
| Bull 2019–2020 | 9.44% | 9.84% | **9.29%** | −0.15pp |
| Crash 2020 | 6.23% | 6.32% | **5.70%** | **−0.53pp** |
| Recov 2020–2021 | 8.88% | 9.04% | **7.95%** | **−0.93pp** |
| Bear 2022 | 8.25% | 8.26% | **7.54%** | **−0.71pp** |
| Recent 2022–2024 | 8.25% | 8.26% | **7.54%** | **−0.71pp** |
| Live 2025–2026 | 4.94% | 5.05% | **4.73%** | **−0.21pp** |

| Period | v1 Return | v2 Return | v3 Return | Return Δ (v1→v3) |
|--------|-----------|-----------|-----------|-------------------|
| Full 2018–2024 | +97.77% | +90.25% | +76.63% | −21.1pp |
| Bull 2019–2020 | −4.28% | −4.84% | −4.73% | −0.45pp |
| Crash 2020 | +28.90% | +27.80% | +26.32% | −2.58pp |
| Recov 2020–2021 | +77.57% | +73.41% | +64.24% | −13.3pp |
| Bear 2022 | +2.29% | +1.98% | +0.81% | −1.48pp |
| Recent 2022–2024 | +29.15% | +29.91% | +21.92% | −7.23pp |
| Live 2025–2026 | −2.79% | −2.91% | −3.12% | −0.33pp |

### Reading the results

**MaxDD improved across every single period** — the trailing stop does exactly what it's supposed to: it exits profitable positions before they fully reverse, capping drawdown. Full period MaxDD improved 2.3pp (15.15% → 12.86%).

**Return dropped more than expected.** The trailing stop generates 311 extra round-trips over the full period (6,269 → 6,580). Each exit+re-entry costs ~0.3% in friction. More importantly, positions that would have run 6+ months are now stopped out at smaller gains during normal pullbacks, then potentially re-entered.

**Calmar ratio (return / MaxDD) tells a clearer story:**

| Version | Full Period Return | MaxDD | Calmar |
|---------|-------------------|-------|--------|
| v1 (bug) | 97.77% | 15.15% | 6.45 |
| v2 (entry ATR) | 90.25% | 15.56% | 5.80 |
| v3 (trailing) | 76.63% | 12.86% | **5.96** |

The trailing stop recovered the Calmar degradation from v2. The raw Sharpe (1.21→1.13) looks worse, but for real-money trading, a system with −12.9% MaxDD vs −15.2% MaxDD is meaningfully more liveable — drawdowns are what cause users to shut off a system emotionally.

**Why returns dropped in bull/recovery periods:** In trending markets, ATR tends to expand as momentum builds. The entry ATR (lower vol, early in trend) combined with a trailing stop creates a tight leash. A stock gaining 15% then pulling back 2× entry-ATR (say 4%) gets stopped out with a 11% gain instead of riding to 15–20%. The system re-enters if the signal re-fires — paying costs again.

**Next tuning lever:** The `atr_multiplier=2.0` is the knob. Testing `2.5×` for the trailing distance would give positions more room to breathe in trends. This is a parameter optimisation question, not a code change.

---

## Part E — ATR Multiplier Sweep (trailing stop: 2.0× vs 2.5× vs 3.0×)

> **Change from Part D:** Same trailing-stop code. Only `atr_multiplier` varies.  
> **Generated:** 2026-05-09 01:09

```
  Sharpe ratio
  Period                 v1-bug      ATR×2.0     ATR×2.5     ATR×3.0
  ------------------------------------------------------------------
  Full  2018–2024          1.21        1.13        1.17        1.22
  Bull  2019–2020         -0.56       -0.67       -0.63       -0.62
  Crash 2020               2.46        2.37        2.22        2.29
  Recov 2020–2021          2.88        2.79        2.64        2.83
  Bear  2022               0.32        0.15        0.33        0.26
  Recent2022–2024          1.27        1.11        1.23        1.21
  Live  2025–2026         -0.43       -0.52       -0.61       -0.65

  Return %
  Period                 v1-bug      ATR×2.0     ATR×2.5     ATR×3.0
  ------------------------------------------------------------------
  Full  2018–2024         97.8%       77.3%       64.0%       53.7%
  Bull  2019–2020         -4.3%       -4.7%       -3.7%       -3.0%
  Crash 2020              28.9%       26.8%       19.8%       16.6%
  Recov 2020–2021         77.6%       64.8%       46.5%       39.9%
  Bear  2022               2.3%        0.8%        1.8%        1.2%
  Recent2022–2024         29.1%       22.3%       21.2%       17.4%
  Live  2025–2026         -2.8%       -3.1%       -3.0%       -2.7%

  MaxDD %  (lower is better)
  Period                 v1-bug      ATR×2.0     ATR×2.5     ATR×3.0
  ------------------------------------------------------------------
  Full  2018–2024         15.2%       12.9%       10.2%        8.5%
  Bull  2019–2020          9.4%        9.3%        7.4%        6.1%
  Crash 2020               6.2%        5.7%        4.7%        3.7%
  Recov 2020–2021          8.9%        8.2%        6.3%        4.8%
  Bear  2022               8.2%        7.5%        5.9%        5.1%
  Recent2022–2024          8.2%        7.5%        5.9%        5.1%
  Live  2025–2026          4.9%        4.7%        4.8%        4.1%

  #Trades
  Period                 v1-bug      ATR×2.0     ATR×2.5     ATR×3.0
  ------------------------------------------------------------------
  Full  2018–2024          6269        6578        6201        5762
  Bull  2019–2020          1127        1158        1102        1049
  Crash 2020               1049        1099        1042         978
  Recov 2020–2021          2088        2239        2068        1901
  Bear  2022                762         796         737         677
  Recent2022–2024          2078        2189        2060        1894
  Live  2025–2026           757         780         712         648
```

### Calmar ratio (Return / MaxDD — higher = better risk-adjusted)

| Version | Full Period Return | MaxDD | Calmar |
|---------|-------------------|-------|--------|
| v1-bug (buggy stop) | 97.8% | 15.2% | 6.43 |
| ATR×2.0 (trailing) | 77.3% | 12.9% | **5.99** |
| ATR×2.5 (trailing) | 64.0% | 10.2% | **6.27** |
| ATR×3.0 (trailing) | 53.7% | 8.5% | **6.32** |

### Verdict

**ATR×3.0 matches v1 Sharpe (1.22) while halving MaxDD (8.5% vs 15.2%).** This is the most striking result: wider trailing stop paradoxically improves risk-adjusted return because it stops fewer round-trips in trending markets (lower friction), while the trailing mechanism still locks in gains before full reversals.

**ATR×2.5 is best for the current bear/choppy regime:**
- Bear 2022 Sharpe: **0.33** — best of all four configs (beats v1's 0.32)
- Recent 2022-2024 Sharpe: **1.23** — second only to v1's 1.27
- MaxDD cut to 10.2% vs 15.2% (v1) — a third lower
- Calmar 6.27 beats ATR×2.0's 5.99

**Why wider stop → fewer trades → better Sharpe:**  
Tighter trailing stop (2.0×) fires more often on normal daily pullbacks, generating unnecessary round-trips that each cost ~0.3% in friction. Wider stop (2.5–3.0×) holds through daily noise, re-enters less → total friction is lower. The cost is lower raw return (position exits at peak less often), but Sharpe improves because the vol of returns also drops.

**Recommendation: deploy ATR×2.5 to production.**

| Consideration | ATR×2.5 | ATR×3.0 |
|---|---|---|
| Full period Sharpe | 1.17 | 1.22 |
| Bear 2022 Sharpe | **0.33** | 0.26 |
| Recent Sharpe | **1.23** | 1.21 |
| Full MaxDD | 10.2% | **8.5%** |
| Full return | **64.0%** | 53.7% |
| Calmar | 6.27 | 6.32 |

ATR×2.5 wins on the two most recent periods (the most relevant forward-looking signal) and retains 10pp more return over the full period. ATR×3.0 would be the choice if minimising drawdown is the overriding goal (e.g., funded account with hard DD limits).

The change to production is a single parameter: `atr_multiplier=2.5` in `RiskAgent.__init__()` in `api/run_paper_signals.py`.

---

## Part G — RSI Threshold Fix (Bug #2: rsi_oversold 5→15, rsi_overbought 80→70)

> **Change:** `RSIMeanReversionStrategy` threshold raised from RSI_3<5 to RSI_3<15 (fires more often).  
> Exit threshold lowered from RSI_3>80 to RSI_3>70 (exits sooner).  
> Both use ATR×2.5 trailing stop. v1-bug shown for reference.  
> **Generated:** 2026-05-10 17:23

```
  Sharpe ratio
  Period                       v1-bug ATR×2.5 RSI=5ATR×2.5 RSI=15
  ----------------------------------------------------------------
  Full  2018–2024                1.21          1.17          1.09
  Bull  2019–2020               -0.56         -0.63         -0.72
  Crash 2020                     2.46          2.22          2.03
  Recov 2020–2021                2.88          2.64          2.58
  Bear  2022                     0.32          0.33          0.30
  Recent2022–2024                1.27          1.23          1.17
  Live  2025–2026               -0.43         -0.61         -0.73

  Win Rate %
  Period                       v1-bug ATR×2.5 RSI=5ATR×2.5 RSI=15
  ----------------------------------------------------------------
  Full  2018–2024               46.5%         46.4%         48.0%  ← higher
  Bear  2022                    41.6%         42.2%         44.3%  ← higher
  Recent2022–2024               46.3%         46.5%         48.1%  ← higher
  Live  2025–2026               39.1%         39.0%         41.9%  ← higher

  MaxDD %  (lower=better)
  Period                       v1-bug ATR×2.5 RSI=5ATR×2.5 RSI=15
  ----------------------------------------------------------------
  Full  2018–2024               15.2%         10.2%         11.6%  ← worse
  Live  2025–2026                4.9%          4.8%          5.3%  ← worse

  #Trades
  Period                       v1-bug ATR×2.5 RSI=5ATR×2.5 RSI=15
  ----------------------------------------------------------------
  Full  2018–2024                6269          6201          6773  ← +572 trades
```

### Verdict: revert RSI threshold back to 5

**The RSI fix proves that RSI-MR IS now trading** — win rate improves by 1.5–3pp across every period, confirming RSI_3<15 captures real mean-reversion bounces. But **net Sharpe worsens** in every period. Why:

1. **Friction > signal.** 572 extra trades × ~0.3% round-trip cost = ~1.7pp additional annual drag. The win rate improvement doesn't generate enough gross PnL to cover the extra friction.

2. **RSI-MR competes with and displaces trend signals.** With a weight of 0.20, RSI-MR BUYs during pullbacks compete against TrendPB and Breakout BUYs on the same stocks. When RSI-MR wins a conflict, it holds the position for 7 days max then exits — cutting off what would have been a longer trend trade.

3. **`max_hold_days=7` is too short for a strategy with 1.5× higher friction.** In a bear market, oversold bounces often take 10-14 days. Exiting after 7 days means selling into a recovery that hasn't fully played out.

**Why Bug #1 (entry_dates persistence) doesn't show here:** The backtest runs one continuous strategy instance per period, so `_entry_dates` persists in memory throughout — time stops already work correctly in backtests. This is a production-only fix.

**Code status:**
- `rsi_oversold=15` reverted to `rsi_oversold=5` in both `run_paper_signals.py` and `run_ujjwal_baseline.py`
- `_entry_dates` persistence for TrendPB and RSI-MR kept in `run_paper_signals.py` (production fix, correct behavior)

---

## Part F — Regime-conditional Stop Multiplier (Improvement #5 test)

> **Config:** Same trailing stop code. `regime_multipliers` map added to RiskAgent:  
> `LOW_VOL_UPTREND=2.5, MID_VOL_UPTREND=2.0, HIGH_VOL_UPTREND=1.5, *_SIDEWAYS=1.5, *_DOWNTREND=1.0`  
> **Comparison:** ATR×2.5 (fixed) vs RegimeCond (this run) vs v1-bug (reference)  
> **Generated:** 2026-05-10 16:39

```
  Sharpe ratio
  Period                     v1-bug     ATR×2.5  RegimeCond
  ----------------------------------------------------------
  Full  2018–2024              1.21        1.17        1.07
  Bull  2019–2020             -0.56       -0.63       -0.69
  Crash 2020                   2.46        2.22        2.48
  Recov 2020–2021              2.88        2.64        2.85
  Bear  2022                   0.32        0.33       -0.04
  Recent2022–2024              1.27        1.23        1.01
  Live  2025–2026             -0.43       -0.61       -0.48

  MaxDD %  (lower=better)
  Period                     v1-bug     ATR×2.5  RegimeCond
  ----------------------------------------------------------
  Full  2018–2024             15.2%       10.2%       13.3%
  Bear  2022                   8.2%        5.9%        7.8%

  #Trades
  Period                     v1-bug     ATR×2.5  RegimeCond
  ----------------------------------------------------------
  Full  2018–2024              6269        6201        6825
```

### Verdict: do not deploy

**RegimeCond fails in the two most important periods for live trading:**
- Bear 2022 Sharpe: **−0.04** vs ATR×2.5's **0.33** — from the best config to the worst
- Recent 2022-2024 Sharpe: **1.01** vs ATR×2.5's **1.23**
- Full MaxDD: **13.3%** vs ATR×2.5's **10.2%** — the protection is actually *worse*

**Why it makes things worse:**

1. **More whipsaw, not less.** In bear/sideways markets, stocks oscillate between SIDEWAYS and DOWNTREND labels daily. The tight 1.0–1.5× stops fire on normal noise, generating 624 extra round-trips (6825 vs 6201) each costing ~0.3% in friction.

2. **Regime labels are noisy at the stock level.** A stock in a mid-uptrend that pulls back 3% flips to SIDEWAYS for one day. The 1.5× stop triggers, exits the position, then the stock resumes the uptrend. Cost paid for no benefit.

3. **The breadth circuit breaker already handles market protection.** New BUYs are blocked when >35% of the universe is in DOWNTREND. Tighter stock-level stops duplicate this but add friction on existing positions.

**Where it helps:** Crash 2020 (Sharpe 2.48 vs v1's 2.46) and Recovery 2020-2021 (2.85 vs v1's 2.88) — fast directional moves where 1.0× DOWNTREND stop correctly exits before full reversals. But these periods are already well-handled by any trailing stop.

**Code status:** `_DEFAULT_REGIME_MULTIPLIERS` and `regime_multipliers` parameter are in `app/risk/agent.py` but `regime_multipliers=None` by default — no behavior change in production. Leave as-is; do not enable.

---

## Before vs After — Bug #1 fix delta

| Period | Sharpe Δ | Return Δ | MaxDD Δ | Trades Δ | Verdict |
|--------|----------|----------|---------|----------|---------|
| Full 2018–2024 | 1.21 → **1.16** (−0.05) | 97.77% → **90.25%** (−7.5pp) | 15.15% → 15.56% (worse) | +57 | Mixed |
| Bull 2019–2020 | −0.56 → −0.64 (−0.08) | −4.28% → −4.84% (−0.6pp) | 9.44% → 9.84% (worse) | +4 | Slightly worse |
| Crash 2020 | 2.46 → 2.38 (−0.08) | 28.90% → 27.80% (−1.1pp) | 6.23% → 6.32% (flat) | +4 | Slightly worse |
| Recov 2020–2021 | 2.88 → 2.80 (−0.08) | 77.57% → 73.41% (−4.2pp) | 8.88% → 9.04% (flat) | +21 | Slightly worse |
| Bear 2022 | 0.32 → 0.28 (−0.04) | 2.29% → 1.98% (−0.3pp) | 8.25% → 8.26% (flat) | +8 | Marginal |
| Recent 2022–2024 | 1.27 → **1.30** (+0.03) | 29.15% → **29.91%** (+0.76pp) | 8.25% → 8.26% (flat) | +5 | Slightly better |
| Live 2025–2026 | −0.43 → −0.45 (−0.02) | −2.79% → −2.91% (−0.1pp) | 4.94% → 5.05% (flat) | +1 | Flat |

### Why the fix slightly hurt bull/recovery periods (counterintuitive)

The fix is theoretically correct but produces a nuanced outcome:

**Bull markets**: In trending upswings, ATR tends to *expand* slightly as momentum builds. This means `entry_atr < current_atr` in bull runs. With the bug (current ATR), stops were *wider* → winners ran longer → higher raw return. With the fix (entry ATR), stops are *tighter* → positions get stopped out on normal pullbacks → 57 more round-trips (churn cost), slightly lower return.

**Bear/choppy periods**: The fix is most correct in crash scenarios where ATR doubles or triples. Here the fix keeps the stop distance at the level from when you entered (lower vol), so positions are exited sooner on drawdowns. The Recent 2022-2024 small improvement (+0.76pp) is consistent with this.

**The fix alone is not sufficient.** The entry ATR stop is the *correct foundation* for a trailing stop — you can't implement a sensible trailing stop (Bug #3) if the stop distance changes with current volatility. The full benefit will show when Bug #3 (trailing high-watermark stop) is added on top: tighter initial stop (entry ATR) + trailing upward as the stock gains = better risk/reward on winners without widening stops in crashes.

**Net assessment:** Bug #1 fix is correct and necessary plumbing for Bug #3. Marginal standalone impact. Implement Bug #3 next before concluding whether the change is net positive.

---

## Column guide

| Column | Meaning |
|--------|---------|
| Sharpe | Annualised Sharpe ratio (higher = better risk-adjusted return) |
| Return | Total return % over the period (net of costs) |
| MaxDD | Maximum drawdown % (worst peak-to-trough decline) |
| PF | Profit factor (gross profit / gross loss; >1 = profitable) |
| WR | Win rate % of closed trades |
| #Trades | Total number of completed round-trips |

## Config variants explained

- **EqualWeight**: All 5 strategies at weight 0.20. No LLM. Deterministic. The comparison floor.
- **Adaptive**: GPT-4o-mini rebalances strategy weights every 5 trading days based on regime snapshot.
- **Adaptive+RCA**: Same as Adaptive, plus RegimeContextAgent feeds breadth-level signals to relax the CB during TRANSITION_UP regimes (earlier re-entry after bear).

---

## How the RiskAgent currently works

The RiskAgent is a **single-pass, per-signal gate** that sits between the strategy router and the execution layer. Every proposed decision (BUY / SELL / HOLD) passes through it in the order it arrives. The code lives in `app/risk/agent.py`.

### Layer 1 — Breadth Circuit Breaker (BUY only)

```
if market_downtrend_pct >= max_downtrend_pct → HOLD
```

Counts how many stocks in the active universe have `"DOWNTREND"` in their stock-level regime label. If the fraction ≥ `pause_threshold_pct` (Ujjwal's config: **35%**), all new BUYs are suppressed for the day. The RCA (RegimeContextAgent) relaxes this to 30% during `TRANSITION_UP` and 38% during `BEAR_EARLY` to allow earlier re-entry.

### Layer 2 — ATR-to-Cost Filter (BUY only)

```
if (ATR / price) < (round_trip_cost × min_atr_cost_ratio) → HOLD
```

Blocks entry when the stock's daily volatility (ATR-14) is too small to cover round-trip costs (0.15%) multiplied by the ratio (3×). This filters out low-vol, choppy stocks where commissions would eat all gross PnL. Effective threshold: ATR must be ≥ **0.45% of price**.

### Layer 3 — Stock-Level Regime Filter (BUY only)

```
if stock_regime not in allowed_regimes → HOLD
```

Each strategy has its own allowlist enforced by `MultiStrategyRouter` *before* the RiskAgent sees the decision. The RiskAgent has a second copy of this gate (currently `allowed_regimes=None` in multi-strategy runs because the router already handles it).

### Layer 4 — ATR Stop (existing positions, any day)

```
stop_price = position.average_price - (atr_multiplier × current_ATR)
if current_price ≤ stop_price → SELL
```

Checked on every day for every held position. If the stock falls more than 2× the current ATR below the original entry price, the RiskAgent overrides any HOLD with a forced SELL. **Uses today's ATR, not ATR at entry.**

### Position sizing (BUY only, after all gates pass)

```
risk_budget   = total_equity × risk_per_trade_pct × strategy_weight
stop_distance = atr_multiplier × atr
vol_qty       = risk_budget / stop_distance          ← ATR-based
max_qty       = total_equity × max_position_pct × strategy_weight / price
quantity      = min(vol_qty, max_qty, available_cash / price)
```

For Ujjwal's config: `risk_per_trade_pct=0.5%`, `max_position_pct=10%`, `strategy_weight=0.20`. A single strategy can deploy at most `10% × 0.20 = 2%` of portfolio per position, and will size down further if ATR is high (stock is volatile).

### Sequential cash gate (signal runner, after RiskAgent)

After RiskAgent approves a set of BUY decisions, `run_paper_signals.py` walks through them sequentially and checks whether remaining cash can cover each one. If not, the signal is dropped (or trimmed). The code comment says "weight-descending order" but the list is **not actually sorted** — see Bug #2 below.

---

## RiskAgent bugs and improvements (priority order)

### Bug #1 — ATR stop widens in volatile markets (HIGH)

**File:** `app/risk/agent.py:95`  
**Severity:** High — directly hurts performance in bear/crash periods  

**Current code:**
```python
stop_price = position.average_price - (self.atr_multiplier * atr)
# `atr` here is TODAY's ATR, which expands when markets are volatile
```

**The problem:** ATR is a measure of recent daily volatility. During a market crash, ATR doubles or triples. When ATR expands, `atr_multiplier × atr` grows, which pushes `stop_price` *further below entry*. This means the stop distance **widens exactly when you most need it to tighten** — a stock in free fall gets a bigger stop, not a smaller one.

Example: Stock bought at ₹500 with ATR=₹10 → stop at ₹480.  
Three weeks later: stock at ₹460, ATR has doubled to ₹20 → stop now at ₹460 − ₹40 = **₹420**, still not hit despite being 8% below entry.

**The fix:** Capture ATR at BUY time and store it with the position. The stop should always use the entry ATR, not the current ATR.


```python
# In Position model: store atr_at_entry when the BUY fills
# In RiskAgent.evaluate():
entry_atr  = getattr(position, "atr_at_entry", atr)  # fall back to current if not stored
stop_price = position.average_price - (self.atr_multiplier * entry_atr)
```

**Expected improvement:** Bear 2022 and Live 2025-2026 periods — fewer trades getting stopped out too late, tighter protection of capital. MaxDD on Full period should shrink from -15.15%.

---

### Bug #2 — Cash gate not weight-ordered (MEDIUM)

**File:** `api/run_paper_signals.py:462–489`  
**Severity:** Medium — causes capital misallocation in adaptive (LLM-weighted) runs  

**Current code:**
```python
# Comment says "weight-descending order" but there is no sort:
for d in final_decisions:
    if d.action != "BUY":
        ...
```

**The problem:** `final_decisions` arrives in proposal-arrival order (alphabetical by symbol within each strategy, then by strategy order). A signal from a low-weight strategy early in the list can consume cash that a high-weight strategy's signal arriving later needs. In EqualWeight mode (all weights=0.20) this doesn't matter. In Adaptive mode, if the LLM assigns DualMA weight=0.40 and RSI-MR weight=0.05, the RSI-MR signal should yield to DualMA, not grab cash first.

**The fix:**
```python
# Sort BUYs by weight descending before walking the gate
buys_sorted = sorted(
    [d for d in final_decisions if d.action == "BUY"],
    key=lambda d: getattr(d, "weight", 0.0),
    reverse=True,
)
non_buys = [d for d in final_decisions if d.action != "BUY"]
ordered_decisions = non_buys + buys_sorted  # SELLs always execute first
```

**Expected improvement:** Cleaner capital allocation in adaptive runs. No measurable impact on EqualWeight backtest results.

---

### Improvement #3 — Trailing ATR stop (HIGH)

**File:** `app/risk/agent.py:93–102`  
**Severity:** High — the biggest single improvement for win quality  

**Current behaviour:** The stop is permanently anchored to the entry price. Once a stock gains 20%, the stop is still below entry — you can give back the entire gain before the stop triggers.

**The fix:** Track the highest closing price seen since entry. Trail the stop upward as the stock rises. Never allow the stop to move down.

```python
# Requires storing high_watermark per position (updated daily)
high_watermark = max(getattr(position, "high_watermark", position.average_price), current_price)
position.high_watermark = high_watermark   # update in-place

entry_atr  = getattr(position, "atr_at_entry", atr)
stop_price = high_watermark - (self.atr_multiplier * entry_atr)

if current_price <= stop_price:
    return Decision(symbol=symbol, action="SELL", ...)
```

**Why this matters for the baseline numbers:**
- Full 2018-2024: Profit factor is 1.42. Trailing stops let winners run longer → PF should increase.
- Recovery 2020-2021 (Sharpe 2.88): The system was already excellent here. Trailing stops should maintain or slightly improve it.
- Live 2025-2026 (Sharpe -0.43): Positions that turned profitable then reversed would have been exited earlier → smaller losses.

**Note:** This requires storing `atr_at_entry` and `high_watermark` alongside each position. In the backtest, these can be stored in the `Portfolio.positions` dict. In the live system (`run_paper_signals.py`), they need to be persisted in the `signal_queue` FILLED rows or a new side-table.

---

### Improvement #4 — Max hold duration for trend strategies (LOW)

**File:** `app/risk/agent.py` (new parameter)  
**Severity:** Low — prevents capital lock-up, minor benefit  

**Current behaviour:** RSI-MR has `max_hold_days=7` enforced inside the strategy itself. DualMA, Breakout, QuietBrk, and TrendPB have no time limit — a position can be held indefinitely if the price stays above the ATR stop and the strategy says HOLD.

**The problem:** In sideways markets, trend positions can sit range-bound for months, consuming a position slot (and cash) without contributing P&L. The opportunity cost is another BUY signal that can't be taken because cash is locked up.

**The fix:** Add `max_hold_days: int | None = None` to RiskAgent. If set, force a SELL when `days_held >= max_hold_days` even if the stop hasn't triggered and the strategy says HOLD.

**Suggested values:** DualMA → 60 days, Breakout/QuietBrk → 20 days, TrendPB → 15 days.

---

### Improvement #5 — Regime-conditional stop multiplier (LOW)

**File:** `app/risk/agent.py`  
**Severity:** Low — fine-tuning, not a structural fix  

**Current behaviour:** `atr_multiplier=2.0` is fixed regardless of regime. In low-vol uptrends, 2× ATR might be too wide (slow to exit). In high-vol downtrends, even with the ATR-at-entry fix (#1), 2× may be too tight.

**The fix:** Map regime → multiplier:
```python
_REGIME_MULTIPLIER = {
    "LOW_VOL_UPTREND":  2.5,   # wider — trend is smooth, let it breathe
    "MID_VOL_UPTREND":  2.0,   # default
    "HIGH_VOL_UPTREND": 1.5,   # tighter — vol is elevated, protect gains faster
    "SIDEWAYS":         1.5,   # tighter — choppy, exit sooner
}
```

---

## Implementation order recommendation

| # | Change | Files | Effort | Expected impact |
|---|--------|-------|--------|----------------|
| 1 | ATR stop uses entry ATR, not current ATR | `app/risk/agent.py` | 1 hour | MaxDD shrinks; bear protection improves |
| 2 | Trailing ATR stop (high watermark) | `app/risk/agent.py`, position model | 2–3 hours | Profit factor increases; win rate may drop slightly but avg win grows |
| 3 | Weight-ordered cash gate | `api/run_paper_signals.py` | 30 min | Cleaner capital allocation in adaptive mode |
| 4 | Max hold duration | `app/risk/agent.py` | 1 hour | Minor; prevents capital lock-up in sideways |
| 5 | Regime-conditional stop multiplier | `app/risk/agent.py` | 1 hour | Fine-tuning; backtest first |

**Do #1 first** — it's a pure bug fix, zero regression risk, and unblocks a correct implementation of #2 (trailing stop must use entry ATR or it becomes even more unstable).


---

## Part I — TrendPullback Regime-Conditional Profit Target

> Baseline (Part H): ATR×2.5 + vol filter, fixed ×1.05 exit.  
> New: same + LOW_VOL→×1.03 / MID_VOL→×1.05 / HIGH_VOL→×1.08.

**Generated:** 2026-05-10 19:00  
**Costs:** 0.10% commission + 0.05% slippage per side

```

========================================================================
  Period: Full  2018–2024   (2018-01-01 → 2024-06-01)
  Universe: 150 symbols → DynamicUniverse top 80 → UnionFilter
  Risk: capital=₹100,000  max_pos=10%  risk/trade=0.5%  CB=35%
  Costs: 0.10% commission + 0.05% slippage per side
========================================================================
  Config                   Sharpe    Return    MaxDD      PF     WR  #Trades
  ----------------------------------------------------------------------  [TrendPB RegimeTarget] ATR×2.5 + vol filter + regime-conditional exit (LOW_VOL→×1.03, MID_VOL→×1.05, HIGH_VOL→×1.08)
  EqW  RegimeTarget          1.15    62.06%   10.09%    1.37  46.4%     6121

========================================================================
  Period: Bull  2019–2020   (2019-01-01 → 2020-02-01)
  Universe: 150 symbols → DynamicUniverse top 80 → UnionFilter
  Risk: capital=₹100,000  max_pos=10%  risk/trade=0.5%  CB=35%
  Costs: 0.10% commission + 0.05% slippage per side
========================================================================
  Config                   Sharpe    Return    MaxDD      PF     WR  #Trades
  ----------------------------------------------------------------------  [TrendPB RegimeTarget] ATR×2.5 + vol filter + regime-conditional exit (LOW_VOL→×1.03, MID_VOL→×1.05, HIGH_VOL→×1.08)
  EqW  RegimeTarget         -0.66    -3.86%    7.38%    0.81  42.2%     1089

========================================================================
  Period: Crash 2020   (2020-01-01 → 2020-12-31)
  Universe: 150 symbols → DynamicUniverse top 80 → UnionFilter
  Risk: capital=₹100,000  max_pos=10%  risk/trade=0.5%  CB=35%
  Costs: 0.10% commission + 0.05% slippage per side
========================================================================
  Config                   Sharpe    Return    MaxDD      PF     WR  #Trades
  ----------------------------------------------------------------------  [TrendPB RegimeTarget] ATR×2.5 + vol filter + regime-conditional exit (LOW_VOL→×1.03, MID_VOL→×1.05, HIGH_VOL→×1.08)
  EqW  RegimeTarget          2.18    19.37%    4.78%    1.83  51.2%     1030

========================================================================
  Period: Recov 2020–2021   (2020-04-01 → 2021-12-31)
  Universe: 150 symbols → DynamicUniverse top 80 → UnionFilter
  Risk: capital=₹100,000  max_pos=10%  risk/trade=0.5%  CB=35%
  Costs: 0.10% commission + 0.05% slippage per side
========================================================================
  Config                   Sharpe    Return    MaxDD      PF     WR  #Trades
  ----------------------------------------------------------------------  [TrendPB RegimeTarget] ATR×2.5 + vol filter + regime-conditional exit (LOW_VOL→×1.03, MID_VOL→×1.05, HIGH_VOL→×1.08)
  EqW  RegimeTarget          2.63    45.84%    5.97%    1.93  50.7%     2040

========================================================================
  Period: Bear  2022   (2022-01-01 → 2022-12-31)
  Universe: 150 symbols → DynamicUniverse top 80 → UnionFilter
  Risk: capital=₹100,000  max_pos=10%  risk/trade=0.5%  CB=35%
  Costs: 0.10% commission + 0.05% slippage per side
========================================================================
  Config                   Sharpe    Return    MaxDD      PF     WR  #Trades
  ----------------------------------------------------------------------  [TrendPB RegimeTarget] ATR×2.5 + vol filter + regime-conditional exit (LOW_VOL→×1.03, MID_VOL→×1.05, HIGH_VOL→×1.08)
  EqW  RegimeTarget          0.32     1.67%    6.00%    1.09  42.8%      724

========================================================================
  Period: Recent2022–2024   (2022-01-01 → 2024-06-01)
  Universe: 150 symbols → DynamicUniverse top 80 → UnionFilter
  Risk: capital=₹100,000  max_pos=10%  risk/trade=0.5%  CB=35%
  Costs: 0.10% commission + 0.05% slippage per side
========================================================================
  Config                   Sharpe    Return    MaxDD      PF     WR  #Trades
  ----------------------------------------------------------------------  [TrendPB RegimeTarget] ATR×2.5 + vol filter + regime-conditional exit (LOW_VOL→×1.03, MID_VOL→×1.05, HIGH_VOL→×1.08)
  EqW  RegimeTarget          1.23    21.10%    6.00%    1.38  46.6%     2033

========================================================================
  Period: Live  2025–2026   (2025-01-01 → 2026-03-24)
  Universe: 150 symbols → DynamicUniverse top 80 → UnionFilter
  Risk: capital=₹100,000  max_pos=10%  risk/trade=0.5%  CB=35%
  Costs: 0.10% commission + 0.05% slippage per side
========================================================================
  Config                   Sharpe    Return    MaxDD      PF     WR  #Trades
  ----------------------------------------------------------------------  [TrendPB RegimeTarget] ATR×2.5 + vol filter + regime-conditional exit (LOW_VOL→×1.03, MID_VOL→×1.05, HIGH_VOL→×1.08)
  EqW  RegimeTarget         -0.53    -2.65%    4.40%    0.85  39.7%      698

========================================================================
  SUMMARY — TrendPullback regime-conditional profit target
  Baseline: Part H (ATR×2.5 + vol filter, fixed ×1.05).
  New:      same + LOW_VOL→×1.03 / MID_VOL→×1.05 / HIGH_VOL→×1.08 exit target.
========================================================================

  Sharpe ratio
  Period                 ATR×2.5 +VolTrendPB RegimeTarget
  --------------------------------------------------
  Full  2018–2024                1.18          1.15
  Bull  2019–2020               -0.57         -0.66
  Crash 2020                     2.19          2.18
  Recov 2020–2021                2.62          2.63
  Bear  2022                     0.36          0.32
  Recent2022–2024                1.24          1.23
  Live  2025–2026               -0.60         -0.53

  Return %
  Period                 ATR×2.5 +VolTrendPB RegimeTarget
  --------------------------------------------------
  Full  2018–2024               64.8%         62.1%
  Bull  2019–2020               -3.4%         -3.9%
  Crash 2020                    19.6%         19.4%
  Recov 2020–2021               46.1%         45.8%
  Bear  2022                     1.9%          1.7%
  Recent2022–2024               21.2%         21.1%
  Live  2025–2026               -3.0%         -2.6%

  MaxDD %  (lower=better)
  Period                 ATR×2.5 +VolTrendPB RegimeTarget
  --------------------------------------------------
  Full  2018–2024                9.8%         10.1%
  Bull  2019–2020                7.3%          7.4%
  Crash 2020                     4.7%          4.8%
  Recov 2020–2021                6.3%          6.0%
  Bear  2022                     5.8%          6.0%
  Recent2022–2024                5.8%          6.0%
  Live  2025–2026                4.8%          4.4%

  Win Rate %
  Period                 ATR×2.5 +VolTrendPB RegimeTarget
  --------------------------------------------------
  Full  2018–2024               46.5%         46.4%
  Bull  2019–2020               42.6%         42.2%
  Crash 2020                    51.2%         51.2%
  Recov 2020–2021               51.0%         50.7%
  Bear  2022                    42.7%         42.8%
  Recent2022–2024               46.6%         46.6%
  Live  2025–2026               39.3%         39.7%

  #Trades
  Period                 ATR×2.5 +VolTrendPB RegimeTarget
  --------------------------------------------------
  Full  2018–2024                6178          6121
  Bull  2019–2020                1093          1089
  Crash 2020                     1040          1030
  Recov 2020–2021                2067          2040
  Bear  2022                      728           724
  Recent2022–2024                2046          2033
  Live  2025–2026                 704           698

  Generated: 2026-05-10 19:00
  Config ID: f786f5cc-09f7-43b2-afbb-4f0b688f55d2 (Ujjwal's Portfolio)
========================================================================
========================================================================
```


---

## Part J — TrendPullback Exit-Only Regime-Conditional Target

> Baseline (Part H): ATR×2.5 + vol filter, fixed ×1.05 exit.  
> New: entry stays ×1.05; exit only: LOW_VOL→×1.03 / MID_VOL→×1.05 / HIGH_VOL→×1.08.  
> (Part I tested both entry+exit change — reverted; this isolates exit only.)

**Generated:** 2026-05-10 21:08  
**Costs:** 0.10% commission + 0.05% slippage per side

```

========================================================================
  Period: Full  2018–2024   (2018-01-01 → 2024-06-01)
  Universe: 150 symbols → DynamicUniverse top 80 → UnionFilter
  Risk: capital=₹100,000  max_pos=10%  risk/trade=0.5%  CB=35%
  Costs: 0.10% commission + 0.05% slippage per side
========================================================================
  Config                   Sharpe    Return    MaxDD      PF     WR  #Trades
  ----------------------------------------------------------------------  [TrendPB ExitOnly] ATR×2.5 + vol filter + regime-conditional EXIT only (entry stays ×1.05; exit: LOW_VOL→×1.03, MID_VOL→×1.05, HIGH_VOL→×1.08)
  EqW  ExitOnly              1.19    65.97%    9.92%    1.39  46.5%     6161

========================================================================
  Period: Bull  2019–2020   (2019-01-01 → 2020-02-01)
  Universe: 150 symbols → DynamicUniverse top 80 → UnionFilter
  Risk: capital=₹100,000  max_pos=10%  risk/trade=0.5%  CB=35%
  Costs: 0.10% commission + 0.05% slippage per side
========================================================================
  Config                   Sharpe    Return    MaxDD      PF     WR  #Trades
  ----------------------------------------------------------------------  [TrendPB ExitOnly] ATR×2.5 + vol filter + regime-conditional EXIT only (entry stays ×1.05; exit: LOW_VOL→×1.03, MID_VOL→×1.05, HIGH_VOL→×1.08)
  EqW  ExitOnly             -0.58    -3.44%    7.26%    0.83  42.6%     1090

========================================================================
  Period: Crash 2020   (2020-01-01 → 2020-12-31)
  Universe: 150 symbols → DynamicUniverse top 80 → UnionFilter
  Risk: capital=₹100,000  max_pos=10%  risk/trade=0.5%  CB=35%
  Costs: 0.10% commission + 0.05% slippage per side
========================================================================
  Config                   Sharpe    Return    MaxDD      PF     WR  #Trades
  ----------------------------------------------------------------------  [TrendPB ExitOnly] ATR×2.5 + vol filter + regime-conditional EXIT only (entry stays ×1.05; exit: LOW_VOL→×1.03, MID_VOL→×1.05, HIGH_VOL→×1.08)
  EqW  ExitOnly              2.17    19.35%    4.77%    1.82  51.1%     1034

========================================================================
  Period: Recov 2020–2021   (2020-04-01 → 2021-12-31)
  Universe: 150 symbols → DynamicUniverse top 80 → UnionFilter
  Risk: capital=₹100,000  max_pos=10%  risk/trade=0.5%  CB=35%
  Costs: 0.10% commission + 0.05% slippage per side
========================================================================
  Config                   Sharpe    Return    MaxDD      PF     WR  #Trades
  ----------------------------------------------------------------------  [TrendPB ExitOnly] ATR×2.5 + vol filter + regime-conditional EXIT only (entry stays ×1.05; exit: LOW_VOL→×1.03, MID_VOL→×1.05, HIGH_VOL→×1.08)
  EqW  ExitOnly              2.62    46.37%    6.25%    1.93  50.9%     2060

========================================================================
  Period: Bear  2022   (2022-01-01 → 2022-12-31)
  Universe: 150 symbols → DynamicUniverse top 80 → UnionFilter
  Risk: capital=₹100,000  max_pos=10%  risk/trade=0.5%  CB=35%
  Costs: 0.10% commission + 0.05% slippage per side
========================================================================
  Config                   Sharpe    Return    MaxDD      PF     WR  #Trades
  ----------------------------------------------------------------------  [TrendPB ExitOnly] ATR×2.5 + vol filter + regime-conditional EXIT only (entry stays ×1.05; exit: LOW_VOL→×1.03, MID_VOL→×1.05, HIGH_VOL→×1.08)
  EqW  ExitOnly              0.38     2.07%    5.69%    1.12  42.9%      727

========================================================================
  Period: Recent2022–2024   (2022-01-01 → 2024-06-01)
  Universe: 150 symbols → DynamicUniverse top 80 → UnionFilter
  Risk: capital=₹100,000  max_pos=10%  risk/trade=0.5%  CB=35%
  Costs: 0.10% commission + 0.05% slippage per side
========================================================================
  Config                   Sharpe    Return    MaxDD      PF     WR  #Trades
  ----------------------------------------------------------------------  [TrendPB ExitOnly] ATR×2.5 + vol filter + regime-conditional EXIT only (entry stays ×1.05; exit: LOW_VOL→×1.03, MID_VOL→×1.05, HIGH_VOL→×1.08)
  EqW  ExitOnly              1.26    21.81%    5.69%    1.40  46.7%     2045

========================================================================
  Period: Live  2025–2026   (2025-01-01 → 2026-03-24)
  Universe: 150 symbols → DynamicUniverse top 80 → UnionFilter
  Risk: capital=₹100,000  max_pos=10%  risk/trade=0.5%  CB=35%
  Costs: 0.10% commission + 0.05% slippage per side
========================================================================
  Config                   Sharpe    Return    MaxDD      PF     WR  #Trades
  ----------------------------------------------------------------------  [TrendPB ExitOnly] ATR×2.5 + vol filter + regime-conditional EXIT only (entry stays ×1.05; exit: LOW_VOL→×1.03, MID_VOL→×1.05, HIGH_VOL→×1.08)
  EqW  ExitOnly             -0.60    -2.98%    4.76%    0.83  39.3%      704

========================================================================
  SUMMARY — TrendPullback exit-only regime-conditional target
  Baseline: Part H (ATR×2.5 + vol filter, fixed ×1.05 exit).
  New:      entry stays ×1.05; exit LOW_VOL→×1.03 / MID→×1.05 / HIGH→×1.08.
========================================================================

  Sharpe ratio
  Period                 ATR×2.5 +VolTrendPB ExitOnly
  --------------------------------------------------
  Full  2018–2024                1.18          1.19
  Bull  2019–2020               -0.57         -0.58
  Crash 2020                     2.19          2.17
  Recov 2020–2021                2.62          2.62
  Bear  2022                     0.36          0.38
  Recent2022–2024                1.24          1.26
  Live  2025–2026               -0.60         -0.60

  Return %
  Period                 ATR×2.5 +VolTrendPB ExitOnly
  --------------------------------------------------
  Full  2018–2024               64.8%         66.0%
  Bull  2019–2020               -3.4%         -3.4%
  Crash 2020                    19.6%         19.4%
  Recov 2020–2021               46.1%         46.4%
  Bear  2022                     1.9%          2.1%
  Recent2022–2024               21.2%         21.8%
  Live  2025–2026               -3.0%         -3.0%

  MaxDD %  (lower=better)
  Period                 ATR×2.5 +VolTrendPB ExitOnly
  --------------------------------------------------
  Full  2018–2024                9.8%          9.9%
  Bull  2019–2020                7.3%          7.3%
  Crash 2020                     4.7%          4.8%
  Recov 2020–2021                6.3%          6.2%
  Bear  2022                     5.8%          5.7%
  Recent2022–2024                5.8%          5.7%
  Live  2025–2026                4.8%          4.8%

  Win Rate %
  Period                 ATR×2.5 +VolTrendPB ExitOnly
  --------------------------------------------------
  Full  2018–2024               46.5%         46.5%
  Bull  2019–2020               42.6%         42.6%
  Crash 2020                    51.2%         51.1%
  Recov 2020–2021               51.0%         50.9%
  Bear  2022                    42.7%         42.9%
  Recent2022–2024               46.6%         46.7%
  Live  2025–2026               39.3%         39.3%

  #Trades
  Period                 ATR×2.5 +VolTrendPB ExitOnly
  --------------------------------------------------
  Full  2018–2024                6178          6161
  Bull  2019–2020                1093          1090
  Crash 2020                     1040          1034
  Recov 2020–2021                2067          2060
  Bear  2022                      728           727
  Recent2022–2024                2046          2045
  Live  2025–2026                 704           704

  Generated: 2026-05-10 21:08
  Config ID: f786f5cc-09f7-43b2-afbb-4f0b688f55d2 (Ujjwal's Portfolio)
========================================================================
========================================================================
```


---

## Part K — RelativeStrength as 6th Strategy

> Baseline (Part H): ATR×2.5 + vol filter, fixed ×1.05 exit, 5 strategies.  
> TrendPB ExitOnly: regime-conditional exit target only (5 strategies).  
> 6-Strat RelStr: +RelativeStrength cross-sectional momentum, 6 strategies at 1/6 each.  
> RelStr signal: score = 0.5×return_20d + 0.5×return_10d; top-5 per day; exit if rank drops below 50th pct or after 15d.

**Generated:** 2026-05-10 22:07  
**Costs:** 0.10% commission + 0.05% slippage per side

```

========================================================================
  Period: Full  2018–2024   (2018-01-01 → 2024-06-01)
  Universe: 150 symbols → DynamicUniverse top 80 → UnionFilter
  Risk: capital=₹100,000  max_pos=10%  risk/trade=0.5%  CB=35%
  Costs: 0.10% commission + 0.05% slippage per side
========================================================================
  Config                   Sharpe    Return    MaxDD      PF     WR  #Trades
  ----------------------------------------------------------------------  [TrendPB ExitOnly] ATR×2.5 + vol filter + regime-conditional EXIT only (entry stays ×1.05; exit: LOW_VOL→×1.03, MID_VOL→×1.05, HIGH_VOL→×1.08)
  EqW  ExitOnly              1.18    64.98%    9.90%    1.38  46.5%     6161
  ----------------------------------------------------------------------  [6-Strat RelStr] ATR×2.5 + vol filter + RelativeStrength (6 strats, 1/6 each)
  EqW  6-Strat               1.21    51.34%    8.11%    1.41  46.7%     5817

========================================================================
  Period: Bull  2019–2020   (2019-01-01 → 2020-02-01)
  Universe: 150 symbols → DynamicUniverse top 80 → UnionFilter
  Risk: capital=₹100,000  max_pos=10%  risk/trade=0.5%  CB=35%
  Costs: 0.10% commission + 0.05% slippage per side
========================================================================
  Config                   Sharpe    Return    MaxDD      PF     WR  #Trades
  ----------------------------------------------------------------------  [TrendPB ExitOnly] ATR×2.5 + vol filter + regime-conditional EXIT only (entry stays ×1.05; exit: LOW_VOL→×1.03, MID_VOL→×1.05, HIGH_VOL→×1.08)
  EqW  ExitOnly             -0.58    -3.44%    7.26%    0.83  42.6%     1090
  ----------------------------------------------------------------------  [6-Strat RelStr] ATR×2.5 + vol filter + RelativeStrength (6 strats, 1/6 each)
  EqW  6-Strat              -0.66    -3.18%    5.83%    0.81  41.6%     1060

========================================================================
  Period: Crash 2020   (2020-01-01 → 2020-12-31)
  Universe: 150 symbols → DynamicUniverse top 80 → UnionFilter
  Risk: capital=₹100,000  max_pos=10%  risk/trade=0.5%  CB=35%
  Costs: 0.10% commission + 0.05% slippage per side
========================================================================
  Config                   Sharpe    Return    MaxDD      PF     WR  #Trades
  ----------------------------------------------------------------------  [TrendPB ExitOnly] ATR×2.5 + vol filter + regime-conditional EXIT only (entry stays ×1.05; exit: LOW_VOL→×1.03, MID_VOL→×1.05, HIGH_VOL→×1.08)
  EqW  ExitOnly              2.17    19.35%    4.77%    1.82  51.1%     1034
  ----------------------------------------------------------------------  [6-Strat RelStr] ATR×2.5 + vol filter + RelativeStrength (6 strats, 1/6 each)
  EqW  6-Strat               2.26    16.02%    3.69%    1.87  51.1%      990

========================================================================
  Period: Recov 2020–2021   (2020-04-01 → 2021-12-31)
  Universe: 150 symbols → DynamicUniverse top 80 → UnionFilter
  Risk: capital=₹100,000  max_pos=10%  risk/trade=0.5%  CB=35%
  Costs: 0.10% commission + 0.05% slippage per side
========================================================================
  Config                   Sharpe    Return    MaxDD      PF     WR  #Trades
  ----------------------------------------------------------------------  [TrendPB ExitOnly] ATR×2.5 + vol filter + regime-conditional EXIT only (entry stays ×1.05; exit: LOW_VOL→×1.03, MID_VOL→×1.05, HIGH_VOL→×1.08)
  EqW  ExitOnly              2.62    46.37%    6.25%    1.93  50.9%     2060
  ----------------------------------------------------------------------  [6-Strat RelStr] ATR×2.5 + vol filter + RelativeStrength (6 strats, 1/6 each)
  EqW  6-Strat               2.75    37.86%    4.74%    2.03  51.3%     1916

========================================================================
  Period: Bear  2022   (2022-01-01 → 2022-12-31)
  Universe: 150 symbols → DynamicUniverse top 80 → UnionFilter
  Risk: capital=₹100,000  max_pos=10%  risk/trade=0.5%  CB=35%
  Costs: 0.10% commission + 0.05% slippage per side
========================================================================
  Config                   Sharpe    Return    MaxDD      PF     WR  #Trades
  ----------------------------------------------------------------------  [TrendPB ExitOnly] ATR×2.5 + vol filter + regime-conditional EXIT only (entry stays ×1.05; exit: LOW_VOL→×1.03, MID_VOL→×1.05, HIGH_VOL→×1.08)
  EqW  ExitOnly              0.38     2.07%    5.69%    1.12  42.9%      727
  ----------------------------------------------------------------------  [6-Strat RelStr] ATR×2.5 + vol filter + RelativeStrength (6 strats, 1/6 each)
  EqW  6-Strat               0.33     1.44%    4.55%    1.10  42.9%      683

========================================================================
  Period: Recent2022–2024   (2022-01-01 → 2024-06-01)
  Universe: 150 symbols → DynamicUniverse top 80 → UnionFilter
  Risk: capital=₹100,000  max_pos=10%  risk/trade=0.5%  CB=35%
  Costs: 0.10% commission + 0.05% slippage per side
========================================================================
  Config                   Sharpe    Return    MaxDD      PF     WR  #Trades
  ----------------------------------------------------------------------  [TrendPB ExitOnly] ATR×2.5 + vol filter + regime-conditional EXIT only (entry stays ×1.05; exit: LOW_VOL→×1.03, MID_VOL→×1.05, HIGH_VOL→×1.08)
  EqW  ExitOnly              1.26    21.81%    5.69%    1.40  46.7%     2045
  ----------------------------------------------------------------------  [6-Strat RelStr] ATR×2.5 + vol filter + RelativeStrength (6 strats, 1/6 each)
  EqW  6-Strat               1.27    17.26%    4.55%    1.41  47.2%     1922

========================================================================
  Period: Live  2025–2026   (2025-01-01 → 2026-03-24)
  Universe: 150 symbols → DynamicUniverse top 80 → UnionFilter
  Risk: capital=₹100,000  max_pos=10%  risk/trade=0.5%  CB=35%
  Costs: 0.10% commission + 0.05% slippage per side
========================================================================
  Config                   Sharpe    Return    MaxDD      PF     WR  #Trades
  ----------------------------------------------------------------------  [TrendPB ExitOnly] ATR×2.5 + vol filter + regime-conditional EXIT only (entry stays ×1.05; exit: LOW_VOL→×1.03, MID_VOL→×1.05, HIGH_VOL→×1.08)
  EqW  ExitOnly             -0.60    -2.98%    4.76%    0.83  39.3%      704
  ----------------------------------------------------------------------  [6-Strat RelStr] ATR×2.5 + vol filter + RelativeStrength (6 strats, 1/6 each)
  EqW  6-Strat              -0.67    -2.62%    4.15%    0.81  38.6%      650

========================================================================
  SUMMARY — Part K: Add RelativeStrength as 6th strategy
  Baseline: Part H (ATR×2.5 + vol filter, fixed ×1.05 exit, 5 strats).
  TrendPB ExitOnly: regime-conditional exit target (5 strats).
  6-Strat RelStr:   +RelativeStrength cross-sectional momentum (6 strats, 1/6 each).
========================================================================

  Sharpe ratio
  Period                 ATR×2.5 +VolTrendPB ExitOnly6-Strat RelStr
  ----------------------------------------------------------------
  Full  2018–2024                1.18          1.18          1.21
  Bull  2019–2020               -0.57         -0.58         -0.66
  Crash 2020                     2.19          2.17          2.26
  Recov 2020–2021                2.62          2.62          2.75
  Bear  2022                     0.36          0.38          0.33
  Recent2022–2024                1.24          1.26          1.27
  Live  2025–2026               -0.60         -0.60         -0.67

  Return %
  Period                 ATR×2.5 +VolTrendPB ExitOnly6-Strat RelStr
  ----------------------------------------------------------------
  Full  2018–2024               64.8%         65.0%         51.3%
  Bull  2019–2020               -3.4%         -3.4%         -3.2%
  Crash 2020                    19.6%         19.4%         16.0%
  Recov 2020–2021               46.1%         46.4%         37.9%
  Bear  2022                     1.9%          2.1%          1.4%
  Recent2022–2024               21.2%         21.8%         17.3%
  Live  2025–2026               -3.0%         -3.0%         -2.6%

  MaxDD %  (lower=better)
  Period                 ATR×2.5 +VolTrendPB ExitOnly6-Strat RelStr
  ----------------------------------------------------------------
  Full  2018–2024                9.8%          9.9%          8.1%
  Bull  2019–2020                7.3%          7.3%          5.8%
  Crash 2020                     4.7%          4.8%          3.7%
  Recov 2020–2021                6.3%          6.2%          4.7%
  Bear  2022                     5.8%          5.7%          4.6%
  Recent2022–2024                5.8%          5.7%          4.6%
  Live  2025–2026                4.8%          4.8%          4.1%

  Win Rate %
  Period                 ATR×2.5 +VolTrendPB ExitOnly6-Strat RelStr
  ----------------------------------------------------------------
  Full  2018–2024               46.5%         46.5%         46.7%
  Bull  2019–2020               42.6%         42.6%         41.6%
  Crash 2020                    51.2%         51.1%         51.1%
  Recov 2020–2021               51.0%         50.9%         51.3%
  Bear  2022                    42.7%         42.9%         42.9%
  Recent2022–2024               46.6%         46.7%         47.2%
  Live  2025–2026               39.3%         39.3%         38.6%

  #Trades
  Period                 ATR×2.5 +VolTrendPB ExitOnly6-Strat RelStr
  ----------------------------------------------------------------
  Full  2018–2024                6178          6161          5817
  Bull  2019–2020                1093          1090          1060
  Crash 2020                     1040          1034           990
  Recov 2020–2021                2067          2060          1916
  Bear  2022                      728           727           683
  Recent2022–2024                2046          2045          1922
  Live  2025–2026                 704           704           650

  Generated: 2026-05-10 22:07
  Config ID: f786f5cc-09f7-43b2-afbb-4f0b688f55d2 (Ujjwal's Portfolio)
========================================================================
========================================================================
```


---

## Part K — RelativeStrength as 6th Strategy

> Baseline (Part H): ATR×2.5 + vol filter, fixed ×1.05 exit, 5 strategies.  
> TrendPB ExitOnly: regime-conditional exit target only (5 strategies).  
> 6-Strat RelStr: +RelativeStrength cross-sectional momentum, 6 strategies at 1/6 each.  
> RelStr signal: score = 0.5×return_20d + 0.5×return_10d; top-5 per day; exit if rank drops below 50th pct or after 15d.

**Generated:** 2026-05-10 22:15  
**Costs:** 0.10% commission + 0.05% slippage per side

```

========================================================================
  Period: Full  2018–2024   (2018-01-01 → 2024-06-01)
  Universe: 150 symbols → DynamicUniverse top 80 → UnionFilter
  Risk: capital=₹100,000  max_pos=10%  risk/trade=0.5%  CB=35%
  Costs: 0.10% commission + 0.05% slippage per side
========================================================================
  Config                   Sharpe    Return    MaxDD      PF     WR  #Trades
  ----------------------------------------------------------------------  [TrendPB ExitOnly] ATR×2.5 + vol filter + regime-conditional EXIT only (entry stays ×1.05; exit: LOW_VOL→×1.03, MID_VOL→×1.05, HIGH_VOL→×1.08)
  EqW  ExitOnly              1.18    64.84%    9.92%    1.38  46.5%     6160
  ----------------------------------------------------------------------  [6-Strat RelStr] ATR×2.5 + vol filter + RelativeStrength (6 strats, 1/6 each)
  EqW  6-Strat               1.21    51.33%    8.11%    1.41  46.7%     5817
  ----------------------------------------------------------------------  [RelStr Weighted] RelStr=0.20, Breakout=0.10, QuietBrk=0.10, others=0.20
  RelStr Weighted            1.12    36.61%    7.02%    1.37  48.1%     5500

========================================================================
  Period: Bull  2019–2020   (2019-01-01 → 2020-02-01)
  Universe: 150 symbols → DynamicUniverse top 80 → UnionFilter
  Risk: capital=₹100,000  max_pos=10%  risk/trade=0.5%  CB=35%
  Costs: 0.10% commission + 0.05% slippage per side
========================================================================
  Config                   Sharpe    Return    MaxDD      PF     WR  #Trades
  ----------------------------------------------------------------------  [TrendPB ExitOnly] ATR×2.5 + vol filter + regime-conditional EXIT only (entry stays ×1.05; exit: LOW_VOL→×1.03, MID_VOL→×1.05, HIGH_VOL→×1.08)
  EqW  ExitOnly             -0.58    -3.44%    7.26%    0.83  42.6%     1090
  ----------------------------------------------------------------------  [6-Strat RelStr] ATR×2.5 + vol filter + RelativeStrength (6 strats, 1/6 each)
  EqW  6-Strat              -0.66    -3.18%    5.83%    0.81  41.6%     1060
  ----------------------------------------------------------------------  [RelStr Weighted] RelStr=0.20, Breakout=0.10, QuietBrk=0.10, others=0.20
  RelStr Weighted           -0.69    -2.81%    5.07%    0.82  43.0%     1033

========================================================================
  Period: Crash 2020   (2020-01-01 → 2020-12-31)
  Universe: 150 symbols → DynamicUniverse top 80 → UnionFilter
  Risk: capital=₹100,000  max_pos=10%  risk/trade=0.5%  CB=35%
  Costs: 0.10% commission + 0.05% slippage per side
========================================================================
  Config                   Sharpe    Return    MaxDD      PF     WR  #Trades
  ----------------------------------------------------------------------  [TrendPB ExitOnly] ATR×2.5 + vol filter + regime-conditional EXIT only (entry stays ×1.05; exit: LOW_VOL→×1.03, MID_VOL→×1.05, HIGH_VOL→×1.08)
  EqW  ExitOnly              2.17    19.35%    4.77%    1.82  51.1%     1034
  ----------------------------------------------------------------------  [6-Strat RelStr] ATR×2.5 + vol filter + RelativeStrength (6 strats, 1/6 each)
  EqW  6-Strat               2.26    16.02%    3.69%    1.87  51.1%      990
  ----------------------------------------------------------------------  [RelStr Weighted] RelStr=0.20, Breakout=0.10, QuietBrk=0.10, others=0.20
  RelStr Weighted            2.20    12.08%    3.02%    1.77  53.2%      928

========================================================================
  Period: Recov 2020–2021   (2020-04-01 → 2021-12-31)
  Universe: 150 symbols → DynamicUniverse top 80 → UnionFilter
  Risk: capital=₹100,000  max_pos=10%  risk/trade=0.5%  CB=35%
  Costs: 0.10% commission + 0.05% slippage per side
========================================================================
  Config                   Sharpe    Return    MaxDD      PF     WR  #Trades
  ----------------------------------------------------------------------  [TrendPB ExitOnly] ATR×2.5 + vol filter + regime-conditional EXIT only (entry stays ×1.05; exit: LOW_VOL→×1.03, MID_VOL→×1.05, HIGH_VOL→×1.08)
  EqW  ExitOnly              2.62    46.37%    6.25%    1.93  50.9%     2060
  ----------------------------------------------------------------------  [6-Strat RelStr] ATR×2.5 + vol filter + RelativeStrength (6 strats, 1/6 each)
  EqW  6-Strat               2.75    37.86%    4.74%    2.03  51.3%     1916
  ----------------------------------------------------------------------  [RelStr Weighted] RelStr=0.20, Breakout=0.10, QuietBrk=0.10, others=0.20
  RelStr Weighted            2.74    28.64%    3.97%    2.05  53.2%     1777

========================================================================
  Period: Bear  2022   (2022-01-01 → 2022-12-31)
  Universe: 150 symbols → DynamicUniverse top 80 → UnionFilter
  Risk: capital=₹100,000  max_pos=10%  risk/trade=0.5%  CB=35%
  Costs: 0.10% commission + 0.05% slippage per side
========================================================================
  Config                   Sharpe    Return    MaxDD      PF     WR  #Trades
  ----------------------------------------------------------------------  [TrendPB ExitOnly] ATR×2.5 + vol filter + regime-conditional EXIT only (entry stays ×1.05; exit: LOW_VOL→×1.03, MID_VOL→×1.05, HIGH_VOL→×1.08)
  EqW  ExitOnly              0.38     2.07%    5.69%    1.12  42.9%      727
  ----------------------------------------------------------------------  [6-Strat RelStr] ATR×2.5 + vol filter + RelativeStrength (6 strats, 1/6 each)
  EqW  6-Strat               0.33     1.44%    4.55%    1.10  42.9%      683
  ----------------------------------------------------------------------  [RelStr Weighted] RelStr=0.20, Breakout=0.10, QuietBrk=0.10, others=0.20
  RelStr Weighted            0.14     0.52%    3.97%    1.04  44.5%      643

========================================================================
  Period: Recent2022–2024   (2022-01-01 → 2024-06-01)
  Universe: 150 symbols → DynamicUniverse top 80 → UnionFilter
  Risk: capital=₹100,000  max_pos=10%  risk/trade=0.5%  CB=35%
  Costs: 0.10% commission + 0.05% slippage per side
========================================================================
  Config                   Sharpe    Return    MaxDD      PF     WR  #Trades
  ----------------------------------------------------------------------  [TrendPB ExitOnly] ATR×2.5 + vol filter + regime-conditional EXIT only (entry stays ×1.05; exit: LOW_VOL→×1.03, MID_VOL→×1.05, HIGH_VOL→×1.08)
  EqW  ExitOnly              1.26    21.81%    5.69%    1.40  46.7%     2045
  ----------------------------------------------------------------------  [6-Strat RelStr] ATR×2.5 + vol filter + RelativeStrength (6 strats, 1/6 each)
  EqW  6-Strat               1.27    17.26%    4.55%    1.41  47.2%     1922
  ----------------------------------------------------------------------  [RelStr Weighted] RelStr=0.20, Breakout=0.10, QuietBrk=0.10, others=0.20
  RelStr Weighted            1.07    11.38%    3.97%    1.34  48.7%     1790

========================================================================
  Period: Live  2025–2026   (2025-01-01 → 2026-03-24)
  Universe: 150 symbols → DynamicUniverse top 80 → UnionFilter
  Risk: capital=₹100,000  max_pos=10%  risk/trade=0.5%  CB=35%
  Costs: 0.10% commission + 0.05% slippage per side
========================================================================
  Config                   Sharpe    Return    MaxDD      PF     WR  #Trades
  ----------------------------------------------------------------------  [TrendPB ExitOnly] ATR×2.5 + vol filter + regime-conditional EXIT only (entry stays ×1.05; exit: LOW_VOL→×1.03, MID_VOL→×1.05, HIGH_VOL→×1.08)
  EqW  ExitOnly             -0.60    -2.98%    4.76%    0.83  39.3%      704
  ----------------------------------------------------------------------  [6-Strat RelStr] ATR×2.5 + vol filter + RelativeStrength (6 strats, 1/6 each)
  EqW  6-Strat              -0.67    -2.62%    4.14%    0.81  38.6%      650
  ----------------------------------------------------------------------  [RelStr Weighted] RelStr=0.20, Breakout=0.10, QuietBrk=0.10, others=0.20
  RelStr Weighted           -0.12    -0.43%    2.17%    0.96  42.3%      614

========================================================================
  SUMMARY — Part K: RelativeStrength as 6th strategy
  Baseline:       Part H (ATR×2.5 + vol filter, 5 strats).
  TrendPB ExitOnly: regime-conditional exit (5 strats).
  6-Strat EqW:    +RelStr at 1/6 each.
  RelStr Weighted: RelStr=0.20, Breakout=QuietBrk=0.10, others=0.20.
========================================================================

  Sharpe ratio
  Period                 ATR×2.5 +VolTrendPB ExitOnly   6-Strat EqWRelStr Weighted
  ------------------------------------------------------------------------------
  Full  2018–2024                1.18          1.18          1.21          1.12
  Bull  2019–2020               -0.57         -0.58         -0.66         -0.69
  Crash 2020                     2.19          2.17          2.26          2.20
  Recov 2020–2021                2.62          2.62          2.75          2.74
  Bear  2022                     0.36          0.38          0.33          0.14
  Recent2022–2024                1.24          1.26          1.27          1.07
  Live  2025–2026               -0.60         -0.60         -0.67         -0.12

  Return %
  Period                 ATR×2.5 +VolTrendPB ExitOnly   6-Strat EqWRelStr Weighted
  ------------------------------------------------------------------------------
  Full  2018–2024               64.8%         64.8%         51.3%         36.6%
  Bull  2019–2020               -3.4%         -3.4%         -3.2%         -2.8%
  Crash 2020                    19.6%         19.4%         16.0%         12.1%
  Recov 2020–2021               46.1%         46.4%         37.9%         28.6%
  Bear  2022                     1.9%          2.1%          1.4%          0.5%
  Recent2022–2024               21.2%         21.8%         17.3%         11.4%
  Live  2025–2026               -3.0%         -3.0%         -2.6%         -0.4%

  MaxDD %  (lower=better)
  Period                 ATR×2.5 +VolTrendPB ExitOnly   6-Strat EqWRelStr Weighted
  ------------------------------------------------------------------------------
  Full  2018–2024                9.8%          9.9%          8.1%          7.0%
  Bull  2019–2020                7.3%          7.3%          5.8%          5.1%
  Crash 2020                     4.7%          4.8%          3.7%          3.0%
  Recov 2020–2021                6.3%          6.2%          4.7%          4.0%
  Bear  2022                     5.8%          5.7%          4.6%          4.0%
  Recent2022–2024                5.8%          5.7%          4.6%          4.0%
  Live  2025–2026                4.8%          4.8%          4.1%          2.2%

  Win Rate %
  Period                 ATR×2.5 +VolTrendPB ExitOnly   6-Strat EqWRelStr Weighted
  ------------------------------------------------------------------------------
  Full  2018–2024               46.5%         46.5%         46.7%         48.1%
  Bull  2019–2020               42.6%         42.6%         41.6%         43.0%
  Crash 2020                    51.2%         51.1%         51.1%         53.2%
  Recov 2020–2021               51.0%         50.9%         51.3%         53.2%
  Bear  2022                    42.7%         42.9%         42.9%         44.5%
  Recent2022–2024               46.6%         46.7%         47.2%         48.7%
  Live  2025–2026               39.3%         39.3%         38.6%         42.3%

  #Trades
  Period                 ATR×2.5 +VolTrendPB ExitOnly   6-Strat EqWRelStr Weighted
  ------------------------------------------------------------------------------
  Full  2018–2024                6178          6160          5817          5500
  Bull  2019–2020                1093          1090          1060          1033
  Crash 2020                     1040          1034           990           928
  Recov 2020–2021                2067          2060          1916          1777
  Bear  2022                      728           727           683           643
  Recent2022–2024                2046          2045          1922          1790
  Live  2025–2026                 704           704           650           614

  Generated: 2026-05-10 22:15
  Config ID: f786f5cc-09f7-43b2-afbb-4f0b688f55d2 (Ujjwal's Portfolio)
========================================================================
========================================================================
```


---

## Part K — RelativeStrength as 6th Strategy

> Baseline (Part H): ATR×2.5 + vol filter, fixed ×1.05 exit, 5 strategies.  
> TrendPB ExitOnly: regime-conditional exit target only (5 strategies).  
> 6-Strat RelStr: +RelativeStrength cross-sectional momentum, 6 strategies at 1/6 each.  
> RelStr signal: score = 0.5×return_20d + 0.5×return_10d; top-5 per day; exit if rank drops below 50th pct or after 15d.

**Generated:** 2026-05-10 22:23  
**Costs:** 0.10% commission + 0.05% slippage per side

```

========================================================================
  Period: Full  2018–2024   (2018-01-01 → 2024-06-01)
  Universe: 150 symbols → DynamicUniverse top 80 → UnionFilter
  Risk: capital=₹100,000  max_pos=10%  risk/trade=0.5%  CB=35%
  Costs: 0.10% commission + 0.05% slippage per side
========================================================================
  Config                   Sharpe    Return    MaxDD      PF     WR  #Trades
  ----------------------------------------------------------------------  [TrendPB ExitOnly] ATR×2.5 + vol filter + regime-conditional EXIT only (entry stays ×1.05; exit: LOW_VOL→×1.03, MID_VOL→×1.05, HIGH_VOL→×1.08)
  EqW  ExitOnly              1.17    64.15%    9.92%    1.38  46.5%     6162
  ----------------------------------------------------------------------  [6-Strat RelStr] ATR×2.5 + vol filter + RelativeStrength (6 strats, 1/6 each)
  EqW  6-Strat               1.21    51.34%    8.11%    1.41  46.7%     5817
  ----------------------------------------------------------------------  [RelStr Weighted] RelStr=0.20, Breakout=0.10, QuietBrk=0.10, others=0.20
  RelStr Weighted            1.12    36.61%    7.02%    1.37  48.1%     5500
  ----------------------------------------------------------------------  [RelStr UpOnly] same weights + RelStr gated to UPTREND_ONLY (no sideways)
  RelStr UpOnly              1.10    35.83%    6.62%    1.36  48.0%     5506

========================================================================
  Period: Bull  2019–2020   (2019-01-01 → 2020-02-01)
  Universe: 150 symbols → DynamicUniverse top 80 → UnionFilter
  Risk: capital=₹100,000  max_pos=10%  risk/trade=0.5%  CB=35%
  Costs: 0.10% commission + 0.05% slippage per side
========================================================================
  Config                   Sharpe    Return    MaxDD      PF     WR  #Trades
  ----------------------------------------------------------------------  [TrendPB ExitOnly] ATR×2.5 + vol filter + regime-conditional EXIT only (entry stays ×1.05; exit: LOW_VOL→×1.03, MID_VOL→×1.05, HIGH_VOL→×1.08)
  EqW  ExitOnly             -0.58    -3.44%    7.26%    0.83  42.6%     1090
  ----------------------------------------------------------------------  [6-Strat RelStr] ATR×2.5 + vol filter + RelativeStrength (6 strats, 1/6 each)
  EqW  6-Strat              -0.66    -3.18%    5.83%    0.81  41.6%     1060
  ----------------------------------------------------------------------  [RelStr Weighted] RelStr=0.20, Breakout=0.10, QuietBrk=0.10, others=0.20
  RelStr Weighted           -0.69    -2.81%    5.07%    0.82  43.0%     1033
  ----------------------------------------------------------------------  [RelStr UpOnly] same weights + RelStr gated to UPTREND_ONLY (no sideways)
  RelStr UpOnly             -0.64    -2.60%    4.72%    0.83  42.8%     1031

========================================================================
  Period: Crash 2020   (2020-01-01 → 2020-12-31)
  Universe: 150 symbols → DynamicUniverse top 80 → UnionFilter
  Risk: capital=₹100,000  max_pos=10%  risk/trade=0.5%  CB=35%
  Costs: 0.10% commission + 0.05% slippage per side
========================================================================
  Config                   Sharpe    Return    MaxDD      PF     WR  #Trades
  ----------------------------------------------------------------------  [TrendPB ExitOnly] ATR×2.5 + vol filter + regime-conditional EXIT only (entry stays ×1.05; exit: LOW_VOL→×1.03, MID_VOL→×1.05, HIGH_VOL→×1.08)
  EqW  ExitOnly              2.17    19.35%    4.77%    1.82  51.1%     1034
  ----------------------------------------------------------------------  [6-Strat RelStr] ATR×2.5 + vol filter + RelativeStrength (6 strats, 1/6 each)
  EqW  6-Strat               2.26    16.02%    3.69%    1.87  51.1%      990
  ----------------------------------------------------------------------  [RelStr Weighted] RelStr=0.20, Breakout=0.10, QuietBrk=0.10, others=0.20
  RelStr Weighted            2.20    12.08%    3.02%    1.77  53.2%      928
  ----------------------------------------------------------------------  [RelStr UpOnly] same weights + RelStr gated to UPTREND_ONLY (no sideways)
  RelStr UpOnly              2.12    11.64%    3.08%    1.74  52.7%      928

========================================================================
  Period: Recov 2020–2021   (2020-04-01 → 2021-12-31)
  Universe: 150 symbols → DynamicUniverse top 80 → UnionFilter
  Risk: capital=₹100,000  max_pos=10%  risk/trade=0.5%  CB=35%
  Costs: 0.10% commission + 0.05% slippage per side
========================================================================
  Config                   Sharpe    Return    MaxDD      PF     WR  #Trades
  ----------------------------------------------------------------------  [TrendPB ExitOnly] ATR×2.5 + vol filter + regime-conditional EXIT only (entry stays ×1.05; exit: LOW_VOL→×1.03, MID_VOL→×1.05, HIGH_VOL→×1.08)
  EqW  ExitOnly              2.62    46.37%    6.25%    1.93  50.9%     2060
  ----------------------------------------------------------------------  [6-Strat RelStr] ATR×2.5 + vol filter + RelativeStrength (6 strats, 1/6 each)
  EqW  6-Strat               2.75    37.86%    4.74%    2.03  51.3%     1916
  ----------------------------------------------------------------------  [RelStr Weighted] RelStr=0.20, Breakout=0.10, QuietBrk=0.10, others=0.20
  RelStr Weighted            2.74    28.67%    3.97%    2.05  53.3%     1776
  ----------------------------------------------------------------------  [RelStr UpOnly] same weights + RelStr gated to UPTREND_ONLY (no sideways)
  RelStr UpOnly              2.70    28.10%    3.94%    2.04  53.0%     1776

========================================================================
  Period: Bear  2022   (2022-01-01 → 2022-12-31)
  Universe: 150 symbols → DynamicUniverse top 80 → UnionFilter
  Risk: capital=₹100,000  max_pos=10%  risk/trade=0.5%  CB=35%
  Costs: 0.10% commission + 0.05% slippage per side
========================================================================
  Config                   Sharpe    Return    MaxDD      PF     WR  #Trades
  ----------------------------------------------------------------------  [TrendPB ExitOnly] ATR×2.5 + vol filter + regime-conditional EXIT only (entry stays ×1.05; exit: LOW_VOL→×1.03, MID_VOL→×1.05, HIGH_VOL→×1.08)
  EqW  ExitOnly              0.38     2.07%    5.69%    1.12  42.9%      727
  ----------------------------------------------------------------------  [6-Strat RelStr] ATR×2.5 + vol filter + RelativeStrength (6 strats, 1/6 each)
  EqW  6-Strat               0.33     1.44%    4.55%    1.10  42.9%      683
  ----------------------------------------------------------------------  [RelStr Weighted] RelStr=0.20, Breakout=0.10, QuietBrk=0.10, others=0.20
  RelStr Weighted            0.14     0.52%    3.97%    1.04  44.5%      643
  ----------------------------------------------------------------------  [RelStr UpOnly] same weights + RelStr gated to UPTREND_ONLY (no sideways)
  RelStr UpOnly              0.13     0.45%    4.10%    1.03  44.1%      646

========================================================================
  Period: Recent2022–2024   (2022-01-01 → 2024-06-01)
  Universe: 150 symbols → DynamicUniverse top 80 → UnionFilter
  Risk: capital=₹100,000  max_pos=10%  risk/trade=0.5%  CB=35%
  Costs: 0.10% commission + 0.05% slippage per side
========================================================================
  Config                   Sharpe    Return    MaxDD      PF     WR  #Trades
  ----------------------------------------------------------------------  [TrendPB ExitOnly] ATR×2.5 + vol filter + regime-conditional EXIT only (entry stays ×1.05; exit: LOW_VOL→×1.03, MID_VOL→×1.05, HIGH_VOL→×1.08)
  EqW  ExitOnly              1.26    21.76%    5.69%    1.40  46.7%     2045
  ----------------------------------------------------------------------  [6-Strat RelStr] ATR×2.5 + vol filter + RelativeStrength (6 strats, 1/6 each)
  EqW  6-Strat               1.27    17.25%    4.55%    1.41  47.2%     1922
  ----------------------------------------------------------------------  [RelStr Weighted] RelStr=0.20, Breakout=0.10, QuietBrk=0.10, others=0.20
  RelStr Weighted            1.07    11.38%    3.97%    1.34  48.7%     1790
  ----------------------------------------------------------------------  [RelStr UpOnly] same weights + RelStr gated to UPTREND_ONLY (no sideways)
  RelStr UpOnly              1.12    12.04%    4.10%    1.36  48.6%     1801

========================================================================
  Period: Live  2025–2026   (2025-01-01 → 2026-03-24)
  Universe: 150 symbols → DynamicUniverse top 80 → UnionFilter
  Risk: capital=₹100,000  max_pos=10%  risk/trade=0.5%  CB=35%
  Costs: 0.10% commission + 0.05% slippage per side
========================================================================
  Config                   Sharpe    Return    MaxDD      PF     WR  #Trades
  ----------------------------------------------------------------------  [TrendPB ExitOnly] ATR×2.5 + vol filter + regime-conditional EXIT only (entry stays ×1.05; exit: LOW_VOL→×1.03, MID_VOL→×1.05, HIGH_VOL→×1.08)
  EqW  ExitOnly             -0.60    -2.98%    4.76%    0.83  39.3%      704
  ----------------------------------------------------------------------  [6-Strat RelStr] ATR×2.5 + vol filter + RelativeStrength (6 strats, 1/6 each)
  EqW  6-Strat              -0.67    -2.62%    4.14%    0.81  38.6%      650
  ----------------------------------------------------------------------  [RelStr Weighted] RelStr=0.20, Breakout=0.10, QuietBrk=0.10, others=0.20
  RelStr Weighted           -0.12    -0.43%    2.17%    0.96  42.3%      614
  ----------------------------------------------------------------------  [RelStr UpOnly] same weights + RelStr gated to UPTREND_ONLY (no sideways)
  RelStr UpOnly             -0.14    -0.47%    2.09%    0.96  41.7%      614

========================================================================
  SUMMARY — Part K: RelativeStrength as 6th strategy
  Baseline:         Part H (ATR×2.5 + vol filter, 5 strats).
  TrendPB ExitOnly: regime-conditional exit (5 strats).
  6-Strat EqW:      +RelStr at 1/6 each.
  RelStr Weighted:  RelStr=0.20, Breakout=QuietBrk=0.10, others=0.20.
  RelStr UpOnly:    same weights + RelStr gated to UPTREND_ONLY.
========================================================================

  Sharpe ratio
  Period                 ATR×2.5 +VolTrendPB ExitOnly   6-Strat EqWRelStr Weighted RelStr UpOnly
  --------------------------------------------------------------------------------------------
  Full  2018–2024                1.18          1.17          1.21          1.12          1.10
  Bull  2019–2020               -0.57         -0.58         -0.66         -0.69         -0.64
  Crash 2020                     2.19          2.17          2.26          2.20          2.12
  Recov 2020–2021                2.62          2.62          2.75          2.74          2.70
  Bear  2022                     0.36          0.38          0.33          0.14          0.13
  Recent2022–2024                1.24          1.26          1.27          1.07          1.12
  Live  2025–2026               -0.60         -0.60         -0.67         -0.12         -0.14

  Return %
  Period                 ATR×2.5 +VolTrendPB ExitOnly   6-Strat EqWRelStr Weighted RelStr UpOnly
  --------------------------------------------------------------------------------------------
  Full  2018–2024               64.8%         64.2%         51.3%         36.6%         35.8%
  Bull  2019–2020               -3.4%         -3.4%         -3.2%         -2.8%         -2.6%
  Crash 2020                    19.6%         19.4%         16.0%         12.1%         11.6%
  Recov 2020–2021               46.1%         46.4%         37.9%         28.7%         28.1%
  Bear  2022                     1.9%          2.1%          1.4%          0.5%          0.5%
  Recent2022–2024               21.2%         21.8%         17.3%         11.4%         12.0%
  Live  2025–2026               -3.0%         -3.0%         -2.6%         -0.4%         -0.5%

  MaxDD %  (lower=better)
  Period                 ATR×2.5 +VolTrendPB ExitOnly   6-Strat EqWRelStr Weighted RelStr UpOnly
  --------------------------------------------------------------------------------------------
  Full  2018–2024                9.8%          9.9%          8.1%          7.0%          6.6%
  Bull  2019–2020                7.3%          7.3%          5.8%          5.1%          4.7%
  Crash 2020                     4.7%          4.8%          3.7%          3.0%          3.1%
  Recov 2020–2021                6.3%          6.2%          4.7%          4.0%          3.9%
  Bear  2022                     5.8%          5.7%          4.6%          4.0%          4.1%
  Recent2022–2024                5.8%          5.7%          4.6%          4.0%          4.1%
  Live  2025–2026                4.8%          4.8%          4.1%          2.2%          2.1%

  Win Rate %
  Period                 ATR×2.5 +VolTrendPB ExitOnly   6-Strat EqWRelStr Weighted RelStr UpOnly
  --------------------------------------------------------------------------------------------
  Full  2018–2024               46.5%         46.5%         46.7%         48.1%         48.0%
  Bull  2019–2020               42.6%         42.6%         41.6%         43.0%         42.8%
  Crash 2020                    51.2%         51.1%         51.1%         53.2%         52.7%
  Recov 2020–2021               51.0%         50.9%         51.3%         53.3%         53.0%
  Bear  2022                    42.7%         42.9%         42.9%         44.5%         44.1%
  Recent2022–2024               46.6%         46.7%         47.2%         48.7%         48.6%
  Live  2025–2026               39.3%         39.3%         38.6%         42.3%         41.7%

  #Trades
  Period                 ATR×2.5 +VolTrendPB ExitOnly   6-Strat EqWRelStr Weighted RelStr UpOnly
  --------------------------------------------------------------------------------------------
  Full  2018–2024                6178          6162          5817          5500          5506
  Bull  2019–2020                1093          1090          1060          1033          1031
  Crash 2020                     1040          1034           990           928           928
  Recov 2020–2021                2067          2060          1916          1776          1776
  Bear  2022                      728           727           683           643           646
  Recent2022–2024                2046          2045          1922          1790          1801
  Live  2025–2026                 704           704           650           614           614

  Generated: 2026-05-10 22:23
  Config ID: f786f5cc-09f7-43b2-afbb-4f0b688f55d2 (Ujjwal's Portfolio)
========================================================================
========================================================================
```


---

## Latest Run

> Config: AdaptiveStrategySelector (gpt-4o-mini, weekly LLM rebalance).  

**Generated:** 2026-05-11 01:10  
**Mode:** --adaptive  
**Costs:** 0.10% commission + 0.05% slippage per side

```
  Mode: --adaptive (AdaptiveStrategySelector, gpt-4o-mini, rebalance every 5 days)

========================================================================
  Period: Full  2018–2024   (2018-01-01 → 2024-06-01)
  Universe: 150 symbols → DynamicUniverse top 80 → UnionFilter
  Risk: capital=₹100,000  max_pos=10%  risk/trade=0.5%  CB=35%
  Costs: 0.10% commission + 0.05% slippage per side
========================================================================
  Config                   Sharpe    Return    MaxDD      PF     WR  #Trades
  ----------------------------------------------------------------------  [Adaptive] ATR×2.5 + AdaptiveStrategySelector (LLM rebalance)
  Adaptive (LLM)             1.31   109.99%   16.91%    1.45  43.6%     5207

========================================================================
  Period: Bull  2019–2020   (2019-01-01 → 2020-02-01)
  Universe: 150 symbols → DynamicUniverse top 80 → UnionFilter
  Risk: capital=₹100,000  max_pos=10%  risk/trade=0.5%  CB=35%
  Costs: 0.10% commission + 0.05% slippage per side
========================================================================
  Config                   Sharpe    Return    MaxDD      PF     WR  #Trades
  ----------------------------------------------------------------------  [Adaptive] ATR×2.5 + AdaptiveStrategySelector (LLM rebalance)
  Adaptive (LLM)            -0.80    -6.19%   10.99%    0.75  39.9%      867

========================================================================
  Period: Crash 2020   (2020-01-01 → 2020-12-31)
  Universe: 150 symbols → DynamicUniverse top 80 → UnionFilter
  Risk: capital=₹100,000  max_pos=10%  risk/trade=0.5%  CB=35%
  Costs: 0.10% commission + 0.05% slippage per side
========================================================================
  Config                   Sharpe    Return    MaxDD      PF     WR  #Trades
  ----------------------------------------------------------------------  [Adaptive] ATR×2.5 + AdaptiveStrategySelector (LLM rebalance)
  Adaptive (LLM)             2.35    30.38%    7.04%    1.89  46.8%      891

========================================================================
  Period: Recov 2020–2021   (2020-04-01 → 2021-12-31)
  Universe: 150 symbols → DynamicUniverse top 80 → UnionFilter
  Risk: capital=₹100,000  max_pos=10%  risk/trade=0.5%  CB=35%
  Costs: 0.10% commission + 0.05% slippage per side
========================================================================
  Config                   Sharpe    Return    MaxDD      PF     WR  #Trades
  ----------------------------------------------------------------------  [Adaptive] ATR×2.5 + AdaptiveStrategySelector (LLM rebalance)
  Adaptive (LLM)             2.84    77.77%    8.85%    2.02  48.5%     1799

========================================================================
  Period: Bear  2022   (2022-01-01 → 2022-12-31)
  Universe: 150 symbols → DynamicUniverse top 80 → UnionFilter
  Risk: capital=₹100,000  max_pos=10%  risk/trade=0.5%  CB=35%
  Costs: 0.10% commission + 0.05% slippage per side
========================================================================
  Config                   Sharpe    Return    MaxDD      PF     WR  #Trades
  ----------------------------------------------------------------------  [Adaptive] ATR×2.5 + AdaptiveStrategySelector (LLM rebalance)
  Adaptive (LLM)             0.84     6.52%    7.91%    1.29  40.5%      615

========================================================================
  Period: Recent2022–2024   (2022-01-01 → 2024-06-01)
  Universe: 150 symbols → DynamicUniverse top 80 → UnionFilter
  Risk: capital=₹100,000  max_pos=10%  risk/trade=0.5%  CB=35%
  Costs: 0.10% commission + 0.05% slippage per side
========================================================================
  Config                   Sharpe    Return    MaxDD      PF     WR  #Trades
  ----------------------------------------------------------------------  [Adaptive] ATR×2.5 + AdaptiveStrategySelector (LLM rebalance)
  Adaptive (LLM)             1.78    46.44%    7.95%    1.59  44.9%     1767

========================================================================
  Period: Live  2025–2026   (2025-01-01 → 2026-03-24)
  Universe: 150 symbols → DynamicUniverse top 80 → UnionFilter
  Risk: capital=₹100,000  max_pos=10%  risk/trade=0.5%  CB=35%
  Costs: 0.10% commission + 0.05% slippage per side
========================================================================
  Config                   Sharpe    Return    MaxDD      PF     WR  #Trades
  ----------------------------------------------------------------------  [Adaptive] ATR×2.5 + AdaptiveStrategySelector (LLM rebalance)
  Adaptive (LLM)            -0.81    -6.05%    8.33%    0.76  36.6%      644

========================================================================
  SUMMARY — Adaptive pre-change vs post-change
  Adaptive baseline: pre-change LLM prompt results (from _ADAPTIVE_BASELINE).
  Adaptive current: this run — measures LLM prompt improvement.
  NOTE: _ADAPTIVE_BASELINE is empty — fill it after the first --adaptive run.
========================================================================

  Sharpe ratio
  Period                Adaptive baseline  Adaptive current
  ----------------------------------------------------------
  Full  2018–2024                    1.31              1.31
  Bull  2019–2020                   -0.80             -0.80
  Crash 2020                         2.35              2.35
  Recov 2020–2021                    2.84              2.84
  Bear  2022                         0.84              0.84
  Recent2022–2024                    1.78              1.78
  Live  2025–2026                   -0.81             -0.81

  Return %
  Period                Adaptive baseline  Adaptive current
  ----------------------------------------------------------
  Full  2018–2024                  110.0%            110.0%
  Bull  2019–2020                   -6.2%             -6.2%
  Crash 2020                        30.4%             30.4%
  Recov 2020–2021                   77.8%             77.8%
  Bear  2022                         6.5%              6.5%
  Recent2022–2024                   46.4%             46.4%
  Live  2025–2026                   -6.0%             -6.0%

  MaxDD %  (lower=better)
  Period                Adaptive baseline  Adaptive current
  ----------------------------------------------------------
  Full  2018–2024                   16.9%             16.9%
  Bull  2019–2020                   11.0%             11.0%
  Crash 2020                         7.0%              7.0%
  Recov 2020–2021                    8.8%              8.8%
  Bear  2022                         7.9%              7.9%
  Recent2022–2024                    7.9%              7.9%
  Live  2025–2026                    8.3%              8.3%

  Win Rate %
  Period                Adaptive baseline  Adaptive current
  ----------------------------------------------------------
  Full  2018–2024                   43.6%             43.6%
  Bull  2019–2020                   39.9%             39.9%
  Crash 2020                        46.8%             46.8%
  Recov 2020–2021                   48.5%             48.5%
  Bear  2022                        40.5%             40.5%
  Recent2022–2024                   44.9%             44.9%
  Live  2025–2026                   36.6%             36.6%

  #Trades
  Period                Adaptive baseline  Adaptive current
  ----------------------------------------------------------
  Full  2018–2024                    5207              5207
  Bull  2019–2020                     867               867
  Crash 2020                          891               891
  Recov 2020–2021                    1799              1799
  Bear  2022                          615               615
  Recent2022–2024                    1767              1767
  Live  2025–2026                     644               644

  Generated: 2026-05-11 01:10
  Mode: --adaptive (LLM)
  Config ID: f786f5cc-09f7-43b2-afbb-4f0b688f55d2 (Ujjwal's Portfolio)
========================================================================
========================================================================
```


---

## Latest Run

> Config: ATR×2.5 trailing stop + volume filter (vol_ratio>1.2).  

**Generated:** 2026-05-11 01:10  
**Mode:** EqualWeight  
**Costs:** 0.10% commission + 0.05% slippage per side

```
  Mode: --adaptive (AdaptiveStrategySelector, gpt-4o-mini, rebalance every 5 days)

========================================================================
  Period: Full  2018–2024   (2018-01-01 → 2024-06-01)
  Universe: 150 symbols → DynamicUniverse top 80 → UnionFilter
  Risk: capital=₹100,000  max_pos=10%  risk/trade=0.5%  CB=35%
  Costs: 0.10% commission + 0.05% slippage per side
========================================================================
  Config                   Sharpe    Return    MaxDD      PF     WR  #Trades
  ----------------------------------------------------------------------  [Adaptive] ATR×2.5 + AdaptiveStrategySelector (LLM rebalance)
  Adaptive (LLM)             1.31   109.99%   16.91%    1.45  43.6%     5207

========================================================================
  Period: Bull  2019–2020   (2019-01-01 → 2020-02-01)
  Universe: 150 symbols → DynamicUniverse top 80 → UnionFilter
  Risk: capital=₹100,000  max_pos=10%  risk/trade=0.5%  CB=35%
  Costs: 0.10% commission + 0.05% slippage per side
========================================================================
  Config                   Sharpe    Return    MaxDD      PF     WR  #Trades
  ----------------------------------------------------------------------  [Adaptive] ATR×2.5 + AdaptiveStrategySelector (LLM rebalance)
  Adaptive (LLM)            -0.80    -6.19%   10.99%    0.75  39.9%      867

========================================================================
  Period: Crash 2020   (2020-01-01 → 2020-12-31)
  Universe: 150 symbols → DynamicUniverse top 80 → UnionFilter
  Risk: capital=₹100,000  max_pos=10%  risk/trade=0.5%  CB=35%
  Costs: 0.10% commission + 0.05% slippage per side
========================================================================
  Config                   Sharpe    Return    MaxDD      PF     WR  #Trades
  ----------------------------------------------------------------------  [Adaptive] ATR×2.5 + AdaptiveStrategySelector (LLM rebalance)
  Adaptive (LLM)             2.35    30.38%    7.04%    1.89  46.8%      891

========================================================================
  Period: Recov 2020–2021   (2020-04-01 → 2021-12-31)
  Universe: 150 symbols → DynamicUniverse top 80 → UnionFilter
  Risk: capital=₹100,000  max_pos=10%  risk/trade=0.5%  CB=35%
  Costs: 0.10% commission + 0.05% slippage per side
========================================================================
  Config                   Sharpe    Return    MaxDD      PF     WR  #Trades
  ----------------------------------------------------------------------  [Adaptive] ATR×2.5 + AdaptiveStrategySelector (LLM rebalance)
  Adaptive (LLM)             2.84    77.77%    8.85%    2.02  48.5%     1799

========================================================================
  Period: Bear  2022   (2022-01-01 → 2022-12-31)
  Universe: 150 symbols → DynamicUniverse top 80 → UnionFilter
  Risk: capital=₹100,000  max_pos=10%  risk/trade=0.5%  CB=35%
  Costs: 0.10% commission + 0.05% slippage per side
========================================================================
  Config                   Sharpe    Return    MaxDD      PF     WR  #Trades
  ----------------------------------------------------------------------  [Adaptive] ATR×2.5 + AdaptiveStrategySelector (LLM rebalance)
  Adaptive (LLM)             0.84     6.52%    7.91%    1.29  40.5%      615

========================================================================
  Period: Recent2022–2024   (2022-01-01 → 2024-06-01)
  Universe: 150 symbols → DynamicUniverse top 80 → UnionFilter
  Risk: capital=₹100,000  max_pos=10%  risk/trade=0.5%  CB=35%
  Costs: 0.10% commission + 0.05% slippage per side
========================================================================
  Config                   Sharpe    Return    MaxDD      PF     WR  #Trades
  ----------------------------------------------------------------------  [Adaptive] ATR×2.5 + AdaptiveStrategySelector (LLM rebalance)
  Adaptive (LLM)             1.78    46.44%    7.95%    1.59  44.9%     1767

========================================================================
  Period: Live  2025–2026   (2025-01-01 → 2026-03-24)
  Universe: 150 symbols → DynamicUniverse top 80 → UnionFilter
  Risk: capital=₹100,000  max_pos=10%  risk/trade=0.5%  CB=35%
  Costs: 0.10% commission + 0.05% slippage per side
========================================================================
  Config                   Sharpe    Return    MaxDD      PF     WR  #Trades
  ----------------------------------------------------------------------  [Adaptive] ATR×2.5 + AdaptiveStrategySelector (LLM rebalance)
  Adaptive (LLM)            -0.81    -6.05%    8.33%    0.76  36.6%      644

========================================================================
  SUMMARY — Adaptive pre-change vs post-change
  Adaptive baseline: pre-change LLM prompt results (from _ADAPTIVE_BASELINE).
  Adaptive current: this run — measures LLM prompt improvement.
  NOTE: _ADAPTIVE_BASELINE is empty — fill it after the first --adaptive run.
========================================================================

  Sharpe ratio
  Period                Adaptive baseline  Adaptive current
  ----------------------------------------------------------
  Full  2018–2024                    1.31              1.31
  Bull  2019–2020                   -0.80             -0.80
  Crash 2020                         2.35              2.35
  Recov 2020–2021                    2.84              2.84
  Bear  2022                         0.84              0.84
  Recent2022–2024                    1.78              1.78
  Live  2025–2026                   -0.81             -0.81

  Return %
  Period                Adaptive baseline  Adaptive current
  ----------------------------------------------------------
  Full  2018–2024                  110.0%            110.0%
  Bull  2019–2020                   -6.2%             -6.2%
  Crash 2020                        30.4%             30.4%
  Recov 2020–2021                   77.8%             77.8%
  Bear  2022                         6.5%              6.5%
  Recent2022–2024                   46.4%             46.4%
  Live  2025–2026                   -6.0%             -6.0%

  MaxDD %  (lower=better)
  Period                Adaptive baseline  Adaptive current
  ----------------------------------------------------------
  Full  2018–2024                   16.9%             16.9%
  Bull  2019–2020                   11.0%             11.0%
  Crash 2020                         7.0%              7.0%
  Recov 2020–2021                    8.8%              8.8%
  Bear  2022                         7.9%              7.9%
  Recent2022–2024                    7.9%              7.9%
  Live  2025–2026                    8.3%              8.3%

  Win Rate %
  Period                Adaptive baseline  Adaptive current
  ----------------------------------------------------------
  Full  2018–2024                   43.6%             43.6%
  Bull  2019–2020                   39.9%             39.9%
  Crash 2020                        46.8%             46.8%
  Recov 2020–2021                   48.5%             48.5%
  Bear  2022                        40.5%             40.5%
  Recent2022–2024                   44.9%             44.9%
  Live  2025–2026                   36.6%             36.6%

  #Trades
  Period                Adaptive baseline  Adaptive current
  ----------------------------------------------------------
  Full  2018–2024                    5207              5207
  Bull  2019–2020                     867               867
  Crash 2020                          891               891
  Recov 2020–2021                    1799              1799
  Bear  2022                          615               615
  Recent2022–2024                    1767              1767
  Live  2025–2026                     644               644

  Generated: 2026-05-11 01:10
  Mode: --adaptive (LLM)
  Config ID: f786f5cc-09f7-43b2-afbb-4f0b688f55d2 (Ujjwal's Portfolio)
========================================================================
========================================================================
```


---

## Latest Run

> Config: AdaptiveStrategySelector (gpt-4o-mini, weekly LLM rebalance).  

**Generated:** 2026-05-11 01:36  
**Mode:** --adaptive  
**Costs:** 0.10% commission + 0.05% slippage per side

```
  Mode: --adaptive (AdaptiveStrategySelector, gpt-4o-mini, rebalance every 5 days)

========================================================================
  Period: Full  2018–2024   (2018-01-01 → 2024-06-01)
  Universe: 150 symbols → DynamicUniverse top 80 → UnionFilter
  Risk: capital=₹100,000  max_pos=10%  risk/trade=0.5%  CB=35%
  Costs: 0.10% commission + 0.05% slippage per side
========================================================================
  Config                   Sharpe    Return    MaxDD      PF     WR  #Trades
  ----------------------------------------------------------------------  [Adaptive] ATR×2.5 + AdaptiveStrategySelector (LLM rebalance)
  Adaptive (LLM)             1.31   111.91%   17.78%    1.45  43.5%     5197

========================================================================
  Period: Bull  2019–2020   (2019-01-01 → 2020-02-01)
  Universe: 150 symbols → DynamicUniverse top 80 → UnionFilter
  Risk: capital=₹100,000  max_pos=10%  risk/trade=0.5%  CB=35%
  Costs: 0.10% commission + 0.05% slippage per side
========================================================================
  Config                   Sharpe    Return    MaxDD      PF     WR  #Trades
  ----------------------------------------------------------------------  [Adaptive] ATR×2.5 + AdaptiveStrategySelector (LLM rebalance)
  Adaptive (LLM)            -0.75    -6.38%   11.24%    0.77  38.5%      899

========================================================================
  Period: Crash 2020   (2020-01-01 → 2020-12-31)
  Universe: 150 symbols → DynamicUniverse top 80 → UnionFilter
  Risk: capital=₹100,000  max_pos=10%  risk/trade=0.5%  CB=35%
  Costs: 0.10% commission + 0.05% slippage per side
========================================================================
  Config                   Sharpe    Return    MaxDD      PF     WR  #Trades
  ----------------------------------------------------------------------  [Adaptive] ATR×2.5 + AdaptiveStrategySelector (LLM rebalance)
  Adaptive (LLM)             2.28    29.63%    7.02%    1.86  47.5%      885

========================================================================
  Period: Recov 2020–2021   (2020-04-01 → 2021-12-31)
  Universe: 150 symbols → DynamicUniverse top 80 → UnionFilter
  Risk: capital=₹100,000  max_pos=10%  risk/trade=0.5%  CB=35%
  Costs: 0.10% commission + 0.05% slippage per side
========================================================================
  Config                   Sharpe    Return    MaxDD      PF     WR  #Trades
  ----------------------------------------------------------------------  [Adaptive] ATR×2.5 + AdaptiveStrategySelector (LLM rebalance)
  Adaptive (LLM)             2.87    81.58%    9.36%    2.02  48.3%     1792

========================================================================
  Period: Bear  2022   (2022-01-01 → 2022-12-31)
  Universe: 150 symbols → DynamicUniverse top 80 → UnionFilter
  Risk: capital=₹100,000  max_pos=10%  risk/trade=0.5%  CB=35%
  Costs: 0.10% commission + 0.05% slippage per side
========================================================================
  Config                   Sharpe    Return    MaxDD      PF     WR  #Trades
  ----------------------------------------------------------------------  [Adaptive] ATR×2.5 + AdaptiveStrategySelector (LLM rebalance)
  Adaptive (LLM)             0.72     5.41%    7.82%    1.24  41.6%      627

========================================================================
  Period: Recent2022–2024   (2022-01-01 → 2024-06-01)
  Universe: 150 symbols → DynamicUniverse top 80 → UnionFilter
  Risk: capital=₹100,000  max_pos=10%  risk/trade=0.5%  CB=35%
  Costs: 0.10% commission + 0.05% slippage per side
========================================================================
  Config                   Sharpe    Return    MaxDD      PF     WR  #Trades
  ----------------------------------------------------------------------  [Adaptive] ATR×2.5 + AdaptiveStrategySelector (LLM rebalance)
  Adaptive (LLM)             1.70    43.30%    7.83%    1.54  45.1%     1763

========================================================================
  Period: Live  2025–2026   (2025-01-01 → 2026-03-24)
  Universe: 150 symbols → DynamicUniverse top 80 → UnionFilter
  Risk: capital=₹100,000  max_pos=10%  risk/trade=0.5%  CB=35%
  Costs: 0.10% commission + 0.05% slippage per side
========================================================================
  Config                   Sharpe    Return    MaxDD      PF     WR  #Trades
  ----------------------------------------------------------------------  [Adaptive] ATR×2.5 + AdaptiveStrategySelector (LLM rebalance)
  Adaptive (LLM)            -0.73    -5.68%    7.60%    0.78  35.9%      644

========================================================================
  SUMMARY — Adaptive pre-change vs post-change
  Adaptive baseline: pre-change LLM prompt results (from _ADAPTIVE_BASELINE).
  Adaptive current: this run — measures LLM prompt improvement.

========================================================================

  Sharpe ratio
  Period                Adaptive baseline  Adaptive current
  ----------------------------------------------------------
  Full  2018–2024                    1.31              1.31
  Bull  2019–2020                   -0.80             -0.75
  Crash 2020                         2.35              2.28
  Recov 2020–2021                    2.84              2.87
  Bear  2022                         0.84              0.72
  Recent2022–2024                    1.78              1.70
  Live  2025–2026                   -0.81             -0.73

  Return %
  Period                Adaptive baseline  Adaptive current
  ----------------------------------------------------------
  Full  2018–2024                  110.0%            111.9%
  Bull  2019–2020                   -6.2%             -6.4%
  Crash 2020                        30.4%             29.6%
  Recov 2020–2021                   77.8%             81.6%
  Bear  2022                         6.5%              5.4%
  Recent2022–2024                   46.4%             43.3%
  Live  2025–2026                   -6.0%             -5.7%

  MaxDD %  (lower=better)
  Period                Adaptive baseline  Adaptive current
  ----------------------------------------------------------
  Full  2018–2024                   16.9%             17.8%
  Bull  2019–2020                   11.0%             11.2%
  Crash 2020                         7.0%              7.0%
  Recov 2020–2021                    8.8%              9.4%
  Bear  2022                         7.9%              7.8%
  Recent2022–2024                    7.9%              7.8%
  Live  2025–2026                    8.3%              7.6%

  Win Rate %
  Period                Adaptive baseline  Adaptive current
  ----------------------------------------------------------
  Full  2018–2024                   43.6%             43.5%
  Bull  2019–2020                   39.9%             38.5%
  Crash 2020                        46.8%             47.5%
  Recov 2020–2021                   48.5%             48.3%
  Bear  2022                        40.5%             41.6%
  Recent2022–2024                   44.9%             45.1%
  Live  2025–2026                   36.6%             35.9%

  #Trades
  Period                Adaptive baseline  Adaptive current
  ----------------------------------------------------------
  Full  2018–2024                    5207              5197
  Bull  2019–2020                     867               899
  Crash 2020                          891               885
  Recov 2020–2021                    1799              1792
  Bear  2022                          615               627
  Recent2022–2024                    1767              1763
  Live  2025–2026                     644               644

  Generated: 2026-05-11 01:36
  Mode: --adaptive (LLM)
  Config ID: f786f5cc-09f7-43b2-afbb-4f0b688f55d2 (Ujjwal's Portfolio)
========================================================================
========================================================================
```


---

## Latest Run

> Config: ATR×2.5 trailing stop + volume filter (vol_ratio>1.2).  

**Generated:** 2026-05-11 01:36  
**Mode:** EqualWeight  
**Costs:** 0.10% commission + 0.05% slippage per side

```
  Mode: --adaptive (AdaptiveStrategySelector, gpt-4o-mini, rebalance every 5 days)

========================================================================
  Period: Full  2018–2024   (2018-01-01 → 2024-06-01)
  Universe: 150 symbols → DynamicUniverse top 80 → UnionFilter
  Risk: capital=₹100,000  max_pos=10%  risk/trade=0.5%  CB=35%
  Costs: 0.10% commission + 0.05% slippage per side
========================================================================
  Config                   Sharpe    Return    MaxDD      PF     WR  #Trades
  ----------------------------------------------------------------------  [Adaptive] ATR×2.5 + AdaptiveStrategySelector (LLM rebalance)
  Adaptive (LLM)             1.31   111.91%   17.78%    1.45  43.5%     5197

========================================================================
  Period: Bull  2019–2020   (2019-01-01 → 2020-02-01)
  Universe: 150 symbols → DynamicUniverse top 80 → UnionFilter
  Risk: capital=₹100,000  max_pos=10%  risk/trade=0.5%  CB=35%
  Costs: 0.10% commission + 0.05% slippage per side
========================================================================
  Config                   Sharpe    Return    MaxDD      PF     WR  #Trades
  ----------------------------------------------------------------------  [Adaptive] ATR×2.5 + AdaptiveStrategySelector (LLM rebalance)
  Adaptive (LLM)            -0.75    -6.38%   11.24%    0.77  38.5%      899

========================================================================
  Period: Crash 2020   (2020-01-01 → 2020-12-31)
  Universe: 150 symbols → DynamicUniverse top 80 → UnionFilter
  Risk: capital=₹100,000  max_pos=10%  risk/trade=0.5%  CB=35%
  Costs: 0.10% commission + 0.05% slippage per side
========================================================================
  Config                   Sharpe    Return    MaxDD      PF     WR  #Trades
  ----------------------------------------------------------------------  [Adaptive] ATR×2.5 + AdaptiveStrategySelector (LLM rebalance)
  Adaptive (LLM)             2.28    29.63%    7.02%    1.86  47.5%      885

========================================================================
  Period: Recov 2020–2021   (2020-04-01 → 2021-12-31)
  Universe: 150 symbols → DynamicUniverse top 80 → UnionFilter
  Risk: capital=₹100,000  max_pos=10%  risk/trade=0.5%  CB=35%
  Costs: 0.10% commission + 0.05% slippage per side
========================================================================
  Config                   Sharpe    Return    MaxDD      PF     WR  #Trades
  ----------------------------------------------------------------------  [Adaptive] ATR×2.5 + AdaptiveStrategySelector (LLM rebalance)
  Adaptive (LLM)             2.87    81.58%    9.36%    2.02  48.3%     1792

========================================================================
  Period: Bear  2022   (2022-01-01 → 2022-12-31)
  Universe: 150 symbols → DynamicUniverse top 80 → UnionFilter
  Risk: capital=₹100,000  max_pos=10%  risk/trade=0.5%  CB=35%
  Costs: 0.10% commission + 0.05% slippage per side
========================================================================
  Config                   Sharpe    Return    MaxDD      PF     WR  #Trades
  ----------------------------------------------------------------------  [Adaptive] ATR×2.5 + AdaptiveStrategySelector (LLM rebalance)
  Adaptive (LLM)             0.72     5.41%    7.82%    1.24  41.6%      627

========================================================================
  Period: Recent2022–2024   (2022-01-01 → 2024-06-01)
  Universe: 150 symbols → DynamicUniverse top 80 → UnionFilter
  Risk: capital=₹100,000  max_pos=10%  risk/trade=0.5%  CB=35%
  Costs: 0.10% commission + 0.05% slippage per side
========================================================================
  Config                   Sharpe    Return    MaxDD      PF     WR  #Trades
  ----------------------------------------------------------------------  [Adaptive] ATR×2.5 + AdaptiveStrategySelector (LLM rebalance)
  Adaptive (LLM)             1.70    43.30%    7.83%    1.54  45.1%     1763

========================================================================
  Period: Live  2025–2026   (2025-01-01 → 2026-03-24)
  Universe: 150 symbols → DynamicUniverse top 80 → UnionFilter
  Risk: capital=₹100,000  max_pos=10%  risk/trade=0.5%  CB=35%
  Costs: 0.10% commission + 0.05% slippage per side
========================================================================
  Config                   Sharpe    Return    MaxDD      PF     WR  #Trades
  ----------------------------------------------------------------------  [Adaptive] ATR×2.5 + AdaptiveStrategySelector (LLM rebalance)
  Adaptive (LLM)            -0.73    -5.68%    7.60%    0.78  35.9%      644

========================================================================
  SUMMARY — Adaptive pre-change vs post-change
  Adaptive baseline: pre-change LLM prompt results (from _ADAPTIVE_BASELINE).
  Adaptive current: this run — measures LLM prompt improvement.

========================================================================

  Sharpe ratio
  Period                Adaptive baseline  Adaptive current
  ----------------------------------------------------------
  Full  2018–2024                    1.31              1.31
  Bull  2019–2020                   -0.80             -0.75
  Crash 2020                         2.35              2.28
  Recov 2020–2021                    2.84              2.87
  Bear  2022                         0.84              0.72
  Recent2022–2024                    1.78              1.70
  Live  2025–2026                   -0.81             -0.73

  Return %
  Period                Adaptive baseline  Adaptive current
  ----------------------------------------------------------
  Full  2018–2024                  110.0%            111.9%
  Bull  2019–2020                   -6.2%             -6.4%
  Crash 2020                        30.4%             29.6%
  Recov 2020–2021                   77.8%             81.6%
  Bear  2022                         6.5%              5.4%
  Recent2022–2024                   46.4%             43.3%
  Live  2025–2026                   -6.0%             -5.7%

  MaxDD %  (lower=better)
  Period                Adaptive baseline  Adaptive current
  ----------------------------------------------------------
  Full  2018–2024                   16.9%             17.8%
  Bull  2019–2020                   11.0%             11.2%
  Crash 2020                         7.0%              7.0%
  Recov 2020–2021                    8.8%              9.4%
  Bear  2022                         7.9%              7.8%
  Recent2022–2024                    7.9%              7.8%
  Live  2025–2026                    8.3%              7.6%

  Win Rate %
  Period                Adaptive baseline  Adaptive current
  ----------------------------------------------------------
  Full  2018–2024                   43.6%             43.5%
  Bull  2019–2020                   39.9%             38.5%
  Crash 2020                        46.8%             47.5%
  Recov 2020–2021                   48.5%             48.3%
  Bear  2022                        40.5%             41.6%
  Recent2022–2024                   44.9%             45.1%
  Live  2025–2026                   36.6%             35.9%

  #Trades
  Period                Adaptive baseline  Adaptive current
  ----------------------------------------------------------
  Full  2018–2024                    5207              5197
  Bull  2019–2020                     867               899
  Crash 2020                          891               885
  Recov 2020–2021                    1799              1792
  Bear  2022                          615               627
  Recent2022–2024                    1767              1763
  Live  2025–2026                     644               644

  Generated: 2026-05-11 01:36
  Mode: --adaptive (LLM)
  Config ID: f786f5cc-09f7-43b2-afbb-4f0b688f55d2 (Ujjwal's Portfolio)
========================================================================
========================================================================
```


---

## Latest Run

> Config: AdaptiveStrategySelector (gpt-4o-mini, weekly LLM rebalance).  

**Generated:** 2026-05-12 18:31  
**Mode:** --adaptive  
**Costs:** 0.10% commission + 0.05% slippage per side

```
  Mode: --adaptive (AdaptiveStrategySelector, gpt-4o-mini, rebalance every 5 days)

========================================================================
  Period: Full  2018–2024   (2018-01-01 → 2024-06-01)
  Universe: 150 symbols → DynamicUniverse top 80 → UnionFilter
  Risk: capital=₹100,000  max_pos=10%  risk/trade=0.5%  CB=35%
  Costs: 0.10% commission + 0.05% slippage per side
========================================================================
  Config                   Sharpe    Return    MaxDD      PF     WR  #Trades
  ----------------------------------------------------------------------  [Adaptive] ATR×2.5 + AdaptiveStrategySelector (LLM rebalance)
  Adaptive (LLM)             1.36   116.62%   17.11%    1.47  44.1%     5191

========================================================================
  Period: Bull  2019–2020   (2019-01-01 → 2020-02-01)
  Universe: 150 symbols → DynamicUniverse top 80 → UnionFilter
  Risk: capital=₹100,000  max_pos=10%  risk/trade=0.5%  CB=35%
  Costs: 0.10% commission + 0.05% slippage per side
========================================================================
  Config                   Sharpe    Return    MaxDD      PF     WR  #Trades
  ----------------------------------------------------------------------  [Adaptive] ATR×2.5 + AdaptiveStrategySelector (LLM rebalance)
  Adaptive (LLM)            -0.71    -5.79%   10.73%    0.77  39.4%      886

========================================================================
  Period: Crash 2020   (2020-01-01 → 2020-12-31)
  Universe: 150 symbols → DynamicUniverse top 80 → UnionFilter
  Risk: capital=₹100,000  max_pos=10%  risk/trade=0.5%  CB=35%
  Costs: 0.10% commission + 0.05% slippage per side
========================================================================
  Config                   Sharpe    Return    MaxDD      PF     WR  #Trades
  ----------------------------------------------------------------------  [Adaptive] ATR×2.5 + AdaptiveStrategySelector (LLM rebalance)
  Adaptive (LLM)             2.32    29.68%    7.51%    1.85  47.3%      903

========================================================================
  Period: Recov 2020–2021   (2020-04-01 → 2021-12-31)
  Universe: 150 symbols → DynamicUniverse top 80 → UnionFilter
  Risk: capital=₹100,000  max_pos=10%  risk/trade=0.5%  CB=35%
  Costs: 0.10% commission + 0.05% slippage per side
========================================================================
  Config                   Sharpe    Return    MaxDD      PF     WR  #Trades
  ----------------------------------------------------------------------  [Adaptive] ATR×2.5 + AdaptiveStrategySelector (LLM rebalance)
  Adaptive (LLM)             2.88    80.27%    9.01%    2.02  49.2%     1785

========================================================================
  Period: Bear  2022   (2022-01-01 → 2022-12-31)
  Universe: 150 symbols → DynamicUniverse top 80 → UnionFilter
  Risk: capital=₹100,000  max_pos=10%  risk/trade=0.5%  CB=35%
  Costs: 0.10% commission + 0.05% slippage per side
========================================================================
  Config                   Sharpe    Return    MaxDD      PF     WR  #Trades
  ----------------------------------------------------------------------  [Adaptive] ATR×2.5 + AdaptiveStrategySelector (LLM rebalance)
  Adaptive (LLM)             0.85     6.45%    7.87%    1.29  41.5%      621

========================================================================
  Period: Recent2022–2024   (2022-01-01 → 2024-06-01)
  Universe: 150 symbols → DynamicUniverse top 80 → UnionFilter
  Risk: capital=₹100,000  max_pos=10%  risk/trade=0.5%  CB=35%
  Costs: 0.10% commission + 0.05% slippage per side
========================================================================
  Config                   Sharpe    Return    MaxDD      PF     WR  #Trades
  ----------------------------------------------------------------------  [Adaptive] ATR×2.5 + AdaptiveStrategySelector (LLM rebalance)
  Adaptive (LLM)             1.57    38.91%    7.80%    1.47  43.9%     1753

========================================================================
  Period: Live  2025–2026   (2025-01-01 → 2026-03-24)
  Universe: 150 symbols → DynamicUniverse top 80 → UnionFilter
  Risk: capital=₹100,000  max_pos=10%  risk/trade=0.5%  CB=35%
  Costs: 0.10% commission + 0.05% slippage per side
========================================================================
  Config                   Sharpe    Return    MaxDD      PF     WR  #Trades
  ----------------------------------------------------------------------  [Adaptive] ATR×2.5 + AdaptiveStrategySelector (LLM rebalance)
  Adaptive (LLM)            -0.77    -5.93%    8.06%    0.77  36.4%      635

========================================================================
  SUMMARY — Adaptive pre-change vs post-change
  Adaptive baseline: pre-change LLM prompt results (from _ADAPTIVE_BASELINE).
  Adaptive current: this run — measures LLM prompt improvement.

========================================================================

  Sharpe ratio
  Period                Adaptive baseline  Adaptive current
  ----------------------------------------------------------
  Full  2018–2024                    1.31              1.36
  Bull  2019–2020                   -0.80             -0.71
  Crash 2020                         2.35              2.32
  Recov 2020–2021                    2.84              2.88
  Bear  2022                         0.84              0.85
  Recent2022–2024                    1.78              1.57
  Live  2025–2026                   -0.81             -0.77

  Return %
  Period                Adaptive baseline  Adaptive current
  ----------------------------------------------------------
  Full  2018–2024                  110.0%            116.6%
  Bull  2019–2020                   -6.2%             -5.8%
  Crash 2020                        30.4%             29.7%
  Recov 2020–2021                   77.8%             80.3%
  Bear  2022                         6.5%              6.5%
  Recent2022–2024                   46.4%             38.9%
  Live  2025–2026                   -6.0%             -5.9%

  MaxDD %  (lower=better)
  Period                Adaptive baseline  Adaptive current
  ----------------------------------------------------------
  Full  2018–2024                   16.9%             17.1%
  Bull  2019–2020                   11.0%             10.7%
  Crash 2020                         7.0%              7.5%
  Recov 2020–2021                    8.8%              9.0%
  Bear  2022                         7.9%              7.9%
  Recent2022–2024                    7.9%              7.8%
  Live  2025–2026                    8.3%              8.1%

  Win Rate %
  Period                Adaptive baseline  Adaptive current
  ----------------------------------------------------------
  Full  2018–2024                   43.6%             44.1%
  Bull  2019–2020                   39.9%             39.4%
  Crash 2020                        46.8%             47.3%
  Recov 2020–2021                   48.5%             49.2%
  Bear  2022                        40.5%             41.5%
  Recent2022–2024                   44.9%             43.9%
  Live  2025–2026                   36.6%             36.4%

  #Trades
  Period                Adaptive baseline  Adaptive current
  ----------------------------------------------------------
  Full  2018–2024                    5207              5191
  Bull  2019–2020                     867               886
  Crash 2020                          891               903
  Recov 2020–2021                    1799              1785
  Bear  2022                          615               621
  Recent2022–2024                    1767              1753
  Live  2025–2026                     644               635

  Generated: 2026-05-12 18:31
  Mode: --adaptive (LLM)
  Config ID: f786f5cc-09f7-43b2-afbb-4f0b688f55d2 (Ujjwal's Portfolio)
========================================================================
========================================================================
```


---

## Latest Run

> Config: ATR×2.5 trailing stop + volume filter (vol_ratio>1.2).  

**Generated:** 2026-05-12 18:31  
**Mode:** EqualWeight  
**Costs:** 0.10% commission + 0.05% slippage per side

```
  Mode: --adaptive (AdaptiveStrategySelector, gpt-4o-mini, rebalance every 5 days)

========================================================================
  Period: Full  2018–2024   (2018-01-01 → 2024-06-01)
  Universe: 150 symbols → DynamicUniverse top 80 → UnionFilter
  Risk: capital=₹100,000  max_pos=10%  risk/trade=0.5%  CB=35%
  Costs: 0.10% commission + 0.05% slippage per side
========================================================================
  Config                   Sharpe    Return    MaxDD      PF     WR  #Trades
  ----------------------------------------------------------------------  [Adaptive] ATR×2.5 + AdaptiveStrategySelector (LLM rebalance)
  Adaptive (LLM)             1.36   116.62%   17.11%    1.47  44.1%     5191

========================================================================
  Period: Bull  2019–2020   (2019-01-01 → 2020-02-01)
  Universe: 150 symbols → DynamicUniverse top 80 → UnionFilter
  Risk: capital=₹100,000  max_pos=10%  risk/trade=0.5%  CB=35%
  Costs: 0.10% commission + 0.05% slippage per side
========================================================================
  Config                   Sharpe    Return    MaxDD      PF     WR  #Trades
  ----------------------------------------------------------------------  [Adaptive] ATR×2.5 + AdaptiveStrategySelector (LLM rebalance)
  Adaptive (LLM)            -0.71    -5.79%   10.73%    0.77  39.4%      886

========================================================================
  Period: Crash 2020   (2020-01-01 → 2020-12-31)
  Universe: 150 symbols → DynamicUniverse top 80 → UnionFilter
  Risk: capital=₹100,000  max_pos=10%  risk/trade=0.5%  CB=35%
  Costs: 0.10% commission + 0.05% slippage per side
========================================================================
  Config                   Sharpe    Return    MaxDD      PF     WR  #Trades
  ----------------------------------------------------------------------  [Adaptive] ATR×2.5 + AdaptiveStrategySelector (LLM rebalance)
  Adaptive (LLM)             2.32    29.68%    7.51%    1.85  47.3%      903

========================================================================
  Period: Recov 2020–2021   (2020-04-01 → 2021-12-31)
  Universe: 150 symbols → DynamicUniverse top 80 → UnionFilter
  Risk: capital=₹100,000  max_pos=10%  risk/trade=0.5%  CB=35%
  Costs: 0.10% commission + 0.05% slippage per side
========================================================================
  Config                   Sharpe    Return    MaxDD      PF     WR  #Trades
  ----------------------------------------------------------------------  [Adaptive] ATR×2.5 + AdaptiveStrategySelector (LLM rebalance)
  Adaptive (LLM)             2.88    80.27%    9.01%    2.02  49.2%     1785

========================================================================
  Period: Bear  2022   (2022-01-01 → 2022-12-31)
  Universe: 150 symbols → DynamicUniverse top 80 → UnionFilter
  Risk: capital=₹100,000  max_pos=10%  risk/trade=0.5%  CB=35%
  Costs: 0.10% commission + 0.05% slippage per side
========================================================================
  Config                   Sharpe    Return    MaxDD      PF     WR  #Trades
  ----------------------------------------------------------------------  [Adaptive] ATR×2.5 + AdaptiveStrategySelector (LLM rebalance)
  Adaptive (LLM)             0.85     6.45%    7.87%    1.29  41.5%      621

========================================================================
  Period: Recent2022–2024   (2022-01-01 → 2024-06-01)
  Universe: 150 symbols → DynamicUniverse top 80 → UnionFilter
  Risk: capital=₹100,000  max_pos=10%  risk/trade=0.5%  CB=35%
  Costs: 0.10% commission + 0.05% slippage per side
========================================================================
  Config                   Sharpe    Return    MaxDD      PF     WR  #Trades
  ----------------------------------------------------------------------  [Adaptive] ATR×2.5 + AdaptiveStrategySelector (LLM rebalance)
  Adaptive (LLM)             1.57    38.91%    7.80%    1.47  43.9%     1753

========================================================================
  Period: Live  2025–2026   (2025-01-01 → 2026-03-24)
  Universe: 150 symbols → DynamicUniverse top 80 → UnionFilter
  Risk: capital=₹100,000  max_pos=10%  risk/trade=0.5%  CB=35%
  Costs: 0.10% commission + 0.05% slippage per side
========================================================================
  Config                   Sharpe    Return    MaxDD      PF     WR  #Trades
  ----------------------------------------------------------------------  [Adaptive] ATR×2.5 + AdaptiveStrategySelector (LLM rebalance)
  Adaptive (LLM)            -0.77    -5.93%    8.06%    0.77  36.4%      635

========================================================================
  SUMMARY — Adaptive pre-change vs post-change
  Adaptive baseline: pre-change LLM prompt results (from _ADAPTIVE_BASELINE).
  Adaptive current: this run — measures LLM prompt improvement.

========================================================================

  Sharpe ratio
  Period                Adaptive baseline  Adaptive current
  ----------------------------------------------------------
  Full  2018–2024                    1.31              1.36
  Bull  2019–2020                   -0.80             -0.71
  Crash 2020                         2.35              2.32
  Recov 2020–2021                    2.84              2.88
  Bear  2022                         0.84              0.85
  Recent2022–2024                    1.78              1.57
  Live  2025–2026                   -0.81             -0.77

  Return %
  Period                Adaptive baseline  Adaptive current
  ----------------------------------------------------------
  Full  2018–2024                  110.0%            116.6%
  Bull  2019–2020                   -6.2%             -5.8%
  Crash 2020                        30.4%             29.7%
  Recov 2020–2021                   77.8%             80.3%
  Bear  2022                         6.5%              6.5%
  Recent2022–2024                   46.4%             38.9%
  Live  2025–2026                   -6.0%             -5.9%

  MaxDD %  (lower=better)
  Period                Adaptive baseline  Adaptive current
  ----------------------------------------------------------
  Full  2018–2024                   16.9%             17.1%
  Bull  2019–2020                   11.0%             10.7%
  Crash 2020                         7.0%              7.5%
  Recov 2020–2021                    8.8%              9.0%
  Bear  2022                         7.9%              7.9%
  Recent2022–2024                    7.9%              7.8%
  Live  2025–2026                    8.3%              8.1%

  Win Rate %
  Period                Adaptive baseline  Adaptive current
  ----------------------------------------------------------
  Full  2018–2024                   43.6%             44.1%
  Bull  2019–2020                   39.9%             39.4%
  Crash 2020                        46.8%             47.3%
  Recov 2020–2021                   48.5%             49.2%
  Bear  2022                        40.5%             41.5%
  Recent2022–2024                   44.9%             43.9%
  Live  2025–2026                   36.6%             36.4%

  #Trades
  Period                Adaptive baseline  Adaptive current
  ----------------------------------------------------------
  Full  2018–2024                    5207              5191
  Bull  2019–2020                     867               886
  Crash 2020                          891               903
  Recov 2020–2021                    1799              1785
  Bear  2022                          615               621
  Recent2022–2024                    1767              1753
  Live  2025–2026                     644               635

  Generated: 2026-05-12 18:31
  Mode: --adaptive (LLM)
  Config ID: f786f5cc-09f7-43b2-afbb-4f0b688f55d2 (Ujjwal's Portfolio)
========================================================================
========================================================================
```


---

## Latest Run

> Config: AdaptiveStrategySelector (gpt-4o-mini, weekly LLM rebalance).  

**Generated:** 2026-05-13 01:22  
**Mode:** --adaptive  
**Costs:** 0.10% commission + 0.05% slippage per side

```
  Mode: --adaptive (AdaptiveStrategySelector, gpt-4o-mini, rebalance every 5 days)

========================================================================
  Period: Full  2018–2024   (2018-01-01 → 2024-06-01)
  Universe: 150 symbols → DynamicUniverse top 80 → UnionFilter
  Risk: capital=₹100,000  max_pos=10%  risk/trade=0.5%  CB=35%
  Costs: 0.10% commission + 0.05% slippage per side
========================================================================
  Config                   Sharpe    Return    MaxDD      PF     WR  #Trades
  ----------------------------------------------------------------------  [Adaptive] ATR×2.5 + AdaptiveStrategySelector (LLM rebalance)
  Adaptive (LLM)             1.29   109.44%   16.71%    1.43  43.5%     5020

========================================================================
  Period: Bull  2019–2020   (2019-01-01 → 2020-02-01)
  Universe: 150 symbols → DynamicUniverse top 80 → UnionFilter
  Risk: capital=₹100,000  max_pos=10%  risk/trade=0.5%  CB=35%
  Costs: 0.10% commission + 0.05% slippage per side
========================================================================
  Config                   Sharpe    Return    MaxDD      PF     WR  #Trades
  ----------------------------------------------------------------------  [Adaptive] ATR×2.5 + AdaptiveStrategySelector (LLM rebalance)
  Adaptive (LLM)            -0.93    -6.88%   10.78%    0.72  39.4%      852

========================================================================
  Period: Crash 2020   (2020-01-01 → 2020-12-31)
  Universe: 150 symbols → DynamicUniverse top 80 → UnionFilter
  Risk: capital=₹100,000  max_pos=10%  risk/trade=0.5%  CB=35%
  Costs: 0.10% commission + 0.05% slippage per side
========================================================================
  Config                   Sharpe    Return    MaxDD      PF     WR  #Trades
  ----------------------------------------------------------------------  [Adaptive] ATR×2.5 + AdaptiveStrategySelector (LLM rebalance)
  Adaptive (LLM)             2.26    29.21%    7.84%    1.85  47.3%      867

========================================================================
  Period: Recov 2020–2021   (2020-04-01 → 2021-12-31)
  Universe: 150 symbols → DynamicUniverse top 80 → UnionFilter
  Risk: capital=₹100,000  max_pos=10%  risk/trade=0.5%  CB=35%
  Costs: 0.10% commission + 0.05% slippage per side
========================================================================
  Config                   Sharpe    Return    MaxDD      PF     WR  #Trades
  ----------------------------------------------------------------------  [Adaptive] ATR×2.5 + AdaptiveStrategySelector (LLM rebalance)
  Adaptive (LLM)             2.94    84.29%    8.21%    2.08  48.9%     1730

========================================================================
  Period: Bear  2022   (2022-01-01 → 2022-12-31)
  Universe: 150 symbols → DynamicUniverse top 80 → UnionFilter
  Risk: capital=₹100,000  max_pos=10%  risk/trade=0.5%  CB=35%
  Costs: 0.10% commission + 0.05% slippage per side
========================================================================
  Config                   Sharpe    Return    MaxDD      PF     WR  #Trades
  ----------------------------------------------------------------------  [Adaptive] ATR×2.5 + AdaptiveStrategySelector (LLM rebalance)
  Adaptive (LLM)             0.83     6.27%    7.54%    1.27  42.6%      594

========================================================================
  Period: Recent2022–2024   (2022-01-01 → 2024-06-01)
  Universe: 150 symbols → DynamicUniverse top 80 → UnionFilter
  Risk: capital=₹100,000  max_pos=10%  risk/trade=0.5%  CB=35%
  Costs: 0.10% commission + 0.05% slippage per side
========================================================================
  Config                   Sharpe    Return    MaxDD      PF     WR  #Trades
  ----------------------------------------------------------------------  [Adaptive] ATR×2.5 + AdaptiveStrategySelector (LLM rebalance)
  Adaptive (LLM)             1.57    39.37%    7.50%    1.48  44.2%     1694

========================================================================
  Period: Live  2025–2026   (2025-01-01 → 2026-03-24)
  Universe: 150 symbols → DynamicUniverse top 80 → UnionFilter
  Risk: capital=₹100,000  max_pos=10%  risk/trade=0.5%  CB=35%
  Costs: 0.10% commission + 0.05% slippage per side
========================================================================
  Config                   Sharpe    Return    MaxDD      PF     WR  #Trades
  ----------------------------------------------------------------------  [Adaptive] ATR×2.5 + AdaptiveStrategySelector (LLM rebalance)
  Adaptive (LLM)            -0.86    -6.42%    8.74%    0.75  35.9%      621

========================================================================
  SUMMARY — Adaptive pre-change vs post-change
  Adaptive baseline: pre-change LLM prompt results (from _ADAPTIVE_BASELINE).
  Adaptive current: this run — measures LLM prompt improvement.

========================================================================

  Sharpe ratio
  Period                Adaptive baseline  Adaptive current
  ----------------------------------------------------------
  Full  2018–2024                    1.36              1.29
  Bull  2019–2020                   -0.71             -0.93
  Crash 2020                         2.32              2.26
  Recov 2020–2021                    2.88              2.94
  Bear  2022                         0.85              0.83
  Recent2022–2024                    1.57              1.57
  Live  2025–2026                   -0.77             -0.86

  Return %
  Period                Adaptive baseline  Adaptive current
  ----------------------------------------------------------
  Full  2018–2024                  116.6%            109.4%
  Bull  2019–2020                   -5.8%             -6.9%
  Crash 2020                        29.7%             29.2%
  Recov 2020–2021                   80.3%             84.3%
  Bear  2022                         6.5%              6.3%
  Recent2022–2024                   38.9%             39.4%
  Live  2025–2026                   -5.9%             -6.4%

  MaxDD %  (lower=better)
  Period                Adaptive baseline  Adaptive current
  ----------------------------------------------------------
  Full  2018–2024                   17.1%             16.7%
  Bull  2019–2020                   10.7%             10.8%
  Crash 2020                         7.5%              7.8%
  Recov 2020–2021                    9.0%              8.2%
  Bear  2022                         7.9%              7.5%
  Recent2022–2024                    7.8%              7.5%
  Live  2025–2026                    8.1%              8.7%

  Win Rate %
  Period                Adaptive baseline  Adaptive current
  ----------------------------------------------------------
  Full  2018–2024                   44.1%             43.5%
  Bull  2019–2020                   39.4%             39.4%
  Crash 2020                        47.3%             47.3%
  Recov 2020–2021                   49.2%             48.9%
  Bear  2022                        41.5%             42.6%
  Recent2022–2024                   43.9%             44.2%
  Live  2025–2026                   36.4%             35.9%

  #Trades
  Period                Adaptive baseline  Adaptive current
  ----------------------------------------------------------
  Full  2018–2024                    5191              5020
  Bull  2019–2020                     886               852
  Crash 2020                          903               867
  Recov 2020–2021                    1785              1730
  Bear  2022                          621               594
  Recent2022–2024                    1753              1694
  Live  2025–2026                     635               621

  Generated: 2026-05-13 01:22
  Mode: --adaptive (LLM)
  Config ID: f786f5cc-09f7-43b2-afbb-4f0b688f55d2 (Ujjwal's Portfolio)
========================================================================
========================================================================
```


---

## Latest Run

> Config: ATR×2.5 trailing stop + volume filter (vol_ratio>1.2).  

**Generated:** 2026-05-13 01:22  
**Mode:** EqualWeight  
**Costs:** 0.10% commission + 0.05% slippage per side

```
  Mode: --adaptive (AdaptiveStrategySelector, gpt-4o-mini, rebalance every 5 days)

========================================================================
  Period: Full  2018–2024   (2018-01-01 → 2024-06-01)
  Universe: 150 symbols → DynamicUniverse top 80 → UnionFilter
  Risk: capital=₹100,000  max_pos=10%  risk/trade=0.5%  CB=35%
  Costs: 0.10% commission + 0.05% slippage per side
========================================================================
  Config                   Sharpe    Return    MaxDD      PF     WR  #Trades
  ----------------------------------------------------------------------  [Adaptive] ATR×2.5 + AdaptiveStrategySelector (LLM rebalance)
  Adaptive (LLM)             1.29   109.44%   16.71%    1.43  43.5%     5020

========================================================================
  Period: Bull  2019–2020   (2019-01-01 → 2020-02-01)
  Universe: 150 symbols → DynamicUniverse top 80 → UnionFilter
  Risk: capital=₹100,000  max_pos=10%  risk/trade=0.5%  CB=35%
  Costs: 0.10% commission + 0.05% slippage per side
========================================================================
  Config                   Sharpe    Return    MaxDD      PF     WR  #Trades
  ----------------------------------------------------------------------  [Adaptive] ATR×2.5 + AdaptiveStrategySelector (LLM rebalance)
  Adaptive (LLM)            -0.93    -6.88%   10.78%    0.72  39.4%      852

========================================================================
  Period: Crash 2020   (2020-01-01 → 2020-12-31)
  Universe: 150 symbols → DynamicUniverse top 80 → UnionFilter
  Risk: capital=₹100,000  max_pos=10%  risk/trade=0.5%  CB=35%
  Costs: 0.10% commission + 0.05% slippage per side
========================================================================
  Config                   Sharpe    Return    MaxDD      PF     WR  #Trades
  ----------------------------------------------------------------------  [Adaptive] ATR×2.5 + AdaptiveStrategySelector (LLM rebalance)
  Adaptive (LLM)             2.26    29.21%    7.84%    1.85  47.3%      867

========================================================================
  Period: Recov 2020–2021   (2020-04-01 → 2021-12-31)
  Universe: 150 symbols → DynamicUniverse top 80 → UnionFilter
  Risk: capital=₹100,000  max_pos=10%  risk/trade=0.5%  CB=35%
  Costs: 0.10% commission + 0.05% slippage per side
========================================================================
  Config                   Sharpe    Return    MaxDD      PF     WR  #Trades
  ----------------------------------------------------------------------  [Adaptive] ATR×2.5 + AdaptiveStrategySelector (LLM rebalance)
  Adaptive (LLM)             2.94    84.29%    8.21%    2.08  48.9%     1730

========================================================================
  Period: Bear  2022   (2022-01-01 → 2022-12-31)
  Universe: 150 symbols → DynamicUniverse top 80 → UnionFilter
  Risk: capital=₹100,000  max_pos=10%  risk/trade=0.5%  CB=35%
  Costs: 0.10% commission + 0.05% slippage per side
========================================================================
  Config                   Sharpe    Return    MaxDD      PF     WR  #Trades
  ----------------------------------------------------------------------  [Adaptive] ATR×2.5 + AdaptiveStrategySelector (LLM rebalance)
  Adaptive (LLM)             0.83     6.27%    7.54%    1.27  42.6%      594

========================================================================
  Period: Recent2022–2024   (2022-01-01 → 2024-06-01)
  Universe: 150 symbols → DynamicUniverse top 80 → UnionFilter
  Risk: capital=₹100,000  max_pos=10%  risk/trade=0.5%  CB=35%
  Costs: 0.10% commission + 0.05% slippage per side
========================================================================
  Config                   Sharpe    Return    MaxDD      PF     WR  #Trades
  ----------------------------------------------------------------------  [Adaptive] ATR×2.5 + AdaptiveStrategySelector (LLM rebalance)
  Adaptive (LLM)             1.57    39.37%    7.50%    1.48  44.2%     1694

========================================================================
  Period: Live  2025–2026   (2025-01-01 → 2026-03-24)
  Universe: 150 symbols → DynamicUniverse top 80 → UnionFilter
  Risk: capital=₹100,000  max_pos=10%  risk/trade=0.5%  CB=35%
  Costs: 0.10% commission + 0.05% slippage per side
========================================================================
  Config                   Sharpe    Return    MaxDD      PF     WR  #Trades
  ----------------------------------------------------------------------  [Adaptive] ATR×2.5 + AdaptiveStrategySelector (LLM rebalance)
  Adaptive (LLM)            -0.86    -6.42%    8.74%    0.75  35.9%      621

========================================================================
  SUMMARY — Adaptive pre-change vs post-change
  Adaptive baseline: pre-change LLM prompt results (from _ADAPTIVE_BASELINE).
  Adaptive current: this run — measures LLM prompt improvement.

========================================================================

  Sharpe ratio
  Period                Adaptive baseline  Adaptive current
  ----------------------------------------------------------
  Full  2018–2024                    1.36              1.29
  Bull  2019–2020                   -0.71             -0.93
  Crash 2020                         2.32              2.26
  Recov 2020–2021                    2.88              2.94
  Bear  2022                         0.85              0.83
  Recent2022–2024                    1.57              1.57
  Live  2025–2026                   -0.77             -0.86

  Return %
  Period                Adaptive baseline  Adaptive current
  ----------------------------------------------------------
  Full  2018–2024                  116.6%            109.4%
  Bull  2019–2020                   -5.8%             -6.9%
  Crash 2020                        29.7%             29.2%
  Recov 2020–2021                   80.3%             84.3%
  Bear  2022                         6.5%              6.3%
  Recent2022–2024                   38.9%             39.4%
  Live  2025–2026                   -5.9%             -6.4%

  MaxDD %  (lower=better)
  Period                Adaptive baseline  Adaptive current
  ----------------------------------------------------------
  Full  2018–2024                   17.1%             16.7%
  Bull  2019–2020                   10.7%             10.8%
  Crash 2020                         7.5%              7.8%
  Recov 2020–2021                    9.0%              8.2%
  Bear  2022                         7.9%              7.5%
  Recent2022–2024                    7.8%              7.5%
  Live  2025–2026                    8.1%              8.7%

  Win Rate %
  Period                Adaptive baseline  Adaptive current
  ----------------------------------------------------------
  Full  2018–2024                   44.1%             43.5%
  Bull  2019–2020                   39.4%             39.4%
  Crash 2020                        47.3%             47.3%
  Recov 2020–2021                   49.2%             48.9%
  Bear  2022                        41.5%             42.6%
  Recent2022–2024                   43.9%             44.2%
  Live  2025–2026                   36.4%             35.9%

  #Trades
  Period                Adaptive baseline  Adaptive current
  ----------------------------------------------------------
  Full  2018–2024                    5191              5020
  Bull  2019–2020                     886               852
  Crash 2020                          903               867
  Recov 2020–2021                    1785              1730
  Bear  2022                          621               594
  Recent2022–2024                    1753              1694
  Live  2025–2026                     635               621

  Generated: 2026-05-13 01:22
  Mode: --adaptive (LLM)
  Config ID: f786f5cc-09f7-43b2-afbb-4f0b688f55d2 (Ujjwal's Portfolio)
========================================================================
========================================================================
```


---

## Latest Run

> Config: ATR×2.5 trailing stop + volume filter (vol_ratio>1.2).  

**Generated:** 2026-05-16 20:28  
**Mode:** EqualWeight  
**Costs:** 0.10% commission + 0.05% slippage per side

```

==========================================================================================
  LOW CAPITAL TEST — capital-aware universe price filter
  Period: Full 2022–2026  (2022-01-01 → 2026-03-24)
  Strategies: 5 equal-weight (0.20 each)  |  max_pos=10%  |  min_order=₹500 (filtered runs)
==========================================================================================
  Capital        Config              Sharpe    Return    MaxDD    WR%  #Trades  Price Ceiling
  -------------------------------------------------------------------------------------
  ₹10,000        A) No filter          0.97      7.0%     2.0%  46.3%      624  
  ₹10,000        B) Price filter       0.00      0.0%     0.0%   0.0%        0  ≤ ₹200

  ₹25,000        A) No filter          0.75     10.1%     3.6%  46.2%     1278  
  ₹25,000        B) Price filter       0.00      0.0%     0.0%   0.0%        0  ≤ ₹500

  ₹50,000        A) No filter          0.64     12.9%     6.2%  45.8%     2201  
  ₹50,000        B) Price filter       0.51      9.1%     8.2%  43.8%     1828  ≤ ₹1000

  ₹1,00,000      A) No filter          0.58     15.3%     6.5%  45.3%     3248  
  ₹1,00,000      B) Price filter       0.59     15.8%     6.5%  45.5%     3243  ≤ ₹2000


  INTERPRETATION GUIDE:
  • #Trades near 0 with 'No filter' = capital too low, all signals sizing to qty=0
  • 'Price filter' should show meaningful #Trades even at low capital
  • Sharpe/WR% may differ as the universe shifts to cheaper mid-cap names
  • ₹1,00,000 rows should be nearly identical (filter ceiling ≫ all stock prices)
==========================================================================================
```


---

## Latest Run

> Config: ATR×2.5 trailing stop + volume filter (vol_ratio>1.2).  

**Generated:** 2026-05-16 20:40  
**Mode:** EqualWeight  
**Costs:** 0.10% commission + 0.05% slippage per side

```

==========================================================================================
  LOW CAPITAL TEST — capital-aware universe price filter
  Period: Full 2022–2026  (2022-01-01 → 2026-03-24)
  Strategies: 5 equal-weight (0.20 each)  |  max_pos=10%  |  min_order=₹500 (filtered runs)
==========================================================================================
  Capital        Config              Sharpe    Return    MaxDD    WR%  #Trades  Price Ceiling
  -------------------------------------------------------------------------------------
  ₹10,000        A) No filter          0.97      7.0%     2.0%  46.3%      624  
  ₹10,000        B) Price filter       0.91      5.9%     2.5%  43.3%      487  ≤ ₹200  min_order=₹100

  ₹25,000        A) No filter          0.75     10.1%     3.6%  46.2%     1278  
  ₹25,000        B) Price filter       0.67      8.2%     4.6%  44.0%     1047  ≤ ₹500  min_order=₹250

  ₹50,000        A) No filter          0.64     12.9%     6.2%  45.8%     2201  
  ₹50,000        B) Price filter       0.51      9.1%     8.2%  43.8%     1828  ≤ ₹1000  min_order=₹500

  ₹1,00,000      A) No filter          0.58     15.3%     6.5%  45.3%     3248  
  ₹1,00,000      B) Price filter       0.57     14.3%     7.9%  45.3%     2825  ≤ ₹2000  min_order=₹1000


  INTERPRETATION GUIDE:
  • #Trades near 0 with 'No filter' = capital too low, all signals sizing to qty=0
  • 'Price filter' should show meaningful #Trades even at low capital
  • Sharpe/WR% may differ as the universe shifts to cheaper mid-cap names
  • ₹1,00,000 rows should be nearly identical (filter ceiling ≫ all stock prices)
==========================================================================================
```
