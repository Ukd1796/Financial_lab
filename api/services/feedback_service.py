# api/services/feedback_service.py
#
# Generates the AI Insights response for a paper trading session.
# Aggregates signal health, position P&L, regime context, and stock news,
# then calls Claude to produce 4 user-facing narrative sections + structured metadata.
#
# Mirrors narrative_service.py: same client pattern, labelled parse, template fallback.
# Results are cached in-memory for 60 minutes — Claude call adds ~1-2s latency.

import os
import time
from datetime import date, timedelta, timezone, datetime

from sqlalchemy import text

from app.core.database import SessionLocal

# ---------------------------------------------------------------------------
# In-memory cache: {session_id: (unix_timestamp, result_dict)}
# ---------------------------------------------------------------------------
_CACHE: dict[str, tuple[float, dict]] = {}
_CACHE_TTL = 3600  # 1 hour


# ---------------------------------------------------------------------------
# Source 1 — Signal stats from signal_queue (last 7 calendar days)
# ---------------------------------------------------------------------------

def _signal_stats(session_id: str) -> dict:
    cutoff = date.today() - timedelta(days=7)
    db = SessionLocal()
    try:
        rows = db.execute(
            text(
                "SELECT status, strategy, notes, action "
                "FROM signal_queue "
                "WHERE session_id = :sid AND signal_date >= :cutoff"
            ),
            {"sid": session_id, "cutoff": cutoff},
        ).fetchall()
    finally:
        db.close()

    total = len(rows)
    filled = cancelled = pending = 0
    strategy_total: dict[str, int] = {}
    strategy_filled: dict[str, int] = {}
    block_reasons: dict[str, int] = {
        "breadth_cb":      0,
        "regime_mismatch": 0,
        "cash_gate":       0,
        "vol_too_low":     0,
        "stop_hit":        0,
    }

    for r in rows:
        s = r.status
        strat = r.strategy or "unknown"
        strategy_total[strat] = strategy_total.get(strat, 0) + 1
        if s == "FILLED":
            filled += 1
            strategy_filled[strat] = strategy_filled.get(strat, 0) + 1
        elif s in ("CANCELLED", "REJECTED"):
            cancelled += 1
        elif s in ("PENDING", "PLACED"):
            pending += 1

        notes = (r.notes or "").lower()
        if "circuit breaker" in notes:
            block_reasons["breadth_cb"] += 1
        elif "regime filter" in notes:
            block_reasons["regime_mismatch"] += 1
        elif "cash gate" in notes or "cashgate" in notes:
            block_reasons["cash_gate"] += 1
        elif "atr" in notes and "below" in notes:
            block_reasons["vol_too_low"] += 1
        elif "stop hit" in notes:
            block_reasons["stop_hit"] += 1

    blocked = sum(block_reasons.values())
    fill_rate = {
        strat: round(strategy_filled.get(strat, 0) / strategy_total[strat], 2)
        for strat in strategy_total
    }
    block_reasons = {k: v for k, v in block_reasons.items() if v > 0}

    return {
        "total": total,
        "filled": filled,
        "blocked": blocked,
        "cancelled": cancelled,
        "pending": pending,
        "fill_rate_by_strategy": fill_rate,
        "block_reasons": block_reasons,
    }


# ---------------------------------------------------------------------------
# Source 2 — Positions + P&L (reuse helpers from paper_trade router)
# ---------------------------------------------------------------------------

def _position_summary(session_id: str) -> dict:
    from api.routers.paper_trade import _get_positions_for_session, _get_latest_prices, _enrich_positions

    raw = _get_positions_for_session(session_id)
    if not raw:
        return {"positions": [], "at_risk": [], "best": None, "worst": None}

    prices = _get_latest_prices([p["symbol"] for p in raw])
    enriched = _enrich_positions(raw, prices, date.today())

    at_risk = [
        p["symbol"] for p in enriched
        if p.get("unrealised_pnl_pct") is not None and p["unrealised_pnl_pct"] < -2.0
    ]
    ranked = sorted(
        [p for p in enriched if p.get("unrealised_pnl_pct") is not None],
        key=lambda p: p["unrealised_pnl_pct"],
        reverse=True,
    )
    best  = ranked[0]  if ranked else None
    worst = ranked[-1] if ranked else None

    return {
        "positions": enriched,
        "at_risk":   at_risk,
        "best":      best,
        "worst":     worst,
    }


# ---------------------------------------------------------------------------
# Source 3 — Regime (cached by regime_service)
# ---------------------------------------------------------------------------

def _regime_context() -> dict:
    try:
        from api.services.regime_service import get_raw_snapshot
        return get_raw_snapshot()
    except Exception:
        return {}


# ---------------------------------------------------------------------------
# Source 4 — Stock news via yfinance (graceful failure)
# ---------------------------------------------------------------------------

def _fetch_news(symbols: list[str]) -> dict[str, list[str]]:
    """Return {symbol: [headline, ...]} for symbols with recent (< 48h) news."""
    if not symbols:
        return {}
    try:
        import yfinance as yf
        cutoff = time.time() - 48 * 3600
        news_map: dict[str, list[str]] = {}
        for sym in symbols[:8]:
            try:
                ticker = yf.Ticker(sym + ".NS")
                articles = ticker.news or []
                recent = [
                    a["title"] for a in articles
                    if a.get("providerPublishTime", 0) >= cutoff and a.get("title")
                ]
                if recent:
                    news_map[sym] = recent[:2]
            except Exception:
                continue
        return news_map
    except Exception:
        return {}


# ---------------------------------------------------------------------------
# Prompt builder
# ---------------------------------------------------------------------------

def _build_prompt(stats: dict, pos: dict, regime: dict, news: dict) -> str:
    lines = [""]

    # Signal activity
    if stats["total"] == 0:
        lines.append("Signal activity (last 7 days): No signals have been generated yet — the strategy is still searching for entries.\n")
    else:
        lines.append("Signal activity (last 7 days):")
        lines.append(f"  Generated: {stats['total']} | Filled: {stats['filled']} | Blocked: {stats['blocked']} | Pending: {stats['pending']}")
        if stats["block_reasons"]:
            reasons = ", ".join(
                f"{v}x {k.replace('_', ' ')}" for k, v in stats["block_reasons"].items()
            )
            lines.append(f"  Block reasons: {reasons}")
        if stats["fill_rate_by_strategy"]:
            fr = " | ".join(
                f"{s}: {int(r*100)}%" for s, r in stats["fill_rate_by_strategy"].items()
            )
            lines.append(f"  Fill rate by strategy: {fr}")
        lines.append("")

    # Positions
    positions = pos.get("positions", [])
    if not positions:
        lines.append("Open positions: None yet.\n")
    else:
        lines.append(f"Open positions ({len(positions)}):")
        for p in positions:
            pnl = p.get("unrealised_pnl_pct")
            pnl_str = f"{pnl:+.1f}%" if pnl is not None else "n/a"
            at_risk = " ← at risk" if p["symbol"] in pos.get("at_risk", []) else ""
            lines.append(f"  {p['symbol']:<14} {pnl_str} | {p['days_held']}d | {p['strategy']}{at_risk}")
        lines.append("")

    # Regime
    if regime:
        broad = regime.get("broad_regime", "UNKNOWN")
        up    = regime.get("pct_uptrend", 0)
        trend = regime.get("trend", "STABLE")
        lines.append(f"Market regime: {broad} | Breadth: {up:.0%} uptrend, trending {trend}\n")

    # News
    if news:
        lines.append("Recent stock news (< 48h):")
        for sym, headlines in news.items():
            for h in headlines:
                lines.append(f"  {sym}: \"{h}\"")
        lines.append("")

    lines.append(
        "You are a friendly financial advisor explaining a paper trading session to someone "
        "who just started investing. Use warm, plain English. Never use technical jargon — "
        "avoid words like ATR, regime, breadth, circuit breaker, volatility filter, "
        "strategy weights, fill rate, or risk parameters. Instead say things like "
        "'the market was too choppy', 'conditions weren't right', 'the system waited'.\n\n"
        "Write exactly 4 labelled sections (2-3 sentences each):\n"
        "SIGNAL_HEALTH: In plain English, what happened with trades this week — "
        "did any go through, and if some were skipped, why (in simple terms)?\n"
        "POSITION_INSIGHT: How is the portfolio doing overall? Mention any stock doing "
        "particularly well or one that needs watching. Keep it reassuring and factual.\n"
        "REGIME_CONTEXT: What is the overall market doing right now, in one simple sentence "
        "a beginner would understand? How does that affect this portfolio?\n"
        "STRATEGY_TIP: One plain-English observation or thing to keep in mind this week. "
        "No technical settings — just a human suggestion.\n\n"
        "Format exactly as:\n"
        "SIGNAL_HEALTH: <text>\n"
        "POSITION_INSIGHT: <text>\n"
        "REGIME_CONTEXT: <text>\n"
        "STRATEGY_TIP: <text>"
    )
    return "\n".join(lines)


def _parse_claude(raw: str) -> dict[str, str]:
    keys = ("SIGNAL_HEALTH", "POSITION_INSIGHT", "REGIME_CONTEXT", "STRATEGY_TIP")
    result: dict[str, str] = {}
    for line in raw.splitlines():
        for key in keys:
            if line.startswith(f"{key}:"):
                result[key] = line[len(key) + 1:].strip()
    return result


# ---------------------------------------------------------------------------
# Fallback narrative (no API key or Claude failure)
# ---------------------------------------------------------------------------

def _fallback(stats: dict, pos: dict, regime: dict) -> dict[str, str]:
    total, filled, blocked = stats["total"], stats["filled"], stats["blocked"]
    broad = regime.get("broad_regime", "")
    n_pos = len(pos.get("positions", []))
    at_risk = pos.get("at_risk", [])

    if total == 0:
        sh = ("No trades have been placed yet — the system is watching the market and will act "
              "when the right opportunity appears.")
    elif blocked > filled:
        sh = (f"{blocked} of {total} potential trades were skipped this week. "
              "The system held back because market conditions weren't quite right — "
              "this is normal and helps protect your capital during uncertain times.")
    else:
        sh = (f"{filled} trade(s) went through this week out of {total} opportunities spotted. "
              "The system is actively working within your setup.")

    if n_pos == 0:
        pi = ("No open positions yet — your capital is sitting safely in cash while the system "
              "looks for good entries.")
    elif at_risk:
        risk_word = "is" if len(at_risk) == 1 else "are"
        pi = (f"You have {n_pos} stock(s) in your portfolio. "
              f"{', '.join(at_risk)} {risk_word} down a bit right now — "
              "keep an eye on it, but the system will act if it falls further.")
    else:
        pi = f"Your {n_pos} stock(s) are holding up well. Nothing urgent to worry about right now."

    broad_display = {
        "BULL":          "mostly rising",
        "BEAR":          "broadly falling",
        "BEAR_EARLY":    "starting to pull back",
        "TRANSITION_UP": "recovering from a dip",
        "SIDEWAYS":      "moving sideways without a clear direction",
    }.get(broad, "mixed")
    rc = (f"The overall market is {broad_display} right now. "
          "This shapes which opportunities the system spots and how cautiously it acts.")

    st = ("Paper trading is a great way to get comfortable with how the system works. "
          "Check the Signals tab to see what the system spotted this week and why it acted — "
          "or didn't.")

    return {
        "SIGNAL_HEALTH":    sh,
        "POSITION_INSIGHT": pi,
        "REGIME_CONTEXT":   rc,
        "STRATEGY_TIP":     st,
    }


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

def generate_feedback(session_id: str) -> dict:
    """
    Generate or return cached AI insights for a paper trading session.
    Cached for _CACHE_TTL seconds to avoid redundant Claude calls.
    """
    now = time.time()
    if session_id in _CACHE:
        ts, cached = _CACHE[session_id]
        if now - ts < _CACHE_TTL:
            return cached

    # Collect data
    stats  = _signal_stats(session_id)
    pos    = _position_summary(session_id)
    regime = _regime_context()

    # News only for symbols we actually care about
    held_symbols    = [p["symbol"] for p in pos.get("positions", [])]
    news = _fetch_news(held_symbols)

    # OpenAI call — mirrors adaptive_selector.py pattern
    narrative: dict[str, str] = {}
    try:
        from openai import OpenAI
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not set")

        prompt  = _build_prompt(stats, pos, regime, news)
        client  = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            max_tokens=600,
            temperature=0.3,
            messages=[{"role": "user", "content": prompt}],
        )
        narrative = _parse_claude(response.choices[0].message.content or "")
    except Exception:
        narrative = _fallback(stats, pos, regime)

    best  = pos.get("best")
    worst = pos.get("worst")

    result = {
        "signal_health":    narrative.get("SIGNAL_HEALTH",    ""),
        "position_insight": narrative.get("POSITION_INSIGHT", ""),
        "regime_context":   narrative.get("REGIME_CONTEXT",   ""),
        "strategy_tip":     narrative.get("STRATEGY_TIP",     ""),
        "meta": {
            "signals_7d":            stats["total"],
            "signals_filled":        stats["filled"],
            "signals_blocked":       stats["blocked"],
            "signals_pending":       stats["pending"],
            "block_reasons":         stats["block_reasons"],
            "fill_rate_by_strategy": stats["fill_rate_by_strategy"],
            "regime":                regime.get("broad_regime", ""),
            "breadth_pct_uptrend":   round(regime.get("pct_uptrend", 0) * 100, 1),
            "positions_at_risk":     pos.get("at_risk", []),
            "best_performer":        best["symbol"]  if best  else None,
            "worst_performer":       worst["symbol"] if worst else None,
            "generated_at":          datetime.now(timezone.utc).isoformat(),
        },
    }

    _CACHE[session_id] = (now, result)
    return result
