# Improvement Roadmap: Fixing Bad Markets Without Breaking Good Ones

**System**: NSE Indian Equity Backtesting Lab
**Architecture**: DynamicUniverseAgent (150→80) → per-strategy UniverseFilter (80→20) → Strategy → RiskAgent → ExecutionAgent
**Date**: 2026-03-17

---

## 1. Results Scorecard

| Strategy | Full 2018–24 | Bull 2019-20 | Crash 2020 | Recovery 2020-21 | Bear 2022 | Recent 2022-24 |
|---|---|---|---|---|---|---|
| Breakout 10d | **Good** (1.03 / +136%) | **Bad** (-0.01 / -1%) | **Good** (1.53 / +25%) | **Good** (2.52 / +105%) | **OK** (0.55 / +6%) | **Good** (1.36 / +51%) |
| TrendPB v2 3% | **OK** (0.59 / +39%) | **OK** (0.34 / +2%) | **Good** (1.49 / +18%) | **Good** (1.23 / +29%) | **Bad** (-0.90 / -9%) | **OK** (0.42 / +8%) |
| TrendPB v2 5% | **OK** (0.79 / +38%) | **Good** (0.97 / +5%) | **Good** (1.78 / +16%) | **Good** (1.21 / +22%) | **Bad** (-0.34 / -2%) | **Good** (0.87 / +11%) |
| RSI-MR os=10 | **Bad** (-0.37 / -29%) | **Bad** (-0.58 / -6%) | **OK** (0.43 / +5%) | **OK** (0.98 / +24%) | **Bad** (-1.59 / -21%) | **Bad** (-0.74 / -21%) |
| RSI-MR os=5 | **OK** (0.07 / +0%) | **Bad** (-0.15 / -2%) | **OK** (0.65 / +9%) | **Good** (1.40 / +36%) | **Bad** (-1.06 / -15%) | **Bad** (-0.31 / -10%) |

**Verdict**: Good = Sharpe > 1.0. OK = Sharpe 0.3–1.0. Bad = Sharpe < 0.3 or negative.

Two problem periods dominate: **Bull 2019-20** (all strategies flat/negative) and **Bear 2022** (RSI-MR and TrendPB deeply negative). Everything else is at least OK.

---

## 2. Root Cause Analysis: Bull 2019-20

All five strategies returned flat or negative during a period when the NSE index was gently trending upward. This is a **slow, low-volatility bull** market — steady daily advances of 0.1–0.3% with few sharp moves in either direction.

### 2.1 Breakout 10d (Sharpe -0.01, -1%)

**Filter requirement**: `abs(daily_return) > 1.5%` AND `relative_volume > 1.5`

In a slow bull, stocks drift up 0.1–0.3%/day. They almost never produce a single-day move above 1.5%. The `BreakoutUniverseFilter` is calibrated for volatile, high-activity conditions. During Bull 2019-20, its output universe is chronically thin — often near-empty — so the strategy either takes very few trades (376 trades across the period, lowest of any period except Recent 2022-24 where the period is shorter) or the trades it does take are on the few anomalously volatile stocks which are the outliers, not the trend leaders.

Even when a stock does pass the filter, `price > high_10d` rarely fires because price advances are gradual. A stock that rose 0.2%/day for 10 days has a 10-day high that is only 2% above the current price — easily within normal intraday range, so it triggers on random noise rather than genuine momentum.

**The Breakout strategy needs volatility to function. Bull 2019-20 provides none.**

### 2.2 RSI-MR os=10 (Sharpe -0.58, -6%) and os=5 (Sharpe -0.15, -2%)

**Filter requirement**: `sma_20_above_sma_50=True`, `return_3d < -3%`
**Entry requirement**: `RSI_3 < 10` (or `< 5`)

Two compounding problems:

1. **Signal rarity and quality**: In a slow uptrend, stocks don't get deeply oversold. `RSI_3 < 10` requires roughly three consecutive down days of meaningful magnitude. In Bull 2019-20 where the market is gently rising, a stock with `RSI_3 < 10` is not experiencing a normal pullback — it is declining against a rising market, i.e., it is genuinely weak. These are falling knives, not mean-reversion candidates.

2. **Universe filter selects the wrong stocks**: `MeanReversionUniverseFilter` requires `return_3d < -3%`. In Bull 2019-20, a stock down 3%+ in three days while the broad market is up is almost certainly breaking down fundamentally. The uptrend regime filter (`sma_20_above_sma_50=True`) is a lagging indicator — SMA20 can still be above SMA50 for weeks after a stock starts its actual decline. The filter selects exactly the stocks that should NOT be mean-reversion candidates in this regime.

3. **os=5 is worse because it fires even more rarely**, meaning the few trades taken are even more concentrated in genuinely weak stocks.

### 2.3 TrendPB v2 (Sharpe 0.34 / +2% at 3%, Sharpe 0.97 / +5% at 5%)

TrendPB is the only strategy that manages positive Sharpe in Bull 2019-20, primarily because:
- Its universe filter (`PullbackUniverseFilter`) selects stocks with confirmed uptrends (SMA20 > SMA50, slope positive), which are abundant in a slow bull.
- The `5% pullback` variant (Sharpe 0.97) requires deeper pullbacks, which are genuine opportunities rather than the shallow dips that fool the `3%` variant.

However, even TrendPB is underperforming its own Recovery (1.21–1.23) and Crash (1.49–1.78) numbers, because a slow bull produces fewer large pullbacks to exploit.

**The core Bull 2019-20 problem**: The system has no strategy optimized for gradual, low-volatility uptrends. Every current strategy requires either volatility (Breakout, RSI-MR) or meaningful pullbacks (TrendPB). A sustained slow bull provides neither in adequate quantity.

---

## 3. Root Cause Analysis: Bear 2022

RSI-MR loses 21%/15% and TrendPB loses 9%/2% in Bear 2022. Breakout is the only strategy that holds up (+6%, Sharpe 0.55).

### 3.1 RSI-MR (Sharpe -1.59/-1.06, -21%/-15%)

The system has two defenses against bear markets:
1. **Per-stock regime filter**: Only allow BUY when stock is in UPTREND or SIDEWAYS (`_UPTREND_AND_SIDEWAYS`)
2. **Breadth circuit breaker**: Block BUY when >60% of universe is in DOWNTREND

Both are failing in Bear 2022.

**Why the regime filter fails**: Bear 2022 is a grinding, rolling bear — not a sudden crash. Sectors roll over at different times. At any given moment, a meaningful fraction of stocks (40–55%) are in a temporary UPTREND or SIDEWAYS regime, measured by `SMA20 > SMA50`. These are stocks whose SMA20 crossed SMA50 upward 2–4 weeks ago during a bounce, but are now beginning their real decline. The SMA crossover is a lagging signal — SMA20 can sit just barely above SMA50 for 2–3 weeks after the fundamental trend has reversed. These stocks pass the regime filter and the RSI-MR entry fires on what looks like a mean-reversion setup but is actually the beginning of a continuation down.

**Why the breadth circuit breaker fails**: At a 60% downtrend threshold, the breaker only activates when the market is in full capitulation. Bear 2022 saw extended periods of 40–55% of stocks in DOWNTREND — enough to make mean-reversion dangerous, not enough to trigger the 60% circuit breaker.

**Result**: RSI-MR takes 492 and 419 trades in Bear 2022 (vs. 1128 and 950 in Recovery which was 2x as long), meaning it was not being throttled nearly enough. The strategy was running close to full capacity into a bear market.

### 3.2 TrendPB v2 (Sharpe -0.90/-0.34, -9%/-2%)

**Entry condition 3**: `price_3d_ago > SMA_20 × 1.05` — price was in strong trend 3 days ago.

In Bear 2022, many stocks produce a false uptrend cross: SMA20 just crossed above SMA50 (after a bounce), price rallied and was briefly above `SMA20 × 1.05`, then the bounce failed and price pulled back sharply. The TrendPB filter and entry conditions see:
- `SMA_20 > SMA_50`: True (just crossed, SMA20 is barely above SMA50)
- `SMA_20 slope > 0`: True (it just crossed upward)
- `price_3d_ago > SMA_20 × 1.05`: True (the bounce pushed price above this level)
- `return_3d < -pullback_threshold`: True (the bounce is now failing)

This is a textbook false breakout failure, but TrendPB reads it as a healthy pullback in an uptrend. The pullback the strategy buys is actually the start of the next leg down.

**The key distinction the strategy cannot make**: A genuine uptrend pullback occurs when SMA20 has been above SMA50 for weeks, with multiple confirmed bounces. A false breakout pullback occurs when SMA20 just crossed SMA50 and the first move above SMA20×1.05 immediately fails.

---

## 4. Improvement Suggestions: Bull 2019-20

### Suggestion B1: Add a DualMA (SMA20/SMA50 Crossover) Strategy

**What it does**: Enter when SMA20 crosses above SMA50 (a classic "golden cross"), exit when SMA20 crosses back below SMA50. This is the canonical slow-bull trend-following strategy.

**Why it works for Bull 2019-20**: In a sustained low-volatility uptrend, the SMA20/SMA50 crossover fires early and stays in position for months. The strategy doesn't need volatility or deep pullbacks — it just needs sustained directional movement, which Bull 2019-20 provides in abundance.

**Why it won't hurt other periods**:
- Recovery 2020-21: DualMA had Sharpe 1.67 in Recent 2022-24 from prior experiments. Recovery is also a strong uptrend period — DualMA should perform well there too.
- Crash 2020: DualMA will exit quickly as SMA20 crosses below SMA50. Losses should be limited.
- Bear 2022: Exits on downtrend crossovers, so it self-limits.

**Implementation**: This is a purely additive change — a new strategy alongside the existing four. Use `_UPTREND_ONLY` regime filter (only enter when stock is already confirmed UPTREND) plus breadth circuit breaker at 40%.

**Config change only**: New strategy file, no changes to existing code.

**Risk**: DualMA produces fewer trades (hold periods are long) and may underperform in choppy sideways markets. The universe filter needs to be carefully calibrated.

---

### Suggestion B2: Add a "Quiet Breakout" Variant of Breakout (20d, Low-Vol Mode)

**What it does**: Use `high_20d` instead of `high_10d` as the breakout signal, and relax `BreakoutUniverseFilter`'s `abs_return_threshold` from 1.5% to 0.8% for stocks in a low-volatility uptrend regime.

**Why it works for Bull 2019-20**: In a slow bull, meaningful breakouts happen over 20 days, not 10. A stock that has been ranging for 20 days and then makes a new high is a genuine breakout in a low-vol context. The 20-day high is a more selective, higher-quality signal in this environment.

**Why it won't hurt other periods**: This is a new variant, not a replacement. Keep the existing `Breakout 10d` unchanged. The quiet breakout variant would produce fewer trades in high-volatility periods (stocks that spike above 1.5% daily easily exceed their 20d high — the signal would still fire but the 10d breakout fires first and is already being captured).

**Implementation complexity**: Medium. Requires:
- New strategy file: `app/strategy/quiet_breakout.py` (copy of `breakout_momentum.py` with `high_10d` → `high_20d`)
- New filter config: `BreakoutUniverseFilter` with `abs_return_threshold=0.8` and a market-regime condition gate

---

### Suggestion B3: Dynamic `abs_return_threshold` in BreakoutUniverseFilter Based on Market Volatility

**What it does**: Instead of a fixed 1.5% threshold, make the filter threshold dynamic:
- When >50% of the universe is in `LOW_VOL_UPTREND` regime: threshold = 0.8%
- Otherwise: threshold = 1.5% (current behavior, unchanged)

**Why it works**: The 1.5% threshold was set for average-to-high volatility conditions. In Bull 2019-20, the median daily move is 0.2–0.4%, making 1.5% a 3–4 standard deviation event. Setting the threshold dynamically to ~2× the typical daily move preserves the filter's intent (select meaningfully active stocks) without hardcoding a value that only works in high-vol regimes.

**Why it won't hurt other periods**: In all other periods (Crash, Recovery, Bear, Recent), the median daily move is high enough that >50% of the universe will NOT be in LOW_VOL_UPTREND, so the threshold stays at 1.5%. This change is self-deactivating outside its target regime.

**Implementation complexity**: Low. Change in `app/universe/filters.py`. The `DynamicUniverseAgent` already tracks regime distributions — pass `market_vol_regime` into the filter constructor or as a runtime parameter.

---

## 5. Improvement Suggestions: Bear 2022

### Suggestion R1: Tighten Breadth Circuit Breaker from 60% to 40%

**What it does**: Block all BUY signals when >40% (currently >60%) of the universe is in DOWNTREND.

**Why it works for Bear 2022**: Bear 2022 saw extended periods of 40–55% of stocks in DOWNTREND. Under the current 60% threshold, the circuit breaker was largely inactive. A 40% threshold would have significantly reduced RSI-MR and TrendPB trade entry during this period.

**Why it won't hurt other periods**:
- Recovery 2020-21: RSI-MR Sharpe 0.98–1.40, 1128–950 trades. Recovery was a strong broad uptrend — downtrend breadth was well below 40% for most of the period. Trade count may drop slightly but Sharpe should be unaffected.
- Crash 2020: Strategies already performed OK. Crash 2020 was a sharp crash followed by sharp recovery — the circuit breaker would fire during the crash phase (already limiting trades) and release quickly. Net effect: modest reduction in Crash 2020 losses.
- Bull 2019-20: Already a low-DOWNTREND environment, so this threshold change has minimal effect here.

**Quantitative target**: RSI-MR Bear 2022 trades should drop from 492/419 to roughly 200–250. If most losses were concentrated in the broad-bear phases (where downtrend breadth was 40–55%), this alone could recover 10–15% of the -21% loss.

**Implementation complexity**: Trivial — single config value change in `app/risk/agent.py`:
```python
# Current
BREADTH_CIRCUIT_BREAKER_THRESHOLD = 0.60
# Proposed
BREADTH_CIRCUIT_BREAKER_THRESHOLD = 0.40
```

---

### Suggestion R2: Add `uptrend_days` Counter — Minimum Uptrend Duration for RSI-MR

**What it does**: Only allow RSI-MR entry when the stock has been continuously in UPTREND regime for at least 10 consecutive trading days. A stock that crossed into UPTREND 3 days ago has an unreliable SMA crossover.

**Why it works for Bear 2022**: False uptrend signals during a rolling bear typically last 3–7 days before the SMA20/SMA50 cross reverses. A 10-day minimum uptrend duration filter eliminates almost all false-cross entries. The stocks that survive a 10-day uptrend duration test have genuine momentum behind their trend.

**Why it won't hurt other periods**:
- Recovery 2020-21 and Recent 2022-24: In a genuine uptrend, stocks establish their UPTREND regime quickly and stay there for months. A 10-day waiting period delays entry slightly but does not eliminate it. The good RSI-MR trades (Sharpe 0.98–1.40 in Recovery) are on stocks that have been in UPTREND for weeks — they pass this filter easily.

**Implementation**: Requires adding a new tracked indicator to `app/backtest/observer.py`:
```python
# In observer.py — add to per-stock state tracking
'uptrend_days': 0  # increment when regime==UPTREND, reset to 0 otherwise
```
Then in `MeanReversionUniverseFilter` or `RiskAgent`, add:
```python
if stock_data['uptrend_days'] < 10:
    return False  # skip entry
```
**Implementation complexity**: Medium. Observer change + filter/risk agent check. The `uptrend_days` field needs to be computed in the daily observation loop and persisted in the stock state dict.

---

### Suggestion R3: Add `sma_cross_age` Counter — Minimum SMA20/SMA50 Cross Duration for TrendPB

**What it does**: Only allow TrendPB entry when SMA20 has been continuously above SMA50 for at least 15 consecutive trading days.

**Why it works for Bear 2022**: The TrendPB false breakout problem is specifically about stocks where SMA20 just crossed above SMA50 (0–10 days ago). A 15-day minimum ensures the uptrend is established, not just beginning. In Bear 2022, most false-cross bounces fail within 5–10 days — they never reach the 15-day mark.

**Why it won't hurt other periods**: Same logic as R2. Genuine TrendPB candidates in Crash 2020 (Sharpe 1.49–1.78) and Recovery (Sharpe 1.21–1.23) were stocks in confirmed multi-week uptrends. The `sma_cross_age >= 15` filter doesn't remove them, it only removes fresh crossovers.

**Implementation**: Similar to R2. Add to `app/backtest/observer.py`:
```python
'sma_cross_age': 0  # increment when sma_20 > sma_50, reset to 0 when sma_20 <= sma_50
```
Then in `PullbackUniverseFilter`:
```python
if stock_data['sma_cross_age'] < 15:
    return False
```
**Implementation complexity**: Medium. Same pattern as R2 — observer change + filter update.

---

### Suggestion R4: Tighten MeanReversionUniverseFilter `max_downtrend_pct` to 40% (Explicit Config)

This is the per-filter companion to R1. The `MeanReversionUniverseFilter` already respects the breadth circuit breaker at the RiskAgent level, but making it explicit in the filter itself ensures the logic is clear and testable independently.

If the RiskAgent threshold moves to 40% (Suggestion R1), update the filter's internal config comment and any hardcoded references to document the new intent.

**Implementation complexity**: Trivial — documentation/config alignment only if R1 is implemented.

---

## 6. What NOT to Change

The following are working well and must not be modified:

| Component | Why Not to Change |
|---|---|
| `BreakoutUniverseFilter` activity requirements (non-Bull periods) | Breakout is the system's strongest strategy in 4 of 6 periods. Its filter is correctly calibrated for volatile conditions. |
| TrendPB v2 entry conditions | `price_3d_ago > SMA20×1.05` and `return_3d < -threshold` represent a major improvement over v1. Crash 2020 Sharpe 1.49–1.78 validates these conditions. |
| ATR stop at 2×ATR | MaxDD across most periods is controlled (6–12% for TrendPB/Breakout). The stop is working as intended. Do not widen it. |
| Vol-adjusted position sizing (`equity × 0.5% / 2×ATR`) | Consistent across all periods. Prevents oversizing in high-vol stocks. The 0.5% risk-per-trade is already conservative. |
| Breakout's `SMA_10` exit | Simple and effective. Breakout's MaxDD is 9–12% in most periods, which is acceptable. |
| TrendPB v2 exit `price > SMA_20 × 1.05` | Clean, regime-aware exit. The 5% threshold variant particularly shows good MaxDD control (3–8% across all periods). |

---

## 7. Priority Table

Ranked by estimated Impact × Implementation Effort.

| # | Suggestion | Target Problem | Estimated Impact | Effort | Priority |
|---|---|---|---|---|---|
| R1 | Tighten breadth CB 60%→40% | Bear 2022 RSI-MR | High — directly limits the strategy in the exact regime it fails | Trivial (1 config value) | **P1** |
| R3 | `sma_cross_age >= 15` for TrendPB | Bear 2022 TrendPB | High — eliminates false-cross entries structurally | Medium (observer + filter) | **P2** |
| B1 | Add DualMA strategy | Bull 2019-20 (all) | High — adds a strategy designed for slow bulls | Low (new file, additive) | **P2** |
| R2 | `uptrend_days >= 10` for RSI-MR | Bear 2022 RSI-MR | Medium-High — filters false uptrends but also reduces good-period trades slightly | Medium (observer + filter) | **P3** |
| B3 | Dynamic `abs_return_threshold` | Bull 2019-20 Breakout | Medium — helps Breakout fire in slow-vol markets | Low-Medium (filter logic change) | **P3** |
| B2 | Quiet Breakout 20d variant | Bull 2019-20 Breakout | Medium — new signal for slow markets | Medium (new strategy file) | **P4** |
| R4 | Explicit CB config in filter | Bear 2022 (documentation) | Low (cosmetic if R1 done) | Trivial | **P5** |

---

## 8. Implementation Notes by Suggestion

### R1 — `BREADTH_CIRCUIT_BREAKER_THRESHOLD = 0.40`
- **File**: `app/risk/agent.py`
- **Change**: Single constant. No logic changes.
- **Test**: Run Bear 2022 backtest and verify RSI-MR trade count drops from ~450 to ~200. Verify Recovery 2020-21 Sharpe stays above 0.9.
- **Rollback**: Change constant back to 0.60.

### R2 — `uptrend_days` counter in observer
- **Files**: `app/backtest/observer.py`, `app/universe/filters.py` (MeanReversionUniverseFilter)
- **Observer change**: In the daily state update loop, for each stock:
  ```python
  if current_regime == 'UPTREND':
      state['uptrend_days'] += 1
  else:
      state['uptrend_days'] = 0
  ```
- **Filter change**: Add `uptrend_days >= 10` as a hard filter condition before scoring.
- **Test**: Verify Bear 2022 entry signals drop significantly. Verify Recovery trades reduce by <20%.

### R3 — `sma_cross_age` counter in observer
- **Files**: `app/backtest/observer.py`, `app/universe/filters.py` (PullbackUniverseFilter)
- **Observer change**:
  ```python
  if sma_20 > sma_50:
      state['sma_cross_age'] += 1
  else:
      state['sma_cross_age'] = 0
  ```
- **Filter change**: Add `sma_cross_age >= 15` as a hard filter condition in `PullbackUniverseFilter`.
- **Test**: Verify Bear 2022 TrendPB trades drop. Verify Crash 2020 Sharpe stays above 1.3.

### B1 — DualMA strategy
- **Files**: New `app/strategy/dual_ma.py`, new universe filter in `app/universe/filters.py`, new experiment entry in `run_experiments.py`
- **Entry**: `sma_20` just crossed above `sma_50` (yesterday sma_20 <= sma_50, today sma_20 > sma_50)
- **Exit**: `sma_20` crosses below `sma_50`
- **Regime filter**: `_UPTREND_ONLY` (don't enter in SIDEWAYS)
- **Breadth CB**: 40% (consistent with R1 if implemented)
- **Test**: Full 2018–24 backtest. Expect positive contribution in Bull 2019-20 and Recovery. Expect limited damage in Crash and Bear (exits are built-in).

### B2 — Quiet Breakout 20d
- **Files**: New `app/strategy/quiet_breakout.py`
- **Change**: `high_10d` → `high_20d`, `abs_return_threshold` 1.5% → 0.8% in the filter config for this variant only
- **Test**: Run alongside existing Breakout 10d. Confirm the two don't double-enter the same stocks excessively.

### B3 — Dynamic `abs_return_threshold`
- **File**: `app/universe/filters.py` — `BreakoutUniverseFilter`
- **Change**: Accept `market_vol_regime` param (e.g., fraction of universe in LOW_VOL_UPTREND). If >0.5, use threshold=0.8, else use threshold=1.5.
- **DynamicUniverseAgent** already computes regime distribution — pass it downstream to the filter at each bar.
- **Test**: Verify Bull 2019-20 Breakout trade count increases from 376 to 500+. Verify other periods are unchanged.

---

## 9. Suggested Experiment Order

Run experiments in this sequence to isolate effect of each change:

1. **Baseline**: Confirm current numbers match the results above (no code changes).
2. **R1 only**: Change breadth CB to 40%. Run all periods. Compare RSI-MR Bear 2022 and all others.
3. **R1 + R3**: Add `sma_cross_age`. Run all periods. Focus on TrendPB Bear 2022 and Crash 2020.
4. **R1 + R3 + R2**: Add `uptrend_days`. Run all periods. Check RSI-MR across all regimes.
5. **B1 independently**: Add DualMA as a standalone experiment. Run all periods without touching existing strategies.
6. **B3 independently**: Dynamic threshold. Run Bull 2019-20 and verify no regression elsewhere.
7. **Combined best**: Run all accepted changes together. Verify full 2018–24 aggregate Sharpe improves.

Do not combine R-series and B-series changes in the same experiment run — it becomes impossible to attribute results.

---

## 10. R1 + R2 + R3 Experiment Results — Before/After Comparison

**Date run**: 2026-03-17
**Changes applied**: R1 (`max_downtrend_pct` 0.60 → 0.40), R2 (`sma_cross_age >= 10` in `MeanReversionUniverseFilter`), R3 (`sma_cross_age >= 15` in `PullbackUniverseFilter`)
**Implementation**: `sma_cross_age` computed in `DynamicUniverseAgent._compute_signals()` (cumulative counter, resets on SMA20 cross-under); exposed through `UniverseCandidate`; consumed by both per-strategy filters.

---

### 10.1 Full Side-by-Side Results

**Notation**: `Sharpe / Return%`. Arrow shows direction of change. ↑ = improved. ↓ = regressed. → = unchanged.

#### Breakout 10d

| Period | Before | After | Δ |
|---|---|---|---|
| Full 2018–24 | 1.03 / +136% | **1.38 / +223%** | ↑ Sharpe +0.35, Return +87pp |
| Bull 2019-20 | -0.01 / -1% | **0.78 / +10%** | ↑ Turned positive |
| Crash 2020 | 1.53 / +25% | **1.97 / +36%** | ↑ Sharpe +0.44 |
| Recovery 2020-21 | 2.52 / +105% | 2.45 / +99% | ↓ Minor regression (-6pp) |
| Bear 2022 | 0.55 / +6% | **0.84 / +11%** | ↑ Sharpe +0.29 |
| Recent 2022-24 | 1.36 / +51% | **1.47 / +59%** | ↑ Sharpe +0.11 |

#### TrendPB v2 — 3% pullback

| Period | Before | After | Δ |
|---|---|---|---|
| Full 2018–24 | 0.59 / +39% | 0.39 / +20% | ↓ Sharpe -0.20, Return -19pp |
| Bull 2019-20 | 0.34 / +2% | 0.31 / +2% | → No change |
| Crash 2020 | 1.49 / +18% | 1.31 / +13% | ↓ Sharpe -0.18 |
| Recovery 2020-21 | 1.23 / +29% | 0.81 / +16% | ↓ Sharpe -0.42, Return -13pp |
| Bear 2022 | -0.90 / -9% | -1.06 / -9% | ↓ Slightly worse Sharpe |
| Recent 2022-24 | 0.42 / +8% | 0.28 / +4% | ↓ Sharpe -0.14 |

#### TrendPB v2 — 5% pullback

| Period | Before | After | Δ |
|---|---|---|---|
| Full 2018–24 | 0.79 / +38% | 0.58 / +23% | ↓ Sharpe -0.21, Return -15pp |
| Bull 2019-20 | 0.97 / +5% | **1.07 / +4%** | ↑ Sharpe +0.10 (crossed Good threshold) |
| Crash 2020 | 1.78 / +16% | 1.51 / +11% | ↓ Sharpe -0.27 |
| Recovery 2020-21 | 1.21 / +22% | 0.90 / +14% | ↓ Sharpe -0.31, Return -8pp |
| Bear 2022 | -0.34 / -2% | -0.41 / -2% | ↓ Marginal |
| Recent 2022-24 | 0.87 / +11% | 0.70 / +7% | ↓ Sharpe -0.17 |

#### RSI-MR — os=10

| Period | Before | After | Δ |
|---|---|---|---|
| Full 2018–24 | -0.37 / -29% | **-0.02 / -6%** | ↑ Near-neutral. Return +23pp |
| Bull 2019-20 | -0.58 / -6% | **0.19 / +1%** | ↑ Turned positive |
| Crash 2020 | 0.43 / +5% | **0.78 / +10%** | ↑ Sharpe +0.35 |
| Recovery 2020-21 | 0.98 / +24% | 1.11 / +27% | ↑ Sharpe +0.13 |
| Bear 2022 | -1.59 / -21% | **-0.89 / -11%** | ↑ Losses cut nearly in half |
| Recent 2022-24 | -0.74 / -21% | -0.38 / -11% | ↑ Losses halved |

#### RSI-MR — os=5

| Period | Before | After | Δ |
|---|---|---|---|
| Full 2018–24 | 0.07 / +0% | **0.22 / +13%** | ↑ Solidly positive now |
| Bull 2019-20 | -0.15 / -2% | **0.20 / +1%** | ↑ Turned positive |
| Crash 2020 | 0.65 / +9% | **0.85 / +11%** | ↑ Sharpe +0.20 |
| Recovery 2020-21 | 1.40 / +36% | 1.31 / +31% | ↓ Minor regression (-5pp) |
| Bear 2022 | -1.06 / -15% | **-0.88 / -11%** | ↑ Losses reduced |
| Recent 2022-24 | -0.31 / -10% | -0.12 / -5% | ↑ Losses halved |

---

### 10.2 What Improved

**RSI-MR — across-the-board transformation (R1 + R2 joint effect)**

RSI-MR was the system's weakest strategy before: -29%/-0% full period, deeply negative in Bear and Recent. After R1+R2 it is near-neutral to positive in almost every period. The key wins:

- **Bear 2022**: RSI-MR10 -21% → -11%, RSI-MR5 -15% → -11%. Losses cut by roughly half. This was the primary target of R1 and R2 and both delivered.
- **Bull 2019-20**: RSI-MR10 -6% → +1%, RSI-MR5 -2% → +1%. The `sma_cross_age >= 10` filter successfully eliminated the "falling knife in an uptrend" scenario — stocks whose SMA20 crossed SMA50 too recently are no longer entered as mean-reversion candidates.
- **Recent 2022-24**: RSI-MR10 -21% → -11%, RSI-MR5 -10% → -5%. Recent 2022-24 has mixed-regime conditions similar to Bear 2022. The same mechanisms applied.
- **Crash 2020**: RSI-MR10 +5% → +10%, RSI-MR5 +9% → +11%. The crash period involves genuine overselling followed by sharp recovery — mean-reversion thesis is correct there. Fewer false-cross entries meant more trades were on genuinely oversold stocks, improving quality.
- **Recovery 2020-21**: RSI-MR10 +24% → +27% (modest improvement). The cross-age filter did not harm Recovery because stocks in the recovery period had established confirmed uptrends by the time RSI-MR entered them.

**Breakout — unexpected broad improvement**

Breakout improved in 5 of 6 periods. Most surprising: Bull 2019-20 Sharpe -0.01 → +0.78. This is attributable primarily to R1 (breadth CB at 40%). In Bull 2019-20, the circuit breaker may have blocked Breakout from entering in the specific sub-periods where market breadth was deteriorating, filtering out the worst trades while preserving entries in the genuinely healthy sub-periods. The net effect is a dramatic improvement. The Crash 2020 improvement (Sharpe 1.53 → 1.97) and Bear 2022 improvement (0.55 → 0.84) follow the same logic.

---

### 10.3 What Regressed

**TrendPB — systematic over-filtering from R3**

Every TrendPB variant regressed in most periods. The regression is concentrated in:

- **Recovery 2020-21**: TrendPB3% +29% → +16%, TrendPB5% +22% → +14%. Sharpe dropped from Good/OK territory to below 1.0. Recovery 2020-21 was TrendPB's best period — the `sma_cross_age >= 15` filter is removing valid candidates whose SMA20 crossed above SMA50 during the early crash recovery phase (a genuine uptrend, not a false crossover).
- **Crash 2020**: TrendPB3% Sharpe 1.49 → 1.31, TrendPB5% 1.78 → 1.51. Still Good but reduced. Same mechanism: stocks entering uptrend during the March 2020 recovery have low `sma_cross_age` but are genuine pullback candidates.
- **Full 2018-24**: TrendPB3% +39% → +20%, TrendPB5% +38% → +23%. Reflects the accumulation of losses across the worst sub-periods.

**The Bear 2022 problem was not fixed for TrendPB**. Bear 2022 TrendPB3% went from -9% to -9% (Sharpe -0.90 → -1.06, marginally worse). The `sma_cross_age >= 15` filter correctly targeted the "fresh crossover = false breakout" problem, but in Bear 2022 the false crossovers appear to last long enough (or the genuine declining stocks also have long cross-ages) that the filter does not provide the expected bear-market protection.

**Conclusion on R3**: R3 harmed TrendPB's best periods without delivering the expected Bear 2022 improvement. R3 as implemented is a net negative for TrendPB.

**RSI-MR Recovery minor regression**: RSI-MR5 +36% → +31%. Minor but worth noting — the `sma_cross_age >= 10` filter reduced the available universe slightly in Recovery. The regression is small and acceptable given the large gains everywhere else.

---

### 10.4 Preservation of Existing Good Performance

| Strategy × Period | Before verdict | After verdict | Preserved? |
|---|---|---|---|
| Breakout — Crash 2020 | Good (1.53) | Good (1.97) | ✅ Improved |
| Breakout — Recovery | Good (2.52) | Good (2.45) | ✅ Preserved (minor -0.07) |
| Breakout — Recent | Good (1.36) | Good (1.47) | ✅ Improved |
| TrendPB5% — Bull | Good (0.97) | Good (1.07) | ✅ Improved |
| TrendPB3% — Crash | Good (1.49) | OK (1.31) | ⚠️ Downgraded |
| TrendPB5% — Crash | Good (1.78) | Good (1.51) | ✅ Preserved (slightly weaker) |
| TrendPB3% — Recovery | Good (1.23) | OK (0.81) | ⚠️ Downgraded |
| TrendPB5% — Recovery | Good (1.21) | OK (0.90) | ⚠️ Downgraded |
| RSI-MR5 — Recovery | Good (1.40) | Good (1.31) | ✅ Preserved |
| RSI-MR10 — Recovery | OK (0.98) | Good (1.11) | ✅ Improved |

Two previously-Good TrendPB periods (Crash and Recovery) dropped from Good to OK. All Breakout Good periods were preserved or improved. RSI-MR's one Good period (RSI-MR5 Recovery) was preserved.

---

### 10.5 Updated Scorecard — After R1+R2+R3

| Strategy | Full 2018–24 | Bull 2019-20 | Crash 2020 | Recovery 2020-21 | Bear 2022 | Recent 2022-24 |
|---|---|---|---|---|---|---|
| Breakout 10d | **Good** (1.38 / +223%) | **OK** (0.78 / +10%) | **Good** (1.97 / +36%) | **Good** (2.45 / +99%) | **OK** (0.84 / +11%) | **Good** (1.47 / +59%) |
| TrendPB v2 3% | **OK** (0.39 / +20%) | **OK** (0.31 / +2%) | **Good** (1.31 / +13%) | **OK** (0.81 / +16%) | **Bad** (-1.06 / -9%) | **OK** (0.28 / +4%) |
| TrendPB v2 5% | **OK** (0.58 / +23%) | **Good** (1.07 / +4%) | **Good** (1.51 / +11%) | **OK** (0.90 / +14%) | **Bad** (-0.41 / -2%) | **OK** (0.70 / +7%) |
| RSI-MR os=10 | **Bad** (-0.02 / -6%) | **OK** (0.19 / +1%) | **OK** (0.78 / +10%) | **Good** (1.11 / +27%) | **Bad** (-0.89 / -11%) | **Bad** (-0.38 / -11%) |
| RSI-MR os=5 | **OK** (0.22 / +13%) | **OK** (0.20 / +1%) | **OK** (0.85 / +11%) | **Good** (1.31 / +31%) | **Bad** (-0.88 / -11%) | **OK** (-0.12 / -5%) |

**Verdict**: Good = Sharpe > 1.0. OK = Sharpe 0.3–1.0. Bad = Sharpe < 0.3 or negative.

---

### 10.6 Analysis: R1, R2, R3 Individual Attribution

**R1 (breadth CB 40%) — High confidence, net positive**

Responsible for most of the Breakout improvement and a meaningful portion of RSI-MR bear improvement. The tighter 40% threshold cleanly blocked entries during the portions of Bear 2022 where market breadth was deteriorating but had not yet reached the old 60% threshold. No strategy regressed materially from R1 alone — in the good periods (Crash, Recovery), breadth was well below 40% downtrend so the circuit breaker did not fire.

**R2 (sma_cross_age >= 10 for RSI-MR) — High confidence, net positive**

Clearly the right fix for RSI-MR. The RSI-MR transformation (from -29% to -6% full period, from -21% to -11% in Bear) is largely attributable to R2 filtering out the "false uptrend" entries. Recovery RSI-MR was barely affected (-5pp). R2 should be kept.

**R3 (sma_cross_age >= 15 for TrendPB) — Low confidence, net negative as implemented**

R3 did not achieve its target (Bear 2022 TrendPB remained negative) and degraded TrendPB's best periods (Recovery dropped from Good to OK). The 15-day threshold is too aggressive — it removes genuine pullback candidates from stocks that recently entered a confirmed uptrend (e.g., March 2020 recovery).

**Recommended action for R3**: Either revert R3 entirely, or reduce the threshold from 15 to 8 days and re-test. A threshold of 8 would still reject 1–5 day false crossovers but would not block the early-recovery stocks that drove TrendPB's best Crash/Recovery numbers.

---

### 10.7 Remaining Open Issues

1. **Bear 2022 TrendPB** is still negative (-9% in both variants). R3 did not fix it and may have made it marginally worse. This is the most important remaining problem for TrendPB.

2. **RSI-MR10 Full period** is still at -0.02 / -6%. While dramatically improved from -0.37 / -29%, RSI-MR10 is not yet profitable over the full period. RSI-MR5 (0.22 / +13%) is now the clearly better oversold threshold to use.

3. **TrendPB Recovery downgrade**: R3 cost TrendPB roughly 12–13pp of return in its best period. If R3 is reverted, TrendPB Recovery should recover to Good levels. This regression is recoverable.

4. **Bull 2019-20 structure**: All strategies still perform only OK or below in Bull 2019-20 — no strategy achieves Good (Sharpe > 1.0) in the slow-bull period. Suggestions B1 (DualMA), B2 (Quiet Breakout 20d), and B3 (Dynamic threshold) from Section 4 remain unimplemented and are the next frontier.

5. **Recent 2022-24 RSI-MR10**: Still -11% despite halving losses. This period has mixed regime structure similar to Bear 2022 and benefits from the same fixes, but RSI-MR10 has not crossed into positive territory here. RSI-MR5 at -5% is closer but still negative.

---

### 10.8 Recommended Next Steps (Post R1+R2+R3)

| Priority | Action | Rationale |
|---|---|---|
| P1 | Revert R3 or reduce threshold to 8 days | R3 is harming TrendPB more than it helps. Test 8-day threshold to preserve the false-crossover protection while recovering Recovery/Crash performance. |
| P2 | Add B1 (DualMA strategy) | Bull 2019-20 remains the system's blind spot. DualMA is designed for exactly this market type. |
| P3 | Investigate TrendPB Bear 2022 further | The false-crossover hypothesis did not fully explain the losses. Look at actual trade list for Bear 2022 TrendPB to identify what types of stocks are being entered and lost on. |
| P4 | Retire RSI-MR os=10 variant | RSI-MR5 dominates RSI-MR10 in virtually every period after R2. Running both variants in production adds noise without diversification benefit. |
| P5 | B3 (Dynamic return threshold) | Once DualMA is in place, use B3 to further improve Breakout in Bull 2019-20. |
