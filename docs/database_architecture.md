# Database Architecture — Current State & Consolidation Plan

## Current State: Three Databases

The system currently writes to and reads from three separate data stores. This has grown organically as the backend and frontend were built independently, and is now causing real bugs (strategy lookup 404, duplicate paper_trade_sessions rows, nil user_id fallbacks).

---

### 1. SQLite — `api_state.db` (Backend only)

| Table | Purpose | Owner |
|---|---|---|
| `strategies` | Strategy configs saved via the old `/api/strategy` save flow | API |
| `backtest_runs` | Run status, progress %, result JSON, error messages | API |
| `paper_sessions` | Paper trade sessions (SQLite-local copy) | API |
| `llm_weight_decisions` | Every LLM rebalance decision with raw response | API |
| `backtest_ab_results` | Side-by-side LLM-adaptive vs fixed-weight baseline results | API |

**Problems:**
- `strategies` is effectively a dead table — the frontend saves strategies directly to Supabase B and never calls the API save endpoint. The 404 bug is entirely caused by this divergence.
- `paper_sessions` is a duplicate of `paper_trade_sessions` in Supabase A — two rows written on every session start, neither fully trusted.
- `llm_weight_decisions` and `backtest_ab_results` are backend-only with no frontend read path.
- SQLite is a local file — doesn't survive server redeployment, can't be queried from the frontend.

---

### 2. Supabase Project A — Backend (`wtvtoiecnqcgodjohrdc`)

Connection: direct PostgreSQL via SQLAlchemy (`app/core/database.py`)

| Table | Purpose | Owner |
|---|---|---|
| `market_ohlc` | Historical OHLC price data | Backend cron |
| `live_positions` | Currently open positions | `run_paper_signals.py` |
| `signal_queue` | Generated BUY/SELL signals | `run_paper_signals.py` |
| `decision_logs` | Per-bar strategy decision logs | Backtest engine |
| `selector_state` | AdaptiveStrategySelector persistence | Adaptive selector |
| `paper_trade_sessions` | Mirror of paper session rows for API queries | API mirror write |

**Problems:**
- `paper_trade_sessions` here is a mirror of the frontend's version in Supabase B — two sources of truth with different schemas, writes can silently fail.
- Has no user auth — `user_id` fields use nil UUID fallback (`00000000-...`) when not provided.
- The frontend cannot query this project directly (different project URL/anon key).

---

### 3. Supabase Project B — Frontend (`dbptdhnamqtfwvupscia`)

Connection: Supabase JS client with anon key + RLS (`strategy-compass/src/lib/supabase.ts`)

| Table | Purpose | Owner |
|---|---|---|
| `user_strategies` | User-created strategy configs (UUID PKs, RLS-protected) | Frontend |
| `backtest_results` | Full backtest results: equity curve, trade log, AI narrative | Frontend (after API run) |
| `paper_trade_sessions` | Paper sessions visible to users, with status management | Frontend |
| *(auth tables)* | Supabase Auth: users, sessions, JWT | Supabase Auth |

**Problems:**
- The backend cannot connect to this project — different DB URL, no service role key configured.
- `paper_trade_sessions` here and the mirror in Supabase A are the same conceptual table but written by different code paths with no sync guarantee.

---

## Where Each Flow Actually Reads/Writes Today

```
Frontend saves strategy     → Supabase B: user_strategies
Frontend runs backtest      → API → SQLite: backtest_runs (status/progress)
                              API → Supabase A: decision_logs
                              Frontend → Supabase B: backtest_results (full result)
Frontend starts paper trade → API → SQLite: paper_sessions     ← writes here
                              API → Supabase A: paper_trade_sessions  ← also here (mirror)
                              Frontend → Supabase B: paper_trade_sessions  ← also here!
Frontend dashboard poll     → Supabase B: paper_trade_sessions (active session)
                              API (/dashboard) → Supabase A: live_positions, signal_queue
LLM rebalance               → SQLite: llm_weight_decisions
Paper signals cron          → Supabase A: signal_queue, live_positions
```

**Three writes just to start one paper trade session.** Two of them can fail silently.

---

## Recommended Architecture: Consolidate to One Supabase Project

### Option 1 — Migrate backend tables into Supabase B (Recommended)

Move `market_ohlc`, `live_positions`, `signal_queue`, `decision_logs`, `selector_state` into the frontend's Supabase project (`dbptdhnamqtfwvupscia`). Update `app/core/database.py` to use Supabase B's connection string.

**Result:**
- One Supabase project for everything user-facing
- Backend can read `user_strategies` directly — strategy validation works
- Backend can read/write `paper_trade_sessions` with real user UUIDs from auth
- Frontend queries one source of truth
- RLS on all tables — each user sees only their own data

**What to keep in SQLite:**
- `backtest_runs` — ephemeral job queue (status/progress during a run, not needed long-term)
- `llm_weight_decisions` — internal diagnostics, no frontend read path yet
- `backtest_ab_results` — internal diagnostics

**What to drop:**
- `paper_sessions` SQLite table — fully replaced by Supabase B's `paper_trade_sessions`
- `strategies` SQLite table — dead; frontend never writes to it

**Migration steps:**
1. Create `market_ohlc`, `live_positions`, `signal_queue`, `decision_logs`, `selector_state` in Supabase B with the same schemas
2. Add Supabase B's service role key to backend `.env` as `DATABASE_URL`
3. Remove the Supabase A mirror write from `POST /paper-trade/start`
4. Remove `paper_sessions` table from SQLite `init_db()`
5. Add `user_strategies` read path in `paper_trade.py` for strategy name lookup (now works)

---

### Option 2 — Keep two Supabase projects, add service role key for B

Keep both projects. Add Supabase B's service role key to the backend `.env` and create a second SQLAlchemy engine pointing to B. The backend uses Project A for market data and Project B for user data.

**Result:**
- No data migration needed
- Backend can now validate strategy UUIDs and write paper sessions with real user IDs
- Still two Supabase bills, two connection pools, two places to add new tables

**Not recommended** — adds operational complexity without addressing the root duplication.

---

### Option 3 — Remove backend validation entirely, rely on frontend

Keep the current three-database state but stop trying to cross-validate. The frontend already enforces "strategy must exist before paper trade" at the UI level. The backend becomes a dumb signal executor with no user-data awareness.

**Result:**
- Fastest to implement (already partially done)
- Doesn't scale — any future user-specific backend logic (per-user risk limits, position sizing, multi-session) will hit the same wall
- Acceptable short-term if migration is weeks away

---

## Recommended Action Plan (Option 1)

| Step | File(s) | Effort |
|---|---|---|
| 1. Provision Supabase B tables: `market_ohlc`, `live_positions`, `signal_queue`, `decision_logs`, `selector_state` | Supabase B SQL editor | ~30 min |
| 2. Add `SUPABASE_B_DATABASE_URL` to `.env`, update `app/core/database.py` | `app/core/database.py`, `.env` | ~10 min |
| 3. Migrate existing rows from A → B (one-time) | `psql` or Supabase dashboard | ~20 min |
| 4. Remove mirror write from `POST /paper-trade/start` | `api/routers/paper_trade.py` | ~5 min |
| 5. Drop `paper_sessions` from SQLite `init_db()` | `api/db/store.py` | ~5 min |
| 6. Re-enable strategy UUID lookup in `paper_trade.py` | `api/routers/paper_trade.py` | ~10 min |
| 7. Add RLS policies on newly migrated tables | Supabase B SQL editor | ~20 min |

Total: ~2 hours of focused work, no frontend changes required.
