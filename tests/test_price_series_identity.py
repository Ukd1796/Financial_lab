"""Price series must be keyed on issuer, not on a single ISIN.

A face-value split mints a **new ISIN**, and the old one stops trading the day
before.  `adjustment_factors` already keys on the issuer prefix, but
`adjusted_close_series` keyed the price lookup on the full ISIN, so for any
issuer that split inside the study window the series silently truncated at the
change -- a 20-session window spanning it returned a partial series or nothing
at all, with no error.

44 of the 597 rolled-cohort issuers carry more than one ISIN in the panel, and
because only long-lived companies have had face-value changes, the loss is
size- and age-correlated.

The fixture is NESTLEIND's real 2024-01-05 split (10:1, ratio 0.10, validated
AGREE against the observed price move), which is the case the research log
records.
"""

import sqlite3
import unittest

from app.analysis.corporate_actions import (
    adjusted_close_series,
    adjusted_close_series_by_issuer,
    ensure_schema,
)

OLD_ISIN = "INE239A01016"  # retired by the split
NEW_ISIN = "INE239A01024"  # issued on the split
SPLIT_EX_DATE = "2024-01-05"
SPLIT_RATIO = 0.10

# Pre-split around Rs 26,000, post-split around Rs 2,600 -- the same economic
# price on a ten-times-larger share count.
PRE_SPLIT = [("2024-01-02", 26000.0), ("2024-01-03", 26100.0), ("2024-01-04", 26200.0)]
POST_SPLIT = [("2024-01-05", 2620.0), ("2024-01-08", 2640.0), ("2024-01-09", 2650.0)]


class IssuerKeyedPriceSeriesTests(unittest.TestCase):
    def setUp(self):
        self.conn = sqlite3.connect(":memory:")
        self.conn.row_factory = sqlite3.Row
        self.conn.executescript(
            """
            CREATE TABLE daily_prices (
                exchange TEXT NOT NULL, session TEXT NOT NULL, isin TEXT NOT NULL,
                symbol TEXT NOT NULL, series TEXT, open REAL, high REAL, low REAL,
                close REAL, prev_close REAL, volume REAL, turnover REAL,
                PRIMARY KEY (exchange, session, isin)
            );
            """
        )
        ensure_schema(self.conn)
        for isin, rows in ((OLD_ISIN, PRE_SPLIT), (NEW_ISIN, POST_SPLIT)):
            self.conn.executemany(
                "INSERT INTO daily_prices "
                "(exchange, session, isin, symbol, series, close, turnover) "
                "VALUES ('NSE', ?, ?, 'NESTLEIND', 'EQ', ?, 1e9)",
                [(session, isin, close) for session, close in rows],
            )
        # The announcement feed keeps quoting the retired code, which is why the
        # action is stored under OLD_ISIN and must still be found from either.
        self.conn.execute(
            "INSERT INTO corporate_actions "
            "(isin, ex_date, subject, kind, announced_ratio, symbol, validation) "
            "VALUES (?, ?, 'Face Value Split From Rs 10 To Re 1', 'SPLIT', ?, "
            "'NESTLEIND', 'AGREE')",
            (OLD_ISIN, SPLIT_EX_DATE, SPLIT_RATIO),
        )
        self.conn.commit()

    def tearDown(self):
        self.conn.close()

    def test_full_isin_lookup_truncates_at_the_split(self):
        """The defect, pinned so a regression is visible rather than silent."""
        old_leg = adjusted_close_series(self.conn, OLD_ISIN, "2024-01-02", "2024-01-09")
        new_leg = adjusted_close_series(self.conn, NEW_ISIN, "2024-01-02", "2024-01-09")
        self.assertEqual(len(old_leg), len(PRE_SPLIT))
        self.assertEqual(len(new_leg), len(POST_SPLIT))

    def test_issuer_lookup_spans_the_isin_change(self):
        series = adjusted_close_series_by_issuer(
            self.conn, OLD_ISIN, "2024-01-02", "2024-01-09"
        )
        self.assertEqual(len(series), len(PRE_SPLIT) + len(POST_SPLIT))
        self.assertEqual([session for session, _ in series], sorted(s for s, _ in series))

    def test_either_isin_resolves_to_the_same_issuer_series(self):
        from_old = adjusted_close_series_by_issuer(self.conn, OLD_ISIN, "2024-01-02", "2024-01-09")
        from_new = adjusted_close_series_by_issuer(self.conn, NEW_ISIN, "2024-01-02", "2024-01-09")
        self.assertEqual(from_old, from_new)

    def test_return_across_the_split_is_what_a_holder_experienced(self):
        """Raw closes say -90%; back-adjusted says roughly flat."""
        series = dict(
            adjusted_close_series_by_issuer(self.conn, NEW_ISIN, "2024-01-02", "2024-01-09")
        )
        raw = 2620.0 / 26200.0 - 1.0
        self.assertAlmostEqual(raw, -0.90, places=2)

        adjusted = series["2024-01-05"] / series["2024-01-04"] - 1.0
        self.assertAlmostEqual(adjusted, 0.0, places=2)

    def test_prices_before_the_ex_date_are_rescaled_onto_the_new_basis(self):
        series = dict(
            adjusted_close_series_by_issuer(self.conn, NEW_ISIN, "2024-01-02", "2024-01-09")
        )
        self.assertAlmostEqual(series["2024-01-04"], 26200.0 * SPLIT_RATIO, places=6)
        self.assertAlmostEqual(series["2024-01-05"], 2620.0, places=6)

    def test_same_session_duplicate_isins_do_not_double_count(self):
        """Defensive: no overlap exists in the panel today, but if one appeared
        a prefix query would otherwise return two rows for one session."""
        self.conn.execute(
            "INSERT INTO daily_prices "
            "(exchange, session, isin, symbol, series, close, turnover) "
            "VALUES ('NSE', '2024-01-05', ?, 'NESTLEIND', 'EQ', 2610.0, 5e8)",
            (OLD_ISIN,),
        )
        series = adjusted_close_series_by_issuer(
            self.conn, NEW_ISIN, "2024-01-02", "2024-01-09"
        )
        sessions = [session for session, _ in series]
        self.assertEqual(len(sessions), len(set(sessions)))
        # The more heavily traded line is the live instrument.
        self.assertAlmostEqual(dict(series)["2024-01-05"], 2620.0, places=6)


if __name__ == "__main__":
    unittest.main()
