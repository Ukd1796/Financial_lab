# Adaptive Strategy Selector — Design & Integration Guide

## 1. What It Is

The Adaptive Strategy Selector is a weekly meta-layer that reads the current market regime
distribution across the active universe and decides **how much capital each strategy should
deploy** for the coming week.

Instead of running each strategy on 100% of available capital independently (the current
approach), all strategies run simultaneously on a shared portfolio, but the capital
allocated to each strategy's signals is scaled by a **weight vector** that shifts based
on market conditions:

```
Current regime snapshot → AdaptiveStrategySelector (LLM) → {CS: 0.4, Breakout: 0.3, DualMA: 0.2, RSI-MR: 0.1}
```

The weights then influence position sizing: a strategy with weight 0.4 gets 40% of the
portfolio's available risk budget, while one with weight 0.1 only gets 10%.

---

## 2. Why It Is Needed — Evidence from Current Results

The results reveal a pattern the rules-based system cannot exploit: **no single strategy
dominates across all regimes, but regime-matched strategies significantly outperform.**

### Per-regime best performer

| Period | Regime | Best strategy | Sharpe | Return |
|---|---|---|---|---|
| Bull 2019 | Trending, low-vol | CS L=100 | 1.53 | +9.6% |
| Crash 2020 | High-vol, falling | Breakout 10d | 1.44 | +23.9% |
| Recovery 2020–21 | V-shaped, high-breadth | Breakout 10d | 2.48 | +101.5% |
| Bear 2022 | Choppy, declining | CS L=100 | 1.11 | +8.4% |
| Recent 2022–24 | Mixed trending | DualMA | 1.67 | +65.8% |

### What gets left on the table

In Recovery 2020–21, RSI-MR (os=10) delivered only +5.7% Sharpe 0.53 while Breakout
delivered +101.5% Sharpe 2.48. A system running both with equal weight averages the two
outcomes. A system that allocated 70% to Breakout in that regime would have captured
most of the upside.

In Bear 2022, DualMA delivered +65.8% on the 2022-24 window while TrendPB lost -10.6%.
Equal weighting again drags the combined result toward the median, not the best performer.

**The core insight:** regime characteristics are measurable from the universe data we
already compute daily (% UPTREND, % DOWNTREND, ATR percentile, breadth). The LLM is
the right tool to translate these signals into a strategy weight vector because the
mapping is pattern-matching with many interacting variables, not a deterministic rule.

---

## 3. Pre-requisites — Fix These Before Building the Selector

**The adaptive selector allocates weight to strategies. If a strategy is structurally
broken, the selector will learn to give it zero weight — but that means the complexity
is wasted.** Fix the strategies first so the selector has 3-4 genuinely profitable
strategies to allocate between.

### 3.1 CS momentum threshold is still dead (Priority: Critical)

`CS L=100 T=0.5` and `CS L=100 T=1.0` produce **identical results** across all six
periods — same 75 trades, same 189.31% full-period return. The risk-adjusted momentum
score (`N_day_return / rolling_vol`) was implemented but the threshold is still not
differentiating.

**Diagnosis to run:** Add a print inside `_compute_momentum()` to log the min, max, and
mean score across the universe for a single date. If all scores are well above both 0.5
and 1.0, the threshold is in dead space for a different reason than before.

**Fix options:**
- Lower thresholds to 0.1 and 0.3 (risk-adj score in recovery periods can be 2-5, in
  sideways periods 0.1-0.5)
- Or remove threshold entirely and rely on top-N selection by score rank

### 3.2 RSI-MR does not emit HOLD decisions (Priority: High)

Unlike Breakout and TrendPullback which were fixed to emit `HOLD` for held positions,
`RSIMeanReversionStrategy.decide()` only emits decisions when the time-stop or RSI exit
fires. When neither condition is met, no decision is emitted → `RiskAgent.evaluate()` is
never called → **the ATR stop is silently disabled for all RSI-MR held positions**.

This is the same bug that was fixed in TrendPullback. For RSI-MR's 1–5 day hold window,
the ATR stop is critical because it cuts losers before the time-stop fires.

**Fix:** Add an explicit `HOLD` emission in the `in_position` branch when neither the
time-stop nor the RSI exit fires (same pattern as Breakout and TrendPullback).

### 3.3 TrendPullback — still losing on full period (Priority: Medium)

Full period: -11.8% (3% threshold), +1.86% (5% threshold). Both are below breakeven
adjusted for opportunity cost. The SMA_20 exit fix helped in Recovery (+16.7%) but the
strategy loses in Bull, Bear, and Recent periods.

**Root issue:** The strategy buys pullbacks in uptrends but the NSE mid-cap stocks in
the universe have highly asymmetric pullback profiles — when they pull back 3-5%, half
of them are breaking down, not pulling back. The `sma_20 > sma_50` filter is too weak.

**Proposed fix before including in the selector:**
- Add a volume confirmation: entry only when pullback occurs on declining volume
  (distribution signal vs panic selling)
- Or add a minimum recovery signal: require RSI_3 < 30 on entry (ensures the pullback
  is extreme, not just a routine -3%)
- Or retire TrendPB from the active strategy pool and replace with a
  volatility-breakout entry (Donchian channels)

### 3.4 RSI-MR needs a hold-duration guard (Priority: Low)

In Bear 2022, RSI-MR (os=10) loses -10.88% with 209 trades. The `max_hold_days=5`
time-stop fires consistently but the position is usually down by then. The problem is
RSI_3 < 10 is a genuine extreme in downtrends — stocks are oversold for a reason.
The breadth circuit breaker (60% in DOWNTREND) helps but Bear 2022 shows -10.88%
despite it, meaning the threshold may need tightening to 50%.

---

## 4. Architecture — How It Integrates

### 4.1 Current system architecture

```
BacktestEngine.run()
  for each day:
    universe_filter()         → active_symbols
    strategy_router.decide()  → proposed_decisions   # ONE strategy runs
    risk_agent.evaluate()     → sized_decisions
    execution_agent.execute() → fills
```

The current `strategy_router` is a single strategy instance. Each experiment runs one
strategy in isolation on the full portfolio.

### 4.2 Target architecture with adaptive selector

```
BacktestEngine.run()
  for each day:
    universe_filter()           → active_symbols
    [weekly] adaptive_selector.rebalance(regime_snapshot) → strategy_weights
    multi_strategy_router.decide(strategy_weights)         → proposed_decisions
    risk_agent.evaluate()       → sized_decisions (weight applied here)
    execution_agent.execute()   → fills
```

Three new components:

```
app/strategy/multi_router.py          # aggregates decisions from all strategies
app/meta/adaptive_selector.py         # LLM call → strategy weights
app/meta/regime_snapshot.py           # builds the regime stats dict for the LLM
```

### 4.3 MultiStrategyRouter

Wraps all registered strategies and merges their decisions. For the same symbol, when
two strategies emit a BUY, only one is kept (highest-weight strategy wins). When one
emits BUY and another HOLD, the BUY is kept. SELL always overrides.

```python
class MultiStrategyRouter:
    def __init__(self, strategies: dict[str, object], weights: dict[str, float] = None):
        self.strategies = strategies   # {"CS": cs_instance, "Breakout": bo_instance, ...}
        self.weights    = weights or {k: 1.0 for k in strategies}

    def decide(self, current_date, symbol_states, portfolio) -> list[Decision]:
        all_decisions = {}  # symbol → Decision (highest-weight wins on conflict)
        for name, strategy in self.strategies.items():
            w = self.weights.get(name, 0.0)
            if w < 0.05:
                continue  # strategy effectively disabled
            decisions = strategy.decide(current_date, symbol_states, portfolio)
            for d in decisions:
                if d.symbol not in all_decisions or w > self.weights.get(all_decisions[d.symbol].source, 0):
                    d.weight = w        # attach weight for RiskAgent to use
                    d.source = name     # which strategy generated it
                    all_decisions[d.symbol] = d
        return list(all_decisions.values())
```

Add `weight` and `source` fields to the `Decision` model.

### 4.4 AdaptiveStrategySelector

Called once per week (not daily — LLM latency is 1-3 seconds per call, daily would add
250 calls per year per backtest run).

```python
class AdaptiveStrategySelector:
    def __init__(self, anthropic_client, strategy_names: list[str]):
        self.client         = anthropic_client
        self.strategy_names = strategy_names
        self.weights        = {s: 1.0 / len(strategy_names) for s in strategy_names}
        self._last_updated  = None

    def rebalance(self, current_date: datetime, regime_snapshot: dict):
        if self._last_updated and (current_date - self._last_updated).days < 7:
            return self.weights   # reuse last week's weights

        prompt = self._build_prompt(regime_snapshot)
        response = self.client.messages.create(
            model="claude-opus-4-6",
            max_tokens=512,
            messages=[{"role": "user", "content": prompt}]
        )
        self.weights    = self._parse_weights(response.content[0].text)
        self._last_updated = current_date
        return self.weights
```

### 4.5 RegimeSnapshot

Computes the regime statistics from the daily symbol states already available in the
engine. No additional data fetching needed.

```python
def build_regime_snapshot(daily_symbol_states: dict, current_date: datetime) -> dict:
    regimes = [s.indicators.get("regime", "") for s in daily_symbol_states.values()]
    n = len(regimes)
    return {
        "date":              current_date.strftime("%Y-%m-%d"),
        "universe_size":     n,
        "pct_uptrend":       sum(1 for r in regimes if "UPTREND"   in str(r)) / n,
        "pct_downtrend":     sum(1 for r in regimes if "DOWNTREND" in str(r)) / n,
        "pct_sideways":      sum(1 for r in regimes if "SIDEWAYS"  in str(r)) / n,
        "pct_high_vol":      sum(1 for r in regimes if "HIGH_VOL"  in str(r)) / n,
        "avg_atr_pct":       mean(s.indicators.get("atr_pct", 0) for s in daily_symbol_states.values()),
        "market_breadth":    round(sum(1 for r in regimes if "UPTREND" in str(r)) / n, 3),
    }
```

### 4.6 LLM Prompt Design

The prompt gives the LLM the regime state, the historical performance of each strategy
per regime (hard-coded from backtest results), and asks for a weight vector.

```python
STRATEGY_REGIME_PERFORMANCE = """
Strategy historical performance by regime (Sharpe ratio):
                    Trending/Bull  Crash/High-vol  Recovery  Bear/Choppy  Sideways
CS L=100 momentum      1.53           1.31          2.74       1.11        1.21
Breakout 10d           0.72           1.44          2.48       0.69        1.07
DualMA SMA20/50       -0.78           0.58          2.24       0.50        1.67
RSI-MR os=5 ob=80     -0.68           0.87          1.32      -1.83       -0.36
"""

def _build_prompt(self, snapshot: dict) -> str:
    return f"""You are a portfolio risk manager allocating capital across four trading
strategies on the NSE Indian equity market.

Current market regime snapshot (computed from {snapshot['universe_size']} stocks):
- Date: {snapshot['date']}
- % in UPTREND:   {snapshot['pct_uptrend']:.1%}
- % in DOWNTREND: {snapshot['pct_downtrend']:.1%}
- % in SIDEWAYS:  {snapshot['pct_sideways']:.1%}
- % HIGH_VOL:     {snapshot['pct_high_vol']:.1%}
- Market breadth: {snapshot['market_breadth']:.3f}
- Avg ATR %:      {snapshot['avg_atr_pct']:.2%}

{STRATEGY_REGIME_PERFORMANCE}

Based on the current regime snapshot, allocate capital weights across the four strategies.
Weights must sum to 1.0. Set a weight to 0 to fully disable a strategy.

Respond ONLY with a JSON object, no explanation:
{{"CS": 0.XX, "Breakout": 0.XX, "DualMA": 0.XX, "RSI-MR": 0.XX}}"""
```

### 4.7 Weight application in RiskAgent

The `Decision` now carries a `weight` field. `RiskAgent._size_position()` applies it:

```python
def _size_position(self, total_equity, price, atr, strategy_weight=1.0) -> int:
    risk_budget = total_equity * self.risk_per_trade_pct * strategy_weight
    stop_distance = self.atr_multiplier * atr
    vol_qty  = risk_budget / stop_distance
    max_qty  = (total_equity * self.max_position_pct * strategy_weight) // price
    return min(int(vol_qty), int(max_qty))
```

A strategy with weight 0.3 can only deploy 30% of what it would otherwise size at
full weight. This is the cleanest integration — no changes to BacktestEngine or
ExecutionAgent.

---

## 5. BacktestEngine Changes

The engine needs two additions:

1. Accept `adaptive_selector` and `multi_strategy_router` parameters (both optional —
   backward compatible with single-strategy experiments).

2. Call `adaptive_selector.rebalance()` weekly and push updated weights to the router.

```python
# In BacktestEngine.run(), inside the daily loop:
if self.adaptive_selector:
    weights = self.adaptive_selector.rebalance(current_date, regime_snapshot)
    self.strategy_router.update_weights(weights)   # MultiStrategyRouter method
```

`regime_snapshot` is built from `daily_symbol_states` after the market-breadth
computation (line 131 in current engine.py) — same data, no extra fetch.

---

## 6. Why the LLM Is the Right Tool Here

A rules-based version of this would look like:

```python
if pct_uptrend > 0.60:
    weights = {CS: 0.5, Breakout: 0.3, DualMA: 0.1, RSI-MR: 0.1}
elif pct_downtrend > 0.50:
    weights = {CS: 0.3, Breakout: 0.4, DualMA: 0.1, RSI-MR: 0.2}
...
```

This requires enumerating every regime combination and manually tuning 4×N weights.
With 4 regime dimensions (uptrend %, downtrend %, vol level, breadth) at 3 levels each,
that's 81 combinations — each requiring manually assigned weights based on intuition.

The LLM instead:
- Reads the performance table once (hard-coded in the prompt)
- Reasons about which regime the current data most closely resembles
- Outputs calibrated weights accounting for interaction effects

The LLM also naturally handles edge cases like "60% uptrend but high ATR" (momentum
strategy is risky — reduce weight) that a rule-based system would need explicit branches
for.

---

## 7. Implementation Order

| Step | What | Effort |
|---|---|---|
| 1 | Fix RSI-MR HOLD emission (same as Breakout fix) | 30 min |
| 2 | Debug CS threshold deadlock (print momentum scores) | 1 hr |
| 3 | Fix TrendPullback or retire it from multi-strategy pool | 1–2 hr |
| 4 | Add `weight` and `source` fields to `Decision` model | 15 min |
| 5 | Build `MultiStrategyRouter` | 2 hr |
| 6 | Build `RegimeSnapshot` helper | 1 hr |
| 7 | Build `AdaptiveStrategySelector` with Anthropic SDK | 2 hr |
| 8 | Wire into `BacktestEngine` (optional `adaptive_selector` param) | 1 hr |
| 9 | Run backtests: compare fixed equal-weight vs adaptive | 1 hr |

Total: ~10 hours of implementation. Steps 1-3 are pre-requisites that should be done
regardless of the adaptive selector.

---

## 8. Expected Impact

Based on the per-regime Sharpe numbers:

**Best-case:** The selector correctly routes capital to CS + Breakout in trending
regimes and to RSI-MR in high-vol/crash regimes. The full-period blended Sharpe should
rise from the current ~1.0 (Breakout alone) toward the regime-matched peak of ~2.0-2.5.

**Conservative case:** The selector correctly avoids deploying RSI-MR and TrendPB in
Bear and Bull regimes where they lose money. Even without finding the optimal weights,
preventing capital allocation to losing strategies in wrong regimes is itself a
meaningful improvement.

**Key risk:** The LLM is calibrated on the same backtest periods it's being tested on.
In live trading, use walk-forward validation — train the performance table on years 1-4,
test the selector's weight choices on year 5, roll forward.

---

## 9. What This Does NOT Solve

- **TrendPullback's structural issue** — weighting it at 0.0 avoids the losses but
  doesn't fix the strategy. Worth fixing or replacing.
- **RSI-MR in choppy/bear markets** — the breadth circuit breaker already addresses
  this partially. The selector adds a second layer.
- **Inter-strategy correlation** — CS and Breakout both buy momentum stocks and will
  often be in the same positions simultaneously. A sector concentration limit (A4 in
  roadmap) is needed to prevent the combined portfolio from being 80% IT + metals.
- **Walk-forward overfitting** — the performance table in the prompt is derived from
  backtests. If live regimes differ from historical ones, the selector's prior is wrong.
  B5 (Regime Narrative Agent) would add a real-time sanity check on top.
