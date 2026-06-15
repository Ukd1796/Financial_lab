import os
from datetime import datetime

from dotenv import load_dotenv
load_dotenv()

# Skip solo strategies + EqualWeight baseline when set; run only Adaptive +
# Adaptive+RCA. Useful when iterating on the meta-layer (MFE-lock, RCA tuning,
# prompt changes) where solo/EqW runs are unaffected and just slow the loop.
# Set ADAPTIVE_ONLY=1 to enable.
ADAPTIVE_ONLY = os.environ.get("ADAPTIVE_ONLY", "0") != "0"
# Skip Adaptive (LLM) and RCA runs — run only solo strategies + EqualWeight.
# Useful for fast diagnostics (no LLM cost, ~3× faster).
EQW_ONLY = os.environ.get("EQW_ONLY", "0") != "0"

from app.backtest.engine import BacktestEngine
from app.backtest.observer import MarketObserverAgent
from app.data.repository import MarketDataRepository
from app.evaluation.agent import EvaluationAgent
from app.execution.agent import ExecutionAgent
from app.portfolio.engine import PortfolioEngine
from app.portfolio.models import Portfolio
from app.risk.agent import RiskAgent
from app.strategy.breakout_momentum import BreakoutMomentumStrategy
from app.strategy.dual_ma import DualMovingAverageStrategy
from app.strategy.multi_router import MultiStrategyRouter
from app.strategy.quiet_breakout import QuietBreakoutStrategy
from app.strategy.rsi_mean_reversion import RSIMeanReversionStrategy
from app.strategy.trend_pullback import TrendPullbackStrategy
from app.universe.dynamic_agent import DynamicUniverseAgent
from app.meta.adaptive_selector import AdaptiveStrategySelector
from app.meta.regime_context_agent import RegimeContextAgent
from app.universe.filters import (
    ActivityTailFilter,
    BreakoutUniverseFilter,
    DualMAUniverseFilter,
    MeanReversionUniverseFilter,
    PullbackUniverseFilter,
    UnionUniverseFilter,
)
from app.analytics.trade_annotator import (
    TradeAnnotator,
    TradeAttributionTracker,
    export_enriched_trades_csv,
)
from app.analytics.opportunity_quality import (
    compute_opportunity_quality_metrics,
    print_opportunity_quality_summary,
)
from app.analytics.ensemble_diagnostics import (
    compute_ensemble_metrics,
    print_ensemble_summary,
)
from app.analytics.universe_tracker import compute_universe_diagnostics

# -----------------------------------------------------------------------
# Full symbol universe — mirrors scripts/ingest_symbols.py
# -----------------------------------------------------------------------
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

# All symbols available in the database
BROAD_UNIVERSE = NIFTY_50 + NIFTY_NEXT_50 + NIFTY_MIDCAP_50

INITIAL_CAPITAL = 100_000

# Set to True to run Priority 5 walk-forward validation (~20 extra backtest runs, slow).
RUN_WALK_FORWARD = False

# -----------------------------------------------------------------------
# Regime sets — passed per-strategy to RiskAgent
# -----------------------------------------------------------------------
# Medium-term strategies: only enter in established uptrends
_UPTREND_ONLY = [
    "LOW_VOL_UPTREND", "MID_VOL_UPTREND", "HIGH_VOL_UPTREND",
]

# Short-term breakout / pullback: uptrend or sideways (momentum still present)
_TREND_AND_SIDEWAYS = [
    "LOW_VOL_UPTREND",   "MID_VOL_UPTREND",   "HIGH_VOL_UPTREND",
    "LOW_VOL_SIDEWAYS",  "MID_VOL_SIDEWAYS",  "HIGH_VOL_SIDEWAYS",
]

# Mean-reversion: works in any regime — None disables the filter entirely
_ALL_REGIMES = None

# Mean-reversion restricted to uptrend/sideways: "oversold in an uptrend"
# Prevents RSI-MR from catching falling knives in downtrending stocks.
_UPTREND_AND_SIDEWAYS = [
    "LOW_VOL_UPTREND",  "MID_VOL_UPTREND",  "HIGH_VOL_UPTREND",
    "LOW_VOL_SIDEWAYS", "MID_VOL_SIDEWAYS",  "HIGH_VOL_SIDEWAYS",
]

# -----------------------------------------------------------------------
# Time periods
# -----------------------------------------------------------------------
PERIODS = {
    "Bull  2019–2020": (datetime(2019, 1, 1),  datetime(2020, 2, 1)),
    "Crash 2020     ": (datetime(2020, 1, 1),  datetime(2020, 12, 31)),
    "Recov 2020–2021": (datetime(2020, 4, 1),  datetime(2021, 12, 31)),
    "Bear  2022     ": (datetime(2022, 1, 1),  datetime(2022, 12, 31)),
    "Recent2022–2024": (datetime(2022, 1, 1),  datetime(2024, 6, 1)),
    "Live  2025–2026": (datetime(2025, 1, 1),  datetime(2026, 3, 24)),
}

# -----------------------------------------------------------------------
# Strategy registry
#
# Each entry:
#   label           — display name (max ~22 chars for column alignment)
#   factory         — callable returning a *fresh* strategy instance
#   max_pos_pct     — max allocation per position passed to RiskAgent
#   allowed_regimes — regime gate for RiskAgent:
#                       _UPTREND_ONLY      → medium-term trend strategies
#                       _TREND_AND_SIDEWAYS → short-term momentum strategies
#                       _ALL_REGIMES (None) → mean-reversion (no gate)
#   group           — section header for the printed table
# -----------------------------------------------------------------------
STRATEGIES = [
    # ---- Medium-term trend strategies (golden cross, uptrend regime only) ----
    {
        "label":           "DualMA SMA20/50",
        "factory":         lambda: DualMovingAverageStrategy(),
        "universe_filter": lambda: DualMAUniverseFilter(max_cross_age=5, top_n=30),
        "max_pos_pct":     0.15,
        "allowed_regimes": _UPTREND_ONLY,
        "group":           "Medium-term",
    },

    # ---- Short-term momentum strategies (uptrend + sideways) ---------
    {
        "label":            "Breakout 10d",
        "factory":          lambda: BreakoutMomentumStrategy(),
        "universe_filter":  lambda: BreakoutUniverseFilter(top_n=20),
        "max_pos_pct":      0.10,
        "allowed_regimes":  _TREND_AND_SIDEWAYS,
        "group":            "Short-term",
    },
    {
        # Quiet variant: 20-day breakout with relaxed activity thresholds.
        # Targets slow-bull conditions where 10d breakout starves for signals.
        # UPTREND_ONLY (not TREND_AND_SIDEWAYS) because QuietBrk loses -10% in Bear
        # when SIDEWAYS entries are allowed — stocks classified SIDEWAYS during a
        # rolling bear are often in early breakdown, not genuine consolidation.
        "label":            "QuietBrk 20d",
        "factory":          lambda: QuietBreakoutStrategy(),
        "universe_filter":  lambda: BreakoutUniverseFilter(
                                vol_threshold=1.2,
                                return_threshold=0.008,
                                top_n=20,
                            ),
        "max_pos_pct":      0.10,
        "allowed_regimes":  _UPTREND_ONLY,
        "group":            "Short-term",
    },
    {
        "label":            "TrendPB v2 pct=3%",
        "factory":          lambda: TrendPullbackStrategy(pullback_threshold=0.03),
        "universe_filter":  lambda: PullbackUniverseFilter(top_n=20),
        "max_pos_pct":      0.10,
        "allowed_regimes":  _TREND_AND_SIDEWAYS,
        "group":            "Short-term",
    },
    {
        "label":            "TrendPB v2 pct=5%",
        "factory":          lambda: TrendPullbackStrategy(pullback_threshold=0.05),
        "universe_filter":  lambda: PullbackUniverseFilter(top_n=20),
        "max_pos_pct":      0.10,
        "allowed_regimes":  _TREND_AND_SIDEWAYS,
        "group":            "Short-term",
    },

    # ---- Mean-reversion strategies (uptrend/sideways only + breadth circuit breaker) --
    # Both the universe filter (stock-level) and allowed_regimes (per-decision gate in
    # RiskAgent) enforce the "oversold in an uptrend only" rule at two independent layers.
    {
        "label":                   "RSI-MR  os=5  ob=80",
        "factory":                 lambda: RSIMeanReversionStrategy(
                                       rsi_oversold=5,  rsi_overbought=80, max_hold_days=7),
        "universe_filter":         lambda: MeanReversionUniverseFilter(top_n=20),
        "max_pos_pct":             0.10,
        "allowed_regimes":         _UPTREND_AND_SIDEWAYS,
        "breadth_circuit_breaker": True,
        "group":                   "Mean-reversion",
    },
]


# -----------------------------------------------------------------------
# Period-level context (built once per period, shared across strategies)
# -----------------------------------------------------------------------
class PeriodContext:
    """
    Holds everything that is identical for every strategy in a given period:
      - dynamic_universe_agent  : preloaded once (bulk DB fetch for all 150 symbols)
      - observer                : read-only MarketState cache, lazy-loaded per symbol
                                  on first encounter and then reused by later strategies
      - historical_dates        : sorted list of trading days in the period
    """

    def __init__(self, repository, start_date, end_date):
        self.start_date = start_date
        self.end_date   = end_date

        # Stage 1 — bulk preload once for all 150 symbols
        self.dynamic_universe_agent = DynamicUniverseAgent(
            repository=repository,
            symbols=BROAD_UNIVERSE,
            top_n=80,
        )
        self.dynamic_universe_agent.preload(start_date, end_date)

        # Observer cache grows lazily; safe to share across strategies because
        # it stores only read-only MarketState (no portfolio state).
        self.observer = MarketObserverAgent(repository)

        # Price feed for CrossSectionalMomentumStrategy — extracted from the
        # dynamic agent's cache (already buffered 200 days before start_date)
        # so CS can compute N-day lookback from day 1 of the period.
        self.price_feed = self.dynamic_universe_agent.get_price_feed()

        # RegimeContextAgent — enhanced regime snapshot with broad breadth signals.
        # Uses the DynamicUniverseAgent cache (already loaded) — zero extra DB queries.
        self.regime_context_agent = RegimeContextAgent(self.dynamic_universe_agent)

        # Timeline derived from the DynamicUniverseAgent cache — avoids a
        # second round-trip to the DB (the bulk fetch above already loaded
        # all 150 symbols, so re-querying 150× would double the bandwidth).
        self.historical_dates = self._build_timeline_from_cache()

    def _build_timeline_from_cache(self):
        """
        Extract the sorted list of trading-day timestamps from the already-loaded
        DynamicUniverseAgent cache, filtered to [start_date, end_date].
        No DB query — zero extra bandwidth.
        """
        timestamps = set()
        for df in self.dynamic_universe_agent._cache.values():
            for ts in df.index:
                if self.start_date <= ts <= self.end_date:
                    timestamps.add(ts)
        return sorted(timestamps)


# -----------------------------------------------------------------------
# Single backtest run  (receives shared period context)
# -----------------------------------------------------------------------
def run_experiment(repository, strategy, ctx: PeriodContext, max_position_pct=0.20, allowed_regimes=None, breadth_circuit_breaker=False, universe_filter=None, adaptive_selector=None, max_downtrend_pct=0.40, min_atr_cost_ratio=0.0, regime_context_agent=None, pnl_tracker=None, regime_multipliers=None, no_atr_stop_strategies=None):

    if not ctx.historical_dates:
        return None

    # Give CS strategy access to the pre-built price feed so it can compute
    # momentum lookbacks from real historical data instead of accumulating
    # prices day-by-day from the rotating filtered universe.
    if hasattr(strategy, "preload_price_feed"):
        strategy.preload_price_feed(ctx.price_feed)

    portfolio        = Portfolio(cash=INITIAL_CAPITAL)
    portfolio_engine = PortfolioEngine(portfolio)
    execution_agent  = ExecutionAgent(
        portfolio_engine,
        commission_pct=0.001,   # 0.10% per side
        slippage_pct=0.0005,    # 0.05% per side
    )
    risk_agent       = RiskAgent(
        max_position_pct=max_position_pct,
        atr_multiplier=2.0,
        allowed_regimes=allowed_regimes,
        risk_per_trade_pct=0.005,      # risk 0.5% of portfolio per trade
        use_vol_sizing=True,
        breadth_circuit_breaker=breadth_circuit_breaker,
        max_downtrend_pct=max_downtrend_pct,
        min_atr_cost_ratio=min_atr_cost_ratio,
        regime_multipliers=regime_multipliers,
        no_atr_stop_strategies=no_atr_stop_strategies,
    )

    active_universe_agent = universe_filter

    engine = BacktestEngine(
        observer=ctx.observer,
        strategy_router=strategy,
        risk_agent=risk_agent,
        execution_agent=execution_agent,
        portfolio=portfolio,
        repository=None,   # no decision logging during backtests — avoids DB timeouts
        dynamic_universe_agent=ctx.dynamic_universe_agent,
        universe_agent=active_universe_agent,
        adaptive_selector=adaptive_selector,
        regime_context_agent=regime_context_agent,
        pnl_tracker=pnl_tracker,
    )

    results, trades = engine.run(BROAD_UNIVERSE, ctx.historical_dates)

    evaluator         = EvaluationAgent()
    portfolio_metrics = evaluator.evaluate(results, INITIAL_CAPITAL)
    trade_metrics     = evaluator.evaluate_trades(trades)

    return {"portfolio_metrics": portfolio_metrics, "trade_metrics": trade_metrics, "trades": trades}


# -----------------------------------------------------------------------
# Print helpers
# -----------------------------------------------------------------------
COL_W   = 22
ROW_W   = COL_W + 46
HEADER  = f"  {'Strategy':<{COL_W}} {'Sharpe':>6} {'Return':>9} {'MaxDD':>8} {'PF':>7} {'WR':>6} {'#Trades':>8}"
DIVIDER = f"  {'-' * ROW_W}"


def _print_row(label, result):
    if result is None:
        print(f"  {label:<{COL_W}}  (no data)")
        return

    pm = result["portfolio_metrics"]
    tm = result["trade_metrics"]

    sharpe  = pm.get("sharpe_ratio",  0.0) or 0.0
    ret     = pm.get("total_return",  0.0) or 0.0
    dd      = pm.get("max_drawdown",  0.0) or 0.0
    pf      = tm.get("profit_factor",  0.0) or 0.0
    wr      = tm.get("win_rate_trade", 0.0) or 0.0
    n       = tm.get("num_trades",     0)

    print(
        f"  {label:<{COL_W}} "
        f"{sharpe:>6.2f} "
        f"{ret * 100:>8.2f}% "
        f"{dd * 100:>7.2f}% "
        f"{pf:>7.2f} "
        f"{wr * 100:>5.1f}% "
        f"{n:>8}"
    )


def _print_router_diagnostics(label: str, router) -> None:
    """Per-strategy signal-drop counters from MultiStrategyRouter.diag_counters."""
    counters = getattr(router, "diag_counters", None)
    if not counters:
        return
    if not any(c.get("signals_issued", 0) > 0 for c in counters.values()):
        return
    print(f"  {'-' * ROW_W}  [{label} — signal-drop diagnostics]")
    print(
        f"  {'Strategy':<12}"
        f"{'issued':>9}{'won':>8}{'prio_loss':>11}"
        f"{'own_block':>11}{'buy_rej':>9}{'pass_thru%':>12}"
    )
    for name, c in counters.items():
        issued   = c.get("signals_issued",    0)
        won      = c.get("won_merge",         0)
        prio     = c.get("dropped_priority",  0)
        own      = c.get("dropped_ownership", 0)
        buy_rej  = c.get("buy_rejected",      0)
        survivors = max(won - buy_rej, 0)
        pct = (survivors / issued * 100.0) if issued > 0 else 0.0
        print(
            f"  {name:<12}"
            f"{issued:>9}{won:>8}{prio:>11}{own:>11}{buy_rej:>9}{pct:>11.1f}%"
        )


def _print_universe_overlap(label: str, universe_filter) -> None:
    """Per-child overlap counts from UnionUniverseFilter — confirms structurally
    orthogonal slices when mean/day is small. Used to track QuietBrk carve-out."""
    get_stats = getattr(universe_filter, "get_overlap_stats", None)
    if get_stats is None:
        return
    stats = get_stats()
    if not stats:
        return
    print(f"\n  {'-' * ROW_W}  [{label} — union-filter overlap (per trading day)]")
    print(f"  {'Filter':<32}{'total':>9}{'max/day':>10}{'mean/day':>11}")
    for s in stats:
        print(f"  {s['name']:<32}{s['total_absorbed']:>9}{s['max_absorbed_in_a_call']:>10}{s['mean_per_call']:>11.2f}")


def _print_exit_attribution(trades: list, label: str = "") -> None:
    """Break down exits by reason (ATR stop vs strategy) and by strategy."""
    from collections import defaultdict
    if not trades:
        return

    by_reason: dict = defaultdict(list)   # reason → [pnl]
    by_strat:  dict = defaultdict(lambda: defaultdict(list))  # strat → reason → [pnl]

    for t in trades:
        reason = getattr(t, "exit_reason", "") or "unknown"
        strat  = getattr(t, "strategy",    "") or "Unknown"
        by_reason[reason].append(t.pnl)
        by_strat[strat][reason].append(t.pnl)

    total = len(trades)
    title = f"Exit Attribution — {label}" if label else "Exit Attribution"
    print(f"\n  {'-' * ROW_W}  [{title}]")
    print(f"  {'Reason':<14} {'Trades':>8} {'  %':>5}  {'WinRate':>8}  {'Avg PnL':>9}  {'Total PnL':>11}")
    for reason in ("atr_stop", "strategy", "unknown"):
        pnls = by_reason.get(reason, [])
        if not pnls:
            continue
        n    = len(pnls)
        wr   = sum(1 for p in pnls if p > 0) / n * 100
        avg  = sum(pnls) / n
        tot  = sum(pnls)
        pct  = n / total * 100
        print(f"  {reason:<14} {n:>8} {pct:>5.1f}% {wr:>7.1f}% {avg:>+10.1f} {tot:>+11.0f}")

    print(f"\n  {'Strategy':<12} {'ATR%':>6} {'Strat%':>7}  {'ATR WR':>7}  {'Strat WR':>9}  {'ATR Avg':>8}  {'Strat Avg':>10}")
    for strat in sorted(by_strat):
        atr   = by_strat[strat].get("atr_stop", [])
        stg   = by_strat[strat].get("strategy", [])
        n_tot = len(atr) + len(stg)
        if n_tot == 0:
            continue
        atr_pct  = len(atr) / n_tot * 100 if n_tot else 0
        stg_pct  = len(stg) / n_tot * 100 if n_tot else 0
        atr_wr   = sum(1 for p in atr if p > 0) / len(atr) * 100 if atr else 0
        stg_wr   = sum(1 for p in stg if p > 0) / len(stg) * 100 if stg else 0
        atr_avg  = sum(atr) / len(atr) if atr else 0
        stg_avg  = sum(stg) / len(stg) if stg else 0
        print(
            f"  {strat:<12} {atr_pct:>5.1f}% {stg_pct:>6.1f}%"
            f" {atr_wr:>7.1f}% {stg_wr:>9.1f}%"
            f" {atr_avg:>+8.1f} {stg_avg:>+10.1f}"
        )


def _print_strategy_attribution(attrib: "TradeAttributionTracker", label: str = "") -> None:
    """Print per-strategy PnL contribution breakdown from a TradeAttributionTracker."""
    from collections import defaultdict
    buckets: dict = defaultdict(list)
    for _date, pnl, strategy in attrib._sells:
        buckets[strategy or "Unknown"].append(pnl)
    if not buckets:
        return
    total_pnl = sum(p for ps in buckets.values() for p in ps)
    title = f"Strategy PnL Attribution — {label}" if label else "Strategy PnL Attribution"
    print(f"\n  {'-' * ROW_W}  [{title}]")
    print(f"  {'Strategy':<12} {'Trades':>8} {'PnL (₹)':>12} {'WinRate':>9} {'Avg/trade':>11} {'Share%':>8}")
    print(f"  {'-' * 64}")
    for name in sorted(buckets, key=lambda s: sum(buckets[s]), reverse=True):
        trades = buckets[name]
        n      = len(trades)
        pnl    = sum(trades)
        wins   = sum(1 for p in trades if p > 0)
        wr     = wins / n * 100 if n else 0.0
        avg    = pnl / n if n else 0.0
        share  = pnl / total_pnl * 100 if total_pnl else 0.0
        print(
            f"  {name:<12} {n:>8} {pnl:>+12.0f} {wr:>8.1f}% {avg:>+10.0f} {share:>7.1f}%"
        )
    print(f"  {'TOTAL':<12} {sum(len(v) for v in buckets.values()):>8} {total_pnl:>+12.0f}")


# -----------------------------------------------------------------------
# In-process OHLC cache (eliminates duplicate DB fetches across periods)
# -----------------------------------------------------------------------

class OHLCCache:
    """
    In-process read-through cache for OHLC data.

    Strategy
    --------
    Call warm_all() once at startup with a date range that covers every
    period you intend to run (including walk-forward sub-periods and their
    200–300-day warm-up buffers).  All subsequent get_ohlc / get_ohlc_bulk
    calls are served from memory as list slices — zero DB round-trips.
    """

    # Full history window — wide enough to cover all periods + their buffers.
    _CACHE_START = datetime(2014, 1, 1)
    _CACHE_END   = datetime(2026, 12, 31)   # far future; capped by actual DB data

    def __init__(self, repository: MarketDataRepository):
        self._repo  = repository
        self._store: dict[str, list] = {}   # symbol → sorted list[MarketOHLC]
        self._warm  = False

    # ------------------------------------------------------------------
    # Public API — drop-in replacement for MarketDataRepository
    # ------------------------------------------------------------------

    def warm_all(self, symbols: list[str],
                 start: datetime | None = None,
                 end:   datetime | None = None) -> None:
        """
        Load history for every symbol in one bulk DB query.

        start / end  — optional window override.  When omitted the class-level
                       _CACHE_START / _CACHE_END constants are used (full history).
                       Pass explicit dates for shorter diagnostic runs to avoid
                       pulling 12 years of data when only 8 months are needed.
        """
        cache_start = start or self._CACHE_START
        cache_end   = end   or self._CACHE_END

        # ── Fast path: local SQLite cache ─────────────────────────────────
        from app.data import local_cache
        if local_cache.cache_exists():
            print(f"\n  [Cache] Loading {len(symbols)} symbols from LOCAL SQLite "
                  f"({cache_start.date()} → {cache_end.date()})...")
            records = local_cache.load_records(symbols, cache_start, cache_end)
            missing = [s for s in symbols if s not in records]
            for symbol, recs in records.items():
                self._store[symbol] = sorted(recs, key=lambda r: r.timestamp)
            total = sum(len(v) for v in self._store.values())
            print(f"  [Cache] Local hit: {total:,} records for "
                  f"{len(self._store)} symbols (no Supabase calls).")
            if missing:
                print(f"  [Cache] {len(missing)} symbols absent from local cache "
                      f"— falling back to Supabase for those:")
                print(f"          {', '.join(missing[:8])}"
                      f"{'...' if len(missing) > 8 else ''}")
                for sym in missing:
                    recs = self._repo.get_ohlc_bulk([sym], cache_start, cache_end)
                    if sym in recs:
                        self._store[sym] = sorted(recs[sym], key=lambda r: r.timestamp)
            print()
            self._warm = True
            return

        # ── Slow path: full Supabase pull (no local cache yet) ────────────
        batch_size = 25
        batches = [symbols[i:i + batch_size] for i in range(0, len(symbols), batch_size)]
        print(f"\n  [Cache] No local cache — pulling {len(symbols)} symbols from "
              f"Supabase ({cache_start.date()} → {cache_end.date()}) "
              f"in {len(batches)} batches of ≤{batch_size}...")
        print(f"  [Cache] Tip: run `finance/bin/python3 scripts/cache_market_data_locally.py` "
              f"once to avoid this in future runs.")
        for idx, batch in enumerate(batches, 1):
            print(f"  [Cache] Batch {idx}/{len(batches)} ({len(batch)} symbols)...",
                  end=" ", flush=True)
            records = self._repo.get_ohlc_bulk(batch, cache_start, cache_end)
            for symbol, recs in records.items():
                self._store[symbol] = sorted(recs, key=lambda r: r.timestamp)
            print("done")
        total = sum(len(v) for v in self._store.values())
        print(f"  [Cache] Loaded {total:,} records for {len(self._store)} symbols "
              f"— all subsequent fetches served from memory.\n")
        self._warm = True

    def get_ohlc(self, symbol: str, start, end) -> list:
        self._ensure_symbol(symbol)
        return [r for r in self._store.get(symbol, [])
                if start <= r.timestamp <= end]

    def get_ohlc_bulk(self, symbols: list[str], start, end) -> dict:
        missing = [s for s in symbols if s not in self._store]
        if missing:
            self._load_symbols(missing)
        result = {}
        for symbol in symbols:
            sliced = [r for r in self._store.get(symbol, [])
                      if start <= r.timestamp <= end]
            if sliced:
                result[symbol] = sliced
        return result

    # Delegate all other repository methods (bulk_upsert, log_decision, etc.)
    def __getattr__(self, name):
        return getattr(self._repo, name)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _ensure_symbol(self, symbol: str) -> None:
        if symbol not in self._store:
            self._load_symbols([symbol])

    def _load_symbols(self, symbols: list[str]) -> None:
        """Fallback: load symbols not yet in cache (shouldn't happen after warm_all)."""
        records = self._repo.get_ohlc_bulk(symbols, self._CACHE_START, self._CACHE_END)
        for sym, recs in records.items():
            self._store[sym] = sorted(recs, key=lambda r: r.timestamp)
        # Symbols with no data at all: store empty list so we don't retry
        for sym in symbols:
            if sym not in self._store:
                self._store[sym] = []


# -----------------------------------------------------------------------
# Walk-forward validation helpers (Priority 5)
# -----------------------------------------------------------------------

# Regime sub-periods used to compute out-of-sample Sharpe for the LLM table.
# Only periods whose END date falls within the training window are used.
_WF_REGIME_PERIODS = {
    "Bull/LowVol":   (datetime(2019, 1, 1), datetime(2020, 2,  1)),
    "Crash/HighVol": (datetime(2020, 1, 1), datetime(2020, 12, 31)),
    "Recovery":      (datetime(2020, 4, 1), datetime(2021, 12, 31)),
    "Bear/Choppy":   (datetime(2022, 1, 1), datetime(2022, 12, 31)),
}

# Solo configs for the 5 strategies used in the adaptive run.
_WF_SOLO_CFGS = [
    {
        "name":            "DualMA",
        "factory":         lambda: DualMovingAverageStrategy(),
        "universe_filter": lambda: DualMAUniverseFilter(max_cross_age=5, top_n=30),
        "max_pos_pct":     0.15,
        "allowed_regimes": _UPTREND_ONLY,
    },
    {
        "name":            "Breakout",
        "factory":         lambda: BreakoutMomentumStrategy(),
        "universe_filter": lambda: BreakoutUniverseFilter(top_n=20),
        "max_pos_pct":     0.10,
        "allowed_regimes": _TREND_AND_SIDEWAYS,
    },
    {
        "name":            "QuietBrk",
        "factory":         lambda: QuietBreakoutStrategy(),
        "universe_filter": lambda: BreakoutUniverseFilter(
                               vol_threshold=1.2, return_threshold=0.008, top_n=20),
        "max_pos_pct":     0.10,
        "allowed_regimes": _UPTREND_ONLY,
    },
    {
        "name":            "TrendPB",
        "factory":         lambda: TrendPullbackStrategy(pullback_threshold=0.05),
        "universe_filter": lambda: PullbackUniverseFilter(top_n=20),
        "max_pos_pct":     0.10,
        "allowed_regimes": _TREND_AND_SIDEWAYS,
    },
    {
        "name":                    "RSI-MR",
        "factory":                 lambda: RSIMeanReversionStrategy(
                                       rsi_oversold=5, rsi_overbought=80, max_hold_days=7),
        "universe_filter":         lambda: MeanReversionUniverseFilter(top_n=20),
        "max_pos_pct":             0.10,
        "allowed_regimes":         _UPTREND_AND_SIDEWAYS,
        "breadth_circuit_breaker": True,
    },
]


def _compute_training_sharpes(repository) -> dict:
    """
    Run each of the 5 strategies in solo mode on each regime sub-period.
    Returns {regime_col: {strategy_name: sharpe}}.
    Called once; results are reused across all walk-forward folds.
    """
    print("\n  [WF] Pre-computing per-regime Sharpe on training sub-periods...")
    results: dict[str, dict[str, float]] = {}

    for regime_col, (start, end) in _WF_REGIME_PERIODS.items():
        print(f"  [WF]   {regime_col}  ({start.date()} → {end.date()})")
        ctx            = PeriodContext(repository, start, end)
        regime_sharpes = {}
        for cfg in _WF_SOLO_CFGS:
            result = run_experiment(
                repository, cfg["factory"](), ctx,
                max_position_pct        = cfg["max_pos_pct"],
                allowed_regimes         = cfg.get("allowed_regimes"),
                breadth_circuit_breaker = cfg.get("breadth_circuit_breaker", False),
                universe_filter         = cfg["universe_filter"](),
            )
            sharpe = (result["portfolio_metrics"].get("sharpe_ratio") or 0.0) if result else 0.0
            regime_sharpes[cfg["name"]] = round(sharpe, 2)
            print(f"  [WF]     {cfg['name']:<10} Sharpe={sharpe:.2f}")
        results[regime_col] = regime_sharpes

    return results


def _format_wf_table(sharpe_data: dict, available: list[str]) -> str:
    """
    Format a walk-forward performance table string for injection into the LLM prompt.
    Columns not in `available` are shown as N/A so the LLM knows no look-ahead was used.
    """
    col_order   = ["Bull/LowVol", "Crash/HighVol", "Recovery", "Bear/Choppy", "Mixed"]
    strat_order = ["DualMA", "Breakout", "QuietBrk", "TrendPB", "RSI-MR"]
    col_w = 14

    header = f"  {'Strategy':<20}" + "".join(f"{c:>{col_w}}" for c in col_order)
    lines  = [
        "Strategy Sharpe ratios by market regime (from training data only — no look-ahead):",
        header,
    ]
    for strat in strat_order:
        row = f"  {strat:<20}"
        for col in col_order:
            if col in available and col in sharpe_data and strat in sharpe_data[col]:
                row += f"{sharpe_data[col][strat]:>{col_w}.2f}"
            else:
                row += f"{'N/A':>{col_w}}"
        lines.append(row)
    lines.append("\nN/A = regime not yet observed in training window.")
    return "\n".join(lines)


def _make_adaptive_components(strategy_names):
    """Return a fresh (router, union_filter) pair for a walk-forward fold."""
    router = MultiStrategyRouter(
        strategies={
            "DualMA":   DualMovingAverageStrategy(),
            "Breakout": BreakoutMomentumStrategy(),
            "QuietBrk": QuietBreakoutStrategy(),
            "TrendPB":  TrendPullbackStrategy(pullback_threshold=0.05),
            "RSI-MR":   RSIMeanReversionStrategy(
                            rsi_oversold=5, rsi_overbought=80, max_hold_days=7),
        },
        weights={n: 0.20 for n in strategy_names},
        allowed_regimes={
            "DualMA":   _UPTREND_ONLY,
            "Breakout": _TREND_AND_SIDEWAYS,
            "QuietBrk": _UPTREND_ONLY,
            "TrendPB":  _TREND_AND_SIDEWAYS,
            "RSI-MR":   _UPTREND_AND_SIDEWAYS,
        },
        per_strategy_universe_source=lambda: union_filter.last_per_strategy_symbols,
        exclusive_strategies={"QuietBrk"},
    )
    union_filter = UnionUniverseFilter([
        ("Breakout", BreakoutUniverseFilter(top_n=20)),
        ("QuietBrk", ActivityTailFilter(top_n=20)),
        ("TrendPB",  PullbackUniverseFilter(top_n=20)),
        ("RSI-MR",   MeanReversionUniverseFilter(top_n=20)),
        ("DualMA",   DualMAUniverseFilter(max_cross_age=5, top_n=30)),
    ])
    return router, union_filter


def run_walk_forward(repository) -> None:
    """
    3-fold expanding-window walk-forward validation for AdaptiveStrategySelector.

    Each fold tests the adaptive selector on a held-out year using ONLY
    performance data from prior years in the LLM prompt (no look-ahead).

    Fold 1: Train 2019–2021  →  Test 2022 (Bear period)
    Fold 2: Train 2019–2022  →  Test 2023
    Fold 3: Train 2019–2023  →  Test Jan–Jun 2024

    Reports OOS Sharpe (out-of-sample table) vs IS Sharpe (hardcoded full table)
    for each fold. Expected OOS/IS ratio: 0.80–0.90× per the doc.
    """
    _STRATEGY_NAMES = ["DualMA", "Breakout", "QuietBrk", "TrendPB", "RSI-MR"]

    # (fold_label, test_start, test_end, regime_cols_available_for_training)
    FOLDS = [
        ("Fold 1 — 2022 (Bear)", datetime(2022, 1, 1), datetime(2022, 12, 31),
         ["Bull/LowVol", "Crash/HighVol", "Recovery"]),
        ("Fold 2 — 2023",        datetime(2023, 1, 1), datetime(2023, 12, 31),
         ["Bull/LowVol", "Crash/HighVol", "Recovery", "Bear/Choppy"]),
        ("Fold 3 — 2024",        datetime(2024, 1, 1), datetime(2024, 6,  1),
         ["Bull/LowVol", "Crash/HighVol", "Recovery", "Bear/Choppy"]),
    ]

    print(f"\n{'=' * (ROW_W + 2)}")
    print(f"  Walk-Forward Validation — 3 Folds")
    print(f"  OOS = out-of-sample table (training data only)")
    print(f"  IS  = in-sample table (hardcoded full-history — upper bound)")
    print(f"{'=' * (ROW_W + 2)}")

    # Compute training Sharpes once — reused across all folds
    training_sharpes = _compute_training_sharpes(repository)

    wf_summary = []

    for fold_label, test_start, test_end, available in FOLDS:
        print(f"\n  {'─' * ROW_W}")
        print(f"  {fold_label}  ({test_start.date()} → {test_end.date()})")
        print(f"  Training regimes: {', '.join(available)}")
        print(f"  {'─' * ROW_W}")
        print(HEADER)

        ctx      = PeriodContext(repository, test_start, test_end)
        wf_table = _format_wf_table(training_sharpes, available)

        # Out-of-sample: uses performance table computed from training data only
        oos_selector = AdaptiveStrategySelector(
            strategy_names=_STRATEGY_NAMES,
            rebalance_frequency_days=5,
            model="gpt-4o",
            verbose=False,
            regime_stability_weeks=2,
            performance_table=wf_table,
        )
        router_oos, filter_oos = _make_adaptive_components(_STRATEGY_NAMES)
        result_oos = run_experiment(
            repository, router_oos, ctx,
            max_position_pct=0.10, allowed_regimes=None,
            breadth_circuit_breaker=True, universe_filter=filter_oos,
            adaptive_selector=oos_selector,
            max_downtrend_pct=0.35, min_atr_cost_ratio=3.0,
        )
        _print_row("OOS-Adaptive", result_oos)

        # In-sample: uses hardcoded full-history table (look-ahead upper bound)
        is_selector = AdaptiveStrategySelector(
            strategy_names=_STRATEGY_NAMES,
            rebalance_frequency_days=5,
            model="gpt-4o",
            verbose=False,
            regime_stability_weeks=2,
        )
        router_is, filter_is = _make_adaptive_components(_STRATEGY_NAMES)
        result_is = run_experiment(
            repository, router_is, ctx,
            max_position_pct=0.10, allowed_regimes=None,
            breadth_circuit_breaker=True, universe_filter=filter_is,
            adaptive_selector=is_selector,
            max_downtrend_pct=0.35, min_atr_cost_ratio=3.0,
        )
        _print_row("IS-Adaptive ", result_is)

        oos_sharpe = (result_oos["portfolio_metrics"].get("sharpe_ratio") or 0.0) if result_oos else 0.0
        is_sharpe  = (result_is["portfolio_metrics"].get("sharpe_ratio")  or 0.0) if result_is  else 0.0
        wf_summary.append((fold_label, oos_sharpe, is_sharpe))

    # Final summary table
    print(f"\n  {'─' * ROW_W}")
    print(f"  {'Fold':<30} {'OOS Sharpe':>12} {'IS Sharpe':>10} {'OOS/IS':>8}")
    print(f"  {'─' * ROW_W}")
    for label, oos, is_ in wf_summary:
        ratio = f"{oos / is_:.2f}×" if is_ else "N/A"
        print(f"  {label:<30} {oos:>12.2f} {is_:>10.2f} {ratio:>8}")
    print(f"  Target OOS/IS: 0.80–0.90× (doc prediction)")
    print(f"{'=' * (ROW_W + 2)}\n")


# -----------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------
def _run_full_periods(repository):
    """Full historical backtest suite. Called from main() when RUN_FULL=True."""
    repository.warm_all(BROAD_UNIVERSE)   # full 2014–2026 window

    # Optional single-period filter for diagnostic / fast-iteration runs:
    #   PERIOD=Bull       → matches "Bull  2019–2020" (case-insensitive substring)
    #   PERIOD=Live       → matches "Live  2025–2026"
    #   unset / empty     → run all 7 periods (default)
    # The matched period's exact label is also exposed back to AdaptiveSelector
    # via the same env var so JSONL log entries are tagged with the period.
    _period_filter = (os.environ.get("PERIOD") or "").strip().lower()
    if _period_filter:
        _filtered = {k: v for k, v in PERIODS.items() if _period_filter in k.lower()}
        if not _filtered:
            print(f"\n[PERIOD filter] No period matches '{os.environ['PERIOD']}'. Available:")
            for k in PERIODS:
                print(f"  - {k.strip()}")
            return
        print(f"\n[PERIOD filter] Running {len(_filtered)} of {len(PERIODS)} periods: "
              f"{', '.join(k.strip() for k in _filtered)}")
        _periods_to_run = _filtered
    else:
        _periods_to_run = PERIODS

    for period_label, (start_date, end_date) in _periods_to_run.items():
        # Re-export the exact label so the AdaptiveSelector JSONL log can tag rows.
        os.environ["PERIOD"] = period_label.strip()

        # Build shared context once — single DB fetch for all 150 symbols
        ctx = PeriodContext(repository, start_date, end_date)

        print(f"\n{'=' * (ROW_W + 2)}")
        print(f"  Period: {period_label}   ({start_date.date()} → {end_date.date()})")
        print(f"  Universe: {len(BROAD_UNIVERSE)} symbols → DynamicUniverse top 80 → UniverseSelection top 20")
        print(f"  Costs: 0.10% commission + 0.05% slippage per side (all returns net of costs)")
        print(f"{'=' * (ROW_W + 2)}")
        print(HEADER)

        # Solo strategies — skipped when ADAPTIVE_ONLY=1.
        if not ADAPTIVE_ONLY:
            current_group = None
            for cfg in STRATEGIES:
                if cfg["group"] != current_group:
                    current_group = cfg["group"]
                    print(f"{DIVIDER}  [{current_group}]")

                strategy         = cfg["factory"]()
                universe_filter  = cfg["universe_filter"]() if cfg.get("universe_filter") else None
                result           = run_experiment(
                    repository, strategy, ctx,
                    max_position_pct=cfg["max_pos_pct"],
                    allowed_regimes=cfg.get("allowed_regimes"),
                    breadth_circuit_breaker=cfg.get("breadth_circuit_breaker", False),
                    universe_filter=universe_filter,
                )
                _print_row(cfg["label"], result)
        else:
            print(f"{DIVIDER}  [ADAPTIVE_ONLY=1 — skipping solo strategies and EqualWeight]")

        # Build the union filter and analytics state once per period — required
        # by Adaptive/RCA even when EqualWeight is skipped (compute_universe_diagnostics
        # and the trade annotator both read these).
        union_filter = UnionUniverseFilter([
            ("Breakout", BreakoutUniverseFilter(top_n=20)),
            ("QuietBrk", ActivityTailFilter(top_n=20)),
            ("TrendPB",  PullbackUniverseFilter(top_n=20)),
            ("RSI-MR",   MeanReversionUniverseFilter(top_n=20)),
            ("DualMA",   DualMAUniverseFilter(max_cross_age=5, top_n=30)),
        ])
        _annotator      = TradeAnnotator(repository, ctx.observer)
        _period_enriched: list = []

        # ------------------------------------------------------------------
        # Step 14 baseline: all 5 strategies at equal weight (0.20 each).
        # Skipped when ADAPTIVE_ONLY=1.
        # ------------------------------------------------------------------
        if not ADAPTIVE_ONLY:
            print(f"{DIVIDER}  [Multi-strategy baseline — equal weight]")

            multi_router = MultiStrategyRouter(
                strategies={
                    "DualMA":   DualMovingAverageStrategy(),
                    "Breakout": BreakoutMomentumStrategy(),
                    "QuietBrk": QuietBreakoutStrategy(),
                    "TrendPB":  TrendPullbackStrategy(pullback_threshold=0.05),
                    "RSI-MR":   RSIMeanReversionStrategy(
                                    rsi_oversold=5, rsi_overbought=80, max_hold_days=7),
                },
                weights={
                    "DualMA":   0.20,
                    "Breakout": 0.20,
                    "QuietBrk": 0.20,
                    "TrendPB":  0.20,
                    "RSI-MR":   0.20,
                },
                # Mirror each strategy's solo allowed_regimes — the router filters
                # symbol_states per-strategy before calling decide().
                allowed_regimes={
                    "DualMA":   _UPTREND_ONLY,
                    "Breakout": _TREND_AND_SIDEWAYS,
                    "QuietBrk": _UPTREND_ONLY,
                    "TrendPB":  _TREND_AND_SIDEWAYS,
                    "RSI-MR":   _UPTREND_AND_SIDEWAYS,
                },
                per_strategy_universe_source=lambda: union_filter.last_per_strategy_symbols,
                exclusive_strategies={"QuietBrk"},
            )

            _ew_attrib = TradeAttributionTracker(list(multi_router.strategies))
            result_multi = run_experiment(
                repository, multi_router, ctx,
                max_position_pct=0.10,        # per-position cap (further scaled by weight inside RiskAgent)
                allowed_regimes=None,         # router handles per-strategy regime gating internally
                breadth_circuit_breaker=True,
                universe_filter=union_filter, # each strategy sees its own domain candidates
                max_downtrend_pct=0.35,       # tighter than solo-strategy default (0.40)
                min_atr_cost_ratio=3.0,       # ATR must cover ≥ 3× round-trip cost (0.45% min ATR)
                pnl_tracker=_ew_attrib,
                no_atr_stop_strategies={"RSI-MR", "TrendPB"},
            )
            _print_row("EqualWeight (5-strat)", result_multi)
            _print_strategy_attribution(_ew_attrib, "EqualWeight")
            _print_router_diagnostics("EqualWeight", multi_router)
            _print_universe_overlap("EqualWeight", union_filter)
            if result_multi and result_multi.get("trades"):
                _print_exit_attribution(result_multi["trades"], "EqualWeight")
                _period_enriched.extend(_annotator.annotate(
                    result_multi["trades"],
                    attribution_tracker=_ew_attrib,
                    period_label=period_label.strip(),
                    run_label="EqualWeight",
                ))

        # ------------------------------------------------------------------
        # Step 15: Adaptive (LLM-driven) multi-strategy run
        #
        # Same 5 strategies + same UnionUniverseFilter as the equal-weight
        # baseline — the ONLY difference is that strategy weights are updated
        # weekly by AdaptiveStrategySelector (OpenAI GPT-4o call).
        #
        # Comparison:
        #   equal-weight  →  measures diversification benefit
        #   adaptive       →  measures LLM allocation benefit ON TOP of that
        # ------------------------------------------------------------------
        result_adaptive = None
        if not EQW_ONLY:
            print(f"{DIVIDER}  [Multi-strategy adaptive — LLM weights]")

            _STRATEGY_NAMES = ["DualMA", "Breakout", "QuietBrk", "TrendPB", "RSI-MR"]

            adaptive_router = MultiStrategyRouter(
                strategies={
                    "DualMA":   DualMovingAverageStrategy(),
                    "Breakout": BreakoutMomentumStrategy(),
                    "QuietBrk": QuietBreakoutStrategy(),
                    "TrendPB":  TrendPullbackStrategy(pullback_threshold=0.05),
                    "RSI-MR":   RSIMeanReversionStrategy(
                                    rsi_oversold=5, rsi_overbought=80, max_hold_days=7),
                },
                weights={n: 0.20 for n in _STRATEGY_NAMES},   # start equal; LLM adjusts weekly
                allowed_regimes={
                    "DualMA":   _UPTREND_ONLY,
                    "Breakout": _TREND_AND_SIDEWAYS,
                    "QuietBrk": _UPTREND_ONLY,
                    "TrendPB":  _TREND_AND_SIDEWAYS,
                    "RSI-MR":   _UPTREND_AND_SIDEWAYS,
                },
                per_strategy_universe_source=lambda: adaptive_union_filter.last_per_strategy_symbols,
                exclusive_strategies={"QuietBrk"},
            )

            selector = AdaptiveStrategySelector(
                strategy_names=_STRATEGY_NAMES,
                rebalance_frequency_days=5,
                model="gpt-4o",
                verbose=True,    # prints each weekly weight update
            )

            adaptive_union_filter = UnionUniverseFilter([
                ("Breakout", BreakoutUniverseFilter(top_n=20)),
                ("QuietBrk", ActivityTailFilter(top_n=20)),
                ("TrendPB",  PullbackUniverseFilter(top_n=20)),
                ("RSI-MR",   MeanReversionUniverseFilter(top_n=20)),
                ("DualMA",   DualMAUniverseFilter(max_cross_age=5, top_n=30)),
            ])

            _adaptive_attrib = TradeAttributionTracker(list(adaptive_router.strategies))
            result_adaptive = run_experiment(
                repository, adaptive_router, ctx,
                max_position_pct=0.10,
                allowed_regimes=None,
                breadth_circuit_breaker=True,
                universe_filter=adaptive_union_filter,
                adaptive_selector=selector,
                max_downtrend_pct=0.35,
                min_atr_cost_ratio=3.0,
                pnl_tracker=_adaptive_attrib,
                no_atr_stop_strategies={"RSI-MR", "TrendPB"},
            )
            _print_row("Adaptive  (5-strat)", result_adaptive)
            print(f"  {'':>{COL_W}} (LLM calls: {selector.call_count})")
            _print_strategy_attribution(_adaptive_attrib, "Adaptive")
            _print_router_diagnostics("Adaptive", adaptive_router)
            _print_universe_overlap("Adaptive", adaptive_union_filter)
            if result_adaptive and result_adaptive.get("trades"):
                _period_enriched.extend(_annotator.annotate(
                    result_adaptive["trades"],
                    attribution_tracker=_adaptive_attrib,
                    period_label=period_label.strip(),
                    run_label="Adaptive",
                ))

        # ------------------------------------------------------------------
        # Step 16: Adaptive + RegimeContextAgent. Skipped when ADAPTIVE_ONLY=1.
        # ------------------------------------------------------------------
        result_rca = None
        if not ADAPTIVE_ONLY and not EQW_ONLY:
            print(f"{DIVIDER}  [Multi-strategy adaptive + RegimeContextAgent]")

            rca_router = MultiStrategyRouter(
                strategies={
                    "DualMA":   DualMovingAverageStrategy(),
                    "Breakout": BreakoutMomentumStrategy(),
                    "QuietBrk": QuietBreakoutStrategy(),
                    "TrendPB":  TrendPullbackStrategy(pullback_threshold=0.05),
                    "RSI-MR":   RSIMeanReversionStrategy(
                                    rsi_oversold=5, rsi_overbought=80, max_hold_days=7),
                },
                weights={n: 0.20 for n in _STRATEGY_NAMES},
                allowed_regimes={
                    "DualMA":   _UPTREND_ONLY,
                    "Breakout": _TREND_AND_SIDEWAYS,
                    "QuietBrk": _UPTREND_ONLY,
                    "TrendPB":  _TREND_AND_SIDEWAYS,
                    "RSI-MR":   _UPTREND_AND_SIDEWAYS,
                },
                per_strategy_universe_source=lambda: rca_filter.last_per_strategy_symbols,
                exclusive_strategies={"QuietBrk"},
            )
            rca_selector = AdaptiveStrategySelector(
                strategy_names=_STRATEGY_NAMES,
                rebalance_frequency_days=5,
                model="gpt-4o",
                verbose=False,
            )
            rca_filter = UnionUniverseFilter([
                ("Breakout", BreakoutUniverseFilter(top_n=20)),
                ("QuietBrk", ActivityTailFilter(top_n=20)),
                ("TrendPB",  PullbackUniverseFilter(top_n=20)),
                ("RSI-MR",   MeanReversionUniverseFilter(top_n=20)),
                ("DualMA",   DualMAUniverseFilter(max_cross_age=5, top_n=30)),
            ])
            _rca_attrib = TradeAttributionTracker(list(rca_router.strategies))
            result_rca = run_experiment(
                repository, rca_router, ctx,
                max_position_pct=0.10,
                allowed_regimes=None,
                breadth_circuit_breaker=True,
                universe_filter=rca_filter,
                adaptive_selector=rca_selector,
                max_downtrend_pct=0.35,
                min_atr_cost_ratio=3.0,
                regime_context_agent=ctx.regime_context_agent,
                pnl_tracker=_rca_attrib,
                no_atr_stop_strategies={"RSI-MR", "TrendPB"},
            )
            _print_row("Adaptive+RCA (5-strat)", result_rca)
            print(f"  {'':>{COL_W}} (LLM calls: {rca_selector.call_count})")
            _print_strategy_attribution(_rca_attrib, "Adaptive+RCA")
            _print_router_diagnostics("Adaptive+RCA", rca_router)
            _print_universe_overlap("Adaptive+RCA", rca_filter)
            if result_rca and result_rca.get("trades"):
                _period_enriched.extend(_annotator.annotate(
                    result_rca["trades"],
                    attribution_tracker=_rca_attrib,
                    period_label=period_label.strip(),
                    run_label="Adaptive+RCA",
                ))

            # Delta row: show RCA improvement at a glance
            if result_adaptive and result_rca:
                base_sharpe = result_adaptive["portfolio_metrics"].get("sharpe_ratio") or 0.0
                rca_sharpe  = result_rca["portfolio_metrics"].get("sharpe_ratio")       or 0.0
                base_ret    = result_adaptive["portfolio_metrics"].get("total_return")  or 0.0
                rca_ret     = result_rca["portfolio_metrics"].get("total_return")       or 0.0
                delta_s = rca_sharpe - base_sharpe
                delta_r = (rca_ret - base_ret) * 100
                sign_s  = "+" if delta_s >= 0 else ""
                sign_r  = "+" if delta_r >= 0 else ""
                print(f"  {'RCA delta':<{COL_W}} {sign_s}{delta_s:>5.2f}  {sign_r}{delta_r:>7.2f}%")

        # ── Period-end analytics ─────────────────────────────────────────────
        # When ADAPTIVE_ONLY=1, the EqW union_filter was created but never run
        # (its last_per_strategy_symbols stays empty), so use adaptive_union_filter
        # for diagnostics instead — its filter state reflects what was actually traded.
        diag_filter = (adaptive_union_filter
                       if (ADAPTIVE_ONLY and not EQW_ONLY)
                       else union_filter)
        _u_tracker = compute_universe_diagnostics(ctx, diag_filter)
        _oqm = compute_opportunity_quality_metrics(_period_enriched, _u_tracker.daily_records)
        print_opportunity_quality_summary(_oqm, period_label.strip())
        if _period_enriched:
            export_enriched_trades_csv(_period_enriched, "trade_analytics.csv")

    print(f"\n{'=' * (ROW_W + 2)}\n")

    if RUN_WALK_FORWARD:
        run_walk_forward(repository)

    if RUN_WALK_FORWARD:
        run_walk_forward(repository)


def main():
    _base = MarketDataRepository()
    repository = OHLCCache(_base)

    # Full historical periods — all PERIODS including "Live 2025-2026".
    # Each period shows: solo strategies + EqualWeight + Adaptive + Adaptive+RCA
    # Switch to _run_recent_diagnostic(repository) for a quick 30-day smoke-test.
    _run_full_periods(repository)


def _run_recent_diagnostic(repository) -> None:
    from datetime import datetime as _dt, timedelta as _td

    DIAG_START = _dt(2026, 2, 1)   # ~50 days back so indicators are warm by Feb 24
    DIAG_END   = _dt(2026, 3, 24)
    _STRAT_NAMES = ["DualMA", "Breakout", "QuietBrk", "TrendPB", "RSI-MR"]

    # Warm only the data window this diagnostic needs.
    # MarketObserverAgent.preload() adds a 300-day buffer internally, so we
    # cover that by going 350 days before DIAG_START — ~8 months total vs 12 years.
    repository.warm_all(
        list({s for s in BROAD_UNIVERSE}),
        start = DIAG_START - _td(days=350),
        end   = DIAG_END,
    )

    print(f"\n{'=' * (ROW_W + 2)}")
    print(f"  Diagnostic: Recent 30-day run — relaxed guardrails (2026-02-24 → 2026-03-24)")
    print(f"  Purpose: see what signals would have fired under looser risk settings")
    print(f"  NOT deployed — Railway config unchanged")
    print(f"{'=' * (ROW_W + 2)}")
    print(HEADER)

    ctx = PeriodContext(repository, DIAG_START, DIAG_END)
    rca = RegimeContextAgent(ctx.dynamic_universe_agent)

    _CONFIGS = [
        {
            "label":               "[A] Production  (CB=35%, regimes=UP/SIDE)",
            "max_downtrend_pct":   0.35,
            "breadth_cb":          True,
            "allowed_regimes":     {
                "DualMA":   _UPTREND_ONLY,
                "Breakout": _TREND_AND_SIDEWAYS,
                "QuietBrk": _UPTREND_ONLY,
                "TrendPB":  _TREND_AND_SIDEWAYS,
                "RSI-MR":   _UPTREND_AND_SIDEWAYS,
            },
        },
        {
            "label":               "[B] Relaxed CB  (CB=70%, regimes=UP/SIDE)",
            "max_downtrend_pct":   0.70,
            "breadth_cb":          True,
            "allowed_regimes":     {
                "DualMA":   _UPTREND_ONLY,
                "Breakout": _TREND_AND_SIDEWAYS,
                "QuietBrk": _UPTREND_ONLY,
                "TrendPB":  _TREND_AND_SIDEWAYS,
                "RSI-MR":   _UPTREND_AND_SIDEWAYS,
            },
        },
        {
            "label":               "[C] No gates    (CB=off, all regimes open)",
            "max_downtrend_pct":   1.00,
            "breadth_cb":          False,
            "allowed_regimes":     {k: None for k in _STRAT_NAMES},
        },
        {
            "label":               "[A+RCA] Production  (CB=35%, +RegimeContext)",
            "max_downtrend_pct":   0.35,
            "breadth_cb":          True,
            "allowed_regimes":     {
                "DualMA":   _UPTREND_ONLY,
                "Breakout": _TREND_AND_SIDEWAYS,
                "QuietBrk": _UPTREND_ONLY,
                "TrendPB":  _TREND_AND_SIDEWAYS,
                "RSI-MR":   _UPTREND_AND_SIDEWAYS,
            },
            "rca": rca,   # ← pass the RCA instance
        },
    ]

    for cfg in _CONFIGS:
        print(f"{DIVIDER}")
        router = MultiStrategyRouter(
            strategies={
                "DualMA":   DualMovingAverageStrategy(),
                "Breakout": BreakoutMomentumStrategy(),
                "QuietBrk": QuietBreakoutStrategy(),
                "TrendPB":  TrendPullbackStrategy(pullback_threshold=0.05),
                "RSI-MR":   RSIMeanReversionStrategy(
                                rsi_oversold=5, rsi_overbought=80, max_hold_days=7),
            },
            weights={n: 0.20 for n in _STRAT_NAMES},
            allowed_regimes=cfg["allowed_regimes"],
            per_strategy_universe_source=lambda: union_filter.last_per_strategy_symbols,
            exclusive_strategies={"QuietBrk"},
        )
        union_filter = UnionUniverseFilter([
            ("Breakout", BreakoutUniverseFilter(top_n=20)),
            ("QuietBrk", ActivityTailFilter(top_n=20)),
            ("TrendPB",  PullbackUniverseFilter(top_n=20)),
            ("RSI-MR",   MeanReversionUniverseFilter(top_n=20)),
            ("DualMA",   DualMAUniverseFilter(max_cross_age=5, top_n=30)),
        ])
        selector = AdaptiveStrategySelector(
            strategy_names=_STRAT_NAMES,
            rebalance_frequency_days=5,
            model="gpt-4o",
            verbose=False,
            regime_stability_weeks=2,
        )
        result = run_experiment(
            repository, router, ctx,
            max_position_pct=0.10,
            allowed_regimes=None,          # router handles per-strategy gating
            breadth_circuit_breaker=cfg["breadth_cb"],
            universe_filter=union_filter,
            adaptive_selector=selector,
            max_downtrend_pct=cfg["max_downtrend_pct"],
            min_atr_cost_ratio=3.0,
            regime_context_agent=cfg.get("rca"),
        )
        _print_row(cfg["label"], result)

    print(f"\n{'=' * (ROW_W + 2)}")
    print(f"  Decision guide:")
    print(f"    [A] = 0 trades → confirmed production behaviour")
    print(f"    [B] trades > 0 → relaxing CB alone is enough to unlock signals")
    print(f"    [C] trades > 0 → regime filter is the primary blocker")
    print(f"    Raise CB threshold in Railway ONLY if [B] drawdown < [A] full-period drawdown")
    print(f"{'=' * (ROW_W + 2)}\n")

    # ------------------------------------------------------------------
    # Historical recovery test — 2020 recovery period
    # RCA should catch TRANSITION_UP earlier than base regime detection,
    # allowing re-entry weeks before the SMA_50-based rules confirm the move.
    # ------------------------------------------------------------------
    print(f"\n{'─' * (ROW_W + 2)}")
    print(f"  Historical Recovery Test — 2020 recovery (2020-04-01 → 2021-12-31)")
    print(f"  Key question: does RCA catch TRANSITION_UP earlier → better returns?")
    print(f"{'─' * (ROW_W + 2)}")
    print(HEADER)

    from datetime import datetime as _dt2
    RECOV_START = _dt2(2020, 4, 1)
    RECOV_END   = _dt2(2021, 12, 31)

    repository.warm_all(
        list({s for s in BROAD_UNIVERSE}),
        start = RECOV_START - _td(days=350),
        end   = RECOV_END,
    )

    ctx_recov = PeriodContext(repository, RECOV_START, RECOV_END)
    rca_recov = RegimeContextAgent(ctx_recov.dynamic_universe_agent)

    _STRAT_NAMES_R = ["DualMA", "Breakout", "QuietBrk", "TrendPB", "RSI-MR"]

    for label_r, use_rca in [
        ("Adaptive  (no RCA)", False),
        ("Adaptive  (+RCA)  ", True),
    ]:
        router_r = MultiStrategyRouter(
            strategies={
                "DualMA":   DualMovingAverageStrategy(),
                "Breakout": BreakoutMomentumStrategy(),
                "QuietBrk": QuietBreakoutStrategy(),
                "TrendPB":  TrendPullbackStrategy(pullback_threshold=0.05),
                "RSI-MR":   RSIMeanReversionStrategy(
                                rsi_oversold=5, rsi_overbought=80, max_hold_days=7),
            },
            weights={n: 0.20 for n in _STRAT_NAMES_R},
            allowed_regimes={
                "DualMA":   _UPTREND_ONLY,
                "Breakout": _TREND_AND_SIDEWAYS,
                "QuietBrk": _UPTREND_ONLY,
                "TrendPB":  _TREND_AND_SIDEWAYS,
                "RSI-MR":   _UPTREND_AND_SIDEWAYS,
            },
            per_strategy_universe_source=lambda: uf_r.last_per_strategy_symbols,
            exclusive_strategies={"QuietBrk"},
        )
        uf_r = UnionUniverseFilter([
            ("Breakout", BreakoutUniverseFilter(top_n=20)),
            ("QuietBrk", ActivityTailFilter(top_n=20)),
            ("TrendPB",  PullbackUniverseFilter(top_n=20)),
            ("RSI-MR",   MeanReversionUniverseFilter(top_n=20)),
            ("DualMA",   DualMAUniverseFilter(max_cross_age=5, top_n=30)),
        ])
        sel_r = AdaptiveStrategySelector(
            strategy_names=_STRAT_NAMES_R,
            rebalance_frequency_days=5,
            model="gpt-4o",
            verbose=False,
            regime_stability_weeks=2,
        )
        result_r = run_experiment(
            repository, router_r, ctx_recov,
            max_position_pct=0.10,
            allowed_regimes=None,
            breadth_circuit_breaker=True,
            universe_filter=uf_r,
            adaptive_selector=sel_r,
            max_downtrend_pct=0.35,
            min_atr_cost_ratio=3.0,
            regime_context_agent=rca_recov if use_rca else None,
        )
        _print_row(label_r, result_r)


if __name__ == "__main__":
    main()
