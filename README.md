# Financial Lab

**NSE Indian Equity Backtesting & Strategy Research System**

Research lab for modular, regime-aware trading strategy design on Indian equity markets.
All results are net of 0.10% commission + 0.05% slippage per side. Paper trading only.

---

## Current Results (March 2026)

Universe: 150 symbols (Nifty 50 + Nifty Next 50 + Nifty Midcap 50)
Pipeline: DynamicUniverseAgent (150 → top 80) → per-strategy filter (80 → top 20)

### Sharpe / Return% by Period

| Strategy | Full 2018–24 | Bull 2019–20 | Crash 2020 | Recovery 2020–21 | Bear 2022 | Recent 2022–24 |
|---|---|---|---|---|---|---|
| **DualMA SMA20/50** | 1.29 / +216% | 0.40 / +4% | 1.38 / +24% | **2.55 / +118%** | **0.56 / +8%** | **1.73 / +81%** |
| **Breakout 10d** | 1.12 / +155% | 0.49 / +6% | 1.49 / +25% | 2.48 / +102% | 0.39 / +4% | 1.15 / +41% |
| **QuietBrk 20d** | 1.05 / +146% | 0.98 / +14% | **2.00 / +35%** | **2.80 / +129%** | -0.67 / -10% | 0.67 / +22% |
| TrendPB 3% | 0.63 / +42% | 0.39 / +3% | 1.49 / +18% | 1.27 / +29% | -0.90 / -9% | 0.44 / +8% |
| TrendPB 5% | 0.80 / +39% | 0.97 / +5% | 1.80 / +16% | 1.23 / +22% | -0.34 / -2% | 0.89 / +12% |
| RSI-MR os=10 | -0.13 / -13% | -0.34 / -4% | 0.78 / +10% | 1.06 / +25% | -0.95 / -12% | -0.37 / -11% |
| RSI-MR os=5 | 0.25 / +15% | 0.21 / +2% | 0.86 / +11% | 1.37 / +33% | -0.66 / -9% | -0.11 / -5% |

**Good** = Sharpe > 1.0 | **OK** = Sharpe 0.3–1.0 | **Bad** = Sharpe < 0.3

### Key Observations

**Regime-strategy mapping is now clear:**

| Regime | Best Strategy | Sharpe | Why |
|---|---|---|---|
| Crash + Recovery | QuietBrk 20d | 2.00–2.80 | High-vol upward moves clear 20d highs cleanly |
| Recovery + Recent | DualMA | 1.73–2.55 | Sustained uptrend; golden crosses stay intact |
| Low-vol Bull | QuietBrk 20d | 0.98 | 0.8% threshold catches moves Breakout 10d misses |
| Bear | DualMA only | 0.56 | Exits on cross-under; all other strategies lose |
| Mixed/Recent | Breakout + DualMA | 1.15–1.73 | Both handle mixed volatility well |

**QuietBrk 20d** is the biggest new finding: it dominates Crash and Recovery (Sharpe 2.00 and 2.80) and is competitive in slow-bull (0.98) but suffers in Bear (-0.67). It should be paired with a regime gate or adaptive weight — not run unconditionally.

**DualMA** is the most consistent bear-survival strategy (+8% in Bear, +81% in Recent, +118% in Recovery). Its golden-cross filter naturally avoids entries when the market is broadly declining.

**RSI-MR** remains structurally weak outside Recovery. The `sma_cross_age >= 10` filter (R2) halved bear losses but RSI-MR 10 is still negative full-period. RSI-MR 5 (+15% full period) is the better variant if one must run it.

---

## System Architecture

```
Market Data (SQLite)
       │
       ▼
DynamicUniverseAgent          ← bulk preloads all 150 symbols, scores by activity
  (150 → top 80 candidates)     signals: relative_volume, daily_return, sma_cross_age,
                                  sma_20_above_sma_50, return_3d, rolling_vol_5d
       │
       ▼
Per-Strategy Universe Filter  ← strategy-specific re-ranking of the 80 candidates
  (80 → top 20 symbols)         BreakoutFilter     : vol spike + large price move
                                 PullbackFilter     : uptrend + quiet pullback
                                 MeanReversionFilter: uptrend + oversold (sma_cross_age≥10)
                                 DualMAFilter       : fresh golden cross (sma_cross_age 1–5)
       │
       ▼
MarketObserverAgent           ← computes per-symbol indicators from OHLC history
  (lazy preload per symbol)     sma_5/10/20/50, atr_5/14, rsi_2/3,
                                 high_10d, high_20d, regime classification
       │
       ▼
Strategy.decide()             ← pure rule-based signal generation
  BreakoutMomentumStrategy      entry: price > high_10d  |  exit: price < sma_10
  QuietBreakoutStrategy         entry: price > high_20d  |  exit: price < sma_20
  TrendPullbackStrategy         entry: pullback in uptrend  |  exit: price > sma_20×1.05
  DualMovingAverageStrategy     entry: sma_20 crosses above sma_50  |  exit: cross below
  RSIMeanReversionStrategy      entry: RSI_3 < threshold  |  exit: RSI overbought or time-stop
       │
       ▼
RiskAgent                     ← position sizing + regime gate + breadth circuit breaker
  vol-adjusted sizing           risk_per_trade = 0.5% of portfolio / (2 × ATR)
  ATR stop (2×ATR)              hard stop checked on every HOLD decision
  regime filter                 e.g. UPTREND_ONLY blocks entry in DOWNTREND stocks
  breadth circuit breaker       blocks BUY when >40% of universe in DOWNTREND (R1)
       │
       ▼
ExecutionAgent + Portfolio    ← fills at close price with commission + slippage
       │
       ▼
EvaluationAgent               ← Sharpe, MaxDD, profit factor, win rate, trade count
```

### Strategy Files

| File | Strategy | Entry Signal | Exit Signal | Horizon |
|---|---|---|---|---|
| `app/strategy/breakout_momentum.py` | BreakoutMomentumStrategy | price > high_10d | price < sma_10 | 3–10d |
| `app/strategy/quiet_breakout.py` | QuietBreakoutStrategy | price > high_20d | price < sma_20 | 5–20d |
| `app/strategy/trend_pullback.py` | TrendPullbackStrategy | pullback in confirmed uptrend | price > sma_20×1.05 | 5–15d |
| `app/strategy/dual_ma.py` | DualMovingAverageStrategy | sma_20 crosses above sma_50 | sma_20 crosses below sma_50 | weeks–months |
| `app/strategy/rsi_mean_reversion.py` | RSIMeanReversionStrategy | RSI_3 < threshold | RSI overbought or max_hold_days | 1–7d |

### Universe Filter Files

| Class | Strategy | Key Filters |
|---|---|---|
| `BreakoutUniverseFilter` | Breakout 10d | rel_vol > 1.5, abs_return > 1.5% |
| `BreakoutUniverseFilter` (relaxed) | QuietBrk 20d | rel_vol > 1.2, abs_return > 0.8% |
| `PullbackUniverseFilter` | TrendPB | sma_20>sma_50, slope+, return_3d in [-12%, -1.5%], low volume |
| `MeanReversionUniverseFilter` | RSI-MR | sma_20>sma_50, sma_cross_age≥10, return_3d < -3% |
| `DualMAUniverseFilter` | DualMA | sma_20>sma_50, sma_cross_age 1–5, rel_vol > 0.8 |

---

## Improvements Applied (R-series)

| ID | Change | Impact |
|---|---|---|
| R1 | Breadth circuit breaker 60% → 40% | Breakout Bull improved -0.01 → +0.49; RSI-MR Bear halved losses |
| R2 | `sma_cross_age >= 10` in MeanReversionFilter | RSI-MR full-period -29% → -13%; Bear -21% → -12% |
| R3 | ~~`sma_cross_age >= 15` in PullbackFilter~~ | **Reverted** — harmed TrendPB Recovery without fixing Bear |
| B1 | DualMA strategy with DualMAUniverseFilter | +216% full period; best bear-survival strategy |
| B2 | QuietBreakoutStrategy (20d, relaxed filter) | Best Crash/Recovery performer (2.00/2.80 Sharpe) |

---

## Next Steps

### Priority 1 — Adaptive Strategy Selector (LLM meta-layer)

The regime-strategy mapping is now clear enough to build a meta-layer that dynamically
allocates capital between strategies based on current market conditions.

**Design** (see `docs/adaptive_strategy_selector.md` for full spec):

```
Weekly: RegimeSnapshot → AdaptiveStrategySelector (Claude API) → strategy weight vector
Daily:  weight vector → MultiStrategyRouter → RiskAgent (weight scales position size)
```

The LLM receives the current regime distribution (% uptrend/downtrend, ATR level,
breadth) plus the historical Sharpe table above and outputs a capital weight per
strategy. Called weekly (not daily) to avoid latency overhead.

**Pre-requisites before building the selector:**

1. **RSI-MR HOLD emission** — RSI-MR does not emit HOLD for held positions, silently
   disabling the ATR stop. Fix: add explicit HOLD in the `in_position` branch (same
   pattern as BreakoutMomentumStrategy and TrendPullbackStrategy).

2. **QuietBrk 20d Bear regime gate** — QuietBrk loses -10% in Bear. Either:
   - Add `_UPTREND_ONLY` as its `allowed_regimes` (currently `_TREND_AND_SIDEWAYS`), or
   - Let the adaptive selector weight it to 0 in bear conditions.

3. **MultiStrategyRouter** — wraps all strategies, merges decisions (SELL overrides BUY,
   highest-weight strategy wins per symbol). Add `weight` and `source` fields to `Decision`.

**Expected impact:** In Recovery 2020-21, QuietBrk (2.80) and DualMA (2.55) both
dominated. A selector routing 60% to QuietBrk + 30% to DualMA in that regime would
significantly outperform running either alone at full capital. In Bear 2022, routing
80% to DualMA and 20% to Breakout (and 0% to everything else) avoids all the losing
strategies.

**Is the LLM the right tool?** Yes, for this specific task:
- 5 strategies × 4 regime dimensions = too many combinations to hand-tune
- The mapping is pattern-matching with interacting variables, not a deterministic rule
- Claude already "knows" the trade-offs (provided via the prompt's performance table)
- A rules-based version requires 50+ manually tuned thresholds; the LLM infers them

See `docs/adaptive_strategy_selector.md` for full architecture, prompt design,
MultiStrategyRouter pseudocode, and implementation order.

### Priority 2 — TrendPB Structural Fix or Replacement

TrendPB 3% is still -9% in Bear 2022. The `sma_cross_age >= 15` filter (R3) was
reverted because it harmed Recovery without fixing Bear. Two options:

- **Fix**: Add volume confirmation on entry — only buy the pullback if volume on
  pullback days is below 20-day average. Distribution (high volume pullback) vs
  healthy rotation (low volume pullback) is the key distinction.
- **Replace**: Donchian channel breakout (20d high + volume confirmation) — similar
  to QuietBrk but with a price-channel rather than SMA exit.

### Priority 3 — RSI-MR 10 vs RSI-MR 5

RSI-MR 10 is -13% full period; RSI-MR 5 is +15%. They share the same universe filter
and risk settings — the only difference is the entry threshold. Consider retiring
RSI-MR 10 from the active strategy pool. Running two variants of the same broken
strategy adds noise without diversification.

### Priority 4 — QuietBrk 20d Bear Regime Gate

QuietBrk 20d loses -10% in Bear 2022 vs +35% in Crash and +129% in Recovery. Its
`allowed_regimes` is currently `_TREND_AND_SIDEWAYS`. Switching to `_UPTREND_ONLY`
(block entries when per-stock regime is DOWNTREND) may reduce Bear losses at the cost
of fewer Crash entries — worth testing since the ATR stop already limits per-trade
losses.

---

## Running Experiments

```bash
# Activate environment
source finance/bin/activate

# Run all strategies across all periods
python3 run_experiments.py
```

Results print per-period with Sharpe, return, max drawdown, profit factor, win rate,
and trade count. Each period independently preloads and caches data — runs are
fully reproducible.

---

## Repository Layout

```
app/
  backtest/
    engine.py          # BacktestEngine — daily loop, universe filtering, P&L tracking
    observer.py        # MarketObserverAgent — per-symbol indicator precomputation
  data/
    models.py          # OHLCRecord, MarketState data models
    repository.py      # MarketDataRepository — SQLite OHLC access
  evaluation/
    agent.py           # EvaluationAgent — Sharpe, MaxDD, profit factor
  execution/
    agent.py           # ExecutionAgent — fill simulation with costs
  features/
    indicators.py      # SMA, ATR, RSI implementations
  portfolio/
    engine.py          # PortfolioEngine — position state, equity valuation
    models.py          # Portfolio dataclass
  risk/
    agent.py           # RiskAgent — sizing, ATR stop, regime gate, breadth CB
  strategy/
    base.py            # BaseStrategyAgent interface
    breakout_momentum.py   # Breakout 10d
    quiet_breakout.py      # Quiet Breakout 20d (B2)
    trend_pullback.py      # TrendPullback v2
    dual_ma.py             # DualMA golden cross (B1)
    rsi_mean_reversion.py  # RSI Mean Reversion
  universe/
    dynamic_agent.py   # DynamicUniverseAgent — bulk 150-symbol scanner
    filters.py         # Per-strategy universe filters (Breakout/Pullback/MeanRev/DualMA)
    models.py          # UniverseCandidate dataclass
    agent.py           # UniverseSelectionAgent (legacy fallback)
docs/
  improvement_roadmap.md         # Full before/after analysis of R1/R2/R3/B1/B2
  adaptive_strategy_selector.md  # LLM meta-layer design spec
  roadmap_next_improvements.md
  experiment_results_analysis.md
run_experiments.py     # Main experiment runner — all strategies × all periods
scripts/               # Data ingestion scripts
```

---

## Disclaimer

Research and educational purposes only. No financial advice. No live trading.
