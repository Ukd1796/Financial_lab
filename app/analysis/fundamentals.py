"""Normalised quarterly fundamentals for the analysis layer.

This module extracts facts.  It does not score, rank, or predict — OQ1-OQ7
(see docs/research_log.md) established that adding transformations of data we
already hold produces coin-flip signals, so the analysis layer is deliberately
descriptive and its outputs are all independently checkable.

Two properties are load-bearing:

**Gaps are first-class.**  A live probe of ``RELIANCE.NS`` returned quarters
ending 2026-06, 2026-03, 2025-12, 2025-06, 2025-03 — the September 2025 quarter
is simply absent, with no error raised.  Anything that compares a quarter to
"four rows back" would silently straddle that hole and compute a nonsense
seasonal change.  Quarters are therefore addressed by calendar bucket, never by
list position, and absent buckets are reported rather than closed up.

**Nothing is imputed.**  A value that is missing stays ``None`` and the reason
travels with it, following the same discipline as
``app/event_research/xbrl_parser.py``.

The yfinance source is restated, has no publication timestamp, and carries no
survivorship control, so :attr:`FundamentalsSeries.is_point_in_time` is always
False for it.  Callers that intend to measure a historical edge must check that
flag; this data cannot support it.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime, timezone
from typing import Iterable, Protocol


SOURCE_YFINANCE = "yfinance"

STATUS_VALID = "VALID"
STATUS_HAS_GAPS = "HAS_GAPS"
STATUS_INSUFFICIENT_HISTORY = "INSUFFICIENT_HISTORY"
STATUS_NO_DATA = "NO_DATA"
STATUS_SOURCE_ERROR = "SOURCE_ERROR"

# Minimum quarters needed before a seasonal (year-on-year) comparison exists.
MIN_QUARTERS_FOR_SEASONAL = 5

# Canonical field -> candidate source labels, in preference order.  yfinance
# renames rows between releases and between companies, so the first label that
# resolves wins rather than assuming a single spelling.
FIELD_LABELS: dict[str, tuple[str, ...]] = {
    "revenue": ("Total Revenue", "Operating Revenue", "Sales", "Revenue"),
    "operating_income": (
        "Operating Income",
        "Total Operating Income As Reported",
        "Operating Profit",
    ),
    "ebitda": ("EBITDA", "Normalized EBITDA"),
    "net_income": (
        "Net Income",
        "Net Income Common Stockholders",
        "Net Income From Continuing Operation Net Minority Interest",
        "Net Profit",
    ),
    "basic_eps": ("Basic EPS", "EPS in Rs"),
    "diluted_eps": ("Diluted EPS",),
}

FIELDS: tuple[str, ...] = tuple(FIELD_LABELS)


def quarter_bucket(period_end: date) -> int:
    """Map a period end onto a monotonic calendar-quarter index.

    Addressing quarters by bucket is what makes a missing quarter detectable:
    consecutive reports differ by exactly one, so any larger step is a hole.
    """
    return period_end.year * 4 + (period_end.month - 1) // 3


@dataclass(frozen=True)
class QuarterFacts:
    period_end: date
    values: dict[str, float | None]

    @property
    def bucket(self) -> int:
        return quarter_bucket(self.period_end)

    @property
    def missing_fields(self) -> tuple[str, ...]:
        return tuple(f for f in FIELDS if self.values.get(f) is None)

    @property
    def is_empty(self) -> bool:
        """True when the period exists but carries no usable value.

        Observed on ``INFY.NS``: the feed returns a column for the quarter with
        every field null.  Counting it as present would report an unbroken
        series that cannot actually be compared against.
        """
        return len(self.missing_fields) == len(FIELDS)


@dataclass(frozen=True)
class FundamentalsSeries:
    """Quarterly facts for one symbol, in ascending period order."""

    symbol: str
    source: str
    retrieved_at: datetime
    is_point_in_time: bool
    quarters: tuple[QuarterFacts, ...] = ()
    missing_buckets: tuple[int, ...] = ()
    empty_buckets: tuple[int, ...] = ()
    status: str = STATUS_NO_DATA
    notes: tuple[str, ...] = field(default_factory=tuple)

    @property
    def unusable_buckets(self) -> tuple[int, ...]:
        """Quarters that cannot be compared against: absent or entirely null."""
        return tuple(sorted(set(self.missing_buckets) | set(self.empty_buckets)))

    def by_bucket(self) -> dict[int, QuarterFacts]:
        return {q.bucket: q for q in self.quarters}

    def quarter_ending(self, period_end: date) -> QuarterFacts | None:
        return self.by_bucket().get(quarter_bucket(period_end))

    @property
    def latest(self) -> QuarterFacts | None:
        return self.quarters[-1] if self.quarters else None

    @property
    def reported_fields(self) -> tuple[str, ...]:
        """Fields this source populates at least once.

        Feeds carry different vocabularies — a Screener-derived source has no
        EBITDA or diluted EPS row at all.  Separating "this source never carries
        the field" from "this quarter is missing it" keeps a vocabulary
        difference from reading as a data defect.
        """
        return tuple(
            f
            for f in FIELDS
            if any(q.values.get(f) is not None for q in self.quarters)
        )

    @property
    def effective_coverage(self) -> float:
        """Coverage across only the fields this source actually supplies."""
        reported = self.reported_fields
        if not self.quarters or not reported:
            return 0.0
        present = sum(
            1 for q in self.quarters for f in reported if q.values.get(f) is not None
        )
        return present / (len(self.quarters) * len(reported))

    @property
    def coverage(self) -> float:
        """Share of non-null values across every field of every quarter."""
        if not self.quarters:
            return 0.0
        total = len(self.quarters) * len(FIELDS)
        present = sum(
            1 for q in self.quarters for f in FIELDS if q.values.get(f) is not None
        )
        return present / total


class FundamentalsSource(Protocol):
    """Supplies raw quarterly rows keyed by period end.

    Kept abstract so the analysis layer can be tested without network access,
    and so a paid feed can replace yfinance without touching normalisation.
    """

    name: str
    is_point_in_time: bool

    def fetch_quarterly(self, symbol: str) -> dict[date, dict[str, float | None]]:
        ...


def _coerce(value: object) -> float | None:
    if value is None:
        return None
    try:
        number = float(value)  # type: ignore[arg-type]
    except (TypeError, ValueError):
        return None
    # yfinance uses NaN for "not reported"; NaN != NaN is the cheapest check.
    return None if number != number else number


def _select(row: dict[str, float | None], labels: Iterable[str]) -> float | None:
    for label in labels:
        if label in row:
            value = _coerce(row[label])
            if value is not None:
                return value
    return None


def normalise(
    symbol: str,
    raw: dict[date, dict[str, float | None]],
    *,
    source: str,
    is_point_in_time: bool,
    retrieved_at: datetime | None = None,
) -> FundamentalsSeries:
    """Turn raw per-period rows into an ordered, gap-annotated series."""
    stamp = retrieved_at or datetime.now(timezone.utc)
    base = dict(
        symbol=symbol,
        source=source,
        retrieved_at=stamp,
        is_point_in_time=is_point_in_time,
    )

    if not raw:
        return FundamentalsSeries(
            **base, status=STATUS_NO_DATA, notes=("source returned no quarters",)
        )

    quarters = tuple(
        QuarterFacts(
            period_end=period_end,
            values={f: _select(row, FIELD_LABELS[f]) for f in FIELDS},
        )
        for period_end, row in sorted(raw.items())
    )

    buckets = [q.bucket for q in quarters]
    missing = tuple(
        b for b in range(buckets[0], buckets[-1] + 1) if b not in set(buckets)
    )

    empty = tuple(q.bucket for q in quarters if q.is_empty)

    notes: list[str] = []
    if missing:
        notes.append(
            f"{len(missing)} quarter(s) absent between "
            f"{quarters[0].period_end} and {quarters[-1].period_end}"
        )
    if empty:
        notes.append(
            f"{len(empty)} quarter(s) present but entirely null — the period is "
            "reported with no usable value"
        )
    if not is_point_in_time:
        notes.append(
            "restated source without publication timestamps — not valid for "
            "historical edge measurement"
        )

    # A quarter that exists but holds nothing breaks a seasonal comparison just
    # as an absent one does, so both drive the same status.
    usable = len(quarters) - len(empty)
    if missing or empty:
        status = STATUS_HAS_GAPS
    elif usable < MIN_QUARTERS_FOR_SEASONAL:
        status = STATUS_INSUFFICIENT_HISTORY
        notes.append(
            f"{usable} usable quarter(s); {MIN_QUARTERS_FOR_SEASONAL} needed for a "
            "seasonal comparison"
        )
    else:
        status = STATUS_VALID

    return FundamentalsSeries(
        **base,
        quarters=quarters,
        missing_buckets=missing,
        empty_buckets=empty,
        status=status,
        notes=tuple(notes),
    )


@dataclass
class YFinanceFundamentalsSource:
    """Free quarterly fundamentals via yfinance.

    Adequate for building and debugging the analysis layer.  Not adequate for
    evidence: coverage is patchy, quarters go missing without warning, the
    figures are restated rather than as-reported, and there is no publication
    timestamp from which a causal clock could be built.
    """

    name: str = SOURCE_YFINANCE
    is_point_in_time: bool = False

    def fetch_quarterly(self, symbol: str) -> dict[date, dict[str, float | None]]:
        import yfinance as yf

        frame = yf.Ticker(symbol).quarterly_financials
        if frame is None or frame.empty:
            return {}

        out: dict[date, dict[str, float | None]] = {}
        for column in frame.columns:
            period_end = getattr(column, "date", lambda: column)()
            if not isinstance(period_end, date):
                continue
            series = frame[column]
            out[period_end] = {
                str(label): series[label] for label in series.index
            }
        return out


def load_series(
    symbol: str, source: FundamentalsSource | None = None
) -> FundamentalsSeries:
    """Fetch and normalise one symbol, reporting source failure as status."""
    src = source or YFinanceFundamentalsSource()
    try:
        raw = src.fetch_quarterly(symbol)
    except Exception as exc:  # noqa: BLE001 - surfaced as a status, not raised
        return FundamentalsSeries(
            symbol=symbol,
            source=src.name,
            retrieved_at=datetime.now(timezone.utc),
            is_point_in_time=src.is_point_in_time,
            status=STATUS_SOURCE_ERROR,
            notes=(f"{type(exc).__name__}: {exc}",),
        )
    return normalise(
        symbol, raw, source=src.name, is_point_in_time=src.is_point_in_time
    )
