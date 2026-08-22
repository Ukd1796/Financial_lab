"""Derived quarterly metrics.

Every metric returns a :class:`MetricResult` rather than a bare number, so a
value that could not be computed is distinguishable from a value that genuinely
is zero, and the inputs behind it stay auditable.

Two rules follow from earlier findings:

* **Seasonal comparisons address the year-ago quarter by calendar bucket**, not
  by counting four rows back.  Sources drop quarters silently (see
  ``app/analysis/fundamentals``), and counting rows across a hole compares the
  wrong periods while looking perfectly healthy.
* **Ratios off a non-positive base are undefined, not large.**  Percentage
  growth from a loss-making or zero quarter has no meaning; returning a number
  there manufactures enormous fake surprises exactly where earnings are most
  volatile.

These are descriptive quantities.  Nothing here ranks, scores, or forecasts.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date

from app.analysis.fundamentals import FundamentalsSeries, QuarterFacts

METRIC_OK = "OK"
METRIC_MISSING_INPUT = "MISSING_INPUT"
METRIC_MISSING_COMPARISON = "MISSING_COMPARISON_QUARTER"
METRIC_UNDEFINED_BASE = "UNDEFINED_BASE"
METRIC_UNKNOWN_QUARTER = "UNKNOWN_QUARTER"

QUARTERS_PER_YEAR = 4


@dataclass(frozen=True)
class MetricResult:
    name: str
    value: float | None
    status: str
    period_end: date | None = None
    inputs: dict[str, float | None] = field(default_factory=dict)
    note: str = ""

    @property
    def ok(self) -> bool:
        return self.status == METRIC_OK


def _fail(name: str, status: str, period_end: date | None, **inputs: float | None):
    return MetricResult(
        name=name, value=None, status=status, period_end=period_end, inputs=inputs
    )


def _ratio(
    name: str, numerator: float | None, denominator: float | None, period_end: date
) -> MetricResult:
    if numerator is None or denominator is None:
        return _fail(
            name,
            METRIC_MISSING_INPUT,
            period_end,
            numerator=numerator,
            denominator=denominator,
        )
    if denominator <= 0:
        return MetricResult(
            name=name,
            value=None,
            status=METRIC_UNDEFINED_BASE,
            period_end=period_end,
            inputs={"numerator": numerator, "denominator": denominator},
            note="denominator is not positive; the ratio has no interpretation",
        )
    return MetricResult(
        name=name,
        value=numerator / denominator,
        status=METRIC_OK,
        period_end=period_end,
        inputs={"numerator": numerator, "denominator": denominator},
    )


def operating_margin(quarter: QuarterFacts) -> MetricResult:
    return _ratio(
        "operating_margin",
        quarter.values.get("operating_income"),
        quarter.values.get("revenue"),
        quarter.period_end,
    )


def net_margin(quarter: QuarterFacts) -> MetricResult:
    return _ratio(
        "net_margin",
        quarter.values.get("net_income"),
        quarter.values.get("revenue"),
        quarter.period_end,
    )


def seasonal_change(
    series: FundamentalsSeries, period_end: date, field_name: str
) -> MetricResult:
    """Year-on-year fractional change for one field, addressed by bucket.

    Returns ``MISSING_COMPARISON_QUARTER`` when the year-ago quarter is absent
    from the series, rather than substituting whichever quarter happens to sit
    four positions away.
    """
    name = f"seasonal_change_{field_name}"
    by_bucket = series.by_bucket()

    current = series.quarter_ending(period_end)
    if current is None:
        return _fail(name, METRIC_UNKNOWN_QUARTER, period_end)

    prior = by_bucket.get(current.bucket - QUARTERS_PER_YEAR)
    if prior is None:
        return MetricResult(
            name=name,
            value=None,
            status=METRIC_MISSING_COMPARISON,
            period_end=period_end,
            note="year-ago quarter is absent from the series",
        )

    now = current.values.get(field_name)
    then = prior.values.get(field_name)
    inputs = {"current": now, "year_ago": then}

    if now is None or then is None:
        return MetricResult(
            name=name,
            value=None,
            status=METRIC_MISSING_INPUT,
            period_end=period_end,
            inputs=inputs,
        )
    if then <= 0:
        return MetricResult(
            name=name,
            value=None,
            status=METRIC_UNDEFINED_BASE,
            period_end=period_end,
            inputs=inputs,
            note="year-ago value is not positive; fractional change is meaningless",
        )
    return MetricResult(
        name=name,
        value=(now - then) / then,
        status=METRIC_OK,
        period_end=period_end,
        inputs=inputs,
    )


def latest_metrics(series: FundamentalsSeries) -> dict[str, MetricResult]:
    """Every supported metric for the most recent quarter in the series."""
    latest = series.latest
    if latest is None:
        return {}

    results = {
        "operating_margin": operating_margin(latest),
        "net_margin": net_margin(latest),
    }
    for field_name in ("basic_eps", "revenue", "net_income"):
        metric = seasonal_change(series, latest.period_end, field_name)
        results[metric.name] = metric
    return results
