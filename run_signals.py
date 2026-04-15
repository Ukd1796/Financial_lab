#!/usr/bin/env python3
# run_signals.py
#
# ==============================================================
# DEPRECATED — do not run or schedule.
# Replaced by api/run_paper_signals.py which is session-aware
# and reads strategy config from the database (user_strategies /
# paper_trade_sessions tables).
# Remove from cron: was scheduled at  35 10 * * 1-5
# ==============================================================
#
# Daily signal generation job for live / paper trading.
# Schedule via cron at 3:35 PM IST on trading days:
#   35 10 * * 1-5 cd /path/to/Financial_lab && python run_signals.py >> logs/signals.log 2>&1
#
# Steps:
#   1. Check NSECalendar — exit if holiday
#   2. Fetch today's EOD OHLC via yfinance, upsert to DB
#   3. Load last 300 days of history for universe warm-up
#   4. Run DynamicUniverseAgent → top 80 candidates
#   5. Run UnionUniverseFilter → 60-80 active symbols
#   6. Run MarketObserver for each symbol → daily_symbol_states
#   7. Build regime_snapshot
#   8. Load/restore AdaptiveStrategySelector state from DB
#   9. Run AdaptiveStrategySelector.rebalance() → weight vector
#  10. Save updated selector state to DB
#  11. Sync live_positions from broker → reconstruct Portfolio
#  12. Run MultiStrategyRouter.decide() → proposed decisions
#  13. Run RiskAgent.evaluate() → risk-adjusted decisions
#  14. Write BUY/SELL decisions to signal_queue (status=PENDING)
#  15. Print session summary
#
# Paper trading: uses PaperAdapter (no real orders).
# Live trading:  swap PaperAdapter → KiteAdapter (not yet built).

import json
import os
import sys
import uuid
from datetime import date, datetime, timedelta

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
from sqlalchemy import select, text  # noqa: F401

# ---------------------------------------------------------------------------
# Universe
# ---------------------------------------------------------------------------
NIFTY_50 = [
    "RELIANCE", "TCS", "HDFCBANK", "BHARTIARTL", "ICICIBANK",
    "INFY", "SBIN", "HINDUNILVR", "ITC", "LT",
    "BAJFINANCE", "HCLTECH", "KOTAKBANK", "AXISBANK", "ASIANPAINT",
    "MARUTI", "SUNPHARMA", "TITAN", "ULTRACEMCO", "WIPRO",
    "NTPC", "POWERGRID", "NESTLEIND", "M&M", "TECHM",
    "BAJAJFINSV", "ADANIENT", "ADANIPORTS", "COALINDIA", "ONGC",
    "GRASIM", "TMCV", "TATASTEEL", "JSWSTEEL", "HINDALCO",
    "BRITANNIA", "DRREDDY", "DIVISLAB", "BPCL", "HDFCLIFE",
    "SBILIFE", "CIPLA", "APOLLOHOSP", "EICHERMOT", "HEROMOTOCO",
    "INDUSINDBK", "BAJAJ-AUTO", "TATACONSUM", "SHRIRAMFIN", "BEL",
]
NIFTY_NEXT_50 = [
    "ADANIGREEN", "AMBUJACEM", "ATGL", "BAJAJHLDNG", "BANKBARODA",
    "BERGEPAINT", "BOSCHLTD", "CANBK", "CHOLAFIN", "COLPAL",
    "DABUR", "DLF", "GODREJCP", "GODREJPROP", "HAVELLS",
    "HDFCAMC", "ICICIGI", "ICICIPRULI", "INDUSTOWER", "INDIGO",
    "IRCTC", "JSWENERGY", "LTIM", "LUPIN", "MUTHOOTFIN",
    "NAUKRI", "OFSS", "PFC", "PIDILITIND", "PNB",
    "RECLTD", "SIEMENS", "TATACOMM", "TATAPOWER", "TORNTPHARM",
    "TORNTPOWER", "UNIONBANK", "VEDL", "ETERNAL", "ZYDUSLIFE",
    "MARICO", "MOTHERSON", "OBEROIRLTY", "PAGEIND", "PERSISTENT",
    "POLYCAB", "SBICARD", "TRENT", "UPL", "VOLTAS",
]
NIFTY_MIDCAP_50 = [
    "ABB", "ABCAPITAL", "ABFRL", "ALKEM", "ASHOKLEY",
    "ASTRAL", "AUROPHARMA", "BALKRISIND", "BANKINDIA", "BHEL",
    "CANFINHOME", "CROMPTON", "CUMMINSIND", "DEEPAKNTR", "DIXON",
    "FEDERALBNK", "GLENMARK", "GLAXO", "GMRAIRPORT", "GNFC",
    "HFCL", "HINDPETRO", "IDFCFIRSTB", "INDIANB", "INDHOTEL",
    "JUBLFOOD", "KAJARIACER", "KPITTECH", "LALPATHLAB", "LAURUSLABS",
    "LICHSGFIN", "LTF", "MAXHEALTH", "METROPOLIS", "MFSL",
    "MPHASIS", "MRF", "NAVINFLUOR", "NMDC", "PIIND",
    "RAYMOND", "SAIL", "SCHAEFFLER", "SUNTV", "SUPREMEIND",
    "THERMAX", "TIINDIA", "TVSMOTOR", "WHIRLPOOL", "ZEEL",
]
BROAD_UNIVERSE = NIFTY_50 + NIFTY_NEXT_50 + NIFTY_MIDCAP_50

# ---------------------------------------------------------------------------
# Regime allowlists (mirrors run_experiments.py)
# ---------------------------------------------------------------------------
_UPTREND_ONLY = [
    "LOW_VOL_UPTREND", "MID_VOL_UPTREND", "HIGH_VOL_UPTREND",
]
_TREND_AND_SIDEWAYS = [
    "LOW_VOL_UPTREND",  "MID_VOL_UPTREND",  "HIGH_VOL_UPTREND",
    "LOW_VOL_SIDEWAYS", "MID_VOL_SIDEWAYS",  "HIGH_VOL_SIDEWAYS",
]
_UPTREND_AND_SIDEWAYS = [
    "LOW_VOL_UPTREND",  "MID_VOL_UPTREND",  "HIGH_VOL_UPTREND",
    "LOW_VOL_SIDEWAYS", "MID_VOL_SIDEWAYS",  "HIGH_VOL_SIDEWAYS",
]

_STRATEGY_NAMES = ["DualMA", "Breakout", "QuietBrk", "TrendPB", "RSI-MR"]

# ---------------------------------------------------------------------------
# Selector state persistence (uses selector_state DB table)
# ---------------------------------------------------------------------------

def _load_selector_state(selector: AdaptiveStrategySelector) -> None:
    """Restore AdaptiveStrategySelector from selector_state DB table."""
    session = SessionLocal()
    try:
        result = session.execute(
            text(
                "SELECT confirmed_regime, pending_regime, pending_count, "
                "weights_json, history_json, last_rebalanced "
                "FROM selector_state WHERE id = 1"
            )
        ).fetchone()
        if result is None:
            return   # first run — start fresh
        confirmed, pending, pending_count, weights_json, history_json, last_rebalanced = result
        selector._confirmed_regime  = confirmed
        selector._pending_regime    = pending
        selector._pending_count     = int(pending_count or 0)
        selector.weights            = json.loads(weights_json)
        selector._snapshot_history  = json.loads(history_json)
        if last_rebalanced:
            selector._last_updated  = datetime.combine(last_rebalanced, datetime.min.time())
        print(f"  [State] Restored selector state: regime={confirmed}, weights loaded")
    except Exception as exc:
        print(f"  [State] Could not load selector state ({exc}) — starting fresh")
    finally:
        session.close()


def _save_selector_state(selector: AdaptiveStrategySelector, rebalanced_today: bool) -> None:
    """Persist AdaptiveStrategySelector state to selector_state DB table."""
    session = SessionLocal()
    try:
        last_reb = selector._last_updated.date() if selector._last_updated else None
        session.execute(
            text(
                """
                INSERT INTO selector_state
                    (id, updated_at, confirmed_regime, pending_regime, pending_count,
                     weights_json, history_json, last_rebalanced)
                VALUES (1, :now, :conf, :pend, :pcount, :wj, :hj, :lr)
                ON CONFLICT (id) DO UPDATE SET
                    updated_at       = EXCLUDED.updated_at,
                    confirmed_regime = EXCLUDED.confirmed_regime,
                    pending_regime   = EXCLUDED.pending_regime,
                    pending_count    = EXCLUDED.pending_count,
                    weights_json     = EXCLUDED.weights_json,
                    history_json     = EXCLUDED.history_json,
                    last_rebalanced  = EXCLUDED.last_rebalanced
                """
            ),
            {
                "now":    datetime.utcnow(),
                "conf":   selector._confirmed_regime,
                "pend":   selector._pending_regime,
                "pcount": selector._pending_count,
                "wj":     json.dumps(selector.weights),
                "hj":     json.dumps(selector._snapshot_history),
                "lr":     last_reb,
            }
        )
        session.commit()
        print(f"  [State] Selector state saved (regime={selector._confirmed_regime})")
    except Exception as exc:
        print(f"  [State] Could not save selector state ({exc})")
    finally:
        session.close()

# ---------------------------------------------------------------------------
# Paper trading capital helpers
# ---------------------------------------------------------------------------

def _get_paper_starting_capital() -> float:
    """
    Read starting_capital from the most-recent active paper_trade_sessions row in Supabase B.
    Falls back to PAPER_CAPITAL env var, then to 500_000.
    """
    default = float(os.environ.get("PAPER_CAPITAL", 500_000))
    try:
        from sqlalchemy import text as _text
        db = SessionLocal()
        try:
            row = db.execute(_text(
                "SELECT starting_capital FROM paper_trade_sessions "
                "WHERE status = 'active' ORDER BY created_at DESC LIMIT 1"
            )).fetchone()
            if row:
                return float(row[0])
        finally:
            db.close()
    except Exception as exc:
        print(f"  [Portfolio] Could not read paper_trade_sessions ({exc}) — using default ₹{default:,.0f}")
    return default


# ---------------------------------------------------------------------------
# Position sync from broker → Portfolio
# ---------------------------------------------------------------------------

def _build_portfolio_from_broker(broker: PaperAdapter) -> tuple[Portfolio, dict]:
    """
    Read live_positions from broker adapter and build a Portfolio object.
    Cash = starting_capital (from paper_sessions) minus deployed capital
    (sum of quantity × average_price for all open positions).
    Returns (Portfolio, position_owners_dict).
    """
    starting_capital = _get_paper_starting_capital()
    position_owners  = {}
    positions        = broker.get_positions()

    deployed_capital = sum(p.quantity * p.average_price for p in positions)
    cash             = max(starting_capital - deployed_capital, 0.0)

    portfolio = Portfolio(cash=cash)
    for pos in positions:
        portfolio.positions[pos.symbol] = type(
            "Position", (), {
                "quantity":      pos.quantity,
                "average_price": pos.average_price,
            }
        )()
        position_owners[pos.symbol] = pos.strategy

    print(f"    Starting capital: ₹{starting_capital:,.0f}  |  "
          f"Deployed: ₹{deployed_capital:,.0f}  |  Cash: ₹{cash:,.0f}")
    return portfolio, position_owners


# ---------------------------------------------------------------------------
# Write signals to signal_queue
# ---------------------------------------------------------------------------

def _write_signals(
    decisions: list,
    daily_symbol_states: dict,
    regime_label: str,
    weights: dict,
    signal_date: date,
) -> int:
    """Write BUY/SELL decisions to signal_queue. Returns count written."""
    session = SessionLocal()
    count = 0
    now   = datetime.utcnow()
    try:
        for decision in decisions:
            if decision.action not in ("BUY", "SELL"):
                continue
            if decision.quantity is None or decision.quantity <= 0:
                continue

            state = daily_symbol_states.get(decision.symbol)
            if state is None:
                continue

            row = SignalQueue(
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
            )
            session.add(row)
            count += 1

        session.commit()
    finally:
        session.close()
    return count


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------

def main():
    today     = date.today()
    today_dt  = datetime.combine(today, datetime.min.time())
    calendar  = NSECalendar()

    # ------------------------------------------------------------------
    # Step 1: Calendar check
    # ------------------------------------------------------------------
    if not calendar.is_trading_day(today):
        print(f"[run_signals] {today} is not a trading day — exiting.")
        sys.exit(0)

    print(f"\n{'='*70}")
    print(f"  run_signals.py — {today}  (paper trading)")
    print(f"{'='*70}")

    # Manual override: suppress all new BUY signals (set env var on high-uncertainty days)
    suppress_buys = os.environ.get("SUPPRESS_NEW_BUYS", "0") == "1"
    if suppress_buys:
        print("  *** SUPPRESS_NEW_BUYS=1 — no new BUY signals will be generated ***")

    # ------------------------------------------------------------------
    # Step 2: Fetch today's EOD data and upsert to DB
    # ------------------------------------------------------------------
    print(f"\n[1/8] Fetching today's EOD data for {len(BROAD_UNIVERSE)} symbols...")
    provider   = YFinanceProvider()
    repository = MarketDataRepository()

    fetch_errors = []
    fetched = 0
    for symbol in BROAD_UNIVERSE:
        try:
            records = provider.fetch_ohlc(symbol, start=today, end=today + timedelta(days=1))
            if records:
                repository.bulk_upsert(records)
                fetched += 1
        except Exception as exc:
            fetch_errors.append(f"{symbol}: {exc}")

    print(f"    Fetched: {fetched} symbols | Errors: {len(fetch_errors)}")
    if fetch_errors:
        print(f"    First errors: {fetch_errors[:3]}")

    # ------------------------------------------------------------------
    # Step 3: Load last 300 days of history for indicator warm-up
    # ------------------------------------------------------------------
    print(f"\n[2/8] Loading 300-day history for universe warm-up...")
    warmup_start = today - timedelta(days=300)
    start_dt     = datetime.combine(warmup_start, datetime.min.time())

    # ------------------------------------------------------------------
    # Step 4-5: Universe selection
    # ------------------------------------------------------------------
    print(f"\n[3/8] Running DynamicUniverseAgent → UnionUniverseFilter...")
    dynamic_agent = DynamicUniverseAgent(
        repository=repository,
        symbols=BROAD_UNIVERSE,
        top_n=80,
    )
    dynamic_agent.preload(start_dt, today_dt)
    rca = RegimeContextAgent(dynamic_agent)
    broad_candidates = dynamic_agent.select_candidates(today_dt)

    union_filter = UnionUniverseFilter([
        BreakoutUniverseFilter(top_n=20),
        BreakoutUniverseFilter(vol_threshold=1.2, return_threshold=0.008, top_n=20),
        PullbackUniverseFilter(top_n=20),
        MeanReversionUniverseFilter(top_n=20),
        DualMAUniverseFilter(max_cross_age=5, top_n=30),
    ])
    active_symbols = union_filter.select_symbols(broad_candidates)
    print(f"    Top 80 candidates → {len(active_symbols)} active symbols after union filter")

    # ------------------------------------------------------------------
    # Step 6: MarketObserver → daily_symbol_states
    # ------------------------------------------------------------------
    print(f"\n[4/8] Computing market states for {len(active_symbols)} symbols...")
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

    print(f"    Market states computed: {len(daily_symbol_states)} symbols")
    if not daily_symbol_states:
        print("    No market states available — exiting.")
        sys.exit(1)

    # ------------------------------------------------------------------
    # Step 7: Build regime snapshot
    # ------------------------------------------------------------------
    print(f"\n[5/8] Building regime snapshot (RegimeContextAgent)...")
    regime_snapshot = rca.build_snapshot(daily_symbol_states, today_dt)
    broad_regime = regime_snapshot.get("broad_regime", "UNKNOWN")
    trend        = regime_snapshot.get("trend", "STABLE")
    pct_above    = regime_snapshot.get("pct_above_sma50_broad", 0.0)
    adv_dec      = regime_snapshot.get("advance_decline_ratio", 0.0)
    print(
        f"    UP={regime_snapshot['pct_uptrend']:.1%}  "
        f"DOWN={regime_snapshot['pct_downtrend']:.1%}  "
        f"ATR={regime_snapshot['avg_atr_pct']:.2%}  "
        f"Universe={regime_snapshot['universe_size']}"
    )
    print(
        f"    Broad regime: {broad_regime}  trend={trend}  "
        f"above_SMA50={pct_above:.1%}  A/D={adv_dec:.1%}  "
        f"broad_n={regime_snapshot.get('broad_universe_size', 0)}"
    )

    # ------------------------------------------------------------------
    # Step 8-9: Adaptive selector — load state, rebalance, save state
    # ------------------------------------------------------------------
    print(f"\n[6/8] Running AdaptiveStrategySelector...")
    selector = AdaptiveStrategySelector(
        strategy_names=_STRATEGY_NAMES,
        rebalance_frequency_days=5,
        model="gpt-4o-mini",
        verbose=True,
        regime_stability_weeks=2,
    )
    _load_selector_state(selector)
    weights = selector.rebalance(today_dt, regime_snapshot)
    _save_selector_state(selector, rebalanced_today=True)

    regime_label = selector._confirmed_regime or "UNKNOWN"
    print(f"    Regime: {regime_label} | Weights: " +
          "  ".join(f"{k}={v:.2f}" for k, v in weights.items()))

    # ------------------------------------------------------------------
    # Step 10-11: Portfolio from broker + position_owners
    # ------------------------------------------------------------------
    print(f"\n[7/8] Syncing live positions from broker...")
    broker   = PaperAdapter()
    portfolio, position_owners = _build_portfolio_from_broker(broker)
    print(f"    Open positions: {len(portfolio.positions)}")

    # ------------------------------------------------------------------
    # Step 12-13: Strategy → Risk evaluation
    # ------------------------------------------------------------------
    print(f"\n[8/8] Generating signals...")

    downtrend_count = sum(
        1 for s in daily_symbol_states.values()
        if isinstance(s.indicators.get("regime"), str)
        and "DOWNTREND" in s.indicators["regime"]
    )
    market_downtrend_pct = downtrend_count / len(daily_symbol_states)

    # CB relaxation: TRANSITION_UP → cap at 30%, BEAR_WATCH/BEAR_TRANSITION → cap at 38%
    if broad_regime == "TRANSITION_UP":
        effective_downtrend_pct = min(market_downtrend_pct, 0.30)
        print(f"    [RCA] TRANSITION_UP — CB relaxed: raw={market_downtrend_pct:.0%} → effective={effective_downtrend_pct:.0%}")
    elif broad_regime in ("BEAR_WATCH", "BEAR_TRANSITION"):
        effective_downtrend_pct = min(market_downtrend_pct, 0.38)
        print(f"    [RCA] {broad_regime} — CB slightly relaxed: raw={market_downtrend_pct:.0%} → effective={effective_downtrend_pct:.0%}")
    else:
        effective_downtrend_pct = market_downtrend_pct

    router = MultiStrategyRouter(
        strategies={
            "DualMA":   DualMovingAverageStrategy(),
            "Breakout": BreakoutMomentumStrategy(),
            "QuietBrk": QuietBreakoutStrategy(),
            "TrendPB":  TrendPullbackStrategy(pullback_threshold=0.05),
            "RSI-MR":   RSIMeanReversionStrategy(
                            rsi_oversold=5, rsi_overbought=80, max_hold_days=7),
        },
        weights=weights,
        allowed_regimes={
            "DualMA":   _UPTREND_ONLY,
            "Breakout": _TREND_AND_SIDEWAYS,
            "QuietBrk": _UPTREND_ONLY,
            "TrendPB":  _TREND_AND_SIDEWAYS,
            "RSI-MR":   _UPTREND_AND_SIDEWAYS,
        },
    )
    # Restore ownership tracking from broker positions
    router.position_owners = position_owners

    proposed = router.decide(today_dt, daily_symbol_states, portfolio)

    risk_agent = RiskAgent(
        max_position_pct=0.10,
        atr_multiplier=2.0,
        risk_per_trade_pct=0.005,
        use_vol_sizing=True,
        breadth_circuit_breaker=True,
        max_downtrend_pct=0.70,
        min_atr_cost_ratio=3.0,
    )

    final_decisions = []
    for decision in proposed:
        if decision is None:
            continue
        state = daily_symbol_states.get(decision.symbol)
        if state is None:
            continue

        # Suppress new BUY signals if override flag is set
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

    # ------------------------------------------------------------------
    # Step 14: Write to signal_queue
    # ------------------------------------------------------------------
    written = _write_signals(
        final_decisions, daily_symbol_states,
        regime_label, weights, today,
    )

    # ------------------------------------------------------------------
    # Step 15: Summary
    # ------------------------------------------------------------------
    print(f"\n{'='*70}")
    print(f"  Signal Summary — {today}")
    print(f"{'='*70}")
    print(f"  Regime:          {regime_label}")
    print(f"  Broad regime:    {broad_regime}  (trend={trend}, above_SMA50={pct_above:.1%})")
    print(f"  Market breadth:  {market_downtrend_pct:.0%} DOWNTREND raw  →  "
          f"{effective_downtrend_pct:.0%} effective "
          f"({'CB ACTIVE' if effective_downtrend_pct >= 0.35 else 'CB clear'})")
    print(f"  Universe:        {len(daily_symbol_states)} symbols")
    print(f"  Signals written: {written}  (BUY: {len(buys)}, SELL: {len(sells)})")
    print()

    if buys:
        print("  BUY signals:")
        for d in buys:
            state = daily_symbol_states.get(d.symbol)
            price = state.latest_price if state else 0
            print(f"    {d.symbol:<14} qty={d.quantity}  @ ₹{price:.2f}  [{d.source}]")

    if sells:
        print("  SELL signals:")
        for d in sells:
            state = daily_symbol_states.get(d.symbol)
            price = state.latest_price if state else 0
            print(f"    {d.symbol:<14} qty={d.quantity}  @ ₹{price:.2f}  [{d.source}]")

    print()
    print(f"  Run run_orders.py tomorrow at 9:15 AM IST to place paper orders.")
    print(f"{'='*70}\n")

    # ------------------------------------------------------------------
    # Email summary
    # ------------------------------------------------------------------
    cb_status = "ACTIVE — BUYs suppressed" if effective_downtrend_pct >= 0.35 else "clear"
    buy_lines  = "\n".join(
        f"  BUY  {d.symbol:<14} qty={d.quantity}  @ ₹{daily_symbol_states[d.symbol].latest_price:.2f}  [{d.source}]"
        for d in buys if d.symbol in daily_symbol_states
    ) or "  (none)"
    sell_lines = "\n".join(
        f"  SELL {d.symbol:<14} qty={d.quantity}  @ ₹{daily_symbol_states[d.symbol].latest_price:.2f}  [{d.source}]"
        for d in sells if d.symbol in daily_symbol_states
    ) or "  (none)"

    email_body = f"""Financial Lab — Signal Report {today}

Regime:        {regime_label}
Broad regime:  {broad_regime}  (trend={trend}, above_SMA50={pct_above:.1%}, A/D={adv_dec:.1%})
Breadth:       {market_downtrend_pct:.0%} DOWNTREND raw  →  {effective_downtrend_pct:.0%} effective  (CB {cb_status})
Universe: {len(daily_symbol_states)} symbols
Weights:  {' '.join(f'{k}={v:.2f}' for k, v in weights.items())}

BUY signals ({len(buys)}):
{buy_lines}

SELL signals ({len(sells)}):
{sell_lines}

Total signals written: {written}
Paper fills will be confirmed by run_orders.py at 9:15 AM IST tomorrow.
"""
    send_email(
        subject=f"[FinLab] Signals {today} — {regime_label} | BUY:{len(buys)} SELL:{len(sells)}",
        body=email_body,
    )


if __name__ == "__main__":
    main()
