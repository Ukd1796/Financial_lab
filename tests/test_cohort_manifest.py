"""Cohort-manifest import rules.

The regression these cover is the one this project keeps rediscovering: a
validation rule that rejects by matching nothing rather than by erroring, and
whose exclusions correlate with something the study cares about.  A blank
issuer name is a missing *label*, and 188 of the 3,900 rolled-cohort rows have
one -- concentrated in post-2024 IPOs, so rejecting them would silently bias
the later cohorts toward older companies.
"""

import unittest

from scripts.event_research.import_pilot_manifest import (
    UNKNOWN_ISSUER_NAME,
    _issuer_label,
    _normalise,
)


def _row(**overrides) -> dict[str, str]:
    row = {
        "cohort_id": "liquid-2024-06-30",
        "as_of_date": "2024-06-30",
        "isin": "INE040A01034",
        "nse_symbol": "HDFCBANK",
        "issuer_name": "HDFC Bank Limited",
        "sector": "",
        "selection_reason": "traded EQ every one of 60 sessions to 2024-06-30",
        "source_url": "https://nsearchives.nseindia.com/content/historical/EQUITIES/x.zip",
        "source_hash": "",
    }
    row.update(overrides)
    return row


class CohortManifestNormalisationTests(unittest.TestCase):
    def test_blank_issuer_name_does_not_reject_the_member(self):
        """A missing descriptive label is reported, never acted on.

        `build_pilot_cohort`'s own docstring already says the issuer name is
        "descriptive labelling, never a selection input"; the importer was
        contradicting it -- and rejecting over a field that
        `eligible_universe_snapshots` does not even have a column for.
        """
        normalised = _normalise(_row(issuer_name=""), line=2)
        self.assertEqual(normalised["isin"], "INE040A01034")
        self.assertNotIn("issuer_name", normalised)

    def test_missing_issuer_name_column_does_not_reject_the_member(self):
        row = _row()
        del row["issuer_name"]
        self.assertEqual(_normalise(row, line=2)["nse_symbol"], "HDFCBANK")

    def test_issuer_label_falls_back_to_unknown(self):
        self.assertEqual(_issuer_label(_row(issuer_name="")), UNKNOWN_ISSUER_NAME)
        self.assertEqual(_issuer_label({}), UNKNOWN_ISSUER_NAME)
        self.assertEqual(_issuer_label(_row()), "HDFC Bank Limited")

    def test_eligibility_fields_are_still_required(self):
        """Only the descriptive label is optional; selection inputs are not."""
        for field in ("cohort_id", "as_of_date", "isin", "nse_symbol", "selection_reason"):
            with self.subTest(field=field):
                with self.assertRaises(ValueError):
                    _normalise(_row(**{field: ""}), line=2)

    def test_source_url_must_be_https(self):
        with self.assertRaises(ValueError):
            _normalise(_row(source_url="http://nsearchives.nseindia.com/x.zip"), line=2)


if __name__ == "__main__":
    unittest.main()
