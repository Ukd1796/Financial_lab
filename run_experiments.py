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
from app.strategy.rsi_mean_reversion import RSIMeanReversionStrategy
from app.strategy.trend_pullback import TrendPullbackStrategy
from app.universe.agent import UniverseSelectionAgent
from app.universe.dynamic_agent import DynamicUniverseAgent

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
    # # ---- Medium-term trend strategies (uptrend regime only) ----------
    # {
    #     "label":           "CS  L=100 R=20 T=5%",
    #     "factory":         lambda: CrossSectionalMomentumStrategy(
    #                            lookback_days=100, top_n=3,
    #                            rebalance_frequency=20, momentum_threshold=0.05),
    #     "max_pos_pct":     0.20,
    #     "allowed_regimes": _UPTREND_ONLY,
    #     "group":           "Medium-term",
    # },
    # {
    #     "label":           "CS  L=80  R=20 T=5%",
    #     "factory":         lambda: CrossSectionalMomentumStrategy(
    #                            lookback_days=80, top_n=3,
    #                            rebalance_frequency=20, momentum_threshold=0.05),
    #     "max_pos_pct":     0.20,
    #     "allowed_regimes": _UPTREND_ONLY,
    #     "group":           "Medium-term",
    # },
    # {
    #     "label":           "CS  L=100 R=20 T=3%",
    #     "factory":         lambda: CrossSectionalMomentumStrategy(
    #                            lookback_days=100, top_n=3,
    #                            rebalance_frequency=20, momentum_threshold=0.03),
    #     "max_pos_pct":     0.20,
    #     "allowed_regimes": _UPTREND_ONLY,
    #     "group":           "Medium-term",
    # },
    # {
    #     "label":           "DualMA SMA20/50",
    #     "factory":         lambda: DualMovingAverageStrategy(),
    #     "max_pos_pct":     0.15,
    #     "allowed_regimes": _UPTREND_ONLY,
    #     "group":           "Medium-term",
    # },

    # ---- Short-term momentum strategies (uptrend + sideways) ---------
    {
        "label":           "Breakout 10d",
        "factory":         lambda: BreakoutMomentumStrategy(),
        "max_pos_pct":     0.10,
        "allowed_regimes": _TREND_AND_SIDEWAYS,
        "group":           "Short-term",
    },
    {
        "label":           "TrendPB v2 pct=3%",
        "factory":         lambda: TrendPullbackStrategy(pullback_threshold=0.03),
        "max_pos_pct":     0.10,
        "allowed_regimes": _TREND_AND_SIDEWAYS,
        "group":           "Short-term",
    },
    {
        "label":           "TrendPB v2 pct=5%",
        "factory":         lambda: TrendPullbackStrategy(pullback_threshold=0.05),
        "max_pos_pct":     0.10,
        "allowed_regimes": _TREND_AND_SIDEWAYS,
        "group":           "Short-term",
    },

    # ---- Mean-reversion strategies (uptrend/sideways only + breadth circuit breaker) --
    # Regime filter: only enter when the *individual stock* is in UPTREND or SIDEWAYS.
    # "Oversold in a downtrend" is a falling knife; "oversold in an uptrend" is a bounce.
    {
        "label":                   "RSI-MR  os=10 ob=70",
        "factory":                 lambda: RSIMeanReversionStrategy(
                                       rsi_oversold=10, rsi_overbought=70, max_hold_days=5),
        "max_pos_pct":             0.10,
        "allowed_regimes":         _UPTREND_AND_SIDEWAYS,
        "breadth_circuit_breaker": True,   # suppress buys when >60% of universe in DOWNTREND
        "group":                   "Mean-reversion",
    },
    {
        "label":                   "RSI-MR  os=5  ob=80",
        "factory":                 lambda: RSIMeanReversionStrategy(
                                       rsi_oversold=5,  rsi_overbought=80, max_hold_days=7),
        "max_pos_pct":             0.10,
        "allowed_regimes":         _UPTREND_AND_SIDEWAYS,
        "breadth_circuit_breaker": True,   # suppress buys when >60% of universe in DOWNTREND
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
def run_experiment(repository, strategy, ctx: PeriodContext, max_position_pct=0.20, allowed_regimes=None, breadth_circuit_breaker=False):

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
        max_downtrend_pct=0.60,        # block BUY when >60% of universe in DOWNTREND
    )

    engine = BacktestEngine(
        observer=ctx.observer,
        strategy_router=strategy,
        risk_agent=risk_agent,
        execution_agent=execution_agent,
        portfolio=portfolio,
        repository=repository,
        dynamic_universe_agent=ctx.dynamic_universe_agent,
        universe_agent=ctx.universe_agent,
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

            strategy = cfg["factory"]()
            result   = run_experiment(
                repository, strategy, ctx,
                max_position_pct=cfg["max_pos_pct"],
                allowed_regimes=cfg.get("allowed_regimes"),
                breadth_circuit_breaker=cfg.get("breadth_circuit_breaker", False),
            )
            _print_row(cfg["label"], result)

    print(f"\n{'=' * (ROW_W + 2)}\n")


if __name__ == "__main__":
    main()
