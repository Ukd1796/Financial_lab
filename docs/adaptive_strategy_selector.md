# Adaptive Strategy Selector — Design & Integration Guide

**Last updated**: 2026-03-22
**Status**: Fully implemented. Running in `run_experiments.py` (backtest) and `run_signals.py` (live paper trade).

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

### 2.1 Per-regime Sharpe matrix (2026-03-21 run — pre all fixes)

| Strategy | Bull 19–20 | Crash 20 | Recov 20–21 | Bear 22 | Recent 22–24 | Full 18–24 |
|---|---|---|---|---|---|---|
| DualMA SMA20/50 | 0.44 | 1.28 | 2.66 | **0.51** | **1.69** | **1.33** |
| Breakout 10d | 0.93 | 1.72 | **3.18** | -0.05 | 1.06 | 1.25 |
| QuietBrk 20d | **1.09** | 1.38 | 2.33 | -0.05¹ | **1.08** | 0.89 |
| TrendPB 5% | 0.97 | **1.81** | 1.19 | -0.34 | 0.90 | 0.79 |
| RSI-MR os=5 | 0.15 | 0.88 | 1.34 | -0.65 | -0.14 | 0.22 |
| **EqualWeight** | -0.52 | **2.41** | 2.84 | **+0.29** | 1.24 | 1.19 |

**Note**: Updated backtest with all 2026-03-22 fixes (RECOVERY threshold, BULL_SUSTAINED,
DualMA floor, regime stability gate, min ATR filter, CB 0.35) has not yet been re-run.
Run `python run_experiments.py` to get updated benchmark numbers.

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

### Backtest mode (`run_experiments.py`)
```
BacktestEngine.run()
  for each day:
    ① dynamic_universe_agent.select_candidates()   → 80 UniverseCandidates
    ② UnionUniverseFilter.select_symbols()          → 60–80 unique symbols
    ③ observer.run_for_day() × N                   → daily_symbol_states
    ④ [weekly] AdaptiveStrategySelector.rebalance() → weight dict
               build_regime_snapshot()              → LLM input
               _classify_regime() Python classifier → explicit label
               GPT-4o-mini → normalised weight vector
               regime_stability_weeks=2 gate        → prevents whipsaw
    ⑤ MultiStrategyRouter.decide()                 → merged decisions
               per-strategy allowed_regimes filter
               ownership gate (position_owners dict)
               SELL > BUY > HOLD conflict resolution
    ⑥ RiskAgent.evaluate()                         → sized decisions
               breadth CB (max_downtrend_pct=0.35)
               min ATR-to-cost filter (min_atr_cost_ratio=3.0)
               ATR stop, weight-scaled position sizing
    ⑦ execution_agent.execute()                    → fills + portfolio update
```

### Live paper trade mode (`run_signals.py` + `run_orders.py`)
```
3:35 PM IST — run_signals.py
    ① NSECalendar.is_trading_day() check
    ② yfinance EOD fetch → upsert market_ohlc
    ③ 300-day history load for warm-up
    ④–⑥ Same universe/observer/regime pipeline as backtest
    ⑦ _load_selector_state() from selector_state DB table
    ⑧ AdaptiveStrategySelector.rebalance() — with stability gate
    ⑨ _save_selector_state() → selector_state DB table
    ⑩ PaperAdapter.get_positions() → reconstruct Portfolio + position_owners
    ⑪ MultiStrategyRouter.decide()
    ⑫ RiskAgent.evaluate() (breadth CB + min ATR)
    ⑬ _write_signals() → signal_queue DB (status=PENDING)
    ⑭ send_email() → Gmail summary to user

9:15 AM IST next day — run_orders.py
    ① Cancel stale PENDING signals (older than 1 trading day)
    ② Load PENDING signals from prev trading day
    ③ Assign PAPER-xxx order IDs → status=PLACED
    ④ PaperAdapter.get_order_status() → simulate fill at next-day open
    ⑤ _update_live_position() → upsert live_positions DB
    ⑥ send_email() → fill confirmation summary
```

### File map

```
app/
  backtest/engine.py         ← adaptive_selector param ✅
  meta/
    regime_snapshot.py       ← build_regime_snapshot() ✅
    adaptive_selector.py     ← BULL_SUSTAINED, stability gate, DualMA floor ✅
  strategy/
    multi_router.py          ← position_owners ownership gate ✅
    models.py                ← Decision.weight, Decision.source ✅
  universe/filters.py        ← UnionUniverseFilter ✅
  risk/agent.py              ← min_atr_cost_ratio, breadth CB 0.35 ✅
  broker/
    base.py                  ← BrokerAdapter ABC ✅
    paper_adapter.py         ← fills at next-day open ✅
    models.py                ← Order, BrokerPosition dataclasses ✅
  data/
    calendar.py              ← NSECalendar, 2025-2026 holidays ✅
    models.py                ← SignalQueue, LivePosition ORM models ✅
  core/
    database.py              ← env-var DATABASE_URL ✅
    notify.py                ← Gmail SMTP email helper ✅
run_experiments.py           ← EqualWeight + Adaptive backtest ✅
run_signals.py               ← daily signal job (3:35 PM IST) ✅
run_orders.py                ← morning fill job (9:15 AM IST) ✅
railway.toml                 ← two cron services for Railway.app ✅
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
| 2 | Breadth CB 60%→40% | ✅ Done | 2026-03-17 | RSI-MR Bear losses halved |
| 3 | sma_cross_age for RSI-MR | ✅ Done | 2026-03-17 | False uptrend entries eliminated |
| 4 | DualMA strategy + filter | ✅ Done | 2026-03-19 | Sharpe 1.69 Recent, 2.66 Recovery |
| 5 | QuietBrk 20d strategy + filter | ✅ Done | 2026-03-19 | |
| 6 | Retire CS momentum | ✅ Done | 2026-03-19 | Commented out of experiments |
| 7 | QuietBrk Bear regime gate | ✅ Done | 2026-03-19 | `_UPTREND_ONLY` — Bear loss near-zero |
| 8 | Retire RSI-MR os=10 | ✅ Done | 2026-03-19 | os=5 dominates in every period |
| 9 | Decision.weight + .source | ✅ Done | 2026-03-19 | `app/strategy/models.py` |
| 10 | MultiStrategyRouter | ✅ Done | 2026-03-21 | Position ownership gate |
| 11 | build_regime_snapshot() | ✅ Done | 2026-03-21 | `app/meta/regime_snapshot.py` |
| 12 | AdaptiveStrategySelector | ✅ Done | 2026-03-21 | GPT-4o-mini, Python classifier |
| 13 | Wire into BacktestEngine | ✅ Done | 2026-03-21 | `adaptive_selector=None` optional |
| 14 | EqualWeight baseline | ✅ Done | 2026-03-21 | UnionUniverseFilter |
| 15 | Adaptive vs EqualWeight | ✅ Done | 2026-03-21 | In `run_experiments.py` |
| 16 | RECOVERY threshold 0.018→0.022 | ✅ Done | 2026-03-22 | Fixes NSE bull over-trigger |
| 17 | BULL_SUSTAINED regime | ✅ Done | 2026-03-22 | Replaces RECOVERY misfire in 2023-24 bull |
| 18 | DualMA minimum floor 0.10 | ✅ Done | 2026-03-22 | `_parse_weights()` |
| 19 | Regime stability gate (2-week) | ✅ Done | 2026-03-22 | `regime_stability_weeks=2` |
| 20 | Min ATR-to-cost filter | ✅ Done | 2026-03-22 | `min_atr_cost_ratio=3.0` in RiskAgent |
| 21 | Breadth CB tightened 0.40→0.35 | ✅ Done | 2026-03-22 | `max_downtrend_pct=0.35` |
| 22 | Paper trade pipeline | ✅ Done | 2026-03-22 | `run_signals.py` + `run_orders.py` |
| 23 | Selector state persistence | ✅ Done | 2026-03-22 | `selector_state` DB table |
| 24 | Email notifications | ✅ Done | 2026-03-22 | `app/core/notify.py` |
| 25 | Railway.app deployment | ✅ Done | 2026-03-22 | `railway.toml`, two cron services |
| — | Re-run backtest with all fixes | ❌ Pending | — | Run `python run_experiments.py` |
| — | Earnings date avoidance gate | ❌ Pending | — | Build before April Q4 season |

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

## 8. Actual Results (2026-03-21 run, pre all fixes)

| Run | Sharpe | Return | MaxDD |
|---|---|---|---|
| EqualWeight (5-strat) | 1.23 | +101.06% | 15.18% |
| Adaptive (LLM weights) | 1.18 | +114.74% | 22.03% |
| Bear 2022 — Adaptive | **1.30** | **+12.56%** | 8.34% |
| Bear 2022 — EqualWeight | 0.27 | +1.88% | 15.21% |

**Post-fix backtest pending.** Expected improvements from 2026-03-22 changes:
- Bull 2019 losses reduced (min ATR filter blocks low-quality entries in choppy low-vol markets)
- 2023-24 allocation improved (BULL_SUSTAINED gives DualMA 0.25 vs previous 0.15-0.17)
- Less allocation churn (stability gate stops weekly RECOVERY↔BEAR flips)
- Full-period Sharpe expected to be ≥ 1.25 (up from 1.18)

**Key ongoing risk:** Look-ahead bias in the embedded Sharpe table. Live performance will
be ~0.80-0.90× the backtest Sharpe until walk-forward validation (Priority 5) is built.

---

## 9. Known Open Issues

- **TrendPB Bear losses** — selector weights it low in bear, but per-trade losses still
  occur at low weight. Structural fix (volume confirmation on entry) remains open.

- **Bull 2019-20 underperformance** — Min ATR filter (done 2026-03-22) is expected to
  reduce drag. Signal persistence (2-day confirmation) would reduce it further — not yet built.

- **Inter-strategy correlation** — DualMA and Breakout both favour trending stocks.
  In Recovery they often enter the same names simultaneously. Per-sector concentration
  limit in RiskAgent (Priority 6) not yet built.

- **Walk-forward validation** — Sharpe table is derived from same data being backtested.
  Live performance will be ~0.8-0.9× backtest until walk-forward validation built.

- **Bear-exit lag** — The regime stability gate prevents whipsaw but also slows
  Recovery entry by 1 additional week. This is an acceptable trade-off for paper trade;
  revisit if Recovery Sharpe degrades.
