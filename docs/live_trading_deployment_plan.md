# Live Trading Deployment Plan — Short-Term Strategies

## Strategy Selection Rationale

From the backtest results, only **Breakout 10d** is viable for short-term live deployment:

| Strategy | Full Period | Crash 2020 | Bear 2022 | Verdict |
|---|---|---|---|---|
| Breakout 10d | +167% / Sharpe 1.17 | +40.6% | +8.6% | **Deploy** — only strategy positive across all regimes |
| TrendPB 3% | -8.2% / Sharpe -0.15 | -8.7% | -9.5% | Do not deploy — negative expected value |
| TrendPB 5% | -0.9% / Sharpe -0.00 | -5.7% | -2.6% | Do not deploy — flat with high drawdown risk |
| RSI-MR os=5 | -2.9% / Sharpe -0.04 | +4.6% (CB helped) | -14.5% | Not ready — bear market still destroys it |

TrendPullback has a structural problem: 60%+ win rate but still loses money, meaning average losses >> average wins. This is not a parameter problem — the pullback premise doesn't hold in this universe. Drop it from short-term live consideration entirely.

---

## Current Architecture — What Each Component Does

```
BACKTEST ONLY:
run_experiments.py
    └── PeriodContext (preloads data once per period)
            └── DynamicUniverseAgent    [bulk DB fetch → top 80 by opportunity score]
            └── UniverseSelectionAgent  [stateless filter → top 20]
            └── MarketObserverAgent     [precomputes all indicators, caches MarketState per day]
    └── BacktestEngine (runs historical date loop)
            └── BreakoutMomentumStrategy.decide() → Decision[]
            └── RiskAgent.evaluate()    [regime filter, ATR stop, vol-adjusted sizing]
            └── ExecutionAgent.execute() [slippage + commission, cash-safe qty]
            └── PortfolioEngine.buy/sell()
    └── EvaluationAgent → metrics printed to stdout
```

Nothing in this stack talks to a broker, monitors live prices, persists results, or runs on a schedule.

---

## Gap Analysis — What Is Missing for Live Trading

### Critical Gaps (system cannot function without these)

| Gap | Current State | Required State |
|---|---|---|
| Data source | yfinance (batch, unreliable) | Reliable EOD feed (Zerodha Breeze / Upstox) |
| Broker integration | None | Broker API for order placement |
| Signal generation pipeline | Driven by backtest loop | Scheduled daily job (runs at 3:30 PM IST) |
| Order placement timing | Assumes close price fill | Next-day open order or pre-open limit |
| Position reconciliation | In-memory Portfolio object | Sync from broker API at session start |
| Result persistence | stdout only | Database (signals, orders, fills, daily P&L) |
| Paper trading mode | None | Full dry-run against live prices, no real orders |
| NSE holiday calendar | Not handled | Skip signal generation on exchange holidays |

### High-Priority Gaps (deploy with known limitations otherwise)

| Gap | Impact |
|---|---|
| Price band / circuit filter check | Placing a buy on an upper-circuit stock gets rejected — wastes API calls and causes position mismatch |
| DDPI / PoA for sell orders | Zerodha requires DDPI authorisation to place delivery sell orders programmatically |
| T+1 settlement awareness | Shares bought today are not deliverable until T+1 — affects whether an intraday exit is possible |
| Daily loss limit circuit breaker | No hard stop on total portfolio loss per day |
| Corporate action adjustment | Live prices are not auto-adjusted for splits/bonuses like yfinance is — needs manual handling or CA data feed |
| Order fill uncertainty | Current model assumes full fill at exec_price; real orders may partially fill or gap |

---

## Section 1 — Data Infrastructure

### 1.1 EOD Data Provider (replace yfinance in production)

**What to build:** `app/data/providers/breeze_provider.py` (or equivalent)

yfinance is fine for backtesting but unreliable for production:
- Rate limits, API changes, occasional wrong prices
- No SLA, no support
- Does not give you intraday data for order timing

For live deployment the data stack should be:

```
EOD prices (after 4:00 PM IST)
    ├── Primary:  ICICI Breeze API  (free with ICICI demat, NSE-direct data)
    │              or Upstox Historical API
    ├── Fallback: yfinance  (acceptable if Breeze fails, not as primary)
    └── Store:    Same market_ohlc table — provider is just a swappable impl of MarketDataProvider
```

The `MarketDataProvider` ABC already exists in `app/data/models.py`. Adding a `BreezeProvider` class that implements `fetch_ohlc()` is a drop-in swap.

**What the daily ingestion job does:**
```
4:00 PM IST — market closed
    → fetch today's OHLC for all 150 symbols from Breeze API
    → upsert into market_ohlc (same schema as today)
    → mark ingestion complete in a run_log table
```

### 1.2 NSE Holiday Calendar

**What to build:** `app/data/calendar.py`

```python
class NSECalendar:
    def is_trading_day(self, date: date) -> bool: ...
    def next_trading_day(self, date: date) -> date: ...
    def previous_trading_day(self, date: date) -> date: ...
```

NSE publishes a holiday list each year. Store it as a static list in the codebase (updated annually). The signal generation job must check `is_trading_day(today)` before running. The backtest engine should also use this instead of inferring trading days from DB records.

---

## Section 2 — Signal Generation Pipeline

This is the core operational loop for live trading. It replaces `run_experiments.py`'s historical date loop with a daily scheduled job.

### 2.1 Architecture

```
run_signals.py  (runs daily at 3:35 PM IST via cron or APScheduler)
    1. Check NSE calendar — skip if holiday
    2. Fetch today's EOD data for all 150 symbols (from Breeze)
    3. Upsert into market_ohlc
    4. Load last 300 days of history per symbol (for indicator warm-up)
    5. Run DynamicUniverseAgent → top 80
    6. Run UniverseSelectionAgent → top 20
    7. Run MarketObserverAgent for today's date
    8. Sync current positions from broker API → populate Portfolio object
    9. Run BreakoutMomentumStrategy.decide()
    10. Run RiskAgent.evaluate() for each decision
    11. Write pending orders to signal_queue table (status=PENDING)
    12. Send summary notification (Telegram / email)
```

### 2.2 Signal Queue Table (new DB table)

```sql
CREATE TABLE signal_queue (
    id          UUID PRIMARY KEY,
    created_at  TIMESTAMP,
    signal_date DATE,                    -- date signal was generated
    symbol      VARCHAR,
    action      VARCHAR,                 -- BUY / SELL
    strategy    VARCHAR,                 -- "breakout_10d"
    raw_price   FLOAT,                   -- close price when signal fired
    target_qty  INTEGER,                 -- RiskAgent recommended quantity
    status      VARCHAR DEFAULT 'PENDING',  -- PENDING / PLACED / FILLED / REJECTED / CANCELLED
    order_id    VARCHAR,                 -- broker order ID after placement
    fill_price  FLOAT,                   -- actual fill (populated after confirmation)
    fill_qty    INTEGER,
    notes       TEXT
);
```

### 2.3 Order Placement Timing — The Close-Price Problem

**Critical issue:** The Breakout 10d strategy fires a signal when today's close > 10-day high. But you only know today's close after 3:30 PM. You cannot trade at today's close price in a live system — the market is already closed.

**Options:**

| Option | Pros | Cons |
|---|---|---|
| **Next-day market-open order** (recommended) | Simple, predictable timing | Gap risk — stock opens higher than close |
| Pre-open session limit at close price (9:00–9:15 AM) | Closer to signal price | Often doesn't fill; pre-open is illiquid |
| Next-day limit order at close + 0.5% | Controls cost | Risk of missing fast movers |
| Same-day intraday trigger (5-min chart breakout of high_10d) | No overnight gap | Requires intraday data feed, different strategy |

**Recommendation:** Place a **market order at next-day open** (9:15 AM IST). Model this honestly in backtesting by using next-day open as the execution price rather than the signal-day close — the current backtest is slightly optimistic here.

### 2.4 Order Execution Job

```
run_orders.py  (runs at 9:15 AM IST next trading day)
    1. Load all PENDING signals from signal_queue for today
    2. Check price bands — if stock hit upper circuit yesterday, skip BUY
    3. For each PENDING BUY/SELL:
        → Place order via broker API
        → Update signal_queue.status = PLACED, order_id = <broker_id>
    4. Poll for fills (broker webhook or polling loop)
    5. On fill confirmation:
        → Update signal_queue: status=FILLED, fill_price, fill_qty
        → Update internal Portfolio DB table
```

---

## Section 3 — Broker Integration

### 3.1 Broker Options (Indian market)

| Broker | API | Notes |
|---|---|---|
| **Zerodha Kite** | `kiteconnect` Python SDK | Most popular, best documentation, daily login token required |
| **Upstox** | `upstox-python` SDK | OAuth2, good REST API |
| **Angel One SmartAPI** | `smartapi-python` | Free API, totp-based auth |
| **5Paisa** | REST API | Less documented |

**Recommendation: Zerodha Kite** — largest retail broker in India, Python SDK is well-maintained, most community resources.

### 3.2 What to Build: `app/broker/` module

```
app/broker/
    __init__.py
    base.py           ← BrokerAdapter ABC (interface)
    kite_adapter.py   ← Zerodha Kite implementation
    paper_adapter.py  ← Paper trading implementation (no real orders)
    models.py         ← Order, Fill, BrokerPosition dataclasses
```

**`BrokerAdapter` interface:**
```python
class BrokerAdapter(ABC):
    def place_order(self, symbol, action, quantity, order_type="MARKET") -> str: ...
    def get_order_status(self, order_id: str) -> Order: ...
    def get_positions(self) -> List[BrokerPosition]: ...
    def get_holdings(self) -> List[BrokerPosition]: ...   # delivery (CNC) positions
    def cancel_order(self, order_id: str) -> bool: ...
```

**`PaperAdapter`** implements the same interface but writes to a local `paper_orders` table instead of calling a real API. This is the paper trading mode — run the full pipeline end-to-end with zero real capital risk.

### 3.3 NSE-Specific Constraints to Handle in `kite_adapter.py`

```python
# Order type for delivery (multi-day holding) vs intraday
product_type = "CNC"   # Cash and Carry (delivery, T+1 settlement)
# Never use "MIS" for Breakout 10d — that's intraday only, auto-squared at 3:20 PM

# Exchange
exchange = "NSE"

# Price band check before placing BUY
# If last close == upper_circuit_limit → skip, market won't accept buy orders
# NSE provides this via /instruments or /quote endpoint

# Minimum order value
# Zerodha requires minimum ₹1 order — not an issue for stocks

# DDPI for sell: required for programmatic delivery sell orders
# User must sign DDPI   Zerodha once; after that, CNC sells work via API
```

---

## Section 4 — Portfolio State Management

### 4.1 The Problem with In-Memory Portfolio

The current `Portfolio` dataclass lives only in memory during a run. For live trading:
- The process restarts every day (signal job runs once)
- Positions must survive across sessions
- Must stay in sync with broker's actual positions (which can diverge due to partial fills, manual trades, corporate actions)

### 4.2 What to Build: Portfolio DB Table + Reconciliation

**New table: `live_positions`**
```sql
CREATE TABLE live_positions (
    symbol          VARCHAR PRIMARY KEY,
    quantity        INTEGER,
    average_price   FLOAT,
    entry_date      DATE,
    strategy        VARCHAR,
    last_synced_at  TIMESTAMP
);
```

**Reconciliation logic** (run at start of each signal generation job):
```
1. Fetch actual positions from broker API (holdings/positions endpoint)
2. Load live_positions from DB
3. Compare:
   - In broker but not in DB → add to DB (manual trade or missed fill)
   - In DB but not in broker → remove from DB (manual exit or corporate action)
   - Qty mismatch → update DB, log warning
4. Use reconciled state to build Portfolio object for signal generation
```

---

## Section 5 — Risk Controls for Live Trading

The backtest RiskAgent handles per-trade sizing and ATR stops. Live trading needs additional portfolio-level controls.

### 5.1 Daily Loss Limit

```python
# In run_signals.py before placing any orders:
today_pnl = portfolio.unrealized_pnl(current_prices) + portfolio.realized_pnl_today
if today_pnl < -(INITIAL_CAPITAL * 0.02):   # -2% daily loss limit
    log.warning("Daily loss limit hit — no new BUY signals today")
    suppress_buys = True
```

### 5.2 Maximum Open Positions

Breakout 10d generated 2,361 trades over 6.5 years — about 1.5 new trades per day. At any time the strategy might want to enter 5–8 positions. Cap:
- Max 8 open positions at once (prevents concentration during false breakout clusters)
- Already partially handled by `max_pos_pct=0.10` (10 positions would use 100% capital), but an explicit count cap is cleaner

### 5.3 Stale Signal Cancellation

If a PENDING signal from yesterday wasn't placed (system was down), cancel it — the breakout condition may no longer hold. In `run_orders.py`:
```python
stale_cutoff = today - timedelta(days=1)
stale = session.query(SignalQueue).filter(
    SignalQueue.status == "PENDING",
    SignalQueue.signal_date < stale_cutoff,
).all()
for s in stale:
    s.status = "CANCELLED"
    s.notes = "Stale signal — not placed within 1 trading day"
```

---

## Section 6 — Observability

### 6.1 Result Persistence (C2 from roadmap)

**New table: `experiment_runs`**
```sql
CREATE TABLE experiment_runs (
    id           UUID PRIMARY KEY,
    run_at       TIMESTAMP,
    strategy     VARCHAR,
    period_start DATE,
    period_end   DATE,
    sharpe       FLOAT,
    total_return FLOAT,
    max_drawdown FLOAT,
    profit_factor FLOAT,
    win_rate     FLOAT,
    num_trades   INTEGER,
    params       JSONB    -- strategy + risk params as dict
);
```

This lets you compare results before/after parameter changes instead of comparing stdout logs.

### 6.2 Daily P&L Report

At end of each trading day (4:30 PM IST), generate and send:
```
Date: 2024-06-14
Open positions: 4
  RELIANCE   +3.2% (entry 2024-06-10, hold 4d, 1.1 ATR from stop)
  TITAN      +1.1% (entry 2024-06-12, hold 2d, 1.8 ATR from stop)
  AXISBANK   -0.8% (entry 2024-06-13, hold 1d, 2.0 ATR from stop — AT STOP)
  INFY       +0.4% (entry 2024-06-11, hold 3d, 1.5 ATR from stop)

Today's fills:
  HDFCBANK BUY  100 @ 1623.50  (signal: breakout above 1619.00)
  WIPRO    SELL  80 @ 482.10   (signal: close < SMA_10, P&L: +₹1,840)

Day P&L: +₹3,240  |  MTD: +₹12,450  |  Equity: ₹1,12,450
```

Send via Telegram bot (`python-telegram-bot`) — simplest notification channel for personal trading.

### 6.3 Monitoring Checklist

Before considering live (non-paper) deployment, all of these must be green:

- [ ] Paper trading ran for ≥ 30 trading days with no crashes
- [ ] Signal counts match backtest frequency (≈1.5 BUY signals/day on average)
- [ ] Position reconciliation passes every day (no phantom positions)
- [ ] Daily P&L report delivered successfully every session
- [ ] At least one manual SELL order successfully executed via API
- [ ] Daily loss limit circuit breaker tested (manually trigger it in paper mode)
- [ ] System handles NSE holiday correctly (no signal job crash)

---

## Implementation Order

This is the minimum path from current state to paper trading live:

| Step | What to build | Where |
|---|---|---|
| 1 | `NSECalendar` with 2024–2025 holiday list | `app/data/calendar.py` |
| 2 | `BreezeProvider` (or keep yfinance initially) | `app/data/providers/breeze_provider.py` |
| 3 | `signal_queue` + `live_positions` + `experiment_runs` DB tables | migration in `app/core/database.py` |
| 4 | `PaperAdapter` — fake broker that writes to DB | `app/broker/paper_adapter.py` |
| 5 | `run_signals.py` — daily signal job, outputs to `signal_queue` | project root |
| 6 | `run_orders.py` — reads `signal_queue`, calls `PaperAdapter` | project root |
| 7 | Daily P&L report (Telegram or email) | `app/reporting/daily_report.py` |
| 8 | Schedule both scripts via `cron` or `APScheduler` | |
| 9 | Run paper trading for 30 days, validate | — |
| 10 | Swap `PaperAdapter` → `KiteAdapter`, go live with small capital | `app/broker/kite_adapter.py` |

---

## Backtest Accuracy Improvements Needed Before Live

Two things in the current backtest give Breakout 10d an unrealistic edge that will hurt you in live trading:

**1. Execution price is today's close, not next-day open**

The signal fires after close. Real execution is next-day open. Indian stocks can gap 1–3% overnight on news. Fix: in `BacktestEngine`, for BUY signals, use next day's `open` price as execution price (not `close`). This will reduce the 167% return somewhat but give you a realistic estimate.

**2. No volume constraint on position size**

The volatility-sized position might want to buy ₹20,000 of a stock that trades ₹5 lakh/day volume — that's 4% of daily volume, causing significant market impact (much more than the 0.05% slippage modelled). Add a constraint:

```python
# In RiskAgent._size_position():
max_adv_qty = int((adv_20 * 0.01) / price)   # limit to 1% of 20-day avg daily volume
quantity = min(quantity, max_adv_qty)
```

`adv_20` (20-day average daily volume × price = daily notional) is already computed in `DynamicUniverseAgent` — expose it through `MarketState.indicators["adv_notional"]`.
