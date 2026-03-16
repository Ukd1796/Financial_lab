# Next Improvements Roadmap

## Results Summary — What the Numbers Are Telling Us

### What is working well
| Strategy | Best period | Full-period return | Verdict |
|---|---|---|---|
| CS L=100 momentum | Recovery 2020–21 (198%) | 1051% | Best risk-adjusted over long horizons |
| Breakout 10d | Crash 2020 (53%) | 387% | Most consistent across all regimes |
| DualMA | Recovery 2020–21 (105%) | 186% | Good in sustained trends, fails in chop |
| RSI-MR os=5 ob=80 | Bull 2019 (16%) | 24% | Only works in low-volatility uptrends |

### What the numbers are flagging as broken or suspicious

**1. CS L=100 T=5% and T=3% still produce identical results**
Both show 1051% / 1059% on the full period with the same 81 trades. The `momentum_threshold` parameter is effectively dead — any stock that survives 100 days of price history is already well above both thresholds. The lookback window is the only real parameter.

**2. CS Profit Factor < 1 with positive return in Crash 2020**
CS shows +35% return but PF = 0.45 (losses > gains on a per-trade basis). This contradiction means equity is growing through compounding / position sizing even though the average losing trade is larger than the average winner. Not a bug, but a signal that stop-loss sizing is too loose — the strategy is winning on frequency (53% WR) and position compounding, not on trade quality.

**3. DualMA 14–22% win rate in Bull and Crash periods**
A 22% WR means ~4 out of 5 trades lose. The SMA_20/50 crossover is generating many false signals in choppy markets before a real trend establishes. The regime filter allows some of these through because individual stock regimes don't perfectly track the market phase.

**4. RSI-MR catches falling knives**
In Crash 2020: -17% (os=10) and -9% (os=5). "Oversold" stocks during a broad market crash keep falling. The strategy needs a market-level circuit breaker, not just a per-stock RSI gate.

**5. TrendPullback has high WR but poor capital efficiency**
62–67% win rate across all periods but returns barely beat a savings account on short periods. The pullback threshold is too conservative — it waits for a deeper pullback that often doesn't recover within the max hold window.

**6. No transaction costs**
All returns are gross. NSE brokerage + STT + exchange charges ≈ 0.1% per side. For Breakout with 2,059 trades (full period), that's ~4,100 transaction events. At 0.1% round-trip cost, this erodes ~8–15% from the 387% gross return. Strategies with high trade counts are significantly overstated.

---

## Section A — Quantitative / Systematic Improvements

### A1. Add Transaction Cost and Slippage Modelling
**Priority: High — results are currently misleading without it**

- Add `commission_pct` (default 0.1%) and `slippage_pct` (default 0.05%) to `ExecutionAgent`
- Slippage should scale with position size relative to ADV (average daily volume) — large orders in illiquid stocks have higher impact
- Re-run all experiments and use post-cost metrics as the benchmark going forward
- Expected impact: Breakout's 387% likely drops to ~320–340%; CS (81 trades) barely affected

### A2. Volatility-Adjusted Position Sizing
**Priority: High — current fixed-% sizing ignores stock-level risk**

Current approach: `max_allocatable = total_equity * max_pos_pct` for every stock equally.

Better approach: size inversely proportional to recent volatility so that each position contributes equal risk to the portfolio:
```
quantity = (portfolio_risk_budget) / (atr_14 * price)
```
where `portfolio_risk_budget = total_equity * risk_per_trade_pct` (e.g. 0.5% portfolio at risk per trade). This is equivalent to 1/volatility weighting and prevents high-ATR stocks from dominating drawdowns.

### A3. Market-Level Circuit Breaker for Mean-Reversion
**Priority: Medium — stops RSI-MR from catching falling knives**

RSI-MR needs a market-wide breadth filter before entering any position:
- If Nifty 50 index is below its own SMA_50, suppress all RSI-MR BUY signals
- If the number of stocks in DOWNTREND regime exceeds 60% of the universe, suppress buys

This keeps RSI-MR active during normal corrections but disables it during systemic selloffs.

### A4. Sector / Correlation Concentration Limit
**Priority: Medium — CS and Breakout pile into the same sector**

When CS selects its top-3 momentum stocks, all three are often from the same sector (e.g. all IT or all metals during sector rotations). Add a rule: max 1 position per GICS sector in the portfolio at any time. Requires tagging each symbol with its sector, then filtering `selected` in CS strategy.

### A5. Momentum Quality Score for CS Strategy
**Priority: Medium — the threshold parameter is currently useless**

Replace raw N-day return with a **risk-adjusted momentum score**:
```
momentum_score = N_day_return / rolling_vol_N_day
```
This normalises momentum by the stock's own volatility, so a stock that went up 20% smoothly scores better than one that went up 20% with huge swings. Also adds real differentiation that makes the threshold parameter meaningful.

### A6. Dynamic Lookback for CS Strategy
**Priority: Low — makes the strategy regime-adaptive**

Use a shorter lookback (50d) in high-volatility regimes and longer lookback (120d) in low-volatility regimes. Market trends compress and extend based on macro conditions. Hardcoding 80 or 100 days treats all regimes the same.

### A7. Trailing Stop Instead of Fixed ATR Stop
**Priority: Medium — locks in gains on winning trades**

Current ATR stop: `stop = entry_price - (2 * ATR)` — fixed at entry.

Better: `stop = max(current_stop, close - 2*ATR)` updated daily as the stock moves up. This lets winners run further while cutting losses at the same absolute level. Particularly important for the CS strategy's 1000%+ full-period run — how much of that is being given back unnecessarily?

---

## Section B — LLM Agent Features

These are features where an LLM provides judgement or reasoning that would be difficult to encode purely as rules.

### B1. Adaptive Strategy Selector Agent
**What it does:** At the start of each week, reads the current market regime distribution across the 150-symbol universe (% in UPTREND / SIDEWAYS / DOWNTREND, average ATR percentile, breadth indicators) and outputs a **strategy weight allocation**:
```
{CS: 0.4, Breakout: 0.3, DualMA: 0.2, RSI-MR: 0.1}
```
The LLM is given the backtest performance tables per regime and asked to decide which strategies to emphasise given current conditions. This replaces running all strategies independently with equal weight.

**Why LLM:** The mapping from regime distribution → optimal strategy mix is a pattern-matching problem with many interacting variables. An LLM can reason about relationships like "high-vol sideways with improving breadth historically favours Breakout but not CS" without being explicitly programmed.

### B2. LLM-Powered Trade Reasoning Journal
**What it does:** After each BUY or SELL execution, an LLM agent is called with:
- The symbol, action, price, strategy name
- The current market state (regime, RSI, recent return, ATR)
- The portfolio context (positions, cash, unrealized P&L)

It outputs a 2–3 sentence reasoning entry explaining *why this trade makes sense* (or flags if it looks suspicious). Stored in the `decision_logs` table alongside the existing execution data.

**Why LLM:** Human-readable explanations of systematic decisions are valuable for debugging, auditing, and for understanding when the strategy is firing correctly vs on noise.

### B3. Corporate Action & News Filter Agent
**What it does:** Before each BUY signal is executed, an LLM agent checks whether the target symbol has any known upcoming events in the next 5 days:
- Earnings announcement
- Ex-dividend date
- AGM / board meeting
- Index rebalancing (which creates technical demand/supply)

If a high-risk event is detected, the agent flags the signal as `"HOLD_PENDING_EVENT"` and defers entry until after the event resolves.

**Why LLM:** Parsing and understanding unstructured corporate action data (from NSE announcements, exchange feeds) is a natural-language task. Rules-based parsers break on format variations; LLMs handle this robustly.

### B4. Dynamic Universe Expansion Agent
**What it does:** Once a month, an LLM agent reviews:
- Which symbols consistently appear in the DynamicUniverse top 80 but never pass the strict filter
- Which symbols have zero activity (never selected at all)
- Current Nifty index rebalancing announcements

It then recommends additions/removals to `BROAD_UNIVERSE` and updates `scripts/ingest_symbols.py` automatically, keeping the investable universe fresh without manual intervention.

**Why LLM:** Index composition changes, delistings, and new listings are announced in unstructured text. An LLM can parse these and map them to the correct yfinance ticker format.

### B5. Regime Narrative Agent
**What it does:** At the start of each backtest period (or each trading week in a live system), generates a plain-English summary of the current market environment:
```
"63% of NSE 150 stocks are in UPTREND with MID_VOL. Sector breadth is broad —
 IT (8/10), Banking (7/9), and Auto (6/8) are trending up. Volatility is in the
 40th percentile of the last year. This environment historically favours
 momentum strategies over mean-reversion."
```
This is displayed in the experiment output and stored as a market context snapshot.

**Why LLM:** Synthesising a cross-sectional view of 150 regime labels into a human-readable market narrative is a summarisation task that plays directly to LLM strengths.

### B6. Parameter Tuning Advisor Agent
**What it does:** After each full experiment run, feeds the results table to an LLM and asks for specific, actionable parameter change recommendations:
```
Input:  Full results table across 6 periods
Output: "CS lookback_days=80 outperforms 100 in recovery periods but underperforms
         in bear markets. Suggest testing a regime-adaptive version: 80d when
         >50% of universe is UPTREND, 100d otherwise. Also, momentum_threshold
         of 3% and 5% produce identical results — threshold is dominated by
         lookback; remove threshold as an experiment variable."
```

**Why LLM:** Interpreting multi-dimensional experiment results and generating structured hypotheses is exactly the kind of reasoning LLMs excel at. This replaces ad-hoc manual analysis.

### B7. Portfolio Risk Explainer Agent
**What it does:** After each simulated trading day (or at EOD in a live system), an LLM summarises the portfolio's current risk exposure:
- Open positions with unrealized P&L and distance to ATR stop
- Concentration by sector and strategy
- Any positions approaching their ATR stop or max hold days
- Suggested actions (e.g. "RELIANCE is 15% below entry and 0.3 ATR from stop — consider early exit")

**Why LLM:** Portfolio-level risk communication across multiple open positions requires synthesising many data points into a prioritised action list — a reasoning task.

---

## Section C — Infrastructure Improvements

### C1. Live Paper Trading Mode
Add a `run_paper_trade.py` that runs the full pipeline on today's data (fetched from yfinance intraday) and outputs today's signals without executing. This validates that the backtested logic works on real-time data before committing to live trading.

### C2. Experiment Result Persistence
Currently results are only printed to stdout. Add a `results` table to the DB that stores each experiment run (strategy, period, all metrics) with a run timestamp. This enables:
- Comparing results before and after code changes
- Plotting equity curves
- Tracking parameter sensitivity over time

### C3. Walk-Forward Validation
The current setup backtests on fixed known periods. Add a walk-forward loop: train on years 1–3, test on year 4, roll forward. This tests whether the parameter choices generalise to unseen data or are overfit to the specific periods chosen.

---

## Priority Order

| # | Item | Effort | Impact |
|---|---|---|---|
| 1 | A1 — Transaction costs | Low | High — results currently overstated |
| 2 | B2 — Trade reasoning journal | Low | Medium — operational value immediately |
| 3 | A2 — Volatility-adjusted sizing | Medium | High — better risk per trade |
| 4 | A3 — Market breadth circuit breaker | Low | High — fixes RSI-MR in crashes |
| 5 | B1 — Adaptive strategy selector | Medium | High — meta-layer over strategies |
| 6 | A5 — Risk-adjusted momentum score | Low | Medium — fixes CS threshold deadlock |
| 7 | A7 — Trailing stop | Medium | Medium — locks in CS gains |
| 8 | B3 — Corporate action filter | Medium | Medium — reduces event-driven noise |
| 9 | C2 — Result persistence | Low | Medium — enables proper comparison |
| 10 | A4 — Sector concentration limit | Medium | Medium — reduces CS blow-up risk |
| 11 | B6 — Parameter tuning advisor | Low | High — replaces manual analysis |
| 12 | C3 — Walk-forward validation | High | High — tests for overfitting |
