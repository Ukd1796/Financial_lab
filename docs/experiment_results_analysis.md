# Experiment Results Analysis

---

## P0 Fixes — Status: ✅ All Applied

| Fix | File | Status |
|---|---|---|
| Equity valuation — stranded positions priced at $0 | `engine.py` — `_last_known_prices` + `equity_prices` | ✅ Fixed |
| WR and #Trades always showing 0 | `run_experiments.py` — `_print_row` key names | ✅ Fixed |
| Held positions never receiving exit signals | `engine.py` — union with `portfolio.positions.keys()` | ✅ Fixed |

**Impact:** Max drawdowns dropped from 90–96% to 5–24%. Trade counts and win rates now reflect actual activity. Results are now interpretable.

---

## What the New Results Show

### What is working correctly

- **Breakout 10d** is the strongest strategy across all periods — 248% full-period return, Sharpe 1.87, MaxDD 10.68%, 3,514 trades. It is naturally synergistic with the dynamic universe filter because high-volume breakout stocks are exactly what the filter selects.
- **DualMA** performs well in sustained trends — 87% return in Recovery 2020–2021, 55% in Recent 2022–2024, good Sharpe and controlled drawdowns.
- **TrendPullback** is consistently profitable with high win rates (62–67%) and modest but stable returns. The smaller trade count means lower transaction costs in practice.
- **RSI-MR** is marginally positive over the full period but struggles in directional markets, which is expected for a mean-reversion strategy.
- Drawdowns are now realistic (5–24%) and Sharpe ratios are comparable across strategies.

### What is still broken or misleading

---

## Remaining Issue 1 — CS Strategy Still Produces Zero Activity for Short Periods

**Status:** P1 — confirmed from results

All three CS variants show `0.00 / 0.00% / 0.00%` for every period shorter than the full 2018–2024 run.

**Root cause:** `CrossSectionalMomentumStrategy` builds its `price_history` by appending prices from `symbol_states` each day. With the dynamic universe giving a rotating set of 20 stocks daily, any individual stock appears sporadically. For `lookback_days=100`, a stock needs 100 consecutive days of history to produce a momentum score. In a 250-day period this is very unlikely to happen for enough stocks to cross the `momentum_threshold`.

For the Full 2018–2024 run it does eventually work because over 1,500+ trading days enough stocks accumulate history — but only because the observer cache is pre-warmed by prior strategy runs in the shared `PeriodContext`.

**Also observed:** CS L=100 T=5% and CS L=100 T=3% produce **identical** results (35 trades, 37.51%). This means the `momentum_threshold` is not the binding constraint — the lookback window is. Any stock that clears 100 days of history already has momentum well above both thresholds.

**Fix needed:**
CS strategy should source price history from the observer's preloaded data (which covers the full date range with a 300-day warm-up buffer) rather than accumulating prices one day at a time through `symbol_states`. This means giving the CS strategy access to the repository or a pre-built price matrix at initialisation.

---

## Remaining Issue 2 — RiskAgent Equity Calculation Understates Portfolio Value

**Status:** P1 — newly identified

**Location:** `app/risk/agent.py`

```python
total_equity   = portfolio.total_equity({symbol: current_price})
max_allocatable = total_equity * self.max_position_pct
```

`total_equity` is called with a single-symbol price dict. All other open positions are valued at **$0** inside this call, so `total_equity` equals only `cash + (this symbol's position value)`. As positions accumulate, the true portfolio value grows but this calculation doesn't see it. The result:

- Position sizes shrink progressively as more positions are held
- The system behaves as if it's nearly out of capital even when significant unrealized gains are sitting in other positions
- Over-concentration in early positions, under-sizing in later ones

**Fix needed:** Pass the full `equity_prices` dict (maintained per day in the engine) through to `RiskAgent.evaluate()`, or change the allocation logic to use `portfolio.cash` for buy sizing (simpler and avoids the cross-dependency).

---

## Remaining Issue 3 — `evaluate_trades` Returns `{}` for Zero-Trade Strategies

**Status:** P2 — cosmetic but misleading

**Location:** `app/evaluation/agent.py`

```python
def evaluate_trades(self, trades):
    if not trades:
        return {}     # ← all keys missing, _print_row shows 0.00 for everything
```

When a strategy produces no completed trades (e.g. CS in short periods), `evaluate_trades` returns an empty dict. `_print_row` falls back to 0.0 for PF and WR, making a zero-activity strategy look identical in format to a bad-performing one. A zero-trade result should display as `—` or `N/A` to distinguish "strategy never fired" from "strategy fired and lost".

**Fix needed:** Return a zero-filled dict with a `"no_trades": True` flag, or check for empty `trade_metrics` in `_print_row` and print a distinct placeholder row.

---

## Remaining Issue 4 — Regime Filter Behaviour in Short Bear/Mixed Periods

**Status:** P1 — partially confirmed

**Location:** `app/risk/agent.py`

```python
self.allowed_regimes = ["LOW_VOL_UPTREND", "MID_VOL_UPTREND", "HIGH_VOL_UPTREND"]
```

In Bull 2019–2020, DualMA shows only 18 trades at 22% win rate, producing -4.8% return in a period where the market was trending up. The regime filter is blocking many valid BUY signals from stocks classified as `SIDEWAYS` or briefly dipping into `DOWNTREND`. The regime classification uses SMA_50 slope, which can lag real trend changes by weeks.

RSI-MR in Crash 2020 shows a positive 0.95% return (good) with 65 trades — this works because RSI-MR generates buys on oversold dips, some of which are in uptrend regimes briefly during the crash recovery intra-year.

**Fix needed:** Either make `allowed_regimes` a per-strategy parameter passed through `run_experiment`, or add `SIDEWAYS` regimes to the allowed set. Short-term strategies in particular should not be regime-filtered the same way as medium-term ones.

---

## Metric Interpretation Guide (Post P0 Fixes)

| Metric | Reliability now |
|---|---|
| **Return** | ✅ Reliable — based on real equity changes with correct position pricing |
| **Max Drawdown** | ✅ Reliable — realistic 5–24% range, no longer dominated by $0-pricing artefact |
| **Sharpe** | ✅ Reliable — consistent with return/drawdown relationship |
| **WR** | ✅ Reliable — correct key now used |
| **#Trades** | ✅ Reliable — correct key now used |
| **PF** | ⚠️ Shows 0.00 for CS zero-trade rows — misleading (see Issue 3) |
| **CS results in short periods** | ❌ All zeros — strategy architectural issue (see Issue 1) |

---

## Updated Priority Fix List

### P1 — Fix for correct strategy behaviour

1. **CS strategy: decouple price history from daily `symbol_states`** — pre-build a full price matrix from the observer cache (or repository) at strategy initialisation so lookback momentum can be computed properly regardless of universe size
2. **RiskAgent: pass full `equity_prices` for position sizing** — replace `portfolio.total_equity({symbol: price})` with the full daily price map so allocation is based on true portfolio value
3. **Regime filter: make it per-strategy** — short-term strategies (RSI-MR, TrendPB) should not share the same uptrend-only regime gate as medium-term ones; pass `allowed_regimes` as a parameter in the strategy config

### P2 — Quality improvements

4. **`evaluate_trades`: return structured zeros instead of empty dict** — display `N/A` rows for strategies that never fire rather than ambiguous 0.00s
5. **Universe filter: expose thresholds as experiment parameters** — `volume_threshold` and `volatility_threshold` should be part of the experiment config so they can be swept alongside strategy parameters
6. **Add time-based position stop** — maximum hold days per position to prevent positions lingering indefinitely when exit conditions are never met (especially relevant for DualMA in sideways markets)

---

## Strategy Summary (Full 2018–2024)

| Strategy | Return | Sharpe | MaxDD | #Trades | Assessment |
|---|---|---|---|---|---|
| Breakout 10d | 248.85% | 1.87 | 10.68% | 3,514 | Best overall — synergistic with universe filter |
| DualMA SMA20/50 | 149.00% | 1.23 | 23.90% | 204 | Good in trends, high drawdown |
| CS L=80 R=20 T=5% | 146.00% | 1.31 | 21.21% | 57 | Promising but only works over long periods |
| CS L=100 variants | 37.51% | 0.65 | 16.24% | 35 | Lookback too long for rotating universe |
| TrendPB 3% | 10.70% | 0.33 | 10.24% | 644 | Stable, low drawdown, good for combining |
| RSI-MR variants | ~1% | ~0.05 | ~10% | 300–345 | Near-flat; mean reversion limited in trends |
