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

import json
import os
import sqlite3
import sys
import uuid
from datetime import date, datetime, timedelta

# Load .env so OPENAI_API_KEY and DATABASE_URL are available
from dotenv import load_dotenv
load_dotenv()

from app.backtest.observer import MarketObserverAgent
from app.broker.paper_adapter import PaperAdapter
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

_API_STATE_DB = os.path.join(os.path.dirname(__file__), "..", "api_state.db")
_API_STATE_DB = os.path.abspath(_API_STATE_DB)


# ---------------------------------------------------------------------------
# Config loaders from api_state.db
# ---------------------------------------------------------------------------

def _load_active_session() -> dict | None:
    """Return the most-recent paper_sessions row, or None."""
    try:
        conn = sqlite3.connect(_API_STATE_DB)
        conn.row_factory = sqlite3.Row
        row = conn.execute(
            "SELECT * FROM paper_sessions ORDER BY created_at DESC LIMIT 1"
        ).fetchone()
        conn.close()
        return dict(row) if row else None
    except Exception as exc:
        print(f"  [Config] Could not read paper_sessions ({exc})")
        return None


def _load_strategy_config(strategy_id: str) -> dict | None:
    """Return the parsed config dict for the given strategy_id, or None."""
    try:
        conn = sqlite3.connect(_API_STATE_DB)
        conn.row_factory = sqlite3.Row
        row = conn.execute(
            "SELECT config_json FROM strategies WHERE id = ?", (strategy_id,)
        ).fetchone()
        conn.close()
        return json.loads(row["config_json"]) if row else None
    except Exception as exc:
        print(f"  [Config] Could not load strategy config ({exc})")
        return None


# ---------------------------------------------------------------------------
# Portfolio reconstruction
# ---------------------------------------------------------------------------

def _build_portfolio(broker: PaperAdapter, starting_capital: float) -> tuple:
    position_owners = {}
    positions = broker.get_positions()
    deployed = sum(p.quantity * p.average_price for p in positions)
    cash = max(starting_capital - deployed, 0.0)

    portfolio = Portfolio(cash=cash)
    for pos in positions:
        portfolio.positions[pos.symbol] = type(
            "Position", (), {
                "quantity":      pos.quantity,
                "average_price": pos.average_price,
            }
        )()
        position_owners[pos.symbol] = pos.strategy

    print(f"    Capital: ₹{starting_capital:,.0f}  |  Deployed: ₹{deployed:,.0f}  |  Cash: ₹{cash:,.0f}")
    return portfolio, position_owners


# ---------------------------------------------------------------------------
# Signal writer
# ---------------------------------------------------------------------------

def _write_signals(decisions, daily_symbol_states, regime_label, weights, signal_date) -> int:
    session = SessionLocal()
    count = 0
    now = datetime.utcnow()
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
            ))
            count += 1
        session.commit()
    finally:
        session.close()
    return count


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------

def main():
    today    = date.today()
    today_dt = datetime.combine(today, datetime.min.time())
    calendar = NSECalendar()

    if not calendar.is_trading_day(today):
        print(f"[paper_signals] {today} is not a trading day — exiting.")
        sys.exit(0)

    print(f"\n{'='*70}")
    print(f"  api/run_paper_signals.py — {today}")
    print(f"{'='*70}")

    # ------------------------------------------------------------------
    # Load active session + strategy config
    # ------------------------------------------------------------------
    session = _load_active_session()
    if session is None:
        print("  No active paper session found — start one via POST /api/paper-trade/start")
        sys.exit(1)

    strategy_config = _load_strategy_config(session["strategy_id"])
    if strategy_config is None:
        print(f"  Strategy '{session['strategy_id']}' not found in DB — exiting.")
        sys.exit(1)

    risk_cfg       = strategy_config.get("risk", {})
    strategies_cfg = strategy_config.get("strategies", [])

    starting_capital = float(session["starting_capital"])
    max_pos_pct      = float(risk_cfg.get("max_position_pct", 10.0)) / 100.0
    risk_per_trade   = float(risk_cfg.get("risk_per_trade_pct", 0.5)) / 100.0
    pause_pct        = float(risk_cfg.get("pause_threshold_pct", 35.0)) / 100.0

    # Resolve enabled strategies
    enabled_internals = [
        _UI_TO_INTERNAL[s["id"]]
        for s in strategies_cfg
        if s.get("enabled") and s["id"] in _UI_TO_INTERNAL
    ]
    if not enabled_internals:
        print("  No enabled strategies in config — falling back to all 5")
        enabled_internals = list(_STRATEGY_FACTORIES.keys())

    print(f"  Session:    {session['session_id']}  (strategy: {session['strategy_id']})")
    print(f"  Capital:    ₹{starting_capital:,.0f}")
    print(f"  Strategies: {enabled_internals}")
    print(f"  Risk:       max_pos={max_pos_pct:.0%}  risk_per_trade={risk_per_trade:.3%}  pause_at={pause_pct:.0%} downtrend")

    suppress_buys = os.environ.get("SUPPRESS_NEW_BUYS", "0") == "1"
    if suppress_buys:
        print("  *** SUPPRESS_NEW_BUYS=1 — no new BUY signals ***")

    # ------------------------------------------------------------------
    # Fetch today's EOD data
    # ------------------------------------------------------------------
    print(f"\n[1/7] Fetching today's EOD data...")
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
    # Universe + regime
    # ------------------------------------------------------------------
    print(f"\n[2/7] Building universe + regime snapshot...")
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
    print(f"    Active symbols: {len(active_symbols)}")

    # ------------------------------------------------------------------
    # Market states
    # ------------------------------------------------------------------
    print(f"\n[3/7] Computing market states...")
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
    print(f"    States: {len(daily_symbol_states)} symbols")

    # ------------------------------------------------------------------
    # Regime snapshot
    # ------------------------------------------------------------------
    print(f"\n[4/7] Regime snapshot...")
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
    # Adaptive selector (fresh instance — no state persistence here;
    # the API singleton in adaptive_weights_service owns persistent state)
    # ------------------------------------------------------------------
    print(f"\n[5/7] AdaptiveStrategySelector...")
    selector = AdaptiveStrategySelector(
        strategy_names=enabled_internals,
        rebalance_frequency_days=5,
        model="gpt-4o-mini",
        verbose=True,
        regime_stability_weeks=2,
    )
    weights = selector.rebalance(today_dt, regime_snapshot)
    regime_label = selector._confirmed_regime or broad_regime
    print(f"    Regime: {regime_label} | Weights: " +
          "  ".join(f"{k}={v:.2f}" for k, v in weights.items()))

    # ------------------------------------------------------------------
    # Portfolio from broker
    # ------------------------------------------------------------------
    print(f"\n[6/7] Syncing positions...")
    broker = PaperAdapter()
    portfolio, position_owners = _build_portfolio(broker, starting_capital)

    # ------------------------------------------------------------------
    # Signal generation
    # ------------------------------------------------------------------
    print(f"\n[7/7] Generating signals...")

    downtrend_count = sum(
        1 for s in daily_symbol_states.values()
        if isinstance(s.indicators.get("regime"), str)
        and "DOWNTREND" in s.indicators["regime"]
    )
    market_downtrend_pct = downtrend_count / len(daily_symbol_states)

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

    proposed = router.decide(today_dt, daily_symbol_states, portfolio)

    risk_agent = RiskAgent(
        max_position_pct=max_pos_pct,
        atr_multiplier=2.0,
        risk_per_trade_pct=risk_per_trade,
        use_vol_sizing=True,
        breadth_circuit_breaker=True,
        max_downtrend_pct=pause_pct,
        min_atr_cost_ratio=3.0,
    )

    final_decisions = []
    for decision in proposed:
        if decision is None:
            continue
        state = daily_symbol_states.get(decision.symbol)
        if state is None:
            continue
        if suppress_buys and decision.action == "BUY":
            continue
        risk_adj = risk_agent.evaluate(
            decision, portfolio, state,
            equity_prices={s: st.latest_price for s, st in daily_symbol_states.items()},
            market_downtrend_pct=effective_downtrend_pct,
        )
        final_decisions.append(risk_adj)

    buys  = [d for d in final_decisions if d.action == "BUY"]
    sells = [d for d in final_decisions if d.action == "SELL"]

    written = _write_signals(final_decisions, daily_symbol_states, regime_label, weights, today)

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------
    cb_active = effective_downtrend_pct >= pause_pct
    print(f"\n{'='*70}")
    print(f"  Paper Signal Summary — {today}")
    print(f"{'='*70}")
    print(f"  Session:         {session['session_id']}")
    print(f"  Regime:          {regime_label}  (broad={broad_regime}, trend={trend})")
    print(f"  Market breadth:  {market_downtrend_pct:.0%} raw → {effective_downtrend_pct:.0%} effective  "
          f"({'CB ACTIVE' if cb_active else 'CB clear'})")
    print(f"  Universe:        {len(daily_symbol_states)} symbols")
    print(f"  Signals written: {written}  (BUY: {len(buys)}, SELL: {len(sells)})")

    if buys:
        print("\n  BUY signals:")
        for d in buys:
            st = daily_symbol_states.get(d.symbol)
            print(f"    {d.symbol:<14} qty={d.quantity}  @ ₹{st.latest_price:.2f}  [{d.source}]")
    if sells:
        print("\n  SELL signals:")
        for d in sells:
            st = daily_symbol_states.get(d.symbol)
            print(f"    {d.symbol:<14} qty={d.quantity}  @ ₹{st.latest_price:.2f}  [{d.source}]")

    print(f"\n  Run run_orders.py tomorrow at 9:15 AM IST to place paper orders.")
    print(f"{'='*70}\n")

    send_email(
        subject=f"[FinLab Paper] Signals {today} — {regime_label} | BUY:{len(buys)} SELL:{len(sells)}",
        body=(
            f"Paper Trade Signal Report — {today}\n\n"
            f"Session:   {session['session_id']}\n"
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


if __name__ == "__main__":
    main()
