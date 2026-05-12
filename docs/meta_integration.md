# `app/meta/` — Meta-Layer Integration Guide

## Overview

`app/meta/` is the weekly intelligence layer that sits between raw market data and strategy execution. It answers two questions every trading week:

1. **What regime is the market in?** (`regime_snapshot.py`, `regime_context_agent.py`)
2. **Given that regime, how should capital be allocated across strategies?** (`adaptive_selector.py`)

The meta layer does not generate trading signals. It adjusts the *weights* passed to `MultiStrategyRouter` and informs the `RiskAgent`'s breadth circuit-breaker relaxation logic. All strategy execution is downstream of these two outputs.

---

## File-by-File

### `regime_snapshot.py`

**Purpose:** Builds a lightweight regime statistics dictionary from market states that are already computed during the backtest daily loop. No extra DB access.

**Function:** `build_regime_snapshot(daily_symbol_states, current_date) → dict`

**Output keys:**

| Key | Type | Description |
|-----|------|-------------|
| `date` | str | ISO date (YYYY-MM-DD) |
| `universe_size` | int | Number of active symbols today |
| `pct_uptrend` | float | Fraction of symbols in any UPTREND regime |
| `pct_downtrend` | float | Fraction of symbols in any DOWNTREND regime |
| `pct_sideways` | float | Fraction in SIDEWAYS |
| `pct_high_vol` | float | Fraction in HIGH_VOL |
| `avg_atr_pct` | float | Mean ATR as % of price across all symbols |
| `market_breadth` | float | Alias for `pct_uptrend` (LLM prompt clarity) |

Used as the base snapshot by both the `AdaptiveStrategySelector` and `RegimeContextAgent`.

---

### `regime_context_agent.py`

**Purpose:** Augments `build_regime_snapshot()` with signals from the full 150-symbol `DynamicUniverseAgent` cache, providing a market-wide breadth view rather than just the active 24–80 symbol trading universe.

**Class:** `RegimeContextAgent(dynamic_agent)`

**Method:** `build_snapshot(daily_symbol_states, current_date) → dict`

Adds these keys on top of the base snapshot:

| Key | Type | Description |
|-----|------|-------------|
| `pct_above_sma50_broad` | float | % of 150-symbol universe where close > SMA_50 |
| `advance_decline_ratio` | float | % of broad universe with positive daily return |
| `broad_universe_size` | int | Actual count of broad-universe symbols found in cache |
| `avg_rolling_vol_5d` | float | Mean 5-day realised volatility across broad universe |
| `trend` | str | `IMPROVING` / `DETERIORATING` / `STABLE` (5-day direction) |
| `broad_regime` | str | Full regime label from `_classify_regime()` (same label set as `AdaptiveStrategySelector`) |

**Trend detection:** Compares `pct_above_sma50_broad` and `pct_downtrend` over the last 5 days. Requires ≥5 days of internal history; returns `STABLE` until then.

**Design note:** This is a drop-in replacement for `build_regime_snapshot()` — the `BacktestEngine` checks for its presence and falls back to the base function if absent. The `broad_regime` key is what enables CB relaxation in the engine (see Data Flow below).

---

### `adaptive_selector.py`

**Purpose:** Calls the OpenAI API on a weekly cadence to produce normalised capital weights for the five strategies. The LLM allocation is constrained by hard per-regime rules to prevent hedging.

**Key components:**

#### `_classify_regime(snapshot) → (label, desc, confidence)`
Deterministic Python-side classifier. Rule priority order (first match wins):

| Label | Condition | Confidence |
|-------|-----------|------------|
| `CRASH_HIGHVOL` | pct_downtrend > 35% **and** avg_atr_pct > 2.3% | HIGH |
| `TRANSITION_UP` | trend == IMPROVING **and** pct_downtrend > 20% | MEDIUM |
| `BEAR_CONFIRMED` | pct_downtrend > 45% | HIGH |
| `BEAR_EARLY` | 35% ≤ pct_downtrend ≤ 45% | MEDIUM |
| `RECOVERY` | pct_uptrend > 60% **and** avg_atr_pct > 2.2% | HIGH |
| `BULL_SUSTAINED` | pct_uptrend > 60% **and** avg_atr_pct ≤ 2.2% | HIGH |
| `BULL_LOWVOL` | pct_uptrend > 55% **and** avg_atr_pct < 1.5% | HIGH |
| `BULL_MEDVOL` | pct_uptrend > 55% | MEDIUM |
| `MIXED` | fallback | LOW |

Note: `TRANSITION_UP` requires the `trend` key (provided by `RegimeContextAgent`). Without it, this label can never fire.

#### `_REGIME_ALLOCATION_RULES`
Hard numeric constraints per regime injected into the LLM prompt as "MANDATORY" language. Examples:
- `BEAR_CONFIRMED`: DualMA MUST be ≥0.55, RSI-MR MUST be ≤0.05
- `RECOVERY`: Breakout MUST be ≥0.35, QuietBrk MUST be ≥0.25
- `MIXED`: No strategy below 0.10 unless negative Sharpe

#### `AdaptiveStrategySelector` class

**Constructor params:**
```python
AdaptiveStrategySelector(
    strategy_names=["DualMA", "Breakout", "QuietBrk", "TrendPB", "RSI-MR"],
    model="gpt-4o-mini",
    rebalance_frequency_days=5,     # weekly cadence
    regime_stability_weeks=2,       # require N consecutive detections before switching
    history_weeks=4,                # rolling snapshot history passed to LLM
    verbose=False,
)
```

**Regime stability gate:** When the classifier returns a new regime label different from the confirmed one, it is tracked as "pending". Only after `regime_stability_weeks` consecutive detections does the new regime become confirmed and trigger a new allocation. This prevents thrashing during noisy transition weeks.

**DualMA floor:** After LLM parsing, DualMA weight is floored at 0.10. DualMA has positive Sharpe in every regime — it is never fully disabled.

**Fallback:** On any API error or JSON parse failure, the previous weights are retained unchanged.

**`on_rebalance` callback:** Optional hook called after each successful LLM rebalance with:
```python
on_rebalance(decided_at, regime, confidence, weights, snapshot, raw_response, model)
```
Used in live trading (`api/services/adaptive_weights_service.py`) to log decisions to the DB.

---

## Data Flow

### Daily Path (every trading day)

```
BacktestEngine.run_day(current_date)
  │
  ├─ 1. Compute daily_symbol_states for all active symbols
  │       (MarketObserverAgent → indicator calculations)
  │
  ├─ 2. Build regime snapshot
  │       if regime_context_agent:
  │           regime_snapshot = regime_context_agent.build_snapshot(states, date)
  │           # adds: pct_above_sma50_broad, trend, broad_regime
  │       else:
  │           regime_snapshot = build_regime_snapshot(states, date)
  │
  ├─ 3. Weekly rebalance (every 5 days)
  │       if adaptive_selector:
  │           new_weights = adaptive_selector.rebalance(date, regime_snapshot)
  │           strategy_router.update_weights(new_weights)
  │
  ├─ 4. CB relaxation (uses broad_regime from snapshot)
  │       effective_downtrend_pct = market_downtrend_pct
  │       if broad_regime == "TRANSITION_UP":
  │           effective_downtrend_pct = min(actual, 0.30)  # allow earlier re-entry
  │       elif broad_regime == "BEAR_EARLY":
  │           effective_downtrend_pct = min(actual, 0.38)  # slight relaxation
  │
  └─ 5. For each proposed signal:
          risk_agent.evaluate(decision, portfolio, market_state,
                              market_downtrend_pct=effective_downtrend_pct)
          → BUY blocked if effective_downtrend_pct > 35% (CB threshold)
```

### Weekly Path (AdaptiveSelector internals)

```
adaptive_selector.rebalance(date, regime_snapshot)
  │
  ├─ _classify_regime(snapshot) → (label, desc, confidence)   [deterministic]
  │
  ├─ Regime stability gate
  │     if label == confirmed_regime: hold allocation, reset pending
  │     elif pending_count < stability_weeks: hold previous allocation
  │     else: promote pending → confirmed, proceed with new label
  │
  ├─ _call_llm(snapshot, label, desc, confidence)
  │     └─ _build_prompt() assembles:
  │           • Current regime classification + breadth stats
  │           • Broad breadth block (if RegimeContextAgent active)
  │           • Inferred trend (IMPROVING/DETERIORATING/STABLE) from history delta
  │             if RegimeContextAgent absent
  │           • Regime age: "_confirmed_weeks rebalance(s)" — LLM stays near
  │             equal-weight on week 1, applies MANDATORY RULE fully on week 3+
  │           • 4-week rolling history of snapshots (← SWITCH tagged on label changes)
  │           • Empirical Sharpe table (hardcoded from 2018–2024 backtests)
  │           • MANDATORY ALLOCATION RULE for this regime
  │     → OpenAI chat completion (temperature=0, gpt-4o-mini)
  │     → _parse_weights(): JSON parse → clip negatives → DualMA floor → normalise
  │
  ├─ strategy_router.update_weights(new_weights)   [called by engine]
  │
  └─ on_rebalance callback (logging, DB write)
```

---

## Integration Map

Every file that imports from `app/meta/`:

| File | What it imports | How it uses it |
|------|----------------|----------------|
| `app/backtest/engine.py` | `build_regime_snapshot`, `RegimeContextAgent`, `AdaptiveStrategySelector` | Orchestrates the daily + weekly meta flow (steps 2–4 above) |
| `app/strategy/multi_router.py` | *(indirect)* | Receives new weights via `update_weights()` called by the engine |
| `app/risk/agent.py` | *(indirect)* | Receives `effective_downtrend_pct` from engine; drives breadth CB |
| `run_backtest.py` | Both selectors | Instantiates for single-strategy test runs |
| `run_ujjwal_baseline.py` | Both selectors | Baseline test runner; `--adaptive` flag enables LLM mode |
| `run_experiments.py` | Both selectors | Walk-forward experiment harness |
| `api/services/adaptive_weights_service.py` | `AdaptiveStrategySelector` | Singleton wrapper; serves `/api/market/adaptive-weights`; logs decisions to DB via `on_rebalance` |
| `api/services/regime_service.py` | `RegimeContextAgent`, `DynamicUniverseAgent` | Computes live regime snapshot; serves `/api/market/regime` |
| `api/routers/market.py` | *(via services)* | REST endpoints for regime + weights |
| `api/services/backtest_service.py` | Both selectors | Backtest API endpoint |

---

## Key Invariants

1. **Same regime label set everywhere.** `_classify_regime()` is imported by both `adaptive_selector.py` and `regime_context_agent.py`. The `broad_regime` key in the enriched snapshot and the `confirmed_regime` in the selector always use the same 9-label set. The CB relaxation in `engine.py` must use labels from this set.

2. **CB relaxation requires `RegimeContextAgent`.** The `broad_regime` key is only present when `RegimeContextAgent` is active (Config C). With plain `build_regime_snapshot()` (Config A/B), `broad_regime` is absent and neither relaxation branch fires.

3. **`TRANSITION_UP` requires `trend` key.** The `TRANSITION_UP` regime condition checks `snapshot.get("trend") == "IMPROVING"`. This key is only set by `RegimeContextAgent`. Without it, the classifier skips this rule and falls through to `BEAR_CONFIRMED` or lower.

4. **Regime stability gate — first call is always immediate.** On the first `rebalance()` call `_confirmed_regime` is `None`, so the new label is accepted immediately without waiting for `regime_stability_weeks`. Subsequent calls require the full stability wait before switching.

5. **DualMA is never fully disabled.** A hard floor of 0.10 is applied after LLM parsing (`_parse_weights`). DualMA has positive Sharpe in every tested regime.

6. **LLM failures silently retain previous weights.** Any exception in `_call_llm` (API error, timeout, bad JSON) returns `None` and `rebalance()` returns the current `self.weights` unchanged.

---

## How to Read LLM Weight Decisions

### In backtests (verbose mode)

```
[AdaptiveSelector] 2024-03-01 [BEAR_EARLY/MEDIUM] → DualMA=0.45  Breakout=0.25  QuietBrk=0.10  TrendPB=0.10  RSI-MR=0.10
[AdaptiveSelector] Regime pending: RECOVERY (1/2 weeks) — holding BEAR_EARLY
[AdaptiveSelector] Regime transition confirmed: BEAR_EARLY → RECOVERY (after 2 weeks)
[AdaptiveSelector] 2024-03-08 [RECOVERY/HIGH] → DualMA=0.21  Breakout=0.37  QuietBrk=0.26  TrendPB=0.11  RSI-MR=0.05
```

The `Regime pending` line fires when a new label is seen but not yet confirmed. `Regime transition confirmed` fires when `regime_stability_weeks` (currently 2) consecutive detections have occurred. After confirmation, `_confirmed_weeks` resets to 1 and increments each rebalance.

### In live trading (DB logs)

`api/services/adaptive_weights_service.py` writes to SQLite (`api_state.db`) via the `on_rebalance` callback. Query with:
```python
from api.db.store import get_state
decisions = get_state("adaptive_weight_decisions") or []
# Each entry: {decided_at, regime, confidence, weights, snapshot, raw_response, model}
```

### Understanding the allocation

Given a regime, cross-reference the weights against `_STRATEGY_REGIME_PERFORMANCE` in `adaptive_selector.py` — the empirical Sharpe table the LLM is given. A well-behaved LLM allocation shifts weight toward strategies with high Sharpe in the detected regime, subject to the MANDATORY RULE constraints.

---

## Changes Made to This Codebase (2026-05-11)

### `app/backtest/engine.py`
- **CB relaxation bug fix:** Lines 174–177 referenced non-existent regime labels `BEAR_WATCH` and `BEAR_TRANSITION`. These were dead code — the elif branch never fired. Fixed to `BEAR_EARLY` (35–45% downtrend), which is the correct semantic match for "early/building bear, not yet confirmed". `BEAR_CONFIRMED` intentionally stays fully blocked.

### `app/meta/adaptive_selector.py`
Three prompt improvements added to `_build_prompt()`:

1. **Regime age tracking (`_confirmed_weeks`):** New `__init__` field tracks how many consecutive rebalances the current regime has been confirmed. Passed into the prompt as `"Regime confirmed for: N rebalance(s)"` so the LLM knows to stay close to equal-weight on week 1 (potentially noisy) vs apply the MANDATORY RULE fully on week 3+.

2. **Inferred trend direction:** When `RegimeContextAgent` is absent (no `trend` key in snapshot), the prompt now computes and injects an `Inferred breadth trend: IMPROVING/DETERIORATING/STABLE` signal from the pct_downtrend delta between the last two history entries (threshold: ±3pp). Removes a reasoning step the LLM frequently drops.

3. **SWITCH annotations in history:** History rows where the regime label changes from the previous week are marked with `← SWITCH`, making regime transitions explicit rather than requiring the LLM to notice them.

---

## Experiment Log

All experiments run against `run_ujjwal_baseline.py`. Adaptive baseline (stability_weeks=2, prompt v1): Full 1.31 / Bear 0.84 / Recent 1.78 / Live -0.81 Sharpe.

| Experiment | Key result | Verdict |
|------------|-----------|---------|
| **ATR stop: current_atr → entry_atr** (Part C) | Full Sharpe 1.21→1.16, MaxDD 15.15→15.56% | ✅ Kept — theoretically correct, minor metric cost |
| **Trailing stop (high-watermark)** (Part D) | MaxDD 15.56→12.86%, Full Sharpe 1.16→1.13 | ✅ Kept — MaxDD improvement justifies small Sharpe cost |
| **ATR multiplier sweep 2.0×/2.5×/3.0×** (Part E) | 2.5× best Sharpe+Calmar balance | ✅ Kept — 2.5× is current production value |
| **RSI threshold rsi_oversold 5→15** (Part G) | Win rate +1.5–3pp BUT Sharpe worse in every period | ❌ Reverted — friction outweighs signal |
| **Regime-conditional stop multiplier** (Part F) | Bear 2022 Sharpe -0.04 vs 0.33 baseline | ❌ Rejected — decimates bear protection |
| **TrendPB regime-conditional profit target** (Parts I/J) | Marginal return gain (+0.5pp), no Sharpe improvement | ❌ Reverted — complexity not worth it |
| **RelativeStrength as 6th strategy** (Part K) | No meaningful Sharpe improvement | ❌ Reverted — dilutes capital without edge |
| **regime_stability_weeks 2→3** (2026-05-11) | Bull -0.80→-0.75 ✓, Live -0.81→-0.73 ✓, Bear 0.84→0.72 ✗, Recent 1.78→1.70 ✗ | ❌ Reverted — marginal gains in weak periods, meaningful loss in strong periods |
| **LLM prompt v2** (regime age + inferred trend + SWITCH) (2026-05-11) | Current production baseline — no pre-change reference available | ✅ Kept — no regression risk, richer context |

### Adaptive vs EqualWeight summary (current production, stability_weeks=2)

| Period | EqW Part H | Adaptive | Delta |
|--------|------------|----------|-------|
| Full 2018–2024 | 1.18 | **1.31** | +0.13 |
| Bull 2019–2020 | -0.57 | -0.80 | -0.23 |
| Crash 2020 | 2.19 | **2.35** | +0.16 |
| Recov 2020–2021 | 2.62 | **2.84** | +0.22 |
| Bear 2022 | 0.36 | **0.84** | +0.48 |
| Recent 2022–2024 | 1.24 | **1.78** | +0.54 |
| Live 2025–2026 | -0.60 | -0.81 | -0.21 |

Adaptive beats EqualWeight in 5/7 periods. It underperforms in both choppy periods (Bull 2019-2020 pre-COVID, Live 2025-2026 current). MaxDD is higher with Adaptive (16.9% vs 9.84%) due to deliberate concentration in single-strategy regimes.

---

## Improvement Backlog (Prioritised)

### HIGH — meaningful expected improvement, not yet implemented

**1. ~~Enable Adaptive+RCA in live paper trading~~ — already done**  
`run_paper_signals.py` already runs `AdaptiveStrategySelector` + `RegimeContextAgent` (Config C equivalent). LLM rebalances every 5 trading days, state persists across cron runs in SQLite (`api_state.db`). CB relaxation (`TRANSITION_UP` → 0.30 cap, `BEAR_EARLY` → 0.38 cap) is active. `_confirmed_weeks` was not persisted across runs until 2026-05-12 — now fixed.

**2. Fix cash gate weight-ordering for adaptive live trading**  
When LLM assigns non-equal weights, the sequential cash gate in `run_paper_signals.py` processes signals in symbol-arrival order — a low-weight strategy signal can consume cash meant for a high-weight strategy signal. In EqualWeight mode this is harmless (all 0.20). In Adaptive mode it causes capital misallocation.  
*File:* `api/run_paper_signals.py` — sort BUY decisions by `strategy_weight` descending before the cash gate loop.  
*Impact:* Zero on EqualWeight runs. Meaningful in Adaptive mode when weights diverge from 0.20.

**3. Update performance table with recent Sharpe data (2022–2026)**  
`_STRATEGY_REGIME_PERFORMANCE` in `adaptive_selector.py` is hardcoded from 2018–2024 backtests. TrendPB's CRASH_HIGHVOL Sharpe is 1.81 in that period (mostly COVID recovery). In the current 2025–2026 choppy crash, TrendPB is likely much lower. The LLM consistently allocates TrendPB=0.40 in CRASH_HIGHVOL based on this stale number. A "Recent 2022–2026" column in the table would give the LLM better calibration for current conditions.  
*Prerequisite:* Run per-strategy individual backtests for 2022–2026 to get strategy-level Sharpe breakdown.

---

### MEDIUM — reasonable hypothesis, not yet tested

**4. Max hold duration per strategy**  
Currently positions can be held indefinitely until ATR stop fires. In sideways/choppy markets, a position can sit for months making no progress while consuming capital. Adding `max_hold_days` (DualMA: 60d, Breakout/QuietBrk: 20d, TrendPB: 15d) would force capital recycling.  
*Risk:* May hurt bull/recovery periods where letting positions run is optimal. Must backtest.

**5. Widen `history_weeks` from 4 to 6**  
The LLM currently sees 4 weeks of regime history. Slow-moving regime shifts (e.g., a gradual bear building over 6 weeks) may not be visible in the 4-week window. Widening to 6 weeks costs ~8 extra tokens per prompt — negligible — and may help the LLM detect gradual deterioration earlier.  
*Risk:* Very low. Purely additive.

**6. Adaptive+RCA Config C backtest**  
We have Config A (EqW) and Config B (Adaptive) results but no Config C (Adaptive+RCA) run in the baseline runner. Adding this to `run_ujjwal_baseline.py --adaptive` would show whether the broad breadth signals and `TRANSITION_UP` regime actually improve results vs Config B.

---

### LOW / NOT RECOMMENDED — tested or low-signal

| Idea | Why not |
|------|---------|
| `regime_stability_weeks=3` | Tested 2026-05-11. Marginal gains in choppy periods (+0.05/+0.08) offset by losses in strong periods (-0.12/-0.08). Unfavorable tradeoff. |
| RSI threshold rsi_oversold 5→15 | Tested Part G. Win rate improves but net Sharpe worse in every period. Friction > signal. |
| Regime-conditional ATR stop multiplier | Tested Part F. Decimates Bear 2022 Sharpe (0.33→-0.04). |
| TrendPB regime-conditional profit target | Tested Parts I/J. +0.5pp return, no Sharpe benefit. Complexity not worth it. |
| RelativeStrength as 6th strategy | Tested Part K. No meaningful improvement, dilutes capital. |
| `regime_stability_weeks=1` | Would increase LLM call frequency and oscillation — opposite direction from the confirmed problem. |
