"""Reproduce the power calculation charter v3 §6 is frozen against.

This reads **only** the price panel and the cohort snapshots.  It never touches
a filing, a surprise or a signal-return relationship, so running it spends none
of the pre-registration -- it measures how much noise a K-name book carries,
which is knowable before any hypothesis is tested.

Two numbers come out of it, and both are load-bearing in charter v3:

* the cross-sectional SD of 20-session peer-de-meaned return per cohort quarter,
* the standard error of the mean of a random K-name equal-weight book, measured
  empirically rather than assumed via sqrt(K).  The empirical figure is what
  captures residual within-quarter correlation; the sqrt(K) figure is printed
  beside it so the gap is visible rather than taken on trust.

Prices are keyed on **ISIN issuer prefix**, not full ISIN: a face-value change
mints a new ISIN, and 44 of the 597 cohort issuers carry more than one in the
panel.

Usage:
  finance/bin/python3 -m scripts.event_research.power_calculation
"""

from __future__ import annotations

import argparse
import csv
import glob
import os
import random
import sqlite3
import statistics
from pathlib import Path

HORIZON_SESSIONS = 20
ISSUER_PREFIX_LEN = 9
DEFAULT_BOOK_SIZES = (20, 30, 40, 60)
DEFAULT_DRAWS = 3000

# The folds charter v2 §2 fixed, so the per-fold standard errors below are
# reported against the windows the pass bar actually uses.
FOLD_QUARTERS = (("fold A ~6q", 6), ("fold B ~4q", 4), ("A+B+C ~11q", 11))


def trading_sessions(conn: sqlite3.Connection, exchange: str = "NSE") -> list[str]:
    """The exchange's own recorded calendar, including weekend special sessions.

    Deriving this from weekdays has already manufactured ~9,800 false corporate
    actions once (research log, 2026-08-14); the recorded status is the source.
    """
    return [
        row[0]
        for row in conn.execute(
            "SELECT session FROM price_sessions "
            "WHERE exchange = ? AND status = 'LOADED' ORDER BY session",
            (exchange,),
        )
    ]


def _closes_for(
    conn: sqlite3.Connection, session: str, prefixes: set[str], exchange: str
) -> dict[str, float]:
    out: dict[str, float] = {}
    for isin, close in conn.execute(
        "SELECT isin, close FROM daily_prices "
        "WHERE exchange = ? AND session = ? AND series = 'EQ'",
        (exchange, session),
    ):
        prefix = isin[:ISSUER_PREFIX_LEN]
        if prefix in prefixes and close:
            out[prefix] = close
    return out


def demeaned_returns(
    conn: sqlite3.Connection,
    cohort_csv: Path,
    sessions: list[str],
    *,
    exchange: str = "NSE",
) -> list[float] | None:
    """Peer-de-meaned 20-session returns for one cohort snapshot.

    De-meaning by the cohort's own cross-sectional mean is a stand-in for the
    frozen peer basket: it removes the market, which is what the standard error
    needs.  It is deliberately not the §1 peer rule -- this script sizes noise,
    it does not evaluate the study.
    """
    as_of = cohort_csv.stem.removeprefix("cohort_")
    with cohort_csv.open() as handle:
        prefixes = {row["isin"][:ISSUER_PREFIX_LEN] for row in csv.DictReader(handle)}

    anchor = next((s for s in sessions if s >= as_of), None)
    if anchor is None:
        return None
    start_index = sessions.index(anchor)
    if start_index + HORIZON_SESSIONS >= len(sessions):
        return None

    first, last = sessions[start_index], sessions[start_index + HORIZON_SESSIONS]
    opening = _closes_for(conn, first, prefixes, exchange)
    closing = _closes_for(conn, last, prefixes, exchange)

    returns = [
        closing[prefix] / opening[prefix] - 1.0
        for prefix in opening
        if prefix in closing
    ]
    if len(returns) < 50:
        return None
    mean = statistics.mean(returns)
    return [r - mean for r in returns]


def empirical_book_se(returns: list[float], book_size: int, draws: int) -> float:
    """SD of the mean of a random book, sampled rather than derived.

    sqrt(K) assumes the names are independent.  Sampling from the quarter's own
    de-meaned returns does not, so the gap between the two is a direct read on
    how much common variation survived de-meaning.
    """
    if book_size > len(returns):
        book_size = len(returns)
    means = [
        statistics.mean(random.sample(returns, book_size)) for _ in range(draws)
    ]
    return statistics.pstdev(means)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--panel-db", type=Path, default=Path("data/analysis/prices.sqlite"))
    parser.add_argument("--cohort-dir", type=Path, default=Path("data/event_research"))
    parser.add_argument("--draws", type=int, default=DEFAULT_DRAWS)
    parser.add_argument("--seed", type=int, default=0, help="Fixed so the table is reproducible")
    parser.add_argument("--cost-bar", type=float, default=1.10,
                        help="Charter v3 §3 bar in percent, for the coincidence check")
    args = parser.parse_args()

    random.seed(args.seed)
    conn = sqlite3.connect(f"file:{args.panel_db}?mode=ro", uri=True)
    try:
        sessions = trading_sessions(conn)
        print(f"NSE sessions: {len(sessions)}  {sessions[0]} .. {sessions[-1]}\n")

        per_quarter: dict[str, list[float]] = {}
        cohort_files = sorted(
            Path(p) for p in glob.glob(os.fspath(args.cohort_dir / "cohort_*.csv"))
        )
        print("Cross-sectional SD of 20-session peer-de-meaned return:")
        for cohort_csv in cohort_files:
            as_of = cohort_csv.stem.removeprefix("cohort_")
            returns = demeaned_returns(conn, cohort_csv, sessions)
            if returns is None:
                print(f"  {as_of}  skipped (no complete forward window)")
                continue
            per_quarter[as_of] = returns
            print(f"  {as_of}  n={len(returns):3d}  SD = {statistics.pstdev(returns) * 100:5.2f}%")

        if not per_quarter:
            raise SystemExit("No cohort quarter had a complete forward window")

        median_sd = statistics.median(
            statistics.pstdev(r) for r in per_quarter.values()
        )
        print(f"\n  median SD across {len(per_quarter)} quarters: {median_sd * 100:.2f}%")

        print(f"\nSE of the mean of a random K-name book ({args.draws} draws, seed {args.seed}):")
        for book_size in DEFAULT_BOOK_SIZES:
            empirical = statistics.median(
                empirical_book_se(r, book_size, args.draws) for r in per_quarter.values()
            )
            naive = statistics.median(
                statistics.pstdev(r) / min(book_size, len(r)) ** 0.5
                for r in per_quarter.values()
            )
            print(
                f"\n  K={book_size:3d}  empirical SE/quarter {empirical * 100:5.2f}%"
                f"   (naive sqrt(K): {naive * 100:5.2f}%)"
            )
            for label, quarters in FOLD_QUARTERS:
                fold_se = empirical / quarters**0.5
                needed = 2 * fold_se * 100
                marker = "  <- coincides with the cost bar" if (
                    book_size == 40
                    and label.startswith("fold A")
                    and abs(needed - args.cost_bar) < 0.15
                ) else ""
                print(
                    f"      {label:12s} SE {fold_se * 100:5.2f}%"
                    f"  -> t=2 needs {needed:5.2f}%/qtr{marker}"
                )
    finally:
        conn.close()


if __name__ == "__main__":
    main()
