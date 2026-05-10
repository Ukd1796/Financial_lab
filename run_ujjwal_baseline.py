"""
Baseline backtest for Ujjwal's live portfolio configuration.

Profile (from pt_ujjwal / user_strategies id=f786f5cc):
  Universe:          broad150 (150 symbols: Nifty50 + NiftyNext50 + NiftyMidcap50)
  Strategies:        all 5 enabled at equal weight (0.20 each)
  max_position_pct:  10%
  risk_per_trade_pct: 0.5%
  pause_threshold_pct: 35%  → max_downtrend_pct=0.35 in RiskAgent
  capital:           ₹1,00,000

Runs three configs per period:
  A. EqualWeight (5-strat) — deterministic, no LLM calls
  B. Adaptive    (5-strat) — LLM weight updates every 5 days
  C. Adaptive+RCA           — Adaptive + RegimeContextAgent breadth signals

Output: docs/baseline_backtest_results.md
"""

import sys
import io
from datetime import datetime

from app.backtest.engine import BacktestEngine
from app.backtest.observer import MarketObserverAgent
from app.data.repository import MarketDataRepository
from app.evaluation.agent import EvaluationAgent
from app.execution.agent import ExecutionAgent
from app.portfolio.engine import PortfolioEngine
from app.portfolio.models import Portfolio
from app.risk.agent import RiskAgent, _DEFAULT_REGIME_MULTIPLIERS
from app.strategy.breakout_momentum import BreakoutMomentumStrategy
from app.strategy.dual_ma import DualMovingAverageStrategy
from app.strategy.multi_router import MultiStrategyRouter
from app.strategy.quiet_breakout import QuietBreakoutStrategy
from app.strategy.rsi_mean_reversion import RSIMeanReversionStrategy
from app.strategy.trend_pullback import TrendPullbackStrategy
from app.universe.agent import UniverseSelectionAgent
from app.universe.dynamic_agent import DynamicUniverseAgent
from app.meta.adaptive_selector import AdaptiveStrategySelector
from app.meta.regime_context_agent import RegimeContextAgent
from app.universe.filters import (
    BreakoutUniverseFilter,
    DualMAUniverseFilter,
    MeanReversionUniverseFilter,
    PullbackUniverseFilter,
    UnionUniverseFilter,
)

# ─── Universe (mirrors Ujjwal's broad150) ──────────────────────────────────

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

# ─── Ujjwal's risk params ──────────────────────────────────────────────────

INITIAL_CAPITAL     = 100_000   # ₹1,00,000
MAX_POSITION_PCT    = 0.10      # 10% per position
RISK_PER_TRADE_PCT  = 0.005     # 0.5% of portfolio per trade
MAX_DOWNTREND_PCT   = 0.35      # 35% pause threshold → breadth CB
MIN_ATR_COST_RATIO  = 3.0       # ATR ≥ 3× round-trip cost

# ─── Regime sets ──────────────────────────────────────────────────────────

_UPTREND_ONLY = [
    "LOW_VOL_UPTREND", "MID_VOL_UPTREND", "HIGH_VOL_UPTREND",
]
_TREND_AND_SIDEWAYS = [
    "LOW_VOL_UPTREND",   "MID_VOL_UPTREND",   "HIGH_VOL_UPTREND",
    "LOW_VOL_SIDEWAYS",  "MID_VOL_SIDEWAYS",  "HIGH_VOL_SIDEWAYS",
]
_UPTREND_AND_SIDEWAYS = _TREND_AND_SIDEWAYS

_ALLOWED_REGIMES = {
    "DualMA":   _UPTREND_ONLY,
    "Breakout": _TREND_AND_SIDEWAYS,
    "QuietBrk": _UPTREND_ONLY,
    "TrendPB":  _TREND_AND_SIDEWAYS,
    "RSI-MR":   _UPTREND_AND_SIDEWAYS,
}

# ─── Periods ──────────────────────────────────────────────────────────────

PERIODS = {
    "Full  2018–2024": (datetime(2018, 1, 1),  datetime(2024, 6, 1)),
    "Bull  2019–2020": (datetime(2019, 1, 1),  datetime(2020, 2, 1)),
    "Crash 2020     ": (datetime(2020, 1, 1),  datetime(2020, 12, 31)),
    "Recov 2020–2021": (datetime(2020, 4, 1),  datetime(2021, 12, 31)),
    "Bear  2022     ": (datetime(2022, 1, 1),  datetime(2022, 12, 31)),
    "Recent2022–2024": (datetime(2022, 1, 1),  datetime(2024, 6, 1)),
    "Live  2025–2026": (datetime(2025, 1, 1),  datetime(2026, 3, 24)),
}

# ─── Helpers ──────────────────────────────────────────────────────────────

COL_W  = 24
ROW_W  = COL_W + 46
HEADER = f"  {'Config':<{COL_W}} {'Sharpe':>6} {'Return':>9} {'MaxDD':>8} {'PF':>7} {'WR':>6} {'#Trades':>8}"
DIVIDER = f"  {'-' * ROW_W}"


def _make_union_filter():
    return UnionUniverseFilter([
        BreakoutUniverseFilter(top_n=20),
        BreakoutUniverseFilter(vol_threshold=1.2, return_threshold=0.008, top_n=20),
        PullbackUniverseFilter(top_n=20),
        MeanReversionUniverseFilter(top_n=20),
        DualMAUniverseFilter(max_cross_age=5, top_n=30),
    ])


def _make_router():
    return MultiStrategyRouter(
        strategies={
            "DualMA":   DualMovingAverageStrategy(),
            "Breakout": BreakoutMomentumStrategy(),
            "QuietBrk": QuietBreakoutStrategy(),
            "TrendPB":  TrendPullbackStrategy(pullback_threshold=0.05),
            "RSI-MR":   RSIMeanReversionStrategy(
                            rsi_oversold=5, rsi_overbought=80, max_hold_days=7),
        },
        weights={"DualMA": 0.20, "Breakout": 0.20, "QuietBrk": 0.20,
                 "TrendPB": 0.20, "RSI-MR": 0.20},
        allowed_regimes=_ALLOWED_REGIMES,
    )


def _run_one(repository, router, ctx, atr_multiplier=2.0,
             regime_multipliers=None,
             adaptive_selector=None, regime_context_agent=None):
    if not ctx.historical_dates:
        return None

    portfolio        = Portfolio(cash=INITIAL_CAPITAL)
    portfolio_engine = PortfolioEngine(portfolio)
    execution_agent  = ExecutionAgent(
        portfolio_engine, commission_pct=0.001, slippage_pct=0.0005)
    risk_agent       = RiskAgent(
        max_position_pct=MAX_POSITION_PCT,
        atr_multiplier=atr_multiplier,
        allowed_regimes=None,
        risk_per_trade_pct=RISK_PER_TRADE_PCT,
        use_vol_sizing=True,
        breadth_circuit_breaker=True,
        max_downtrend_pct=MAX_DOWNTREND_PCT,
        min_atr_cost_ratio=MIN_ATR_COST_RATIO,
        regime_multipliers=regime_multipliers,
    )
    engine = BacktestEngine(
        observer=ctx.observer,
        strategy_router=router,
        risk_agent=risk_agent,
        execution_agent=execution_agent,
        portfolio=portfolio,
        repository=None,
        dynamic_universe_agent=ctx.dynamic_universe_agent,
        universe_agent=ctx.universe_filter,
        adaptive_selector=adaptive_selector,
        regime_context_agent=regime_context_agent,
    )
    results, trades = engine.run(BROAD_UNIVERSE, ctx.historical_dates)

    evaluator         = EvaluationAgent()
    portfolio_metrics = evaluator.evaluate(results, INITIAL_CAPITAL)
    trade_metrics     = evaluator.evaluate_trades(trades)
    return {"portfolio_metrics": portfolio_metrics, "trade_metrics": trade_metrics}


def _fmt_row(label, result):
    if result is None:
        return f"  {label:<{COL_W}}  (no data)"
    pm = result["portfolio_metrics"]
    tm = result["trade_metrics"]
    sharpe = pm.get("sharpe_ratio", 0.0) or 0.0
    ret    = pm.get("total_return",  0.0) or 0.0
    dd     = pm.get("max_drawdown",  0.0) or 0.0
    pf     = tm.get("profit_factor",  0.0) or 0.0
    wr     = tm.get("win_rate_trade", 0.0) or 0.0
    n      = tm.get("num_trades",     0)
    return (
        f"  {label:<{COL_W}} "
        f"{sharpe:>6.2f} "
        f"{ret * 100:>8.2f}% "
        f"{dd * 100:>7.2f}% "
        f"{pf:>7.2f} "
        f"{wr * 100:>5.1f}% "
        f"{n:>8}"
    )


# ─── Period context ────────────────────────────────────────────────────────

class PeriodContext:
    def __init__(self, repository, start_date, end_date):
        self.start_date = start_date
        self.end_date   = end_date
        self.dynamic_universe_agent = DynamicUniverseAgent(
            repository=repository, symbols=BROAD_UNIVERSE, top_n=80)
        self.dynamic_universe_agent.preload(start_date, end_date)
        self.universe_filter = _make_union_filter()
        self.observer        = MarketObserverAgent(repository)
        self.price_feed      = self.dynamic_universe_agent.get_price_feed()
        self.regime_context_agent = RegimeContextAgent(self.dynamic_universe_agent)
        self.historical_dates = self._build_timeline()

    def _build_timeline(self):
        timestamps = set()
        for df in self.dynamic_universe_agent._cache.values():
            for ts in df.index:
                if self.start_date <= ts <= self.end_date:
                    timestamps.add(ts)
        return sorted(timestamps)


# ─── OHLCCache (same as run_experiments.py) ────────────────────────────────

class OHLCCache:
    _CACHE_START = datetime(2014, 1, 1)
    _CACHE_END   = datetime(2026, 12, 31)

    def __init__(self, repository):
        self._repo  = repository
        self._store = {}
        self._warm  = False

    def warm_all(self, symbols, start=None, end=None):
        cache_start = start or self._CACHE_START
        cache_end   = end   or self._CACHE_END
        print(f"\n  [Cache] Warming {len(symbols)} symbols from DB "
              f"({cache_start.date()} → {cache_end.date()})...")
        records = self._repo.get_ohlc_bulk(symbols, cache_start, cache_end)
        for symbol, recs in records.items():
            self._store[symbol] = sorted(recs, key=lambda r: r.timestamp)
        total = sum(len(v) for v in self._store.values())
        print(f"  [Cache] Loaded {total:,} records for {len(self._store)} symbols\n")
        self._warm = True

    def get_ohlc(self, symbol, start, end):
        self._ensure_symbol(symbol)
        return [r for r in self._store.get(symbol, []) if start <= r.timestamp <= end]

    def get_ohlc_bulk(self, symbols, start, end):
        missing = [s for s in symbols if s not in self._store]
        if missing:
            self._load_symbols(missing)
        result = {}
        for symbol in symbols:
            sliced = [r for r in self._store.get(symbol, []) if start <= r.timestamp <= end]
            if sliced:
                result[symbol] = sliced
        return result

    def __getattr__(self, name):
        return getattr(self._repo, name)

    def _ensure_symbol(self, symbol):
        if symbol not in self._store:
            self._load_symbols([symbol])

    def _load_symbols(self, symbols):
        records = self._repo.get_ohlc_bulk(symbols, self._CACHE_START, self._CACHE_END)
        for sym, recs in records.items():
            self._store[sym] = sorted(recs, key=lambda r: r.timestamp)
        for sym in symbols:
            if sym not in self._store:
                self._store[sym] = []


# ─── Main ─────────────────────────────────────────────────────────────────

_STRAT_NAMES = ["DualMA", "Breakout", "QuietBrk", "TrendPB", "RSI-MR"]

# Collect all output lines so we can write both to stdout and MD
_lines = []


def out(line=""):
    print(line)
    _lines.append(line)


def _extract(result):
    if not result:
        return 0.0, 0.0, 0.0, 0.0, 0
    pm = result["portfolio_metrics"]
    tm = result["trade_metrics"]
    return (
        pm.get("sharpe_ratio", 0.0) or 0.0,
        (pm.get("total_return", 0.0) or 0.0) * 100,
        (pm.get("max_drawdown", 0.0) or 0.0) * 100,
        (tm.get("win_rate_trade", 0.0) or 0.0) * 100,
        tm.get("num_trades", 0),
    )


# Hardcoded from the previous ATR multiplier sweep (Part E of results doc)
_ATR25_RESULTS = {
    "Full  2018–2024":  (1.17, 63.96, 10.18, 46.4, 6201),
    "Bull  2019–2020":  (-0.63, -3.68, 7.40, 42.2, 1102),
    "Crash 2020":       (2.22, 19.83, 4.71, 51.4, 1042),
    "Recov 2020–2021":  (2.64, 46.54, 6.30, 51.2, 2068),
    "Bear  2022":       (0.33, 1.79, 5.86, 42.2, 737),
    "Recent2022–2024":  (1.23, 21.20, 5.86, 46.5, 2060),
    "Live  2025–2026":  (-0.61, -3.01, 4.77, 39.0, 712),
}

V1_BASELINE = {
    "Full  2018–2024":  (1.21, 97.77, 15.15, 46.5, 6269),
    "Bull  2019–2020":  (-0.56, -4.28, 9.44, 42.5, 1127),
    "Crash 2020":       (2.46, 28.90, 6.23, 51.7, 1049),
    "Recov 2020–2021":  (2.88, 77.57, 8.88, 51.5, 2088),
    "Bear  2022":       (0.32, 2.29, 8.25, 41.6, 762),
    "Recent2022–2024":  (1.27, 29.15, 8.25, 46.3, 2078),
    "Live  2025–2026":  (-0.43, -2.79, 4.94, 39.1, 757),
}

# Hardcoded from Part H — ATR×2.5 + vol_ratio>1.2 volume filter (committed 2026-05-10)
_VOLFILTER_RESULTS = {
    "Full  2018–2024":  (1.18, 64.80, 9.84, 46.5, 6178),
    "Bull  2019–2020":  (-0.57, -3.39, 7.27, 42.6, 1093),
    "Crash 2020":       (2.19, 19.56, 4.71, 51.2, 1040),
    "Recov 2020–2021":  (2.62, 46.11, 6.30, 51.0, 2067),
    "Bear  2022":       (0.36,  1.93, 5.76, 42.7,  728),
    "Recent2022–2024":  (1.24, 21.24, 5.76, 46.6, 2046),
    "Live  2025–2026":  (-0.60, -2.98, 4.76, 39.3,  704),
}


def _make_router_regime_exit():
    """Router with exit-only regime-conditional TrendPB target.

    Entry check stays at ×1.05 (strong pre-pullback filter unchanged).
    Only the profit exit varies by vol-regime: LOW_VOL→1.03, MID_VOL→1.05, HIGH_VOL→1.08.
    """
    return MultiStrategyRouter(
        strategies={
            "DualMA":   DualMovingAverageStrategy(),
            "Breakout": BreakoutMomentumStrategy(),
            "QuietBrk": QuietBreakoutStrategy(),
            "TrendPB":  TrendPullbackStrategy(
                            pullback_threshold=0.05,
                            target_mult_by_vol=None,   # uses _DEFAULT_TARGET_MULTS
                        ),
            "RSI-MR":   RSIMeanReversionStrategy(
                            rsi_oversold=5, rsi_overbought=80, max_hold_days=7),
        },
        weights={"DualMA": 0.20, "Breakout": 0.20, "QuietBrk": 0.20,
                 "TrendPB": 0.20, "RSI-MR": 0.20},
        allowed_regimes=_ALLOWED_REGIMES,
    )


def run_baseline():
    _base      = MarketDataRepository()
    repository = OHLCCache(_base)
    repository.warm_all(BROAD_UNIVERSE)

    # {period_label: result} — TrendPB with regime-conditional profit target
    new_results = {}

    for period_label, (start_date, end_date) in PERIODS.items():
        ctx = PeriodContext(repository, start_date, end_date)

        out()
        out("=" * (ROW_W + 2))
        out(f"  Period: {period_label.strip()}   ({start_date.date()} → {end_date.date()})")
        out(f"  Universe: {len(BROAD_UNIVERSE)} symbols → DynamicUniverse top 80 → UnionFilter")
        out(f"  Risk: capital=₹{INITIAL_CAPITAL:,}  max_pos={MAX_POSITION_PCT*100:.0f}%  "
            f"risk/trade={RISK_PER_TRADE_PCT*100:.1f}%  CB={MAX_DOWNTREND_PCT*100:.0f}%")
        out(f"  Costs: 0.10% commission + 0.05% slippage per side")
        out("=" * (ROW_W + 2))
        out(HEADER)

        out(f"{DIVIDER}  [TrendPB ExitOnly] ATR×2.5 + vol filter + regime-conditional EXIT only "
            f"(entry stays ×1.05; exit: LOW_VOL→×1.03, MID_VOL→×1.05, HIGH_VOL→×1.08)")
        router = _make_router_regime_exit()
        result = _run_one(repository, router, ctx, atr_multiplier=2.5)
        out(_fmt_row("EqW  ExitOnly", result))
        new_results[period_label.strip()] = result

    # ── Summary: Part H (vol filter) vs exit-only regime-conditional target ──
    CONFIGS = [
        ("ATR×2.5 +Vol",   _VOLFILTER_RESULTS),  # Part H hardcoded baseline
        ("TrendPB ExitOnly", None),               # this fresh run
    ]

    out()
    out("=" * (ROW_W + 2))
    out("  SUMMARY — TrendPullback exit-only regime-conditional target")
    out("  Baseline: Part H (ATR×2.5 + vol filter, fixed ×1.05 exit).")
    out("  New:      entry stays ×1.05; exit LOW_VOL→×1.03 / MID→×1.05 / HIGH→×1.08.")
    out("=" * (ROW_W + 2))

    col_w = 14

    def _hdr():
        return ("  " + f"{'Period':<20} " +
                "".join(f"{lbl:>{col_w}}" for lbl, _ in CONFIGS))

    def _v(label, plabel, field_idx, rdict):
        if rdict is None:
            r = new_results.get(plabel)
            return _extract(r)[field_idx] if r else 0.0
        return rdict.get(plabel, (0,)*5)[field_idx]

    for metric_name, field_idx, fmt in [
        ("Sharpe ratio",           0, lambda v: f"{v:>{col_w}.2f}"),
        ("Return %",               1, lambda v: f"{v:>{col_w-1}.1f}%"),
        ("MaxDD %  (lower=better)",2, lambda v: f"{v:>{col_w-1}.1f}%"),
        ("Win Rate %",             3, lambda v: f"{v:>{col_w-1}.1f}%"),
        ("Profit Factor",          None, None),  # placeholder — extracted below
        ("#Trades",                4, lambda v: f"{v:>{col_w}}"),
    ]:
        if field_idx is None:
            continue
        out(f"\n  {metric_name}")
        out(_hdr())
        out(f"  {'-' * (20 + len(CONFIGS) * col_w + 2)}")
        for plabel in new_results:
            row = f"  {plabel:<20} "
            for lbl, rdict in CONFIGS:
                val = _v(lbl, plabel, field_idx, rdict)
                row += fmt(val)
            out(row)

    out()
    out(f"  Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    out(f"  Config ID: f786f5cc-09f7-43b2-afbb-4f0b688f55d2 (Ujjwal's Portfolio)")
    out("=" * (ROW_W + 2))
    out("=" * (ROW_W + 2))


def append_results_to_md():
    """Append Part J results to the existing MD file."""
    md_path = "docs/baseline_backtest_results.md"
    results_block = (
        "\n\n---\n\n"
        "## Part J — TrendPullback Exit-Only Regime-Conditional Target\n\n"
        "> Baseline (Part H): ATR×2.5 + vol filter, fixed ×1.05 exit.  \n"
        "> New: entry stays ×1.05; exit only: LOW_VOL→×1.03 / MID_VOL→×1.05 / HIGH_VOL→×1.08.  \n"
        "> (Part I tested both entry+exit change — reverted; this isolates exit only.)\n\n"
        f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}  \n"
        f"**Costs:** 0.10% commission + 0.05% slippage per side\n\n"
        "```\n"
        + "\n".join(_lines)
        + "\n```\n"
    )
    with open(md_path, "a") as f:
        f.write(results_block)
    print(f"\n  Results appended to {md_path}")


if __name__ == "__main__":
    import os
    from dotenv import load_dotenv
    load_dotenv()

    run_baseline()
    append_results_to_md()
