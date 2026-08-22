"""An unlinkable revision must be recorded, not fatal.

`import_validated_filing` raises when a revision's predecessor is absent.  That
is the right thing for the repository to do -- a revision must never be stored
as though it were an original -- but the fetchers let it propagate, so a single
unlinkable row aborted a 7,056-filing run after four hours (2026-08-18).

The charter's rule is explicit: "A filing whose facts cannot be proved from the
document is still stored, with its parse status, and an exception is logged.
Events are never dropped because their data is inconvenient."  Fatal is worse
than dropped.
"""

import unittest

from app.event_research.database import initialize_schema
from app.event_research.repository import EventResearchRepository


class RevisionPredecessorTests(unittest.TestCase):
    def test_repository_still_refuses_an_orphan_revision(self):
        """The guard itself must stay: a revision without its original is not
        an original, and storing it as one would silently rewrite history."""
        repo = EventResearchRepository()
        payload = {
            "event": {
                "isin": "INE000A01001",
                "nse_symbol": "EXAMPLE",
                "issuer_name": "Example Limited",
                "instrument_valid_from": "2024-01-01",
                "instrument_source_url": "https://example.invalid/cohort",
                "result_period_end": "2024-06-30",
                "fiscal_quarter": "Q1",
                "source_exchange": "NSE",
                "source_url": "https://example.invalid/revision.xml",
                "raw_sha256": "f" * 64,
                "raw_storage_path": "/dev/null",
                "source_format": "xbrl",
                "received_at": None,
                "disseminated_at": "2024-08-01T17:15:00+05:30",
                "available_at": "2024-08-01T17:15:00+05:30",
                "is_revision": True,
                "supersedes_source_sha256": "a" * 64,  # never imported
            },
            "facts": {
                "reporting_scope": "consolidated",
                "is_cumulative": False,
                "audit_status": "UNAUDITED",
                "basic_eps": 1.0,
                "parser_version": "test",
                "validation_status": "VALID",
            },
        }
        with self.assertRaises(ValueError):
            repo.import_validated_filing(payload)

    def test_fetchers_catch_it_rather_than_aborting(self):
        """The regression: both fetchers must handle the ValueError inline."""
        import inspect

        from scripts.event_research import (
            fetch_cohort_filings,
            fetch_cohort_integrated_filings,
        )

        for module in (fetch_cohort_filings, fetch_cohort_integrated_filings):
            with self.subTest(module=module.__name__):
                source = inspect.getsource(module.main)
                self.assertIn("except ValueError", source)
                self.assertIn("REVISION_PREDECESSOR_MISSING", source)


if __name__ == "__main__":
    unittest.main()
