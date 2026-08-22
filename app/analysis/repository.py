"""Reads and writes for the analysis fact store.

Writes are append-only.  Refetching a symbol adds a vintage; it never edits an
earlier one, so a restatement stays visible as a difference between snapshots.
"""

from __future__ import annotations

import json
from datetime import date, datetime, timezone
from typing import Any, Iterable

from sqlalchemy import Integer, cast, func, select

from app.analysis.database import new_session
from app.analysis.models import (
    ApiCallLedger,
    CohortSnapshot,
    FetchSnapshot,
    FundamentalFact,
    IngestionException,
)


def budget_period(moment: datetime | None = None) -> str:
    """Provider quotas reset monthly, so spend is bucketed by ``YYYY-MM``."""
    return (moment or datetime.now(timezone.utc)).strftime("%Y-%m")


class AnalysisRepository:
    def __init__(self, database_url: str | None = None):
        self.database_url = database_url

    def _session(self):
        return new_session(self.database_url)

    # ---------------------------------------------------------------- ledger

    def record_call(
        self,
        *,
        endpoint: str,
        params: dict[str, Any],
        http_status: int | None = None,
        response_sha256: str | None = None,
        response_bytes: int | None = None,
        cache_hit: bool = False,
        error: str | None = None,
        period: str | None = None,
    ) -> None:
        session = self._session()
        try:
            session.add(
                ApiCallLedger(
                    endpoint=endpoint,
                    params_json=json.dumps(params, sort_keys=True),
                    http_status=http_status,
                    response_sha256=response_sha256,
                    response_bytes=response_bytes,
                    cache_hit=cache_hit,
                    error=error,
                    budget_period=period or budget_period(),
                )
            )
            session.commit()
        finally:
            session.close()

    def calls_spent(self, period: str | None = None) -> int:
        """Network calls charged against the quota in this billing period.

        Cache hits are excluded because they never reached the provider; this
        is the number that should match the dashboard.
        """
        session = self._session()
        try:
            return int(
                session.execute(
                    select(func.count(ApiCallLedger.id)).where(
                        ApiCallLedger.budget_period == (period or budget_period()),
                        ApiCallLedger.cache_hit.is_(False),
                    )
                ).scalar_one()
            )
        finally:
            session.close()

    def spend_summary(self) -> list[dict[str, Any]]:
        session = self._session()
        try:
            rows = session.execute(
                select(
                    ApiCallLedger.budget_period,
                    ApiCallLedger.endpoint,
                    func.count(ApiCallLedger.id),
                    func.sum(cast(ApiCallLedger.cache_hit, Integer)),
                )
                .group_by(ApiCallLedger.budget_period, ApiCallLedger.endpoint)
                .order_by(ApiCallLedger.budget_period, ApiCallLedger.endpoint)
            ).all()
            return [
                {
                    "period": p,
                    "endpoint": e,
                    "total": int(total),
                    "cache_hits": int(hits or 0),
                    "billed": int(total) - int(hits or 0),
                }
                for p, e, total, hits in rows
            ]
        finally:
            session.close()

    # -------------------------------------------------------------- snapshots

    def has_snapshot(self, symbol: str, endpoint: str, stats: str = "") -> bool:
        """Whether this (symbol, endpoint, stats) was ever fetched.

        Drives resumability: a backfill killed mid-run and restarted must not
        re-spend a single call on work already stored.
        """
        session = self._session()
        try:
            return (
                session.execute(
                    select(FetchSnapshot.id).where(
                        FetchSnapshot.symbol == symbol,
                        FetchSnapshot.endpoint == endpoint,
                        FetchSnapshot.stats == stats,
                    ).limit(1)
                ).first()
                is not None
            )
        finally:
            session.close()

    def fetched_pairs(self) -> set[tuple[str, str, str]]:
        """Every stored (symbol, endpoint, stats), for a one-query resume."""
        session = self._session()
        try:
            return {
                (s, e, st)
                for s, e, st in session.execute(
                    select(FetchSnapshot.symbol, FetchSnapshot.endpoint, FetchSnapshot.stats)
                ).all()
            }
        finally:
            session.close()

    def save_snapshot(
        self,
        *,
        symbol: str,
        endpoint: str,
        stats: str,
        raw_sha256: str,
        raw_storage_path: str,
        http_status: int,
        facts: Iterable[dict[str, Any]] = (),
        retrieved_at: datetime | None = None,
        source: str = "indianapi",
    ) -> tuple[Any, bool]:
        """Store one vintage and its facts.

        An identical payload for the same key is a no-op: the source often
        returns byte-identical history, and recording that as a fresh vintage
        would fake a restatement record we do not have.
        """
        session = self._session()
        try:
            existing = session.execute(
                select(FetchSnapshot).where(
                    FetchSnapshot.symbol == symbol,
                    FetchSnapshot.endpoint == endpoint,
                    FetchSnapshot.stats == stats,
                    FetchSnapshot.raw_sha256 == raw_sha256,
                )
            ).scalar_one_or_none()
            if existing is not None:
                return existing, False

            snapshot = FetchSnapshot(
                symbol=symbol,
                endpoint=endpoint,
                stats=stats,
                raw_sha256=raw_sha256,
                raw_storage_path=raw_storage_path,
                http_status=http_status,
                source=source,
                is_point_in_time=False,
                retrieved_at=retrieved_at or datetime.now(timezone.utc),
            )
            session.add(snapshot)
            session.flush()

            seen: set[tuple[date, str]] = set()
            for fact in facts:
                key = (fact["period_end"], fact["metric"])
                if key in seen:
                    continue
                seen.add(key)
                session.add(
                    FundamentalFact(
                        snapshot_id=snapshot.id,
                        symbol=symbol,
                        endpoint=endpoint,
                        stats=stats,
                        period_end=fact["period_end"],
                        bucket=fact["bucket"],
                        metric=fact["metric"],
                        value=fact.get("value"),
                        raw_value=fact.get("raw_value"),
                    )
                )
            session.commit()
            return snapshot, True
        finally:
            session.close()

    def record_exception(
        self,
        *,
        endpoint: str,
        failure_type: str,
        details: str,
        symbol: str | None = None,
        stats: str = "",
        http_status: int | None = None,
    ) -> None:
        session = self._session()
        try:
            session.add(
                IngestionException(
                    symbol=symbol,
                    endpoint=endpoint,
                    stats=stats,
                    failure_type=failure_type,
                    details=details,
                    http_status=http_status,
                )
            )
            session.commit()
        finally:
            session.close()

    # ----------------------------------------------------------------- cohort

    def save_cohort(self, cohort_id: str, members: Iterable[dict[str, Any]]) -> int:
        session = self._session()
        stored = 0
        try:
            known = {
                s
                for (s,) in session.execute(
                    select(CohortSnapshot.symbol).where(CohortSnapshot.cohort_id == cohort_id)
                ).all()
            }
            for member in members:
                if member["symbol"] in known:
                    continue
                session.add(CohortSnapshot(cohort_id=cohort_id, **member))
                known.add(member["symbol"])
                stored += 1
            session.commit()
            return stored
        finally:
            session.close()

    def cohort_members(self, cohort_id: str) -> list[dict[str, Any]]:
        """Symbol and ISIN, ranked.

        The ISIN matters: the probe established that ``/stock_target_price`` and
        ``/stock_forecasts`` accept an ISIN as their ``stock_id``, so bhavcopy
        already supplies the identifier and no lookup call is needed to get one.
        """
        session = self._session()
        try:
            return [
                {"symbol": symbol, "isin": isin}
                for symbol, isin in session.execute(
                    select(CohortSnapshot.symbol, CohortSnapshot.isin)
                    .where(CohortSnapshot.cohort_id == cohort_id)
                    .order_by(CohortSnapshot.rank)
                ).all()
            ]
        finally:
            session.close()

    def cohort_symbols(self, cohort_id: str) -> list[str]:
        session = self._session()
        try:
            return [
                s
                for (s,) in session.execute(
                    select(CohortSnapshot.symbol)
                    .where(CohortSnapshot.cohort_id == cohort_id)
                    .order_by(CohortSnapshot.rank)
                ).all()
            ]
        finally:
            session.close()

    # --------------------------------------------------------------- reading

    def series(self, symbol: str, stats: str, metric: str | None = None) -> list[dict[str, Any]]:
        """Latest-vintage facts for one symbol/stats, ascending by period.

        Where several vintages carry the same period, the most recently
        retrieved wins — earlier ones stay in the table as the restatement
        record rather than being resolved away at write time.
        """
        session = self._session()
        try:
            stmt = (
                select(
                    FundamentalFact.period_end,
                    FundamentalFact.bucket,
                    FundamentalFact.metric,
                    FundamentalFact.value,
                    FetchSnapshot.retrieved_at,
                )
                .join(FetchSnapshot, FundamentalFact.snapshot_id == FetchSnapshot.id)
                .where(FundamentalFact.symbol == symbol, FundamentalFact.stats == stats)
                .order_by(FundamentalFact.period_end, FetchSnapshot.retrieved_at)
            )
            if metric:
                stmt = stmt.where(FundamentalFact.metric == metric)

            latest: dict[tuple[date, str], dict[str, Any]] = {}
            for period_end, bucket, name, value, retrieved_at in session.execute(stmt).all():
                latest[(period_end, name)] = {
                    "period_end": period_end,
                    "bucket": bucket,
                    "metric": name,
                    "value": value,
                    "retrieved_at": retrieved_at,
                }
            return [latest[k] for k in sorted(latest, key=lambda k: (k[0], k[1]))]
        finally:
            session.close()

    def save_outcomes(
        self, outcomes: Iterable[Any], *, window_start: date, window_end: date
    ) -> int:
        """Replace this window's outcome labels.

        Keyed on (isin, window), so re-running with a different threshold
        updates in place rather than accumulating contradictory labels — unlike
        the fact tables, this is a *derived* view and has no vintage meaning.

        Replace means replace: an ISIN previously stored for this window and
        absent from ``outcomes`` is deleted, not left behind.  A merge that only
        upserts cannot express a *shrinking* universe, and the universe does
        shrink — excluding the 412 ``INF*`` fund/ETF ISINs left exactly that
        many orphans carrying stale labels, which is how this was found.
        """
        from app.analysis.models import DelistingOutcome

        session = self._session()
        stored = 0
        try:
            existing = {
                row.isin: row
                for row in session.execute(
                    select(DelistingOutcome).where(
                        DelistingOutcome.window_start == window_start,
                        DelistingOutcome.window_end == window_end,
                    )
                ).scalars()
            }
            outcomes = list(outcomes)
            incoming = {outcome.isin for outcome in outcomes}
            for isin, row in existing.items():
                if isin not in incoming:
                    session.delete(row)
            for outcome in outcomes:
                row = existing.get(outcome.isin)
                values = {
                    "symbol": outcome.symbol,
                    "first_seen": outcome.first_seen,
                    "last_seen": outcome.last_seen,
                    "months_observed": outcome.months_observed,
                    "gap_months": outcome.gap_months,
                    "last_close": outcome.last_close,
                    "close_12m_before": outcome.close_12m_before,
                    "close_6m_before": outcome.close_6m_before,
                    "return_12m": outcome.return_12m,
                    "return_6m": outcome.return_6m,
                    "peak_close": outcome.peak_close,
                    "drawdown_from_peak": outcome.drawdown_from_peak,
                    "status": outcome.status,
                    "listed_elsewhere": getattr(outcome, "listed_elsewhere", "UNCHECKED"),
                    "notes": outcome.notes,
                }
                if row is None:
                    session.add(
                        DelistingOutcome(
                            isin=outcome.isin,
                            window_start=window_start,
                            window_end=window_end,
                            **values,
                        )
                    )
                    stored += 1
                else:
                    for key, value in values.items():
                        setattr(row, key, value)
            session.commit()
            return stored
        finally:
            session.close()

    def symbols_with_stats(self, stats: str) -> list[str]:
        """Symbols holding at least one stored fact for this vocabulary."""
        session = self._session()
        try:
            return [
                s
                for (s,) in session.execute(
                    select(func.distinct(FundamentalFact.symbol))
                    .where(FundamentalFact.stats == stats)
                    .order_by(FundamentalFact.symbol)
                ).all()
            ]
        finally:
            session.close()

    def coverage_summary(self) -> dict[str, Any]:
        session = self._session()
        try:
            snapshots = int(
                session.execute(select(func.count(FetchSnapshot.id))).scalar_one()
            )
            symbols = int(
                session.execute(
                    select(func.count(func.distinct(FetchSnapshot.symbol)))
                ).scalar_one()
            )
            facts = int(session.execute(select(func.count(FundamentalFact.id))).scalar_one())
            by_endpoint = [
                {"endpoint": e, "stats": st, "symbols": int(n)}
                for e, st, n in session.execute(
                    select(
                        FetchSnapshot.endpoint,
                        FetchSnapshot.stats,
                        func.count(func.distinct(FetchSnapshot.symbol)),
                    ).group_by(FetchSnapshot.endpoint, FetchSnapshot.stats)
                ).all()
            ]
            exceptions = [
                {"failure_type": t, "count": int(n)}
                for t, n in session.execute(
                    select(IngestionException.failure_type, func.count(IngestionException.id))
                    .group_by(IngestionException.failure_type)
                ).all()
            ]
            return {
                "snapshots": snapshots,
                "symbols": symbols,
                "facts": facts,
                "by_endpoint": sorted(by_endpoint, key=lambda r: (r["endpoint"], r["stats"])),
                "exceptions": exceptions,
                "calls_spent_this_period": self.calls_spent(),
            }
        finally:
            session.close()
