# Strategy Guide — Financial Lab

**Strategies:** 5 active  
**Features library:** `app/features/indicators.py`  
**Strategy code:** `app/strategy/`  
**Regime classification:** `app/backtest/observer.py`

---

## How the system works (big picture)

Every trading day, each strategy scans the universe of ~80 active stocks and proposes BUY / SELL / HOLD decisions. The **MultiStrategyRouter** collects all proposals, resolves conflicts (SELL beats BUY beats HOLD; higher-weight strategy wins ties), and passes the merged list to the **RiskAgent**, which applies position sizing, ATR stop checks, and the breadth circuit breaker before anything gets executed.

Each stock is also assigned a **regime** (e.g. `LOW_VOL_UPTREND`, `HIGH_VOL_SIDEWAYS`) which gates which strategies are allowed to trade it. Each strategy has an allowlist — it only sees stocks in compatible regimes.

---

## The 5 strategies

### 1. DualMA — Dual Moving Average Crossover

**Plain English:** Buy when the short-term trend catches up to and crosses above the long-term trend ("golden cross"). Sell when it falls back below ("death cross"). This is a classic trend-following signal.

**Entry:** SMA_20 crosses above SMA_50 (yesterday it was below, today it is above)  
**Exit:** SMA_20 crosses below SMA_50  
**Hold horizon:** Weeks to months  
**Indicators used:** SMA_20, SMA_50  
**Regime allowlist:** Uptrend regimes only (`LOW/MID/HIGH_VOL_UPTREND`)

**What makes it useful:** Very clean signal — it only fires when a stock has been rising consistently for 20 days and that short-term momentum is now stronger than the medium-term trend. Low trade frequency = low friction.

**Weakness:** The signal is lagging by design. By the time SMA_20 crosses SMA_50, the stock has already moved 10–20% off the bottom. You buy late and sell late. In choppy sideways markets it generates whipsaw trades — crosses up, then immediately crosses back down.

---

### 2. Breakout Momentum

**Plain English:** Buy when a stock closes at its highest price in the last 10 days — it's breaking out into new territory, which attracts momentum buyers. Sell when the stock falls back below its 10-day average, signalling the breakout has failed.

**Entry:** Today's close > yesterday's 10-day rolling high  
**Exit:** Close falls below SMA_10  
**Hold horizon:** 3–10 days  
**Indicators used:** high_10d (previous 10-day rolling max), SMA_10  
**Regime allowlist:** Uptrend + high-vol regimes (fast-moving stocks)

**What makes it useful:** Catches stocks just as they start to move. Short hold time = capital cycles quickly. Works well in recovery/momentum markets.

**Weakness:** A 10-day high is easy to break on a quiet day in a rangebound stock — many signals are false. No volume confirmation means a stock can "break out" on thin trading, then reverse immediately. High trade frequency → high friction.

---

### 3. QuietBreakout — Low-Volatility Breakout

**Plain English:** The same idea as Breakout Momentum but for calmer markets. Instead of a 10-day high, the bar is set to 20 days — the stock has to clear a longer range of prices, making it a more selective, more confident signal.

**Entry:** Today's close > yesterday's 20-day rolling high  
**Exit:** Close falls below SMA_20  
**Hold horizon:** 5–20 days  
**Indicators used:** high_20d (previous 20-day rolling max), SMA_20  
**Regime allowlist:** Low/mid-vol uptrend regimes (slow-bull markets)

**What makes it useful:** More selective than Breakout — fewer signals, but each signal has cleared a wider range of prices. Better suited to the low-volatility bull periods where stocks grind higher steadily.

**Weakness:** Same structural problem as Breakout — no volume filter. In slow-bull markets, a 20-day high is a meaningful signal, but in a strong bull, even weak stocks will break 20-day highs just on market-wide lifting.

---

### 4. TrendPullback — Buy the Dip in an Uptrend

**Plain English:** Find stocks that are in a strong uptrend and have just pulled back 3–5% in the last 3 days. Buy the dip and wait for the stock to recover back to its pre-pullback level. Exit if it doesn't recover within 10 days (it was probably a real breakdown, not a dip).

**Entry — all 4 conditions must be true simultaneously:**
1. SMA_20 > SMA_50 (medium-term uptrend is intact)
2. SMA_20 is rising day-over-day (trend is still accelerating)
3. The stock was >5% above SMA_20 three days ago (it was in a strong trend, not just barely above)
4. The stock has fallen >3% over the last 3 days (the pullback has happened)

**Exit (profit):** Price recovers to >5% above SMA_20 (back to pre-pullback strength)  
**Exit (time):** Still not recovered after 10 days → cut the position  
**Hold horizon:** 3–10 days  
**Indicators used:** SMA_20, SMA_50, return_3d, previous day's SMA_20  
**Regime allowlist:** Uptrend regimes

**What makes it useful:** Counter-trend within a trend. Buys temporary weakness in strong stocks — lower entry price, defined exit target. The 5% above SMA_20 filter is good at avoiding entries into stocks that are already weakening.

**Weakness:** The in-memory `_entry_dates` tracking (used for the 10-day time stop) is **reset every time the process restarts**. In production, the cron script creates a new instance each run — so the time stop never fires. Positions can be held indefinitely even if they don't recover. (See Bug #1 below.)

---

### 5. RSI Mean Reversion

**Plain English:** Buy a stock that has fallen so hard and so fast that it is statistically "oversold" by a very short-term measure (RSI over just 3 days). These extreme sell-offs often snap back quickly. Exit when the RSI recovers above 80 (overbought) or after 7 days, whichever comes first.

**Entry:** RSI_3 drops below 5 (extreme 3-day oversold — happens maybe 1–2% of trading days)  
**Exit:** RSI_3 rises above 80, OR 7 days have passed  
**Hold horizon:** 1–5 days  
**Indicators used:** RSI_3  
**Regime allowlist:** Uptrend + sideways regimes (avoids buying in confirmed downtrends)

**What makes it useful:** Very short-term. Gets in and out quickly. Profits from panic selling overreactions. In recovery/bounce periods this can capture large one-day moves.

**Weakness:** RSI_3 < 5 is extremely rare — the threshold is too tight. In the backtest period this strategy likely generated very few signals and contributed little alpha. Also shares the same `_entry_dates` restart bug as TrendPullback — the 7-day time stop doesn't fire in production.

---

## Indicators / features library

| Indicator | Window | Used by | What it measures |
|-----------|--------|---------|------------------|
| SMA_5 | 5 days | — | Very short-term average price |
| SMA_10 | 10 days | Breakout exit | Short-term average; acts as dynamic support |
| SMA_20 | 20 days | QuietBrk, TrendPB, DualMA | Medium-short trend; primary trend reference |
| SMA_50 | 50 days | DualMA, Regime, TrendPB | Medium-term trend; regime baseline |
| ATR_5 | 5 days | — | Short-term daily volatility |
| ATR_14 | 14 days | RiskAgent, Regime | Standard daily volatility; used for position sizing and stop distance |
| RSI_2 | 2 days | — | Ultra-short mean reversion oscillator (computed, not currently used) |
| RSI_3 | 3 days | RSI-MR | 3-day momentum oscillator; extreme oversold/overbought |
| return_3d | — | TrendPB | 3-day % price change |
| return_5d, return_10d | — | — | Medium-short momentum (computed, not currently used) |
| rolling_vol_5d/10d | — | — | Short-term return volatility (computed, not currently used) |
| high_10d | 10 days | Breakout | Previous 10-day rolling high (shifted 1 day to avoid look-ahead) |
| high_20d | 20 days | QuietBrk | Previous 20-day rolling high (shifted) |
| low_10d | 10 days | — | Previous 10-day rolling low (computed, not currently used) |

**Regime classification (per stock, per day):**

| Component | How computed |
|-----------|-------------|
| Trend state | `UPTREND` if close > SMA_50 and SMA_50 rising; `DOWNTREND` if close < SMA_50 and SMA_50 falling; else `SIDEWAYS` |
| Vol state | ATR_14 as percentile of trailing 252 days: bottom 33% = `LOW_VOL`, middle = `MID_VOL`, top 33% = `HIGH_VOL` |
| Regime | Combined: `LOW_VOL_UPTREND`, `MID_VOL_SIDEWAYS`, etc. — 9 possible labels |

---

## Bugs and improvements — priority order

### Bug #1 (HIGH) — In-memory `_entry_dates` lost on every cron run

**Affects:** TrendPullback, RSI-MR  
**Files:** `app/strategy/trend_pullback.py`, `app/strategy/rsi_mean_reversion.py`

Both strategies track entry dates in `self._entry_dates: dict[str, datetime]`. In production, `run_paper_signals.py` creates a fresh strategy instance on every run. `_entry_dates` is always empty → the 10-day time stop (TrendPB) and 7-day time stop (RSI-MR) **never fire in the live system**.

Impact: positions that fail to recover after 10 days are held indefinitely until the ATR stop or the strategy's signal-based exit fires. This leads to capital lock-up in losing positions.

**Fix:** Persist `_entry_dates` to SQLite using the existing `save_regime_state` / `load_regime_state` pattern, keyed by `entry_dates_{strategy}_{session_id}`. Load at the start of each run, save after decisions are generated.

```python
# In _run_session(), after building the router:
saved_entry_dates = load_regime_state(f"entry_dates_TrendPB_{sid}") or {}
router.strategies["TrendPB"]._entry_dates = {
    sym: datetime.fromisoformat(dt) for sym, dt in saved_entry_dates.items()
}
# ... after final_decisions:
save_regime_state(f"entry_dates_TrendPB_{sid}", {
    sym: dt.isoformat()
    for sym, dt in router.strategies["TrendPB"]._entry_dates.items()
})
```

---

### Bug #2 (MEDIUM) — RSI_3 threshold too extreme

**Affects:** RSI-MR  
**File:** `api/run_paper_signals.py` (construction), `run_ujjwal_baseline.py`

`rsi_oversold=5` means RSI_3 must drop below 5 — this is an extremely rare event (roughly 1-2 occurrences per stock per year). The strategy likely contributes near-zero signals in most market conditions, occupying 20% of the capital weight while doing almost nothing.

**Evidence from backtest:** Win rates across periods are around 39-51%. RSI-MR, being a mean-reversion strategy, should show different characteristics (higher win rate, smaller wins) vs the trend strategies. The fact that overall win rates don't show this suggests RSI-MR is barely trading.

**Fix:** Raise the threshold to `rsi_oversold=15` and lower `rsi_overbought=70`. This will generate more signals in genuinely oversold conditions while still filtering out moderate pullbacks.

---

### Improvement #1 (HIGH) — No volume confirmation on breakouts

**Affects:** Breakout, QuietBreakout  
**Files:** `app/strategy/breakout_momentum.py`, `app/strategy/quiet_breakout.py`

Both strategies buy when price breaks a recent high — but have no check on whether trading volume supported the move. A breakout on 50% of average volume is a weak signal; on 200% of average volume it is a genuine momentum move.

Volume data is available in `market_ohlc`. Adding a `vol_ratio` indicator (today's volume / 20-day avg volume) and requiring `vol_ratio > 1.2` on entry would filter ~30-40% of false breakout signals.

**Expected improvement:** Fewer trades (lower friction) with higher win rate. Profit factor should improve from ~1.37 toward 1.5+.

```python
# In observer.py — add to indicator computation:
volume_s     = pd.Series([r.volume for r in records], dtype=float)
volume_sma20 = volume_s.rolling(20, min_periods=10).mean().shift(1)
vol_ratio    = volume_s / volume_sma20   # > 1 = above-average volume

# In BreakoutMomentumStrategy.decide():
vol_ratio = state.indicators.get("vol_ratio")
if not in_position and price > high_10d and (vol_ratio is None or vol_ratio > 1.2):
    ...BUY
```

---

### Improvement #2 (MEDIUM) — Breakout and QuietBreakout are redundant

**Affects:** Capital allocation  
**Files:** `api/run_paper_signals.py`, `run_ujjwal_baseline.py`

Both strategies are breakout strategies differentiated only by lookback window (10 vs 20 days) and regime target (high-vol vs low-vol). They share 40% of the capital weight (0.20 each) but are fundamentally the same idea. In practice they will often fire on the same stock, with the router keeping only the higher-weight one.

A more useful 5th strategy would be one with **negative or low correlation to the other four** — something that performs well when trend strategies don't.

**Candidates:**
- **Relative strength / sector rotation**: buy the top N stocks by 20-day return within the universe. Pure momentum cross-section, uncorrelated to single-stock breakout signals.
- **MACD crossover**: similar to DualMA but uses exponential MAs, faster to react.
- **Bollinger Band squeeze**: buys when volatility contracts and then expands (a volatility-based entry, different character from price-level breakouts).

---

### Improvement #3 (MEDIUM) — DualMA is purely lagging

**Affects:** DualMA  
**File:** `app/strategy/dual_ma.py`

The SMA_20/SMA_50 crossover requires 50 bars to compute and signals only after the move is already confirmed. The entry is typically 8-15% late on a trend move. A hybrid approach would add an early-entry confirmation:

**Option A:** Add RSI_14 > 50 as a pre-filter — only trade crossovers where the stock also shows positive medium-term momentum (RSI above neutral). This filters crossovers in stocks that are recovering from deeply oversold (late signal) vs stocks resuming a healthy trend.

**Option B:** Replace with EMA crossover (SMA_9 / EMA_21). EMAs react faster to recent price, giving 2-3 days earlier signal than SMA. The existing `simple_moving_average()` function would need an `exponential_moving_average()` companion.

---

### Improvement #4 (LOW) — Computed features going unused

**Affects:** Overall signal quality  
**File:** `app/backtest/observer.py`

The observer computes `rsi_2`, `return_5d`, `return_10d`, `rolling_vol_5d`, `rolling_vol_10d`, and `low_10d` — none of which are currently used by any strategy. These are computed every run for every symbol, adding processing time without benefiting any signal.

Either:
1. **Remove them** to reduce compute time, or
2. **Use them** — `return_5d`/`return_10d` could strengthen TrendPullback entries (requiring 5-day momentum > 0 as an uptrend confirmation), and `rolling_vol_5d` could be a regime-conditional entry filter for Breakout (only breakout when short-term vol is expanding).

---

### Improvement #5 (LOW) — TrendPullback profit target is fixed

**Affects:** TrendPullback exit quality  
**File:** `app/strategy/trend_pullback.py`

The exit target `price > sma_20 * 1.05` is a fixed 5% above SMA_20. In LOW_VOL markets the stock may never reach +5% above SMA_20 (slow-moving stocks don't run that far) and the time stop fires instead. In HIGH_VOL markets a stock can run to +10% above SMA_20 and the strategy exits too early.

A regime-conditional target would let the profit run further in high-vol environments:
```python
target_mult = {"LOW_VOL": 1.03, "MID_VOL": 1.05, "HIGH_VOL": 1.08}.get(vol_state, 1.05)
if price > sma_20 * target_mult:
    ...SELL
```

---

## Summary table

| # | Category | Strategy | Effort | Expected impact |
|---|----------|----------|--------|----------------|
| 1 | Bug | Persist `_entry_dates` across runs | Medium | Fixes broken time stops for TrendPB + RSI-MR in production |
| 2 | Bug | Raise RSI oversold threshold (5→15) | Trivial | RSI-MR actually trades; contributes alpha |
| 3 | Improvement | Volume confirmation on breakouts | Medium | Fewer false signals; higher profit factor |
| 4 | Improvement | Replace QuietBreakout with uncorrelated strategy | Large | Better diversification; smoother equity curve |
| 5 | Improvement | DualMA early entry (RSI_14 filter or EMA) | Small | Earlier entries; less lag on crossover signals |
| 6 | Cleanup | Remove unused computed features, or use them | Small | Faster compute; or improved signal quality |
| 7 | Improvement | Regime-conditional TrendPB profit target | Small | Better exit timing in low/high-vol regimes |
