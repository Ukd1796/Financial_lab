# FastAPI Integration Spec — Financial Lab ↔ QuantCanvas UI

This document defines all FastAPI endpoints needed to replace mock data in the UI
with real Financial Lab engine output. Ordered by what to build first.

---

## Base URL

```
http://localhost:8000/api
```

CORS must allow `http://localhost:5173` (Vite dev server) and the production frontend origin.

---

## Strategy ID Mapping

The UI `strategyStore` uses these IDs — map them to Financial Lab classes:

| UI `strategy.id`  | Financial Lab Class            | File                        |
|-------------------|--------------------------------|-----------------------------|
| `trend-follow`    | `DualMovingAverageStrategy`    | `app/strategy/dual_ma.py`   |
| `breakout`        | `BreakoutMomentumStrategy`     | `app/strategy/breakout_momentum.py` |
| `quiet-breakout`  | `QuietBreakoutStrategy`        | `app/strategy/quiet_breakout.py` |
| `trend-pullback`  | `TrendPullbackStrategy`        | `app/strategy/trend_pullback.py` |
| `mean-reversion`  | `RSIMeanReversionStrategy`     | `app/strategy/rsi_mean_reversion.py` |

## Universe Mapping

| UI `universe`  | Symbol count | Financial Lab universe                       |
|----------------|-------------|----------------------------------------------|
| `nifty50`      | 50          | Nifty 50 only                                |
| `nifty100`     | 100         | Nifty 50 + Nifty Next 50                     |
| `broad150`     | 150         | Nifty 50 + Nifty Next 50 + Nifty Midcap 50  |

---

## Phase 1 — Core Endpoints (Build These First)

These are the minimum needed to make the Strategy Builder + Backtest pages live.

---

### 1. `GET /api/market/regime`

**Used by:** Strategy Builder canvas (the `Market Regime` node), Backtest Results header badge.

**What it does:** Runs `DynamicUniverseAgent` + `RegimeContextAgent` on the latest available market data and returns the current market state.

**Response:**
```json
{
  "regime": "BULL_CONFIRMED",
  "breadth_pct_uptrend": 72.4,
  "breadth_pct_downtrend": 18.1,
  "active_stocks": 74,
  "atr_level": "normal",
  "as_of_date": "2026-03-27",
  "note": "Breadth improving for 3 consecutive days."
}
```

**Regime values** (match product_readme.md exactly):
`BULL_CONFIRMED` | `BULL_EARLY` | `BULL_WATCH` | `SIDEWAYS_CHOPPY` |
`TRANSITION_UP` | `BEAR_WATCH` | `BEAR_TRANSITION` | `BEAR_CONFIRMED`

---

### 2. `GET /api/market/universe-stats`

**Used by:** Strategy Builder canvas (`Universe` node subtitle — "74 stocks active").

**What it does:** For each of the three universe options, returns how many stocks passed `DynamicUniverseAgent` scoring today (top 80 from 150, scaled proportionally for smaller universes).

**Response:**
```json
{
  "nifty50":   { "total": 50,  "active": 38, "as_of_date": "2026-03-27" },
  "nifty100":  { "total": 100, "active": 74, "as_of_date": "2026-03-27" },
  "broad150":  { "total": 150, "active": 80, "as_of_date": "2026-03-27" }
}
```

---

### 3. `GET /api/market/strategy-weights`

**Used by:** Strategy Builder canvas — each strategy node shows `AI weight: 30%`.

**What it does:** Calls `AdaptiveStrategySelector` (or a simplified rule-based version initially) with the current regime and returns recommended capital weights per strategy.

**Query params:** `regime` (optional, uses live regime if omitted)

**Response:**
```json
{
  "regime": "BULL_CONFIRMED",
  "weights": {
    "trend-follow":   0.35,
    "breakout":       0.30,
    "quiet-breakout": 0.20,
    "trend-pullback": 0.15,
    "mean-reversion": 0.00
  },
  "rationale": "In BULL_CONFIRMED, Trend Follow and Breakout dominate. Mean Reversion weight set to 0 — performs poorly in strong bull phases."
}
```

---

### 4. `POST /api/strategies`

**Used by:** Strategy Builder "Save" action (to be wired up). Returns a server-side `id` for the strategy that becomes the `:id` URL param.

**Request body:**
```json
{
  "name": "My First Strategy",
  "universe": "nifty100",
  "strategies": [
    { "id": "trend-follow",    "enabled": true,  "floor_weight": 0.10 },
    { "id": "breakout",        "enabled": true,  "floor_weight": 0.00 },
    { "id": "quiet-breakout",  "enabled": true,  "floor_weight": 0.00 },
    { "id": "trend-pullback",  "enabled": true,  "floor_weight": 0.00 },
    { "id": "mean-reversion",  "enabled": false, "floor_weight": 0.00 }
  ],
  "risk": {
    "risk_per_trade_pct": 0.5,
    "max_position_pct":   10.0,
    "pause_threshold_pct": 5.0,
    "capital_amount":     1000000
  }
}
```

**Response:**
```json
{
  "id": "strat_a1b2c3",
  "created_at": "2026-03-27T10:30:00Z"
}
```

---

### 5. `GET /api/strategies/{id}`

**Used by:** Strategy Builder page on load — rehydrates the canvas from a saved config.

**Response:** Same shape as the `POST /api/strategies` request body, plus `id` and `created_at`.

---

### 6. `POST /api/backtest/run`

**Used by:** "Backtest" button in Strategy Builder. The most important endpoint.

**What it does:** Takes a strategy config, runs `BacktestEngine` across the standard historical periods (matching `run_experiments.py` periods), and returns full results. This will take 10–30 seconds — respond with a `run_id` immediately and poll for completion.

**Request body:** Same as `POST /api/strategies` body (can pass the `id` of a saved strategy or inline config).

```json
{
  "strategy_id": "strat_a1b2c3"
}
```

or inline:

```json
{
  "config": { ... }
}
```

**Response (immediate, 202 Accepted):**
```json
{
  "run_id": "bt_x9y8z7",
  "status": "queued",
  "estimated_seconds": 15
}
```

---

### 7. `GET /api/backtest/{run_id}`

**Used by:** BacktestResultsPage polls this until `status == "complete"`.

**Response (while running):**
```json
{
  "run_id": "bt_x9y8z7",
  "status": "running",
  "progress_pct": 42
}
```

**Response (on completion):**
```json
{
  "run_id": "bt_x9y8z7",
  "status": "complete",
  "strategy_id": "strat_a1b2c3",
  "config_snapshot": { ... },

  "summary": {
    "total_return_pct":  94.3,
    "max_drawdown_pct": -18.7,
    "sharpe_ratio":      1.14,
    "win_rate_pct":     58.0,
    "total_trades":     284,
    "benchmark_return_pct": 67.2,
    "benchmark_max_dd_pct": -38.1,
    "benchmark_sharpe":      0.82
  },

  "equity_curve": [
    { "date": "2019-01-31", "portfolio": 1000000, "benchmark": 1000000 },
    { "date": "2019-02-28", "portfolio": 1021000, "benchmark": 1015000 }
  ],

  "period_breakdown": [
    {
      "period": "Bull Run",
      "start_date": "2019-01-01",
      "end_date":   "2020-02-28",
      "regime":       "BULL_CONFIRMED",
      "return_pct":    32.1,
      "max_dd_pct":   -8.2,
      "sharpe":        1.41,
      "vs_nifty_pct": 12.3
    }
  ],

  "trade_log": [
    {
      "date":      "2024-11-12",
      "symbol":    "RELIANCE",
      "action":    "BUY",
      "strategy":  "trend-follow",
      "entry_price": 2480,
      "exit_price":  2620,
      "pnl_pct":   5.6,
      "regime_at_entry": "BULL_CONFIRMED",
      "reason":    "20/50 MA crossover confirmed, sma_cross_age=2"
    }
  ],

  "ai_narrative": {
    "what_worked":    "string",
    "what_to_watch":  "string",
    "bear_behavior":  "string",
    "improvement_tip": "string"
  }
}
```

**Notes:**
- `equity_curve` — one entry per trading day (or month is fine for display). The UI uses this for the Recharts `LineChart`.
- `period_breakdown` — use the same regime periods already defined in `run_experiments.py`. Add `vs_nifty_pct` by subtracting Nifty return in the same window.
- `trade_log` — pull directly from `EvaluationAgent` trade records. The UI filters by `action` (BUY / SELL / BLOCKED).
- `ai_narrative` — generate using Claude API with the summary + period breakdown as context. Can be a simple prompt: "Given these backtest stats for an NSE equity strategy, write 4 short paragraphs: what worked, what to watch, bear behavior, one improvement tip."

---

## Phase 2 — Paper Trading (Build After Backtest Works)

These activate the PaperTradePage. Run the signal pipeline at 3:35 PM IST daily.

### `POST /api/paper-trade/start`
Activates paper trading for a strategy. Requires a completed backtest run first.
**Body:** `{ "strategy_id": "strat_a1b2c3", "starting_capital": 1000000 }`
**Response:** `{ "session_id": "pt_abc123", "start_date": "2026-03-27", "unlock_live_date": "2026-05-16" }`

### `GET /api/paper-trade/{session_id}/dashboard`
Everything the paper trade dashboard needs in one call: portfolio value, open positions, today's signals, regime, day count.

### `GET /api/paper-trade/{session_id}/positions`
Open positions with unrealised P&L, strategy source, days held.

### `GET /api/paper-trade/{session_id}/signals`
Today's generated signals (BUY / SELL / HOLD / BLOCKED) with reason.

### `GET /api/paper-trade/{session_id}/report/weekly`
Weekly health report: period return, vs backtest expectation, regime summary, notable trades.

---

## Phase 3 — Live Trading (After 30 Paper Trading Days)

### `POST /api/broker/connect`
Store Zerodha/Upstox API key (encrypted at rest). Never log or return the key.
**Body:** `{ "broker": "zerodha", "api_key": "...", "api_secret": "..." }`

### `GET /api/broker/status`
Connection health check — confirms key is valid and broker API is reachable.

### `POST /api/live-trade/start`
Unlocks only if `paper_days_completed >= 30`. Mirrors paper trade config to live execution.

### `GET /api/live-trade/{session_id}/orders`
Orders placed today through broker, with fill prices and status.

---

## Implementation Order

```
Week 1:  GET /market/regime          ← unblocks canvas live data
         GET /market/universe-stats
         GET /market/strategy-weights

Week 2:  POST /strategies            ← unblocks saving + URL-based strategy IDs
         GET  /strategies/{id}

Week 3:  POST /backtest/run          ← the big one; wire up run_experiments.py
         GET  /backtest/{run_id}     ← polling + full results response

Week 4+: Phase 2 paper trade endpoints
```

---

## Suggested Project Structure in Financial Lab

```
api/
  main.py              # FastAPI app, CORS config, router mounts
  routers/
    market.py          # /market/* endpoints
    strategies.py      # /strategies/* endpoints
    backtest.py        # /backtest/* endpoints
    paper_trade.py     # /paper-trade/* endpoints (Phase 2)
    live_trade.py      # /live-trade/* endpoints (Phase 3)
  models/
    request.py         # Pydantic request schemas
    response.py        # Pydantic response schemas
  services/
    backtest_service.py  # wraps BacktestEngine, runs in background thread/task
    regime_service.py    # wraps DynamicUniverseAgent + RegimeContextAgent
    narrative_service.py # calls Claude API to generate ai_narrative
  db/
    run_store.py         # persists backtest run_id → results (SQLite is fine)
    strategy_store.py    # persists saved strategy configs
```

Run with:
```bash
uvicorn api.main:app --reload --port 8000
```

---

## Notes

- **Backtest is slow** — use `BackgroundTasks` or `asyncio.to_thread` to run it off the event loop. The UI polls `GET /backtest/{run_id}` every 2 seconds.
- **No auth yet** — use a simple `X-Session-Token` header for the paper/live trade phases so sessions are isolated per user.
- **Benchmark data** — the equity curve needs Nifty 50 index prices for the same date range. Store these in the same SQLite DB used for OHLC data, or pull from `NSEPy`/`yfinance` once and cache.
- **ai_narrative** — don't block the backtest response on this. Generate it async and include it when ready, or add a separate `GET /backtest/{run_id}/narrative` endpoint.
