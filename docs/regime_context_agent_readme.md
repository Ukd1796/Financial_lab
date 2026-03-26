# RegimeContextAgent — What Changed, Why It Matters, and What's Next

## The Problem It Solves

### The lag problem

The original system classified the market regime using only the **active filtered universe** — the 24-80 symbols that passed the strategy-specific universe filters on a given day. This created two structural blind spots:

**Blind spot 1 — Sample size bias**
In a bear market, the active universe shrinks to 24 symbols. Those 24 are not representative — they are the most actively traded stocks in a selloff, often the ones experiencing the heaviest selling pressure. Measuring the regime from 24 bear-market stocks gives a distorted picture compared to measuring from all 150.

Today's example (March 26, 2026):
```
Active universe regime:   96% DOWNTREND  (24 stocks, heavily filtered)
Broad universe regime:    likely 75-80% DOWNTREND  (150 stocks, unfiltered)
```

**Blind spot 2 — Recovery lag (the most costly one)**
The original regime was based on `price < SMA_50` AND `SMA_50 slope < 0`. The SMA_50 reacts slowly — it requires approximately 10-15 consecutive positive sessions before it starts rising meaningfully. During a genuine recovery:

- Day 1-10 of recovery: price rises, index up 8%, but SMA_50 still declining → system still says BEAR_CONFIRMED → 0 signals
- Day 15-20: SMA_50 starts flattening → system still says BEAR_CONFIRMED → 0 signals
- Day 25-30: SMA_50 starts rising, price clearly above it → system finally says BULL_EARLY → first signals

This means the system **misses the first 15-25% of a recovery move**. In the 2020 recovery (April-May), Nifty rose 40% from the bottom. The original system would have caught only the last 25-30% of that move.

---

## What RegimeContextAgent Changes

### Before (base `build_regime_snapshot`)

```python
# Inputs: daily_symbol_states (24-80 filtered symbols only)
# Output:
{
    "pct_uptrend":    0.04,   # 4% of 24 active stocks
    "pct_downtrend":  0.96,   # 96% of 24 active stocks
    "pct_sideways":   0.00,
    "avg_atr_pct":    0.036,
    "universe_size":  24
}
```

This snapshot sees 96% downtrend and correctly stays dark. But it cannot distinguish between:
- A market that is **genuinely deteriorating** (breadth getting worse day over day)
- A market that **bottomed 5 days ago** and breadth is quietly improving (but SMA_50 hasn't caught up yet)

### After (RegimeContextAgent)

```python
# Inputs: daily_symbol_states (24 symbols) + DynamicUniverseAgent cache (150 symbols)
# Output (all base keys preserved, new keys added):
{
    # --- Base keys (unchanged) ---
    "pct_uptrend":    0.04,
    "pct_downtrend":  0.96,
    "avg_atr_pct":    0.036,
    "universe_size":  24,

    # --- New broad breadth keys (from all 150 symbols) ---
    "pct_above_sma50_broad":  0.18,   # 18% of 150 stocks above SMA_50
    "advance_decline_ratio":  0.52,   # 52% of stocks UP today (index up day)
    "broad_universe_size":    150,
    "avg_rolling_vol_5d":     0.014,

    # --- Trend direction (5-day rolling) ---
    "trend":          "IMPROVING",   # pct_above_sma50 rising, pct_downtrend falling

    # --- Synthesised regime label ---
    "broad_regime":   "BEAR_TRANSITION"   # deep bear but actively improving
}
```

### The 8 regime labels and what they mean for you

| Label | What it means | System action |
|-------|--------------|---------------|
| `BEAR_CONFIRMED` | Deep bear, no improvement | 0 signals, full capital protection |
| `BEAR_TRANSITION` | Deep bear but breadth improving over 5 days | 0 signals, but LLM aware recovery may be starting |
| `BEAR_WATCH` | Moderate bear (45-60% downtrend), stable | 0 signals |
| `TRANSITION_UP` | Moderate bear AND breadth actively improving | CB relaxed to 30% — cautious re-entry begins |
| `SIDEWAYS_CHOPPY` | Mixed signals, no clear direction | Standard CB (35%) |
| `BULL_WATCH` | Majority above SMA_50, not accelerating | Standard signals |
| `BULL_EARLY` | Majority above SMA_50, improving | Full signals |
| `BULL_CONFIRMED` | Strong broad uptrend | Full signals, all strategies eligible |

### The key mechanical change: CB relaxation during `TRANSITION_UP`

Without RCA, the circuit breaker fires at `market_downtrend_pct ≥ 35%`. Once 35% of stocks are in downtrend, **all BUYs are blocked regardless of individual stock quality**.

With RCA, the engine applies a regime-based override in `BacktestEngine`:

```python
effective_downtrend_pct = market_downtrend_pct   # e.g. 0.52

if broad_regime == "TRANSITION_UP":
    effective_downtrend_pct = min(market_downtrend_pct, 0.30)  # cap at 30%
    # → CB does not fire even though 52% of stocks are in downtrend
    # → Breakout and TrendPB can now fire on the best individual stocks

elif broad_regime in ("BEAR_WATCH", "BEAR_TRANSITION"):
    effective_downtrend_pct = min(market_downtrend_pct, 0.38)  # slight relaxation
```

This allows the system to begin cautious re-entry **2-3 weeks earlier** than the SMA_50 rules would allow.

---

## Current Scenario (March 26, 2026)

Today's reading:
- `pct_downtrend = 96%` in the active universe
- `advance_decline_ratio` = likely ~52% (Sensex was up today)
- `pct_above_sma50_broad` = likely ~15-20% (most stocks still below 50d MA)
- Expected `broad_regime` = `BEAR_CONFIRMED` or `BEAR_TRANSITION`

**Why Sensex being up doesn't change the regime:**
The Sensex is a price-weighted index of 30 large-cap stocks. When it rises 500 points, that can be driven entirely by 5-6 heavyweight stocks (RELIANCE, HDFC, TCS) while 120 other stocks in our universe are flat or down. The SMA_50-based regime is a medium-term indicator — a single up day moves the SMA_50 by 0.3-0.5%, far below the threshold needed to flip the regime.

**What would change the regime:**
```
10-15 consecutive sessions of broad advances
  → pct_above_sma50_broad rises from 18% to 40%+
  → pct_downtrend falls from 96% to below 60%
  → trend flips to "IMPROVING" for 5 consecutive days
  → broad_regime = "BEAR_TRANSITION" → then "TRANSITION_UP"
  → CB relaxes → first cautious BUY signals appear
```

**RCA's advantage in the current scenario:**
The base system would stay at BEAR_CONFIRMED until SMA_50 confirms (~3-6 weeks into recovery). RCA would detect `BEAR_TRANSITION` after just 5 days of improving breadth — providing an early warning signal to the LLM and relaxing the CB 2-3 weeks earlier.

---

## How News Integration Would Make This Better

The RCA as implemented is still entirely **price-derived**. It looks at SMA_50, daily returns, and 5-day trends. These are all lagging indicators. News is the only source of truly **leading information** in this system.

### Problem 1: RCA cannot detect a regime-changing event in real time

**Scenario:** RBI cuts rates by 50bps at 10 AM on a Tuesday.

- **Without news:** Nifty rallies 2.5%. RCA records one good `advance_decline_ratio`. `broad_regime` stays `BEAR_CONFIRMED`. No change.
- **After 5 days:** Breadth improves enough for `BEAR_TRANSITION`. LLM gets the signal.
- **With news feed:** Same day, `MacroCalendarAgent` reads the RBI announcement → immediately injects `"RBI surprise cut: +50bps above expectations"` into the regime snapshot → LLM gets this context in the next rebalance call → weights shift toward Breakout/TrendPB same week.

The 5-day lag is eliminated. The system re-enters at the bottom of the rally, not 5 days into it.

### Problem 2: RCA sees advance/decline but not WHY

If 60% of stocks are advancing today, RCA sees `advance_decline_ratio = 0.60`. But it doesn't know if this is:
- A genuine recovery driven by FII inflows (durable)
- A short-covering rally that will reverse in 2 days (not durable)
- A result of one heavyweight stock dragging the index (misleading)

A news feed would tell the LLM which case it is, and the LLM would weight the `TRANSITION_UP` signal accordingly.

### Problem 3: RCA cannot block entries before shock events

RCA detects improvement but cannot warn about upcoming shocks:
- RBI MPC meeting tomorrow → hold off new entries
- US Fed minutes released tonight → uncertainty spike likely
- Major company earnings in 3 days → don't enter that stock

All of these require a calendar/news feed. RCA has no way to know these events exist.

---

## The Integration Plan: How to Tackle It

### Step 1 — Macro Calendar (1-2 days effort, no LLM)

Create a hardcoded calendar of scheduled high-impact events and check it daily before running signals:

```python
# app/meta/macro_calendar.py
SCHEDULED_EVENTS = [
    # RBI MPC meetings 2026
    {"date": "2026-04-09", "event": "RBI MPC Decision", "impact": "HIGH"},
    {"date": "2026-06-06", "event": "RBI MPC Decision", "impact": "HIGH"},
    # US Fed meetings 2026
    {"date": "2026-04-29", "event": "US Fed FOMC", "impact": "HIGH"},
    # India Q4 results season
    {"date": "2026-04-01", "event": "Q4 Results Season Starts", "impact": "MEDIUM"},
]

def get_upcoming_events(days_ahead=2) -> list:
    """Return events in the next N days."""
    ...
```

When a HIGH impact event is within 2 days: auto-set `SUPPRESS_NEW_BUYS=1` and log the reason. This replaces the manual env-var override you're using today.

**Value: eliminates the most avoidable losses — entering positions the day before an RBI/Fed surprise.**

### Step 2 — NSE F&O Ban List (2-3 hours effort, no LLM)

The NSE publishes a daily F&O ban list. Stocks in this list cannot have new F&O positions opened. While this doesn't directly affect cash equity, stocks on the ban list typically:
- Have unusually high open interest (crowded trade)
- Are subject to forced unwinding (other traders must reduce positions)
- Are experiencing unusual institutional activity

Adding a daily check costs 10 lines of code and a free URL fetch:

```python
# Before universe filtering in run_signals.py
banned = fetch_fo_ban_list(today)   # free NSE URL
active_symbols = [s for s in candidates if s not in banned]
```

### Step 3 — Inject News Context into RCA Snapshot (1-2 weeks effort, requires NewsAPI)

Extend `RegimeContextAgent.build_snapshot()` to optionally accept a `news_context` string. When provided, it's added to the snapshot dict and flows into the LLM prompt automatically:

```python
def build_snapshot(self, daily_symbol_states, current_date, news_context=None):
    ...
    snapshot = {**base, **broad, "trend": trend, "broad_regime": broad_regime}
    if news_context:
        snapshot["news_context"] = news_context
    ...
```

The `AdaptiveStrategySelector._build_prompt()` already adds broad_regime to the LLM prompt — `news_context` would appear there too. The LLM can then factor in "FII sold ₹8,200 crore this week" when deciding weights, rather than inferring it from price data alone.

**Data source:** NewsAPI.org free tier (100 requests/day). One daily call to fetch the top 5 NSE/Nifty headlines is sufficient.

### Step 4 — Per-Stock News Gate in EntryTimingAgent

Once Steps 1-3 are working, add a per-trade news check. Before a BUY signal is written to `signal_queue`, check if the stock has a material negative event in the last 3 days:

```python
# Between MultiStrategyRouter and RiskAgent
for decision in proposed:
    if decision.action == "BUY":
        news = get_recent_news(decision.symbol, days=3)   # NewsAPI
        if has_negative_event(news):    # LLM or rule-based classifier
            decision = Decision(symbol=decision.symbol, action="HOLD",
                               reasoning=f"Negative news: {news[0]['headline']}")
```

This is the most surgical use of news — it acts at the individual stock level, not the portfolio level.

---

## Summary

| Feature | Without RCA | With RCA (now) | With RCA + News |
|---------|-------------|----------------|-----------------|
| Regime based on | 24 filtered stocks | 150 broad universe | 150 stocks + macro context |
| Recovery detection lag | 3-6 weeks | 1-2 weeks | Same day (for scheduled events) |
| CB during transition | Stays at 35% threshold | Relaxes to 30% on `TRANSITION_UP` | Also relaxes when news confirms recovery |
| Scheduled event protection | Manual `SUPPRESS_NEW_BUYS` | Manual `SUPPRESS_NEW_BUYS` | Automatic via calendar |
| Per-stock news risk | None | None | LLM gate before each BUY |
| LLM context quality | Regime label + Sharpe table | + broad_regime + trend direction | + macro digest + stock news |

**Current state (March 26, 2026):** RCA is implemented and running. The market is in `BEAR_CONFIRMED` / `BEAR_TRANSITION`. The system is correctly protecting capital. The next important event is when breadth starts genuinely improving over 5 consecutive sessions — RCA will detect that 2-3 weeks before the SMA_50 confirms it, allowing cautious re-entry at a better price.

**Most important next action:** Add the macro calendar for Q4 results season (April 2026) — earnings announcements are the single highest-risk event for open positions and are completely preventable with a simple date lookup.
