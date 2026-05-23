# app/data/local_cache.py
#
# Local SQLite cache for market OHLC data — eliminates repeated Supabase
# pulls during heavy backtesting iteration.
#
# Workflow:
#   1. Run scripts/cache_market_data_locally.py ONCE to dump all symbols
#      across full history (~12 years) into data_cache/market_ohlc.sqlite.
#   2. From then on, OHLCCache.warm_all() checks this file first. If the
#      requested symbol + date range is covered locally, serves from disk
#      (~50-100× faster than Supabase). Falls back to Supabase only if
#      the local cache is missing or incomplete.
#
# Schema mirrors the production market_ohlc table (app/data/models.py) but
# uses (symbol, timestamp) as the natural primary key — we don't need the
# UUIDs that production uses for primary-key uniqueness.
#
# The cache is read-only from the engine's perspective; refreshing is a
# manual operation (re-run the sync script). This is deliberate: backtests
# should be reproducible across runs, and silent cache updates would
# defeat that.

from __future__ import annotations

import os
import sqlite3
from datetime import datetime
from typing import Iterable, Optional

from app.data.models import MarketOHLC


# Default location. Override via the `path` arg in any function below.
DEFAULT_CACHE_PATH = os.path.join("data_cache", "market_ohlc.sqlite")


# ---------------------------------------------------------------------------
# Schema
# ---------------------------------------------------------------------------
_CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS market_ohlc (
    symbol     TEXT    NOT NULL,
    timestamp  TEXT    NOT NULL,  -- ISO 8601 UTC string for sortable indexing
    open       REAL    NOT NULL,
    high       REAL    NOT NULL,
    low        REAL    NOT NULL,
    close      REAL    NOT NULL,
    volume     REAL    NOT NULL,
    PRIMARY KEY (symbol, timestamp)
);
"""

_CREATE_INDEX_SQL = """
CREATE INDEX IF NOT EXISTS idx_market_ohlc_timestamp
    ON market_ohlc(timestamp);
"""

# Pragmas tuned for bulk write + read. We don't care about durability for
# backtest data (it's a regeneratable cache) so synchronous=OFF is safe.
_TUNING_PRAGMAS = [
    "PRAGMA journal_mode = WAL;",
    "PRAGMA synchronous  = NORMAL;",
    "PRAGMA cache_size   = -262144;",  # ~256 MB page cache
    "PRAGMA temp_store   = MEMORY;",
]


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------
def cache_exists(path: str = DEFAULT_CACHE_PATH) -> bool:
    """True iff a non-empty SQLite cache exists at `path`."""
    return os.path.isfile(path) and os.path.getsize(path) > 0


def init_db(path: str = DEFAULT_CACHE_PATH) -> None:
    """Create the cache file + schema if it doesn't exist."""
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    conn = sqlite3.connect(path)
    try:
        for pragma in _TUNING_PRAGMAS:
            conn.execute(pragma)
        conn.execute(_CREATE_TABLE_SQL)
        conn.execute(_CREATE_INDEX_SQL)
        conn.commit()
    finally:
        conn.close()


def save_records(
    records_by_symbol: dict[str, list[MarketOHLC]],
    path: str = DEFAULT_CACHE_PATH,
    replace_existing: bool = False,
) -> int:
    """
    Bulk-write OHLC records to the local cache. Returns rows inserted.

    `replace_existing` — when True, deletes any existing rows for each
    symbol before writing. Useful when refreshing with longer history.
    When False (default), uses INSERT OR IGNORE so re-running on the same
    dates is a no-op (safe to re-run partial syncs).
    """
    init_db(path)
    conn = sqlite3.connect(path)
    inserted = 0
    try:
        for pragma in _TUNING_PRAGMAS:
            conn.execute(pragma)
        cur = conn.cursor()
        for symbol, records in records_by_symbol.items():
            if replace_existing:
                cur.execute("DELETE FROM market_ohlc WHERE symbol = ?", (symbol,))
            rows = [
                (
                    symbol,
                    r.timestamp.isoformat(),
                    float(r.open),
                    float(r.high),
                    float(r.low),
                    float(r.close),
                    float(r.volume),
                )
                for r in records
            ]
            if rows:
                cur.executemany(
                    "INSERT OR IGNORE INTO market_ohlc "
                    "(symbol, timestamp, open, high, low, close, volume) "
                    "VALUES (?, ?, ?, ?, ?, ?, ?)",
                    rows,
                )
                inserted += cur.rowcount if cur.rowcount > 0 else 0
        conn.commit()
    finally:
        conn.close()
    return inserted


def load_records(
    symbols: Iterable[str],
    start: datetime,
    end: datetime,
    path: str = DEFAULT_CACHE_PATH,
) -> dict[str, list[MarketOHLC]]:
    """
    Bulk-read OHLC records from the local cache. Mirrors
    MarketDataRepository.get_ohlc_bulk() return shape so it's a drop-in
    swap for callers.

    Returns dict[symbol -> sorted list[MarketOHLC]]. Symbols with no
    rows in the requested window are absent from the result (matching
    the production repo behavior).
    """
    if not cache_exists(path):
        return {}

    symbols_list = list(symbols)
    if not symbols_list:
        return {}

    conn = sqlite3.connect(path)
    try:
        for pragma in _TUNING_PRAGMAS:
            conn.execute(pragma)

        # SQLite has a 999-param default limit; chunk to stay well below.
        result: dict[str, list[MarketOHLC]] = {}
        start_iso = start.isoformat()
        end_iso   = end.isoformat()
        chunk_size = 200
        for i in range(0, len(symbols_list), chunk_size):
            chunk = symbols_list[i:i + chunk_size]
            placeholders = ",".join("?" * len(chunk))
            cur = conn.execute(
                f"SELECT symbol, timestamp, open, high, low, close, volume "
                f"FROM market_ohlc "
                f"WHERE symbol IN ({placeholders}) "
                f"  AND timestamp >= ? "
                f"  AND timestamp <= ? "
                f"ORDER BY symbol ASC, timestamp ASC",
                chunk + [start_iso, end_iso],
            )
            for row in cur.fetchall():
                sym, ts, o, h, lo, c, v = row
                m = MarketOHLC(
                    symbol=sym,
                    timestamp=datetime.fromisoformat(ts),
                    open=o, high=h, low=lo, close=c, volume=v,
                )
                result.setdefault(sym, []).append(m)
        return result
    finally:
        conn.close()


def stats(path: str = DEFAULT_CACHE_PATH) -> dict:
    """Quick inspection: total rows, unique symbols, date range."""
    if not cache_exists(path):
        return {"exists": False, "path": path}
    conn = sqlite3.connect(path)
    try:
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*), COUNT(DISTINCT symbol), "
                    "MIN(timestamp), MAX(timestamp) FROM market_ohlc")
        n_rows, n_symbols, ts_min, ts_max = cur.fetchone()
        return {
            "exists":     True,
            "path":       path,
            "rows":       n_rows,
            "symbols":    n_symbols,
            "first_date": ts_min,
            "last_date":  ts_max,
            "size_mb":    round(os.path.getsize(path) / 1024 / 1024, 2),
        }
    finally:
        conn.close()


def cached_symbols(path: str = DEFAULT_CACHE_PATH) -> set[str]:
    """Set of symbols present in the local cache."""
    if not cache_exists(path):
        return set()
    conn = sqlite3.connect(path)
    try:
        cur = conn.execute("SELECT DISTINCT symbol FROM market_ohlc")
        return {row[0] for row in cur.fetchall()}
    finally:
        conn.close()


def coverage_window(
    symbol: str,
    path: str = DEFAULT_CACHE_PATH,
) -> Optional[tuple[datetime, datetime]]:
    """Earliest + latest timestamp present for `symbol`, or None if absent."""
    if not cache_exists(path):
        return None
    conn = sqlite3.connect(path)
    try:
        cur = conn.execute(
            "SELECT MIN(timestamp), MAX(timestamp) FROM market_ohlc WHERE symbol = ?",
            (symbol,),
        )
        ts_min, ts_max = cur.fetchone()
        if ts_min is None:
            return None
        return (datetime.fromisoformat(ts_min), datetime.fromisoformat(ts_max))
    finally:
        conn.close()
