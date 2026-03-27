---
name: FastAPI layer — api/ directory
description: FastAPI endpoints built in api/ to serve QuantCanvas UI from Financial Lab engine
type: project
---

FastAPI layer lives entirely in `api/` directory — never touches existing app/ code.
Run with: `uvicorn api.main:app --reload --port 8000`

**Phase 1 (built):**
- GET /api/market/regime — RegimeContextAgent + DynamicUniverseAgent, 1h cache
- GET /api/market/universe-stats — active stock counts per universe tier
- GET /api/market/strategy-weights — rule-based weights (no LLM), per regime
- POST/GET /api/strategies — SQLite-backed strategy config persistence
- POST /api/backtest/run → GET /api/backtest/{run_id} — async backtest via thread pool

**Phase 2 (built):**
- POST /api/paper-trade/start — creates SQLite session record
- GET /api/paper-trade/{id}/dashboard|positions|signals|report/weekly — reads from Supabase signal_queue + live_positions

**State:**
- `api_state.db` (SQLite, auto-created) — strategies, backtest runs, paper sessions
- Supabase (existing) — market_ohlc, signal_queue, live_positions

**Why:** ANTHROPIC_API_KEY → Claude claude-sonnet-4-6 for ai_narrative; falls back to templated text if not set.

**How to apply:** When adding new endpoints, add router in api/routers/, mount in api/main.py. Never modify app/ code.
