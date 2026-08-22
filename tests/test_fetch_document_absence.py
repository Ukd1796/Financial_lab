"""Absence of a document is not a failure to fetch one.

Two facts were being recorded as the same exception:

* NSE publishes a literal ``-`` in the xbrl column when a filing has **no XBRL
  document**.  It is truthy, so it was being turned into
  ``.../corporate/xbrl/-``, fetched, 404'd three times and logged as a failure
  that never had a document behind it -- 23 of the first 36 exceptions.
* NSE's index sometimes lists a document its archive no longer serves.  That is
  a permanent absence; retrying cannot fix it.

Both used to land in ``FETCH_FAILED`` alongside genuine transient errors, which
is the same conflation the BSE work hit: a landing page served on a holiday
must not be allowed to claim "no session existed".  Charter §6's missing-data
gate needs these counted apart.
"""

import unittest

from app.event_research.nse_client import NSEDocumentNotFound, NSEUnavailable
from scripts.event_research.fetch_cohort_filings import document_url


class DocumentUrlTests(unittest.TestCase):
    def test_placeholder_dash_is_not_a_url(self):
        self.assertIsNone(document_url({"xbrl": "-"}))

    def test_surrounding_whitespace_does_not_rescue_a_placeholder(self):
        self.assertIsNone(document_url({"xbrl": "  -  "}))

    def test_empty_and_missing_are_absent(self):
        self.assertIsNone(document_url({"xbrl": ""}))
        self.assertIsNone(document_url({}))
        self.assertIsNone(document_url({"xbrl": None}))

    def test_other_null_markers_are_absent(self):
        for marker in ("NA", "n/a", "null", "None"):
            with self.subTest(marker=marker):
                self.assertIsNone(document_url({"xbrl": marker}))

    def test_a_real_url_survives(self):
        url = "https://nsearchives.nseindia.com/corporate/xbrl/INDAS_1477042_WEB.xml"
        self.assertEqual(document_url({"xbrl": url}), url)

    def test_a_real_url_is_stripped(self):
        url = "https://nsearchives.nseindia.com/corporate/xbrl/X.xml"
        self.assertEqual(document_url({"xbrl": f"  {url}\n"}), url)


class ExceptionTaxonomyTests(unittest.TestCase):
    def test_not_found_is_a_kind_of_unavailable(self):
        """The subclass relationship is what made the conflation possible, so
        the ordering of `except` clauses in the fetchers is load-bearing."""
        self.assertTrue(issubclass(NSEDocumentNotFound, NSEUnavailable))

    def test_catching_unavailable_first_would_swallow_not_found(self):
        try:
            raise NSEDocumentNotFound("gone")
        except NSEDocumentNotFound:
            caught = "DOCUMENT_ABSENT"
        except NSEUnavailable:  # pragma: no cover - ordering guard
            caught = "FETCH_FAILED"
        self.assertEqual(caught, "DOCUMENT_ABSENT")


if __name__ == "__main__":
    unittest.main()
