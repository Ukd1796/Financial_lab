"""The frozen feature rules from charter v3.

These are the rules a result will be reported against, so they are tested
against the charter's wording rather than against the implementation's
convenience.  The clock tests cover charter §6's release gate: "100% of sampled
events have a timezone-aware timestamp and entry later than signal_ready_at".
"""

import unittest
from datetime import date, datetime, timedelta

from app.event_research.features import (
    HOLDING_SESSIONS,
    IST,
    METHOD_CROSS_SECTIONAL,
    METHOD_TIME_SERIES,
    MIN_TIME_SERIES_HISTORY,
    equal_weight_mean,
    fold_for,
    participation_ok,
    peer_basket,
    resolve_clock,
    seasonal_difference,
    select_standardisation,
    simple_return,
    standardise_cross_sectional,
    standardise_time_series,
)


def _sessions(start: date, count: int) -> list[date]:
    """A contiguous run of trading days, weekends included.

    Deliberately not weekday-filtered: NSE holds Budget, Muhurat and
    disaster-recovery sessions on weekends, and the calendar comes from the
    exchange's recorded status, never from the day of the week.
    """
    return [start + timedelta(days=offset) for offset in range(count)]


class CausalClockTests(unittest.TestCase):
    def setUp(self):
        self.sessions = _sessions(date(2024, 1, 1), 60)

    def test_filing_after_the_close_reacts_the_next_session(self):
        clock = resolve_clock(datetime(2024, 1, 10, 18, 0, tzinfo=IST), self.sessions)
        self.assertEqual(clock.reaction_session, date(2024, 1, 11))
        self.assertEqual(clock.prior_session, date(2024, 1, 10))
        self.assertEqual(clock.entry_session, date(2024, 1, 12))

    def test_filing_mid_session_does_not_claim_that_session(self):
        """A filing released at 11:00 cannot be credited with a move that was
        already half-complete when it landed."""
        clock = resolve_clock(datetime(2024, 1, 10, 11, 0, tzinfo=IST), self.sessions)
        self.assertEqual(clock.reaction_session, date(2024, 1, 11))

    def test_filing_before_the_open_reacts_the_same_session(self):
        clock = resolve_clock(datetime(2024, 1, 10, 8, 0, tzinfo=IST), self.sessions)
        self.assertEqual(clock.reaction_session, date(2024, 1, 10))
        self.assertEqual(clock.prior_session, date(2024, 1, 9))

    def test_entry_is_always_after_the_reaction_close(self):
        """Charter §6's gate, asserted across every hour of the day."""
        for hour in range(24):
            with self.subTest(hour=hour):
                clock = resolve_clock(
                    datetime(2024, 1, 10, hour, 0, tzinfo=IST), self.sessions
                )
                self.assertGreater(clock.entry_session, clock.reaction_session)
                self.assertLess(clock.prior_session, clock.reaction_session)

    def test_exit_is_the_holding_horizon_after_entry(self):
        clock = resolve_clock(datetime(2024, 1, 10, 18, 0, tzinfo=IST), self.sessions)
        entry_index = self.sessions.index(clock.entry_session)
        self.assertEqual(
            clock.exit_session, self.sessions[entry_index + HOLDING_SESSIONS]
        )

    def test_naive_timestamp_is_rejected(self):
        with self.assertRaises(ValueError):
            resolve_clock(datetime(2024, 1, 10, 18, 0), self.sessions)

    def test_calendar_running_out_yields_no_clock(self):
        """An event too close to the end of the panel has no measurable outcome;
        it must be reported as unmeasurable, never silently truncated."""
        self.assertIsNone(
            resolve_clock(datetime(2024, 2, 20, 18, 0, tzinfo=IST), self.sessions)
        )

    def test_event_before_the_panel_yields_no_clock(self):
        self.assertIsNone(
            resolve_clock(datetime(2023, 6, 1, 18, 0, tzinfo=IST), self.sessions)
        )

    def test_utc_timestamp_is_converted_not_assumed(self):
        """23:00 UTC on the 10th is 04:30 IST on the 11th, before that session
        opens -- so it reacts on the 11th, not the 12th."""
        clock = resolve_clock(
            datetime(2024, 1, 10, 23, 0, tzinfo=__import__("zoneinfo").ZoneInfo("UTC")),
            self.sessions,
        )
        self.assertEqual(clock.reaction_session, date(2024, 1, 11))


class SurpriseStandardisationTests(unittest.TestCase):
    def test_seasonal_difference_is_year_on_year(self):
        self.assertAlmostEqual(seasonal_difference(12.5, 10.0), 2.5)

    def test_time_series_needs_the_minimum_history(self):
        short = [1.0] * (MIN_TIME_SERIES_HISTORY - 1)
        self.assertIsNone(standardise_time_series(2.0, short))

    def test_time_series_standardises_against_own_history(self):
        prior = [1.0, 2.0, 3.0, 4.0]
        value = standardise_time_series(5.0, prior)
        self.assertIsNotNone(value)
        self.assertGreater(value, 0)

    def test_zero_dispersion_is_not_an_infinite_surprise(self):
        self.assertIsNone(standardise_time_series(5.0, [2.0, 2.0, 2.0, 2.0]))

    def test_cross_sectional_centres_on_the_quarter(self):
        quarter = [0.01, 0.02, 0.03, 0.04]
        self.assertAlmostEqual(standardise_cross_sectional(0.025, quarter), 0.0)
        self.assertGreater(standardise_cross_sectional(0.04, quarter), 0)

    def test_hybrid_prefers_time_series_when_available(self):
        value, method = select_standardisation(1.5, -0.3)
        self.assertEqual((value, method), (1.5, METHOD_TIME_SERIES))

    def test_hybrid_falls_back_to_cross_sectional(self):
        value, method = select_standardisation(None, -0.3)
        self.assertEqual((value, method), (-0.3, METHOD_CROSS_SECTIONAL))

    def test_hybrid_reports_nothing_when_neither_is_computable(self):
        self.assertEqual(select_standardisation(None, None), (None, None))


class PeerBasketTests(unittest.TestCase):
    def setUp(self):
        # Two orders of magnitude, as the real cohort spans.
        self.candidates = {f"INE{i:06d}": float(10**6 * (1.4**i)) for i in range(40)}
        self.target = "INE000020"

    def test_target_is_never_its_own_peer(self):
        peers = peer_basket(self.target, self.candidates)
        self.assertNotIn(self.target, peers)

    def test_basket_is_the_frozen_size(self):
        self.assertEqual(len(peer_basket(self.target, self.candidates)), 20)

    def test_peers_are_nearest_in_log_traded_value(self):
        peers = set(peer_basket(self.target, self.candidates, size=4))
        self.assertEqual(peers, {"INE000018", "INE000019", "INE000021", "INE000022"})

    def test_small_cohort_returns_what_exists(self):
        small = {"INE000001": 1e8, "INE000002": 2e8}
        self.assertEqual(peer_basket("INE000001", small), ["INE000002"])

    def test_unknown_or_zero_target_has_no_basket(self):
        self.assertEqual(peer_basket("INE999999", self.candidates), [])
        self.assertEqual(peer_basket("INE000001", {"INE000001": 0.0}), [])

    def test_prefix_keying_matches_across_an_isin_change(self):
        """The cohort may hold either side of a face-value change."""
        candidates = {"INE239A01": 5e9, "INE040A01": 5.1e9, "INE002A01": 5.2e9}
        self.assertIn("INE040A01", peer_basket("INE239A01024", candidates, size=2))


class AdmissibilityTests(unittest.TestCase):
    def test_liquid_name_clears_the_participation_cap(self):
        self.assertIs(participation_ok(7e8), True)

    def test_illiquid_name_fails_the_cap(self):
        self.assertIs(participation_ok(1e6), False)

    def test_unmeasurable_traded_value_is_not_a_failure(self):
        self.assertIsNone(participation_ok(None))
        self.assertIsNone(participation_ok(0.0))

    def test_simple_return_rejects_unusable_prices(self):
        self.assertIsNone(simple_return(None, 100.0))
        self.assertIsNone(simple_return(0.0, 100.0))
        self.assertAlmostEqual(simple_return(100.0, 110.0), 0.10)

    def test_equal_weight_mean_ignores_missing_peers(self):
        self.assertAlmostEqual(equal_weight_mean([0.1, None, 0.3]), 0.2)
        self.assertIsNone(equal_weight_mean([None, None]))


class FoldAssignmentTests(unittest.TestCase):
    def test_fold_windows_match_the_charter(self):
        self.assertEqual(fold_for(date(2023, 7, 1)), "A")
        self.assertEqual(fold_for(date(2024, 12, 31)), "A")
        self.assertEqual(fold_for(date(2025, 1, 1)), "B")
        self.assertEqual(fold_for(date(2025, 12, 31)), "B")
        self.assertEqual(fold_for(date(2026, 1, 1)), "C")

    def test_pre_study_era_belongs_to_no_fold(self):
        self.assertIsNone(fold_for(date(2023, 6, 30)))


if __name__ == "__main__":
    unittest.main()
