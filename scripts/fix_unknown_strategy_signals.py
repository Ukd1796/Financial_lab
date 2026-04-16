#!/usr/bin/env python3
"""
scripts/fix_unknown_strategy_signals.py

Backfill script for session pt_ujjwal that does three things in one pass:

  1. Fix strategy='unknown' on existing BUY signals by re-running the
     MultiStrategyRouter against historical OHLC data for each affected date.

  2. Write any SELL signals that the router would have generated on past
     dates but weren't captured (and immediately fill them at next-day open
     so portfolio state is correct for subsequent dates).

  3. Optionally run today's signal generation for the session so that
     current SELL / BUY signals are produced with correct strategy labels.

Usage:
    python scripts/fix_unknown_strategy_signals.py              # dry-run
    python scripts/fix_unknown_strategy_signals.py --apply      # write to DB
    python scripts/fix_unknown_strategy_signals.py --apply --run-today

LLM note: AdaptiveStrategySelector.rebalance() calls OpenAI once per date.
This is intentional — production does the same (fresh selector each daily run,
no saved state). Expect ~7 LLM calls for 7 affected dates.
"""

import argparse
import sys
import os
import uuid
from collections import defaultdict
from datetime import date, datetime, timedelta

from dotenv import load_dotenv
load_dotenv()

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import select, text as _text, update, and_

from app.core.database import SessionLocal
from app.data.models import SignalQueue, MarketOHLC
from app.data.repository import MarketDataRepository
from app.backtest.observer import MarketObserverAgent
from app.meta.adaptive_selector import AdaptiveStrategySelector
from app.meta.regime_context_agent import RegimeContextAgent
from app.portfolio.models import Portfolio
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

from run_experiments import NIFTY_50, NIFTY_NEXT_50, NIFTY_MIDCAP_50

BROAD_UNIVERSE = NIFTY_50 + NIFTY_NEXT_50 + NIFTY_MIDCAP_50
SESSION_ID = "pt_ujjwal"
LOOKBACK_DAYS = 12

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
    "RSI-MR":   lambda: RSIMeanReversionStrategy(rsi_oversold=5, rsi_overbought=80, max_hold_days=7),
}
_UPTREND_ONLY = ["LOW_VOL_UPTREND", "MID_VOL_UPTREND", "HIGH_VOL_UPTREND"]
_TREND_AND_SIDEWAYS = [
    "LOW_VOL_UPTREND", "MID_VOL_UPTREND", "HIGH_VOL_UPTREND",
    "LOW_VOL_SIDEWAYS", "MID_VOL_SIDEWAYS", "HIGH_VOL_SIDEWAYS",
]
_ALLOWED_REGIMES = {
    "DualMA":   _UPTREND_ONLY,
    "Breakout": _TREND_AND_SIDEWAYS,
    "QuietBrk": _UPTREND_ONLY,
    "TrendPB":  _TREND_AND_SIDEWAYS,
    "RSI-MR":   _TREND_AND_SIDEWAYS,
}
_IST = timedelta(hours=5, minutes=30)


# ---------------------------------------------------------------------------
# DB helpers
# ---------------------------------------------------------------------------

def _load_session_config() -> tuple[dict, dict] | tuple[None, None]:
    db = SessionLocal()
    try:
        sess = db.execute(_text(
            "SELECT session_id, strategy_id, strategy_name, starting_capital "
            "FROM paper_trade_sessions WHERE session_id = :sid"
        ), {"sid": SESSION_ID}).fetchone()
        if sess is None:
            print(f"ERROR: session '{SESSION_ID}' not found in paper_trade_sessions")
            return None, None
        sess_dict = dict(sess._mapping)

        strat = db.execute(_text(
            "SELECT name, universe, strategies, risk "
            "FROM user_strategies WHERE id = :sid"
        ), {"sid": sess_dict["strategy_id"]}).fetchone()
        if strat is None:
            print(f"ERROR: strategy_id '{sess_dict['strategy_id']}' not found in user_strategies")
            return sess_dict, None
        return sess_dict, {
            "name":       strat.name,
            "universe":   strat.universe,
            "strategies": strat.strategies,
            "risk":       strat.risk,
        }
    finally:
        db.close()


def _fetch_unknown_signals() -> list:
    cutoff = date.today() - timedelta(days=LOOKBACK_DAYS)
    db = SessionLocal()
    try:
        rows = db.execute(
            select(SignalQueue)
            .where(SignalQueue.session_id == SESSION_ID)
            .where(SignalQueue.strategy == "unknown")
            .where(SignalQueue.signal_date >= cutoff)
            .order_by(SignalQueue.signal_date.asc(), SignalQueue.created_at.asc())
        ).scalars().all()
        return list(rows)
    finally:
        db.close()


def _signal_exists(symbol: str, action: str, signal_date: date) -> bool:
    """Check if a signal already exists for (symbol, action, date, session)."""
    db = SessionLocal()
    try:
        row = db.execute(
            select(SignalQueue).where(
                and_(
                    SignalQueue.session_id  == SESSION_ID,
                    SignalQueue.symbol      == symbol,
                    SignalQueue.action      == action,
                    SignalQueue.signal_date == signal_date,
                    SignalQueue.status.notin_(["CANCELLED"]),
                )
            ).limit(1)
        ).scalar_one_or_none()
        return row is not None
    finally:
        db.close()


def _get_next_open_price(symbol: str, signal_date: date) -> float | None:
    """Get the next trading day's open price from market_ohlc (mirrors PaperAdapter)."""
    next_day = signal_date + timedelta(days=1)
    cutoff   = signal_date + timedelta(days=5)
    db = SessionLocal()
    try:
        row = db.execute(
            select(MarketOHLC)
            .where(MarketOHLC.symbol == symbol)
            .where(MarketOHLC.timestamp >= datetime.combine(next_day, datetime.min.time()) - _IST)
            .where(MarketOHLC.timestamp <= datetime.combine(cutoff, datetime.max.time()) - _IST)
            .order_by(MarketOHLC.timestamp.asc())
            .limit(1)
        ).scalar_one_or_none()
        return row.open if row else None
    finally:
        db.close()


def _write_and_fill_sell(symbol: str, action: str, quantity: int, strategy: str,
                          raw_price: float, regime_label: str, weight: float,
                          signal_date: date, notes: str | None) -> bool:
    """Write a SELL signal and immediately fill it at next-day open. Returns True if written."""
    fill_price = _get_next_open_price(symbol, signal_date)
    db = SessionLocal()
    try:
        now = datetime.utcnow()
        order_id = f"PAPER-{uuid.uuid4().hex[:8].upper()}"
        if fill_price is not None:
            status     = "FILLED"
            fill_qty   = quantity
            fill_notes = f"{notes or ''} | Paper fill @ {fill_price:.2f} (backfill)".strip(" |")
        else:
            status     = "PENDING"
            fill_qty   = None
            fill_notes = notes

        db.add(SignalQueue(
            id           = uuid.uuid4(),
            created_at   = now,
            signal_date  = signal_date,
            symbol       = symbol,
            action       = action,
            strategy     = strategy,
            regime_label = regime_label,
            weight       = weight,
            raw_price    = raw_price,
            target_qty   = quantity,
            status       = status,
            order_id     = order_id if fill_price else None,
            fill_price   = fill_price,
            fill_qty     = fill_qty,
            notes        = fill_notes,
            session_id   = SESSION_ID,
        ))
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        print(f"    ERROR writing SELL signal for {symbol}: {e}")
        return False
    finally:
        db.close()


def _build_running_portfolio(up_to_date: date, starting_capital: float) -> tuple:
    """Build portfolio from FILLED signals up to (not including) up_to_date."""
    db = SessionLocal()
    try:
        fills = db.execute(
            select(SignalQueue)
            .where(SignalQueue.session_id == SESSION_ID)
            .where(SignalQueue.status == "FILLED")
            .where(SignalQueue.signal_date < up_to_date)
            .order_by(SignalQueue.created_at.asc())
        ).scalars().all()
    finally:
        db.close()

    positions: dict[str, dict] = {}
    for fill in fills:
        if fill.action == "BUY":
            if fill.symbol in positions:
                ex = positions[fill.symbol]
                new_qty = ex["quantity"] + fill.fill_qty
                new_avg = (ex["quantity"] * ex["average_price"]
                           + fill.fill_qty * fill.fill_price) / new_qty
                ex["quantity"] = new_qty
                ex["average_price"] = new_avg
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
    cash = max(starting_capital - deployed, 0.0)
    portfolio = Portfolio(cash=cash)
    position_owners: dict[str, str] = {}
    for sym, pos in positions.items():
        portfolio.positions[sym] = type("Position", (), {
            "quantity":      pos["quantity"],
            "average_price": pos["average_price"],
        })()
        position_owners[sym] = pos["strategy"]
    return portfolio, position_owners


def _build_symbol_states_for_date(
    target_date: date,
    extra_symbols: list[str],
    observer: MarketObserverAgent,
    dynamic_agent: DynamicUniverseAgent,
) -> tuple[dict, dict]:
    target_dt    = datetime.combine(target_date, datetime.min.time())
    warmup_start = target_date - timedelta(days=300)
    start_dt     = datetime.combine(warmup_start, datetime.min.time())

    try:
        dynamic_agent.preload(start_dt, target_dt)
    except Exception as e:
        print(f"    Warning: dynamic_agent.preload: {e}")

    union_filter = UnionUniverseFilter([
        BreakoutUniverseFilter(top_n=20),
        BreakoutUniverseFilter(vol_threshold=1.2, return_threshold=0.008, top_n=20),
        PullbackUniverseFilter(top_n=20),
        MeanReversionUniverseFilter(top_n=20),
        DualMAUniverseFilter(max_cross_age=5, top_n=30),
    ])
    active_symbols = list(set(
        union_filter.select_symbols(dynamic_agent.select_candidates(target_dt))
    ) | set(extra_symbols))

    for sym in active_symbols:
        if sym not in observer.symbol_cache:
            try:
                observer.preload(sym, start_dt, target_dt)
            except Exception:
                pass

    symbol_states = {}
    for sym in active_symbols:
        try:
            state = observer.run_for_day(sym, target_dt)
            if state:
                symbol_states[sym] = state
        except Exception:
            pass

    rca = RegimeContextAgent(dynamic_agent)
    regime_snapshot = rca.build_snapshot(symbol_states, target_dt)
    return symbol_states, regime_snapshot


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true",
                        help="Write changes to DB (default: dry-run)")
    parser.add_argument("--run-today", action="store_true",
                        help="After backfill, run today's signal generation for pt_ujjwal")
    args = parser.parse_args()

    print(f"\n{'='*70}")
    print(f"  fix_unknown_strategy_signals.py — session={SESSION_ID}")
    print(f"  Mode: {'APPLY' if args.apply else 'DRY-RUN'}")
    print(f"  LLM: AdaptiveStrategySelector makes ~1 OpenAI call per date (expected)")
    print(f"{'='*70}\n")

    sess, strat_cfg = _load_session_config()
    if sess is None or strat_cfg is None:
        sys.exit(1)

    starting_capital = float(sess["starting_capital"])
    strategies_cfg   = strat_cfg.get("strategies") or []

    enabled_internals = [
        _UI_TO_INTERNAL[s["id"]]
        for s in strategies_cfg
        if s.get("enabled") and s["id"] in _UI_TO_INTERNAL
    ] or list(_STRATEGY_FACTORIES.keys())

    print(f"Session:    {sess['session_id']} — {sess.get('strategy_name', '')}")
    print(f"Capital:    ₹{starting_capital:,.0f}")
    print(f"Strategies: {enabled_internals}\n")

    unknown_signals = _fetch_unknown_signals()
    if not unknown_signals:
        print("No unknown-strategy signals found.")
        if not args.run_today:
            sys.exit(0)

    if unknown_signals:
        print(f"Found {len(unknown_signals)} signal(s) with strategy='unknown' across "
              f"{len(set(s.signal_date for s in unknown_signals))} date(s).\n")

    # All affected dates (for unknown BUYs). We process ALL dates in range to
    # also catch SELL opportunities even on dates with no unknown BUYs.
    by_date: dict[date, list] = defaultdict(list)
    for sig in unknown_signals:
        by_date[sig.signal_date].append(sig)

    # Determine full date range to replay
    if unknown_signals:
        earliest = min(by_date.keys())
        latest   = max(by_date.keys())
    else:
        earliest = latest = date.today()

    # Shared infrastructure — preload once
    repository    = MarketDataRepository()
    observer      = MarketObserverAgent(repository)
    dynamic_agent = DynamicUniverseAgent(repository=repository, symbols=BROAD_UNIVERSE, top_n=80)

    warmup_start = earliest - timedelta(days=400)
    today_dt     = datetime.combine(date.today(), datetime.min.time())

    print("[1/3] Preloading broad universe data...")
    dynamic_agent.preload(
        datetime.combine(warmup_start, datetime.min.time()), today_dt
    )
    print("      Done.\n")

    # ---------------------------------------------------------------------------
    # Process each date in chronological order
    # ---------------------------------------------------------------------------
    resolved_buys: dict[str, str] = {}   # signal_id → strategy name
    fallback_buys: list = []
    sell_log: list[dict] = []            # projected/written SELLs

    print("[2/3] Replaying signal routing for each date...\n")

    for target_date in sorted(by_date.keys()):
        unknown_on_date = by_date[target_date]
        extra_syms = [s.symbol for s in unknown_on_date]
        target_dt  = datetime.combine(target_date, datetime.min.time())

        print(f"  ── {target_date} ─────────────────────────────────────────────")

        # Portfolio state at start of this date
        portfolio, position_owners = _build_running_portfolio(target_date, starting_capital)
        default_strategy = enabled_internals[0]
        position_owners = {
            sym: (strat if strat in enabled_internals else default_strategy)
            for sym, strat in position_owners.items()
        }

        held_symbols = set(portfolio.positions.keys())
        symbol_states, regime_snapshot = _build_symbol_states_for_date(
            target_date, list(set(extra_syms) | held_symbols), observer, dynamic_agent
        )
        if not symbol_states:
            print(f"    WARNING: No symbol states — skipping")
            fallback_buys.extend(unknown_on_date)
            for sig in unknown_on_date:
                resolved_buys[str(sig.id)] = default_strategy
            continue

        broad_regime = regime_snapshot.get("broad_regime", "UNKNOWN")

        selector = AdaptiveStrategySelector(
            strategy_names=enabled_internals,
            rebalance_frequency_days=5,
            model="gpt-4o-mini",
            verbose=False,
            regime_stability_weeks=2,
        )
        weights = selector.rebalance(target_dt, regime_snapshot)
        regime_label = selector._confirmed_regime or broad_regime
        print(f"    Regime: {regime_label}  Weights: " +
              "  ".join(f"{k}={v:.2f}" for k, v in weights.items()))

        # Make sure held symbols have states for exit evaluation
        for sym in held_symbols - set(symbol_states.keys()):
            try:
                start_dt = datetime.combine(target_date - timedelta(days=300), datetime.min.time())
                observer.preload(sym, start_dt, target_dt)
                state = observer.run_for_day(sym, target_dt)
                if state:
                    symbol_states[sym] = state
            except Exception:
                pass

        router = MultiStrategyRouter(
            strategies={name: _STRATEGY_FACTORIES[name]() for name in enabled_internals},
            weights=weights,
            allowed_regimes={name: _ALLOWED_REGIMES[name] for name in enabled_internals},
        )
        router.position_owners = position_owners
        decisions = router.decide(target_dt, symbol_states, portfolio)

        # ── BUY attribution ──────────────────────────────────────────────
        decision_map: dict[tuple, str] = {}
        for d in decisions:
            if d and d.action in ("BUY", "SELL") and d.source:
                key = (d.symbol, d.action)
                if key not in decision_map:
                    decision_map[key] = d.source

        for sig in unknown_on_date:
            key = (sig.symbol, sig.action)
            if key in decision_map:
                resolved_buys[str(sig.id)] = decision_map[key]
                print(f"    MATCH   {sig.symbol:<14} {sig.action:<4} → {decision_map[key]}")
            else:
                resolved_buys[str(sig.id)] = default_strategy
                fallback_buys.append(sig)
                print(f"    FALLBACK {sig.symbol:<14} {sig.action:<4} → {default_strategy} (no router match)")

        # ── SELL signal generation ───────────────────────────────────────
        sell_decisions = [d for d in decisions if d and d.action == "SELL" and d.source]
        new_sells = 0
        for d in sell_decisions:
            if not d.quantity or d.quantity <= 0:
                continue
            state = symbol_states.get(d.symbol)
            if state is None:
                continue
            already_exists = _signal_exists(d.symbol, "SELL", target_date)
            if already_exists:
                continue

            fill_price = _get_next_open_price(d.symbol, target_date)
            sell_log.append({
                "date":       target_date,
                "symbol":     d.symbol,
                "qty":        d.quantity,
                "strategy":   d.source,
                "raw_price":  state.latest_price,
                "fill_price": fill_price,
                "apply":      False,
            })

            if args.apply:
                ok = _write_and_fill_sell(
                    symbol      = d.symbol,
                    action      = "SELL",
                    quantity    = int(d.quantity),
                    strategy    = d.source,
                    raw_price   = state.latest_price,
                    regime_label= regime_label,
                    weight      = weights.get(d.source, 0.0),
                    signal_date = target_date,
                    notes       = d.reasoning[:200] if d.reasoning else None,
                )
                if ok:
                    sell_log[-1]["apply"] = True
                    new_sells += 1
                    fill_str = f"@ ₹{fill_price:.2f}" if fill_price else "PENDING fill"
                    print(f"    SELL    {d.symbol:<14} qty={d.quantity}  {fill_str}  [{d.source}]  ✓ written")
            else:
                fill_str = f"@ ₹{fill_price:.2f}" if fill_price else "(fill not yet available)"
                print(f"    SELL    {d.symbol:<14} qty={d.quantity}  {fill_str}  [{d.source}]  [DRY-RUN]")

    # ---------------------------------------------------------------------------
    # Summary
    # ---------------------------------------------------------------------------
    print(f"\n[3/3] Summary\n{'─'*68}")

    if unknown_signals:
        print(f"\n  BUY strategy attribution ({len(resolved_buys)} signals):")
        print(f"  {'DATE':<12} {'SYMBOL':<14} {'STRATEGY':<14} {'STATUS':<10} {'NOTE'}")
        for sig in unknown_signals:
            sid      = str(sig.id)
            strat    = resolved_buys.get(sid, "?")
            is_fb    = sig in fallback_buys
            note     = "*fallback*" if is_fb else ""
            print(f"  {str(sig.signal_date):<12} {sig.symbol:<14} {strat:<14} {sig.status:<10} {note}")

    if sell_log:
        print(f"\n  SELL signals {'(written)' if args.apply else '(projected — not written in dry-run)'}:")
        print(f"  {'DATE':<12} {'SYMBOL':<14} {'QTY':<6} {'STRATEGY':<12} {'FILL PRICE'}")
        for s in sell_log:
            fp = f"₹{s['fill_price']:.2f}" if s['fill_price'] else "no fill data"
            status = "✓" if s.get("apply") else "[dry-run]"
            print(f"  {str(s['date']):<12} {s['symbol']:<14} {s['qty']:<6} {s['strategy']:<12} {fp}  {status}")
    else:
        print(f"\n  No new SELL signals identified for the backfill range.")

    print(f"\n  Resolved BUYs:    {len(resolved_buys)}")
    print(f"  Fallback BUYs:    {len(fallback_buys)} (assigned to {enabled_internals[0]})")
    print(f"  New SELL signals: {len(sell_log)}")

    if not args.apply:
        print(f"\n  DRY-RUN complete — no DB changes. Re-run with --apply to commit.\n")
        sys.exit(0)

    # ---------------------------------------------------------------------------
    # Apply BUY strategy label updates
    # ---------------------------------------------------------------------------
    print(f"\n  Updating strategy labels on {len(resolved_buys)} BUY signal(s)...")
    db = SessionLocal()
    try:
        updated = 0
        for sig_id_str, strat_name in resolved_buys.items():
            db.execute(
                update(SignalQueue)
                .where(SignalQueue.id == sig_id_str)
                .values(strategy=strat_name)
            )
            updated += 1
        db.commit()
        print(f"  Updated {updated} row(s).\n")
    except Exception as e:
        db.rollback()
        print(f"  ERROR: {e}")
        sys.exit(1)
    finally:
        db.close()

    # ---------------------------------------------------------------------------
    # Optionally run today's signals
    # ---------------------------------------------------------------------------
    if args.run_today:
        print("Running today's full signal generation for pt_ujjwal...\n")
        from api.run_paper_signals import _load_active_sessions, _run_session
        from app.data.calendar import NSECalendar
        from app.data.providers.yfinance_provider import YFinanceProvider

        today    = date.today()
        today_dt = datetime.combine(today, datetime.min.time())
        calendar = NSECalendar()

        if not calendar.is_trading_day(today):
            print(f"Today ({today}) is not a trading day — skipping.")
            sys.exit(0)

        active_sessions = [s for s in _load_active_sessions() if s["session_id"] == SESSION_ID]
        if not active_sessions:
            print(f"Session {SESSION_ID} is not active — skipping.")
            sys.exit(0)

        provider = YFinanceProvider()
        for symbol in BROAD_UNIVERSE:
            try:
                records = provider.fetch_ohlc(symbol, start=today, end=today + timedelta(days=1))
                if records:
                    repository.bulk_upsert(records)
            except Exception:
                pass

        warmup_today = today - timedelta(days=300)
        start_dt_today = datetime.combine(warmup_today, datetime.min.time())
        dynamic_agent.preload(start_dt_today, today_dt)

        union_filter = UnionUniverseFilter([
            BreakoutUniverseFilter(top_n=20),
            BreakoutUniverseFilter(vol_threshold=1.2, return_threshold=0.008, top_n=20),
            PullbackUniverseFilter(top_n=20),
            MeanReversionUniverseFilter(top_n=20),
            DualMAUniverseFilter(max_cross_age=5, top_n=30),
        ])
        active_syms_today = union_filter.select_symbols(
            dynamic_agent.select_candidates(today_dt)
        )
        observer_today = MarketObserverAgent(repository)
        for sym in active_syms_today:
            try:
                observer_today.preload(sym, start_dt_today, today_dt)
            except Exception:
                pass

        daily_symbol_states = {}
        for sym in active_syms_today:
            state = observer_today.run_for_day(sym, today_dt)
            if state:
                daily_symbol_states[sym] = state

        rca_today = RegimeContextAgent(dynamic_agent)
        regime_snapshot_today = rca_today.build_snapshot(daily_symbol_states, today_dt)
        broad_regime_today    = regime_snapshot_today.get("broad_regime", "UNKNOWN")
        suppress_buys         = os.environ.get("SUPPRESS_NEW_BUYS", "0") == "1"

        for sess_row in active_sessions:
            _run_session(
                sess               = sess_row,
                daily_symbol_states= daily_symbol_states,
                regime_snapshot    = regime_snapshot_today,
                broad_regime       = broad_regime_today,
                suppress_buys      = suppress_buys,
                today              = today,
                today_dt           = today_dt,
                observer           = observer_today,
                start_dt           = start_dt_today,
            )

    print("\nDone.\n")


if __name__ == "__main__":
    main()
