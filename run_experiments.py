from datetime import datetime

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
from app.universe.agent import UniverseSelectionAgent
from app.universe.dynamic_agent import DynamicUniverseAgent
from app.meta.adaptive_selector import AdaptiveStrategySelector
from app.universe.filters import (
    BreakoutUniverseFilter,
    DualMAUniverseFilter,
    MeanReversionUniverseFilter,
    PullbackUniverseFilter,
    UnionUniverseFilter,
)

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
    "Full  2018–2024": (datetime(2018, 1, 1),  datetime(2024, 6, 1)),
    "Bull  2019–2020": (datetime(2019, 1, 1),  datetime(2020, 2, 1)),
    "Crash 2020     ": (datetime(2020, 1, 1),  datetime(2020, 12, 31)),
    "Recov 2020–2021": (datetime(2020, 4, 1),  datetime(2021, 12, 31)),
    "Bear  2022     ": (datetime(2022, 1, 1),  datetime(2022, 12, 31)),
    "Recent2022–2024": (datetime(2022, 1, 1),  datetime(2024, 6, 1)),
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
      - universe_agent          : stateless filter, shared freely
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

        # Stage 2 — stateless, nothing to preload
        self.universe_agent = UniverseSelectionAgent(
            volume_threshold=1.5,
            volatility_threshold=0.02,
            top_n=20,
        )

        # Observer cache grows lazily; safe to share across strategies because
        # it stores only read-only MarketState (no portfolio state).
        self.observer = MarketObserverAgent(repository)

        # Price feed for CrossSectionalMomentumStrategy — extracted from the
        # dynamic agent's cache (already buffered 200 days before start_date)
        # so CS can compute N-day lookback from day 1 of the period.
        self.price_feed = self.dynamic_universe_agent.get_price_feed()

        # Timeline computed once from the DB for the period
        self.historical_dates = self._build_timeline(repository)

    def _build_timeline(self, repository):
        records = []
        for symbol in BROAD_UNIVERSE:
            records.extend(repository.get_ohlc(symbol, self.start_date, self.end_date))
        return sorted({r.timestamp for r in records})


# -----------------------------------------------------------------------
# Single backtest run  (receives shared period context)
# -----------------------------------------------------------------------
def run_experiment(repository, strategy, ctx: PeriodContext, max_position_pct=0.20, allowed_regimes=None, breadth_circuit_breaker=False, universe_filter=None, adaptive_selector=None):

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
        max_downtrend_pct=0.40,        # block BUY when >40% of universe in DOWNTREND (R1)
    )

    # Use the per-strategy universe filter when provided; fall back to the
    # shared UniverseSelectionAgent (the original activity-based filter).
    active_universe_agent = universe_filter if universe_filter is not None else ctx.universe_agent

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
    )

    results, trades = engine.run(BROAD_UNIVERSE, ctx.historical_dates)

    evaluator         = EvaluationAgent()
    portfolio_metrics = evaluator.evaluate(results, INITIAL_CAPITAL)
    trade_metrics     = evaluator.evaluate_trades(trades)

    return {"portfolio_metrics": portfolio_metrics, "trade_metrics": trade_metrics}


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


# -----------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------
def main():
    repository = MarketDataRepository()

    for period_label, (start_date, end_date) in PERIODS.items():

        # Build shared context once — single DB fetch for all 150 symbols
        ctx = PeriodContext(repository, start_date, end_date)

        print(f"\n{'=' * (ROW_W + 2)}")
        print(f"  Period: {period_label}   ({start_date.date()} → {end_date.date()})")
        print(f"  Universe: {len(BROAD_UNIVERSE)} symbols → DynamicUniverse top 80 → UniverseSelection top 20")
        print(f"  Costs: 0.10% commission + 0.05% slippage per side (all returns net of costs)")
        print(f"{'=' * (ROW_W + 2)}")
        print(HEADER)

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

        # ------------------------------------------------------------------
        # Step 14 baseline: all 5 strategies at equal weight (0.20 each)
        # on a shared portfolio.
        #
        # Three correctness requirements addressed here:
        #   1. decision.weight (0.20) is now applied in RiskAgent._size_position()
        #      so each strategy deploys 20% of the normal risk budget per trade.
        #   2. Per-strategy allowed_regimes are enforced inside MultiStrategyRouter
        #      before each strategy's decide() is called — same gates as solo runs.
        #   3. Universe uses the activity-based top-20 filter (same as solo runs)
        #      so each strategy sees the same candidate pool it was calibrated on.
        #
        # This is the comparison floor for AdaptiveStrategySelector (step 15).
        # ------------------------------------------------------------------
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
        )

        # Build the union filter once per period — runs each strategy's own filter
        # on the top-80 DynamicAgent candidates and takes the de-duplicated union.
        # This gives each strategy a domain-appropriate candidate pool without
        # competing for the same 20 activity-filtered slots.
        union_filter = UnionUniverseFilter([
            BreakoutUniverseFilter(top_n=20),
            BreakoutUniverseFilter(vol_threshold=1.2, return_threshold=0.008, top_n=20),  # QuietBrk
            PullbackUniverseFilter(top_n=20),
            MeanReversionUniverseFilter(top_n=20),
            DualMAUniverseFilter(max_cross_age=5, top_n=30),
        ])

        result_multi = run_experiment(
            repository, multi_router, ctx,
            max_position_pct=0.10,        # per-position cap (further scaled by weight inside RiskAgent)
            allowed_regimes=None,         # router handles per-strategy regime gating internally
            breadth_circuit_breaker=True,
            universe_filter=union_filter, # each strategy sees its own domain candidates
        )
        _print_row("EqualWeight (5-strat)", result_multi)

        # ------------------------------------------------------------------
        # Step 15: Adaptive (LLM-driven) multi-strategy run
        #
        # Same 5 strategies + same UnionUniverseFilter as the equal-weight
        # baseline — the ONLY difference is that strategy weights are updated
        # weekly by AdaptiveStrategySelector (OpenAI GPT-4o-mini call).
        #
        # Comparison:
        #   equal-weight  →  measures diversification benefit
        #   adaptive       →  measures LLM allocation benefit ON TOP of that
        # ------------------------------------------------------------------
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
        )

        selector = AdaptiveStrategySelector(
            strategy_names=_STRATEGY_NAMES,
            rebalance_frequency_days=5,
            model="gpt-4o-mini",
            verbose=True,    # prints each weekly weight update
        )

        adaptive_union_filter = UnionUniverseFilter([
            BreakoutUniverseFilter(top_n=20),
            BreakoutUniverseFilter(vol_threshold=1.2, return_threshold=0.008, top_n=20),
            PullbackUniverseFilter(top_n=20),
            MeanReversionUniverseFilter(top_n=20),
            DualMAUniverseFilter(max_cross_age=5, top_n=30),
        ])

        result_adaptive = run_experiment(
            repository, adaptive_router, ctx,
            max_position_pct=0.10,
            allowed_regimes=None,
            breadth_circuit_breaker=True,
            universe_filter=adaptive_union_filter,
            adaptive_selector=selector,
        )
        _print_row("Adaptive  (5-strat)", result_adaptive)
        print(f"  {'':>{COL_W}} (LLM calls: {selector.call_count})")

    print(f"\n{'=' * (ROW_W + 2)}\n")


if __name__ == "__main__":
    main()
