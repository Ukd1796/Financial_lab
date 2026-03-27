# QuantCanvas — Systematic Trading for People Who Don't Have Time to Trade

**Tagline:** *Your capital. Your rules. Institutional-grade stock filtering and regime-aware strategy selection — fully managed, fully explainable.*

---

## Who This Is For

You have ₹5–50 lakh sitting in a savings account or FDs. You've watched the market go up 60% since 2020 and wonder if you're leaving money on the table. You've looked at mutual funds — they're too passive. You've tried trading — it consumed too much time and you made emotional decisions. You know there has to be a smarter middle ground.

**You are right. There is.**

QuantCanvas is built for:

- **The busy professional** (doctor, engineer, consultant, business owner) who can check in once a week, not 8 hours a day
- **The capital-first, time-poor investor** who has ₹10–50 lakh to deploy systematically but no bandwidth to stare at charts
- **The curious learner** who wants to understand *why* a trade happens, not just follow signals blindly
- **The someone who tried intraday trading** and realized it's a job, not a strategy — and now wants something that works on weekly and monthly time horizons

**What you will not find here:** day trading tools, intraday charts, options screeners, tip services, or "hot picks." This platform is for investors who want to build and run a rules-based, tested, automated strategy — and then get out of the way.

---

## The Problem with Every Existing Tool

| Platform | What It Claims | What's Actually Missing |
|----------|---------------|------------------------|
| Zerodha Streak | Backtest your own strategy | Requires knowing what indicators to use and how to combine them. No regime awareness — your strategy runs the same in a bear market and a bull market. |
| Smallcase | Curated thematic baskets | You're buying someone else's fixed ideas. No personalization, no testing, no regime adjustment. |
| TradingView | Charts + Pine Script | Need to learn a programming language. No automated execution. No portfolio-level risk management. |
| Tijori / Screener | Great for stock research | Not for running automated strategies. No backtest, no signals, no automation. |
| QuantConnect | Serious quant platform | Full Python required. Designed for engineers, not investors. |

**The gap:** A platform that gives a non-coder the actual edge that systematic funds use — intelligent stock filtering, regime-aware position management, AI-driven strategy blending — without any of the complexity.

---

## What Makes QuantCanvas Different: The Financial Lab Engine

QuantCanvas is not built on generic indicators and a chart library. It is built on the **Financial Lab engine** — a system developed and live-tested in the Indian market since 2018, with 6+ years of backtest data across every major market regime (2020 COVID crash, 2020-21 recovery, 2022 rate-hike bear, 2023-24 bull, 2025-26 geopolitical bear).

Three things the engine does that no retail platform currently offers:

---

### 1. Intelligent Stock Filtering (Not a Screener — A Daily Selection Agent)

Most platforms ask you to pick your stocks and then run your strategy on them. QuantCanvas runs a **daily selection pipeline** that automatically identifies the 60-80 highest-quality candidates from the broader universe using a multi-layer agent system:

```
150 NSE stocks scanned daily
        ↓
DynamicUniverseAgent
  Scores every stock on: volume momentum, price momentum,
  volatility quality, trend age. Selects top 80.
        ↓
UnionUniverseFilter (5 specialist filters running in parallel)
  Breakout filter:     stocks forming new highs with volume confirmation
  Pullback filter:     stocks in uptrend pulling back to support
  Mean Reversion:      oversold stocks in otherwise healthy uptrends
  Trend filter:        clean SMA crossovers with confirmed direction
  Quiet Breakout:      stocks breaking out of low-volatility compression
        ↓
60-80 active symbols — the day's working universe
```

**What this means for you:** You never pick stocks. The engine scans 150 stocks every trading day, runs them through specialist filters, and surfaces only those that match the conditions your chosen strategy needs. Stocks that don't qualify don't appear. You only see — and trade — stocks that meet a rigorous multi-layer bar.

You control **which universe you start from** (Nifty 50, Nifty 100, or Broad 150). Everything else is managed.

---

### 2. Regime Context Awareness (The Market's State, Not Just Your Stock's State)

This is the most important feature most traders never think about — and why most retail strategies fail in bear markets.

Every strategy behaves differently depending on the state of the broader market. A breakout strategy that returns 40% in a bull market can lose 15% in a bear market running the exact same signals. The difference is not the strategy — it is whether the strategy is running in the right market environment.

QuantCanvas uses a **RegimeContextAgent** that reads the state of all 150 tracked stocks every day and classifies the market into one of 8 states:

| Regime | What it means | What the platform does |
|--------|--------------|----------------------|
| `BULL_CONFIRMED` | Strong uptrend, majority above 50d average | All strategies eligible, full signal generation |
| `BULL_EARLY` | Majority above 50d average, improving trend | Full signals, Breakout and TrendPullback favored |
| `BULL_WATCH` | Most stocks above 50d average but not accelerating | Standard signals, moderate position sizes |
| `SIDEWAYS_CHOPPY` | Mixed signals, no clear direction | Selective signals, tighter risk |
| `TRANSITION_UP` | Market was bearish but breadth is actively improving | Cautious re-entry begins — 2-3 weeks before traditional signals confirm |
| `BEAR_WATCH` | Moderate downtrend (45-60% of stocks falling) | No new buys, existing positions managed |
| `BEAR_TRANSITION` | Deep bear, but breadth showing early improvement | No new buys, early warning to user that recovery may be starting |
| `BEAR_CONFIRMED` | Deep bear, no improvement signal | Full capital protection, zero new entries |

**The `TRANSITION_UP` advantage:** Traditional tools wait until the market clearly recovers before re-entering. By that point, the first 15-25% of the recovery move is already gone. QuantCanvas detects improving breadth across all 150 stocks and begins cautious re-entry 2-3 weeks earlier — catching more of the recovery without taking on full bear-market risk.

**What you see:** A simple traffic light on your dashboard (Green / Yellow / Red) with a one-sentence explanation. The complex 150-stock breadth calculation happens invisibly in the background.

---

### 3. AI Strategy Selection — You Choose the Strategies, the AI Chooses the Mix

You pick which strategies you want in your portfolio. The platform's **AdaptiveStrategySelector** then decides how much capital to allocate to each one every week, based on which strategies are performing best in the current regime.

**The 5 available strategies:**

| Strategy | What it does | Best in | Avg hold period |
|----------|-------------|---------|-----------------|
| **Trend Follow** (SMA Crossover) | Buys when 20d average crosses above 50d average | Sustained bull markets | 3-8 weeks |
| **Breakout** | Buys on 10-day price highs with above-average volume | Recovery, early bull | 1-3 weeks |
| **Quiet Breakout** | Buys stocks breaking out of low-volatility compression | Sideways → bull transitions | 2-4 weeks |
| **Trend Pullback** | Buys 5% dips within confirmed uptrends | Strong trending markets | 1-3 weeks |
| **Mean Reversion** | Buys short-term oversold conditions in healthy uptrends | Recovery periods | 3-10 days |

**How the AI allocation works:**

In a `BULL_CONFIRMED` regime, the AI weights Breakout and TrendPullback higher — they generate signals in strong trending conditions. In `BEAR_WATCH`, it eliminates those strategies entirely and moves weight to defensive positions. In `TRANSITION_UP`, it begins cautiously tilting toward Breakout even before the regime fully confirms recovery.

You can:
- Enable or disable any strategy (toggle on/off)
- Set a floor weight for strategies you want always included (e.g., "always at least 20% Trend Follow")
- Let the AI decide everything within your constraints

The AI rebalances weights once per week. It does not chase daily noise.

---

## The Platform: What You Actually Do

### Step 1 — Configure Your Strategy (15 minutes, once)

**Universe:** Which stocks do you want the engine to scan?
- Nifty 50 — India's 50 largest (lowest risk, fewer opportunities)
- Nifty 100 — Top 100 (recommended default)
- Broad 150 — Adds midcaps (more opportunities, slightly higher volatility)

**Strategy selection:** Toggle which strategies you want active. The AI handles allocation between them. You cannot accidentally allocate 100% to one strategy — the platform enforces diversification minimums.

**Risk parameters — three sliders:**
- *Risk per trade:* What % of your total capital can you lose if a single stop-loss hits? (0.2% → 1.5%)
- *Maximum single position:* What's the most you'll ever put in one stock? (5% → 20%)
- *Weekly drawdown pause:* Automatically pause all new buys if your portfolio drops X% in a week (3% → 8%)

**One toggle: Weekly/Monthly mode**
- Weekly mode: strategy checks signals every trading day, typically 2-5 trades per week
- Monthly mode: strategy batches entries and reviews positions once per week, 5-15 trades per month

**That's it.** The stock filtering, regime detection, and strategy weight allocation are all platform-managed. You don't touch them unless you want to.

---

### Step 2 — Backtest It (10 seconds)

Click "Backtest." The engine runs your configuration through 6+ years of real NSE market data across every market regime. Results appear in ~10 seconds.

**What you see:**

```
My Strategy — Backtest 2019 → 2025

Total Return     Max Drawdown     Sharpe Ratio     # Trades
  +94.3%           -18.7%            1.14            284

vs Nifty 50:   +67.2% return   -38.1% max drawdown

How you did in each market phase:
  Bull 2019-2020         +31.4%    -8.2%    ✅ Beat index
  COVID Crash 2020        -4.1%    -9.6%    ✅ Protected capital (Nifty: -38%)
  Recovery 2020-21       +48.2%    -6.1%    ✅ Captured most of recovery
  Bear 2022 (rate hikes)  +8.3%    -7.4%    ✅ Positive while Nifty -17%
  Bull 2023-24           +22.7%   -11.3%    ✅ Participated in bull run
```

**AI Explanation (always present, always specific to your numbers):**

> *"Your strategy significantly outperformed the Nifty 50 on risk-adjusted terms. The most important number here is not total return — it is max drawdown. The Nifty 50 fell 38% during the 2020 crash. Your strategy fell only 9.6%. This happened because the RegimeContextAgent detected a `BEAR_CONFIRMED` state and stopped all new entries on February 28, 2020 — two weeks before the market bottomed. You didn't catch the fall because you weren't buying into it.*
>
> *Your weakest period was the 2019 pre-COVID slow bull, where you lagged by about 8%. This is normal for systematic strategies — they need clear directional trends, and 2019 was choppy. If you toggle on the Mean Reversion strategy, it performs well in choppy markets and would have partially offset this.*
>
> *A Sharpe ratio of 1.14 means for every 1 unit of risk you took, you earned 1.14 units of return. The index earned 0.82 per unit of risk. You were a more efficient capital allocator."*

You can adjust parameters and re-run immediately. Change the risk per trade from 0.5% to 1%, see how it affects drawdown. Toggle off Mean Reversion, see what you gain and lose. The feedback loop is seconds, not hours.

---

### Step 3 — Paper Trade (30 days)

When you're satisfied with the backtest, activate paper trading. The platform:

- Runs the full signal pipeline every trading day at 3:35 PM IST automatically
- Sends you a nightly email (and optional push notification) with what happened
- Tracks a simulated portfolio in real-time showing positions, unrealised P&L, and regime status
- Generates a weekly health report comparing your paper results to backtest expectations

**You check in once a week.** Or every evening if you're curious. The system runs whether you log in or not.

**Paper trading is mandatory for 30 trading days before live is unlocked.** Not advisory — enforced. This is by design. 30 days covers at least one full market week of varied conditions and forces you to observe how the strategy behaves in real-time before real money is on the line.

**Your weekly check-in (5 minutes):**

```
Week 3 of 4 — Paper Trading Report

Portfolio:    ₹10,42,310  (+4.2% vs start)
Nifty 50:     -1.1% same period
Regime:       BEAR_TRANSITION → watch for TRANSITION_UP

Open positions: 4
  RELIANCE    +3.1%  [Trend Follow]   — hold
  TITAN       +5.3%  [Breakout]       — hold
  HDFCBANK    +1.1%  [Trend Follow]   — hold
  INFY        -1.0%  [Breakout]       — within normal range, hold

This week: 0 new buys (market in cautious zone), 1 exit (BAJFINANCE stop-loss -3.8%)

Regime note: Breadth is improving for 3 consecutive days. If this continues
2 more days, the regime shifts to TRANSITION_UP and cautious re-entry begins.
```

---

### Step 4 — Go Live (one hour of setup, then automated)

After 30 paper trading days, the "Go Live" button activates.

**Broker connection:** Provide your Zerodha / Upstox API key. The platform connects to your existing broker account. Your capital stays with your broker — we never hold funds.

**Capital allocation:** Tell the platform how much of your broker account to trade with. We recommend starting at 25-50% of your intended final allocation for the first month.

**What changes:** Signals that were paper-tracked now become real orders placed through your broker at market open (9:15 AM IST next day). Everything else — the dashboard, the email reports, the weekly health check — stays identical to paper trading.

**What you still don't have to do:** check charts, pick stocks, time entries, decide when to exit. The platform handles all of it. Your job is to review the weekly report, adjust risk parameters if something feels off, and trust the system you spent 30 days paper-testing.

---

## The Application: Pages and Flow

### Dashboard (Home)

The first thing you see every time you log in. Designed to answer one question: *"Is everything running as it should?"*

```
┌─────────────────────────────────────────────────────────────────┐
│  My Strategy        ●  Running   Paper day 18/30               │
│                                                                  │
│  ₹10,42,310    +4.2%     -9.6% max dd     1.14 Sharpe          │
│  Paper value   vs start  this run          current              │
│                                                                  │
│  Market today: BEAR_TRANSITION  ⚠️ Cautious — no new buys      │
│  Breadth improving for 3 days. Watching for TRANSITION_UP.      │
│                                                                  │
│  Open positions: 4   │  Signals today: 0 buy, 1 sell           │
│  Last signal: BAJFINANCE SELL (stop-loss) — ₹6,840  -3.8%      │
│                                                                  │
│  [View Positions]  [View Signals]  [Strategy Settings]          │
└─────────────────────────────────────────────────────────────────┘
```

The regime indicator is the most prominent element. Users learn to read it before anything else.

---

### Strategy Builder

Where you configure your pipeline. Not a blank canvas — a guided configuration panel with the platform's engine pre-wired:

```
┌──────────────────────────────────────────────────────────────────┐
│  Strategy Builder — My Strategy                                   │
├─────────────────────────────────────────────────────────────────-┤
│                                                                   │
│  STOCK UNIVERSE          ← platform scans and filters this       │
│  ○ Nifty 50  ● Nifty 100  ○ Broad 150                           │
│  Active stocks today: 74  (updated daily at 3:35 PM)            │
│  [How does the stock selection work? →]                          │
│                                                                   │
│  MARKET REGIME           ← platform manages this automatically   │
│  ● Breadth-based (recommended)  ○ Simple up/down                │
│  Current: BEAR_TRANSITION                                         │
│  Pause all buys when: [35%▼] of stocks in downtrend             │
│                                                                   │
│  STRATEGIES              ← you pick, AI allocates               │
│  [x] Trend Follow   floor: [10%]                                 │
│  [x] Breakout       floor: [0%]                                  │
│  [x] Quiet Breakout floor: [0%]                                  │
│  [x] Trend Pullback floor: [0%]                                  │
│  [ ] Mean Reversion  (disabled)                                  │
│  Current AI allocation: TF=45% BRK=30% QBK=15% TPB=10%         │
│                                                                   │
│  RISK PARAMETERS         ← you control these                     │
│  Risk per trade:    ●————————  0.5%  (₹500 on ₹1L)             │
│  Max position:      ————●————  10%                               │
│  Weekly pause at:   ————●————  -5%                               │
│                                                                   │
│  MODE:  ○ Weekly (2-5 trades/wk)  ● Monthly (5-15 trades/mo)   │
│                                                                   │
│  [ Run Backtest ]  [ Save Changes ]                              │
└──────────────────────────────────────────────────────────────────┘
```

Every label has a `[?]` tooltip and an AI explain button. Nothing is assumed.

---

### Backtest Results

Full results with period breakdown, trade log, and AI narrative. Three interaction modes:

- **Summary** — headline numbers + AI narrative (default, readable in 2 minutes)
- **Period Detail** — regime-by-regime breakdown, what each strategy contributed
- **Trade Log** — every trade: date, symbol, strategy, entry/exit, P&L, reason

Sharpe, max drawdown, and win rate are always shown alongside their plain-English meaning. Users cannot see the Sharpe without seeing "what this means" in the same view.

---

### Live Positions

Table of all open positions with:
- Entry date, entry price, current price, unrealised P&L
- Which strategy owns this position
- Stop-loss level (in price and % terms)
- Days held
- "Why was this entered?" — one sentence generated at entry time, always visible

```
  TITAN        Entered Apr 3  @ ₹3,210   Now ₹3,380   +5.3%  [Breakout]
               Stop-loss: ₹3,089  (-3.8%)   Held 4 days
               "Entered on 10-day high with 2.3× volume in BULL_WATCH regime"
```

---

### Signal History

Every signal ever generated — including ones that were blocked. Users can see:
- Signals that fired and became trades
- Signals that were blocked by the circuit breaker and why
- Signals that were blocked by risk rules (position size limit, etc.)

This is important for understanding the system's behavior during periods when it generates no trades. "Why wasn't I in the market in March 2026?" → "Circuit breaker active: 62% of tracked stocks in downtrend (threshold: 35%)"

---

### Learn

Not a course. Contextual, on-demand explanations.

Every term on the platform is clickable. Every explanation uses your actual data, not generic examples. The AI tutor is available in a chat panel on every page.

**Sample AI tutor interactions:**

User: *"Why did the strategy not buy anything this week?"*
> *"The RegimeContextAgent classified the market as BEAR_TRANSITION this week — 58% of the 100 stocks in your universe were below their 50-day average, which exceeds your 35% threshold. The circuit breaker activated on Monday and held through Friday. The system is protecting your capital. The breadth signal has been improving for 3 days, which means if another 2 days of improvement follow, the regime will shift to TRANSITION_UP and cautious re-entry will begin."*

User: *"What is the Sharpe ratio?"*
> *"Think of it like return per unit of stress. Two portfolios both returned 20% last year. Portfolio A had wild swings — it was up 35% in June and down 18% in October. Portfolio B was steady — gradually up all year. Both returned the same, but Portfolio B was easier to hold through, and less likely to have caused you to panic-sell at the bottom. The Sharpe ratio measures this efficiency: return divided by volatility. Your current Sharpe of 1.14 means you earned 1.14 units of return for every 1 unit of volatility risk you took. The Nifty 50 earns about 0.8 over the same period. You are a more efficient capital allocator."*

User: *"Should I add Mean Reversion to my strategy?"*
> *"Based on your current configuration (Nifty 100 universe, 0.5% risk per trade, Trend Follow + Breakout active), Mean Reversion would have added approximately +4.2% total return over the 2019-2025 backtest period, primarily by filling in the choppy sideways periods of 2019 and mid-2023 where your other strategies generate few signals. The tradeoff: Mean Reversion adds about 2.3 trades per week on average and increases max drawdown by 1.8% (from 18.7% to 20.5%). If you have a ₹10 lakh portfolio, that's roughly ₹18,000 more drawdown risk in exchange for approximately ₹42,000 in additional expected return over 6 years. Would you like to run a backtest with it enabled to see the exact numbers?"*

---

### Health Report (Weekly, via Email)

A single email every weekend that covers:
- Portfolio value and change since start
- Market regime this week and direction it's heading
- Trades taken: entry/exit, strategy, P&L
- What the circuit breaker blocked and why
- Next week outlook (regime expectation, events to watch)
- One suggested action (e.g., "Consider enabling Mean Reversion — the regime is moving toward sideways choppy conditions where it performs best")

Designed to be fully informative in under 3 minutes of reading time. Users who check only the weekly email are fully informed.

---

## What the Platform Manages vs What You Control

This distinction is core to the product's philosophy.

| Layer | Managed by | User interaction |
|-------|-----------|-----------------|
| Stock scanning (150 → 60-80) | Platform (DynamicUniverseAgent + 5 specialist filters) | Choose universe size (50/100/150) |
| Market regime classification | Platform (RegimeContextAgent, 150-stock breadth) | Set the circuit breaker threshold % |
| Strategy weight allocation | Platform AI (AdaptiveStrategySelector, weekly) | Enable/disable strategies, set floor weights |
| Position sizing | Platform (ATR-based, risk-per-trade formula) | Set risk per trade %, max position % |
| Entry/exit execution | Platform (daily pipeline, broker API) | Weekly vs monthly mode |
| Stop-loss management | Platform (ATR multiplier) | Not configurable — this protects you |
| Circuit breaker | Platform (breadth threshold) | Set the trigger threshold (25-60%) |

**The philosophy:** Everything that requires real-time market data, quantitative calculation, or consistent discipline is managed by the platform. Everything that reflects your personal risk tolerance and financial goals is yours to set.

---

## How New Strategies and Agents Get Added

The platform is agent-based. When the research team adds a new capability, it integrates as a new block option in the strategy builder — not a platform-wide change that affects everyone.

**Upcoming additions (roadmap):**
- **Macro Calendar Agent** — automatically flags RBI/Fed decision days, Q4 earnings season; suggests activating the buy-pause toggle in advance
- **Stock Insight Agent** — adds an AI-assisted qualitative filter on top of the quantitative pipeline; ranks the 60-80 candidates by fit with current regime and strategy context
- **NSE F&O Ban Filter** — removes stocks on the NSE derivatives ban list from the active universe daily (high open interest crowding indicator)
- **News Context Layer** — enriches the regime snapshot with macro news headlines; LLM adjusts regime interpretation when a major catalyst (rate cut, budget announcement) occurred

Each of these will appear as a toggle in the Strategy Builder when ready. Users can opt in or out. The existing pipeline continues to run unchanged for those who don't want the additional layer.

---

## Phase-Wise Build Plan

### Phase 1 — Core Web App (Months 1-3)

**Goal:** A user can configure a strategy, run a backtest, and understand the results. No automation yet.

- Strategy Builder page (5 blocks, guided config, no drag-and-drop yet)
- Backtest engine (wrap the existing Financial Lab Python engine via FastAPI)
- Results page with AI narrative generation (Claude API)
- User accounts, strategy save/load
- AI tutor (term explanations, contextual Q&A)
- Historical data: 150-stock NSE universe, 2018-2025, preloaded

**Technical:** Next.js frontend, FastAPI backend, Supabase database (already in use), Railway workers, Claude API for explanations.

**Monetization gate:** Free tier (3 backtests/month, 2019-2023 data). Paid unlocks full history and unlimited backtests.

---

### Phase 2 — Paper Trading (Months 4-6)

**Goal:** Strategies run automatically every trading day. Users observe live paper results.

- Paper trading engine (reuse `run_signals.py` + `run_orders.py` pipeline, per-user isolation)
- Daily dashboard with live position updates
- Nightly AI briefing email (auto-generated after each session)
- Weekly health report email
- 30-day paper trade gate before live unlock
- Push notifications for signals

---

### Phase 3 — Live Trading (Months 7-9)

**Goal:** One-click live trading through existing broker account.

- Zerodha Kite adapter (OAuth2, order placement, position sync)
- Upstox adapter
- Capital allocation UI
- Live vs paper portfolio view
- Broker order log with signal price vs fill price (slippage tracking)
- Daily loss limit enforcement (platform-managed, not optional)

---

### Phase 4 — Intelligence Expansion (Months 10-12)

**Goal:** Smarter agents, richer context, social learning.

- Macro Calendar Agent (RBI/Fed/earnings auto-flagging)
- Stock Insight Agent (LLM-assisted final candidate ranking)
- News Context Layer (regime snapshot enriched with macro headlines)
- Strategy performance leaderboard (anonymized, opt-in)
- Template marketplace: pre-built strategies for specific market philosophies

---

### Phase 5 — Advanced Builder (Month 12+)

**Goal:** Power users who want custom logic without full Python.

- React Flow-based drag-and-drop canvas (visual data pipeline)
- Custom indicator parameters (change RSI period, SMA lookback, volume thresholds)
- AND/OR logic gates between signal conditions
- Export to Python (for users who want to continue in code)
- Live backtest preview as blocks are connected

---

## Pricing

| Tier | Price | Who it's for |
|------|-------|-------------|
| **Free** | ₹0 | Try the backtest with limited data (2021-2023). 3 runs/month. No automation. |
| **Builder** | ₹499/mo | Unlimited backtests, full 2018-2025 data, AI explanations. No paper trading. |
| **Trader** | ₹999/mo | Everything in Builder + paper trading (1 active strategy), weekly health reports |
| **Pro** | ₹1,999/mo | Everything in Trader + live trading, 3 simultaneous strategies, broker integration, priority AI |

Annual billing: 2 months free. No USD pricing. Indian billing (UPI/credit card via Razorpay).

Capital minimum for live trading: ₹1 lakh (enforced at onboarding).

---

## The Explanation Layer — Understanding Everything the Platform Does

Every number, every decision, every blocked signal has an explanation available. This is not optional, not hidden behind a help centre link, and not generic. Every explanation is generated using your actual strategy, your actual data, and your actual results.

The platform operates on one principle: **you should never see a number you don't understand.**

---

### Three Levels of Explanation Available at All Times

**Level 1 — Inline context (always visible)**

Every metric on every screen has a one-line plain-English meaning shown directly beneath it. No clicking required.

```
Sharpe Ratio: 1.14
Return earned per unit of risk. Anything above 1.0 is considered strong.

Max Drawdown: -18.7%
The worst peak-to-trough drop this strategy experienced. Your lowest point
before recovery was 18.7% below your highest point.

Breadth CB: ACTIVE (62% downtrend)
More than 35% of your tracked stocks are falling. New buys are paused.
```

**Level 2 — Click to expand (one click, still in context)**

Click any number, term, or event → a panel slides in with a 3-paragraph explanation using your specific data.

```
[Clicking on "Sharpe Ratio: 1.14"]

What it is:
The Sharpe ratio measures how much return you earned relative to the
risk (volatility) you took. A Sharpe of 1.14 means for every 1 unit
of volatility you absorbed, you earned 1.14 units of return.

How yours compares:
The Nifty 50 index earns approximately 0.82 Sharpe over the same period.
Your strategy of 1.14 is meaningfully better — you generated more return
per rupee of risk taken. Anything above 1.0 is considered good by
institutional fund standards.

What would change it:
Reducing your risk per trade from 0.5% to 0.3% would lower your total
return but also reduce volatility — your Sharpe might stay similar or
improve slightly. Increasing it to 1% would raise return but also raise
drawdown, likely lowering Sharpe. Run a backtest with each to compare.
```

**Level 3 — AI tutor (full conversation, any page)**

A persistent chat panel available on every page. Ask anything, in plain language. The tutor has context of your specific strategy, your backtest results, and the current market regime.

Sample conversations:

> *"Why did my strategy stop generating signals in March?"*
> → Full explanation of which regime state activated the circuit breaker, on which date, using what breadth reading, and what needs to change before signals resume.

> *"Is this drawdown normal or something I should be worried about?"*
> → Compares current drawdown to the historical max drawdown for similar regime periods in the backtest. Tells you whether you're within expected range or outside it.

> *"My friend is running a different strategy and outperforming me. Should I switch?"*
> → Explains survivorship bias, regime dependency, and why outperformance in one period does not predict the next. Compares your strategy's profile (where it wins, where it loses) to help you decide.

> *"Explain the 2020 COVID crash section of my backtest like I'm 15 years old."*
> → Full narrative of what happened, what the strategy did, what the circuit breaker blocked, and how the portfolio behaved — in completely plain language.

---

### What Gets Explained, and When

| Event | When explanation appears | What it covers |
|-------|------------------------|----------------|
| Strategy configured | After each setting is changed | What this setting does, what extreme values mean, what the backtest says about the current value |
| Backtest completed | Full AI narrative auto-generated | What happened in each regime period, what worked, what to watch, what would improve it |
| New signal generated | In the nightly email and signal log | Which strategy fired, what condition was met, what the stock's indicators looked like at entry |
| Signal blocked by circuit breaker | In the nightly email and signal log | Exact breadth reading that day, how far from threshold, what needs to change for signals to resume |
| Signal blocked by risk rules | In the signal log | Which rule was violated (position limit, daily loss limit, etc.) and what the exact numbers were |
| Position exits (stop-loss) | In the nightly email | Stop-loss price, what triggered it, whether it was within expected ATR range, portfolio impact |
| Regime changes | Push notification + dashboard | What changed in breadth, what the new regime means for signal generation, historical analogs |
| Weekly health report | Email every weekend | Full narrative of the week: regime, signals, positions, what the system is watching for next week |

---

### The Learning Path (Built Into Normal Usage)

Users do not take a course before using QuantCanvas. Learning happens through use, in context, over time.

**Week 1 (Backtest phase):**
User runs their first backtest. The AI narrative explains what the Sharpe ratio means using their exact number. They click on "max drawdown" and learn what it means by seeing their own worst period. They ask the tutor why their strategy underperformed in 2019. By the end of this, they understand three metrics they didn't before — without reading a single article.

**Week 2-4 (Paper trading):**
User receives nightly emails explaining what happened today. They start reading about circuit breakers because they see one activate. They ask the tutor "why isn't the regime improving faster?" and learn how the 50-day moving average works — not as an abstract concept but as the specific number blocking their signals right now.

**Month 2 (Pattern recognition):**
User notices their strategy generates more signals after certain regime shifts. They ask the tutor about it. The tutor confirms the pattern (TRANSITION_UP is the regime just before signal generation resumes) and explains the breadth math behind it. User now understands regime detection at a conceptual level without ever reading the source code.

**Month 3+ (Advanced questions):**
User starts asking sharper questions: "Why did Trend Follow get only 10% allocation this week when the regime is BULL_WATCH?" The tutor explains the specific LLM reasoning from the AdaptiveStrategySelector that week. User can now agree or disagree with the AI's reasoning — which is the highest form of system literacy.

---

## Advanced Controls — For Users Who Want to Go Deeper

The platform has three tiers of control. Every user starts at Tier 1. Moving to Tier 2 or 3 requires reading a short explanation of what changes and what risks are added.

---

### Tier 1 — Standard (Default for All Users)

The five parameters described in the main flow:
- Universe size
- Which strategies to enable
- Risk per trade %
- Max position size %
- Weekly drawdown pause threshold

Everything else is platform-managed. Recommended for new users and anyone who wants to spend less than 15 minutes per week on this.

---

### Tier 2 — Strategy Parameters (Available After First Successful Backtest)

For users who want to tune how each strategy behaves, not just which strategies to use.

Unlocked after completing one full backtest. Shown behind a "Show advanced settings" toggle on the Strategy Builder page.

**Breakout strategy parameters:**
```
Breakout lookback period: [10 days ▼]   (range: 5-20 days)
  "How many days back does the system look to define a new high?"
  Shorter = more signals, noisier. Longer = fewer signals, stronger breakouts.

Volume confirmation threshold: [1.5× ▼]  (range: 1.0-3.0×)
  "How much above average daily volume is required to confirm a breakout?"
  Higher = fewer false breakouts but misses some real ones.

Minimum ATR-to-price ratio: [1.5% ▼]   (range: 0.5-3.0%)
  "The minimum volatility the stock must have for this strategy to fire."
  Lower = trades more stocks including very calm ones.
```

**Trend Follow parameters:**
```
Fast SMA period: [20 days ▼]   (range: 10-30)
Slow SMA period: [50 days ▼]   (range: 30-100)
  "The crossover that triggers an entry."
  Shorter fast/slow = earlier entries, more whipsaws in choppy markets.
  Longer fast/slow = fewer trades, more reliable signals, higher lag.

Minimum cross age: [0 days ▼]   (range: 0-10)
  "How many days the crossover must have been in place before entry."
  Higher = avoids entering immediately after a cross (reduces false starts).
```

**Trend Pullback parameters:**
```
Pullback threshold: [5% ▼]   (range: 2-12%)
  "How far the stock must have pulled back from its recent high."
  Smaller = enters earlier in the pullback (more risk, better price).
  Larger = enters only on deeper pullbacks (fewer signals, better entry quality).
```

**Mean Reversion parameters:**
```
RSI oversold threshold: [30 ▼]   (range: 5-40)
  "RSI below this level triggers a potential entry."
  Lower = only buys extremely oversold stocks (very few signals).
  Higher = buys moderately oversold stocks (more signals, lower conviction).

Maximum hold days: [7 days ▼]   (range: 3-20)
  "How long to hold a mean reversion trade before forcing exit."
  Shorter = faster cycle, more trades per year.
```

**Regime circuit breaker (advanced):**
```
Downtrend pause threshold: [35% ▼]   (range: 25-60%)
  Default: 35%. This is the breadth level at which ALL new buys stop.

TRANSITION_UP relaxation: [ON ▼]
  When the regime is improving (TRANSITION_UP), the effective threshold
  is capped at 30% rather than your raw breadth reading. This allows
  cautious re-entry 2-3 weeks before traditional signals confirm recovery.
  Turning this OFF makes your strategy more conservative during transitions.
```

Every parameter change immediately shows its effect on the backtest results panel on the right. No separate backtest run needed for Tier 2 changes — the sensitivity preview updates in real-time.

---

### Tier 3 — Custom Universe and Signal Logic (Available After 30 Days of Paper Trading)

For users who have spent at least 30 days paper trading and want to build something beyond the preset options.

**Custom universe:**
Add any NSE-listed stock to your universe beyond the Nifty 150 presets. Stocks outside the 150 default list are fetched on-demand and included in your personal scanning pipeline only.

```
Search and add stocks:  [ BAJAJCON ▼ ]  [ + Add to universe ]

Your custom additions: BAJAJCON, MTAR, KALYANKJIL
Note: Custom stocks are scanned daily but not included in the
broad regime calculation (RegimeContextAgent uses the 150-stock
base universe). This is by design — the regime signal must be
consistent across all users.
```

**Strategy combination logic:**
Add custom entry conditions using AND/OR gates between existing signal types. No coding — visual rule builder.

```
Entry fires when:
  [ Breakout signal ] AND [ Regime is BULL_WATCH or better ]
  OR
  [ TrendPullback signal ] AND [ Stock volume > 2× average ]

  [+ Add condition]   [Preview: estimated 3.2 signals/week]
```

**Custom exit rules:**
Beyond the ATR stop-loss, add time-based or target-based exit conditions:

```
Exit when:  [ Held for 15 days ]   (time stop)
        OR: [ Position up 20% ]    (profit target)
        OR: [ ATR stop triggered ] (existing default)
```

**Position sizing override (per-strategy):**
Give specific strategies a different risk-per-trade than your default setting:

```
Global risk per trade: 0.5%

Override per strategy:
  Breakout:       0.8%   (higher conviction, willing to size up)
  Mean Reversion: 0.3%   (lower conviction, size down)
  Trend Follow:   0.5%   (use global default)
```

---

### Tier 4 — Python Export (Available on Pro Plan)

For users who want full control and are comfortable writing some code.

The platform generates the Python configuration file for your strategy — you can take it, modify it, and run it locally against the Financial Lab engine (open-sourced separately). Any changes you make locally can be imported back into the platform as a custom strategy.

```python
# Generated by QuantCanvas — My Strategy
# Export date: 2026-04-05

STRATEGY_CONFIG = {
    "universe": "nifty_100",
    "strategies": {
        "TrendFollow": {"enabled": True, "fast_sma": 20, "slow_sma": 50},
        "Breakout":    {"enabled": True, "lookback": 10, "vol_threshold": 1.5},
        "TrendPB":     {"enabled": True, "pullback_pct": 0.05},
    },
    "risk": {
        "risk_per_trade_pct": 0.005,
        "max_position_pct":   0.10,
        "breadth_cb_threshold": 0.35,
        "transition_up_relaxation": True,
    },
    "regime": {
        "agent": "RegimeContextAgent",
        "broad_universe_size": 150,
    },
}
```

Full documentation for the Python API is available in the developer portal.

---

### Guardrails That Never Move (Regardless of Tier)

Some limits apply at all tiers and cannot be overridden. These exist to protect users from configuration mistakes that can cause significant financial harm:

| Guardrail | Limit | Reason |
|-----------|-------|--------|
| Max position size | 20% of capital | A single stock above 20% creates unacceptable concentration risk |
| Max risk per trade | 2% of capital | Above 2%, a string of 10 losing trades can halve a portfolio |
| Circuit breaker | Must be set (minimum 50% threshold) | Cannot run with no breadth protection at all |
| Stop-loss | Required on every position | Platform will not enter a position without a defined exit |
| Live trading minimum | 30 days of paper trading on the same strategy | No exceptions |

These are not restrictions — they are the product's structural safety layer. Every institutional trading desk has analogous hard limits. Yours are just visible and explained.

---

## Safety and Transparency Commitments

**We never hold your money.** Capital stays in your Zerodha/Upstox account. We generate signals; your broker executes them.

**30-day paper trading gate.** You cannot go live on a new strategy without 30 trading days of paper results. No exceptions, no overrides, no "I've already tested this elsewhere."

**Risk floors are mandatory.** The platform prevents position sizes above 20% of capital and requires a circuit breaker threshold. You can make the rules less conservative, but you cannot remove them entirely.

**Every decision is logged and explained.** Every signal — including blocked ones — is stored with its reasoning. You can always see exactly what the system did and why.

**Your strategies are yours.** We do not use your strategy configurations for our own trading or to build competing products. Strategies are private by default; sharing is always opt-in.

**We tell you when the system is uncertain.** When the market is in `BEAR_TRANSITION` or `SIDEWAYS_CHOPPY`, the dashboard says so explicitly. The system does not project false confidence in ambiguous conditions.

---

## The North Star

The best trading strategy you will ever run is one you understand well enough to hold through two consecutive losing weeks.

Most retail investors abandon good systematic strategies at exactly the wrong moment — during the first drawdown — because they don't understand what the strategy is doing or why. They see red numbers and switch to something that was recently green. This is the single most expensive mistake in retail investing.

QuantCanvas fixes this by making the strategy legible at every point in its life: the moment you configure it, the moment you backtest it, the moment you paper trade it, and the moment it stops generating signals because the market is in a bear phase and the circuit breaker is protecting your capital.

When you understand the system, you trust it. When you trust it, you hold through the drawdown. When you hold through the drawdown, you capture the recovery.

*That is the edge.*

---

*Powered by the Financial Lab engine — 6+ years of NSE data, 5 validated strategies, RegimeContextAgent breadth detection, AdaptiveStrategySelector AI allocation, live paper trading since March 2026.*
