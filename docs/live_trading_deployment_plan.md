# Live Trading Deployment Plan — Multi-Strategy Adaptive System

**Last updated**: 2026-03-22
**Status**: Paper trade pipeline complete. Cron scheduled. Ready to run from 2026-03-23.

---

## Current System Status

The system has evolved significantly since this doc was first written (single Breakout 10d).
The current deployed stack is a **5-strategy adaptive portfolio** driven by an LLM regime classifier.

### What is built and validated (backtest 2018–2024)

| Component | File | Status | Validated result |
|---|---|---|---|
| DualMA SMA20/50 | `app/strategy/dual_ma.py` | ✅ Done | Sharpe 1.33, Bear 2022 +ve |
| Breakout 10d | `app/strategy/breakout_momentum.py` | ✅ Done | Sharpe 1.25, Recovery leader |
| QuietBrk 20d | `app/strategy/quiet_breakout.py` | ✅ Done | Sharpe 0.89, Crash specialist |
| TrendPB 5% | `app/strategy/trend_pullback.py` | ✅ Done | Sharpe 0.79, Crash/Recovery |
| RSI-MR os=5 | `app/strategy/rsi_mean_reversion.py` | ✅ Done | Sharpe 0.22, Recovery only |
| MultiStrategyRouter | `app/strategy/multi_router.py` | ✅ Done | position_owners ownership gate |
| AdaptiveStrategySelector | `app/meta/adaptive_selector.py` | ✅ Done | GPT-4o-mini, weekly rebalance |
| UnionUniverseFilter | `app/universe/filters.py` | ✅ Done | 60-80 symbol pool |
| BacktestEngine | `app/backtest/engine.py` | ✅ Done | adaptive_selector param wired |
| RiskAgent | `app/risk/agent.py` | ✅ Done | ATR stop, breadth CB, vol sizing |

### Known issues that affect live deployment

| Issue | Impact | Fix status |
|---|---|---|
| RECOVERY over-triggers in NSE bull markets | DualMA underweighted in 2023-24 | ✅ Threshold raised to 0.022 |
| BULL_SUSTAINED regime missing | 2023-24 bull misclassified as RECOVERY | ✅ Regime added |
| DualMA minimum weight floor | Could drop below 0.10 in RECOVERY | ✅ Floor added in `_parse_weights()` |
| Bull 2019 loss from commission drag | Multi-strategy 5× trade frequency hurts | ✅ Min ATR-to-cost filter in `RiskAgent` |
| Regime stability gate (2-week) | Allocation whipsaws on brief regime spikes | ✅ Built in `AdaptiveStrategySelector` |
| Breadth circuit breaker threshold | Default 0.40 too loose for current bear | ✅ Tightened to 0.35 in `run_signals.py` |
| Signal persistence (2-day breakout confirm) | False entries in choppy markets | ❌ Not built (post-paper-trade) |
| Execution price = close (not next-day open) | Backtest slightly optimistic | ❌ Not fixed (paper run will measure gap) |
| No volume constraint on sizing | Market impact underestimated for small-caps | ❌ Not built (post-paper-trade) |
| Look-ahead bias in Sharpe table | LLM "knows" which strategies work — live will be lower | ❌ Structural — needs walk-forward |

### Current backtest results (full 2018–2024)

| Run | Sharpe | Return | MaxDD |
|---|---|---|---|
| EqualWeight (5-strat) | 1.23 | +101.06% | 15.18% |
| Adaptive (LLM weights) | 1.18 | +114.74% | 22.03% |
| Bear 2022 — Adaptive | **1.30** | **+12.56%** | 8.34% |
| Bear 2022 — EqualWeight | 0.27 | +1.88% | 15.21% |

---

## Pre-Paper-Trade Checklist

These are the items that MUST be done before starting any paper trade run.
Items are sorted: code changes → infrastructure → validation.

### Code changes — status as of 2026-03-22

- [x] **Enable `breadth_circuit_breaker=True`** — ✅ Done. `max_downtrend_pct=0.35` in `run_signals.py`
- [x] **Minimum ATR-to-cost filter** — ✅ Done. `min_atr_cost_ratio=3.0` in `RiskAgent` + `run_signals.py`
- [x] **Regime stability gate (2-week)** — ✅ Done. `regime_stability_weeks=2` in `AdaptiveStrategySelector`
- [x] **RECOVERY threshold 0.018 → 0.022** — ✅ Done in `_classify_regime()`
- [x] **BULL_SUSTAINED regime** — ✅ Done in `_classify_regime()` + LLM allocation rules
- [x] **DualMA minimum weight floor 0.10** — ✅ Done in `_parse_weights()`
- [ ] **Earnings date avoidance gate** — ❌ Needed before April 2026 Q4 season. See `app/data/earnings_calendar.py`
- [ ] **Re-run backtest with all improvements** — ❌ Run `python run_experiments.py` to update reference Sharpe numbers

### Infrastructure — status as of 2026-03-22

- [x] **`app/broker/base.py`** — ✅ `BrokerAdapter` ABC
- [x] **`app/broker/paper_adapter.py`** — ✅ Fills at next-day open from `market_ohlc`
- [x] **`app/broker/models.py`** — ✅ `Order`, `BrokerPosition` dataclasses
- [x] **`signal_queue` DB table** — ✅ Live in Supabase (`scripts/init_db.py`)
- [x] **`live_positions` DB table** — ✅ Live in Supabase (`scripts/init_db.py`)
- [x] **`selector_state` DB table** — ✅ Live in Supabase (`scripts/create_live_tables.sql`)
- [x] **`run_signals.py`** — ✅ Complete 15-step pipeline (3:35 PM IST)
- [x] **`run_orders.py`** — ✅ Complete fill simulation job (9:15 AM IST)
- [x] **`app/data/calendar.py`** — ✅ `NSECalendar` with 2025-2026 NSE holidays
- [x] **`scripts/run_signals.sh`** — ✅ Cron wrapper (loads `.env`, runs venv python)
- [x] **`scripts/run_orders.sh`** — ✅ Cron wrapper
- [x] **`logs/` directory** — ✅ Created
- [ ] **`.env` file** — ⚠️ Created at `.env`. **Add real `OPENAI_API_KEY` before first run.**
- [ ] **Cron installed** — ⚠️ macOS blocked write (Terminal needs Full Disk Access). See install instructions below.
- [x] **Email notifications** — ✅ Done. `app/core/notify.py` sends Gmail SMTP summary after each run.
- [ ] **Daily P&L report (Telegram)** — ❌ Not built. Email covers immediate needs; Telegram can be added later.

### Deployment: Railway.app (Mac does NOT need to be running)

The pipeline is deployed to **Railway.app** — a cloud platform that runs the two cron jobs on its servers.
Your Mac only needs to be on to push code changes.

**Architecture:**
```
Railway cloud
  ├─ run-signals service  → cron: 5 10 * * 1-5  (3:35 PM IST)
  └─ run-orders service   → cron: 45 3 * * 1-5  (9:15 AM IST)
          ↓
  Supabase (PostgreSQL) — already cloud-hosted
          ↓
  Gmail SMTP → email to you after each run
```

**One-time Railway setup:**

1. Install Railway CLI:
   ```bash
   brew install railway
   ```
2. Login and create project:
   ```bash
   railway login
   railway init        # creates a new Railway project linked to this repo
   ```
3. Set environment variables in Railway dashboard (or CLI):
   ```bash
   railway variables set OPENAI_API_KEY=sk-...
   railway variables set EMAIL_FROM=your@gmail.com
   railway variables set EMAIL_TO=your@gmail.com
   railway variables set EMAIL_APP_PASSWORD=xxxx-xxxx-xxxx-xxxx
   # DATABASE_URL is optional — fallback is hardcoded in app/core/database.py
   ```
4. Deploy:
   ```bash
   git add .
   git commit -m "add Railway deployment"
   railway up
   ```
5. Railway reads `railway.toml` and creates both cron services automatically.
   Verify at: `https://railway.app/dashboard` → your project → two services visible.

**Cost:** ~$5/month on Railway Hobby plan (two lightweight cron jobs, minimal CPU/RAM).

**Gmail App Password setup (for email):**
1. Enable 2-Step Verification on your Google account
2. Go to: Google Account → Security → App Passwords
3. Create one named "Financial Lab" — get a 16-char password like `abcd efgh ijkl mnop`
4. Use that (without spaces) as `EMAIL_APP_PASSWORD`

### Validation (before calling paper trade "running")

- [ ] Dry-run `run_signals.py` manually (`./finance/bin/python3 run_signals.py`) — verify signal counts
- [ ] Check `signal_queue` table for written signals after first real run
- [ ] Verify `live_positions` persists correctly after `run_orders.py` fills
- [ ] Trigger `breadth_circuit_breaker` manually (set `max_downtrend_pct=0.01`) — confirm BUY suppressed
- [ ] Confirm earnings date avoidance fires for a known Q4 result date (build first)
- [ ] Confirm paper portfolio equity calculation matches manual check

---

## Implementation Order — Minimum Path to Paper Trade

Ordered by dependency and impact. Items in **bold** block everything downstream.

| Priority | Task | Effort | Blocks |
|---|---|---|---|
| ~~P0~~ | ~~Enable `breadth_circuit_breaker=True`~~ | ✅ Done | — |
| ~~P1~~ | ~~Min ATR-to-cost filter~~ | ✅ Done | — |
| ~~P1~~ | ~~Regime stability gate~~ | ✅ Done | — |
| **P1** | **Earnings date avoidance gate** | **2 hrs — build before April** | **Q4 season** |
| P2 | Re-run backtest with all improvements | 15 min | Updated reference numbers |
| ~~P3~~ | ~~`app/broker/base.py` + `paper_adapter.py`~~ | ✅ Done | — |
| ~~P3~~ | ~~`signal_queue` + `live_positions` DB tables~~ | ✅ Done | — |
| ~~P4~~ | ~~`run_signals.py` daily signal job~~ | ✅ Done | — |
| ~~P4~~ | ~~`app/data/calendar.py` NSE holiday calendar~~ | ✅ Done | — |
| ~~P5~~ | ~~`run_orders.py` order placement job~~ | ✅ Done | — |
| ~~P5~~ | ~~Email notifications~~ | ✅ Done (`app/core/notify.py`) | — |
| **P5** | **Set env vars in Railway + deploy** | **15 min — do now** | **Cloud scheduling** |
| P6 | Daily P&L report (Telegram) | 2 hrs | Richer observability |
| P7 | 5-day observation (check logs/signals.log daily) | 1 week | Validation |
| **P8** | **Paper trade: 6–8 weeks** | **6–8 weeks** | **Confidence before real money** |

---

## Section 1 — Current Market Context (March 2026)

### Why paper trade is especially important right now

The market is in a **news-driven bearish regime** due to ongoing geopolitical conflict.
This is structurally different from the 2022 data-driven bear the system was trained on:

| Characteristic | 2022 Bear (training data) | Current Bear (Mar 2026) |
|---|---|---|
| Driver | RBI rate hikes, global inflation | War/conflict headlines |
| Speed | Slow-grinding over months | Can flip intraday on ceasefire rumours |
| Breadth signal | pct_downtrend built steadily to 45%+ | May oscillate week-to-week on news |
| DualMA signal | Captured correctly after 2-3 week lag | Lag more costly when news reverses trend |
| Classifier reliability | High — orderly macro signal | Lower — choppy, news-driven |

**What this means for the system:**
- The adaptive selector will likely see oscillating BEAR_EARLY / MIXED / BEAR_CONFIRMED labels week-to-week
- The regime stability gate (P1 above) is more important than usual — without it, allocation will whipsaw
- DualMA's 2022 edge (sustained 45%+ downtrend breadth) may not be present if news-driven bears are shorter and more volatile

### The adaptive selector in the current regime

Looking at how the selector would behave today:
- If breadth crosses 45% DOWNTREND → `BEAR_CONFIRMED` → DualMA 65-73%
- If ceasefire news → breadth drops to 35% → `BEAR_EARLY` → DualMA 40%
- If news-driven rally → breadth drops further → `RECOVERY` → DualMA 16-20%

Without the regime stability gate, a single good-news week could trigger a full allocation
shift from defensive to aggressive. The stability gate ensures the bear allocation holds
through 1-week noise spikes. **Build this before starting the paper run.**

---

## Section 2 — Data Infrastructure

### 2.1 EOD Data Provider

For paper trading, yfinance is acceptable as a starting point (it is already integrated).
The reliability issues (rate limits, occasional wrong prices) matter more in live trading.

**Paper trade (now):** Keep yfinance. Add a fallback and a data validation check:
```python
# After fetching OHLC, validate basic sanity:
assert price > 0 and volume > 0 and high >= low
```

**Before real money:** Switch to a reliable provider:
- ICICI Breeze API (free with ICICI demat, NSE-direct data)
- Upstox Historical API (OAuth2, clean REST)
- Both are drop-in swaps via the `MarketDataProvider` ABC in `app/data/models.py`

### 2.2 NSE Holiday Calendar

**What to build:** `app/data/calendar.py`

```python
class NSECalendar:
    def is_trading_day(self, date: date) -> bool: ...
    def next_trading_day(self, date: date) -> date: ...
```

NSE publishes the holiday list annually. Store as a static list, update once per year.
The `run_signals.py` job must check `is_trading_day(today)` before running — otherwise
the job runs on a holiday, fetches stale data, and generates ghost signals.

---

## Section 3 — Signal Generation Pipeline

### 3.1 Daily job architecture

```
run_signals.py  (cron: 3:35 PM IST on trading days)
    1. Check NSECalendar — exit immediately if holiday
    2. Fetch today's EOD OHLC for all 150 symbols
    3. Upsert into market_ohlc
    4. Load last 300 days of history per symbol (indicator warm-up)
    5. Run DynamicUniverseAgent → top 80
    6. Run UnionUniverseFilter → 60-80 unique symbols
    7. Run MarketObserver.run_for_day() for each symbol
    8. Build regime_snapshot from daily_symbol_states
    9. Run AdaptiveStrategySelector.rebalance() — get weekly weights
    10. Sync current positions from broker/paper adapter → build Portfolio
    11. Run MultiStrategyRouter.decide()
    12. Run RiskAgent.evaluate() for each decision
    13. Write PENDING signals to signal_queue
    14. Send daily summary notification
```

### 3.2 Order timing — the close-price problem

The strategy fires on close price. Real execution is next-day open. This creates a gap risk.

**Recommended approach for paper trade:** Place market-open orders (9:15 AM IST next day).
Record both the signal price (close) and fill price (next open) to measure slippage in paper.

This will reveal the real gap cost — currently the backtest uses close as fill price, which
is slightly optimistic. Paper trading will give you the honest number.

### 3.3 Signal queue table

```sql
CREATE TABLE signal_queue (
    id           UUID PRIMARY KEY,
    created_at   TIMESTAMP,
    signal_date  DATE,
    symbol       VARCHAR,
    action       VARCHAR,        -- BUY / SELL
    strategy     VARCHAR,        -- which sub-strategy generated it
    regime_label VARCHAR,        -- regime at time of signal
    weight       FLOAT,          -- strategy weight at signal time
    raw_price    FLOAT,          -- close price when signal fired
    target_qty   INTEGER,
    status       VARCHAR DEFAULT 'PENDING',
    order_id     VARCHAR,
    fill_price   FLOAT,
    fill_qty     INTEGER,
    notes        TEXT
);
```

`regime_label` and `weight` are new additions not in the original plan — critical for
paper trading review (did the regime call match what happened?).

---

## Section 4 — Broker Integration

### 4.1 Paper adapter (build first)

```
app/broker/
    base.py            ← BrokerAdapter ABC
    paper_adapter.py   ← Logs to DB, simulates fills at next-day open
    kite_adapter.py    ← Build later, only needed for real money
    models.py          ← Order, Fill, BrokerPosition dataclasses
```

`PaperAdapter.place_order()`:
- Writes to `signal_queue` with status=PLACED
- On next call to `get_order_status()`, returns FILLED at simulated fill price
- Fill price = next-day open from the historical/live data feed
- This captures the open-price gap that the backtest currently ignores

### 4.2 For real money: Zerodha Kite

Zerodha Kite is the recommended broker (largest retail in India, well-maintained Python SDK).
Key constraints to handle:
- `product_type = "CNC"` for delivery (not MIS — that is intraday only, auto-squared at 3:20 PM)
- `exchange = "NSE"`
- DDPI must be signed once before programmatic sell orders work
- Price band check before BUY: if stock hit upper circuit yesterday, skip

---

## Section 5 — Portfolio State & Reconciliation

```sql
CREATE TABLE live_positions (
    symbol          VARCHAR PRIMARY KEY,
    quantity        INTEGER,
    average_price   FLOAT,
    entry_date      DATE,
    strategy        VARCHAR,    -- which sub-strategy owns this position
    last_synced_at  TIMESTAMP
);
```

**Reconciliation** (start of each `run_signals.py` run):
1. Fetch positions from broker/paper adapter
2. Compare against `live_positions` DB
3. Resolve mismatches: add untracked, remove stale, log qty differences
4. Rebuild `position_owners` dict for `MultiStrategyRouter` from `live_positions.strategy` column

This ensures `MultiStrategyRouter.position_owners` survives process restarts — without it,
the ownership gate resets daily and all positions become "untracked" (exit responsibility lost).

---

## Section 6 — Risk Controls for Live Trading

### 6.1 Daily loss limit
```python
if today_pnl < -(total_equity * 0.02):   # -2% daily loss limit
    suppress_buys = True
```

### 6.2 Maximum open positions
- Cap at 10 open positions across all strategies (at 10% weight each = 100% capital deployed)
- Check before each BUY: `if len(portfolio.positions) >= 10: return HOLD`

### 6.3 Stale signal cancellation
Any PENDING signal older than 1 trading day → mark CANCELLED before placing.
The breakout condition may no longer hold by the time the order runs.

### 6.4 Conflict/news day suppression (current market context)
On days with known high macro uncertainty:
- RBI MPC decision days (next: April 2026)
- Major escalation/de-escalation news (detected by manual flag or macro event calendar)

Set a `SUPPRESS_NEW_BUYS` environment variable that `run_signals.py` checks:
```bash
# On RBI day morning, set manually before signals run:
export SUPPRESS_NEW_BUYS=1
```
Simple, no complex NLP needed. You override it manually on days you know are high-uncertainty.

---

## Section 7 — Observability & Paper Trade Monitoring

### 7.1 What to log every day (paper trade period)

Beyond standard P&L, log these for the adaptive system review:

```
Date: 2026-04-03
Regime: BEAR_CONFIRMED/HIGH (pct_down=0.48, ATR=2.31%)
Weights: DualMA=0.69 Breakout=0.25 QuietBrk=0.00 TrendPB=0.06 RSI-MR=0.00

Signals generated: 3 BUY, 2 SELL
  DualMA  BUY  RELIANCE  → 45 shares @ ₹1,423 (signal ₹1,418, gap: +0.35%)
  DualMA  BUY  HDFCBANK  → 30 shares @ ₹1,672 (signal ₹1,665, gap: +0.42%)
  Breadth CB fired: 12 BUY signals suppressed (pct_down=0.48 > 0.35 threshold)

Open positions: 6
  DualMA: RELIANCE, HDFCBANK, TCS
  Breakout: TITAN, INFY
  QuietBrk: (none)

Day P&L: -₹1,240  |  MTD: +₹3,450  |  Equity: ₹1,003,450
```

### 7.2 Weekly regime review checklist

At end of each week during paper trade:
- [ ] Did the regime label match your subjective read of the market?
- [ ] Did DualMA receive defensive weight (≥0.55) during confirmed bear weeks?
- [ ] Did the breadth circuit breaker fire on the right days?
- [ ] Was the trade count consistent with backtest frequency for this regime?
- [ ] Any symbol that entered on earnings day? (earnings filter validation)

### 7.3 Failure conditions — delay real money deployment if any of these fire

- Paper portfolio drops >8% in any 4-week window (backtest worst: 5-6% for equivalent)
- Regime oscillates BEAR ↔ RECOVERY more than 3 times in 4 weeks (classifier confused)
- Trade count exceeds 2× backtest frequency for current regime type
- Adaptive consistently underperforms equal-weight for 4+ consecutive weeks
- Daily P&L report fails to deliver for 2+ consecutive days (pipeline reliability issue)

### 7.4 Monitoring checklist before switching to real money

- [ ] Paper trade ran ≥ 30 trading days with zero pipeline crashes
- [ ] At least one full regime transition observed and correctly classified
- [ ] Signal count per week matches backtest frequency ±30%
- [ ] Position reconciliation passes every day (no phantom positions)
- [ ] Daily loss limit circuit breaker tested (manually triggered in paper mode)
- [ ] Earnings date avoidance confirmed working on at least 2 result dates
- [ ] NSE holiday handling tested (signal job skips correctly)
- [ ] Backtest benchmark re-run with CB-enabled + min ATR filter — reference numbers updated

---

## Section 8 — Phased Real-Money Deployment

Only after the Section 7 checklist is complete:

### Phase 1 — 10% capital (month 3)

```python
risk_per_trade_pct = 0.003   # half the backtest default of 0.005
max_position_pct   = 0.10    # backtest default
```

Run for 4 weeks. If MaxDD < 5% and regime calls look correct, move to Phase 2.

### Phase 2 — 50% capital (month 4-5)

Increase `risk_per_trade_pct = 0.005` (full backtest default).
Monitor trade-level slippage: is actual gap cost consistent with paper trade estimate?

### Phase 3 — Full capital (month 6+)

Only if Phase 1-2 live results are within ±20% of backtest expected Sharpe for the regime.
Consider switching to `model="gpt-4o"` for the adaptive selector (better nuance on edge cases).

---

## Backtest Accuracy Improvements Needed Before Real Money

These make the backtest a more accurate prediction of live results:

| Issue | Current (optimistic) | Fix |
|---|---|---|
| Execution price | Close price | Use next-day open in `BacktestEngine` |
| Slippage model | Fixed 0.05% | Use 0.1% for small-caps with low volume |
| Volume constraint | None | Cap at 1% of 20-day avg daily volume |
| Sharpe table bias | Full 2018-2024 (look-ahead) | Walk-forward: train on N years, test year N+1 |
| Commission rate | 0.10% | Validate against your actual Zerodha brokerage |

Expected impact of fixes: backtest Sharpe drops ~10-15% but becomes a reliable floor estimate.
