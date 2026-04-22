#!/usr/bin/env python3
# api/run_paper_signals.py
#
# Paper-trade signal generation job — reads strategy config from the API state DB
# so that the risk parameters and enabled strategies match what the user configured
# in the frontend.
#
# Designed to run as a cron job at 3:35 PM IST on trading days:
#   35 10 * * 1-5 cd /path/to/Financial_lab && python -m api.run_paper_signals >> logs/paper_signals.log 2>&1
#
# Differences from run_signals.py (the personal script):
#   - Reads max_position_pct, risk_per_trade_pct, pause_threshold_pct, enabled strategies
#     from the most-recent paper session's saved strategy config in api_state.db.
#   - Writes only for the active paper session — not a general-purpose signals run.
#   - Does NOT save/restore AdaptiveStrategySelector state (uses live market API
#     singleton instead, so state is shared with the API endpoints).

import os
import sys
import uuid
from datetime import date, datetime, timedelta, timezone

# Load .env so OPENAI_API_KEY and DATABASE_URL are available
from dotenv import load_dotenv
load_dotenv()

from app.backtest.observer import MarketObserverAgent
from app.data.calendar import NSECalendar
from app.data.models import SignalQueue
from app.data.providers.yfinance_provider import YFinanceProvider
from app.data.repository import MarketDataRepository
from app.meta.adaptive_selector import AdaptiveStrategySelector
from app.meta.regime_context_agent import RegimeContextAgent
from app.portfolio.models import Portfolio
from app.risk.agent import RiskAgent
from app.strategy.breakout_momentum import BreakoutMomentumStrategy
from app.strategy.dual_ma import DualMovingAverageStrategy
from app.strategy.multi_router import MultiStrategyRouter
from app.strategy.quiet_breakout import QuietBreakoutStrategy
from app.strategy.rsi_mean_reversion import RSIMeanReversionStrategy
from app.strategy.trend_pullback import TrendPullbackStrategy
from app.universe.dynamic_agent import DynamicUniverseAgent
from app.universe.filters import (
    BreakoutUniverseFilter,
    DualMAUniverseFilter,
    MeanReversionUniverseFilter,
    PullbackUniverseFilter,
    UnionUniverseFilter,
)
from app.core.database import SessionLocal
from app.core.notify import send_email
from app.core.push import send_push_to_session_user
from sqlalchemy import select

from run_experiments import NIFTY_50, NIFTY_NEXT_50, NIFTY_MIDCAP_50

BROAD_UNIVERSE = NIFTY_50 + NIFTY_NEXT_50 + NIFTY_MIDCAP_50

# ---------------------------------------------------------------------------
# Regime allowlists (mirrors backtest_service.py)
# ---------------------------------------------------------------------------
_UPTREND_ONLY = ["LOW_VOL_UPTREND", "MID_VOL_UPTREND", "HIGH_VOL_UPTREND"]
_TREND_AND_SIDEWAYS = [
    "LOW_VOL_UPTREND",  "MID_VOL_UPTREND",  "HIGH_VOL_UPTREND",
    "LOW_VOL_SIDEWAYS", "MID_VOL_SIDEWAYS",  "HIGH_VOL_SIDEWAYS",
]
_UPTREND_AND_SIDEWAYS = _TREND_AND_SIDEWAYS[:]

# UI id → internal name (mirrors backtest_service.py)
_UI_TO_INTERNAL = {
    "trend-follow":   "DualMA",
    "breakout":       "Breakout",
    "quiet-breakout": "QuietBrk",
    "trend-pullback": "TrendPB",
    "mean-reversion": "RSI-MR",
}

_STRATEGY_FACTORIES = {
    "DualMA":   lambda: DualMovingAverageStrategy(),
    "Breakout": lambda: BreakoutMomentumStrategy(),
    "QuietBrk": lambda: QuietBreakoutStrategy(),
    "TrendPB":  lambda: TrendPullbackStrategy(pullback_threshold=0.05),
    "RSI-MR":   lambda: RSIMeanReversionStrategy(
                    rsi_oversold=5, rsi_overbought=80, max_hold_days=7),
}

_ALLOWED_REGIMES = {
    "DualMA":   _UPTREND_ONLY,
    "Breakout": _TREND_AND_SIDEWAYS,
    "QuietBrk": _UPTREND_ONLY,
    "TrendPB":  _TREND_AND_SIDEWAYS,
    "RSI-MR":   _UPTREND_AND_SIDEWAYS,
}

# ---------------------------------------------------------------------------
# Config loaders from Supabase B
# ---------------------------------------------------------------------------

def _load_active_sessions() -> list[dict]:
    """Return all active paper sessions from Supabase B paper_trade_sessions."""
    from sqlalchemy import text as _text
    db = SessionLocal()
    try:
        rows = db.execute(_text(
            "SELECT session_id, strategy_id, strategy_name, starting_capital "
            "FROM paper_trade_sessions WHERE status = 'active'"
        )).fetchall()
        return [dict(r._mapping) for r in rows]
    except Exception as exc:
        print(f"  [Config] Could not read paper_trade_sessions ({exc})")
        return []
    finally:
        db.close()


def _load_strategy_config(strategy_id: str) -> dict | None:
    """Return strategy config from Supabase B user_strategies (universe, strategies, risk)."""
    from sqlalchemy import text as _text
    db = SessionLocal()
    try:
        row = db.execute(_text(
            "SELECT name, universe, strategies, risk "
            "FROM user_strategies WHERE id = :sid"
        ), {"sid": strategy_id}).fetchone()
        if row is None:
            return None
        # strategies and risk are JSONB — already dicts when fetched via psycopg2
        return {
            "name":       row.name,
            "universe":   row.universe,
            "strategies": row.strategies,
            "risk":       row.risk,
        }
    except Exception as exc:
        print(f"  [Config] Could not load strategy config ({exc})")
        return None
    finally:
        db.close()


# ---------------------------------------------------------------------------
# Portfolio reconstruction — derived from session's own signal_queue fills.
# Does NOT read live_positions (which has no session isolation and mixes
# personal paper-trading fills with API paper-session fills).
# ---------------------------------------------------------------------------

def _build_portfolio(session_id: str, starting_capital: float) -> tuple:
    """Rebuild portfolio state from FILLED signals in signal_queue for this session."""
    db = SessionLocal()
    try:
        fills = db.execute(
            select(SignalQueue)
            .where(SignalQueue.session_id == session_id)
            .where(SignalQueue.status == "FILLED")
            .order_by(SignalQueue.created_at.asc())
        ).scalars().all()
    finally:
        db.close()

    # Compute open positions from fill history
    positions: dict[str, dict] = {}
    for fill in fills:
        if fill.action == "BUY":
            if fill.symbol in positions:
                existing = positions[fill.symbol]
                new_qty  = existing["quantity"] + fill.fill_qty
                new_avg  = (existing["quantity"] * existing["average_price"]
                            + fill.fill_qty * fill.fill_price) / new_qty
                existing["quantity"]      = new_qty
                existing["average_price"] = new_avg
            else:
                positions[fill.symbol] = {
                    "quantity":      fill.fill_qty,
                    "average_price": fill.fill_price,
                    "strategy":      fill.strategy,
                }
        elif fill.action == "SELL" and fill.symbol in positions:
            remaining = positions[fill.symbol]["quantity"] - fill.fill_qty
            if remaining <= 0:
                del positions[fill.symbol]
            else:
                positions[fill.symbol]["quantity"] = remaining

    deployed = sum(p["quantity"] * p["average_price"] for p in positions.values())

    # Also deduct capital committed to PENDING/PLACED BUY signals that haven't
    # been filled yet — otherwise the cash gate re-opens to full capital the
    # next morning before yesterday's fills are processed and allows double-allocation.
    db2 = SessionLocal()
    try:
        pending_buys = db2.execute(
            select(SignalQueue)
            .where(SignalQueue.session_id == session_id)
            .where(SignalQueue.action == "BUY")
            .where(SignalQueue.status.in_(["PENDING", "PLACED"]))
        ).scalars().all()
    finally:
        db2.close()
    pending_deployed = sum(
        (r.target_qty or 0) * (r.raw_price or 0) for r in pending_buys
    )

    cash = max(starting_capital - deployed - pending_deployed, 0.0)

    portfolio        = Portfolio(cash=cash)
    position_owners  = {}
    for sym, pos in positions.items():
        portfolio.positions[sym] = type("Position", (), {
            "quantity":      pos["quantity"],
            "average_price": pos["average_price"],
        })()
        position_owners[sym] = pos["strategy"]

    print(f"    Capital: ₹{starting_capital:,.0f}  |  Deployed: ₹{deployed:,.0f}  |  Pending: ₹{pending_deployed:,.0f}  |  Cash: ₹{cash:,.0f}  |  Positions: {len(positions)}")
    if positions:
        for sym, pos in positions.items():
            print(f"      {sym:<14} qty={pos['quantity']}  avg=₹{pos['average_price']:.2f}  [{pos['strategy']}]")
    return portfolio, position_owners


# ---------------------------------------------------------------------------
# Signal writer
# ---------------------------------------------------------------------------

def _write_signals(decisions, daily_symbol_states, regime_label, weights, signal_date,
                   paper_session_id: str) -> int:
    session = SessionLocal()
    count = 0
    now = datetime.now(timezone.utc).replace(tzinfo=None)
    try:
        for decision in decisions:
            if decision.action not in ("BUY", "SELL"):
                continue
            if not decision.quantity or decision.quantity <= 0:
                continue
            state = daily_symbol_states.get(decision.symbol)
            if state is None:
                continue
            session.add(SignalQueue(
                id           = uuid.uuid4(),
                created_at   = now,
                signal_date  = signal_date,
                symbol       = decision.symbol,
                action       = decision.action,
                strategy     = decision.source or "unknown",
                regime_label = regime_label,
                weight       = weights.get(decision.source, 0.0),
                raw_price    = state.latest_price,
                target_qty   = int(decision.quantity),
                status       = "PENDING",
                notes        = decision.reasoning[:200] if decision.reasoning else None,
                session_id   = paper_session_id,
            ))
            count += 1
        session.commit()
    finally:
        session.close()
    return count


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------

def _run_session(sess: dict, daily_symbol_states: dict, regime_snapshot: dict,
                 broad_regime: str, suppress_buys: bool, today: date,
                 today_dt: datetime, observer, start_dt: datetime) -> None:
    """Run signal generation for a single paper session and write results."""
    sid       = sess["session_id"]
    strat_id  = sess["strategy_id"]

    config = _load_strategy_config(strat_id)
    if config is None:
        print(f"  [SKIP] {sid} — strategy '{strat_id}' not found in user_strategies")
        return

    risk_cfg       = config.get("risk") or {}
    strategies_cfg = config.get("strategies") or []

    starting_capital = float(sess["starting_capital"])
    max_pos_pct      = float(risk_cfg.get("max_position_pct", 10.0)) / 100.0
    risk_per_trade   = float(risk_cfg.get("risk_per_trade_pct", 0.5)) / 100.0
    pause_pct        = max(float(risk_cfg.get("pause_threshold_pct", 35.0)), 20.0) / 100.0

    enabled_internals = [
        _UI_TO_INTERNAL[s["id"]]
        for s in strategies_cfg
        if s.get("enabled") and s["id"] in _UI_TO_INTERNAL
    ]
    if not enabled_internals:
        enabled_internals = list(_STRATEGY_FACTORIES.keys())

    print(f"\n  ── Session {sid} ─────────────────────────────────────────")
    print(f"     Strategy: {sess.get('strategy_name', strat_id)}")
    print(f"     Capital:  ₹{starting_capital:,.0f}  |  Strategies: {enabled_internals}")
    print(f"     Risk:     max_pos={max_pos_pct:.0%}  rpt={risk_per_trade:.3%}  pause@{pause_pct:.0%}")

    # Adaptive weights for this session's enabled strategies
    selector = AdaptiveStrategySelector(
        strategy_names=enabled_internals,
        rebalance_frequency_days=5,
        model="gpt-4o-mini",
        verbose=False,
        regime_stability_weeks=2,
    )
    weights = selector.rebalance(today_dt, regime_snapshot)
    regime_label = selector._confirmed_regime or broad_regime
    print(f"     Regime: {regime_label} | Weights: " +
          "  ".join(f"{k}={v:.2f}" for k, v in weights.items()))

    portfolio, position_owners = _build_portfolio(sid, starting_capital)

    # Fix 1: Positions migrated from personal scripts have strategy='unknown'.
    # Reassign to first enabled strategy so the router can propose exit signals.
    default_strategy = enabled_internals[0]
    position_owners = {
        sym: (strat if strat in enabled_internals else default_strategy)
        for sym, strat in position_owners.items()
    }

    # Fix 2: Held positions that fell out of the active universe still need exit
    # evaluation. Preload their market state and add to a local extended dict.
    held_symbols = set(portfolio.positions.keys())
    missing_from_universe = held_symbols - set(daily_symbol_states.keys())
    extended_states = dict(daily_symbol_states)
    if missing_from_universe:
        loaded = 0
        for symbol in missing_from_universe:
            try:
                observer.preload(symbol, start_dt, today_dt)
                state = observer.run_for_day(symbol, today_dt)
                if state:
                    extended_states[symbol] = state
                    loaded += 1
            except Exception:
                pass
        print(f"     Loaded {loaded}/{len(missing_from_universe)} held-but-unmanaged "
              f"position states for exit evaluation")

    downtrend_count = sum(
        1 for s in extended_states.values()
        if isinstance(s.indicators.get("regime"), str)
        and "DOWNTREND" in s.indicators["regime"]
    )
    market_downtrend_pct = downtrend_count / len(extended_states)
    if broad_regime == "TRANSITION_UP":
        effective_downtrend_pct = min(market_downtrend_pct, 0.30)
    elif broad_regime in ("BEAR_WATCH", "BEAR_TRANSITION"):
        effective_downtrend_pct = min(market_downtrend_pct, 0.38)
    else:
        effective_downtrend_pct = market_downtrend_pct

    router = MultiStrategyRouter(
        strategies={name: _STRATEGY_FACTORIES[name]() for name in enabled_internals},
        weights=weights,
        allowed_regimes={name: _ALLOWED_REGIMES[name] for name in enabled_internals},
    )
    router.position_owners = position_owners
    proposed = router.decide(today_dt, extended_states, portfolio)

    risk_agent = RiskAgent(
        max_position_pct=max_pos_pct,
        atr_multiplier=2.0,
        risk_per_trade_pct=risk_per_trade,
        use_vol_sizing=True,
        breadth_circuit_breaker=True,
        max_downtrend_pct=pause_pct,
        min_atr_cost_ratio=3.0,
    )

    equity_prices = {s: st.latest_price for s, st in extended_states.items()}

    cb_active = effective_downtrend_pct >= pause_pct
    n_proposed = len([d for d in proposed if d is not None])
    cb_blocked = 0

    final_decisions = []
    for decision in proposed:
        if decision is None:
            continue
        state = extended_states.get(decision.symbol)
        if state is None:
            continue
        if suppress_buys and decision.action == "BUY":
            continue
        original_source = decision.source  # preserve before RiskAgent creates new Decision
        evaluated = risk_agent.evaluate(
            decision, portfolio, state,
            equity_prices=equity_prices,
            market_downtrend_pct=effective_downtrend_pct,
        )
        # RiskAgent always returns a fresh Decision without source — copy it back.
        if not getattr(evaluated, "source", None):
            evaluated.source = original_source
        if decision.action == "BUY" and evaluated.action == "HOLD" and cb_active:
            cb_blocked += 1
        final_decisions.append(evaluated)

    # Sequential cash gate: BUY signals are evaluated against the same cash
    # snapshot, so multiple BUYs can collectively exceed available cash.
    # Walk through BUYs in weight-descending order and drop/trim any that
    # don't fit in the remaining cash.
    remaining_cash = portfolio.cash
    cash_gated = []
    for d in final_decisions:
        if d.action != "BUY":
            cash_gated.append(d)
            continue
        state = extended_states.get(d.symbol)
        price = state.latest_price if state else 0.0
        if price <= 0:
            cash_gated.append(d)
            continue
        affordable_qty = int(remaining_cash // price)
        if affordable_qty <= 0:
            print(f"     [CashGate] DROP  {d.symbol} — no cash remaining (₹{remaining_cash:,.0f})")
            continue
        if affordable_qty < d.quantity:
            print(f"     [CashGate] TRIM  {d.symbol} qty {d.quantity}→{affordable_qty} "
                  f"(cash ₹{remaining_cash:,.0f}, price ₹{price:.2f})")
            d = Decision(symbol=d.symbol, action="BUY", quantity=affordable_qty,
                         reasoning=(d.reasoning or "") + f" | trimmed by cash gate",
                         source=d.source, weight=getattr(d, "weight", None))
        remaining_cash -= d.quantity * price
        cash_gated.append(d)
    final_decisions = cash_gated

    buys  = [d for d in final_decisions if d.action == "BUY"]
    sells = [d for d in final_decisions if d.action == "SELL"]
    written = _write_signals(final_decisions, extended_states, regime_label, weights,
                             today, paper_session_id=sid)

    cb_status = f"ACTIVE — {effective_downtrend_pct:.0%} downtrend > pause {pause_pct:.0%}" if cb_active else "clear"
    print(f"     Router proposals: {n_proposed}  →  BUY:{len(buys)}  SELL:{len(sells)}  CB-blocked:{cb_blocked}  CB={cb_status}")
    print(f"     Signals written: {written}")

    send_email(
        subject=f"[FinLab Paper] {sid} — {today} | {regime_label} | BUY:{len(buys)} SELL:{len(sells)}",
        body=(
            f"Paper Trade Signal Report — {today}\n\n"
            f"Session:   {sid}  ({sess.get('strategy_name', strat_id)})\n"
            f"Regime:    {regime_label}  (broad={broad_regime})\n"
            f"Breadth:   {market_downtrend_pct:.0%} raw → {effective_downtrend_pct:.0%} effective  "
            f"(CB {'ACTIVE' if cb_active else 'clear'})\n"
            f"Weights:   {' '.join(f'{k}={v:.2f}' for k, v in weights.items())}\n\n"
            f"BUY ({len(buys)}):\n" +
            ("\n".join(
                f"  {d.symbol:<14} qty={d.quantity}  @ ₹{daily_symbol_states[d.symbol].latest_price:.2f}  [{d.source}]"
                for d in buys if d.symbol in daily_symbol_states
            ) or "  (none)") +
            f"\n\nSELL ({len(sells)}):\n" +
            ("\n".join(
                f"  {d.symbol:<14} qty={d.quantity}  @ ₹{daily_symbol_states[d.symbol].latest_price:.2f}  [{d.source}]"
                for d in sells if d.symbol in daily_symbol_states
            ) or "  (none)")
        ),
    )

    if written > 0:
        top_tickers = ", ".join(d.symbol for d in buys[:3]) if buys else None
        push_body = f"{len(buys)} BUY · {len(sells)} SELL · {regime_label}"
        if top_tickers:
            push_body += f" — {top_tickers}"
        send_push_to_session_user(
            sid,
            title=f"Signals ready — {today}",
            body=push_body,
            data={"screen": "PaperTrade"},
        )
    else:
        reason = "Breadth circuit breaker active" if cb_active else f"Regime: {regime_label}"
        send_push_to_session_user(
            sid,
            title="No signals today",
            body=f"Strategy paused — {reason}. Open Insights for details.",
            data={"screen": "PaperTrade"},
        )


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--session", metavar="SESSION_ID", default=None,
                        help="Run for a single session only (skips trading-day check)")
    args = parser.parse_args()

    today    = date.today()
    today_dt = datetime.combine(today, datetime.min.time())
    calendar = NSECalendar()

    if not args.session and not calendar.is_trading_day(today):
        print(f"[paper_signals] {today} is not a trading day — exiting.")
        sys.exit(0)

    print(f"\n{'='*70}")
    print(f"  api/run_paper_signals.py — {today}")
    if args.session:
        print(f"  *** Single-session mode: {args.session} ***")
    print(f"{'='*70}")

    # ------------------------------------------------------------------
    # Load sessions — filter to the requested one if --session passed
    # ------------------------------------------------------------------
    active_sessions = _load_active_sessions()
    if args.session:
        active_sessions = [s for s in active_sessions if s["session_id"] == args.session]
        if not active_sessions:
            print(f"  Session '{args.session}' not found or not active — exiting.")
            sys.exit(1)
    if not active_sessions:
        print("  No active paper sessions — exiting.")
        sys.exit(0)
    print(f"  Active sessions: {len(active_sessions)}")

    suppress_buys = os.environ.get("SUPPRESS_NEW_BUYS", "0") == "1"
    if suppress_buys:
        print("  *** SUPPRESS_NEW_BUYS=1 — no new BUY signals ***")

    # ------------------------------------------------------------------
    # Fetch today's EOD data (once, shared across all sessions)
    # ------------------------------------------------------------------
    print(f"\n[1/4] Fetching today's EOD data...")
    provider   = YFinanceProvider()
    repository = MarketDataRepository()
    fetched = 0
    for symbol in BROAD_UNIVERSE:
        try:
            records = provider.fetch_ohlc(symbol, start=today, end=today + timedelta(days=1))
            if records:
                repository.bulk_upsert(records)
                fetched += 1
        except Exception:
            pass
    print(f"    Fetched: {fetched} symbols")

    # ------------------------------------------------------------------
    # Universe + market states + regime (once, shared across all sessions)
    # ------------------------------------------------------------------
    print(f"\n[2/4] Building universe + market states...")
    warmup_start = today - timedelta(days=300)
    start_dt     = datetime.combine(warmup_start, datetime.min.time())

    dynamic_agent = DynamicUniverseAgent(repository=repository, symbols=BROAD_UNIVERSE, top_n=80)
    dynamic_agent.preload(start_dt, today_dt)
    rca = RegimeContextAgent(dynamic_agent)

    union_filter = UnionUniverseFilter([
        BreakoutUniverseFilter(top_n=20),
        BreakoutUniverseFilter(vol_threshold=1.2, return_threshold=0.008, top_n=20),
        PullbackUniverseFilter(top_n=20),
        MeanReversionUniverseFilter(top_n=20),
        DualMAUniverseFilter(max_cross_age=5, top_n=30),
    ])
    active_symbols = union_filter.select_symbols(dynamic_agent.select_candidates(today_dt))

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
        print("    No market states — exiting.")
        sys.exit(1)
    print(f"    Active symbols: {len(active_symbols)}  |  States: {len(daily_symbol_states)}")

    # ------------------------------------------------------------------
    # Regime snapshot (once, shared)
    # ------------------------------------------------------------------
    print(f"\n[3/4] Regime snapshot...")
    regime_snapshot = rca.build_snapshot(daily_symbol_states, today_dt)
    broad_regime = regime_snapshot.get("broad_regime", "UNKNOWN")
    trend        = regime_snapshot.get("trend", "STABLE")
    print(
        f"    UP={regime_snapshot['pct_uptrend']:.1%}  "
        f"DOWN={regime_snapshot['pct_downtrend']:.1%}  "
        f"ATR={regime_snapshot['avg_atr_pct']:.2%}  "
        f"Broad={broad_regime}  trend={trend}"
    )

    # ------------------------------------------------------------------
    # Per-session signal generation
    # ------------------------------------------------------------------
    print(f"\n[4/4] Generating signals for {len(active_sessions)} session(s)...")
    for sess in active_sessions:
        try:
            _run_session(sess, daily_symbol_states, regime_snapshot,
                         broad_regime, suppress_buys, today, today_dt,
                         observer, start_dt)
        except Exception as exc:
            print(f"  [ERROR] Session {sess['session_id']}: {exc}")

    print(f"\n{'='*70}")
    print(f"  Done — {today}")
    print(f"{'='*70}\n")


if __name__ == "__main__":
    main()
