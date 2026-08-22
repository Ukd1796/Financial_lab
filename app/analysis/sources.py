"""Fundamentals sources behind a common protocol.

Keeping every feed behind ``FundamentalsSource`` means a vendor can be judged by
running the identical quality report over the identical symbols, rather than by
its marketing copy.  Normalisation, gap detection and metric rules are shared,
so any difference in the report is a difference in the data.

None of these sources is point-in-time.  They all serve the current view of
history, which is fine for a forward run and inadmissible for measuring a
historical edge.
"""

from __future__ import annotations

import calendar
import os
from dataclasses import dataclass
from datetime import date

from app.analysis.fundamentals import (  # noqa: F401 - re-exported for callers
    SOURCE_YFINANCE,
    FundamentalsSource,
    YFinanceFundamentalsSource,
)

SOURCE_INDIAN_API = "indianapi"

INDIAN_API_BASE = "https://stock.indianapi.in"
INDIAN_API_KEY_ENV = "INDIAN_API_KEY"

# Every `stats` value the free tier was confirmed to reach (2026-08-11 probe).
# All seven return the same transposed shape, so one parser covers them.
HISTORICAL_STATS = (
    "quarter_results",
    "yoy_results",
    "balancesheet",
    "cashflow",
    "ratios",
    "shareholding_pattern_quarterly",
    "shareholding_pattern_yearly",
)

_MONTHS = {m: i for i, m in enumerate(calendar.month_abbr) if m}


class MissingAPIKey(RuntimeError):
    """Raised when a paid source is selected without credentials."""


def parse_quarter_label(label: str) -> date | None:
    """Turn a ``"Jun 2024"`` column heading into that quarter's month end.

    Screener-derived feeds label quarters by month and year rather than by an
    explicit period end.  Returning the month end keeps the value comparable
    with feeds that report real dates, since both land in the same calendar
    bucket.
    """
    parts = label.strip().split()
    if len(parts) != 2:
        return None
    month = _MONTHS.get(parts[0][:3].title())
    if month is None:
        return None
    try:
        year = int(parts[1])
    except ValueError:
        return None
    return date(year, month, calendar.monthrange(year, month)[1])


def parse_transposed(payload: object) -> dict[date, dict[str, float | None]]:
    """Turn ``{metric: {"Jun 2024": value}}`` into ``{period_end: {metric: value}}``.

    Every one of the seven ``historical_stats`` vocabularies shares this shape;
    they differ only in which metric names appear.  Parsing structurally rather
    than against a known field list means a vocabulary this project has never
    seen still lands in the store instead of being silently discarded.
    """
    if not isinstance(payload, dict):
        return {}

    out: dict[date, dict[str, float | None]] = {}
    for metric, by_period in payload.items():
        if not isinstance(by_period, dict):
            continue
        for label, value in by_period.items():
            period_end = parse_quarter_label(str(label))
            if period_end is None:
                continue
            out.setdefault(period_end, {})[str(metric)] = value
    return out


@dataclass
class IndianAPIFundamentalsSource:
    """One ``stats`` vocabulary from indianapi.in's ``/historical_stats``.

    The response is transposed relative to most feeds — ``{metric: {quarter:
    value}}`` — and quarters are labelled ``"Jun 2024"``.  Both are normalised
    here so the rest of the analysis layer sees one shape.

    Rows are Screener-style (``Sales``, ``Operating Profit``, ``Net Profit``,
    ``EPS in Rs``), which suggests a Screener-derived pipeline: far deeper
    quarterly history than yfinance, still restated and still without a
    publication timestamp, so :attr:`is_point_in_time` stays False.

    Requests go through :class:`IndianAPIClient`, which enforces the call
    budget, paces to the provider's 1 req/sec limit and serves repeat reads
    from disk.  Constructing this source spends nothing.
    """

    stats: str = "quarter_results"
    api_key: str | None = None
    name: str = SOURCE_INDIAN_API
    is_point_in_time: bool = False
    base_url: str = INDIAN_API_BASE
    timeout_seconds: float = 30.0
    client: object | None = None

    def __post_init__(self) -> None:
        self.api_key = self.api_key or os.environ.get(INDIAN_API_KEY_ENV)

    def _client(self):
        if self.client is None:
            from app.analysis.indianapi_client import IndianAPIClient

            self.client = IndianAPIClient(
                api_key=self.api_key,
                base_url=self.base_url,
                timeout_seconds=self.timeout_seconds,
            )
        return self.client

    def fetch_raw(self, symbol: str) -> dict:
        """Return the untouched JSON, for inspecting an unfamiliar schema."""
        if not self.api_key:
            raise MissingAPIKey(
                f"set {INDIAN_API_KEY_ENV} to query {self.name}; "
                "a free key is issued on signup"
            )
        # Feeds keyed on NSE codes do not use the Yahoo suffix, so the same
        # symbol list can be pointed at either source.
        stock = symbol.split(".")[0]
        payload, _from_cache, _digest = self._client().get(
            "/historical_stats", {"stock_name": stock, "stats": self.stats}
        )
        return payload

    def fetch_quarterly(self, symbol: str) -> dict[date, dict[str, float | None]]:
        return parse_transposed(self.fetch_raw(symbol))


SOURCES: dict[str, type] = {
    SOURCE_YFINANCE: YFinanceFundamentalsSource,
    SOURCE_INDIAN_API: IndianAPIFundamentalsSource,
}


def get_source(name: str) -> FundamentalsSource:
    try:
        return SOURCES[name]()  # type: ignore[return-value]
    except KeyError:
        raise SystemExit(
            f"unknown source {name!r}; choose from {', '.join(sorted(SOURCES))}"
        ) from None
