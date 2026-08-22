"""Derive delisting outcomes from NSE bhavcopies. Costs no vendor API calls.

This produces the **labels** the red-flag work needs.  indianapi supplies what a
company looked like; it cannot supply what became of it — a failed company is
simply absent from the feed, with no date and no notice.  Bhavcopy records every
security that actually traded, so the session a name last appears in *is* its
exit date, and the price path into that session is what an owner experienced.

**Why no delisting reason is looked up.**  A merger at a premium and a
bankruptcy both remove a ticker, and a legal reason code treats them alike.  The
price path into the last trade separates them directly, using data already in
hand.  The reason is a proxy for the outcome; the price path is the outcome.

Three ways this could quietly produce wrong labels, each handled explicitly:

* **Renames.**  Keying on SYMBOL would read a ticker change as one death plus
  one birth — 102 such renames were measured between 2018 and 2026.  ISIN is
  the key throughout.
* **Suspensions.**  A name can vanish for months and return.  Gaps are counted
  and reported; only a trailing absence ends a series.
* **Splits and bonuses.**  Bhavcopy ``CLOSE`` is unadjusted, so a 1:10 split is
  a -90% move that is not a loss.  Detected actions are **back-adjusted** so the
  whole series sits on one share basis, rather than being withheld: RELIANCE's
  October-2024 bonus otherwise leaves it looking 58% below peak while trading
  near an all-time high.

**Why fall-from-peak rather than trailing return.**  The first version used the
trailing 12-month return and mislabelled DHFL and RCOM as benign exits — both
collapsed years before delisting and spent their last year bouncing as penny
stocks, so a one-year window measured the bounce. Distance below the lifetime
peak at the final trade identified both correctly, and is what an owner from the
peak actually experienced.
"""

from __future__ import annotations

import calendar
from collections.abc import Collection, Iterable
from dataclasses import dataclass, field
from datetime import date, timedelta

# Sampling is monthly.  A daily walk over eight years is ~2,000 downloads for a
# resolution the label does not need: the exit month plus the price path is
# enough to tell a collapse from a buyout.
MAX_BACKTRACK_DAYS = 12

STATUS_ACTIVE = "ACTIVE"
STATUS_EXIT_AFTER_COLLAPSE = "EXIT_AFTER_COLLAPSE"
STATUS_EXIT_FLAT_OR_UP = "EXIT_FLAT_OR_UP"
STATUS_EXIT_AMBIGUOUS = "EXIT_AMBIGUOUS"
STATUS_EXIT_UNKNOWN_PATH = "EXIT_UNKNOWN_PATH"
STATUS_INSTRUMENT_CHANGED = "INSTRUMENT_CHANGED"

# Leaving NSE is not dying.  Charter amendment v2 §4 defines "delisted" as
# absent from NSE *and* BSE, so listing survival is tracked as its own
# dimension rather than folded into `status`.  The two answer different
# questions and disagree for 111 of the 231 collapses: IL&FSTRANS, HDIL and
# SANWARIA all fell 70-95% off their peak and still trade on BSE today.  The
# money was lost either way — that is what `status` records — but the
# instrument did not stop existing, which is what this records.
LISTING_BSE_SAME_ISIN = "BSE_SAME_ISIN"
LISTING_BSE_ISSUER = "BSE_ISSUER"      # successor instrument, same issuer prefix
LISTING_ABSENT = "ABSENT"              # checked against BSE and not found — a true exit
LISTING_NOT_APPLICABLE = "NOT_APPLICABLE"  # never left NSE, so the question is moot
LISTING_UNCHECKED = "UNCHECKED"        # no reference data supplied; never assume ABSENT

# An ISIN's first nine characters identify the issuer; the last three identify
# the instrument.  A face-value change or split issues a NEW ISIN for the SAME
# company — INE092B01017 -> INE092B01025 — so keying deaths on ISIN alone
# invents one.  Measured 2026-08-12: 318 of 1,002 apparent deaths (32%) were
# this, including CONCOR, IEX, NBCC, ZENSARTECH and AVANTIFEED, all trading
# today.  Keying on SYMBOL instead reintroduces the rename problem, so identity
# is: same issuer prefix, and a successor instrument still trading.
ISIN_ISSUER_LENGTH = 9

# Indian ISINs beginning INF are mutual-fund and ETF units, not companies.  One
# AMC's prefix covers dozens of products (ICICI's INF109K.. spans 29 ETFs), so
# they both pollute an equity study and break issuer-identity reasoning.
NON_EQUITY_ISIN_PREFIX = "INF"


def isin_issuer(isin: str) -> str:
    return (isin or "")[:ISIN_ISSUER_LENGTH]


def is_company(isin: str) -> bool:
    return bool(isin) and not isin.startswith(NON_EQUITY_ISIN_PREFIX)

# AMENDED 2026-08-12 after inspecting known cases.  The original design used the
# trailing 12-month return alone, which mislabelled DHFL (+53%) and RCOM (+72%)
# as benign exits: both collapsed two to three years before delisting and spent
# their final year bouncing as penny stocks, so a one-year window measured the
# bounce rather than the failure.  Their fall from lifetime peak — -97% and -91%
# — identified both correctly.
#
# The *mechanism* was wrong, not the threshold; the amendment is recorded here
# and in docs/research_log.md rather than folded in silently.  Both figures are
# stored on every row, so any later screen can re-threshold either one.
COLLAPSE_DRAWDOWN = -0.70
BENIGN_DRAWDOWN = -0.25

# Ratios a split or bonus issue produces, checked against **month-over-month**
# moves rather than the whole-year change.  A year-long ratio cannot separate the
# two cases at all: 0.75 is equally a 3:4 bonus and an ordinary -25% year.  A
# split, by contrast, lands the entire move in one month at a near-exact ratio,
# which an organic decline does essentially never.
#
# Loose ratios (1/3, 1/4, 2/3, 3/4) are deliberately excluded: as monthly moves
# they are common enough organically that including them would withhold large
# numbers of genuine declines, which is the more damaging error here — the
# collapse population is the whole point of the exercise.
#
# 🔴 KNOWN LIMIT, measured 2026-08-12.  This detector is deliberately tight and
# therefore MISSES real actions.  RELIANCE's 1:1 bonus (ex-28-Oct-2024) shows as
# 2953.15 -> 1332.05, a ratio of 0.451 rather than 0.500, because the stock also
# fell ~10% that month; it is not adjusted.  Widening the tolerance does not fix
# this — at a loose band, 72 of the 231 collapse-labelled names match, and
# inspection shows most are genuine failures (GITANJALI, IL&FSTRANS, IVRCLINFRA,
# LEEL) that merely halved in a month, as collapsing stocks do.
#
# Monthly close ratios cannot identify corporate actions: the same observation is
# produced by a split and by a crash.  A correct fix needs an actual
# corporate-actions join (NSE's feed, or indianapi's /corporate_actions at one
# call per symbol) or daily data, where the ex-date's adjusted PREVCLOSE settles
# it.  Until then the tight setting is the right trade: a missed action on an
# ACTIVE name never reaches a label, whereas a false adjustment would erase a
# genuine collapse from the very population this exists to collect.
_ACTION_RATIOS = (1 / 2, 1 / 5, 1 / 10, 1 / 20, 1 / 100)
_RATIO_TOLERANCE = 0.015


def month_ends(start: date, end: date) -> list[date]:
    """Calendar month-ends in ``[start, end]``, ascending."""
    out: list[date] = []
    year, month = start.year, start.month
    while (year, month) <= (end.year, end.month):
        last = date(year, month, calendar.monthrange(year, month)[1])
        if start <= last <= end:
            out.append(last)
        month += 1
        if month > 12:
            year, month = year + 1, 1
    return out


def looks_like_corporate_action(ratio: float) -> bool:
    """Whether a *single-month* price ratio matches a split/bonus ratio.

    This is a heuristic, not proof.  Bhavcopy carries no face value and no
    adjustment factor, so the exact answer needs the NSE corporate-actions feed;
    that lookup is deliberately not a dependency here.  Adjustments applied are
    reported on the row so an over-eager match stays visible.
    """
    if ratio <= 0:
        return False
    return any(abs(ratio - r) <= _RATIO_TOLERANCE * r for r in _ACTION_RATIOS)


def split_adjusted(closes_by_index: dict[int, float]) -> tuple[dict[int, float], list[float]]:
    """Back-adjust a close series across detected split/bonus points.

    Without this, a 1:1 bonus reads as a −50% fall for the rest of the series:
    RELIANCE's October-2024 bonus made it look 58% below its peak while trading
    near an all-time high.  Prices *before* each detected action are divided by
    its ratio, so the whole series is expressed on the latest share basis.

    Returns the adjusted series and the ratios applied, so a caller can report
    that an adjustment happened rather than silently changing the numbers.
    """
    indexes = sorted(closes_by_index)
    ratios: list[float] = []
    for position, index in enumerate(indexes):
        if position == 0:
            continue
        previous = closes_by_index[indexes[position - 1]]
        current = closes_by_index[index]
        # Only adjacent sampled months: a gap could hide a genuine multi-month
        # decline that happens to land on a split-like ratio.
        if index - indexes[position - 1] != 1 or not previous:
            continue
        ratio = current / previous
        if looks_like_corporate_action(ratio):
            ratios.append(ratio)

    if not ratios:
        return dict(closes_by_index), []

    adjusted = dict(closes_by_index)
    factor = 1.0
    for position in range(len(indexes) - 1, 0, -1):
        index, prior = indexes[position], indexes[position - 1]
        previous, current = closes_by_index[prior], closes_by_index[index]
        if index - prior == 1 and previous and looks_like_corporate_action(current / previous):
            factor *= current / previous
        adjusted[prior] = closes_by_index[prior] * factor
    return adjusted, ratios


@dataclass
class Snapshot:
    """One sampled session: what traded, at what price."""

    session: date
    rows: dict[str, dict[str, str]] = field(default_factory=dict)  # isin -> row


def collect_monthly_snapshots(client, start: date, end: date, *, log=None) -> list[Snapshot]:
    """One bhavcopy per calendar month — the last session on or before month end.

    Walking back a few days handles weekends and exchange holidays without a
    holiday table, which is the same property that makes bhavcopy availability
    usable as the trading calendar.
    """
    from app.event_research.nse_client import NSEDocumentNotFound, NSEUnavailable

    snapshots: list[Snapshot] = []
    for target in month_ends(start, end):
        cursor = target
        for _ in range(MAX_BACKTRACK_DAYS):
            try:
                rows = client.fetch_bhavcopy(cursor)
            except NSEDocumentNotFound:
                cursor -= timedelta(days=1)
                continue
            except NSEUnavailable as exc:
                if log:
                    log(f"  {cursor}: unavailable ({exc}); month skipped")
                break

            keyed = {
                (row.get("ISIN") or "").strip(): row
                for row in rows
                if row.get("SERIES") == "EQ" and is_company((row.get("ISIN") or "").strip())
            }
            snapshots.append(Snapshot(session=cursor, rows=keyed))
            if log:
                log(f"  {cursor}: {len(keyed)} EQ securities")
            break
    return snapshots


def _close(row: dict[str, str]) -> float | None:
    try:
        value = float(row.get("CLOSE") or 0.0)
    except (TypeError, ValueError):
        return None
    return value if value > 0 else None


@dataclass
class Outcome:
    isin: str
    symbol: str
    first_seen: date
    last_seen: date
    months_observed: int
    gap_months: int
    last_close: float | None
    close_12m_before: float | None
    close_6m_before: float | None
    return_12m: float | None
    return_6m: float | None
    peak_close: float | None
    drawdown_from_peak: float | None
    status: str
    notes: str = ""
    # Independent of `status`: see the LISTING_* constants.  Defaults to
    # UNCHECKED so an un-annotated run can never be read as "confirmed dead".
    listed_elsewhere: str = LISTING_UNCHECKED


def annotate_listed_elsewhere(
    outcomes: Iterable[Outcome], reference_isins: Collection[str] | None
) -> list[Outcome]:
    """Record whether each NSE exit still trades on another exchange.

    ``reference_isins`` is a recent snapshot of what trades on the other
    exchange — "is this alive *now*", which is the question mortality asks, so
    it needs one current snapshot rather than a parallel history.

    Matching is tried on the exact ISIN first, then on the issuer prefix, for
    the same reason exits are: a face-value change reissues the ISIN, so an
    exact-only match would report a living issuer as absent.

    Passing ``None`` leaves every row UNCHECKED.  Absence of evidence is not
    recorded as evidence of absence — that distinction is the whole reason the
    2026-08-12 measurement mattered, when 48% of apparent deaths turned out to
    be still trading.
    """
    outcomes = list(outcomes)
    if reference_isins is None:
        return outcomes

    exact = {isin for isin in reference_isins if isin}
    issuers = {isin_issuer(isin) for isin in exact}

    for outcome in outcomes:
        if not outcome.status.startswith("EXIT"):
            outcome.listed_elsewhere = LISTING_NOT_APPLICABLE
        elif outcome.isin in exact:
            outcome.listed_elsewhere = LISTING_BSE_SAME_ISIN
        elif isin_issuer(outcome.isin) in issuers:
            outcome.listed_elsewhere = LISTING_BSE_ISSUER
        else:
            outcome.listed_elsewhere = LISTING_ABSENT
    return outcomes


def months_observed_count(indexes: list[int]) -> int:
    return len(indexes)


def build_outcomes(
    snapshots: list[Snapshot],
    *,
    collapse_drawdown: float = COLLAPSE_DRAWDOWN,
    benign_drawdown: float = BENIGN_DRAWDOWN,
) -> list[Outcome]:
    """Classify each ISIN's fate from its appearances across the samples."""
    if not snapshots:
        return []

    ordered = sorted(snapshots, key=lambda s: s.session)
    sessions = [s.session for s in ordered]
    final_session = sessions[-1]

    seen: dict[str, list[int]] = {}
    for index, snapshot in enumerate(ordered):
        for isin in snapshot.rows:
            seen.setdefault(isin, []).append(index)

    # Issuers still trading at the window end, by ISIN issuer prefix.  An ISIN
    # that stops while a sibling instrument of the same issuer continues is a
    # face-value change or split, not a death.
    live_issuers = {isin_issuer(isin) for isin in ordered[-1].rows}

    outcomes: list[Outcome] = []
    for isin, indexes in seen.items():
        first_index, last_index = indexes[0], indexes[-1]
        last_row = ordered[last_index].rows[isin]
        symbol = (last_row.get("SYMBOL") or "").strip()

        # Months inside the observed span where the name did not trade at all.
        span = last_index - first_index + 1
        gaps = span - len(indexes)

        raw_closes = {
            i: c for i in indexes if (c := _close(ordered[i].rows[isin])) is not None
        }
        # Adjust before measuring anything: on the raw series a bonus issue is
        # indistinguishable from a fall of the same size.
        closes_by_index, action_ratios = split_adjusted(raw_closes)

        last_close = closes_by_index.get(last_index, _close(last_row))
        close_12m = closes_by_index.get(last_index - 12)
        close_6m = closes_by_index.get(last_index - 6)

        def change(then: float | None, now: float | None = last_close) -> float | None:
            if then is None or now is None or then <= 0:
                return None
            return (now - then) / then

        return_12m, return_6m = change(close_12m), change(close_6m)

        closes = list(closes_by_index.values())
        peak = max(closes) if closes else None
        drawdown = (
            (last_close - peak) / peak if peak and last_close is not None and peak > 0 else None
        )

        notes: list[str] = []
        if gaps:
            notes.append(f"{gaps} month(s) absent then trading again — suspension, not exit")
        if action_ratios:
            notes.append(
                f"{len(action_ratios)} split/bonus adjustment(s) applied "
                f"({', '.join(f'{r:.3f}' for r in action_ratios)})"
            )

        if last_index == len(ordered) - 1:
            status = STATUS_ACTIVE
        elif (
            isin_issuer(isin) in live_issuers
            and (drawdown is None or drawdown > collapse_drawdown)
        ):
            # A surviving issuer code rescues the name ONLY if the holding did not
            # collapse first.  DHFL's prefix now belongs to PIRAMALFIN, which
            # absorbed it through insolvency — the entity continued, the equity was
            # wiped out.  We label what a holder experienced, not legal identity.
            status = STATUS_INSTRUMENT_CHANGED
            notes.append(
                "issuer still trades under a different ISIN — face-value change, "
                "split or rename, not an exit"
            )
        elif drawdown is None:
            status = STATUS_EXIT_UNKNOWN_PATH
            notes.append("no usable close within the window; path unknown")
        elif months_observed_count(indexes) < 2:
            # One sighting is a price, not a path: nothing can be said about how
            # the holding behaved before it went.
            status = STATUS_EXIT_UNKNOWN_PATH
            notes.append("only one observation; path unknown")
        else:
            # Fall from the lifetime peak, not the trailing year — a slow
            # collapse has usually finished long before the ticker disappears.
            if drawdown <= collapse_drawdown:
                status = STATUS_EXIT_AFTER_COLLAPSE
            elif drawdown >= benign_drawdown:
                status = STATUS_EXIT_FLAT_OR_UP
            else:
                status = STATUS_EXIT_AMBIGUOUS

        outcomes.append(
            Outcome(
                isin=isin,
                symbol=symbol,
                first_seen=sessions[first_index],
                last_seen=sessions[last_index],
                months_observed=len(indexes),
                gap_months=gaps,
                last_close=last_close,
                close_12m_before=close_12m,
                close_6m_before=close_6m,
                return_12m=return_12m,
                return_6m=return_6m,
                peak_close=peak,
                drawdown_from_peak=drawdown,
                status=status,
                notes="; ".join(notes),
            )
        )

    outcomes.sort(key=lambda o: (o.last_seen, o.symbol))
    return outcomes


class CachedBhavcopyClient:
    """Disk-caching wrapper so re-running the extractor downloads nothing.

    NSE is not metered, but a monthly sweep is still ~100 downloads at a
    courtesy delay.  Caching makes re-classification with a different threshold
    instant, which keeps the thresholds honest — a re-run should cost nothing,
    so there is no incentive to tune on a single pass.
    """

    def __init__(self, client, cache_dir):
        from pathlib import Path

        self.client = client
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.downloads = 0
        self.cache_hits = 0

    def fetch_bhavcopy(self, trade_date: date) -> list[dict[str, str]]:
        import json

        from app.event_research.nse_client import NSEDocumentNotFound

        path = self.cache_dir / f"{trade_date.isoformat()}.json"
        miss = self.cache_dir / f"{trade_date.isoformat()}.absent"
        if miss.exists():
            # Remembering "no session" matters as much as remembering the data:
            # without it every re-run re-walks every weekend and holiday.
            raise NSEDocumentNotFound(f"cached: no bhavcopy for {trade_date}")
        if path.exists():
            try:
                self.cache_hits += 1
                return json.loads(path.read_text())
            except json.JSONDecodeError:
                path.unlink()  # truncated write; fall through and re-fetch
                self.cache_hits -= 1

        try:
            rows = self.client.fetch_bhavcopy(trade_date)
        except NSEDocumentNotFound:
            miss.write_text("")
            raise

        # Only EQ rows are kept; the rest is 30% of the file and never read.
        keep = [r for r in rows if r.get("SERIES") == "EQ"]
        path.write_text(json.dumps(keep))
        self.downloads += 1
        return keep
