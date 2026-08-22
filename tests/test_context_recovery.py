"""Recovering an undefined OneD/FourD pair from the document's own values.

Pre-2023 filings reference `OneD` and `FourD` and never define them.  Guessing
inverts the seasonal surprise, so the parser refused to guess.  It no longer has
to: the Indian fiscal year runs Apr-Mar, so year-to-date at fiscal quarter N
spans N quarters, and FourD/OneD on a large additive flow discriminates
cumulative from discrete.  Measured over 439 real filings: median 1.92 at Q2,
2.89 at Q3, 3.87 at Q4.

The recovery is opt-in and lands its own status, so a result can always be
re-run without these filings.
"""

import unittest
from datetime import date

from app.event_research.xbrl_parser import (
    VALIDATION_RECOVERED_CONVENTION,
    VALIDATION_UNRESOLVED_CONTEXT,
    parse_result_xbrl,
)


def _instance(one_income, four_income, one_eps, *, extra=""):
    """An instance referencing OneD/FourD without ever defining them."""
    return f"""<?xml version="1.0"?>
<xbrl xmlns="http://www.xbrl.org/2003/instance">
  <Income contextRef="OneD">{one_income}</Income>
  <Income contextRef="FourD">{four_income}</Income>
  <Expenses contextRef="OneD">{one_income * 0.7:.2f}</Expenses>
  <Expenses contextRef="FourD">{four_income * 0.7:.2f}</Expenses>
  <BasicEarningsLossPerShareFromContinuingOperations contextRef="OneD">{one_eps}</BasicEarningsLossPerShareFromContinuingOperations>
  <BasicEarningsLossPerShareFromContinuingOperations contextRef="FourD">{one_eps * 3:.2f}</BasicEarningsLossPerShareFromContinuingOperations>
  {extra}
</xbrl>""".encode()


class ConventionRecoveryTests(unittest.TestCase):
    def test_default_is_still_to_refuse(self):
        """Strict reading stays the default; recovery must be asked for."""
        result = parse_result_xbrl(
            _instance(1e9, 3e9, 12.5), expected_period_end=date(2022, 12, 31)
        )
        self.assertEqual(result.validation_status, VALIDATION_UNRESOLVED_CONTEXT)
        self.assertIsNone(result.facts["basic_eps"])

    def test_q3_ratio_of_three_recovers_the_quarter(self):
        result = parse_result_xbrl(
            _instance(1e9, 3e9, 12.5),
            expected_period_end=date(2022, 12, 31),
            resolve_conventions=True,
        )
        self.assertEqual(result.validation_status, VALIDATION_RECOVERED_CONVENTION)
        self.assertAlmostEqual(result.facts["basic_eps"], 12.5)
        self.assertTrue(any("OneD" in n for n in result.notes))

    def test_q4_ratio_of_four_recovers_the_quarter(self):
        result = parse_result_xbrl(
            _instance(1e9, 4e9, 9.0),
            expected_period_end=date(2023, 3, 31),
            resolve_conventions=True,
        )
        self.assertEqual(result.validation_status, VALIDATION_RECOVERED_CONVENTION)
        self.assertAlmostEqual(result.facts["basic_eps"], 9.0)

    def test_unequal_quarters_still_resolve(self):
        """The test discriminates, it does not measure: Q3 expecting 3 but
        observing 2.5 is still unambiguously cumulative."""
        result = parse_result_xbrl(
            _instance(1e9, 2.5e9, 5.0),
            expected_period_end=date(2022, 12, 31),
            resolve_conventions=True,
        )
        self.assertEqual(result.validation_status, VALIDATION_RECOVERED_CONVENTION)

    def test_ratio_near_one_is_refused(self):
        """If FourD does not span more than a quarter, nothing is proved."""
        result = parse_result_xbrl(
            _instance(1e9, 1.05e9, 5.0),
            expected_period_end=date(2022, 12, 31),
            resolve_conventions=True,
        )
        self.assertEqual(result.validation_status, VALIDATION_UNRESOLVED_CONTEXT)
        self.assertIsNone(result.facts["basic_eps"])

    def test_no_comparable_pair_is_refused(self):
        instance = b"""<?xml version="1.0"?>
<xbrl xmlns="http://www.xbrl.org/2003/instance">
  <BasicEarningsLossPerShareFromContinuingOperations contextRef="OneD">12.5</BasicEarningsLossPerShareFromContinuingOperations>
</xbrl>"""
        result = parse_result_xbrl(
            instance, expected_period_end=date(2022, 12, 31), resolve_conventions=True
        )
        self.assertEqual(result.validation_status, VALIDATION_UNRESOLVED_CONTEXT)

    def test_q1_is_value_neutral_and_allowed(self):
        """At Q1 year-to-date IS the quarter, so the ratio cannot discriminate --
        but neither assignment changes any value."""
        result = parse_result_xbrl(
            _instance(1e9, 1e9, 4.0),
            expected_period_end=date(2023, 6, 30),
            resolve_conventions=True,
        )
        self.assertEqual(result.validation_status, VALIDATION_RECOVERED_CONVENTION)
        self.assertAlmostEqual(result.facts["basic_eps"], 4.0)

    def test_non_standard_period_end_is_refused(self):
        result = parse_result_xbrl(
            _instance(1e9, 3e9, 12.5),
            expected_period_end=date(2022, 11, 30),
            resolve_conventions=True,
        )
        self.assertEqual(result.validation_status, VALIDATION_UNRESOLVED_CONTEXT)

    def test_recovered_status_is_not_valid(self):
        """A recovered filing must remain separable from a fully proved one, so
        any result can be re-run without them."""
        from app.event_research.xbrl_parser import VALIDATION_VALID

        self.assertNotEqual(VALIDATION_RECOVERED_CONVENTION, VALIDATION_VALID)


if __name__ == "__main__":
    unittest.main()
