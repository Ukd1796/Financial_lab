"""Tests for the analysis layer.

The behaviour worth protecting is refusal.  A fundamentals feed that quietly
drops a quarter, reports NaN, or posts a loss will produce confident-looking
numbers from naive code, and those numbers are indistinguishable from real ones
once they reach a table.  Each test below pins a case where the correct output
is "no value, and here is why".
"""

import unittest
from datetime import date, datetime, timezone

from app.analysis.fundamentals import (
    STATUS_HAS_GAPS,
    STATUS_INSUFFICIENT_HISTORY,
    STATUS_NO_DATA,
    STATUS_SOURCE_ERROR,
    STATUS_VALID,
    FundamentalsSeries,
    load_series,
    normalise,
    quarter_bucket,
)
from app.analysis.metrics import (
    METRIC_MISSING_COMPARISON,
    METRIC_OK,
    METRIC_UNDEFINED_BASE,
    net_margin,
    seasonal_change,
)


def _row(revenue=1000.0, operating=200.0, net=100.0, eps=10.0, **extra):
    row = {
        "Total Revenue": revenue,
        "Operating Income": operating,
        "Net Income": net,
        "Basic EPS": eps,
        "Diluted EPS": eps,
        "EBITDA": operating,
    }
    row.update(extra)
    return row


def _series(raw, *, is_pit=False):
    return normalise(
        "TEST.NS",
        raw,
        source="test",
        is_point_in_time=is_pit,
        retrieved_at=datetime(2026, 8, 11, tzinfo=timezone.utc),
    )


# Mirrors the live yfinance response for RELIANCE.NS observed 2026-08-10:
# the September 2025 quarter is absent with no error raised.
RELIANCE_SHAPED = {
    date(2025, 3, 31): _row(eps=12.0),
    date(2025, 6, 30): _row(eps=19.95),
    date(2025, 12, 31): _row(eps=14.0),
    date(2026, 3, 31): _row(eps=13.0),
    date(2026, 6, 30): _row(eps=15.48),
}


class FundamentalsTests(unittest.TestCase):
    def test_absent_quarter_is_detected_not_closed_up(self):
        series = _series(RELIANCE_SHAPED)
        self.assertEqual(series.status, STATUS_HAS_GAPS)
        self.assertEqual(series.missing_buckets, (quarter_bucket(date(2025, 9, 30)),))
        self.assertIn("absent", series.notes[0])

    def test_quarters_are_ordered_ascending_regardless_of_source_order(self):
        series = _series(RELIANCE_SHAPED)
        ends = [q.period_end for q in series.quarters]
        self.assertEqual(ends, sorted(ends))
        self.assertEqual(series.latest.period_end, date(2026, 6, 30))

    def test_nan_is_treated_as_missing_rather_than_a_number(self):
        series = _series({date(2026, 6, 30): _row(revenue=float("nan"))})
        self.assertIsNone(series.quarters[0].values["revenue"])
        self.assertIn("revenue", series.quarters[0].missing_fields)

    def test_label_preference_falls_back_to_alternate_spelling(self):
        row = _row()
        del row["Net Income"]
        row["Net Income Common Stockholders"] = 250.0
        series = _series({date(2026, 6, 30): row})
        self.assertEqual(series.quarters[0].values["net_income"], 250.0)

    def test_non_point_in_time_source_is_flagged_on_every_series(self):
        series = _series(RELIANCE_SHAPED)
        self.assertFalse(series.is_point_in_time)
        self.assertTrue(any("not valid for historical edge" in n for n in series.notes))

    def test_short_history_is_reported_as_insufficient_not_valid(self):
        series = _series({date(2026, 3, 31): _row(), date(2026, 6, 30): _row()})
        self.assertEqual(series.status, STATUS_INSUFFICIENT_HISTORY)

    def test_present_but_entirely_null_quarter_is_not_counted_as_usable(self):
        # Observed on INFY.NS: the feed returns a column for the quarter with
        # every field null.  Treating that as present reports an unbroken series
        # that nothing can actually be compared against.
        raw = {
            date(2025, 3, 31): _row(),
            date(2025, 6, 30): _row(),
            date(2025, 9, 30): {},
            date(2025, 12, 31): _row(),
            date(2026, 3, 31): _row(),
        }
        series = _series(raw)
        self.assertEqual(series.status, STATUS_HAS_GAPS)
        self.assertEqual(series.empty_buckets, (quarter_bucket(date(2025, 9, 30)),))
        self.assertIn(quarter_bucket(date(2025, 9, 30)), series.unusable_buckets)
        self.assertTrue(any("entirely null" in n for n in series.notes))

    def test_full_unbroken_history_is_valid(self):
        raw = {
            date(y, m, 30): _row()
            for y, m in [(2025, 3), (2025, 6), (2025, 9), (2025, 12), (2026, 3)]
        }
        self.assertEqual(_series(raw).status, STATUS_VALID)

    def test_empty_source_yields_no_data_not_an_exception(self):
        self.assertEqual(_series({}).status, STATUS_NO_DATA)

    def test_source_failure_becomes_a_status(self):
        class Broken:
            name = "broken"
            is_point_in_time = False

            def fetch_quarterly(self, symbol):
                raise ConnectionError("upstream refused")

        series = load_series("TEST.NS", Broken())
        self.assertEqual(series.status, STATUS_SOURCE_ERROR)
        self.assertIn("upstream refused", series.notes[0])


class MetricTests(unittest.TestCase):
    def test_seasonal_change_refuses_when_year_ago_quarter_is_missing(self):
        # 2025-09 is the absent quarter, so it is the 2026-09 report that has no
        # valid comparison.  This is not hypothetical: it is what Reliance's next
        # September filing will hit against this feed.
        raw = dict(RELIANCE_SHAPED)
        raw[date(2026, 9, 30)] = _row(eps=16.0)
        result = seasonal_change(_series(raw), date(2026, 9, 30), "basic_eps")
        self.assertEqual(result.status, METRIC_MISSING_COMPARISON)
        self.assertIsNone(result.value)

    def test_seasonal_change_addresses_by_calendar_not_by_position(self):
        # The trap this pins: with 2025-09 absent, 2025-03 sits exactly four
        # *positions* behind 2026-06, so counting rows would compare against
        # 12.0 and report growth.  The true year-ago quarter is 2025-06 at
        # 19.95, and the honest answer is a decline.
        series = _series(RELIANCE_SHAPED)
        result = seasonal_change(series, date(2026, 6, 30), "basic_eps")
        self.assertEqual(result.status, METRIC_OK)
        self.assertEqual(result.inputs["year_ago"], 19.95)
        self.assertAlmostEqual(result.value, (15.48 - 19.95) / 19.95)
        self.assertLess(result.value, 0)

    def test_growth_from_a_loss_making_quarter_is_undefined_not_enormous(self):
        raw = {
            date(2025, 6, 30): _row(eps=-5.0),
            date(2025, 9, 30): _row(),
            date(2025, 12, 31): _row(),
            date(2026, 3, 31): _row(),
            date(2026, 6, 30): _row(eps=5.0),
        }
        result = seasonal_change(_series(raw), date(2026, 6, 30), "basic_eps")
        self.assertEqual(result.status, METRIC_UNDEFINED_BASE)
        self.assertIsNone(result.value)

    def test_margin_on_zero_revenue_is_undefined(self):
        series = _series({date(2026, 6, 30): _row(revenue=0.0)})
        self.assertEqual(net_margin(series.latest).status, METRIC_UNDEFINED_BASE)

    def test_metric_carries_its_inputs_for_audit(self):
        series = _series({date(2026, 6, 30): _row(revenue=1000.0, net=250.0)})
        result = net_margin(series.latest)
        self.assertEqual(result.value, 0.25)
        self.assertEqual(result.inputs, {"numerator": 250.0, "denominator": 1000.0})



class IndianAPISourceTests(unittest.TestCase):
    """The adapter is normalisation only; a key is needed to judge the feed."""

    def test_quarter_label_becomes_that_month_end(self):
        from app.analysis.sources import parse_quarter_label

        self.assertEqual(parse_quarter_label("Jun 2024"), date(2024, 6, 30))
        self.assertEqual(parse_quarter_label("Dec 2023"), date(2023, 12, 31))
        self.assertEqual(parse_quarter_label("Feb 2024"), date(2024, 2, 29))
        for junk in ("", "Q1 2024", "Smarch 2024", "Jun", "Jun twenty"):
            self.assertIsNone(parse_quarter_label(junk), junk)

    def test_transposed_screener_shape_normalises_to_our_fields(self):
        from app.analysis.sources import IndianAPIFundamentalsSource

        payload = {
            "Sales": {"Jun 2024": 62613, "Sep 2024": 70000},
            "Net Profit": {"Jun 2024": 12105, "Sep 2024": 13000},
            "EPS in Rs": {"Jun 2024": 33.28, "Sep 2024": 35.0},
            "Operating Profit": {"Jun 2024": 9000, "Sep 2024": 9500},
        }
        source = IndianAPIFundamentalsSource(api_key="test")
        source.fetch_raw = lambda symbol: payload  # type: ignore[method-assign]

        series = load_series("TATAMOTORS.NS", source)
        first = series.quarter_ending(date(2024, 6, 30))
        self.assertEqual(first.values["revenue"], 62613.0)
        self.assertEqual(first.values["net_income"], 12105.0)
        self.assertEqual(first.values["basic_eps"], 33.28)
        self.assertEqual(first.values["operating_income"], 9000.0)
        self.assertFalse(series.is_point_in_time)

    def test_missing_key_is_reported_as_status_not_a_crash(self):
        from app.analysis.sources import IndianAPIFundamentalsSource

        source = IndianAPIFundamentalsSource(api_key=None)
        source.api_key = None
        series = load_series("RELIANCE.NS", source)
        self.assertEqual(series.status, STATUS_SOURCE_ERROR)
        self.assertIn("INDIAN_API_KEY", series.notes[0])

if __name__ == "__main__":
    unittest.main()
