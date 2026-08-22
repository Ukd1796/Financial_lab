"""Tests for the Phase-1 XBRL fact parser.

The parser's job is to refuse to guess.  Two distinct ways an instance can be
unprovable are covered here:

* **Undefined contexts** -- facts reference base contexts (``OneD``/``FourD``)
  the document never defines.  Uniform across NSE's 2019-2022 era.
* **Colliding contexts** -- the document defines ``OneD`` (the discrete quarter)
  and ``FourD`` (the cumulative year-to-date figure) with *identical dates* and
  different values.  Measured 2026-08-13 in 190 of 226 usable filings.  Matching
  on period alone leaves the choice to document order, which would silently
  store a ~3x inflated "quarterly" EPS for any filer emitting ``FourD`` first.

Note: NSE instances do **not** carry the year-ago quarter -- 226 of 226 usable
filings define no prior-year context (``docs/research_log.md`` 2026-08-13), so
a seasonal surprise must chain two separate filings.
"""

import unittest
from datetime import date

from app.event_research.xbrl_parser import (
    VALIDATION_AMBIGUOUS_PERIOD,
    VALIDATION_UNPARSEABLE,
    VALIDATION_UNRESOLVED_CONTEXT,
    VALIDATION_VALID,
    parse_result_xbrl,
    to_fact_payload,
)


def _instance(contexts: str, facts: str) -> bytes:
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<xbrli:xbrl xmlns:xbrli="http://www.xbrl.org/2003/instance"
            xmlns:xbrldi="http://xbrl.org/2006/xbrldi"
            xmlns:in-bse-fin="http://www.bseindia.com/xbrl/fin/2020-03-31/in-bse-fin">
{contexts}
{facts}
</xbrli:xbrl>""".encode()


def _duration(context_id: str, start: str, end: str, member: str | None = None) -> str:
    dimension = (
        f'<xbrli:entity><xbrli:identifier scheme="http://www.nse">X</xbrli:identifier>'
        f'<xbrli:segment><xbrldi:explicitMember dimension="in-bse-fin:SegmentAxis">'
        f'in-bse-fin:{member}</xbrldi:explicitMember></xbrli:segment></xbrli:entity>'
        if member else ""
    )
    return (
        f'<xbrli:context id="{context_id}">{dimension}'
        f'<xbrli:period><xbrli:startDate>{start}</xbrli:startDate>'
        f'<xbrli:endDate>{end}</xbrli:endDate></xbrli:period></xbrli:context>'
    )


QUARTER = _duration("QuarterD", "2023-10-01", "2023-12-31")
YEAR_AGO = _duration("YearAgoD", "2022-10-01", "2022-12-31")


class XBRLParserTests(unittest.TestCase):
    def test_reported_quarter_is_selected_over_year_ago_quarter(self):
        facts = (
            '<in-bse-fin:BasicEarningsLossPerShareFromContinuingAndDiscontinuedOperations '
            'contextRef="QuarterD">6.80</in-bse-fin:BasicEarningsLossPerShareFromContinuingAndDiscontinuedOperations>'
            '<in-bse-fin:BasicEarningsLossPerShareFromContinuingAndDiscontinuedOperations '
            'contextRef="YearAgoD">13.06</in-bse-fin:BasicEarningsLossPerShareFromContinuingAndDiscontinuedOperations>'
        )
        result = parse_result_xbrl(
            _instance(QUARTER + YEAR_AGO, facts),
            expected_period_start=date(2023, 10, 1),
            expected_period_end=date(2023, 12, 31),
        )
        self.assertEqual(result.validation_status, VALIDATION_VALID)
        self.assertEqual(result.facts["basic_eps"], 6.80)
        self.assertEqual(result.period_end, date(2023, 12, 31))

    def test_undefined_context_withholds_facts_instead_of_guessing(self):
        # Reproduces the defect observed in NSE's 2019-2022 instances, where
        # headline facts reference base contexts the document never defines.
        facts = (
            '<in-bse-fin:BasicEarningsLossPerShareFromContinuingAndDiscontinuedOperations '
            'contextRef="OneD">6.80</in-bse-fin:BasicEarningsLossPerShareFromContinuingAndDiscontinuedOperations>'
        )
        result = parse_result_xbrl(
            _instance(QUARTER, facts),
            expected_period_start=date(2023, 10, 1),
            expected_period_end=date(2023, 12, 31),
        )
        self.assertEqual(result.validation_status, VALIDATION_UNRESOLVED_CONTEXT)
        self.assertIn("OneD", result.unresolved_context_refs)
        self.assertIsNone(result.facts["basic_eps"])

    def test_segment_breakdown_is_not_mistaken_for_the_headline_figure(self):
        segment = _duration("SegmentD", "2023-10-01", "2023-12-31", member="OneSegmentMember")
        facts = (
            '<in-bse-fin:RevenueFromOperations contextRef="SegmentD">111.0</in-bse-fin:RevenueFromOperations>'
            '<in-bse-fin:RevenueFromOperations contextRef="QuarterD">999.0</in-bse-fin:RevenueFromOperations>'
        )
        result = parse_result_xbrl(
            _instance(QUARTER + segment, facts),
            expected_period_start=date(2023, 10, 1),
            expected_period_end=date(2023, 12, 31),
        )
        self.assertEqual(result.facts["revenue"], 999.0)

    def test_cumulative_context_is_not_mistaken_for_the_quarter(self):
        # The real NSE shape: OneD and FourD declare the SAME dates, but OneD
        # holds the quarter (12.93) and FourD the year-to-date figure (54.70).
        one = _duration("OneD", "2023-01-01", "2023-03-31")
        four = _duration("FourD", "2023-01-01", "2023-03-31")
        facts = (
            '<in-bse-fin:BasicEarningsLossPerShareFromContinuingOperations '
            'contextRef="OneD">12.93</in-bse-fin:BasicEarningsLossPerShareFromContinuingOperations>'
            '<in-bse-fin:BasicEarningsLossPerShareFromContinuingOperations '
            'contextRef="FourD">54.70</in-bse-fin:BasicEarningsLossPerShareFromContinuingOperations>'
        )
        result = parse_result_xbrl(
            _instance(one + four, facts),
            expected_period_start=date(2023, 1, 1),
            expected_period_end=date(2023, 3, 31),
        )
        self.assertEqual(result.validation_status, VALIDATION_VALID)
        self.assertEqual(result.facts["basic_eps"], 12.93)

    def test_selection_does_not_depend_on_document_order(self):
        # Identical to the case above with FourD defined FIRST.  Before the
        # naming rule this stored 54.70 -- a fabricated quarterly EPS, not a
        # noisy one.
        one = _duration("OneD", "2023-01-01", "2023-03-31")
        four = _duration("FourD", "2023-01-01", "2023-03-31")
        facts = (
            '<in-bse-fin:BasicEarningsLossPerShareFromContinuingOperations '
            'contextRef="OneD">12.93</in-bse-fin:BasicEarningsLossPerShareFromContinuingOperations>'
            '<in-bse-fin:BasicEarningsLossPerShareFromContinuingOperations '
            'contextRef="FourD">54.70</in-bse-fin:BasicEarningsLossPerShareFromContinuingOperations>'
        )
        result = parse_result_xbrl(
            _instance(four + one, facts),
            expected_period_start=date(2023, 1, 1),
            expected_period_end=date(2023, 3, 31),
        )
        self.assertEqual(result.facts["basic_eps"], 12.93)

    def test_unresolvable_collision_withholds_rather_than_picking(self):
        # Two same-dated contexts, differing values, neither matching a known
        # convention: the discrete period cannot be proved, so nothing is stored.
        a = _duration("PeriodAD", "2023-01-01", "2023-03-31")
        b = _duration("PeriodBD", "2023-01-01", "2023-03-31")
        facts = (
            '<in-bse-fin:BasicEarningsLossPerShareFromContinuingOperations '
            'contextRef="PeriodAD">12.93</in-bse-fin:BasicEarningsLossPerShareFromContinuingOperations>'
            '<in-bse-fin:BasicEarningsLossPerShareFromContinuingOperations '
            'contextRef="PeriodBD">54.70</in-bse-fin:BasicEarningsLossPerShareFromContinuingOperations>'
        )
        result = parse_result_xbrl(
            _instance(a + b, facts),
            expected_period_start=date(2023, 1, 1),
            expected_period_end=date(2023, 3, 31),
        )
        self.assertEqual(result.validation_status, VALIDATION_AMBIGUOUS_PERIOD)
        self.assertIsNone(result.facts["basic_eps"])

    def test_colliding_contexts_agreeing_on_values_are_not_an_error(self):
        # A collision only matters when it changes the answer.
        a = _duration("PeriodAD", "2023-01-01", "2023-03-31")
        b = _duration("PeriodBD", "2023-01-01", "2023-03-31")
        facts = (
            '<in-bse-fin:BasicEarningsLossPerShareFromContinuingOperations '
            'contextRef="PeriodAD">12.93</in-bse-fin:BasicEarningsLossPerShareFromContinuingOperations>'
            '<in-bse-fin:BasicEarningsLossPerShareFromContinuingOperations '
            'contextRef="PeriodBD">12.93</in-bse-fin:BasicEarningsLossPerShareFromContinuingOperations>'
        )
        result = parse_result_xbrl(
            _instance(a + b, facts),
            expected_period_start=date(2023, 1, 1),
            expected_period_end=date(2023, 3, 31),
        )
        self.assertEqual(result.validation_status, VALIDATION_VALID)
        self.assertEqual(result.facts["basic_eps"], 12.93)

    def test_unparseable_document_is_reported_not_raised(self):
        result = parse_result_xbrl(b"<not-xml")
        self.assertEqual(result.validation_status, VALIDATION_UNPARSEABLE)
        self.assertIsNone(result.facts["basic_eps"])

    def test_fact_payload_carries_parse_status_to_the_repository(self):
        result = parse_result_xbrl(_instance(QUARTER, ""),
                                   expected_period_start=date(2023, 10, 1),
                                   expected_period_end=date(2023, 12, 31))
        payload = to_fact_payload(
            result, reporting_scope="consolidated", is_cumulative=False, audit_status="UNAUDITED"
        )
        self.assertEqual(payload["validation_status"], result.validation_status)
        self.assertEqual(payload["reporting_scope"], "consolidated")
        self.assertFalse(payload["is_cumulative"])


if __name__ == "__main__":
    unittest.main()
