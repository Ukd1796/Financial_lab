# Paper Trade Cron Design — Issues & Proposed Architecture

## What Happens Today (Current Flow)

### When a user starts paper trading (frontend)

```
User clicks "Start Paper Trading"
  → POST /api/paper-trade/start  { strategy_id: "31a16bed-...", starting_capital: 10000 }
      → backend writes SQLite paper_sessions row
  → frontend writes Supabase B paper_trade_sessions row (with real user_id)
  → returns { session_id: "pt_abc123", start_date, unlock_live_date }
```

At this point the session exists in two places (SQLite + Supabase B), but **no signals are running yet**. Nothing happens automatically — the cron job has to run at 3:35 PM IST to generate signals.

### What the cron job does (`api/run_paper_signals.py`)

```
3:35 PM IST daily cron
  → reads ONE paper_sessions row from SQLite (most recent)
  → looks up strategy config from SQLite strategies table
  → generates signals → writes to Supabase B signal_queue
  → sends email summary
```

---

## Critical Issues in the Current Design

### Issue 1 — Wrong database for strategy config (breaks today)

`api/run_paper_signals.py` line 126:
```python
"SELECT config_json FROM strategies WHERE id = ?", (strategy_id,)
```

The `strategies` SQLite table is populated by the old `POST /api/strategies` endpoint,
which the frontend **never calls**. The frontend saves strategies directly to Supabase B
`user_strategies` with UUID ids like `31a16bed-...`.

**Result:** `_load_strategy_config()` always returns `None` for every frontend-created strategy.
The script hits `sys.exit(1)` immediately after finding the session.

**Fix:** Read from Supabase B `user_strategies` where `id = strategy_id` using SQLAlchemy.

---

### Issue 2 — Single-session assumption (breaks multi-user)

The script reads only the most-recent `paper_sessions` row:
```python
"SELECT * FROM paper_sessions ORDER BY created_at DESC LIMIT 1"
```

If 5 users have active paper sessions, only the most recently created one gets signals.
All others are silently ignored.

**Fix:** Read ALL `active` sessions from Supabase B `paper_trade_sessions`, loop over each.

---

### Issue 3 — Signals are not tagged by session

`signal_queue` has no `session_id` column. All signals go into one shared pool.
When `GET /paper-trade/{session_id}/signals` is called, it returns signals for `date.today()`
regardless of which strategy the session is running.

If two users have different strategies (one BUY-heavy, one SELL-heavy), both see the merged
signal list instead of their own.

**Fix:** Add a nullable `session_id` column to `signal_queue`. Each session's signals are
filtered by `session_id` when reading for the dashboard.

---

### Issue 4 — `run_orders.py` doesn't load `.env`

`run_orders.py` has no `load_dotenv()` call. After the DATABASE_URL move from hardcoded
fallback to `.env`, running it standalone (outside a shell that already sourced `.env`)
will raise `RuntimeError: DATABASE_URL is not set`.

**Fix:** Add `load_dotenv()` at the top of `run_orders.py`.

---

### Issue 5 — No paper-specific orders script

`run_orders.py` is shared between live and paper trading, reads the single global signal queue,
and processes fills for all sessions at once. It doesn't know which session each signal belongs to.

Once signals are tagged by `session_id` (Issue 3 fix), orders need to be processed per session
so each user's position state stays isolated.

---

### Issue 6 — Railway cron can't be auto-updated

Railway cron jobs are static YAML entries. When a new user starts a paper session the cron
already exists — it just needs to pick up the new session from the DB on the next run.
No Railway config change is needed IF the script loops over all active sessions.

**The misunderstanding:** you don't need to add a new cron job per user. One cron job loops
over all active sessions in the DB. The "auto-update" is the DB row, not the Railway config.

---

## Proposed Architecture

### Data model change — tag signals by session

```sql
-- Run in Supabase B SQL editor
ALTER TABLE public.signal_queue
    ADD COLUMN IF NOT EXISTS session_id text;

CREATE INDEX IF NOT EXISTS idx_signal_queue_session
    ON public.signal_queue (session_id, signal_date);
```

Also update the SQLAlchemy model:
```python
# app/data/models.py — SignalQueue
session_id = Column(String, nullable=True)   # paper session that generated this signal
```

---

### Fixed Railway cron schedule (no changes needed to Railway config)

IST is UTC+5:30. Convert both jobs:

| Job | IST time | UTC time | Railway cron expression |
|---|---|---|---|
| `api/run_paper_signals.py` | 3:35 PM | 10:05 UTC | `5 10 * * 1-5` |
| `api/run_paper_orders.py` | 9:15 AM | 3:45 UTC | `45 3 * * 1-5` |

In Railway dashboard → your service → **Cron Jobs** → Add two entries:

```
# Signals job — runs every weekday at 3:35 PM IST (10:05 UTC)
# Command:
python -m api.run_paper_signals

# Orders job — runs every weekday at 9:15 AM IST (3:45 UTC)
# Command:
python -m api.run_paper_orders
```

Set the cron schedule field to `5 10 * * 1-5` and `45 3 * * 1-5` respectively.
The working directory must be `/app` (or wherever Railway deploys your repo root).

Both scripts discover active sessions from Supabase B at runtime. Adding/removing user
sessions updates the DB, not the Railway config.

---

### Rewritten `api/run_paper_signals.py` — key changes

```python
def _load_active_sessions() -> list[dict]:
    """Read ALL active paper sessions from Supabase B."""
    db = SessionLocal()
    try:
        rows = db.execute(text(
            "SELECT session_id, strategy_id, strategy_name, starting_capital "
            "FROM paper_trade_sessions WHERE status = 'active'"
        )).fetchall()
        return [dict(r._mapping) for r in rows]
    finally:
        db.close()


def _load_strategy_config(strategy_id: str) -> dict | None:
    """Read strategy config from Supabase B user_strategies (not SQLite)."""
    db = SessionLocal()
    try:
        row = db.execute(text(
            "SELECT name, universe, strategies, risk FROM user_strategies WHERE id = :sid"
        ), {"sid": strategy_id}).fetchone()
        if row is None:
            return None
        return {
            "name":       row.name,
            "universe":   row.universe,
            "strategies": row.strategies,   # already parsed JSONB
            "risk":       row.risk,
        }
    finally:
        db.close()


def main():
    sessions = _load_active_sessions()
    if not sessions:
        print("No active paper sessions — exiting.")
        sys.exit(0)

    print(f"Active sessions: {len(sessions)}")

    # Preload market data once (shared across all sessions for efficiency)
    # ... fetch OHLC, build universe, compute market states, regime snapshot ...

    for session in sessions:
        config = _load_strategy_config(session["strategy_id"])
        if config is None:
            print(f"  [SKIP] {session['session_id']} — strategy config not found")
            continue

        # Extract enabled strategies + risk params from config
        # Generate signals tagged with session["session_id"]
        # Write to signal_queue with session_id column
        _generate_and_write_signals(session, config, daily_symbol_states, regime_snapshot)
```

Key principle: **market data loading happens once per run, signal generation loops per session**.
If 5 users have active sessions, you fetch OHLC once but run the strategy + risk logic 5 times.

---

### New `api/run_paper_orders.py` — per-session order processing

```python
def main():
    sessions = _load_active_sessions()   # same helper as above

    for session in sessions:
        pending = _get_pending_signals(session["session_id"], prev_trading_day)
        if not pending:
            continue

        for signal in pending:
            # Attempt fill via PaperAdapter
            # Update signal_queue status to FILLED / CANCELLED
            # Update live_positions tagged with session_id
            pass

        # Email per-session fill summary
```

---

### How Railway auto-picks up new sessions

```
User starts paper trade          Railway cron (already scheduled)
      │                                    │
      ▼                                    │
Supabase B:                         3:35 PM IST
paper_trade_sessions                       │
  { session_id: "pt_xyz",                  ▼
    status: "active",           api/run_paper_signals.py
    strategy_id: "uuid-...",      SELECT * FROM paper_trade_sessions
    starting_capital: 50000 }       WHERE status = 'active'
                                         │
                                   finds pt_xyz  ← NEW session auto-discovered
                                         │
                                   generates signals for pt_xyz
                                   writes to signal_queue(session_id='pt_xyz')
```

No Railway config change, no redeployment. The DB row IS the registration.

---

## Implementation Checklist

| Step | Status | What | Where |
|---|---|---|---|
| 1 | ✅ Done | Add `session_id` column to `signal_queue` in Supabase B | Executed via SQLAlchemy |
| 2 | ✅ Done | Add `session_id = Column(String, nullable=True)` to `SignalQueue` model | `app/data/models.py` |
| 3 | ✅ Done | Rewrite `_load_active_sessions()` to read from Supabase B | `api/run_paper_signals.py` |
| 4 | ✅ Done | Rewrite `_load_strategy_config()` to read from Supabase B `user_strategies` | `api/run_paper_signals.py` |
| 5 | ✅ Done | Loop over sessions in `main()`, tag written signals with `session_id` | `api/run_paper_signals.py` |
| 6 | ✅ Done | Create `api/run_paper_orders.py` (per-session version of `run_orders.py`) | `api/run_paper_orders.py` |
| 7 | ✅ Done | Add `load_dotenv()` to `run_orders.py` | `run_orders.py` |
| 8 | ✅ Done | Update signal/dashboard endpoints to filter by `session_id` | `api/routers/paper_trade.py` |
| 9 | ⏳ TODO | Set Railway cron jobs (see cron schedule table above) | Railway dashboard |

---

## What `run_signals.py` and `run_orders.py` remain for

These are your **personal live trading scripts** — fixed params, all 5 strategies, your own
capital. They're not user-facing and do not need to support multiple sessions. Keep them as-is.

The `api/` versions are the multi-user, config-driven equivalents:

| Script | Purpose | Config source |
|---|---|---|
| `run_signals.py` | Personal live trading | Hardcoded in script |
| `run_orders.py` | Personal live order fills | Hardcoded in script |
| `api/run_paper_signals.py` | All active paper sessions | Supabase B `user_strategies` |
| `api/run_paper_orders.py` | All active paper session fills | Supabase B `paper_trade_sessions` |
