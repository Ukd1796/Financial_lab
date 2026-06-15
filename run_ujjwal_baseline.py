"""
Baseline backtest for Ujjwal's live portfolio configuration.

Profile (from pt_ujjwal / user_strategies id=f786f5cc):
  Universe:          broad150 (150 symbols: Nifty50 + NiftyNext50 + NiftyMidcap50)
  Strategies:        all 5 enabled
  max_position_pct:  10%
  risk_per_trade_pct: 0.5%
  pause_threshold_pct: 35%  → max_downtrend_pct=0.35 in RiskAgent
  capital:           ₹1,00,000

Usage:
  python run_ujjwal_baseline.py                  # EqualWeight + Adaptive (both)
  python run_ujjwal_baseline.py --equal-weight-only  # EqualWeight only — fast, no LLM calls

Default (no flag):
  Runs BOTH EqualWeight and AdaptiveStrategySelector side-by-side, producing a
  3-column summary: Part H baseline | EqW Current | Adaptive Current.

--equal-weight-only:
  Skips the LLM/Adaptive run. Use this for fast regression checks after code
  changes when you only care about confirming equal-weight results are unchanged.

Output: docs/baseline_backtest_results.md
"""

import sys
import io
import argparse
from datetime import datetime

# Load .env before any app imports so DATABASE_URL is available at import time
from dotenv import load_dotenv
load_dotenv()

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
from app.analytics.universe_tracker import compute_universe_diagnostics

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
    # "Full  2018–2024": (datetime(2018, 1, 1),  datetime(2024, 6, 1)),
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
    # Order matters: earlier filters get priority on overlap (UnionUniverseFilter
    # dedups by first-seen). Breakout listed before QuietBrk so the rare names
    # that satisfy both criteria are routed to Breakout, and QuietBrk gets the
    # activity tail (moderate-activity stocks Breakout's strict thresholds reject).
    # Tagged with strategy names so MultiStrategyRouter can gate each strategy's
    # symbol_states to its own slice via exclusive_strategies={"QuietBrk"} —
    # prevents Breakout from poaching QuietBrk's reserved activity-tail symbols.
    return UnionUniverseFilter([
        ("Breakout", BreakoutUniverseFilter(top_n=20)),
        ("QuietBrk", ActivityTailFilter(top_n=20)),
        ("TrendPB",  PullbackUniverseFilter(top_n=20)),
        ("RSI-MR",   MeanReversionUniverseFilter(top_n=20)),
        ("DualMA",   DualMAUniverseFilter(max_cross_age=5, top_n=30)),
    ])


def _make_router(universe_filter=None):
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
        per_strategy_universe_source=(
            (lambda: universe_filter.last_per_strategy_symbols)
            if universe_filter is not None else None
        ),
        exclusive_strategies={"QuietBrk"} if universe_filter is not None else None,
    )


def _run_one(repository, router, ctx, atr_multiplier=2.0,
             regime_multipliers=None,
             adaptive_selector=None, regime_context_agent=None,
             attrib_tracker=None):
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
        pnl_tracker=attrib_tracker,
    )
    results, trades = engine.run(BROAD_UNIVERSE, ctx.historical_dates)

    evaluator         = EvaluationAgent()
    portfolio_metrics = evaluator.evaluate(results, INITIAL_CAPITAL)
    trade_metrics     = evaluator.evaluate_trades(trades)
    return {"portfolio_metrics": portfolio_metrics, "trade_metrics": trade_metrics, "trades": trades}


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


def _print_router_diagnostics(label: str, router) -> None:
    counters = getattr(router, "diag_counters", None)
    if not counters:
        return
    if not any(c.get("signals_issued", 0) > 0 for c in counters.values()):
        return
    print(f"  {'-' * ROW_W}  [{label} — signal-drop diagnostics]")
    print(f"  {'Strategy':<12}{'issued':>9}{'won':>8}{'prio_loss':>11}{'own_block':>11}{'buy_rej':>9}{'pass_thru%':>12}")
    for name, c in counters.items():
        issued   = c.get("signals_issued", 0)
        won      = c.get("won_merge", 0)
        prio     = c.get("dropped_priority", 0)
        own      = c.get("dropped_ownership", 0)
        buy_rej  = c.get("buy_rejected", 0)
        survivors = max(won - buy_rej, 0)
        pct = (survivors / issued * 100.0) if issued > 0 else 0.0
        print(f"  {name:<12}{issued:>9}{won:>8}{prio:>11}{own:>11}{buy_rej:>9}{pct:>11.1f}%")


def _print_universe_overlap(label: str, universe_filter) -> None:
    # Reports how often each child filter's picks were already claimed by an
    # earlier filter in UnionUniverseFilter's dedup ordering. Low mean
    # (< 3/day) confirms the carve is structurally orthogonal; high mean
    # (> 8/day) means filters are competing for the same cohort.
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


def _print_strategy_attribution(attrib: "TradeAttributionTracker", label: str = "") -> None:
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
        print(f"  {name:<12} {n:>8} {pnl:>+12.0f} {wr:>8.1f}% {avg:>+10.0f} {share:>7.1f}%")
    print(f"  {'TOTAL':<12} {sum(len(v) for v in buckets.values()):>8} {total_pnl:>+12.0f}")


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

    def warm_all(self, symbols, start=None, end=None, batch_size=25):
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
        batches = [symbols[i:i + batch_size] for i in range(0, len(symbols), batch_size)]
        print(f"\n  [Cache] No local cache — pulling {len(symbols)} symbols from "
              f"Supabase ({cache_start.date()} → {cache_end.date()}) "
              f"in {len(batches)} batches of ≤{batch_size}...")
        print(f"  [Cache] Tip: run `finance/bin/python3 scripts/cache_market_data_locally.py` "
              f"once to avoid this in future runs.")
        for idx, batch in enumerate(batches, 1):
            print(f"  [Cache] Batch {idx}/{len(batches)} ({len(batch)} symbols)...", end=" ", flush=True)
            records = self._repo.get_ohlc_bulk(batch, cache_start, cache_end)
            for symbol, recs in records.items():
                self._store[symbol] = sorted(recs, key=lambda r: r.timestamp)
            print("done")
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

# Adaptive baseline — prompt v2 + weight-ordering fix (2026-05-13)
# stability_weeks=2, regime_age hint, inferred trend, SWITCH annotations, BUY sort
# Format: (sharpe, return_pct, maxdd_pct, win_rate_pct, num_trades)
_ADAPTIVE_BASELINE: dict = {
    "Full  2018–2024":  (1.36, 116.6, 17.1, 44.1, 5191),
    "Bull  2019–2020":  (-0.71, -5.8, 10.7, 39.4, 886),
    "Crash 2020":       (2.32, 29.7,  7.5, 47.3,  903),
    "Recov 2020–2021":  (2.88, 80.3,  9.0, 49.2, 1785),
    "Bear  2022":       (0.85,  6.5,  7.9, 41.5,  621),
    "Recent2022–2024":  (1.57, 38.9,  7.8, 43.9, 1753),
    "Live  2025–2026":  (-0.77, -5.9, 8.1, 36.4,  635),
}


def run_baseline(equal_weight_only: bool = False):
    _base      = MarketDataRepository()
    repository = OHLCCache(_base)
    repository.warm_all(BROAD_UNIVERSE)

    eqw_results      = {}
    adaptive_results = {}

    if equal_weight_only:
        out("  Mode: --equal-weight-only (deterministic, no LLM calls)")
    else:
        out("  Mode: EqualWeight + Adaptive+RCA (both; gpt-4o, rebalance every 5 days, RegimeContextAgent)")

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

        # Per-period analytics setup — universe tracker computed once,
        # passed to annotate() so universe_rank_at_entry is populated.
        _annotator    = TradeAnnotator(repository, observer=ctx.observer)
        _univ_tracker = compute_universe_diagnostics(ctx, ctx.universe_filter)
        _period_enriched = []

        # ── EqualWeight ──
        out(f"{DIVIDER}  [EqW] ATR×2.5 trailing stop + volume filter")
        router     = _make_router(universe_filter=ctx.universe_filter)
        _ew_attrib = TradeAttributionTracker(list(_STRAT_NAMES))
        eqw_result = _run_one(repository, router, ctx, atr_multiplier=2.5,
                              attrib_tracker=_ew_attrib)
        out(_fmt_row("EqW  Current", eqw_result))
        eqw_results[period_label.strip()] = eqw_result
        _print_router_diagnostics("EqW", router)
        _print_strategy_attribution(_ew_attrib, "EqW")
        if eqw_result:
            _period_enriched.extend(_annotator.annotate(
                eqw_result["trades"],
                attribution_tracker=_ew_attrib,
                universe_tracker=_univ_tracker,
                period_label=period_label.strip(),
                run_label="EqW",
            ))

        # ── Adaptive (LLM) ──
        if not equal_weight_only:
            out(f"{DIVIDER}  [Adaptive+RCA] ATR×2.5 + AdaptiveStrategySelector + RegimeContextAgent")
            router   = _make_router(universe_filter=ctx.universe_filter)
            selector = AdaptiveStrategySelector(
                strategy_names=_STRAT_NAMES,
                model="gpt-4o",
                rebalance_frequency_days=5,
                regime_stability_weeks=2,
                verbose=True,
            )
            _adaptive_attrib = TradeAttributionTracker(list(_STRAT_NAMES))
            adaptive_result  = _run_one(repository, router, ctx, atr_multiplier=2.5,
                                        adaptive_selector=selector,
                                        regime_context_agent=ctx.regime_context_agent,
                                        attrib_tracker=_adaptive_attrib)
            out(_fmt_row("Adaptive+RCA (LLM)", adaptive_result))
            adaptive_results[period_label.strip()] = adaptive_result
            _print_router_diagnostics("Adaptive+RCA", router)
            _print_strategy_attribution(_adaptive_attrib, "Adaptive+RCA")
            if adaptive_result:
                _period_enriched.extend(_annotator.annotate(
                    adaptive_result["trades"],
                    attribution_tracker=_adaptive_attrib,
                    universe_tracker=_univ_tracker,
                    period_label=period_label.strip(),
                    run_label="Adaptive+RCA",
                ))

        # ── Period-end analytics ──
        if _period_enriched:
            _oqe = compute_opportunity_quality_metrics(_period_enriched)
            print_opportunity_quality_summary(_oqe)
            export_enriched_trades_csv(_period_enriched, "trade_analytics.csv")
        _print_universe_overlap(period_label.strip(), ctx.universe_filter)

    # ── Summary ──
    if equal_weight_only:
        CONFIGS = [
            ("Part H baseline", _VOLFILTER_RESULTS),
            ("EqW Current",     None),        # None → pull from eqw_results
        ]
        summary_note = (
            "Part H: ATR×2.5 trailing stop + volume filter (committed reference).\n"
            "  EqW Current: this run — confirms no regression from code changes."
        )
        summary_title = "SUMMARY — EqualWeight current vs Part H baseline"
        new_results = eqw_results
    else:
        CONFIGS = [
            ("Part H baseline",   _VOLFILTER_RESULTS),
            ("EqW Current",       None),       # None → pull from eqw_results
            ("Adaptive+RCA",       "adaptive"),  # sentinel → pull from adaptive_results
        ]
        summary_note = (
            "Part H: ATR×2.5 committed reference.  "
            "EqW: equal-weight this run.  Adaptive+RCA: LLM-rebalanced + RegimeContextAgent (matches live)."
        )
        summary_title = "SUMMARY — Part H baseline vs EqW vs Adaptive+RCA"
        new_results = eqw_results

    out()
    out("=" * (ROW_W + 2))
    out(f"  {summary_title}")
    out(f"  {summary_note}")
    out("=" * (ROW_W + 2))

    col_w = 18

    def _hdr():
        return ("  " + f"{'Period':<20} " +
                "".join(f"{lbl:>{col_w}}" for lbl, _ in CONFIGS))

    def _v(label, plabel, field_idx, rdict):
        if rdict == "adaptive":
            r = adaptive_results.get(plabel)
            return _extract(r)[field_idx] if r else 0.0
        if rdict is None:
            r = eqw_results.get(plabel)
            return _extract(r)[field_idx] if r else 0.0
        return rdict.get(plabel, (0,)*5)[field_idx]

    for metric_name, field_idx, fmt in [
        ("Sharpe ratio",           0, lambda v: f"{v:>{col_w}.2f}"),
        ("Return %",               1, lambda v: f"{v:>{col_w-1}.1f}%"),
        ("MaxDD %  (lower=better)",2, lambda v: f"{v:>{col_w-1}.1f}%"),
        ("Win Rate %",             3, lambda v: f"{v:>{col_w-1}.1f}%"),
        ("#Trades",                4, lambda v: f"{v:>{col_w}}"),
    ]:
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
    mode_str = "--equal-weight-only" if equal_weight_only else "EqualWeight + Adaptive (LLM)"
    out(f"  Mode: {mode_str}")
    out(f"  Config ID: f786f5cc-09f7-43b2-afbb-4f0b688f55d2 (Ujjwal's Portfolio)")
    out("=" * (ROW_W + 2))
    out("=" * (ROW_W + 2))


def append_results_to_md(equal_weight_only: bool = False):
    """Append latest run to the existing MD file."""
    md_path = "docs/baseline_backtest_results.md"
    mode_desc = (
        "EqualWeight only (ATR×2.5, no LLM)."
        if equal_weight_only else
        "EqualWeight + AdaptiveStrategySelector + RegimeContextAgent (gpt-4o, weekly LLM rebalance, matches live)."
    )
    results_block = (
        "\n\n---\n\n"
        "## Latest Run\n\n"
        f"> Config: {mode_desc}  \n\n"
        f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}  \n"
        f"**Mode:** {'--equal-weight-only' if equal_weight_only else 'EqualWeight + Adaptive+RCA'}  \n"
        f"**Costs:** 0.10% commission + 0.05% slippage per side\n\n"
        "```\n"
        + "\n".join(_lines)
        + "\n```\n"
    )
    with open(md_path, "a") as f:
        f.write(results_block)
    print(f"\n  Results appended to {md_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ujjwal baseline backtest runner")
    parser.add_argument(
        "--equal-weight-only",
        action="store_true",
        dest="equal_weight_only",
        help="Skip Adaptive/LLM run — fast regression check, no OpenAI calls",
    )
    args = parser.parse_args()
    run_baseline(equal_weight_only=args.equal_weight_only)
    append_results_to_md(equal_weight_only=args.equal_weight_only)
