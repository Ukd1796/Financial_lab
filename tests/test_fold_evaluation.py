"""The fold decision engine — charter v3 §7 applied literally.

This is the code that turns numbers into a verdict, so it is tested against the
charter's conditions one at a time, with the others held passing.  A bug here
does not produce a wrong number; it produces a wrong *conclusion*, which is
worse and harder to notice.

The book-construction tests also pin the point-in-time rule from v3 §A2: the
response median comes from the PRIOR completed quarter, never the current one.
"""

import unittest
from datetime import date

from app.event_research import features as F
from scripts.event_research.run_fold import (
    build_book,
    evaluate,
    response_median_reference,
    verdict,
)

Q1, Q2, Q3, Q4, Q5 = (
    date(2024, 3, 31),
    date(2024, 6, 30),
    date(2024, 9, 30),
    date(2024, 12, 31),
    date(2025, 3, 31),
)


def _event(period, surprise, response, forward, isin="INE000A01001", method="CROSS_SECTIONAL"):
    return {
        "event_id": f"{isin}-{period}-{surprise}",
        "isin": isin,
        "symbol": "TEST",
        "period_end": period,
        "surprise": surprise,
        "method": method,
        "response": response,
        "forward": forward,
    }


def _quarter(period, count, forward, *, surprise=1.0, response_centre=0.0):
    """A quarter of `count` distinct issuers with a *dispersed* initial response.

    The dispersion matters: the bucket filter is a strict `response < median`,
    so a fixture where every response is identical produces an empty book and
    silently tests nothing.  Spreading them symmetrically about the centre puts
    roughly half the quarter below the prior quarter's median, which is what
    real data does.
    """
    return [
        _event(
            period,
            surprise + i * 0.01,
            response_centre + (i - count / 2) * 0.001,
            forward,
            isin=f"INE{i:06d}A01",
        )
        for i in range(count)
    ]


class ResponseMedianReferenceTests(unittest.TestCase):
    def test_first_quarter_has_no_reference(self):
        events = _quarter(Q1, 20, 0.02)
        reference = response_median_reference(events, [Q1])
        self.assertIsNone(reference[Q1])

    def test_reference_comes_from_the_prior_quarter_not_the_current_one(self):
        """The point-in-time rule: a quarter is judged by its predecessor."""
        events = _quarter(Q1, 20, 0.02, response_centre=-0.10) + _quarter(
            Q2, 20, 0.02, response_centre=0.50
        )
        reference = response_median_reference(events, [Q1, Q2])
        # Q1's centre, not Q2's -- the two are far apart so the source is unambiguous.
        self.assertAlmostEqual(reference[Q2], -0.10, delta=0.01)

    def test_only_positive_surprises_define_the_median(self):
        events = [
            _event(Q1, 1.0, 0.20, 0.0, isin="INE000001A01"),
            _event(Q1, 1.0, 0.30, 0.0, isin="INE000002A01"),
            _event(Q1, -5.0, -9.99, 0.0, isin="INE000003A01"),
        ] + _quarter(Q2, 5, 0.0)
        reference = response_median_reference(events, [Q1, Q2])
        self.assertAlmostEqual(reference[Q2], 0.25)


class BookConstructionTests(unittest.TestCase):
    def test_no_reference_means_no_book(self):
        self.assertEqual(build_book(_quarter(Q1, 30, 0.02), None), [])

    def test_book_is_capped_at_the_frozen_size(self):
        events = _quarter(Q1, 200, 0.02)
        self.assertEqual(len(build_book(events, median_response=0.0)), F.BOOK_SIZE)

    def test_book_takes_the_largest_surprises(self):
        events = _quarter(Q1, 60, 0.02)
        book = build_book(events, median_response=0.0)
        surprises = [e["surprise"] for e in book]
        self.assertEqual(surprises, sorted(surprises, reverse=True))
        # Half the quarter sits below the median, which is under the cap here,
        # so the book is what qualified rather than what the cap allows.
        self.assertEqual(len(book), 30)

    def test_negative_surprises_are_excluded(self):
        events = [_event(Q1, -1.0, -0.05, 0.02, isin=f"INE{i:06d}A01") for i in range(30)]
        self.assertEqual(build_book(events, median_response=0.0), [])

    def test_responses_at_or_above_the_median_are_excluded(self):
        events = [_event(Q1, 1.0, 0.05, 0.02, isin=f"INE{i:06d}A01") for i in range(30)]
        self.assertEqual(build_book(events, median_response=0.0), [])

    def test_events_without_a_forward_return_are_excluded(self):
        events = [_event(Q1, 1.0, -0.05, None, isin=f"INE{i:06d}A01") for i in range(30)]
        self.assertEqual(build_book(events, median_response=0.0), [])


class SufficiencyTests(unittest.TestCase):
    def test_thin_quarters_are_dropped_not_counted(self):
        events = _quarter(Q1, 20, 0.02) + _quarter(Q2, F.MIN_EVENTS_PER_QUARTER - 1, 0.02)
        result = evaluate(events, collapsed=set())
        by_period = {q["period"]: q for q in result["quarters"]}
        self.assertFalse(by_period[Q2]["usable"])

    def test_too_few_quarters_is_inconclusive_not_fail(self):
        """A thin sample is a reason to disbelieve, not a verdict on the sign."""
        events = _quarter(Q1, 60, 0.50) + _quarter(Q2, 60, 0.50)
        outcome, notes = verdict(evaluate(events, collapsed=set()))
        self.assertEqual(outcome, "INCONCLUSIVE")
        self.assertIn("usable quarters", notes[0])

    def test_inconclusive_is_returned_even_when_returns_are_huge(self):
        events = _quarter(Q1, 60, 5.0) + _quarter(Q2, 60, 5.0)
        self.assertEqual(verdict(evaluate(events, collapsed=set()))[0], "INCONCLUSIVE")


class DecisionTableTests(unittest.TestCase):
    """One condition at a time, with the others held passing."""

    def _five_quarters(self, forward):
        events = []
        for index, period in enumerate([Q1, Q2, Q3, Q4, Q5]):
            value = forward[index] if isinstance(forward, list) else forward
            events += _quarter(period, 100, value)
        return events

    def test_return_above_the_bar_passes(self):
        # Gross must clear the bar plus the round-trip cost.
        gross = F.PASS_BAR + F.ROUND_TRIP_COST + 0.01
        outcome, _ = verdict(evaluate(self._five_quarters(gross), collapsed=set()))
        self.assertEqual(outcome, "PASS")

    def test_return_below_the_bar_fails_condition_1(self):
        gross = F.ROUND_TRIP_COST + 0.001  # net is positive but under the bar
        outcome, failures = verdict(evaluate(self._five_quarters(gross), collapsed=set()))
        self.assertEqual(outcome, "FAIL")
        self.assertTrue(any("cond.1" in f for f in failures))

    def test_negative_net_fails_both_sign_and_bar(self):
        outcome, failures = verdict(evaluate(self._five_quarters(0.0), collapsed=set()))
        self.assertEqual(outcome, "FAIL")
        self.assertTrue(any("cond.2" in f for f in failures))

    def test_one_dominant_quarter_fails_condition_3(self):
        """A result carried by a single quarter is not a demonstrated edge."""
        gross = F.ROUND_TRIP_COST
        forward = [gross, gross, gross, gross, gross + 0.40]
        outcome, failures = verdict(evaluate(self._five_quarters(forward), collapsed=set()))
        self.assertEqual(outcome, "FAIL")
        self.assertTrue(any("cond.3" in f for f in failures))

    def test_edge_carried_only_by_collapsed_names_fails_condition_5(self):
        """A sleeve that only works when failures are excluded has not been shown."""
        collapsed_isin = "INE000000A01"
        events = []
        for period in [Q1, Q2, Q3, Q4, Q5]:
            # One collapsed name carries a large gain; the rest lose.
            events.append(_event(period, 99.0, -0.50, 2.0, isin=collapsed_isin))
            # Dispersed responses, so roughly half clear the prior quarter's
            # median and the book is non-empty.
            events += [
                _event(period, 1.0 + i * 0.01, (i - 20) * 0.001, -0.02, isin=f"INE{i:06d}A01")
                for i in range(40)
            ]
        result = evaluate(events, collapsed={collapsed_isin[:9]})
        self.assertGreater(result["aggregate_net"], 0)
        self.assertLess(result["aggregate_net_ex_collapsed"], 0)
        outcome, failures = verdict(result)
        self.assertEqual(outcome, "FAIL")
        self.assertTrue(any("cond.5" in f for f in failures))

    def test_t_statistic_uses_the_frozen_standard_error(self):
        """Judged against the SE frozen in v3 §6, not one recomputed from the
        result -- otherwise a lucky sample would shrink its own error bar."""
        gross = F.PASS_BAR + F.ROUND_TRIP_COST
        result = evaluate(self._five_quarters(gross), collapsed=set())
        expected_se = 0.0142 / result["usable_quarters"] ** 0.5
        self.assertAlmostEqual(result["standard_error"], expected_se)


if __name__ == "__main__":
    unittest.main()
