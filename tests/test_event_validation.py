import tempfile
import unittest
from pathlib import Path

from app.event_research.validation import archive_raw_filing, sha256_file, validate_filing_payload
from app.event_research.database import initialize_schema
from app.event_research.repository import EventResearchRepository


class EventValidationTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.raw_file = Path(self.temp_dir.name) / "result.html"
        self.raw_file.write_text("original NSE filing")
        self.payload = {
            "event": {
                "isin": "INE000A01001",
                "nse_symbol": "EXAMPLE",
                "issuer_name": "Example Limited",
                "instrument_valid_from": "2019-01-01",
                "result_period_end": "2024-06-30",
                "fiscal_quarter": "Q1",
                "source_exchange": "NSE",
                "source_url": "https://archives.nseindia.com/corporate/example.html",
                "source_format": "xbrl",
                "disseminated_at": "2024-08-01T17:15:00+05:30",
            },
            "facts": {
                "reporting_scope": "consolidated",
                "is_cumulative": False,
                "audit_status": "UNAUDITED",
                "basic_eps": 12.5,
                "revenue": 1000.0,
                "profit_after_tax": 120.0,
            },
        }

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_valid_payload_preserves_offset_and_hash(self):
        result = validate_filing_payload(self.payload, self.raw_file)
        self.assertTrue(result.is_valid, result.errors)
        self.assertEqual(result.normalized["event"]["available_at"].utcoffset().total_seconds(), 19800)
        self.assertEqual(len(result.normalized["event"]["raw_sha256"]), 64)

    def test_naive_timestamp_is_rejected(self):
        self.payload["event"]["disseminated_at"] = "2024-08-01T17:15:00"
        result = validate_filing_payload(self.payload, self.raw_file)
        self.assertFalse(result.is_valid)
        self.assertTrue(any("timezone offset" in error for error in result.errors))

    def test_missing_eps_is_visible_not_dropped(self):
        self.payload["facts"].pop("basic_eps")
        result = validate_filing_payload(self.payload, self.raw_file)
        self.assertTrue(result.is_valid, result.errors)
        self.assertTrue(any("basic_eps is missing" in warning for warning in result.warnings))

    def test_raw_filing_archive_is_content_addressed(self):
        result = validate_filing_payload(self.payload, self.raw_file)
        archive = archive_raw_filing(self.raw_file, Path(self.temp_dir.name) / "archive", result.normalized["event"]["raw_sha256"])
        self.assertEqual(sha256_file(archive), result.normalized["event"]["raw_sha256"])

    def test_revision_requires_predecessor_hash(self):
        self.payload["event"]["is_revision"] = True
        result = validate_filing_payload(self.payload, self.raw_file)
        self.assertFalse(result.is_valid)
        self.assertTrue(any("supersedes_source_sha256" in error for error in result.errors))

    def test_explicit_none_supersedes_hash_is_not_the_string_None(self):
        """A non-revision that sets the key explicitly to None must normalise to
        None, never to the literal string "None".

        `str(event.get(key, ""))` returns "None" for an explicit None, which is
        truthy, so the repository took every such filing down the revision-linking
        branch, failed to find a predecessor with source_sha256 == "None", and
        raised.  The legacy fetcher omits the key so it never saw this; the
        integrated fetcher sets it to None for non-revisions, and the defect
        silently rejected all 3,127 filings of the 2025+ era -- fold B and fold C
        had no corpus at all (2026-08-22).
        """
        self.payload["event"]["is_revision"] = False
        self.payload["event"]["supersedes_source_sha256"] = None
        result = validate_filing_payload(self.payload, self.raw_file)
        self.assertTrue(result.is_valid, result.errors)
        self.assertIsNone(result.normalized["event"]["supersedes_source_sha256"])

    def test_validated_event_imports_to_isolated_sqlite_database(self):
        result = validate_filing_payload(self.payload, self.raw_file)
        archive = archive_raw_filing(
            self.raw_file, Path(self.temp_dir.name) / "archive", result.normalized["event"]["raw_sha256"]
        )
        result.normalized["event"]["raw_storage_path"] = str(archive)
        database_url = f"sqlite:///{Path(self.temp_dir.name) / 'research.sqlite'}"
        initialize_schema(database_url)
        repository = EventResearchRepository(database_url)
        event, created = repository.import_validated_filing(result.normalized)
        self.assertTrue(created)
        self.assertEqual(event.source_sha256, result.normalized["event"]["raw_sha256"])
        self.assertEqual(repository.coverage_summary()["events"], 1)


if __name__ == "__main__":
    unittest.main()
