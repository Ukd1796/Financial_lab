# api/services/regime_service.py
#
# Wraps DynamicUniverseAgent + RegimeContextAgent to compute the current
# market regime and universe stats.
#
# Results are cached per-day (regime rarely changes intra-day) and refreshed
# at most once every CACHE_TTL_SECONDS seconds within the same day.

import time
from datetime import datetime, timedelta
from typing import Any

from app.backtest.observer import MarketObserverAgent
from app.data.repository import MarketDataRepository
from app.meta.regime_context_agent import RegimeContextAgent
from app.universe.dynamic_agent import DynamicUniverseAgent
from app.universe.filters import (
    BreakoutUniverseFilter,
    DualMAUniverseFilter,
    MeanReversionUniverseFilter,
    PullbackUniverseFilter,
    UnionUniverseFilter,
)

# ---------------------------------------------------------------------------
# Universe symbol lists (mirrors run_experiments.py)
# ---------------------------------------------------------------------------
from run_experiments import NIFTY_50, NIFTY_NEXT_50, NIFTY_MIDCAP_50

NIFTY_100 = NIFTY_50 + NIFTY_NEXT_50
BROAD_UNIVERSE = NIFTY_50 + NIFTY_NEXT_50 + NIFTY_MIDCAP_50

UNIVERSE_SYMBOLS = {
    "nifty50":  NIFTY_50,
    "nifty100": NIFTY_100,
    "broad150": BROAD_UNIVERSE,
}

CACHE_TTL_SECONDS = 3600  # 1 hour

_cache: dict[str, Any] = {}
_cache_ts: float = 0.0


def _is_stale() -> bool:
    return (time.time() - _cache_ts) > CACHE_TTL_SECONDS


def _build_snapshot() -> dict:
    """
    Run DynamicUniverseAgent → RegimeContextAgent for the latest available date.
    Returns the enriched regime snapshot dict.
    """
    today_dt = datetime.combine(datetime.utcnow().date(), datetime.min.time())
    start_dt = today_dt - timedelta(days=300)

    repository = MarketDataRepository()

    dynamic_agent = DynamicUniverseAgent(
        repository=repository,
        symbols=BROAD_UNIVERSE,
        top_n=80,
    )
    dynamic_agent.preload(start_dt, today_dt)

    union_filter = UnionUniverseFilter([
        BreakoutUniverseFilter(top_n=20),
        BreakoutUniverseFilter(vol_threshold=1.2, return_threshold=0.008, top_n=20),
        PullbackUniverseFilter(top_n=20),
        MeanReversionUniverseFilter(top_n=20),
        DualMAUniverseFilter(max_cross_age=5, top_n=30),
    ])

    broad_candidates = dynamic_agent.select_candidates(today_dt)
    active_symbols   = union_filter.select_symbols(broad_candidates)

    observer = MarketObserverAgent(repository)
    for symbol in active_symbols:
        try:
            observer.preload(symbol, start_dt, today_dt)
        except Exception:
            pass

    daily_symbol_states = {}
    for symbol in active_symbols:
        state = observer.run_for_day(symbol, today_dt)
        if state:
            daily_symbol_states[symbol] = state

    if not daily_symbol_states:
        raise RuntimeError("No market states computed — DB may be missing recent data.")

    rca      = RegimeContextAgent(dynamic_agent)
    snapshot = rca.build_snapshot(daily_symbol_states, today_dt)

    # Attach active symbol counts per universe tier
    all_candidates  = dynamic_agent.select_candidates(today_dt)
    candidate_syms  = {c.symbol for c in all_candidates}

    universe_active = {
        "nifty50": {
            "total": len(NIFTY_50),
            "active": len(candidate_syms & set(NIFTY_50)),
        },
        "nifty100": {
            "total": len(NIFTY_100),
            "active": len(candidate_syms & set(NIFTY_100)),
        },
        "broad150": {
            "total": len(BROAD_UNIVERSE),
            "active": len(candidate_syms & set(BROAD_UNIVERSE)),
        },
    }

    return {
        "snapshot":       snapshot,
        "universe_active": universe_active,
        "as_of_date":     today_dt.strftime("%Y-%m-%d"),
    }


def _maybe_refresh() -> None:
    global _cache, _cache_ts
    if _is_stale():
        data       = _build_snapshot()
        _cache     = data
        _cache_ts  = time.time()


def _atr_level(avg_atr_pct: float) -> str:
    if avg_atr_pct < 0.015:
        return "low"
    if avg_atr_pct <= 0.022:
        return "normal"
    return "high"


def _note(snapshot: dict) -> str:
    trend = snapshot.get("trend", "STABLE")
    if trend == "IMPROVING":
        return "Breadth improving for 3+ consecutive days."
    if trend == "DETERIORATING":
        return "Breadth deteriorating — downtrend expanding."
    return "Breadth stable — no significant directional shift."


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def get_regime() -> dict:
    """Return current regime for GET /api/market/regime."""
    _maybe_refresh()
    snap = _cache["snapshot"]
    return {
        "regime":                snap.get("broad_regime", "SIDEWAYS_CHOPPY"),
        "breadth_pct_uptrend":   round(snap.get("pct_uptrend", 0) * 100, 1),
        "breadth_pct_downtrend": round(snap.get("pct_downtrend", 0) * 100, 1),
        "active_stocks":         snap.get("universe_size", 0),
        "atr_level":             _atr_level(snap.get("avg_atr_pct", 0.015)),
        "as_of_date":            _cache["as_of_date"],
        "note":                  _note(snap),
    }


def get_universe_stats() -> dict:
    """Return active stock counts for GET /api/market/universe-stats."""
    _maybe_refresh()
    as_of = _cache["as_of_date"]
    return {
        universe: {**counts, "as_of_date": as_of}
        for universe, counts in _cache["universe_active"].items()
    }


def get_raw_snapshot() -> dict:
    """Return the full regime snapshot dict (used by backtest service)."""
    _maybe_refresh()
    return _cache["snapshot"]
