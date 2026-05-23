# Analytics Layer — What We Measure and Why

## Overview

The analytics layer is a set of **post-hoc observational modules** added alongside the backtest engine. They attach to a backtest run, watch everything that happens, and produce structured output for diagnosis. They do **not** change any backtest behaviour — no signals, no sizing, no exits are modified.

The output lives in two places:
- **Console** — summary blocks printed after each period's results
- **`trade_analytics.csv`** — one row per completed trade, appendable across runs, openable in Excel or Pandas

There are five components:

---

## 1. Trade Annotator

**File:** `app/analytics/trade_annotator.py`

### What it does

For every completed trade (BUY → SELL pair), it goes back into the OHLC price history and computes metrics that the backtest engine's standard output doesn't capture.

### Metrics it adds to each trade

| Metric | What it measures |
|---|---|
| **MFE %** | Max Favorable Excursion — the furthest the trade moved *in your favour* during the hold period, measured from daily highs |
| **MAE %** | Max Adverse Excursion — the furthest it moved *against you*, measured from daily lows (negative number) |
| **MFE Efficiency** | `final_return / MFE` — did you exit near the peak? 1.0 = you captured the full move. 0.3 = you got 30% of the peak then gave it back |
| **Post-exit drift 1d/3d/5d** | Did the stock keep moving *after* you exited? Positive = you sold too early; negative = you got out in time |
| **Continuation success** | Boolean — was the 5-day post-exit drift positive? |
| **Breakout survival days** | Consecutive trading days the close stayed above your entry price |
| **Regime at entry** | Stock-level regime (e.g. `MID_VOL_UPTREND`) when you entered |
| **Universe rank at entry** | The stock's rank in the filtered universe that day (1 = highest-ranked pick) |
| **Strategy** | Which of the 5 strategies owned this trade (Breakout, DualMA, etc.) |

### Simple example

You buy RELIANCE at ₹2,400. Over the next 8 days it peaks at ₹2,520 (+5%), then you exit at ₹2,448 (+2%). The annotator records:
- MFE = +5.0%
- Final return = +2.0%
- MFE efficiency = 0.40 (you captured 40% of the peak move)
- If the stock then fell to ₹2,390 the next day: post-exit drift 1d = −2.4% (good exit)
- If it kept rising to ₹2,580 two days later: post-exit drift 3d = +5.5% (early exit)

### Why it matters

The standard backtest only tells you win rate and total return. It cannot tell you *why* you're losing — whether exits are too early, whether entries are in weak regimes, or whether a promising setup reversed during the hold. The annotator surfaces exactly that.

---

## 2. Opportunity Quality Engine (OQE)

**File:** `app/analytics/opportunity_quality.py`

### What it does

Aggregates all enriched trades for a period into a summary diagnostic block. Answers the question: **"Is the market giving us good opportunities, and are we capturing them well?"**

### Metrics it computes

#### Breakout Quality
| Metric | What it means |
|---|---|
| **Follow-through rate** | % of trades where price continued moving in the trade direction after exit |
| **False breakout rate** | % where MFE > 2% during hold but final return was negative (looked good, reversed) |
| **Persistence half-life** | Median days a breakout stock stayed above its entry price |
| **Avg MFE efficiency** | Average of (final return / MFE) across all trades |

#### Continuation Decay Curves
Separately for winners and losers: what was the average post-exit drift at 1d, 3d, 5d?

```
                  1D       3D       5D
Winners        +0.31%   +0.58%   +0.92%   ← market kept going up after good exits
Losers         -0.72%   -1.10%   -1.54%   ← market kept falling after bad exits
```

This tells you whether exits are structurally early or late.

#### Per-Regime Breakdown
Win rate and average return broken out by the stock-level regime at entry:

```
Regime                         N     WinRate    AvgRet
LOW_VOL_UPTREND               312     58.3%    +2.31%
MID_VOL_UPTREND               418     51.4%    +1.14%
HIGH_VOL_SIDEWAYS             203     39.1%    −0.87%
```

If HIGH_VOL_SIDEWAYS entries are consistently losing, the regime filter for that strategy should be tightened.

#### Universe vs PnL Correlations
- **Stability vs PnL correlation**: are trades better when the universe is stable (same stocks day after day) vs constantly churning?
- **Turnover vs success**: does high daily churn in the universe predict failed entries?

### Simple example

In Live 2025-26 the OQE showed:
- False breakout rate = 38% (nearly 4 in 10 "breakouts" reversed)
- Persistence half-life = 3 days (stocks left entry price within 3 days on average)
- Winner continuation: +0.1% at 5d (exits were about right)
- Loser continuation: −1.8% at 5d (losers kept falling — ATR stops were working)

This confirmed the issue was *entry quality*, not exit quality.

---

## 3. Ensemble Diagnostics

**File:** `app/analytics/ensemble_diagnostics.py`

### What it does

Measures how the 5 strategies compete inside the `MultiStrategyRouter` and how much of that competition reaches actual execution.

### The signal pipeline

A signal goes through 4 stages before becoming a trade:

```
Strategy generates signal
       ↓
Router merge (priority/weight competition — only one strategy wins per symbol per day)
       ↓
RiskAgent evaluation (ATR ratio, breadth CB, cash gate, regime filter)
       ↓
ExecutionAgent (fills the order)
```

The ensemble diagnostics counts what happens at each stage.

### Metrics

| Metric | What it measures |
|---|---|
| **Participation %** | Per strategy: signals_issued → won_merge rate |
| **Signal passthrough %** | Per strategy: signals that survived all the way to execution |
| **Execution entropy** | Shannon entropy of won_merge distribution. Low = one strategy dominates. High = balanced |
| **Router concentration (HHI)** | Herfindahl-Hirschman Index: 0 = perfectly distributed, 1 = monopoly |
| **Universe diversity score** | How much overlap exists between the 5 strategy filters' candidate sets |

### Technical example

```
Strategy      issued    won    particip%    pass-thru%
DualMA         1,240    890     71.8%         61.2%
Breakout       3,100  1,820     58.7%         44.1%
QuietBrk       2,200    640     29.1%         22.3%
TrendPB        2,800    910     32.5%         25.8%
RSI-MR         1,900    640     33.7%         29.4%

Execution entropy : 1.5821 nats  (max=1.6094 for equal share)
Router concentration (HHI): 0.2314  (0=distributed · 1=monopoly)
Universe unique symbols : 84
Diversity score         : 0.7821  (1.0 = zero overlap between filters)
```

A low participation% for QuietBrk (29%) means it's generating signals but losing the merge competition to higher-priority strategies. A low pass-thru% means even its wins are being killed by the RiskAgent.

### Why it matters

Without this, you cannot distinguish between "the strategy isn't generating signals" and "the strategy is generating signals but they're being killed downstream." The Live 2025-26 issue was the latter — ~3,600 SELL signals were blocked because cross-strategy exits were forbidden under the ownership rules.

---

## 4. Universe Tracker

**File:** `app/analytics/universe_tracker.py`

### What it does

Re-runs the universe filter on every historical date after the backtest and records the composition of the selected universe each day.

### Metrics

| Metric | What it means |
|---|---|
| **Daily turnover %** | Fraction of stocks that changed vs yesterday (10% = 8 new stocks in/out of 80) |
| **Weekly turnover %** | Same but vs 5 trading days ago |
| **Stability score** | 1 − rolling 10-day average daily turnover. 1.0 = static universe, 0.0 = fully churning every day |
| **Leader half-life** | Mean days a stock currently stays in the universe before dropping out |

### Simple example

In a bull market (Recovery 2020-21):
- Stability score = 0.78 — universe fairly stable, same trending stocks staying in
- Leader half-life = 12 days — stocks hold their position for 2 weeks on average

In Live 2025-26:
- Stability score = 0.44 — universe churning heavily
- Leader half-life = 4 days — stocks exit the universe after 4 days on average

High churn means the strategy enters a stock one day, then it drops out of the universe filter the next day — reducing holding time and compounding transaction costs.

---

## 5. Signal Drop Diagnostics (in-engine counters)

**File:** `app/strategy/multi_router.py` + `app/backtest/engine.py`

### What it does

Three counters per strategy, incremented in real-time during the backtest:

| Counter | Incremented when |
|---|---|
| `signals_issued` | Strategy generates any BUY/SELL/HOLD signal |
| `won_merge` | Strategy wins the router's per-symbol priority competition |
| `buy_rejected` | Strategy won merge, but RiskAgent/execution blocked the BUY |

### Printed as

```
Strategy      signals   won_merge   buy_rej   particip%
DualMA          1,240         890       110      71.8%
Breakout        3,100       1,820       470      58.7%
RSI-MR          1,900         640       120      33.7%
```

### Why it matters

This was how we diagnosed the Live 2025-26 underperformance. RSI-MR and TrendPB were issuing SELL signals on Breakout-owned positions — the router blocked ~3,600 of these under the ownership rules (only the opening strategy can close a position). Without the counters this was invisible in the summary metrics.

---

## What the CSV Contains (`trade_analytics.csv`)

Each row is one completed trade. Columns:

```
period, run, strategy, symbol,
entry_date, exit_date, holding_days,
entry_price, exit_price,
final_return_pct, pnl,
mfe_pct, mae_pct, mfe_efficiency,
drift_1d, drift_3d, drift_5d,
continuation_success, breakout_survival_days,
regime_at_entry, weight_at_entry, universe_rank_at_entry
```

### Example rows

```csv
period,run,strategy,symbol,entry_date,exit_date,holding_days,...,mfe_pct,mfe_efficiency,drift_5d,regime_at_entry
Recov 2020-2021,EqW,Breakout,TITAN,2020-07-14,2020-07-22,8,...,8.420%,0.731,+1.230%,MID_VOL_UPTREND
Live 2025-2026,EqW,TrendPB,DIXON,2025-03-03,2025-03-07,4,...,2.100%,0.190,−2.400%,HIGH_VOL_SIDEWAYS
```

The second row shows a classic false breakout: MFE was 2.1% but MFE efficiency was only 0.19 (barely captured 19% of the move), and the stock fell 2.4% in the 5 days after exit.

---

## How These Connect to the Other Systems

```
BacktestEngine
  ├─ pnl_tracker (StrategyPnLTracker / TradeAttributionTracker)
  │    └─ fed via record_fill() on every SELL
  │    └─ fed via record_daily_equity() end-of-day
  │    └─ used by PerformanceFeedbackAgent → AdaptiveSelector LLM prompt
  │    └─ used by ExposureGate → halves BUY size when all core strategies bleeding
  │
  └─ diag_counters (in MultiStrategyRouter)
       └─ signals_issued / won_merge → Ensemble Diagnostics
       └─ buy_rejected (added by engine post-risk) → signal passthrough %

Post-backtest (per period):
  TradeAnnotator      → EnrichedTrade list → trade_analytics.csv
  UniverseTracker     → daily stability/turnover
  OQE                 → breakout quality / continuation decay / regime breakdown
  EnsembleDiagnostics → participation%, entropy, HHI, universe overlap
```

---

## Summary: What Question Each Component Answers

| Component | Question it answers |
|---|---|
| Trade Annotator | Was each individual trade a good entry? Did we exit at the right time? |
| Opportunity Quality Engine | Is the *market* offering good opportunities in this period? |
| Ensemble Diagnostics | Is any one strategy monopolising the router? Where are signals dying? |
| Universe Tracker | Is the stock universe stable or churning? Does instability hurt trades? |
| Signal Drop Diagnostics | Exactly how many signals die at each stage (generation → merge → risk → execution)? |
