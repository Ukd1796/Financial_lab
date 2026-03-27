# QuantCanvas — Frontend Build Prompt

Use this prompt with any AI coding assistant (Claude Code, Cursor, v0, Lovable) to scaffold the full frontend application. Copy the relevant section for the phase you are building.

---

## Master Context (include in every prompt)

```
You are building QuantCanvas — a systematic trading platform for busy Indian retail investors
who want to run rule-based, AI-assisted stock strategies on NSE/BSE without writing code or
reading charts. The backend is a Python FastAPI service wrapping an existing backtesting
engine. The frontend is the primary user surface.

Design philosophy:
- Clean, minimal, data-forward. Think Linear or Vercel dashboard aesthetic — dark or light
  mode, neutral grays, strong typographic hierarchy, very little decoration.
- Every number on screen has a one-line explanation beneath it. Users are not finance experts.
- The AI tutor (chat panel) is present on every page. It has context of the user's strategy
  and results. It answers plain-English questions using their specific data.
- Mobile-responsive is a stretch goal. Desktop-first (1280px+ primary breakpoint).
- No chart libraries for stock price charts — the platform deliberately avoids candle charts.
  Use simple line charts (Recharts or Tremor) for portfolio value over time only.

Tech stack:
- Framework: Next.js 14 (App Router)
- Styling: Tailwind CSS + shadcn/ui component library
- Drag-and-drop canvas: React Flow (reactflow.dev) — used for the Strategy Builder page
- Charts: Recharts (simple line/bar only — no candlesticks)
- Icons: Lucide React
- Animations: Framer Motion (subtle, functional — not decorative)
- State: Zustand for global strategy config state
- API calls: React Query (TanStack Query)
- Auth: Clerk (simplest path) or Supabase Auth

Color palette:
- Background: #0A0A0A (dark) or #FAFAFA (light) — build both, dark is primary
- Surface: #111111 / #F5F5F5
- Border: #1F1F1F / #E5E5E5
- Primary accent: #6366F1 (indigo) — used sparingly for CTAs and active states
- Success: #22C55E
- Warning: #F59E0B
- Danger: #EF4444
- Text primary: #FAFAFA / #0A0A0A
- Text muted: #71717A

Typography:
- Font: Geist (or Inter as fallback)
- Heading scale: text-2xl font-semibold for page titles, text-base font-medium for section
  headers, text-sm for labels
- Every metric: text-2xl font-bold for the number, text-xs text-muted-foreground for the
  one-line explanation directly below it
```

---

## PHASE 1 PROMPT — Backtesting Web App

```
Build Phase 1 of QuantCanvas. This phase covers four pages: Landing, Onboarding Wizard,
Strategy Builder (drag-and-drop canvas), and Backtest Results. There is no live data in
Phase 1 — everything is historical backtesting. Paper and live trading pages exist only as
"Coming Soon" shells in the navigation.

Use the master context above for design system and tech stack.

---

PAGE 1: Landing Page  (/home or /)

Layout: Full-width, no sidebar. Dark background.

Hero section:
  Headline (large, centered):
    "Build a trading strategy.
     Test it on 6 years of real data.
     Run it automatically."
  Subheadline (muted, max-w-xl centered):
    "No charts. No code. No guesswork. QuantCanvas gives busy investors
     the same systematic edge as institutional quant funds — in 15 minutes."
  CTA buttons (centered, side by side):
    Primary: "Build My Strategy →" (routes to /onboarding)
    Secondary: "See a sample backtest" (opens a demo modal with pre-filled results)

Social proof strip below hero (single row, horizontal scroll on mobile):
  "Tested on 6+ years of NSE data"
  "5 validated strategies"
  "150 stocks scanned daily"
  "Live since March 2026"
  Each item: small icon + text, separated by a divider dot

Three-column feature section (below fold):
  Column 1 — "Intelligent Stock Filtering"
    Icon: Filter (Lucide)
    Heading: "150 stocks scanned. You see only the 60-80 that qualify."
    Body: 2 sentences explaining the DynamicUniverseAgent pipeline without naming it.
    Small diagram: "150 stocks → [Quality Filter] → 80 candidates → [5 Specialist Filters] → 60 active"
    (Build this as a static SVG or CSS flex diagram — no external library)

  Column 2 — "Regime-Aware Protection"
    Icon: Shield (Lucide)
    Heading: "The system knows when to stop."
    Body: 2 sentences. Mention that new buys auto-pause when the market is in a downtrend.
    Pill badges showing the 8 regime states: BULL_CONFIRMED (green), TRANSITION_UP (amber),
    BEAR_CONFIRMED (red), etc. Non-interactive, just illustrative.

  Column 3 — "AI Picks the Strategy Mix"
    Icon: Sparkles (Lucide)
    Heading: "You pick the strategies. AI handles the allocation."
    Body: 2 sentences on AdaptiveStrategySelector.
    Animated weight bar (CSS only): 5 strategies, bar widths shifting slowly to simulate
    weekly rebalancing.

How it works section (numbered steps, left-to-right flow):
  1. Configure → 2. Backtest → 3. Paper Trade → 4. Go Live
  Each step: number, title, 1-sentence description, small illustration
  Steps 3 and 4 are visually grayed with a "Phase 2" / "Phase 3" badge

Footer:
  Logo, tagline, links (Privacy, Terms, Contact)
  "Built on 6+ years of real NSE data. Not financial advice."

---

PAGE 2: Onboarding Wizard  (/onboarding)

A 4-step wizard. Full-page centered card (max-w-2xl). Step indicator at top (dots or
numbered pills). "Back" and "Next →" at bottom. Wizard state stored in Zustand.

Step 1 of 4 — "Which stocks should I track?"
  Title: "Pick your universe"
  Subtitle (muted): "The system scans these stocks every trading day and selects the
  best 60-80 automatically."

  Three radio cards (full-width, stacked):
    ○ Nifty 50
      "India's 50 largest companies. Lower risk, fewer opportunities."
      Tag: "Conservative"

    ● Nifty 100  [default selected]
      "Top 100 stocks — a good balance of quality and opportunity."
      Tag: "Recommended"

    ○ Broad 150
      "Adds midcaps. More opportunities, slightly more volatility."
      Tag: "More active"

  AI tutor bubble (bottom of card, always visible in wizard):
    Icon: small bot icon
    Text: "A universe is just the list of stocks the system watches. You don't pick
    individual stocks — the platform filters this list every day and finds the best
    candidates automatically. Starting with Nifty 100 is the right call for most people."

Step 2 of 4 — "How should I enter trades?"
  Title: "Pick your strategies"
  Subtitle: "Select one or more. The AI will decide how much to allocate to each one
  every week based on market conditions."

  Five toggle cards (grid 2-col, last one full width):
    Each card contains:
      - Strategy name (bold)
      - One-sentence plain-English description
      - "Best in:" tag (e.g., "Bull markets")
      - Average hold period
      - Toggle switch (right side)

    [x] Trend Follow
        "Buys when the 20-day average crosses above the 50-day average."
        Best in: Sustained bull markets   Hold: 3-8 weeks

    [x] Breakout
        "Buys stocks making new 10-day highs with above-average volume."
        Best in: Recovery, early bull    Hold: 1-3 weeks

    [x] Quiet Breakout
        "Buys stocks breaking out after a period of low volatility."
        Best in: Sideways → bull transitions   Hold: 2-4 weeks

    [x] Trend Pullback
        "Buys 5% dips within confirmed uptrends."
        Best in: Strong trending markets   Hold: 1-3 weeks

    [ ] Mean Reversion
        "Buys short-term oversold stocks that are still in healthy uptrends."
        Best in: Recovery periods   Hold: 3-10 days

  AI tutor: "You've selected 4 strategies. In a bull market, this combination would have
  generated 2-4 signals per week on average. In a bear market, the circuit breaker would
  have paused all of them. The AI rebalances how much goes to each strategy every week."

Step 3 of 4 — "How much can I afford to lose per trade?"
  Title: "Set your risk limits"
  Subtitle: "These three numbers control how the system sizes every trade. You can change
  them anytime."

  Three slider controls (stacked, full-width):

    Slider 1: "Risk per trade"
      Label: "If a stop-loss hits, what % of my total capital should I lose at most?"
      Range: 0.1% → 2.0%  |  Default: 0.5%  |  Step: 0.1%
      Live preview below slider:
        "On a ₹10 lakh portfolio: maximum loss per trade = ₹5,000"
        (updates as slider moves — requires portfolio size input below)
      Portfolio size input (small, right-aligned): "My capital: ₹ [______]"

    Slider 2: "Maximum single position"
      Label: "The most I'll put into any one stock"
      Range: 5% → 20%  |  Default: 10%
      Live preview: "On ₹10 lakh: max ₹1,00,000 in any one stock"

    Slider 3: "Pause when portfolio drops"
      Label: "Stop all new buys if my portfolio falls this much in a week"
      Range: 2% → 10%  |  Default: 5%
      Live preview: "On ₹10 lakh: pause trigger = -₹50,000 in a week"

  AI tutor: "The most important slider is 'Risk per trade.' At 0.5%, even 20 consecutive
  losing trades would lose only 10% of your capital. Professional quant funds typically
  use 0.25-1.0%. Anything above 1.5% is aggressive — only use it if you're comfortable
  with larger swings."

Step 4 of 4 — "Name and launch"
  Title: "You're ready to backtest"
  Subtitle: "Review your configuration, name your strategy, and run your first backtest."

  Summary card (read-only, clean two-column layout):
    Universe:      Nifty 100
    Strategies:    Trend Follow, Breakout, Quiet Breakout, Trend Pullback
    Risk/trade:    0.5%
    Max position:  10%
    Pause at:      -5% weekly

  Strategy name input: "Name your strategy" → [ My First Strategy ]

  Large primary CTA: "Run Backtest on 2018–2025 Data →"
  Muted text below: "Takes about 10 seconds. Free for your first 3 backtests."

---

PAGE 3: Strategy Builder + Drag-and-Drop Canvas  (/strategy/[id])

This is the most important page. It has two sub-modes toggled by a tab:
  Tab 1: "Canvas" — React Flow drag-and-drop visual pipeline (default)
  Tab 2: "Settings" — traditional form-based config (same data, different view)

LAYOUT (Canvas mode):
  Top bar (full-width, sticky):
    Left: ← Back   |  "My First Strategy"  |  [unsaved indicator dot if changes pending]
    Right: [ Backtest ] (primary, indigo)   [ Paper Trade ] (secondary, grayed + "Phase 2" badge)
           [ Live ] (secondary, grayed + "Phase 3" badge)

  Left sidebar (280px, fixed):
    Section: "Add Blocks"
    Five draggable block items (styled as pills with drag handle icon):
      ⠿ Universe Filter
      ⠿ Market Regime
      ⠿ Strategy (Trend Follow)
      ⠿ Strategy (Breakout)
      ⠿ Risk Rules

    Section: "Templates"  (collapsed by default)
    Four template buttons that load a preset node arrangement:
      Bear Shield | Bull Rider | Balanced | Recovery

    Section: "AI Assistant"  (persistent, bottom of sidebar)
    Small chat input: "Ask about your strategy..."
    Last AI message visible (2 lines, expandable)

  Main canvas area (flex-1, dark background #0D0D0D):
    React Flow canvas with a subtle dot-grid background pattern.
    Zoom controls bottom-right (React Flow default, restyled to match design).
    MiniMap bottom-right (React Flow, optional toggle).

    NODES (React Flow custom node components):

    Node 1 — Universe Node
      Shape: Rounded rectangle, 220px wide
      Header: "Universe" label + Globe icon (indigo)
      Body:
        Selected: "Nifty 100"
        Active today: "74 stocks" (small muted text)
      Footer: [Edit ✎] button
      Handle: output handle on right side only

    Node 2 — Regime Node
      Header: "Market Regime" + Shield icon
      Body:
        Current: pill badge showing current regime label (color-coded)
          GREEN: BULL_CONFIRMED, BULL_EARLY, BULL_WATCH
          AMBER: SIDEWAYS_CHOPPY, TRANSITION_UP, BEAR_WATCH, BEAR_TRANSITION
          RED: BEAR_CONFIRMED
        Pause threshold: "35% downtrend"
      Footer: [Edit ✎]
      Handles: input left, output right

    Node 3+ — Strategy Nodes (one per enabled strategy)
      Header: Strategy name + appropriate icon
      Body: Key parameter displayed (e.g., "Lookback: 10 days")
      Footer: AI allocation badge: "AI weight: 30%" (amber pill)
      Handles: input left, output right

    Node — Risk Rules Node
      Header: "Risk Rules" + Lock icon
      Body (3 rows):
        Risk/trade: 0.5%
        Max position: 10%
        Stop-loss: ATR × 2
      Footer: [Edit ✎]
      Handle: input left, output right (connects to "Signals" terminal node)

    Node — Signals (terminal)
      Header: "Live Signals"
      Body: "~3 signals/week" (estimated, from backtest data)
      No edit button. Informational only.

    EDGES:
      Animated dashed edges (React Flow animated prop) between connected nodes.
      Edge color: indigo (#6366F1) when regime is BULL, amber when TRANSITION, red when BEAR.

    EMPTY STATE (no nodes placed yet):
      Centered ghost text: "Drag blocks from the left panel to build your pipeline"
      Dashed border rectangle showing suggested layout
      "Or load a template →" link

  Right panel (320px, slides in when a node is clicked — closed by default):
    Node edit panel. Content depends on which node is selected.

    UNIVERSE node panel:
      Title: "Universe Settings"
      Radio group: Nifty 50 / Nifty 100 (●) / Broad 150
      Info card: "The DynamicUniverseAgent scans your chosen universe daily, scores
      every stock on volume momentum and trend quality, and selects the top 80 candidates.
      The 5 specialist filters then narrow this to 60-80 active symbols."
      [?] links next to every term

    STRATEGY node panel:
      Title: "[Strategy Name] Settings"
      Toggle: Enabled (ON by default)
      Minimum floor weight: slider 0% → 40%
      Expandable "Advanced Parameters" section (collapsed by default):
        Strategy-specific params (lookback period, volume threshold, etc.)
        Each param: label + slider + one-line explanation
      Backtest contribution: small stat row showing this strategy's Sharpe/Return
      contribution when enabled vs disabled (from most recent backtest)

    RISK node panel:
      Title: "Risk Rules"
      Note at top: "These rules apply to every trade regardless of which strategy fires."
      Three sliders (same as wizard step 3 but in panel form)
      Read-only section: "Platform-managed (cannot be changed)"
        ATR stop-loss multiplier: 2.0×
        Min ATR-to-cost ratio: 3.0×
        Explanation: "These prevent entering trades where the expected gain is too small
        relative to commission cost and volatility."

  AND/OR Logic Gate Nodes (advanced, available via sidebar):
    Custom React Flow node type: LogicGateNode
    Displays: AND gate or OR gate visual (simple rectangle with operator label)
    Can be inserted between Strategy nodes and the Risk node
    Example: Breakout → [AND gate] → Risk (gate checks: Breakout signal AND regime BULL_WATCH or better)
    Gate config panel (in right panel when selected):
      Condition builder: dropdown (signal type) + dropdown (operator) + dropdown (value)
      [+ Add condition]
      "Entry fires when: ALL of these / ANY of these" toggle

---

PAGE 4: Backtest Results  (/strategy/[id]/backtest)

LAYOUT: No sidebar. Full-width. Three content columns on desktop (stats, chart, AI panel).

Top section — Strategy summary bar:
  Strategy name + regime badge (current regime)
  Tabs: [ Overview ] [ Period Breakdown ] [ Trade Log ] [ Compare ]

OVERVIEW TAB:

Hero metrics row (4 cards, equal width, top of page):
  Card 1: Total Return
    Large number: "+94.3%"
    Subtext (muted, small): "Total return 2019 → 2025"
    Explanation line: "Cumulative growth of ₹10 lakh invested at start"
    Comparison pill: "Nifty 50: +67.2%" (gray background)

  Card 2: Max Drawdown
    Large number: "-18.7%"
    Subtext: "Worst peak-to-trough decline"
    Explanation line: "Largest drop from a portfolio high before recovering"
    Comparison pill: "Nifty 50: -38.1%" (this card shows advantage clearly)

  Card 3: Sharpe Ratio
    Large number: "1.14"
    Subtext: "Risk-adjusted return quality"
    Explanation line: "Return earned per unit of risk. Above 1.0 is strong."
    Comparison pill: "Nifty 50: 0.82"

  Card 4: Win Rate
    Large number: "58%"
    Subtext: "Trades that closed profitable"
    Explanation line: "58 out of every 100 trades ended in a gain"

Click any card → right panel slides in with Level 2 explanation (3 paragraphs, specific
to user's numbers)

Portfolio value chart:
  Simple line chart (Recharts LineChart)
  Two lines: "My Strategy" (indigo) and "Nifty 50" (gray dashed)
  X-axis: years (2019, 2020, 2021, 2022, 2023, 2024, 2025)
  Y-axis: portfolio value (starts at ₹10 lakh)
  Tooltip: date, strategy value, Nifty value, difference
  Regime shading: vertical colored bands behind the chart (green for bull periods,
  red for bear periods, amber for transition) — subtle, low opacity (0.08)
  Chart title: "₹10 lakh invested in Jan 2019"

AI Narrative section (full-width card below chart):
  Header: "What happened — explained"  + bot icon
  Content: 4-6 paragraph AI-generated narrative (fetched after backtest completes)
  Loading state: skeleton lines while streaming
  The narrative uses headers: "What worked", "What to watch", "In bear markets",
  "If you want to improve this"

PERIOD BREAKDOWN TAB:
  Table with columns: Period | Dates | Return | Max Drawdown | Regime | vs Nifty
  Each row is a distinct market phase (Bull 2019-20, Crash 2020, Recovery 2020-21, etc.)
  Color-coded return cells (green positive, red negative)
  Click any row → expands to show: which strategies fired, how many trades, what
  the regime context was doing during that period

TRADE LOG TAB:
  Filterable table: All / BUY / SELL / Blocked
  Columns: Date | Symbol | Action | Strategy | Entry Price | Exit Price | P&L | Reason
  "Blocked" filter shows trades the circuit breaker or risk rules prevented
  Each row has a [Why?] icon → inline tooltip explaining the signal logic
  Export to CSV button (top right of table)

COMPARE TAB:
  Side-by-side comparison. Start with current strategy pre-loaded in slot 1.
  Slot 2, 3, 4: "Add strategy" dropdown (from user's saved strategies) or "Nifty 50"
  Metric comparison grid: same 4 hero metrics + trades/year + best period + worst period
  AI comparison narrative: "Strategy A has a better Sharpe but lower total return.
  Here's why that tradeoff might be worth it for you..."

---

NAVIGATION & GLOBAL COMPONENTS:

Top navigation (sticky, full-width):
  Left: QuantCanvas logo
  Center: [ Dashboard ] [ My Strategies ] [ Learn ] [ Paper Trade (Phase 2) ] [ Live (Phase 3) ]
  "Phase 2" and "Phase 3" nav items are grayed out with a lock icon and tooltip:
  "Available after 30 days of successful backtesting. Coming in Phase 2."
  Right: AI tutor toggle button + avatar/account menu

AI Tutor panel (global, slides in from right):
  Triggered by: tutor toggle button in nav, or "Ask" buttons throughout pages
  Width: 380px
  Header: "AI Tutor" + close button
  Chat history (scrollable)
  Input: "Ask anything about your strategy..." + send button
  The panel retains context: knows which page the user is on, their current strategy
  config, and their most recent backtest results
  Suggested prompts (shown when input is empty, as clickable chips):
    "Why did my strategy underperform in 2019?"
    "What does Sharpe ratio mean?"
    "How do I reduce my drawdown?"
    "Should I add Mean Reversion?"

Phase 2 / Phase 3 "Coming Soon" pages:
  /paper-trade → full-page centered card:
    Title: "Paper Trading — Phase 2"
    Description: "Run your tested strategy in real-time without risking real money.
    Watch live signals, track positions, and receive daily briefings — before going live."
    Feature list (with checkmarks): Live signal generation | Nightly AI briefing email |
    Position tracking | Weekly health report | 30-day gate before live
    CTA: "Join the waitlist" → email capture form
    Timeline: "Expected: Month 4-6"

  /live-trading → same treatment:
    Title: "Live Trading — Phase 3"
    Feature list: Zerodha / Upstox broker connection | Real order placement |
    Capital allocation controls | Daily loss limit enforcement
    Timeline: "Expected: Month 7-9"
```

---

## PHASE 2 PROMPT — Paper Trading Dashboard

```
Build Phase 2 pages for QuantCanvas. Users in Phase 2 have a strategy configured and
backtested. These pages show real-time paper trading results. Add to the existing Phase 1
app — the /paper-trade route now resolves to these pages instead of the Coming Soon shell.

Use the master context for design system. All Phase 2 pages live under /paper-trade/[id].

---

PAGE 5: Paper Trading Dashboard  (/paper-trade/[id])

This is the primary daily-use page. Users check this once per day or once per week.
The design goal is: answer "is everything OK?" in under 5 seconds.

LAYOUT:
  Top: same global nav. Active: "Paper Trade" (indigo underline)
  Body: 2-column layout — left column (flex-1) = main content, right column (360px) = AI panel

LEFT COLUMN:

Status header (large, top of content):
  Strategy name | Status badge: ● Running (green pulse dot)
  "Paper trading — Day 18 of 30"   progress bar (18/30, indigo fill)
  Sub-line: "Go Live unlocks in 12 days after completing 30 paper trading days."

Four metric cards (same pattern as backtest — number, explanation, comparison):
  Portfolio Value    | P&L since start      | Max Drawdown (so far) | vs Nifty
  ₹10,42,310        | +4.2% (+₹42,310)     | -3.1%                 | +5.3% ahead

Market Regime card (full-width, prominent):
  Left: Large regime label with appropriate color
    "BEAR_TRANSITION" (amber)
  Center: Breadth reading
    "62% of tracked stocks in downtrend"
    Progress bar: 0% ————●——————— 100% with threshold marker at 35%
    "Circuit breaker active above 35%"
  Right: Trend direction
    Arrow icon (up/flat/down) + "Improving for 3 consecutive days"
  Bottom: one-line AI note:
    "If breadth improves 2 more days, regime shifts to TRANSITION_UP and cautious
    re-entry begins."

Open Positions section:
  Table: Symbol | Held since | Entry price | Current price | P&L% | Strategy | Stop-loss
  Each row is clickable → expands to show the entry reason ("why was this entered?")
  P&L% column: green text for positive, red for negative
  Stop-loss column: shows the exact stop price (e.g., ₹3,089) + distance in % (e.g., -3.8%)
  "Why was this entered?" expansion: one sentence, e.g.:
  "Entered on 10-day high with 2.3× volume in BULL_WATCH regime on Apr 3."

Today's Signals section:
  Two columns: Fired | Blocked
  Fired list: signal symbol, action, strategy, price — same table style as trade log
  Blocked list: symbol, action that would have fired, reason blocked
    Reason examples:
    "Circuit breaker: 62% downtrend (threshold: 35%)"
    "Position limit: already at 10% max for this stock"
    "Daily loss limit: portfolio down 4.8% today (threshold: 5%)"

RIGHT COLUMN — AI Daily Briefing:
  Header: "Today's Briefing"  + date
  Auto-generated after each trading day ends (3:35 PM IST)
  Loading state: "Briefing generates after market close (3:35 PM IST)"
  Content: structured narrative
    - One headline sentence (what kind of day was it)
    - Regime paragraph (what happened with breadth)
    - Signals paragraph (what fired, what was blocked, why)
    - Positions paragraph (notable movers)
    - Forward-looking sentence (what to watch tomorrow / next week)
  "Ask a follow-up" input at bottom of briefing (routes to AI tutor)

---

PAGE 6: Live Positions  (/paper-trade/[id]/positions)

LAYOUT: Full-width, no right column. Data-dense.

Page header:
  Title: "Open Positions"
  Subtitle: "4 positions | ₹3,92,450 deployed | ₹6,49,860 available"

Position cards (card grid, 2-col on desktop):
  Each card:
    Top: Symbol (large, bold) | Strategy badge (small colored pill)
    Row 1: Entry ₹3,210  →  Current ₹3,380  |  +5.3%  (+₹2,040)
    Row 2: Held 4 days  |  Stop-loss: ₹3,089 (-3.8% from current)
    Row 3: "Why entered:" one-sentence reason
    Row 4 (collapsed, expandable): full indicator snapshot at time of entry
      ATR at entry, regime at entry, volume ratio, RSI

  Click card → full-page detail slide-in (not a new route):
    Detailed position view with P&L chart (line chart, from entry date to today)
    All indicators at entry + current indicators
    AI note: "This position is behaving as expected for a Trend Follow entry in
    BULL_WATCH regime. The stop-loss gives the trade room for normal volatility
    (ATR = ₹48, stop is 2 ATR away = ₹96 below entry)."

Closed positions section (below open):
  Simpler table: Symbol | Entry | Exit | Return | Days held | Strategy | Exit reason

---

PAGE 7: Signal History  (/paper-trade/[id]/signals)

LAYOUT: Full-width, filter bar at top.

Filter bar:
  [ All ] [ BUY ] [ SELL ] [ Blocked — CB ] [ Blocked — Risk ] [ Date range picker ]
  Search: symbol name

Signal table:
  Date | Symbol | Action | Strategy | Price | Status | Reason
  Status badges: FIRED (green) | BLOCKED-CB (amber) | BLOCKED-RISK (amber) | FILLED (indigo)
  Click row → side panel with full context:
    All indicator values at signal time
    Exact circuit breaker reading (e.g., "62% downtrend vs 35% threshold")
    AI explanation of why this signal fired or was blocked

Insights card (top of page, above table):
  "Since paper trading started, the circuit breaker has blocked 34 signals.
  Without it, your maximum paper drawdown would have been -12.4% instead of -3.1%."
  (AI-generated, updated daily)

---

PAGE 8: Weekly Health Report  (/paper-trade/[id]/report)

LAYOUT: Single-column, centered, max-w-3xl. Designed to be printable / email-friendly.

This page mirrors the email report but is also accessible on-platform.

Header:
  "Weekly Health Report — My First Strategy"
  "Week ending April 5, 2026"
  Status badge: ✅ All systems normal

Summary cards row (4 across):
  Week P&L | Regime this week | Signals fired | Days to Go Live unlock

Narrative sections (styled as report sections with subtle dividers):
  "What the market did this week" — regime classification, breadth trend
  "What your strategy did" — trades taken, trades blocked, notable exits
  "Open positions this week" — brief summary of each position
  "What to watch next week" — upcoming events, regime trajectory, AI suggestion

Suggested action card (amber background, bottom):
  Icon: lightbulb
  Title: "One thing to consider"
  Body: AI-generated suggestion, e.g.:
  "The market has been in BEAR_TRANSITION for 6 days. If breadth improves
  through next week, consider increasing your 'Trend Follow' minimum floor weight
  from 0% to 20% to capture the early recovery signal."
  [ Open Strategy Settings ] button

```

---

## PHASE 3 PROMPT — Live Trading (Coming Soon Shell → Full Build)

```
Build Phase 3 pages for QuantCanvas. In the current release, Phase 3 pages show as
"Coming Soon" shells with waitlist capture. The full Phase 3 build prompt below is for
the future release when live trading is ready.

---

PAGE 9: Live Trading Setup  (/live-trading)

This page is currently a Coming Soon shell. Build the shell now. The full build is
described below for when Phase 3 is ready.

COMING SOON SHELL (build now):

  Full-page centered layout (no sidebar):

  Breadcrumb: Dashboard → Live Trading

  Large centered card (max-w-xl):
    Title: "Live Trading — Phase 3"
    Subtitle: "Trade real capital through your existing Zerodha or Upstox account.
    Signals become real orders. The same strategy you paper-tested goes live."

    Feature list (checkmarks, 2-column):
      ✓ Zerodha & Upstox integration    ✓ Real order placement at market open
      ✓ Capital allocation controls      ✓ Daily loss limit (auto-enforced)
      ✓ Same pipeline as paper trading   ✓ Live vs paper portfolio comparison

    Requirement banner (amber, with icon):
      "Requires 30 days of completed paper trading on your strategy.
      You are on paper trading day 18."
      Progress bar: 18/30

    Email capture:
      "Notify me when live trading opens:"
      [ your@email.com ] [ Notify Me ]

    Timeline: "Expected: Month 7-9 (approx. October 2026)"

FULL LIVE TRADING BUILD (when Phase 3 is ready):

  Step 1 — Broker Connection  (/live-trading/connect)
    Card with broker selector:
      Large radio cards (same style as universe selector):
        ● Zerodha (recommended)
            "India's largest retail broker. Direct MF + equity delivery."
        ○ Upstox
        ○ Angel One
        ○ ICICI Breeze

      After selecting Zerodha:
        API setup instructions (numbered, with screenshots referenced):
          1. Go to kite.trade/connect
          2. Create an app and copy your API Key and API Secret
          3. Paste below

        Two inputs: API Key | API Secret (password type)
        [ Authenticate with Zerodha → ] (OAuth2 redirect)

      After successful auth:
        Green success banner: "Connected to Zerodha — Ujjwal Kumar"
        Account details: Available margin | Existing positions | Demat holdings
        [ Continue to Capital Allocation → ]

  Step 2 — Capital Allocation  (/live-trading/allocate)
    Single centered card:
      Title: "How much capital to deploy?"

      Input: ₹ [1,00,000] (number input, formatted)

      Info card below input:
        "Recommended: Start with 25-50% of your intended final amount.
        At ₹1,00,000 with your current risk settings:"
        Three rows:
          Max loss per trade:     ₹500  (0.5% of ₹1,00,000)
          Max open positions:     10
          Daily loss pause at:    -₹5,000 (5% of ₹1,00,000)

      Risk summary (read-only recap of current risk settings)

      [ Continue to Review → ]

  Step 3 — Go Live Review  (/live-trading/review)
    Title: "Review before going live"
    Full strategy config summary (clean two-column table, read-only)
    Paper trading results summary (30-day results card)
    Compliance note (collapsible):
      "By activating live trading, I confirm I understand this platform generates
      automated signals executed through my broker account. Signals are based on
      historical backtesting and do not guarantee future returns."
    Two buttons:
      [ Keep Paper Trading ] (secondary)
      [ Activate Live Trading ] (primary, red — intentionally alarming color to signal gravity)

    After clicking Activate:
      Modal confirmation:
        "Are you sure? This will place real orders through your Zerodha account
        starting tomorrow at 9:15 AM IST."
        [ Cancel ] [ Yes, Go Live ]

  Live Trading Dashboard (same layout as Paper Trading Dashboard):
    Identical to paper trading dashboard but:
      Status badge: ● Live (red pulse dot instead of green)
      "Paper day 18 of 30" replaced with "Live since April 15, 2026 (Day 12)"
      P&L numbers are real
      Positions link out to Zerodha for order confirmation
      Additional card: "Broker Order Log" showing signal → order → fill chain with
      slippage comparison (signal price vs fill price for each trade)
```

---

## Global Components to Build (used across all phases)

```
Build these as reusable components before building any page:

1. MetricCard
   Props: value (string), label (string), explanation (string), comparison (optional string),
   onClick (optional — triggers Level 2 explanation panel)
   Use: everywhere a metric is displayed

2. RegimeBadge
   Props: regime (string — one of the 8 regime labels)
   Renders: colored pill with regime name. Color mapping:
     BULL_CONFIRMED, BULL_EARLY, BULL_WATCH → green (#22C55E variants)
     SIDEWAYS_CHOPPY → gray
     TRANSITION_UP, BEAR_WATCH, BEAR_TRANSITION → amber (#F59E0B variants)
     BEAR_CONFIRMED → red (#EF4444)

3. ExplainPanel
   Props: title (string), paragraphs (string[]), onClose
   Renders: 380px right slide-in panel with 3-paragraph explanation
   Triggered by: clicking any MetricCard, clicking [?] icons, clicking signal rows

4. AITutorPanel
   Props: strategyContext (object), currentPage (string)
   State: message history (array), input value, loading
   Renders: 380px right slide-in chat panel
   API: POST /api/tutor with { message, context } → streaming response

5. ComingSoonPage
   Props: phase (string), title (string), description (string), features (string[]),
   timeline (string)
   Renders: full-page centered coming soon card with email capture

6. PipelineNode (React Flow custom node)
   Props: type (universe|regime|strategy|risk|signals|logic-gate), config (object),
   isSelected (boolean)
   All five node types use this base + type-specific body content

7. LogicGateNode (React Flow custom node)
   Props: operator (AND|OR), conditions (array), isSelected
   Visual: rectangle with operator label in center, input handles on left, output right

8. StrategyConfigPanel
   Props: nodeType, config, onChange
   Used in the React Flow right panel when a node is selected
   Contains all Tier 1 and Tier 2 config options for that block type
```

---

## API Routes Expected from Backend (FastAPI)

```
Phase 1:
  POST /api/backtest           { strategy_config } → { results, trades, periods }
  GET  /api/strategies         → list of user's saved strategies
  POST /api/strategies         { config, name } → { id }
  PUT  /api/strategies/[id]    { config } → { ok }
  POST /api/tutor              { message, context } → streaming text

Phase 2:
  GET  /api/paper/[id]         → { portfolio_value, pnl, positions, signals_today }
  GET  /api/paper/[id]/signals → paginated signal history
  GET  /api/paper/[id]/report  → weekly health report data
  POST /api/paper/[id]/start   → activates daily signal pipeline for strategy

Phase 3:
  POST /api/live/connect       { broker, api_key, api_secret } → OAuth redirect
  POST /api/live/[id]/activate { capital } → activates live trading
  GET  /api/live/[id]/orders   → broker order log with fill prices
```

---

## Notes for the Builder

- Build Phase 1 first, fully. Phase 2 and 3 exist only as Coming Soon shells in Phase 1.
- The React Flow canvas is the primary builder UI from day one — not a Phase 5 feature.
  The drag-and-drop canvas, custom indicator parameters, and AND/OR logic gates are all
  in Phase 1. This is what differentiates the product visually from the start.
- Do not add a stock price chart (candlestick or OHLC). The platform deliberately has none.
- Every metric number must have an explanation string rendered beneath it in muted text.
  This is a hard design requirement — never show a raw number without its plain-English meaning.
- The AI tutor panel is always accessible (global nav button). It is not a page — it is a
  persistent overlay that can be opened from anywhere.
- Phase 2 and 3 nav items are visible but grayed with a lock icon. Clicking them shows a
  tooltip: "Complete [X] to unlock." This communicates the roadmap without hiding it.
```
