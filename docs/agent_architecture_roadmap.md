# Agent Architecture Roadmap

## Current System Map

```
DB (Supabase)
    │
    ▼
DynamicUniverseAgent          ← bulk scans 150 symbols, scores by vol/momentum
    │  top 80 candidates
    ▼
UnionUniverseFilter            ← 5 rule-based filters (Breakout, Pullback, MR, DualMA, QuietBrk)
    │  60-80 active symbols
    ▼
MarketObserverAgent            ← computes MarketState (20+ indicators) per symbol
    │  symbol → MarketState dict
    ▼
MultiStrategyRouter            ← 5 strategies, per-strategy regime gate
    │  proposed decisions
    ▼
AdaptiveStrategySelector       ← LLM (GPT-4o-mini), reweights strategies weekly  ← only LLM today
    │  weights vector
    ▼
RiskAgent                      ← ATR sizing, breadth CB, regime filter
    │  final decisions
    ▼
signal_queue / PaperAdapter
```

---

## Where New Agents Could Add Value

There are four distinct integration points. Each is described below with value estimate and implementation complexity.

---

### Agent 1 — StockInsightAgent  *(Universe filter stage)*

**Where it plugs in:** After `UnionUniverseFilter` produces 60-80 candidates, before `MarketObserverAgent` runs in full.

**What it does:**
The current filter is entirely rule-based (thresholds on RSI, SMA cross age, relative volume). A `StockInsightAgent` would take the top N candidates with their indicator snapshots and ask the LLM to produce a ranked shortlist with a brief rationale per stock.

Inputs to LLM per candidate:
- relative_volume, daily_return, rolling_vol_5d, atr_ratio
- sma_20_above_sma_50, sma_cross_age, return_3d
- Current regime label (BEAR_CONFIRMED, MID_VOL_UPTREND, etc.)

LLM output per stock:
```json
{ "symbol": "TITAN", "rank": 1, "action": "include",
  "reason": "Fresh SMA cross (age=3), 2.1× volume, positive 3d momentum in MID_VOL_UPTREND" }
{ "symbol": "SBIN", "rank": 18, "action": "exclude",
  "reason": "Cross age=2, but return_3d negative and sector under pressure" }
```

**Value:**
- Adds a soft qualitative layer over hard quantitative thresholds
- Can incorporate context the rules can't express (e.g., "this stock has been a false-cross machine for 3 months")
- Makes universe selection explainable — each filtered-out stock has a reason logged

**Risk / Cost:**
- Adds ~20-30 LLM calls per day (one per candidate batch)
- Needs a compact prompt — indicators only, no narrative news (we don't have that data yet)
- May not outperform rules in a pure bull market where signal quality is already high

**Priority:** Medium. Most useful when the system is in TRANSITION regimes where rule-based filters have high false-positive rates.

---

### Agent 2 — RegimeContextAgent  *(Regime snapshot stage)*

**Where it plugs in:** Replaces or augments `build_regime_snapshot()` in `run_signals.py` step 7, feeding richer context into `AdaptiveStrategySelector`.

**What it does:**
Currently the regime snapshot is purely quantitative:
```python
{"pct_uptrend": 0.22, "pct_downtrend": 0.71, "avg_atr_pct": 0.018, "universe_size": 24}
```

A `RegimeContextAgent` would compute additional breadth signals and synthesize them:

Additional signals (all computable from existing OHLC cache, no new data):
- `pct_above_sma_200` — % of 150-symbol universe above 200d MA
- `advance_decline_5d` — ratio of symbols up vs down over 5 days
- `sector_breadth` — which sectors (IT, BANK, PHARMA, etc.) are in uptrend vs downtrend
- `vol_trend` — is ATR expanding or contracting over the past 10 days (regime transition signal)

LLM synthesizes these into a structured regime label:
```
BEAR_CONFIRMED     → pct_downtrend > 60%, pct_above_200d < 30%
BEAR_WATCH         → pct_downtrend 45-60%, mixed breadth
TRANSITION_UP      → pct_downtrend falling, advance_decline improving
SIDEWAYS_CHOPPY    → pct_downtrend 35-50%, vol_trend contracting
BULL_EARLY         → pct_above_200d crossing 50%, advance_decline > 1.5
BULL_CONFIRMED     → pct_above_200d > 70%, most sectors in uptrend
```

**Value:**
- More nuanced than binary UPTREND/DOWNTREND per stock
- `TRANSITION_UP` is the highest-value label — it lets the system begin positioning 1-2 weeks before current rules would fire
- Currently the system would stay fully off during a `TRANSITION_UP` because 71% downtrend still triggers CB
- This agent could selectively unlock RSI-MR (mean reversion) while keeping Breakout/DualMA off during transition

**Implementation sketch:**
```python
# app/meta/regime_context_agent.py
class RegimeContextAgent:
    def build_snapshot(self, symbol_states: dict, dynamic_cache: dict) -> dict:
        # compute breadth signals from existing caches
        # call LLM to synthesize regime label
        # return enriched snapshot dict
```

**Priority:** HIGH. This is the most impactful single change. The current system's biggest failure mode is staying dark during the early recovery phase of a bear market. A `TRANSITION_UP` label would allow selective re-entry before the SMA_50-based rules catch up.

---

### Agent 3 — EntryTimingAgent  *(Pre-signal gate)*

**Where it plugs in:** Between `MultiStrategyRouter.decide()` and `RiskAgent.evaluate()` — a proposed BUY passes here before being risk-sized.

**What it does:**
Reviews each proposed BUY individually and either approves, defers, or rejects. This is the most surgical LLM integration — it acts on individual stock-level decisions.

Inputs per proposed BUY:
- Full `MarketState` (all 20 indicators)
- Strategy that proposed it
- Current portfolio (open positions, sector exposure)
- Regime label

LLM output:
```json
{ "symbol": "AXISBANK", "decision": "approve",
  "reason": "RSI_2=4, above SMA_20, volume 2.3× avg, BANK sector showing breadth recovery" }

{ "symbol": "HDFCBANK", "decision": "defer",
  "reason": "Earnings in 4 days (Q4 result). Wait until post-announcement." }

{ "symbol": "TCS", "decision": "reject",
  "reason": "IT sector showing 3 consecutive down weeks. Breakout signal is against sector trend." }
```

**Value:**
- Earnings avoidance — the single most actionable improvement (mentioned in docs as pending)
- Sector momentum alignment — avoid IT breakouts when IT sector is in downtrend
- Position concentration — reject if we already have 3 open positions in BANK sector
- This is the "second opinion" layer — rules get you 80% there, LLM handles the edge cases

**Cost:**
- 1 LLM call per proposed BUY (typically 2-8 calls per day in normal markets)
- Requires an earnings calendar feed or lightweight hardcoded NSE earnings dates

**Priority:** HIGH for earnings avoidance specifically — this can be implemented as a rule-based gate first (no LLM needed), then upgraded to LLM later. The earnings calendar is the blocking dependency.

---

### Agent 4 — PortfolioConstructionAgent  *(Position sizing)*

**Where it plugs in:** Replaces/augments `RiskAgent._size_position()` for the portfolio-level allocation decision.

**What it does:**
Currently each position is sized independently by ATR stop distance. There is no portfolio-level awareness:
- If 4 positions are in highly correlated stocks (all NSE banks), the effective risk is 4× intended
- If the portfolio is 80% in IT stocks, a sector crash wipes 80% of open positions simultaneously

A `PortfolioConstructionAgent` would:
1. Compute pairwise correlation of proposed new position with existing positions (from OHLC cache)
2. Check sector concentration
3. Scale position size down if correlation is too high

This is actually implementable **without LLM** — pure pandas correlation math. LLM adds value only for the narrative explanation and edge-case handling.

**Value:**
- Reduces correlated drawdowns significantly
- Would have materially helped in 2022 bear — many portfolio losses came from sector-level drawdowns, not individual stock risk

**Priority:** Medium. Implement the rule-based correlation check first (30 lines of pandas). LLM layer is optional.

---

## Priority Order

| # | Change | Type | Impact | Effort |
|---|--------|------|--------|--------|
| 1 | **Earnings avoidance gate** | Rule-based | High — removes known failure mode | Low |
| 2 | **RegimeContextAgent** (breadth signals + TRANSITION_UP) | LLM | High — unlocks early recovery re-entry | Medium |
| 3 | **Sector concentration limit** | Rule-based | Medium — reduces correlated drawdowns | Low |
| 4 | **EntryTimingAgent** (sector trend alignment) | LLM | Medium — better entry quality | Medium |
| 5 | **StockInsightAgent** (universe ranking) | LLM | Low-Medium — mostly adds explainability | High |
| 6 | **PortfolioConstructionAgent** (correlation sizing) | Rule/LLM | Medium | Medium |

---

## What Is More Important Right Now

Before building new agents, two things have higher leverage:

### 1. Earnings Avoidance (no new agent needed)
The NSE Q4 results season starts ~April 2026. Entering positions 3-5 days before earnings announcements is the single most avoidable loss source. This needs:
- A hardcoded or fetched `earnings_dates` dict in `run_signals.py`
- A 5-line check in the signal loop: `if days_to_earnings(symbol) <= 5: skip`
- No LLM, no new architecture — just a guard

### 2. `TRANSITION_UP` Regime Detection
The current system correctly stayed dark during Feb–Mar 2026 (confirmed by the diagnostic: all configs lost money). But when the recovery begins, the SMA_50-based regime detection will lag by 3-6 weeks. The `RegimeContextAgent` using breadth signals (`pct_above_sma_200`, `advance_decline_5d`) would catch it 2-3 weeks earlier.

This is the difference between the system re-entering at Nifty 22,000 vs 24,000 in the next bull phase.

---

## How the LLM Fits In Each Agent

| Agent | LLM Role | Prompt Input | LLM Output |
|-------|----------|-------------|------------|
| `AdaptiveStrategySelector` (existing) | Strategy weight allocation | Regime label + strategy Sharpe table | Weight vector |
| `RegimeContextAgent` | Synthesize breadth into regime label | pct_uptrend, pct_above_200d, advance_decline, sector_breadth, vol_trend | Regime label + confidence |
| `EntryTimingAgent` | Per-trade gate | MarketState, portfolio, earnings proximity | approve / defer / reject + reason |
| `StockInsightAgent` | Universe ranking | Indicator snapshot for top-30 candidates | Ranked list with rationale |

The existing `AdaptiveStrategySelector` already handles the **"which strategy to run"** question. The new agents handle **"which stocks to consider"** (StockInsightAgent), **"what market phase are we in"** (RegimeContextAgent), and **"is this specific entry sound"** (EntryTimingAgent). They operate at different granularities and are non-overlapping.

---

---

## News & Daily Affairs Integration

### Why the current system is news-blind

Every signal today is derived exclusively from OHLC price data. The system has no awareness of:
- An RBI rate decision tomorrow morning
- A promoter pledging shares in a stock it just bought
- Earnings results released after market close
- A sector-wide regulatory action (e.g., SEBI order on an NBFC)
- FII selling ₹5,000 crore in a single session

These events move stocks 5-15% overnight and are invisible to any indicator computed from yesterday's close. News integration is the single highest-leverage addition that is **not derivable from price data**.

---

### Types of News That Matter

| Category | Examples | Frequency | Impact window |
|----------|----------|-----------|---------------|
| **Company event** | Earnings, AGM, board meeting, promoter buy/sell | Daily | 1-5 days |
| **Regulatory** | SEBI action, RBI diktat on NBFC/bank, drug recall (pharma) | Weekly | 1-10 days |
| **Macro / policy** | RBI MPC decision, Union Budget, US Fed meeting, CPI print | Monthly | 1-3 weeks |
| **Market structure** | F&O ban list entry/exit, index rebalancing, circuit filter hit | Daily | 1-2 days |
| **Sector** | Auto monthly sales data, IT deal wins, bank NPA disclosures | Monthly | 3-7 days |
| **Global** | US earnings (Nasdaq move), crude oil spike, China macro shock | Daily | 1-2 days |

---

### Integration Points — Where News Adds Value

#### Point 1 — Pre-universe filter: Macro circuit breaker  *(highest value)*

**Where:** Before `DynamicUniverseAgent.select_candidates()` runs. At the top of `run_signals.py`.

**What:** A daily macro news digest is checked before anything else. If a high-impact scheduled event is happening today or tomorrow (RBI MPC, US Fed, Budget, major global event), the system can:
- Suppress all new BUY signals (same as `SUPPRESS_NEW_BUYS=1` today, but automated)
- Or downsize position sizing by 50% to reflect uncertainty

This is already half-implemented as a manual env var (`SUPPRESS_NEW_BUYS`). A `MacroCalendarAgent` would automate it by reading a scheduled events calendar and setting the flag programmatically.

**Data needed:** A simple hardcoded or fetched economic calendar (RBI MPC dates, US Fed dates, India CPI/GDP release dates). NSE publishes these. No LLM required for the calendar check; LLM optional for interpreting surprise vs expected outcomes.

**Value:** Avoids entering positions the day before a known volatility spike. High value, low effort.

---

#### Point 2 — Universe filter: Stock-level news blacklist  *(high value)*

**Where:** Inside or just after `UnionUniverseFilter`, before `MarketObserverAgent.preload()`.

**What:** Any stock that has a material negative event in the past N days is removed from the candidate universe entirely, regardless of its technical signals.

Negative events that should blacklist a stock (3-5 day window):
- Promoter pledge increase > 5% of total shares
- SEBI show-cause notice or exchange query
- Auditor resignation or qualification
- Earnings miss > 15% of estimates
- Credit rating downgrade

This prevents the system from chasing a "breakout" that is actually the last buyers exiting before a collapse. Technically attractive stocks with news-driven hidden risk are the most dangerous entries.

**Data needed:** NSE corporate announcements API (free, JSON). BSE Listing Center. Scraping is feasible. LLM adds value here for classifying announcement text as positive/negative/neutral when the event type isn't obvious.

**LLM role:** Feed the raw NSE announcement text → LLM classifies as `BLACKLIST / NEUTRAL / POSITIVE` with a one-line reason. Cached daily.

---

#### Point 3 — EntryTimingAgent enrichment: Per-trade news context  *(medium value)*

**Where:** Inside `EntryTimingAgent` (the proposed per-trade gate between router and RiskAgent).

**What:** Before approving a BUY, the agent checks if there is recent news on that specific stock and feeds it to the LLM as additional context alongside the technical indicators.

Prompt enrichment:
```
Symbol: AXISBANK
Technical: RSI_2=4, SMA cross age=8, relative volume=2.1×
Recent news (last 3 days):
  - AXISBANK Q3 net profit up 18% YoY, in line with estimates (2 days ago)
  - RBI imposes ₹2 crore penalty on AXISBANK for KYC non-compliance (1 day ago)

Approve / defer / reject this BUY?
```

Without news, the LLM sees only technical context. With news, it can correctly reject an entry where the penalty creates headline risk, even though the Q3 result was fine.

**Data needed:** NewsAPI.org (free tier: 100 req/day), or Google News RSS per symbol. This is sufficient for 10-20 trade decisions per day.

---

#### Point 4 — RegimeContextAgent enrichment: Macro news for regime label  *(medium value)*

**Where:** Inside `RegimeContextAgent.build_snapshot()` (the enhanced regime snapshot).

**What:** The regime label currently comes from price-derived breadth (% stocks above SMA_50). Adding a macro news digest enriches the regime classification:

- RBI surprise rate cut → upgrades SIDEWAYS_CHOPPY to TRANSITION_UP immediately (not after 3 weeks of SMA convergence)
- US Fed hawkish surprise → downgrades BULL_EARLY to BEAR_WATCH before the price data catches up
- FII net buying for 5 consecutive days → positive weight toward TRANSITION_UP even if SMA_50 hasn't crossed

This is the most impactful use of news in the entire system. A single RBI cut can cause a 3% single-day Nifty rally. Without news, the system would need ~15 trading days of price data before the SMA_50-based regime logic catches it. With a macro news feed, regime can update same day.

**LLM role:** Given today's macro news digest + current price-based regime signals, synthesize a regime label and confidence score. The LLM is well suited here because macro interpretation is inherently qualitative.

---

#### Point 5 — AdaptiveStrategySelector: Strategy weight context  *(low-medium value)*

**Where:** Inside the existing `AdaptiveStrategySelector` prompt, as additional context.

**What:** Currently the LLM prompt for strategy weights contains only the regime label and historical Sharpe table. Adding a one-paragraph weekly macro digest gives the LLM context it currently lacks:

```
Current macro context (week of March 24, 2026):
- RBI held rates at 6.25% (in line with expectations)
- FII net sold ₹8,200 crore in equities this week
- US Fed minutes suggested 1 cut in 2026 vs prior 2 cuts expected
- Nifty Bank underperformed Nifty by 2.1% this week
```

With this, the LLM can correctly reduce DualMA weight (trend strategy) and increase RSI-MR weight (mean reversion) in a rate-hold + FII selling environment — rather than relying purely on the Sharpe table which may lag current conditions.

**Data needed:** A weekly 200-word macro digest. Could be auto-generated by a separate LLM call summarising the week's headlines, or manually written (15 minutes on Sunday).

---

### Data Sources (all free or low-cost)

| Source | What it provides | Cost | Integration effort |
|--------|-----------------|------|--------------------|
| **NSE Corporate Announcements API** | Earnings dates, board meetings, promoter disclosures | Free | Low — JSON REST API |
| **BSE Listing Center** | Same as NSE, sometimes faster | Free | Low |
| **RBI website** | MPC dates, rate decisions | Free | Low — parse calendar page |
| **NSE F&O ban list** | Daily ban list (stocks in ban can't have new positions) | Free | Very low — single URL |
| **NewsAPI.org** | Company and sector news headlines | Free tier (100/day) | Low — REST API |
| **Google News RSS** | Per-symbol news feed | Free | Low — RSS parse |
| **Economic Survey / Budget** | Annual macro context | Free | Manual — once a year |

The paid sources (Bloomberg, Refinitiv) add breadth and reliability but are not necessary for the value described above. The free tier of NewsAPI.org and NSE's own APIs cover 90% of what's needed.

---

### News Integration Priority

| # | Integration point | Value | Effort | Data source |
|---|-------------------|-------|--------|-------------|
| 1 | **Macro calendar → auto SUPPRESS_NEW_BUYS** | High | Low | RBI/Fed hardcoded dates |
| 2 | **F&O ban list check per symbol** | High | Very Low | NSE ban list URL |
| 3 | **Earnings date guard (per stock)** | High | Low | NSE Corporate API |
| 4 | **Stock blacklist from NSE announcements** | High | Medium | NSE Corporate API + LLM classify |
| 5 | **Macro digest → RegimeContextAgent** | High | Medium | NewsAPI + LLM summarise |
| 6 | **Per-trade news → EntryTimingAgent** | Medium | Medium | NewsAPI per symbol |
| 7 | **Weekly macro digest → AdaptiveStrategySelector** | Medium | Low | Manual or LLM-generated |

---

### What the pipeline looks like with news integrated

```
Macro calendar check          ← NEW: suppress BUYs on event days (RBI, Fed, Budget)
    │
    ▼
F&O ban list check            ← NEW: remove banned stocks before universe scan
    │
    ▼
DynamicUniverseAgent          ← unchanged
    │
    ▼
UnionUniverseFilter           ← unchanged
    │
NSE announcements blacklist   ← NEW: remove stocks with negative corporate events
    │
    ▼
MarketObserverAgent           ← unchanged
    │
    ▼
RegimeContextAgent            ← ENHANCED: breadth signals + macro news digest
    │  richer regime label (TRANSITION_UP, BEAR_CONFIRMED, etc.)
    ▼
AdaptiveStrategySelector      ← ENHANCED: macro digest added to prompt
    │
    ▼
MultiStrategyRouter           ← unchanged
    │
    ▼
EntryTimingAgent              ← NEW: per-trade gate with stock news context
    │
    ▼
RiskAgent                     ← unchanged
    │
    ▼
signal_queue
```

### Summary

News adds value at **5 distinct points** in the pipeline. The two highest-leverage, lowest-effort additions are:
1. **F&O ban list check** — 10 lines of code, free, catches a known category of forced sellers
2. **Macro calendar auto-suppress** — automates what `SUPPRESS_NEW_BUYS` does manually today

These require no LLM and no new architecture. Everything else builds on top of them.

---

## Suggested Implementation Sequence

```
Phase 1 — Rule-based guards (no LLM, no new architecture):
  ├── F&O ban list check       — remove banned symbols before universe scan
  ├── Earnings date guard      — skip BUY if earnings within 5 days (NSE Corporate API)
  ├── Macro calendar suppress  — auto SUPPRESS_NEW_BUYS on RBI/Fed/Budget days
  └── Sector concentration     — max 2 open positions per sector in RiskAgent

Phase 2 — New agents, no LLM yet:
  ├── RegimeContextAgent       — breadth signals (pct_above_200d, advance_decline),
  │                              rule-based TRANSITION_UP / BULL_EARLY labels
  └── PortfolioConstructionAgent — correlation check, scale sizing for correlated entries

Phase 3 — LLM enrichment:
  ├── NSE announcement classifier  — LLM classifies corporate announcements as
  │                                  BLACKLIST / NEUTRAL / POSITIVE (cached daily)
  ├── RegimeContextAgent upgrade   — add macro news digest to regime synthesis prompt
  ├── EntryTimingAgent             — per-trade LLM gate with stock news context
  └── Wire reasons into signal_queue.notes for full explainability

Phase 4 — Weekly macro digest:
  ├── Auto-generate weekly macro summary (LLM call on Sunday)
  └── Feed into AdaptiveStrategySelector prompt alongside Sharpe table

Phase 5 — Optional, high effort:
  └── StockInsightAgent — LLM universe ranking (explainability, marginal alpha)
```
