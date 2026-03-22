# Hold Logic, Bull 2019 Losses & Future Improvements

**Last updated**: 2026-03-22

---

## 1. Bull 2019 Loss Analysis

### 1.1 What the data shows

Both EqualWeight (-4.19%, Sharpe -0.54) and Adaptive (-4.82%, Sharpe -0.47) lost money
in the 2019–2020 Bull period, despite every individual strategy being profitable on its own:

| Strategy | Sharpe | Return | #Trades |
|---|---|---|---|
| DualMA | -0.02 | -1.01% | 66 |
| Breakout | 0.68 | +8.82% | 374 |
| QuietBrk | 0.80 | +10.38% | 242 |
| TrendPB 5% | 0.97 | +4.89% | 124 |
| RSI-MR | 0.37 | +3.13% | 416 |
| **EqualWeight** | -0.54 | **-4.19%** | **1132** |
| **Adaptive** | -0.47 | **-4.82%** | **842** |

### 1.2 Root cause: commission drag at high trade frequency

The multi-strategy portfolio trades 1132 times in 13 months at 0.15% round-trip cost:

```
1132 trades × 0.15% × ~₹50,000 avg position = ~₹84,900 in commissions
Starting capital ₹1,000,000 → ~8.5% gross drag just from costs
```

Individual strategies are individually profitable (Breakout +8.82%, QuietBrk +10.38%)
because they trade fewer times with less overlap. Merged together at 20% weight each:
- Each strategy only deploys 20% of the capital it would solo
- But each strategy still fires its full number of entry/exit signals
- The 5-strategy pool generates 5× the trade frequency at 1/5 the per-trade position size
- Cost load relative to gross PnL is far higher than any single-strategy run

### 1.3 The RECOVERY mis-classification in 2019

The adaptive log shows RECOVERY/HIGH firing most weeks through 2019 (Jan-Jun, Sep-Dec).
This means NSE breadth consistently exceeded 60% UPTREND with ATR > 2.2% even after
the threshold increase. 2019 was a choppy-but-positive year — the market kept oscillating
between RECOVERY-like and brief BEAR spikes:

```
Jan 2019: RECOVERY → BEAR_CONFIRMED (Jan 27) → CRASH (Feb 3) → BEAR_EARLY → RECOVERY
Jul 2019: CRASH_HIGHVOL (3 weeks) → BEAR (Aug) → CRASH (Sep) → MIXED → RECOVERY (Oct)
```

The regime was flip-flopping weekly, causing the adaptive selector to whipsaw allocations.
In a genuinely trending bull, this wastes rebalance cycles and destabilises positions.

### 1.4 Why adaptive loses more than equal-weight in 2019

- Adaptive had 842 trades vs EW's 1132 — fewer trades, yet worse outcome
- The allocation churn shifted capital away from the two best strategies (Breakout, QuietBrk)
  during BEAR_CONFIRMED / CRASH_HIGHVOL weeks — exactly when those strategies' existing
  positions needed to be held, not the capital redirected
- DualMA at 73% during the Aug 2019 mini-bear deployed large positions in a period where
  DualMA generated -1.01% return for the full year — capital concentrated in the weakest
  strategy during a brief bear that lasted only 2-3 weeks

---

## 2. Existing Hold / No-Trade Logic (Full Inventory)

The system already has multiple layers that suppress unnecessary trades. Here is every
mechanism currently active:

### 2.1 Per-strategy HOLD emission (strategy layer)

Each strategy emits `Decision(action="HOLD")` when the entry/exit condition is not met.
This is not "do nothing" — it is an explicit signal that triggers the ATR stop check in
RiskAgent for any held positions.

| Strategy | HOLD when |
|---|---|
| `DualMA` | No crossover event (flat trend, both MAs moving together) |
| `BreakoutMomentumStrategy` | In position + price ≥ SMA_10 (holding intact) |
| `QuietBreakoutStrategy` | In position + price ≥ SMA_20 (holding intact) |
| `TrendPullbackStrategy` | In position + no exit signal |
| `RSI-MR` | RSI between oversold and overbought thresholds |
| All strategies | Required indicators (ATR, SMA, etc.) not yet available |

**Critical design note**: Breakout and QuietBrk explicitly emit HOLD for in-position
symbols (lines 59-65 in `breakout_momentum.py`, lines 66-72 in `quiet_breakout.py`).
Without this, the RiskAgent's ATR stop would never check those positions — a gap-down
that breached the stop but landed above SMA_10 would not trigger the exit.

### 2.2 RiskAgent HOLD conversions (risk layer)

`RiskAgent.evaluate()` converts BUY → HOLD in these cases:

| Condition | Code location | Effect |
|---|---|---|
| Breadth circuit breaker | `risk/agent.py:49-58` | Blocks ALL new entries when >40% of universe in DOWNTREND |
| Regime filter | `risk/agent.py:62-68` | Blocks entry if stock's own regime not in `allowed_regimes` |
| ATR stop hit | `risk/agent.py:70-80` | Converts HOLD → SELL (overrides strategy signal) |
| Already in position | `risk/agent.py:93-95` | Prevents duplicate BUY on same symbol |
| Insufficient cash | `risk/agent.py:106-110` | Skips entry if position would cost more than available cash |
| Vol sizing = 0 shares | `risk/agent.py:103-104` | ATR-based quantity rounds to zero (too expensive/wide stop) |

### 2.3 MultiStrategyRouter filters (routing layer)

| Condition | Code location | Effect |
|---|---|---|
| Strategy weight < 0.01 | `multi_router.py:127-128` | Skips strategy entirely (treated as disabled) |
| Cross-strategy SELL | `multi_router.py:141-144` | Discards SELL from non-owning strategy |
| Per-strategy regime gate | `multi_router.py:188-197` | Filters symbol_states to only allowed regimes |
| SELL > BUY > HOLD priority | `multi_router.py:232-235` | Most defensive action wins conflicts |

### 2.4 Per-strategy regime allowlists

Configured in `run_experiments.py` via `allowed_regimes` parameter to `MultiStrategyRouter`:

```python
_UPTREND_ONLY = [regime strings containing "UPTREND"]
# QuietBrk: only sees UPTREND stocks — Bear losses near-zero
# RSI-MR:   only fires in UPTREND/SIDEWAYS — blocks bear mean-reversion entries
# DualMA:   no filter — runs on all regimes (handles bear exposure)
```

---

## 3. What Is NOT Yet In the System (Gaps That Explain Bull 2019 Losses)

### 3.1 No minimum holding period

A Breakout entry can be exited after 1 day if price dips below SMA_10 on the next bar,
then re-entered the following day when it bounces back. This generates 3 round-trips
(BUY → SELL → BUY) from what should be 1 trade. In a choppy 2019 market this is common.

**No mechanism currently prevents re-entering the same symbol within N days of exit.**

### 3.2 No portfolio-level daily trade cap

In a 60-80 stock universe, on a high-signal day all strategies can simultaneously
generate 10-20 BUY signals. Each fires regardless of how many other trades are
happening. There is no "we've traded enough today" gate.

### 3.3 No signal persistence requirement

Entry fires the moment `price > high_10d` (Breakout). If the price closes at exactly
the breakout level and pulls back the next day, it was a false breakout. A 2-day
persistence check (must close above high_10d for 2 consecutive days) would eliminate
many of these false entries in choppy conditions.

### 3.4 No expected-return vs cost threshold

The system enters any signal that passes regime and risk checks regardless of whether
the expected gross return exceeds the round-trip cost. In a low-ATR choppy market,
ATR-based stops are tight, positions are small, and the cost-to-return ratio is poor.

---

## 4. Improvements — Status as of 2026-03-22

### ✅ 4.1 Minimum trade quality filter (done)

`min_atr_cost_ratio=3.0` added to `RiskAgent` and wired in `run_signals.py`.
ATR must be ≥ 3× round-trip cost (0.45% min). Fires only in low-ATR environments —
Bear 2022 and Recovery 2020 results unchanged (ATR is high in those periods).

### 4.2 Signal persistence: 2-day breakout confirmation (open)

Require `price > high_10d` for 2 consecutive days before entering.
Needs `prev_high_10d` in `market_state.previous_indicators`. ~30-40% fewer false entries
in choppy markets. Build after paper trade baseline is established.

### 4.3 Portfolio trade rate limiter (open, low priority)

Cap total new entries across all strategies to N per week.
Risk: may block valid Recovery breakout clusters. Calibration-sensitive.
Deprioritised — min ATR filter addresses the core cost-drag issue more cleanly.

### ✅ 4.4 Regime stability gate (done)

`regime_stability_weeks=2` in `AdaptiveStrategySelector`. The 2019 whipsaw
(RECOVERY → BEAR_CONFIRMED → CRASH → RECOVERY in 3 weeks) will no longer trigger
full capital reallocation on 1-week regime spikes. State persists via `selector_state` DB table.

---

## 5. News Handling Agent — Analysis

### 5.1 Is it a good strategy?

**Yes, as a negative filter (block bad entries) — No, as a primary selector.**

The strongest evidence-based use case for news in quantitative trading is blocking
entries when there is known negative information: earnings misses, regulatory actions,
promoter selling, or sector headwinds. Using news as a *positive* selector (buy on
good news) is harder to reliably implement and more prone to overfitting.

For NSE specifically:
- Earnings season (quarterly results) is highly predictable — companies are required
  to announce within 45 days of quarter end
- SEBI regulatory actions, promoter pledging disclosures, and insider trading
  disclosures are public and often precede technical breakdown
- RBI monetary policy decisions (6 per year) are known dates — avoid entries the day
  before or after for volatility-sensitive strategies

### 5.2 Architecture options

#### Option A: Pre-entry news filter (recommended first step)

```
DynamicUniverseAgent → top 80 candidates
    ↓
NewsFilterAgent.filter(candidates, current_date)
    → remove any symbol with negative news in last 7 days
    → returns filtered list (60-75 symbols typically)
    ↓
UnionUniverseFilter → per-strategy pools
```

Data source options:
- **NSE announcements feed** (free): earnings releases, board decisions, dividend
  announcements — available via NSE website or Yahoo Finance `news` attribute
- **Financial newspapers API** (paid): Economic Times, Business Standard, Moneycontrol
- **Google News / RSS** (free but noisy): requires keyword + company name matching

Negative news signals worth filtering on:
- Revenue miss or guidance cut in earnings announcement
- Promoter stake reduction >2%
- SEBI show-cause notice or investigation announcement
- Sector regulator adverse order (TRAI, IRDA, SEBI, RBI)
- Debt downgrade by CRISIL/ICRA

#### Option B: Macro news as regime input

Incorporate known macro events into the regime classifier:

```python
# Hypothetical macro_event_flag in regime_snapshot
if rbi_policy_day_within_3_days:
    snapshot["macro_uncertainty"] = True
# → regime classifier can shift from BULL_SUSTAINED to MIXED on policy days
```

Known NSE macro catalysts:
- RBI MPC meeting (every 2 months) — increases ATR before announcement
- Union Budget (Feb 1) — historically high volatility day
- US Fed meetings — correlated volatility in NSE export/IT stocks
- MSCI/FTSE rebalance dates — mechanical flows distort individual stock signals

#### Option C: Sentiment scoring for position sizing

Score each candidate from -1 (strongly negative news) to +1 (no bad news / positive news).
Feed this as a modifier to `risk_per_trade_pct` in RiskAgent:

```python
sentiment_modifier = news_agent.get_score(symbol, current_date)  # -1 to 1
adjusted_risk_pct = base_risk_pct * (1.0 + 0.5 * sentiment_modifier)
# Positive sentiment → slightly larger position
# Negative sentiment → smaller position (or 0 = skip)
```

### 5.3 Realistic impact assessment

| Use case | Expected impact | Implementation complexity |
|---|---|---|
| Block entries on known negative events (earnings miss, SEBI notice) | -15 to -25% fewer losing trades | Low — NSE announcements feed is structured |
| Avoid positions ±2 days around earnings dates | Reduces event-driven gaps | Very low — dates known in advance |
| Macro event awareness in regime classifier | Smoother Bear-to-Recovery transition | Medium |
| Full sentiment scoring | Marginal on top of above | High — NLP model, NSE corpus |

### 5.4 Recommendation

**Phase 1** (implement now, low risk):
1. Add an earnings date avoidance gate: avoid new entries within 3 days of a known
   earnings announcement for any symbol in the universe
2. Block entries on symbols with SEBI action or major corporate event in past 7 days

**Phase 2** (after validating Phase 1):
3. RBI/Budget macro awareness → shift regime toward MIXED on known high-uncertainty dates
4. Promoter pledging / insider selling disclosure filter

**Phase 3** (if Phase 1-2 show measurable improvement):
5. Full NLP sentiment scoring on NSE announcements and financial press

---

## 6. Deployment Strategy — Current Market Context (March 2026)

### 6.1 Should you deploy now?

**Short answer: not with real money yet. Paper trade first — and the current market
environment makes this even more important than usual.**

The system has only been validated on historical backtests from 2018–2024. Before live
deployment, two things must be true:
1. The strategy produces results in live conditions that match the backtest pattern
2. You understand how the strategy behaves in the specific regime you're entering

Neither condition is currently met. The backtest still has known structural issues
(RECOVERY over-triggering, Bull 2019 drag, look-ahead bias in the Sharpe table).
Going live with unresolved structural issues means you cannot tell whether a live loss
is bad luck, a market regime the system mishandles, or a bug.

### 6.2 The current market context: news-driven bearish regime

As of March 2026, the market is in a **news-driven bear** — which is structurally
different from the data-driven bear the system was trained on.

**What the backtest bears looked like (2018–2024):**
- 2022 bear: slow-grinding, breadth-driven — pct_downtrend built up over months
- COVID crash: fast (3 weeks down, 8 weeks up) but the signal was clear in price action
- Both were captured reasonably well by the regime classifier once they were underway

**What a war/conflict-driven bear looks like:**
- Regime can flip in hours on a single headline (ceasefire rumour = +3%, escalation = -4%)
- pct_downtrend may not be extreme even when the market is genuinely vulnerable
  (stocks rally on rumoured peace, fall on fresh news — breadth oscillates)
- The 4-week rolling history the LLM uses will be full of contradictory signals
- DualMA SMA20/50 cross takes 2–3 weeks to confirm — it will be late by days that matter

**Why this is important for your strategy:**
The system's regime classifier was calibrated on orderly macro-driven bears. In a
headline-driven market, the classifier will likely oscillate between BEAR_EARLY and
MIXED week-to-week, underweighting the defensive allocation at exactly the wrong moment.

### 6.3 Paper trading plan — what to run and what to watch

**Phase 1: Paper trade for 6–8 weeks minimum (now)**

Run the adaptive multi-strategy system in paper trading mode:

1. **Match live data to backtest universe**: use the same Nifty50 + NiftyNext50 +
   NiftyMidcap50 universe. Do not expand it.

2. **Log every adaptive selector call**: capture the date, regime label, confidence,
   weight vector. Compare to what the backtest predicted for similar market conditions.

3. **Track these specific metrics weekly:**
   - Did `BEAR_CONFIRMED` fire when you subjectively judged the market to be bearish?
   - Did the weight shift actually reduce drawdown, or did it arrive 1-2 weeks late?
   - What is the trade count per week vs the backtest average? (Bull 2019: ~22/week; Bear 2022: ~8/week)
   - Are commissions eating into gross PnL at the expected rate?

4. **Failure conditions that should delay real-money deployment:**
   - Paper portfolio drops >8% in any 4-week window (max expected from backtest: 5-6%)
   - Regime label oscillates >3 times in one month (classifier is confused)
   - Trade count exceeds 2× backtest average for that regime type (signal quality issue)
   - Adaptive consistently underperforms equal-weight for 4+ consecutive weeks

**Phase 2: Real money with tight size limits (after 6-8 clean paper weeks)**

Start at 10–20% of intended capital. Do not increase size until:
- 3 full months of live results within ±20% of backtest expected return for the regime
- MaxDD never exceeded 12% (backtest worst case: 22% full-period)
- You have personally seen the system navigate at least one regime transition correctly

### 6.4 Should you add the news filter before going live?

**Yes — and the current news-driven market makes it more valuable than usual.**

In a war/conflict market, news is the primary price driver, not technicals. The news
filter is not optional in this environment — it is the only mechanism the system has
to avoid buying into a stock that is about to gap down on an unexpected headline.

**What to add before paper trading, ranked by effort vs impact:**

| Priority | Feature | Why now | Effort |
|---|---|---|---|
| 1 | **Earnings date avoidance** (±3 days) | NSE Q4 results season is April-May 2026 | 1-2 hours — dates are structured data |
| 2 | **BEAR_CONFIRMED breadth CB** | Market is bearish — suppress new BUY signals when >40% downtrend | Already in code (`breadth_circuit_breaker=True`) — just enable it |
| 3 | **Macro event calendar** | RBI MPC next meeting, Budget impact still digesting | 2-3 hours — known dates, flag as MIXED |
| 4 | **NSE corporate action filter** | SEBI notices, promoter selling — material during conflict risk-off | 3-4 hours — structured announcements feed |
| 5 | **Global conflict headline filter** | Block new entries on days with active escalation news | High effort, high noise — Phase 2 |

**Quick win that is already in the code but may not be enabled:**

The `breadth_circuit_breaker` in RiskAgent defaults to `False`. In the current market:
```python
risk_agent = RiskAgent(
    breadth_circuit_breaker=True,   # ← enable this now
    max_downtrend_pct=0.35,         # ← tighter threshold for conflict markets (vs 0.40)
)
```
This requires zero new code — just change the parameter in `run_experiments.py` and
in your live trading setup. When >35% of the universe is in DOWNTREND, all new BUY
signals are blocked system-wide until breadth recovers.

### 6.5 Recommended deployment sequence

```
Now (March 2026)
│
├─ Week 1-2: Enable breadth_circuit_breaker=True in paper run
│            Add earnings date avoidance gate (Phase 1 news filter)
│
├─ Week 3-8: Paper trade full adaptive system
│            Log regime calls vs actual market moves
│            Monitor: is DualMA receiving appropriate weight in current bear?
│
├─ Month 3:  If paper performance matches backtest pattern:
│            Deploy 10-20% of target capital, real money
│            Keep position sizes small (risk_per_trade_pct = 0.003 initially)
│
├─ Month 4-6: If live MaxDD < 12% and regime calls look correct:
│             Scale to 50% of target capital
│             Add macro event calendar awareness
│
└─ Month 7+:  Full capital if all metrics within tolerance
              Consider GPT-4o upgrade for final live validation
```

### 6.6 The honest risk assessment (updated 2026-03-22)

The system is **not ready for real money yet** but is **ready to paper trade**:

**Fixed since last assessment:**
- Min ATR-to-cost filter — Bull 2019 commission drag partially addressed
- Regime stability gate — 2019 allocation whipsaw addressed
- BULL_SUSTAINED regime — 2023-24 misclassification addressed
- Breadth CB at 0.35 — tighter for current news-driven bear
- Full paper trade pipeline deployed on Railway.app with email notifications

**Still open:**
1. Backtest with all fixes not yet re-run — reference Sharpe numbers are pre-fix estimates
2. Signal persistence (2-day confirmation) not yet built — some choppy-market false entries remain
3. Look-ahead bias in Sharpe table — live will be ~0.8-0.9× backtest Sharpe
4. First live regime transition not yet observed

**What the system is ready for (as of 2026-03-22):**
- Paper trading starts 2026-03-23 — `run_signals.py` auto-runs at 3:35 PM IST
- Regime call quality can be evaluated weekly against subjective market assessment
- The 2022-style bear edge (Adaptive Sharpe 1.30 vs EW 0.27) is the clearest validated signal

---

## 7. Summary — Current State vs Recommended Additions

| Layer | Current | Recommended addition |
|---|---|---|
| Per-strategy HOLD | ✅ All strategies emit HOLD | ✅ No change needed |
| ATR stop | ✅ RiskAgent post-signal | Consider tighter stop in low-ATR regimes |
| Breadth circuit breaker | ✅ In RiskAgent (configurable) | Ensure enabled for multi-strategy runs |
| Regime gate per strategy | ✅ MultiStrategyRouter | ✅ No change needed |
| Cross-strategy SELL block | ✅ position_owners tracking | ✅ No change needed |
| Weight floor (DualMA) | ✅ Just added (0.10 floor) | ✅ No change needed |
| RECOVERY threshold | ✅ Just raised to 0.022 | Still over-triggering in 2019 — monitor |
| BULL_SUSTAINED regime | ✅ Just added | Expected to help 2023-24 allocation |
| Min ATR-to-cost ratio | ✅ Built (`min_atr_cost_ratio=3.0`) | — |
| Signal persistence (2-day) | ❌ Not implemented | Add to Breakout/QuietBrk — reduces churn |
| Regime stability gate (2-week) | ✅ Built (`regime_stability_weeks=2`) | — |
| News/event filter | ❌ Not implemented | Phase 1: earnings date avoidance (before April) |
| Macro event awareness | ❌ Not implemented | Phase 2: RBI/Budget MIXED shift |
