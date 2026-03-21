# Adaptive Strategy Selector — Design & Integration Guide

**Last updated**: 2026-03-21
**Status**: Fully implemented. Running in `run_experiments.py` (step 15).

---

## 1. What It Is

The Adaptive Strategy Selector is a weekly meta-layer that reads the current market regime
distribution across the active universe and decides **how much capital each strategy should
deploy** for the coming week.

Five strategies run simultaneously on a shared portfolio. The capital allocated to each
strategy's signals is scaled by a **weight vector** that shifts weekly based on what the
LLM observes in the regime snapshot:

```
regime_snapshot (daily breadth/vol stats)
    ↓ every 5 trading days
AdaptiveStrategySelector (GPT-4o-mini API call)
    ↓
{DualMA: 0.40, Breakout: 0.25, QuietBrk: 0.20, TrendPB: 0.10, RSI-MR: 0.05}
    ↓
MultiStrategyRouter.update_weights()
    ↓
RiskAgent._size_position(strategy_weight=0.40)  ← scales risk budget per position
```

---

## 2. Why It Is Needed — Evidence from Current Results

No single strategy dominates across all regimes. Regime-matched strategies significantly
outperform:

### 2.1 Per-regime Sharpe matrix (updated 2026-03-21)

| Strategy | Bull 19–20 | Crash 20 | Recov 20–21 | Bear 22 | Recent 22–24 | Full 18–24 |
|---|---|---|---|---|---|---|
| DualMA SMA20/50 | 0.44 | 1.28 | 2.66 | **0.51** | **1.69** | **1.33** |
| Breakout 10d | 0.93 | 1.72 | **3.18** | -0.05 | 1.06 | 1.25 |
| QuietBrk 20d | **1.09** | 1.38 | 2.33 | -0.05¹ | **1.08** | 0.89 |
| TrendPB 5% | 0.97 | **1.81** | 1.19 | -0.34 | 0.90 | 0.79 |
| RSI-MR os=5 | 0.15 | 0.88 | 1.34 | -0.65 | -0.14 | 0.22 |
| **EqualWeight** | -0.52 | **2.41** | 2.84 | **+0.29** | 1.24 | 1.19 |

¹ QuietBrk Bear Sharpe improved from -0.67 to -0.05 after `_UPTREND_ONLY` regime gate.

### 2.2 What the equal-weight baseline already achieves

The EqualWeight row above reveals the diversification benefit from simply running all five
together with fixed 20% weights:
- **Crash 2020**: Best Sharpe (2.41) and MaxDD (6.05%) across all strategies
- **Bear 2022**: +2.06% when every individual strategy is negative or near-zero
- **Full period**: 1.19 Sharpe, 96.45% return, 15.18% MaxDD

The adaptive selector's job is to improve *on top of* this floor by shifting weight toward
the regime-optimal strategies each week.

### 2.3 What the LLM can capture

**Recovery regime** (>60% UPTREND, ATR>2%): Breakout has 3.18 Sharpe, QuietBrk 2.33.
Equal-weight blends toward ~2.0. Routing 40% to Breakout + 30% to QuietBrk should lift
the blended Sharpe toward 2.5+.

**Bear regime** (>40% DOWNTREND): DualMA is the only positive strategy (+0.51 Sharpe).
Equal-weight loses ~4%. Routing 60-70% to DualMA limits bear losses to near-zero.

**Slow Bull** (>55% UPTREND, low ATR): QuietBrk and TrendPB outperform Breakout.
The LLM should reduce Breakout/RSI-MR and increase QuietBrk/TrendPB in these conditions.

---

## 3. System Architecture — Current State

```
BacktestEngine.run()
  for each day:
    ① dynamic_universe_agent.select_candidates()   → 80 UniverseCandidates (top-80 by activity)
    ② UnionUniverseFilter.select_symbols()          → 60–80 unique symbols (per-strategy pools merged)
    ③ observer.run_for_day() × N                   → daily_symbol_states {symbol: MarketState}
    ④ [weekly] AdaptiveStrategySelector.rebalance() → new weight dict  ← NEW
               build_regime_snapshot(daily_symbol_states)               ← feeds the LLM
               GPT-4o-mini API call → normalised weight vector
               MultiStrategyRouter.update_weights(new_weights)
    ⑤ MultiStrategyRouter.decide()                 → merged decisions
               ├── per-strategy allowed_regimes filter
               ├── ownership gate (only owning strategy can SELL its positions)
               └── conflict resolution: SELL > BUY > HOLD, ties by weight
    ⑥ RiskAgent.evaluate(decision.weight)          → sized decisions
               ATR stop, breadth circuit breaker, weight-scaled position sizing
    ⑦ execution_agent.execute()                    → fills + portfolio update
```

### File map

```
app/
  backtest/
    engine.py              ← accepts adaptive_selector=None param (step 13 ✅)
  meta/
    __init__.py
    regime_snapshot.py     ← build_regime_snapshot() (step 11 ✅)
    adaptive_selector.py   ← AdaptiveStrategySelector (step 12 ✅)
  strategy/
    multi_router.py        ← MultiStrategyRouter with position_owners (step 10 ✅)
    models.py              ← Decision.weight, Decision.source (step 9 ✅)
  universe/
    filters.py             ← UnionUniverseFilter (step 14 support ✅)
run_experiments.py         ← EqualWeight (step 14 ✅) + Adaptive (step 15 ✅)
```

---

## 4. Component Details

### 4.1 AdaptiveStrategySelector (`app/meta/adaptive_selector.py`)

**Initialization:**
```python
selector = AdaptiveStrategySelector(
    strategy_names=["DualMA", "Breakout", "QuietBrk", "TrendPB", "RSI-MR"],
    rebalance_frequency_days=5,   # ≈ one trading week
    model="gpt-4o-mini",          # ~$0.0002 per call; 1 call/week ≈ $0.01/year
    verbose=True,                 # prints each weekly weight update
)
```

**Weekly call flow:**
1. `build_regime_snapshot()` computes breadth/vol stats from already-populated `daily_symbol_states`
2. `selector.rebalance(date, snapshot)` checks if 5+ days have elapsed since last call
3. If yes: constructs prompt → OpenAI API call → parses JSON → normalises weights
4. Returns current weight dict (unchanged if within the week)
5. `router.update_weights(new_weights)` propagates to position sizing

**Failure safety:** Any API or parse failure leaves weights unchanged. The backtest
continues with the last known weights. `verbose=True` prints a warning.

**Cost:** GPT-4o-mini at ~$0.0002/call. For a 6-year backtest (≈1500 trading days, 300
weeks): ~300 API calls × $0.0002 = **$0.06 per full backtest run**.

### 4.2 Regime snapshot (`app/meta/regime_snapshot.py`)

```python
snapshot = build_regime_snapshot(daily_symbol_states, current_date)
# Returns:
{
  "date":           "2022-06-15",
  "universe_size":  78,
  "pct_uptrend":    0.321,    # fraction with "UPTREND" in regime string
  "pct_downtrend":  0.487,    # → LLM identifies this as Bear/Choppy
  "pct_sideways":   0.192,
  "pct_high_vol":   0.641,
  "avg_atr_pct":    0.0218,   # mean ATR-14 / price
  "market_breadth": 0.321,    # alias for pct_uptrend
}
```

No extra DB access — reuses data already computed in the engine's daily loop.

### 4.3 MultiStrategyRouter — position ownership tracking

Critical fix added in the equal-weight baseline work: each position is tracked to the
strategy that entered it. Only the owning strategy (or ATR stop via RiskAgent) may close it.

```python
router.position_owners = {"RELIANCE": "DualMA", "HDFCBANK": "Breakout", ...}
```

**Why this matters:** Without ownership tracking, RSI-MR would SELL DualMA's multi-week
positions when RSI crossed 80 (a normal event during an uptrend). This was the root cause
of the -55% → -10% → -0% improvement sequence in the equal-weight baseline development.

### 4.4 RiskAgent — weight-scaled position sizing

`Decision.weight` (set by MultiStrategyRouter from its current weight vector) scales both
the risk budget and the position cap:

```python
risk_budget = total_equity × risk_per_trade_pct × strategy_weight
max_qty     = (total_equity × max_position_pct × strategy_weight) // price
```

A strategy at weight 0.40 deploys 40% of its solo risk budget per trade. With 5 strategies
each at variable weights summing to 1.0, the total capital deployment equals what a single
full-weight strategy would deploy — but distributed according to regime fit.

### 4.5 LLM Prompt Design

The prompt contains three sections:
1. **Current regime snapshot** — 5 numeric signals (% uptrend/downtrend/sideways/high_vol, avg ATR%)
2. **Empirical Sharpe table** — 5 strategies × 5 regime types from 2018–2024 backtests
3. **Allocation rules** — 7 regime-specific hard rules derived from backtest evidence

Key design decisions:
- `temperature=0.0` — deterministic output for the same snapshot
- `max_tokens=128` — just enough for a 5-key JSON dict, no padding
- JSON-only output instruction + markdown-stripping fallback parser
- Strategy names in expected-output template prevent key hallucination

---

## 5. UnionUniverseFilter — the universe fix for multi-strategy runs

Before the `UnionUniverseFilter`, all 5 strategies shared a single activity-based top-20
universe. Each got ~4 candidates/day at 20% weight = 4% of normal capital → portfolio
mostly cash → costs eroded returns.

`UnionUniverseFilter` runs each strategy's own filter on the top-80 DynamicAgent candidates
and takes the de-duplicated union (60–80 unique stocks/day):

```python
UnionUniverseFilter([
    BreakoutUniverseFilter(top_n=20),               # high-activity stocks
    BreakoutUniverseFilter(vol_threshold=1.2, ...),  # relaxed for QuietBrk
    PullbackUniverseFilter(top_n=20),                # quiet pullbacks in uptrends
    MeanReversionUniverseFilter(top_n=20),           # oversold in uptrends
    DualMAUniverseFilter(max_cross_age=5, top_n=30), # fresh golden crosses
])
```

Each strategy sees stocks from its preferred domain without competing with others for the
same 20 activity-filtered slots.

---

## 6. Implementation Checklist

| # | Step | Status | Date | Notes |
|---|---|---|---|---|
| 1 | RSI-MR HOLD emission | ✅ Done | 2026-03-17 | ATR stop active on all held positions |
| 2 | R1: Breadth CB 60%→40% | ✅ Done | 2026-03-17 | RSI-MR Bear losses halved |
| 3 | R2: sma_cross_age for RSI-MR | ✅ Done | 2026-03-17 | False uptrend entries eliminated |
| 4 | DualMA strategy + filter | ✅ Done | 2026-03-19 | Sharpe 1.69 Recent, 2.66 Recovery |
| 5 | QuietBrk 20d strategy + filter | ✅ Done | 2026-03-19 | Sharpe 3.18 (via Breakout filter) |
| 6 | Retire CS momentum | ✅ Done | 2026-03-19 | Commented out of experiments |
| 7 | QuietBrk Bear regime gate | ✅ Done | 2026-03-19 | `_UPTREND_ONLY` — Bear loss near-zero |
| 8 | Retire RSI-MR os=10 | ✅ Done | 2026-03-19 | os=5 dominates in every period |
| 9 | Decision.weight + .source | ✅ Done | 2026-03-19 | `app/strategy/models.py` |
| 10 | MultiStrategyRouter | ✅ Done | 2026-03-21 | Position ownership gate added |
| 11 | build_regime_snapshot() | ✅ Done | 2026-03-21 | `app/meta/regime_snapshot.py` |
| 12 | AdaptiveStrategySelector | ✅ Done | 2026-03-21 | `app/meta/adaptive_selector.py`, OpenAI |
| 13 | Wire into BacktestEngine | ✅ Done | 2026-03-21 | `adaptive_selector=None` optional param |
| 14 | EqualWeight baseline | ✅ Done | 2026-03-21 | UnionUniverseFilter fixed capital deployment |
| 15 | Adaptive vs EqualWeight | ✅ Done | 2026-03-21 | In `run_experiments.py` final block |

---

## 7. Active Strategy Pool

| Strategy | File | Full Sharpe | Bear Sharpe | Regime strength |
|---|---|---|---|---|
| DualMA SMA20/50 | `dual_ma.py` | 1.33 | **0.51** | Bear survival + sustained trends |
| Breakout 10d | `breakout_momentum.py` | 1.25 | -0.05 | Consistent across all vol regimes |
| QuietBrk 20d | `quiet_breakout.py` | 0.89 | -0.05¹ | Crash + Recovery specialist |
| TrendPB 5% | `trend_pullback.py` | 0.79 | -0.34 | Crash/Recovery; reduce in Bear |
| RSI-MR os=5 | `rsi_mean_reversion.py` | 0.22 | -0.65 | Recovery only; near-zero weight in Bear |

¹ Gated to `_UPTREND_ONLY` — significantly reduces Bear exposure.

---

## 8. Expected Impact

**Conservative (selector avoids losing strategies in wrong regime):**
- Bear 2022: routing 60-70% to DualMA should convert equal-weight +2.06% into +4-6%
- Recovery: routing 35-40% to Breakout lifts blended Sharpe from 2.84 toward 3.0+

**Best case (correct regime-transition identification):**
- Full 2018-24 blended Sharpe: from 1.19 (equal-weight) toward 1.5-2.0

**Key risk — look-ahead bias in the performance table:**
The Sharpe table in the prompt is from the same 2018-2024 data being tested. In live or
walk-forward usage, use a rolling table: train on years 1-N, test year N+1, roll forward.
The backtest result is an upper bound. Walk-forward will give the realistic number.

---

## 9. What This Does NOT Solve

- **TrendPB Bear losses** — selector weights it low in bear, but per-trade losses still
  occur at low weight. Structural fix (volume confirmation on entry) remains open.

- **Bull 2019-20 underperformance** — EqualWeight showed -4.06% when all individuals are
  positive (+0.93% to +14.71%). Root cause: all five strategies are marginal in this
  choppy period; cost load exceeds aggregate gross gains at 20% position sizes. The
  adaptive selector should help by concentrating weight in the best performers (QuietBrk,
  TrendPB in this period) and zeroing RSI-MR (Sharpe 0.15).

- **Inter-strategy correlation** — DualMA and Breakout both favour trending stocks.
  In Recovery they often enter the same names simultaneously. A per-sector concentration
  limit in RiskAgent would prevent the portfolio being 80% in one sector.

- **Walk-forward overfitting** — the LLM's performance table must be kept out-of-sample
  in any live deployment. The current backtest is an upper bound.

- **Latency** — each weekly rebalance is ~1-2s (one GPT-4o-mini API call). Acceptable
  for paper trading. For live intraday systems, pre-compute overnight.
