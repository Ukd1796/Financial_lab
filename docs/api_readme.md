# Financial Lab — FastAPI Layer

This document covers all API endpoints exposed by `api/main.py`.
Base URL: **`http://localhost:8000/api`**

---

## Quick Start

```bash
# Install API dependencies (in addition to existing requirements.txt)
pip install -r api/requirements.txt

# Run the server
uvicorn api.main:app --reload --port 8000
```

Interactive docs: http://localhost:8000/docs

---

## Architecture

```
api/
├── main.py                  # FastAPI app, CORS config, router mounts
├── requirements.txt         # fastapi, uvicorn, anthropic
├── routers/
│   ├── market.py            # GET /api/market/*
│   ├── strategies.py        # POST/GET /api/strategies
│   ├── backtest.py          # POST/GET /api/backtest
│   └── paper_trade.py       # /api/paper-trade/* (Phase 2)
├── models/
│   └── request.py           # Pydantic request schemas
├── services/
│   ├── regime_service.py    # DynamicUniverseAgent + RegimeContextAgent
│   ├── backtest_service.py  # BacktestEngine orchestration
│   └── narrative_service.py # Claude API narrative generation
└── db/
    └── store.py             # SQLite store (strategies, runs, sessions)
```

**State stores:**
- **Supabase PostgreSQL** (existing) — `market_ohlc`, `signal_queue`, `live_positions`
- **`api_state.db`** (SQLite, auto-created) — saved strategies, backtest runs, paper sessions

---

## Phase 1 — Core Endpoints

### `GET /api/market/regime`

Current broad market regime from `RegimeContextAgent`. Results are cached for 60 minutes.

**Response:**
```json
{
  "regime": "BULL_CONFIRMED",
  "breadth_pct_uptrend": 72.4,
  "breadth_pct_downtrend": 18.1,
  "active_stocks": 74,
  "atr_level": "normal",
  "as_of_date": "2026-03-27",
  "note": "Breadth improving for 3+ consecutive days."
}
```

**Regime values:** `BULL_CONFIRMED` | `BULL_EARLY` | `BULL_WATCH` | `SIDEWAYS_CHOPPY` | `TRANSITION_UP` | `BEAR_WATCH` | `BEAR_TRANSITION` | `BEAR_CONFIRMED`

---

### `GET /api/market/universe-stats`

Active stock count (passed `DynamicUniverseAgent` scoring) per universe tier.

**Response:**
```json
{
  "nifty50":  { "total": 50,  "active": 38, "as_of_date": "2026-03-27" },
  "nifty100": { "total": 100, "active": 74, "as_of_date": "2026-03-27" },
  "broad150": { "total": 150, "active": 80, "as_of_date": "2026-03-27" }
}
```

---

### `GET /api/market/strategy-weights`

Rule-based capital weights per strategy for the current (or overridden) regime.

**Query params:** `regime` (optional)

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
  "rationale": "Broad uptrend confirmed. Trend-follow and Breakout dominate..."
}
```

---

### `POST /api/strategies`

Save a strategy configuration. Returns a server-side ID.

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

**Response `201`:**
```json
{ "id": "strat_a1b2c3", "created_at": "2026-03-27T10:30:00Z" }
```

---

### `GET /api/strategies/{id}`

Load a previously saved strategy config.

**Response:** Same shape as the `POST /api/strategies` request body, plus `id` and `created_at`.

---

### `POST /api/backtest/run`

Start a backtest in the background. Returns `run_id` immediately (HTTP 202).

**Request body (by strategy ID):**
```json
{ "strategy_id": "strat_a1b2c3" }
```

**Request body (inline config):**
```json
{ "config": { ...same as POST /api/strategies body... } }
```

**Response `202`:**
```json
{
  "run_id": "bt_x9y8z7",
  "status": "queued",
  "estimated_seconds": 20
}
```

The backtest runs 2019–present using `BacktestEngine` with `MultiStrategyRouter`.
Benchmark is Nifty 50 (`^NSEI` via yfinance).

---

### `GET /api/backtest/{run_id}`

Poll for backtest status. The UI calls this every 2 seconds.

**While running:**
```json
{ "run_id": "bt_x9y8z7", "status": "running", "progress_pct": 42 }
```

**On completion:**
```json
{
  "run_id": "bt_x9y8z7",
  "status": "complete",
  "strategy_id": "strat_a1b2c3",
  "config_snapshot": { ... },

  "summary": {
    "total_return_pct":    94.3,
    "max_drawdown_pct":   -18.7,
    "sharpe_ratio":         1.14,
    "win_rate_pct":        58.0,
    "total_trades":        284,
    "benchmark_return_pct": 67.2,
    "benchmark_max_dd_pct": -38.1,
    "benchmark_sharpe":     0.82
  },

  "equity_curve": [
    { "date": "2019-01-31", "portfolio": 1000000, "benchmark": 1000000 }
  ],

  "period_breakdown": [
    {
      "period": "Bull Run",
      "start_date": "2019-01-01",
      "end_date": "2020-02-01",
      "regime": "BULL_CONFIRMED",
      "return_pct": 32.1,
      "max_dd_pct": -8.2,
      "sharpe": 1.41,
      "vs_nifty_pct": 12.3
    }
  ],

  "trade_log": [
    {
      "date": "2024-11-12",
      "symbol": "RELIANCE",
      "action": "SELL",
      "strategy": "multi-strategy",
      "entry_price": 2480,
      "exit_price": 2620,
      "pnl_pct": 5.6,
      "regime_at_entry": "",
      "reason": ""
    }
  ],

  "ai_narrative": {
    "what_worked": "...",
    "what_to_watch": "...",
    "bear_behavior": "...",
    "improvement_tip": "..."
  }
}
```

---

## Phase 2 — Paper Trading

Signal generation still runs via `run_signals.py` (cron at 3:35 PM IST).
These endpoints expose session state and live data from the existing Supabase tables.

---

### `POST /api/paper-trade/start`

Create a paper trading session for a saved strategy.

**Headers:** `X-Session-Token: <token>` (optional; for future multi-user isolation)

**Request body:**
```json
{ "strategy_id": "strat_a1b2c3", "starting_capital": 1000000 }
```

**Response `201`:**
```json
{
  "session_id":       "pt_abc123",
  "start_date":       "2026-03-27",
  "unlock_live_date": "2026-05-10"
}
```

---

### `GET /api/paper-trade/{session_id}/dashboard`

Everything the dashboard needs in one call: portfolio value, open positions, today's signals, regime, day count.

---

### `GET /api/paper-trade/{session_id}/positions`

Open positions with days held and strategy source. Unrealised P&L field returns `null` — supply at the UI layer using a live price feed.

---

### `GET /api/paper-trade/{session_id}/signals`

Today's generated signals from `signal_queue` (BUY / SELL / PENDING / FILLED / CANCELLED).

---

### `GET /api/paper-trade/{session_id}/report/weekly`

Weekly health report: total signals, filled buys/sells, pending signals, current regime, notable completed trades.

---

## Strategy ID Mapping

| UI `strategy.id`  | Internal name | Financial Lab Class             |
|-------------------|---------------|---------------------------------|
| `trend-follow`    | `DualMA`      | `DualMovingAverageStrategy`     |
| `breakout`        | `Breakout`    | `BreakoutMomentumStrategy`      |
| `quiet-breakout`  | `QuietBrk`    | `QuietBreakoutStrategy`         |
| `trend-pullback`  | `TrendPB`     | `TrendPullbackStrategy`         |
| `mean-reversion`  | `RSI-MR`      | `RSIMeanReversionStrategy`      |

---

## Environment Variables

| Variable           | Required | Description                                      |
|--------------------|----------|--------------------------------------------------|
| `DATABASE_URL`     | Yes      | Supabase PostgreSQL URL (already in `.env`)      |
| `ANTHROPIC_API_KEY`| No       | Claude API key for `ai_narrative` generation     |
| `ALLOWED_ORIGINS`  | No       | Comma-separated extra CORS origins               |

If `ANTHROPIC_API_KEY` is not set the narrative falls back to a templated response.

---

## Notes

- **Backtest duration:** A full 2019–present run takes 15–45 seconds depending on universe size.
- **Regime cache:** `/api/market/regime` and `/api/market/universe-stats` share a 60-minute in-memory cache. Restart the server to force a refresh.
- **Paper trade signals:** Populated by `run_signals.py` which must run as a cron job. The API endpoints are read-only views over `signal_queue` and `live_positions`.
- **No auth on Phase 1:** Phase 2 paper trade endpoints accept an optional `X-Session-Token` header for future multi-user isolation.
