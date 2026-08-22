"""Tests for the ingestion layer.

The behaviour worth protecting here is *not spending money*.  A quota is
consumed permanently and cannot be refunded by fixing the bug afterwards, so
every test below pins a case where the correct action is to refuse, reuse, or
record — never to quietly issue another request.

Nothing here touches the network.  A stub transport stands in for ``requests``
so the guarantees can be exercised without a key.
"""

from __future__ import annotations

import json
import tempfile
import unittest
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

from app.analysis.database import initialize_schema
from app.analysis.indianapi_client import (
    APIError,
    BudgetExhausted,
    IndianAPIClient,
    MissingAPIKey,
    cache_key,
)
from app.analysis.repository import AnalysisRepository, budget_period
from app.analysis.sources import parse_transposed


class _Response:
    def __init__(self, payload, status=200):
        self._payload = payload
        self.status_code = status
        self.content = json.dumps(payload).encode()
        self.text = json.dumps(payload)

    @property
    def ok(self):
        return 200 <= self.status_code < 300

    def json(self):
        return self._payload


class _Transport:
    """Counts every request that would have reached the provider."""

    def __init__(self, payload=None, status=200):
        self.payload = payload if payload is not None else {"Sales": {"Jun 2024": 1.0}}
        self.status = status
        self.calls: list[tuple[str, dict]] = []

    def get(self, url, params=None, headers=None, timeout=None):
        self.calls.append((url, dict(params or {})))
        return _Response(self.payload, self.status)


class IngestionTestCase(unittest.TestCase):
    """Each test gets its own SQLite file and raw directory."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        root = Path(self._tmp.name)
        self.url = f"sqlite:///{root / 'analysis.sqlite'}"
        self.cache = root / "raw"
        initialize_schema(self.url)
        self.repo = AnalysisRepository(self.url)

    def tearDown(self):
        # The engine cache would otherwise hold a connection to a file that is
        # about to be deleted.
        from app.analysis.database import _engine

        _engine(self.url).dispose()
        self._tmp.cleanup()

    def _client(self, transport=None, budget=10, **kwargs):
        client = IndianAPIClient(
            api_key="test-key",
            budget=budget,
            repository=self.repo,
            cache_dir=self.cache,
            min_interval_seconds=0.0,
            **kwargs,
        )
        client._session = transport or _Transport()
        return client


class BudgetTests(IngestionTestCase):
    def test_call_over_the_cap_is_refused_not_truncated(self):
        """Stopping early would leave a half-filled store that looks complete."""
        transport = _Transport()
        client = self._client(transport, budget=3)

        for i in range(3):
            client.get("/historical_stats", {"stock_name": f"SYM{i}"})

        with self.assertRaises(BudgetExhausted):
            client.get("/historical_stats", {"stock_name": "SYM3"})

        self.assertEqual(len(transport.calls), 3, "a 4th request reached the network")
        self.assertEqual(client.spent(), 3)
        self.assertEqual(client.remaining(), 0)

    def test_budget_counts_across_process_restarts(self):
        """The cap lives in the ledger, not in memory, so a restart cannot reset it."""
        first = self._client(budget=5)
        for i in range(4):
            first.get("/historical_stats", {"stock_name": f"SYM{i}"})

        # A brand-new client object, as if the script had been re-launched.
        second = self._client(budget=5)
        self.assertEqual(second.spent(), 4)
        self.assertEqual(second.remaining(), 1)

    def test_default_budget_is_the_free_tier_allowance(self):
        """An unset environment must not be able to spend a paid plan's quota."""
        from app.analysis.indianapi_client import DEFAULT_CALL_BUDGET

        self.assertEqual(DEFAULT_CALL_BUDGET, 500)

    def test_missing_key_is_named_clearly(self):
        client = IndianAPIClient(
            api_key=None, budget=5, repository=self.repo, cache_dir=self.cache
        )
        client.api_key = None
        with self.assertRaises(MissingAPIKey) as ctx:
            client.get("/historical_stats", {"stock_name": "RELIANCE"})
        self.assertIn("INDIAN_API_KEY", str(ctx.exception))

    def test_dry_run_spends_nothing_and_records_the_plan(self):
        transport = _Transport()
        client = self._client(transport, budget=100, dry_run=True)

        with self.assertRaises(BudgetExhausted):
            client.get("/historical_stats", {"stock_name": "RELIANCE"})

        self.assertEqual(transport.calls, [])
        self.assertEqual(client.spent(), 0)
        self.assertEqual(client.planned, [("/historical_stats", {"stock_name": "RELIANCE"})])


class CacheTests(IngestionTestCase):
    def test_repeat_read_costs_zero_calls(self):
        """Re-parsing a vocabulary must never re-spend; only time is unrecoverable."""
        transport = _Transport()
        client = self._client(transport)

        first, from_cache_1, _ = client.get("/historical_stats", {"stock_name": "RELIANCE"})
        second, from_cache_2, _ = client.get("/historical_stats", {"stock_name": "RELIANCE"})

        self.assertEqual(first, second)
        self.assertFalse(from_cache_1)
        self.assertTrue(from_cache_2)
        self.assertEqual(len(transport.calls), 1, "the second read hit the network")
        self.assertEqual(client.spent(), 1, "a cache hit was billed against the quota")

    def test_cache_key_ignores_parameter_ordering(self):
        a = cache_key("/historical_stats", {"stock_name": "TCS", "stats": "ratios"})
        b = cache_key("/historical_stats", {"stats": "ratios", "stock_name": "TCS"})
        self.assertEqual(a, b)

    def test_truncated_cache_file_is_not_served_as_a_hit(self):
        """A file killed mid-write must re-fetch rather than pose as data."""
        transport = _Transport()
        client = self._client(transport)
        client.get("/historical_stats", {"stock_name": "RELIANCE"})

        path = self.cache / f"{cache_key('/historical_stats', {'stock_name': 'RELIANCE'})}.json"
        path.write_text('{"Sales": {"Jun 2024"')  # truncated

        self.assertIsNone(client.cached("/historical_stats", {"stock_name": "RELIANCE"}))
        client.get("/historical_stats", {"stock_name": "RELIANCE"})
        self.assertEqual(len(transport.calls), 2)

    def test_failed_response_is_not_cached(self):
        """Caching a 500 would make the failure permanent and invisible."""
        transport = _Transport(payload={"detail": "server error"}, status=500)
        client = self._client(transport)

        with self.assertRaises(APIError):
            client.get("/historical_stats", {"stock_name": "RELIANCE"})

        self.assertIsNone(client.cached("/historical_stats", {"stock_name": "RELIANCE"}))


class LedgerTests(IngestionTestCase):
    def test_billed_count_excludes_cache_hits(self):
        """This count is what reconciles against the provider dashboard."""
        transport = _Transport()
        client = self._client(transport)
        client.get("/historical_stats", {"stock_name": "RELIANCE"})
        client.get("/historical_stats", {"stock_name": "RELIANCE"})
        client.get("/historical_stats", {"stock_name": "TCS"})

        self.assertEqual(len(transport.calls), 2)
        self.assertEqual(self.repo.calls_spent(), 2)

        billed = sum(row["billed"] for row in self.repo.spend_summary())
        self.assertEqual(billed, 2)

    def test_transport_failure_is_still_ledgered(self):
        """Otherwise the ledger and the dashboard drift for the wrong reason."""
        import requests

        class _Broken:
            def get(self, *a, **k):
                raise requests.ConnectionError("no route to host")

        client = self._client(_Broken())
        with self.assertRaises(APIError):
            client.get("/historical_stats", {"stock_name": "RELIANCE"})
        self.assertEqual(self.repo.calls_spent(), 1)

    def test_api_key_never_reaches_the_ledger(self):
        transport = _Transport()
        client = self._client(transport)
        client.get("/historical_stats", {"stock_name": "RELIANCE"})

        for row in self.repo.spend_summary():
            self.assertNotIn("test-key", json.dumps(row))

        from sqlalchemy import select

        from app.analysis.database import new_session
        from app.analysis.models import ApiCallLedger

        session = new_session(self.url)
        try:
            for (params_json,) in session.execute(select(ApiCallLedger.params_json)).all():
                self.assertNotIn("test-key", params_json)
                self.assertNotIn("Api-Key", params_json)
        finally:
            session.close()

    def test_spend_is_bucketed_by_month(self):
        """Quotas reset monthly, so last month's spend must not count against this one."""
        last_month = (datetime.now(timezone.utc) - timedelta(days=40)).strftime("%Y-%m")
        for _ in range(7):
            self.repo.record_call(
                endpoint="/historical_stats", params={"stock_name": "OLD"}, period=last_month
            )
        self.assertEqual(self.repo.calls_spent(), 0)
        self.assertEqual(self.repo.calls_spent(last_month), 7)
        self.assertNotEqual(budget_period(), last_month)


class StoreTests(IngestionTestCase):
    def _facts(self, payload, stats="quarter_results"):
        from app.analysis.fundamentals import quarter_bucket

        return [
            {
                "period_end": period_end,
                "bucket": quarter_bucket(period_end),
                "metric": metric,
                "value": float(value) if isinstance(value, (int, float)) else None,
                "raw_value": str(value),
            }
            for period_end, row in parse_transposed(payload).items()
            for metric, value in row.items()
        ]

    def test_facts_round_trip_through_the_eav_table(self):
        payload = {
            "Sales": {"Jun 2024": 62613, "Sep 2024": 70000},
            "EPS in Rs": {"Jun 2024": 33.28, "Sep 2024": 35.0},
        }
        self.repo.save_snapshot(
            symbol="RELIANCE", endpoint="/historical_stats", stats="quarter_results",
            raw_sha256="a" * 64, raw_storage_path="raw/a.json", http_status=200,
            facts=self._facts(payload),
        )
        rows = self.repo.series("RELIANCE", "quarter_results", metric="EPS in Rs")
        self.assertEqual([r["period_end"] for r in rows], [date(2024, 6, 30), date(2024, 9, 30)])
        self.assertEqual([r["value"] for r in rows], [33.28, 35.0])

    def test_an_unknown_vocabulary_is_retained_not_discarded(self):
        """A metric this project has never seen still lands in the store."""
        payload = {"Cash Conversion Cycle": {"Jun 2024": 41.0}}
        self.repo.save_snapshot(
            symbol="TCS", endpoint="/historical_stats", stats="ratios",
            raw_sha256="b" * 64, raw_storage_path="raw/b.json", http_status=200,
            facts=self._facts(payload, stats="ratios"),
        )
        rows = self.repo.series("TCS", "ratios")
        self.assertEqual(rows[0]["metric"], "Cash Conversion Cycle")
        self.assertEqual(rows[0]["value"], 41.0)

    def test_identical_payload_does_not_fake_a_new_vintage(self):
        """The source often returns byte-identical history; that is not a restatement."""
        payload = {"Sales": {"Jun 2024": 62613}}
        kwargs = dict(
            symbol="RELIANCE", endpoint="/historical_stats", stats="quarter_results",
            raw_sha256="c" * 64, raw_storage_path="raw/c.json", http_status=200,
        )
        _, created_first = self.repo.save_snapshot(**kwargs, facts=self._facts(payload))
        _, created_again = self.repo.save_snapshot(**kwargs, facts=self._facts(payload))
        self.assertTrue(created_first)
        self.assertFalse(created_again)

    def test_a_restatement_keeps_both_vintages_and_reads_the_latest(self):
        """The whole point of append-only: a changed number stays visible as a change."""
        earlier = datetime(2026, 5, 1, tzinfo=timezone.utc)
        later = datetime(2026, 8, 1, tzinfo=timezone.utc)
        self.repo.save_snapshot(
            symbol="RELIANCE", endpoint="/historical_stats", stats="quarter_results",
            raw_sha256="d" * 64, raw_storage_path="raw/d.json", http_status=200,
            retrieved_at=earlier, facts=self._facts({"EPS in Rs": {"Jun 2024": 19.95}}),
        )
        self.repo.save_snapshot(
            symbol="RELIANCE", endpoint="/historical_stats", stats="quarter_results",
            raw_sha256="e" * 64, raw_storage_path="raw/e.json", http_status=200,
            retrieved_at=later, facts=self._facts({"EPS in Rs": {"Jun 2024": 15.48}}),
        )

        rows = self.repo.series("RELIANCE", "quarter_results", metric="EPS in Rs")
        self.assertEqual(len(rows), 1, "the reader should resolve to one value per period")
        self.assertEqual(rows[0]["value"], 15.48, "the latest vintage should win")

        summary = self.repo.coverage_summary()
        self.assertEqual(summary["snapshots"], 2, "the earlier vintage must be retained")

    def test_failures_are_stored_rather_than_dropped(self):
        """Dropping them would preferentially delete the deteriorating companies."""
        self.repo.record_exception(
            symbol="DHFL", endpoint="/historical_stats", stats="quarter_results",
            failure_type="EMPTY_PAYLOAD", details="source returned no quarters",
        )
        summary = self.repo.coverage_summary()
        self.assertEqual(summary["exceptions"], [{"failure_type": "EMPTY_PAYLOAD", "count": 1}])


class BackfillPlanTests(unittest.TestCase):
    """The plan is arithmetic the operator checks before spending; pin it."""

    def test_tier_costs_match_the_published_arithmetic(self):
        from scripts.analysis.backfill import plan_for

        self.assertEqual(len(plan_for(["A"], "core")), 4)
        self.assertEqual(len(plan_for(["A"], "full")), 9)
        self.assertEqual(len(plan_for(["A"] * 500, "full")), 4500)

    def test_estimate_endpoints_key_on_isin_without_a_lookup_call(self):
        """Probe 2026-08-12: stock_id accepts an ISIN, which bhavcopy already has."""
        from scripts.analysis.backfill import plan_for

        items = plan_for([{"symbol": "RELIANCE", "isin": "INE002A01018"}], "everything")
        forecasts = [(e, p) for _s, e, _st, p in items if e == "/stock_forecasts"]
        self.assertTrue(forecasts)
        for _endpoint, params in forecasts:
            self.assertEqual(params["stock_id"], "INE002A01018")
        self.assertIn(
            "Interim",
            {p["period_type"] for _e, p in forecasts},
            "quarterly (Interim) surprise must be planned, not just Annual",
        )

    def test_estimates_are_skipped_when_no_isin_is_known(self):
        """Better to skip than to burn a call per symbol discovering an identifier."""
        from scripts.analysis.backfill import plan_for

        items = plan_for([{"symbol": "RELIANCE", "isin": None}], "everything")
        endpoints = {endpoint for _s, endpoint, _st, _p in items}
        self.assertNotIn("/stock_forecasts", endpoints)
        self.assertNotIn("/stock_target_price", endpoints)

    def test_statement_is_never_planned(self):
        """Its enum duplicates historical_stats and it returns one period, not a series."""
        from scripts.analysis.backfill import plan_for

        for tier in ("core", "full", "everything"):
            endpoints = {
                endpoint
                for _s, endpoint, _st, _p in plan_for(
                    [{"symbol": "A", "isin": "INE0"}], tier
                )
            }
            self.assertNotIn("/statement", endpoints, tier)

    def test_non_numeric_cells_keep_their_raw_value(self):
        """A reported non-number must stay distinguishable from an absent quarter."""
        from scripts.analysis.backfill import facts_from

        facts = {f["metric"]: f for f in facts_from({
            "Sales": {"Jun 2024": 62613},
            "ROCE %": {"Jun 2024": "18.4%"},
            "Note": {"Jun 2024": "n/a"},
        })}
        self.assertEqual(facts["Sales"]["value"], 62613.0)
        self.assertEqual(facts["ROCE %"]["value"], 18.4)
        self.assertIsNone(facts["Note"]["value"])
        self.assertEqual(facts["Note"]["raw_value"], "n/a")


class StoreReportTests(IngestionTestCase):
    def test_report_rebuilds_a_series_from_the_store_without_network(self):
        from app.analysis.fundamentals import STATUS_VALID, quarter_bucket

        # Six unbroken quarters so the series clears the seasonal-history bar.
        periods = [date(2024, 9, 30), date(2024, 12, 31), date(2025, 3, 31),
                   date(2025, 6, 30), date(2025, 9, 30), date(2025, 12, 31)]
        facts = [
            {"period_end": p, "bucket": quarter_bucket(p), "metric": metric,
             "value": value, "raw_value": str(value)}
            for p in periods
            for metric, value in (("Sales", 1000.0), ("Net Profit", 100.0),
                                  ("Operating Profit", 200.0), ("EPS in Rs", 10.0))
        ]
        self.repo.save_snapshot(
            symbol="RELIANCE", endpoint="/historical_stats", stats="quarter_results",
            raw_sha256="f" * 64, raw_storage_path="raw/f.json", http_status=200, facts=facts,
        )

        import app.analysis.repository as repo_module
        from scripts.analysis import quality_report

        original = repo_module.AnalysisRepository
        repo_module.AnalysisRepository = lambda *a, **k: AnalysisRepository(self.url)
        try:
            series = quality_report.load_from_store("RELIANCE", "quarter_results")
        finally:
            repo_module.AnalysisRepository = original

        self.assertEqual(series.status, STATUS_VALID)
        self.assertEqual(len(series.quarters), 6)
        self.assertFalse(series.is_point_in_time, "stored vendor data is never PIT")
        self.assertEqual(series.quarter_ending(date(2025, 6, 30)).values["basic_eps"], 10.0)


class ListedElsewhereTests(unittest.TestCase):
    """Listing survival is a second dimension, never a rewrite of `status`."""

    def _outcomes(self):
        from app.analysis.delisting import (
            Outcome, STATUS_ACTIVE, STATUS_EXIT_AFTER_COLLAPSE, STATUS_EXIT_FLAT_OR_UP,
        )

        def make(isin, symbol, status):
            return Outcome(
                isin=isin, symbol=symbol, first_seen=date(2018, 1, 31),
                last_seen=date(2022, 6, 30), months_observed=50, gap_months=0,
                last_close=1.0, close_12m_before=10.0, close_6m_before=5.0,
                return_12m=-0.9, return_6m=-0.8, peak_close=100.0,
                drawdown_from_peak=-0.99, status=status,
            )

        return [
            make("INE066A01013", "STILLTHERE", STATUS_EXIT_AFTER_COLLAPSE),
            make("INE202B01019", "REISSUED", STATUS_EXIT_AFTER_COLLAPSE),
            make("INE999Z01011", "TRULYGONE", STATUS_EXIT_AFTER_COLLAPSE),
            make("INE018A01030", "NEVERLEFT", STATUS_ACTIVE),
            make("INE001A01012", "BOUGHTOUT", STATUS_EXIT_FLAT_OR_UP),
        ]

    def test_collapse_label_is_untouched_by_listing_survival(self):
        """A -99% fall is a -99% fall wherever the name later trades."""
        from app.analysis.delisting import (
            LISTING_BSE_SAME_ISIN, STATUS_EXIT_AFTER_COLLAPSE, annotate_listed_elsewhere,
        )

        annotated = annotate_listed_elsewhere(self._outcomes(), {"INE066A01013"})
        survivor = next(o for o in annotated if o.symbol == "STILLTHERE")

        self.assertEqual(survivor.status, STATUS_EXIT_AFTER_COLLAPSE)
        self.assertEqual(survivor.listed_elsewhere, LISTING_BSE_SAME_ISIN)

    def test_successor_instrument_counts_as_still_listed(self):
        """A face-value change reissues the ISIN; exact-match alone reads it as dead."""
        from app.analysis.delisting import LISTING_BSE_ISSUER, annotate_listed_elsewhere

        annotated = annotate_listed_elsewhere(self._outcomes(), {"INE202B01027"})
        reissued = next(o for o in annotated if o.symbol == "REISSUED")

        self.assertEqual(reissued.listed_elsewhere, LISTING_BSE_ISSUER)

    def test_absent_from_both_exchanges_is_the_only_true_delisting(self):
        from app.analysis.delisting import LISTING_ABSENT, annotate_listed_elsewhere

        annotated = annotate_listed_elsewhere(self._outcomes(), {"INE066A01013"})
        gone = next(o for o in annotated if o.symbol == "TRULYGONE")

        self.assertEqual(gone.listed_elsewhere, LISTING_ABSENT)

    def test_a_name_that_never_left_nse_is_not_asked_the_question(self):
        from app.analysis.delisting import LISTING_NOT_APPLICABLE, annotate_listed_elsewhere

        annotated = annotate_listed_elsewhere(self._outcomes(), set())
        active = next(o for o in annotated if o.symbol == "NEVERLEFT")

        self.assertEqual(active.listed_elsewhere, LISTING_NOT_APPLICABLE)

    def test_missing_reference_data_leaves_rows_unchecked_not_dead(self):
        """A missing price panel must not manufacture confirmed deaths.

        This is the same silent-failure shape as the NSE endpoint migrations:
        absence of evidence read as evidence of absence.
        """
        from app.analysis.delisting import LISTING_UNCHECKED, annotate_listed_elsewhere

        annotated = annotate_listed_elsewhere(self._outcomes(), None)

        self.assertTrue(all(o.listed_elsewhere == LISTING_UNCHECKED for o in annotated))


class OutcomeReplacementTests(IngestionTestCase):
    """``save_outcomes`` promises replacement, so it must handle a shrinking universe."""

    WINDOW = {"window_start": date(2018, 1, 1), "window_end": date(2026, 8, 11)}

    def _make_outcome(self, isin: str, status: str):
        from app.analysis.delisting import Outcome

        return Outcome(
            isin=isin, symbol=isin[:6], first_seen=date(2018, 1, 31),
            last_seen=date(2026, 7, 31), months_observed=100, gap_months=0,
            last_close=10.0, close_12m_before=10.0, close_6m_before=10.0,
            return_12m=0.0, return_6m=0.0, peak_close=10.0,
            drawdown_from_peak=0.0, status=status,
        )

    def _stored(self):
        from app.analysis.models import DelistingOutcome
        from sqlalchemy import select

        session = self.repo._session()
        try:
            return {
                row.isin: row.status
                for row in session.execute(select(DelistingOutcome)).scalars()
            }
        finally:
            session.close()

    def test_isin_dropped_from_the_universe_is_deleted_not_orphaned(self):
        """An upsert-only merge left 412 INF* fund ISINs behind carrying stale labels.

        The universe legitimately shrinks — excluding non-equity instruments, or
        raising the liquidity floor — and a row that survives its own exclusion
        is worse than no row, because it still answers queries.
        """
        self.repo.save_outcomes(
            [self._make_outcome("INE000A01011", "ACTIVE"),
             self._make_outcome("INF109KB1WF4", "INSTRUMENT_CHANGED")],
            **self.WINDOW,
        )
        self.assertEqual(len(self._stored()), 2)

        # Re-run after excluding INF* units, as build_delisting_labels now does.
        self.repo.save_outcomes([self._make_outcome("INE000A01011", "ACTIVE")], **self.WINDOW)

        self.assertEqual(
            self._stored(), {"INE000A01011": "ACTIVE"},
            "the excluded fund ISIN outlived its exclusion",
        )

    def test_relabelled_isin_is_updated_in_place(self):
        """Re-thresholding must correct a label, never store two contradictory ones."""
        self.repo.save_outcomes([self._make_outcome("INE001A01012", "EXIT_AMBIGUOUS")], **self.WINDOW)
        self.repo.save_outcomes(
            [self._make_outcome("INE001A01012", "EXIT_AFTER_COLLAPSE")], **self.WINDOW
        )

        self.assertEqual(self._stored(), {"INE001A01012": "EXIT_AFTER_COLLAPSE"})

    def test_a_different_window_is_a_separate_set(self):
        """Deletion is scoped to the window being rewritten, not the whole table."""
        self.repo.save_outcomes([self._make_outcome("INE002A01018", "ACTIVE")], **self.WINDOW)
        self.repo.save_outcomes(
            [self._make_outcome("INE003A01024", "ACTIVE")],
            window_start=date(2019, 1, 1), window_end=date(2020, 1, 1),
        )

        self.assertEqual(len(self._stored()), 2, "rewriting one window erased another")


class ResumabilityTests(IngestionTestCase):
    def test_restart_after_interruption_respends_nothing(self):
        transport = _Transport()
        client = self._client(transport, budget=100)

        planned = [("RELIANCE", "quarter_results"), ("RELIANCE", "ratios"), ("TCS", "ratios")]

        def run(pairs):
            done = self.repo.fetched_pairs()
            for symbol, stats in pairs:
                if (symbol, "/historical_stats", stats) in done:
                    continue
                payload, _, digest = client.get(
                    "/historical_stats", {"stock_name": symbol, "stats": stats}
                )
                self.repo.save_snapshot(
                    symbol=symbol, endpoint="/historical_stats", stats=stats,
                    raw_sha256=digest, raw_storage_path=f"raw/{digest}.json",
                    http_status=200, facts=[],
                )

        run(planned[:2])          # interrupted after two
        before = len(transport.calls)
        run(planned)              # restarted with the full list

        self.assertEqual(before, 2)
        self.assertEqual(len(transport.calls), 3, "already-stored work was re-fetched")
        self.assertTrue(self.repo.has_snapshot("TCS", "/historical_stats", "ratios"))


if __name__ == "__main__":
    unittest.main()


class BhavcopyFormatTests(unittest.TestCase):
    """NSE migrated the end-of-day file mid-2024; both layouts must read alike.

    The failure this guards against is silent: if only one format is tried, a
    404 from the wrong template is indistinguishable from a market holiday, and
    an entire archive reads as "no sessions held" with no error raised.
    """

    def test_udiff_row_is_renamed_to_the_legacy_schema(self):
        from app.event_research.nse_client import normalise_bhavcopy_row

        row = normalise_bhavcopy_row({
            "TckrSymb": "RELIANCE", "SctySrs": " EQ ", "ISIN": "INE002A01018",
            "ClsPric": "1334.80", "TtlTradgVol": "9885638",
            "TtlTrfVal": "13138878797.80", "TradDt": "2026-08-07",
        })
        self.assertEqual(row["SYMBOL"], "RELIANCE")
        self.assertEqual(row["SERIES"], "EQ")
        self.assertEqual(row["TOTTRDVAL"], "13138878797.80")
        self.assertEqual(row["ISIN"], "INE002A01018")

    def test_legacy_row_passes_through_untouched(self):
        from app.event_research.nse_client import normalise_bhavcopy_row

        row = {"SYMBOL": "TCS", "SERIES": "EQ", "TOTTRDVAL": "1234.5"}
        self.assertEqual(normalise_bhavcopy_row(dict(row)), row)

    def test_unmapped_udiff_columns_are_kept_not_dropped(self):
        from app.event_research.nse_client import normalise_bhavcopy_row

        row = normalise_bhavcopy_row({"TckrSymb": "X", "SsnId": "F", "OpnIntrst": "0"})
        self.assertEqual(row["SsnId"], "F")

    def test_recent_dates_try_udiff_first_and_old_dates_try_legacy_first(self):
        from app.event_research.nse_client import NSEResearchClient

        client = NSEResearchClient.__new__(NSEResearchClient)
        self.assertIn("BhavCopy_NSE_CM", client._bhavcopy_urls(date(2026, 8, 7))[0])
        self.assertIn("historical/EQUITIES", client._bhavcopy_urls(date(2019, 3, 15))[0])
        # Both are always attempted, so the cutover window cannot lose a session.
        for probe in (date(2026, 8, 7), date(2019, 3, 15)):
            self.assertEqual(len(client._bhavcopy_urls(probe)), 2)


class DelistingLabelTests(unittest.TestCase):
    """The outcome labels the vendor feed cannot supply.

    Each test pins a way the label could be quietly wrong: a rename read as a
    death, a suspension read as an exit, or a stock split read as a collapse.
    """

    @staticmethod
    def _snapshots(series):
        """series: {isin: {month_index: (symbol, close)}} over 25 monthly samples."""
        from app.analysis.delisting import Snapshot

        out = []
        for index in range(25):
            rows = {}
            for isin, points in series.items():
                if index in points:
                    symbol, close = points[index]
                    rows[isin] = {"SYMBOL": symbol, "SERIES": "EQ",
                                  "ISIN": isin, "CLOSE": str(close)}
            out.append(Snapshot(session=date(2024, 1, 1) + timedelta(days=30 * index), rows=rows))
        return out

    def _one(self, points, **kwargs):
        from app.analysis.delisting import build_outcomes

        return build_outcomes(self._snapshots({"INE001": points}), **kwargs)[0]

    def test_a_name_trading_at_the_end_is_active(self):
        from app.analysis.delisting import STATUS_ACTIVE

        outcome = self._one({i: ("ALIVE", 100.0) for i in range(25)})
        self.assertEqual(outcome.status, STATUS_ACTIVE)

    def test_exit_after_a_collapse_is_labelled_as_such(self):
        from app.analysis.delisting import STATUS_EXIT_AFTER_COLLAPSE

        points = {i: ("DYING", 100.0) for i in range(12)}
        points.update({i: ("DYING", 100.0 * (1 - 0.11 * (i - 11))) for i in range(12, 20)})
        outcome = self._one(points)
        self.assertEqual(outcome.status, STATUS_EXIT_AFTER_COLLAPSE)
        self.assertLess(outcome.drawdown_from_peak, -0.70)

    def test_a_slow_collapse_that_bounced_before_delisting_is_still_a_collapse(self):
        """The DHFL/RCOM case: -97% years earlier, then a penny-stock bounce.

        The trailing 12-month return is POSITIVE here and would call this a
        benign exit; distance from the lifetime peak is what identifies it.
        """
        from app.analysis.delisting import STATUS_EXIT_AFTER_COLLAPSE

        points = {i: ("SLOWDEATH", 600.0) for i in range(6)}
        points.update({i: ("SLOWDEATH", 15.0) for i in range(6, 14)})
        points.update({i: ("SLOWDEATH", 23.0) for i in range(14, 20)})
        outcome = self._one(points)
        self.assertGreater(outcome.return_12m, 0, "the bounce should show as a positive year")
        self.assertLess(outcome.drawdown_from_peak, -0.90)
        self.assertEqual(outcome.status, STATUS_EXIT_AFTER_COLLAPSE)

    def test_exit_at_a_flat_price_is_not_called_a_failure(self):
        """A buyout removes the ticker too; calling it a failure inverts the label."""
        from app.analysis.delisting import STATUS_EXIT_FLAT_OR_UP

        outcome = self._one({i: ("ACQUIRED", 100.0 + i) for i in range(20)})
        self.assertEqual(outcome.status, STATUS_EXIT_FLAT_OR_UP)

    def test_a_split_is_adjusted_away_not_counted_as_a_collapse(self):
        """Bhavcopy close is unadjusted: 1:10 looks like -90% and is not a loss."""
        from app.analysis.delisting import STATUS_EXIT_FLAT_OR_UP

        points = {i: ("SPLITTER", 1000.0) for i in range(14)}
        points.update({i: ("SPLITTER", 100.0) for i in range(14, 20)})
        outcome = self._one(points)
        self.assertEqual(outcome.status, STATUS_EXIT_FLAT_OR_UP)
        self.assertIn("split/bonus adjustment", outcome.notes)
        self.assertAlmostEqual(outcome.drawdown_from_peak, 0.0, places=6)

    def test_an_active_name_with_a_bonus_is_not_left_looking_crashed(self):
        """RELIANCE's Oct-2024 bonus made it read 58% below peak near an all-time high."""
        from app.analysis.delisting import STATUS_ACTIVE, split_adjusted

        points = {i: ("BONUSCO", 1400.0) for i in range(12)}
        points.update({i: ("BONUSCO", 700.0) for i in range(12, 25)})
        outcome = self._one(points)
        self.assertEqual(outcome.status, STATUS_ACTIVE)
        self.assertAlmostEqual(outcome.drawdown_from_peak, 0.0, places=6)
        adjusted, ratios = split_adjusted({0: 1400.0, 1: 700.0})
        self.assertEqual(ratios, [0.5])
        self.assertAlmostEqual(adjusted[0], 700.0)

    def test_a_suspension_is_reported_as_a_gap_not_an_early_exit(self):
        points = {i: ("PAUSED", 100.0) for i in range(25) if i not in (10, 11, 12)}
        outcome = self._one(points)
        self.assertEqual(outcome.gap_months, 3)
        self.assertIn("suspension", outcome.notes)
        self.assertEqual(outcome.last_seen, self._snapshots({"INE001": points})[24].session)

    def test_isin_keying_means_a_rename_is_not_a_death_and_a_birth(self):
        """102 such renames were measured between 2018 and 2026 (e.g. PVR->PVRINOX)."""
        from app.analysis.delisting import STATUS_ACTIVE, build_outcomes

        points = {i: ("OLDNAME", 100.0) for i in range(12)}
        points.update({i: ("NEWNAME", 100.0) for i in range(12, 25)})
        outcomes = build_outcomes(self._snapshots({"INE001": points}))
        self.assertEqual(len(outcomes), 1, "a rename produced two records")
        self.assertEqual(outcomes[0].status, STATUS_ACTIVE)
        self.assertEqual(outcomes[0].symbol, "NEWNAME")

    def test_an_exit_without_prior_history_is_unknown_not_guessed(self):
        from app.analysis.delisting import STATUS_EXIT_UNKNOWN_PATH

        outcome = self._one({0: ("BRIEF", 100.0)})
        self.assertEqual(outcome.status, STATUS_EXIT_UNKNOWN_PATH)
        self.assertIsNone(outcome.return_12m)

    def test_the_ambiguous_band_is_visible_rather_than_absorbed(self):
        from app.analysis.delisting import STATUS_EXIT_AMBIGUOUS

        points = {i: ("MEH", 100.0) for i in range(12)}
        points.update({i: ("MEH", 55.0) for i in range(12, 20)})
        self.assertEqual(self._one(points).status, STATUS_EXIT_AMBIGUOUS)

    def test_common_split_ratios_are_recognised_and_ordinary_losses_are_not(self):
        from app.analysis.delisting import looks_like_corporate_action

        for ratio in (0.5, 0.2, 0.1, 0.05, 0.01):
            self.assertTrue(looks_like_corporate_action(ratio), ratio)
        # Deliberately NOT flagged: as monthly moves these occur organically
        # often enough that withholding them would delete genuine declines.
        for ratio in (0.75, 0.667, 0.33, 0.25, 0.42, 0.63, 0.08, 0.9):
            self.assertFalse(looks_like_corporate_action(ratio), ratio)

    def test_month_ends_covers_the_window_inclusively(self):
        from app.analysis.delisting import month_ends

        ends = month_ends(date(2024, 1, 1), date(2024, 4, 30))
        self.assertEqual(ends, [date(2024, 1, 31), date(2024, 2, 29),
                                date(2024, 3, 31), date(2024, 4, 30)])


class InstrumentChangeTests(unittest.TestCase):
    """An ISIN change is not a death.

    A face-value change or split issues a new ISIN for the same company
    (INE092B01017 -> INE092B01025).  Keying deaths on ISIN alone invented 318 of
    1,002 apparent exits, including CONCOR, IEX and NBCC — all trading today.
    """

    @staticmethod
    def _snap(session, entries):
        from app.analysis.delisting import Snapshot

        return Snapshot(session=session, rows={
            isin: {"SYMBOL": sym, "SERIES": "EQ", "ISIN": isin, "CLOSE": str(close)}
            for isin, sym, close in entries
        })

    def test_successor_instrument_means_the_issuer_did_not_die(self):
        from app.analysis.delisting import STATUS_INSTRUMENT_CHANGED, build_outcomes

        old, new = "INE092B01017", "INE092B01025"
        snaps = [self._snap(date(2024, 1, 1), [(old, "INDNIPPON", 100.0)]),
                 self._snap(date(2024, 2, 1), [(old, "INDNIPPON", 90.0)]),
                 self._snap(date(2024, 3, 1), [(new, "INDNIPPON", 45.0)]),
                 self._snap(date(2024, 4, 1), [(new, "INDNIPPON", 47.0)])]
        outcomes = {o.isin: o for o in build_outcomes(snaps)}
        self.assertEqual(outcomes[old].status, STATUS_INSTRUMENT_CHANGED)
        self.assertIn("different ISIN", outcomes[old].notes)

    def test_a_genuine_death_has_no_surviving_sibling(self):
        from app.analysis.delisting import STATUS_EXIT_AFTER_COLLAPSE, build_outcomes

        dead, other = "INE202B01012", "INE999Z01011"
        snaps = [self._snap(date(2024, 1, 1), [(dead, "DHFL", 600.0), (other, "SAFE", 100.0)]),
                 self._snap(date(2024, 2, 1), [(dead, "DHFL", 300.0), (other, "SAFE", 100.0)]),
                 self._snap(date(2024, 3, 1), [(dead, "DHFL", 18.0), (other, "SAFE", 100.0)]),
                 self._snap(date(2024, 4, 1), [(other, "SAFE", 100.0)])]
        outcomes = {o.isin: o for o in build_outcomes(snaps)}
        self.assertEqual(outcomes[dead].status, STATUS_EXIT_AFTER_COLLAPSE)

    def test_issuer_prefix_is_the_first_nine_characters(self):
        from app.analysis.delisting import isin_issuer

        self.assertEqual(isin_issuer("INE092B01017"), isin_issuer("INE092B01025"))
        self.assertNotEqual(isin_issuer("INE092B01017"), isin_issuer("INE202B01012"))


class IssuerSuccessionTests(unittest.TestCase):
    """A surviving issuer code does not mean a surviving holding."""

    @staticmethod
    def _snap(session, entries):
        from app.analysis.delisting import Snapshot

        return Snapshot(session=session, rows={
            isin: {"SYMBOL": sym, "SERIES": "EQ", "ISIN": isin, "CLOSE": str(close)}
            for isin, sym, close in entries
        })

    def test_a_wipeout_is_not_rescued_by_its_successor_entity(self):
        """DHFL: absorbed by PIRAMALFIN via insolvency, equity holders got nothing."""
        from app.analysis.delisting import STATUS_EXIT_AFTER_COLLAPSE, build_outcomes

        old, new = "INE202B01012", "INE202B01038"
        snaps = [self._snap(date(2024, 1, 1), [(old, "DHFL", 600.0)]),
                 self._snap(date(2024, 2, 1), [(old, "DHFL", 200.0)]),
                 self._snap(date(2024, 3, 1), [(old, "DHFL", 12.0)]),
                 self._snap(date(2024, 4, 1), [(new, "PIRAMALFIN", 900.0)])]
        outcomes = {o.isin: o for o in build_outcomes(snaps)}
        self.assertEqual(outcomes[old].status, STATUS_EXIT_AFTER_COLLAPSE)

    def test_a_rename_without_a_collapse_is_still_rescued(self):
        from app.analysis.delisting import STATUS_INSTRUMENT_CHANGED, build_outcomes

        old, new = "INE854D01016", "INE854D01024"
        snaps = [self._snap(date(2024, 1, 1), [(old, "MCDOWELL-N", 100.0)]),
                 self._snap(date(2024, 2, 1), [(old, "MCDOWELL-N", 104.0)]),
                 self._snap(date(2024, 3, 1), [(new, "UNITDSPR", 106.0)])]
        outcomes = {o.isin: o for o in build_outcomes(snaps)}
        self.assertEqual(outcomes[old].status, STATUS_INSTRUMENT_CHANGED)

    def test_fund_and_etf_isins_are_excluded_from_an_equity_study(self):
        from app.analysis.delisting import is_company

        self.assertTrue(is_company("INE202B01012"))
        self.assertFalse(is_company("INF109KB1WF4"))
        self.assertFalse(is_company(""))
