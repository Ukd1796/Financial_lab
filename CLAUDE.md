# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Run the API locally
uvicorn api.main:app --reload --port 8000

# Run a cron script manually (from project root)
finance/bin/python3 -m api.run_paper_signals
finance/bin/python3 -m api.run_paper_orders
finance/bin/python3 -m api.run_daily_pnl

# Run a backtest
finance/bin/python3 run_backtest.py

# Install dependencies into the venv
finance/bin/pip install -r requirements.txt

# Deploy to Railway
railway up --detach
```

Always use `finance/bin/python3` (the project venv), not the system python.

## Architecture

### Two databases, two concerns

| Store | What | Where |
|---|---|---|
| **Supabase B** (`dbptdhnamqtfwvupscia`) | Market data, signals, sessions, positions, push tokens | `app/core/database.py` → `SessionLocal` (SQLAlchemy) |
| **SQLite** (`api_state.db`) | Strategy configs, backtest runs, LLM weight decisions | `api/db/store.py` (lightweight KV-style) |

The FastAPI app is deployed on Railway. Cron jobs run locally (macOS crontab) against the same Supabase B. The frontend (React web + tactiq-mobile) writes `paper_trade_sessions` and `user_strategies` directly via the Supabase JS client with the user's JWT.

### Request flow

```
Mobile / Web → Railway FastAPI (api/main.py)
                  ├─ api/routers/          # thin HTTP layer
                  ├─ api/services/         # business logic (backtest, regime, narrative, weights)
                  └─ app/                  # domain logic (shared with cron scripts)
                        ├─ strategy/       # 5 strategies: DualMA, Breakout, QuietBrk, TrendPB, RSI-MR
                        ├─ meta/           # AdaptiveStrategySelector (GPT-4o-mini), RegimeContextAgent
                        ├─ risk/           # RiskAgent: position sizing, breadth CB, cash gate
                        ├─ universe/       # DynamicUniverseAgent + union filters
                        ├─ data/           # MarketDataRepository, YFinanceProvider, NSECalendar
                        └─ core/           # database.py, notify.py (email), push.py (Expo)
```

### Paper trading lifecycle

1. **Frontend** creates a session row in `paper_trade_sessions` (Supabase JS client).
2. **`api/run_paper_signals.py`** (10:35 UTC cron): loads all active sessions, fetches EOD data, runs each session through `MultiStrategyRouter → RiskAgent → sequential cash gate`, writes `PENDING` rows to `signal_queue`.
3. **`api/run_paper_orders.py`** (10:45 UTC cron): processes yesterday's `PENDING` signals, fills them at next-day open via `PaperAdapter`, updates status to `FILLED`.
4. **`api/run_daily_pnl.py`** (10:15 UTC cron): reads `FILLED` signals, prices from `market_ohlc`, sends push notification with P&L summary.
5. **API endpoints** (`/api/paper-trade/{session_id}/...`) reconstruct portfolio state on-demand from `FILLED` rows — there is no authoritative positions table.

### Strategy selection & weighting

`MultiStrategyRouter` composes strategies with weights from `AdaptiveStrategySelector`. The selector rebalances every 5 days using GPT-4o-mini based on a regime snapshot. Each strategy has an `_ALLOWED_REGIMES` allowlist — signals outside the allowed regime are discarded. `RiskAgent` then applies: max position %, ATR-based sizing, breadth circuit-breaker (pauses BUY when >N% stocks in downtrend), and a sequential cash gate.

### AI narrative pattern

`api/services/narrative_service.py` is the existing pattern for Claude-powered text generation: call `anthropic.Anthropic`, parse labelled paragraph output, fall back to templates if the key is missing. Follow this pattern for any new AI-generated content.

### Notifications

`app/core/push.py` — Expo push helper. Use `send_push_to_session_user(session_id, title, body, data)` from cron scripts; it joins `push_tokens` → `paper_trade_sessions` on `user_id`. `app/core/notify.py` handles email (Resend API → Gmail SMTP fallback).

### Key environment variables

| Var | Purpose |
|---|---|
| `DATABASE_URL` | Supabase B transaction pooler (port 6543 for API, use 5432 for DDL) |
| `OPENAI_API_KEY` | GPT-4o-mini for `AdaptiveStrategySelector`, `narrative_service`, and `feedback_service` |
| `RESEND_API_KEY` | Email via Resend (preferred over SMTP on Railway) |
| `SUPPRESS_NEW_BUYS` | Set to `1` to block all new BUY signals (manual kill switch) |
