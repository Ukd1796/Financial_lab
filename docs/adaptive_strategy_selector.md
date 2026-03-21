# Adaptive Strategy Selector — Design & Integration Guide

**Last updated**: 2026-03-19
**Status**: Pre-requisites complete. Ready to build.

---

## 1. What It Is

The Adaptive Strategy Selector is a weekly meta-layer that reads the current market regime
distribution across the active universe and decides **how much capital each strategy should
deploy** for the coming week.

Instead of running each strategy on 100% of available capital independently (the current
approach), all strategies run simultaneously on a shared portfolio, but the capital
allocated to each strategy's signals is scaled by a **weight vector** that shifts based
on market conditions:

```
Current regime snapshot → AdaptiveStrategySelector (Claude API) →
  {DualMA: 0.35, Breakout: 0.30, QuietBrk: 0.20, TrendPB: 0.10, RSI-MR: 0.05}
```

The weights influence position sizing: a strategy with weight 0.35 gets 35% of the
portfolio's available risk budget, while one with weight 0.05 only gets 5%.

---

## 2. Why It Is Needed — Evidence from Current Results

The results reveal a pattern the rules-based system cannot exploit: **no single strategy
dominates across all regimes, but regime-matched strategies significantly outperform.**

### 2.1 Per-regime best performer (current strategy pool)

| Period | Regime character | Best strategy | Sharpe | Return |
|---|---|---|---|---|
| Bull 2019–20 | Slow, low-vol uptrend | QuietBrk 20d | 0.98 | +14% |
| Crash 2020 | High-vol, V-shaped | QuietBrk 20d | 2.00 | +35% |
| Recovery 2020–21 | Broad uptrend, high breadth | QuietBrk 20d | **2.80** | +129% |
| Bear 2022 | Choppy, rolling decline | DualMA | **0.56** | +8% |
| Recent 2022–24 | Mixed, trending | DualMA | **1.73** | +81% |

### 2.2 Full Sharpe matrix — current strategy pool

| Strategy | Bull 19–20 | Crash 20 | Recov 20–21 | Bear 22 | Recent 22–24 | Full 18–24 |
|---|---|---|---|---|---|---|
| DualMA SMA20/50 | 0.40 | 1.38 | 2.55 | **0.56** | **1.73** | 1.29 |
| Breakout 10d | 0.49 | 1.49 | 2.48 | 0.39 | 1.15 | 1.12 |
| QuietBrk 20d | 0.98 | **2.00** | **2.80** | -0.67 | 0.67 | 1.05 |
| TrendPB 5% | 0.97 | 1.80 | 1.23 | -0.34 | 0.89 | 0.80 |
| RSI-MR os=5 | 0.21 | 0.86 | 1.37 | -0.66 | -0.11 | 0.25 |

### 2.3 What gets left on the table

**Recovery 2020–21**: QuietBrk produced Sharpe 2.80 (+129%) while RSI-MR os=5 produced
Sharpe 1.37 (+33%). Running both at equal weight averages toward 2.09. A selector routing
60% to QuietBrk + 30% to Breakout + 10% to DualMA in that regime would have captured
most of the upside while maintaining diversification.

**Bear 2022**: DualMA is the only positive strategy (+8%, Sharpe 0.56). QuietBrk loses
-10%, TrendPB loses -9%, RSI-MR loses -9% to -12%. An equal-weight portfolio of all
five would have lost roughly -4% in Bear 2022. A selector routing 70% to DualMA + 20%
to Breakout + 10% to TrendPB5% (the least-bad of the others) limits losses to near-zero
and still captures the DualMA upside.

**The core insight:** regime characteristics are measurable from the universe data already
computed daily (% UPTREND, % DOWNTREND, ATR percentile, breadth). The selector translates
these signals into a weight vector. The key insight is that **QuietBrk and DualMA are
complementary**: QuietBrk excels in volatile trending conditions (Crash/Recovery),
DualMA excels when the trend is sustained and low-noise (Bear survival + Recent trending).
No single strategy holds both characteristics.

---

## 3. Pre-requisites — Status

All critical pre-requisites are now resolved. The strategy pool is ready for the selector.

### ✅ 3.1 RSI-MR HOLD emission — DONE

`RSIMeanReversionStrategy.decide()` emits explicit `HOLD` decisions for all held positions
when neither the time-stop nor the RSI exit fires. The ATR stop in `RiskAgent` runs
correctly on every bar. Verified in code (`rsi_mean_reversion.py` lines 90–105).

### ✅ 3.2 Breadth circuit breaker tightened to 40% — DONE (R1)

`RiskAgent.max_downtrend_pct` default is now 0.40. BUY signals are blocked when >40%
of the active universe is in DOWNTREND. This was the primary Bear 2022 fix — RSI-MR
Bear losses reduced from -21% to -12% as a result.

### ✅ 3.3 sma_cross_age filter for RSI-MR — DONE (R2)

`MeanReversionUniverseFilter` requires `sma_cross_age >= 10`. Stocks whose SMA20 crossed
SMA50 in the last 9 days are rejected as mean-reversion candidates (false uptrends in
bear markets). This complemented R1 in cutting RSI-MR bear losses.

### ✅ 3.4 CS momentum strategy — RETIRED

`CrossSectionalMomentumStrategy` is commented out of `run_experiments.py`. It is not
part of the active strategy pool and does not need to be included in the selector.

### ⚠️ 3.5 QuietBrk 20d Bear regime gate — OPEN (Priority: High before multi-strategy run)

QuietBrk 20d loses -10% in Bear 2022 (Sharpe -0.67). Its current `allowed_regimes` is
`_TREND_AND_SIDEWAYS`, which permits entries on stocks classified as SIDEWAYS even when
the broad market is declining.

**Two options:**
- Switch `allowed_regimes` to `_UPTREND_ONLY` in `run_experiments.py` (tightest gate —
  blocks entry on any stock not in a confirmed UPTREND per SMA50 regime classifier)
- Or let the adaptive selector handle it by weighting QuietBrk to ~0.05 in bear regimes
  (simpler, but the per-trade losses still occur even at low weight)

**Recommendation:** Apply `_UPTREND_ONLY` first. Test that Crash/Recovery Sharpe is
preserved (the crash-to-recovery V-shape has most stocks in confirmed UPTREND by the
time QuietBrk entries fire). Then confirm the selector can further down-weight it in bear.

### ⚠️ 3.6 RSI-MR os=10 — SHOULD BE RETIRED from multi-strategy pool

RSI-MR os=10 is -13% full period and -12% in Bear 2022. RSI-MR os=5 dominates it in
every single period (higher or equal Sharpe, lower or equal losses). Running both in the
multi-strategy pool adds execution noise without diversification benefit. The selector
should only include RSI-MR os=5.

### ⚠️ 3.7 TrendPB Bear 2022 — STRUCTURAL ISSUE REMAINS

TrendPB 3% and 5% both lose in Bear 2022 (-9% / -2%). R3 (`sma_cross_age >= 15` filter)
was reverted because it harmed Recovery without fixing Bear. TrendPB 5% has an acceptable
full-period result (+39%, Sharpe 0.80) and should remain in the selector pool, but the
selector should learn to down-weight it in bear conditions. TrendPB 3% (+42%, Sharpe 0.63)
offers minimal additional diversification over TrendPB 5% — consider dropping it from
the multi-strategy pool to reduce decision noise (5% threshold dominates in most periods).

---

## 4. Architecture — How It Integrates

### 4.1 Current system architecture

```
BacktestEngine.run()
  for each day:
    dynamic_universe_agent.select_candidates()  → 80 UniverseCandidates
    per_strategy_filter.select_symbols()        → 20 active symbols
    strategy_router.decide()                    → proposed_decisions  # ONE strategy
    risk_agent.evaluate()                       → sized_decisions
    execution_agent.execute()                   → fills
```

Each experiment in `run_experiments.py` runs one strategy in isolation on the full
portfolio. The five strategies have never run simultaneously on a shared capital pool.

### 4.2 Target architecture with adaptive selector

```
BacktestEngine.run()
  for each day:
    dynamic_universe_agent.select_candidates()  → 80 UniverseCandidates
    [each strategy's filter runs independently] → per-strategy symbol lists
    [weekly] adaptive_selector.rebalance(regime_snapshot) → strategy_weights
    multi_strategy_router.decide(strategy_weights)         → merged decisions
    risk_agent.evaluate(decision.weight)        → sized_decisions (weight scales size)
    execution_agent.execute()                   → fills
```

Three new components to build:

```
app/strategy/multi_router.py     # aggregates decisions from all active strategies
app/meta/adaptive_selector.py    # Claude API call → strategy weight vector (weekly)
app/meta/regime_snapshot.py      # builds the regime stats dict from daily symbol states
```

### 4.3 MultiStrategyRouter

Wraps all registered strategies and merges their decisions for each day.

Conflict resolution rules:
- Same symbol, two BUYs → keep the one from the highest-weight strategy
- Same symbol, BUY + HOLD → keep BUY (the active signal takes precedence)
- Same symbol, any SELL → SELL always overrides (risk-first)
- Each winning decision carries `weight` and `source` for RiskAgent sizing

```python
class MultiStrategyRouter:
    def __init__(self, strategies: dict[str, BaseStrategyAgent], weights: dict[str, float] = None):
        self.strategies = strategies  # {"DualMA": dual_ma, "Breakout": breakout, ...}
        self.weights    = weights or {k: 1.0 / len(strategies) for k in strategies}

    def update_weights(self, weights: dict[str, float]):
        self.weights = weights

    def decide(self, current_date, symbol_states, portfolio) -> list[Decision]:
        # Per-strategy decisions, keyed by symbol
        per_strategy: dict[str, dict[str, Decision]] = {}
        for name, strategy in self.strategies.items():
            w = self.weights.get(name, 0.0)
            if w < 0.05:
                continue  # effectively disabled
            decisions = strategy.decide(current_date, symbol_states, portfolio)
            per_strategy[name] = {d.symbol: d for d in decisions}

        # Merge: SELL > BUY > HOLD; ties broken by strategy weight
        merged: dict[str, tuple[Decision, float]] = {}  # symbol → (decision, weight)
        action_priority = {"SELL": 2, "BUY": 1, "HOLD": 0}

        for name, decisions in per_strategy.items():
            w = self.weights[name]
            for symbol, d in decisions.items():
                if symbol not in merged:
                    merged[symbol] = (d, w)
                else:
                    existing_d, existing_w = merged[symbol]
                    p_new = action_priority.get(d.action, 0)
                    p_old = action_priority.get(existing_d.action, 0)
                    if p_new > p_old or (p_new == p_old and w > existing_w):
                        merged[symbol] = (d, w)

        result = []
        for symbol, (d, w) in merged.items():
            d.weight = w
            d.source = next(
                (n for n, ds in per_strategy.items() if symbol in ds and ds[symbol] is d),
                "unknown",
            )
            result.append(d)
        return result
```

Add `weight: float = 1.0` and `source: str = ""` fields to `app/strategy/models.py`
`Decision` dataclass.

**Universe filter handling**: Each strategy in the router needs its own filter. The
`MultiStrategyRouter.decide()` receives `symbol_states` — these must include the union
of all strategies' filtered universes. Two approaches:

- **Simple**: Pass the full top-80 `symbol_states` to all strategies (no per-strategy
  filter at the router level). Each strategy's entry conditions act as their own filter.
  Fastest to implement.
- **Correct**: Run each per-strategy filter before calling `strategy.decide()`, passing
  only that strategy's filtered symbol list. Slower but preserves the filter architecture.

Recommended: start with the simple approach. The per-strategy entry conditions (RSI threshold,
20d high, golden cross) already filter heavily — the universe filter just pre-scores.

### 4.4 AdaptiveStrategySelector

Called once per week. Returns a weight dict; weights hold until next rebalance.

```python
import json
from datetime import datetime
import anthropic


class AdaptiveStrategySelector:
    def __init__(self, strategy_names: list[str]):
        self.client         = anthropic.Anthropic()
        self.strategy_names = strategy_names
        self.weights        = {s: 1.0 / len(strategy_names) for s in strategy_names}
        self._last_updated: datetime | None = None

    def rebalance(self, current_date: datetime, regime_snapshot: dict) -> dict[str, float]:
        if self._last_updated and (current_date - self._last_updated).days < 5:
            return self.weights  # trading week not elapsed yet

        prompt   = self._build_prompt(regime_snapshot)
        response = self.client.messages.create(
            model="claude-opus-4-6",
            max_tokens=256,
            messages=[{"role": "user", "content": prompt}],
        )
        raw = response.content[0].text.strip()
        try:
            parsed = json.loads(raw)
            # Normalise to sum=1.0, clip negatives
            total = sum(max(0.0, v) for v in parsed.values())
            if total > 0:
                self.weights = {
                    k: max(0.0, parsed.get(k, 0.0)) / total
                    for k in self.strategy_names
                }
        except (json.JSONDecodeError, KeyError):
            pass  # keep previous weights if parse fails

        self._last_updated = current_date
        return self.weights
```

### 4.5 RegimeSnapshot

Computes regime statistics from the daily symbol states already available in the engine.
No additional data fetching required — `daily_symbol_states` is built before the strategy
layer runs.

```python
def build_regime_snapshot(daily_symbol_states: dict, current_date: datetime) -> dict:
    states  = list(daily_symbol_states.values())
    regimes = [s.indicators.get("regime", "") for s in states]
    n       = max(len(regimes), 1)

    # ATR as % of price — both fields available in every MarketState
    atr_pcts = [
        s.indicators["atr_14"] / s.latest_price
        for s in states
        if s.indicators.get("atr_14") and s.latest_price
    ]
    avg_atr_pct = sum(atr_pcts) / len(atr_pcts) if atr_pcts else 0.0

    return {
        "date":          current_date.strftime("%Y-%m-%d"),
        "universe_size": n,
        "pct_uptrend":   sum(1 for r in regimes if "UPTREND"   in str(r)) / n,
        "pct_downtrend": sum(1 for r in regimes if "DOWNTREND" in str(r)) / n,
        "pct_sideways":  sum(1 for r in regimes if "SIDEWAYS"  in str(r)) / n,
        "pct_high_vol":  sum(1 for r in regimes if "HIGH_VOL"  in str(r)) / n,
        "avg_atr_pct":   avg_atr_pct,
    }
```

### 4.6 LLM Prompt Design

The prompt gives the model the current regime snapshot and the empirical Sharpe table
from backtests, then asks for a normalised weight vector.

```python
# Hard-coded from backtest results (updated March 2026, net of 0.10%+0.05% costs)
STRATEGY_REGIME_PERFORMANCE = """\
Strategy Sharpe by market regime (NSE Indian equities, 2018–2024 backtests):

                  Bull/LowVol  Crash/HighVol  Recovery  Bear/Choppy  Mixed/Recent
DualMA SMA20/50      0.40          1.38         2.55        0.56         1.73
Breakout 10d         0.49          1.49         2.48        0.39         1.15
QuietBrk 20d         0.98          2.00         2.80       -0.67         0.67
TrendPB 5%           0.97          1.80         1.23       -0.34         0.89
RSI-MR os=5          0.21          0.86         1.37       -0.66        -0.11

Regime definitions:
  Bull/LowVol    : >55% stocks in UPTREND, avg ATR% < 1.5%, broad slow uptrend
  Crash/HighVol  : >30% stocks in DOWNTREND, avg ATR% > 2.5%, sharp high-vol moves
  Recovery       : >60% stocks in UPTREND, avg ATR% > 2.0%, post-crash V-shape
  Bear/Choppy    : >40% stocks in DOWNTREND, avg ATR% 1.5–2.5%, grinding decline
  Mixed/Recent   : 30–55% UPTREND, 20–40% DOWNTREND, moderate vol — sector rotation
"""


def _build_prompt(self, snapshot: dict) -> str:
    return f"""You are a portfolio risk manager allocating capital across five trading
strategies on the NSE Indian equity market. Your goal is to maximise risk-adjusted
returns by concentrating capital in the strategies best suited to the current regime.

Current market regime snapshot ({snapshot['universe_size']} stocks):
  Date:         {snapshot['date']}
  % UPTREND:    {snapshot['pct_uptrend']:.1%}
  % DOWNTREND:  {snapshot['pct_downtrend']:.1%}
  % SIDEWAYS:   {snapshot['pct_sideways']:.1%}
  % HIGH_VOL:   {snapshot['pct_high_vol']:.1%}
  Avg ATR %:    {snapshot['avg_atr_pct']:.2%}

{STRATEGY_REGIME_PERFORMANCE}

Rules:
- Weights must sum to 1.0
- Minimum weight is 0.0 (fully disable) — do not force capital into losing strategies
- A weight of 0.05 is the practical minimum for any active strategy (below this, sizing
  rounds to 0 shares at current position sizing parameters)
- In bear/downtrend regimes, strongly prefer DualMA; all other strategies have negative
  or near-zero historical Sharpe in bear conditions
- QuietBrk 20d is high-reward in recovery/crash but deeply negative in bear — weight
  it proportionally to the probability that the current regime is NOT bear/choppy

Respond ONLY with a JSON object, no explanation:
{{"DualMA": 0.XX, "Breakout": 0.XX, "QuietBrk": 0.XX, "TrendPB": 0.XX, "RSI-MR": 0.XX}}"""
```

### 4.7 Weight application in RiskAgent

`Decision` carries a `weight` field (default 1.0 for backward compatibility). The
`RiskAgent._size_position()` scales the risk budget by this weight:

```python
def _size_position(self, total_equity: float, price: float, atr, strategy_weight: float = 1.0) -> int:
    if self.use_vol_sizing and atr and atr > 0:
        risk_budget   = total_equity * self.risk_per_trade_pct * strategy_weight
        stop_distance = self.atr_multiplier * atr
        vol_qty       = risk_budget / stop_distance
        max_qty       = (total_equity * self.max_position_pct * strategy_weight) // price
        return min(int(vol_qty), int(max_qty))
    return int((total_equity * self.max_position_pct * strategy_weight) // price)
```

A strategy with weight 0.30 sizes positions to 30% of what it would deploy at full
weight. This is the cleanest integration point — no changes required in `BacktestEngine`
or `ExecutionAgent`.

---

## 5. BacktestEngine Changes

Two minimal additions to `app/backtest/engine.py`:

**1. Accept optional new components** (backward compatible — existing single-strategy
experiments continue to work unchanged):

```python
def __init__(self, ..., adaptive_selector=None):
    ...
    self.adaptive_selector = adaptive_selector
```

**2. Weekly rebalance + regime snapshot in the daily loop**, inserted after the
market-breadth computation block (currently lines 132–140 in `engine.py`):

```python
# Build regime snapshot for adaptive selector (reuses data already computed)
if self.adaptive_selector:
    regime_snapshot = build_regime_snapshot(daily_symbol_states, current_date)
    weights = self.adaptive_selector.rebalance(current_date, regime_snapshot)
    self.strategy_router.update_weights(weights)  # MultiStrategyRouter method
```

`build_regime_snapshot()` iterates over `daily_symbol_states` which is already populated
at this point in the loop — no extra data access.

---

## 6. Why the LLM Is the Right Tool Here

A rules-based version of the selector would look like:

```python
if pct_uptrend > 0.60 and avg_atr_pct > 0.020:   # Recovery
    weights = {"DualMA": 0.25, "Breakout": 0.25, "QuietBrk": 0.35, "TrendPB": 0.10, "RSI-MR": 0.05}
elif pct_downtrend > 0.40:                         # Bear
    weights = {"DualMA": 0.70, "Breakout": 0.20, "QuietBrk": 0.00, "TrendPB": 0.05, "RSI-MR": 0.05}
elif pct_uptrend > 0.55 and avg_atr_pct < 0.015:  # Slow Bull
    weights = {"DualMA": 0.20, "Breakout": 0.15, "QuietBrk": 0.35, "TrendPB": 0.25, "RSI-MR": 0.05}
...
```

With 5 regime dimensions (uptrend %, downtrend %, vol level, breadth, ATR trend) at
3 levels each, there are 243 possible combinations — each requiring manually calibrated
weights for 5 strategies. That's 1215 parameters set by intuition.

The LLM instead:
- Reads the empirical Sharpe table once per prompt call
- Reasons about which historical regime the current snapshot most resembles
- Outputs a calibrated weight vector accounting for interactions (e.g., "high ATR but
  also high downtrend breadth" signals crash-phase volatility, not recovery volatility —
  favour Breakout over QuietBrk since QuietBrk's bear losses outweigh its crash gains)

The LLM also handles transition regimes naturally: when pct_downtrend is 35% (just
below the Bear threshold), it can assign partial weights to DualMA without requiring
a hard if/else boundary.

---

## 7. Implementation Checklist

### Completed

| # | Step | Completed | Notes |
|---|---|---|---|
| 1 | RSI-MR HOLD emission | ✅ 2026-03-17 | `rsi_mean_reversion.py` lines 90–105 — ATR stop now active on all held positions |
| 2 | R1: Breadth CB 60%→40% | ✅ 2026-03-17 | `RiskAgent.max_downtrend_pct=0.40` default — RSI-MR Bear losses halved |
| 3 | R2: sma_cross_age for RSI-MR | ✅ 2026-03-17 | `MeanReversionUniverseFilter(min_cross_age=10)` — false uptrend entries eliminated |
| 4 | DualMA strategy + filter | ✅ 2026-03-19 | `dual_ma.py` + `DualMAUniverseFilter` — Sharpe 1.73 Recent, 2.55 Recovery |
| 5 | QuietBrk 20d strategy + filter | ✅ 2026-03-19 | `quiet_breakout.py` + relaxed `BreakoutUniverseFilter` — Sharpe 2.80 Recovery |
| 6 | Retire CS momentum | ✅ 2026-03-19 | Commented out in `run_experiments.py` |
| 7 | QuietBrk Bear regime gate | ✅ 2026-03-19 | `allowed_regimes=_UPTREND_ONLY` in `run_experiments.py` — blocks SIDEWAYS entries during rolling bear |
| 8 | Retire RSI-MR os=10 from pool | ✅ 2026-03-19 | Removed from `STRATEGIES` — os=5 dominates in every period |
| 9 | Add `weight`+`source` to `Decision` | ✅ 2026-03-19 | `app/strategy/models.py` — defaults 1.0/"" preserve all existing call sites |

### Active strategy pool (post-cleanup)

Five strategies remain. This is the pool the multi-strategy router will operate over.

| Strategy | File | Full Sharpe | Bear Sharpe | Regime strength |
|---|---|---|---|---|
| DualMA SMA20/50 | `dual_ma.py` | 1.29 | **0.56** | Bear survival + sustained trends |
| Breakout 10d | `breakout_momentum.py` | 1.12 | 0.39 | Consistent across all vol regimes |
| QuietBrk 20d | `quiet_breakout.py` | 1.05 | — (gated) | Crash + Recovery specialist |
| TrendPB 5% | `trend_pullback.py` | 0.80 | -0.34 | Crash/Recovery; reduce in Bear |
| RSI-MR os=5 | `rsi_mean_reversion.py` | 0.25 | -0.66 | Recovery only; weight near-zero in Bear |

### Next — build the meta-layer (in order)

| # | Step | Effort | Why this order |
|---|---|---|---|
| 10 | Build `MultiStrategyRouter` | ~2 hr | Foundation — must exist before steps 11–13 can be tested |
| 11 | Build `build_regime_snapshot()` | ~1 hr | Standalone util, no dependencies, easy to unit-test |
| 12 | Build `AdaptiveStrategySelector` | ~2 hr | Depends on 11 for input shape; Anthropic SDK call |
| 13 | Wire into `BacktestEngine` | ~1 hr | Add optional `adaptive_selector` param; backward compatible |
| 14 | Baseline: equal-weight multi-strategy run | ~1 hr | **Must run before step 15** — establishes the comparison floor |
| 15 | Adaptive run: compare vs equal-weight | ~1 hr | Final validation — is the LLM adding value over equal weighting? |

**Step 14 is critical.** Run all five strategies simultaneously with equal weights (0.20
each) before enabling the LLM layer. This isolates two effects:
- Equal-weight multi-strategy vs best single strategy (diversification benefit)
- Adaptive-weight vs equal-weight (LLM allocation benefit)

Without step 14 you cannot separate the two effects and cannot tell whether any
improvement in step 15 comes from the LLM or simply from running five strategies at once.

**Files to create:**

```
app/
  strategy/
    multi_router.py          # step 10
  meta/
    __init__.py
    regime_snapshot.py       # step 11
    adaptive_selector.py     # step 12
```

---

## 8. Expected Impact

Based on the per-regime Sharpe numbers:

**Conservative case** (selector avoids allocating to losing strategies in the wrong regime):
- In Bear 2022, routing away from QuietBrk (-0.67), TrendPB (-0.34), and RSI-MR (-0.66)
  toward DualMA (0.56) alone could convert an equal-weight portfolio Bear loss of ~-4%
  into a near-zero or positive Bear outcome.
- In Recovery, routing toward QuietBrk (2.80) + DualMA (2.55) at combined 65% weight
  should lift the blended Recovery Sharpe from ~1.6 (equal weight) toward 2.3+.

**Best case** (selector correctly identifies regime transitions):
- Full 2018–24 blended Sharpe should rise from ~1.0 (best single strategy) toward
  1.6–2.0 if the selector correctly allocates in 4 of 6 regime periods.

**Key risk — look-ahead bias in the prompt**: The performance table in the prompt is
derived from the same backtest periods it's being tested on. In a live or walk-forward
setting, use a rolling performance table: train on years 1–4, test on year 5, roll forward.
The backtest result is an upper bound on what the selector can achieve — it knows the
"correct" answer. Walk-forward validation will give the realistic number.

---

## 9. What This Does NOT Solve

- **TrendPB Bear losses** — the selector weights TrendPB low in bear conditions, but the
  per-trade losses still occur at low weight. The structural fix (volume confirmation on
  entry) remains open.

- **QuietBrk Bear losses** — mitigated by the Bear regime gate (step 7 above), but the
  gap between its crash performance (2.00) and bear performance (-0.67) is the largest
  regime sensitivity in the strategy pool. Monitor carefully.

- **Inter-strategy correlation** — DualMA and Breakout both favour trending, high-activity
  stocks. In Recovery, they will often be in overlapping positions simultaneously (both
  buying the same momentum names). A per-sector or per-position concentration limit in
  `RiskAgent` would prevent the combined portfolio from being 80% in one sector.

- **Walk-forward overfitting** — addressed in section 8. The selector's performance table
  must be kept out-of-sample in any live deployment.

- **Latency in live trading** — each weekly rebalance is one Claude API call (~1–2s).
  For a paper-trading system this is acceptable. For live intraday systems it would need
  to be pre-computed overnight.
