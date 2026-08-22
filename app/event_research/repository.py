"""Repository for immutable Phase-1 event-research records."""

from __future__ import annotations

from datetime import date
from typing import Any

from sqlalchemy import case, func, select

from app.event_research.database import new_session
from app.event_research.models import (
    EligibleUniverseSnapshot,
    EventDataException,
    EventResearchInstrument,
    FinancialResultEvent,
    FinancialResultFact,
)


class EventResearchRepository:
    def __init__(self, database_url: str | None = None):
        self.database_url = database_url

    def _session(self):
        return new_session(self.database_url)

    def import_validated_filing(self, normalized: dict[str, Any]) -> tuple[FinancialResultEvent, bool]:
        """Persist one validated original filing. Existing source hashes are no-ops."""
        event_data = normalized["event"]
        fact_data = normalized["facts"]
        session = self._session()
        try:
            existing = session.execute(
                select(FinancialResultEvent).where(
                    FinancialResultEvent.source_sha256 == event_data["raw_sha256"]
                )
            ).scalar_one_or_none()
            if existing:
                return existing, False

            supersedes_event_id = None
            supersedes_hash = event_data.get("supersedes_source_sha256")
            if supersedes_hash:
                superseded = session.execute(
                    select(FinancialResultEvent).where(
                        FinancialResultEvent.source_sha256 == supersedes_hash
                    )
                ).scalar_one_or_none()
                if superseded is None:
                    raise ValueError("Revision predecessor has not been imported")
                supersedes_event_id = superseded.id

            valid_from = date.fromisoformat(str(event_data["instrument_valid_from"]))
            instrument = session.execute(
                select(EventResearchInstrument).where(
                    EventResearchInstrument.isin == event_data["isin"],
                    EventResearchInstrument.valid_from == valid_from,
                )
            ).scalar_one_or_none()
            if instrument is None:
                instrument = EventResearchInstrument(
                    isin=event_data["isin"],
                    nse_symbol=event_data["nse_symbol"],
                    issuer_name=event_data["issuer_name"],
                    valid_from=valid_from,
                    source_url=event_data["instrument_source_url"],
                )
                session.add(instrument)
                session.flush()

            event = FinancialResultEvent(
                instrument_id=instrument.id,
                result_period_end=event_data["result_period_end"],
                fiscal_quarter=event_data["fiscal_quarter"],
                source_exchange=event_data["source_exchange"],
                source_url=event_data["source_url"],
                source_sha256=event_data["raw_sha256"],
                raw_storage_path=event_data["raw_storage_path"],
                source_format=event_data["source_format"],
                received_at=event_data["received_at"],
                disseminated_at=event_data["disseminated_at"],
                available_at=event_data["available_at"],
                is_revision=event_data["is_revision"],
                supersedes_event_id=supersedes_event_id,
            )
            session.add(event)
            session.flush()
            session.add(FinancialResultFact(event_id=event.id, **fact_data))
            session.commit()
            return event, True
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def record_exception(self, *, source_url: str | None, exception_type: str, details: str) -> None:
        session = self._session()
        try:
            session.add(EventDataException(
                source_url=source_url, exception_type=exception_type, details=details
            ))
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def coverage_summary(self, cohort_id: str | None = None) -> dict[str, Any]:
        """Report what was captured and what could not be proved.

        Coverage is reported before any outcome is computed, and the primary
        study subset (consolidated, non-cumulative) is counted separately so a
        parse failure concentrated in one year or one issuer is visible rather
        than silently shrinking the sample.
        """
        session = self._session()
        # The primary EPS study can only use an original consolidated,
        # non-cumulative filing whose facts were proved from the document.
        primary_subset = (
            (FinancialResultFact.reporting_scope == "consolidated")
            & (FinancialResultFact.is_cumulative.is_(False))
            & (FinancialResultEvent.is_revision.is_(False))
        )
        try:
            year = func.extract("year", FinancialResultEvent.disseminated_at).label("year")
            by_year = session.execute(
                select(
                    year,
                    func.count(FinancialResultEvent.id).label("events"),
                    func.count(FinancialResultFact.basic_eps).label("with_basic_eps"),
                    func.sum(case((primary_subset, 1), else_=0)).label("primary_eligible"),
                    func.sum(
                        case((primary_subset & FinancialResultFact.basic_eps.isnot(None), 1), else_=0)
                    ).label("primary_with_eps"),
                    func.sum(
                        case((FinancialResultEvent.available_at.is_(None), 1), else_=0)
                    ).label("missing_available_at"),
                )
                .join(FinancialResultFact, FinancialResultFact.event_id == FinancialResultEvent.id)
                .group_by("year")
                .order_by("year")
            ).all()

            by_status = session.execute(
                select(
                    year,
                    FinancialResultFact.validation_status,
                    func.count(FinancialResultEvent.id),
                )
                .join(FinancialResultFact, FinancialResultFact.event_id == FinancialResultEvent.id)
                .group_by("year", FinancialResultFact.validation_status)
                .order_by("year")
            ).all()
            status_by_year: dict[int, dict[str, int]] = {}
            for row_year, status, count in by_status:
                status_by_year.setdefault(int(row_year), {})[status] = count

            by_issuer = session.execute(
                select(
                    EventResearchInstrument.nse_symbol,
                    EventResearchInstrument.isin,
                    func.count(FinancialResultEvent.id).label("events"),
                    func.sum(
                        case((primary_subset & FinancialResultFact.basic_eps.isnot(None), 1), else_=0)
                    ).label("primary_with_eps"),
                )
                .join(FinancialResultEvent, FinancialResultEvent.instrument_id == EventResearchInstrument.id)
                .join(FinancialResultFact, FinancialResultFact.event_id == FinancialResultEvent.id)
                .group_by(EventResearchInstrument.isin, EventResearchInstrument.nse_symbol)
                .order_by(EventResearchInstrument.nse_symbol)
            ).all()

            exceptions_by_type = session.execute(
                select(EventDataException.exception_type, func.count(EventDataException.id))
                .group_by(EventDataException.exception_type)
                .order_by(EventDataException.exception_type)
            ).all()

            cohort_members = 0
            if cohort_id:
                cohort_members = session.execute(
                    select(func.count(func.distinct(EligibleUniverseSnapshot.isin)))
                    .where(EligibleUniverseSnapshot.cohort_id == cohort_id)
                ).scalar_one()
            event_count, issuer_count = session.execute(
                select(
                    func.count(FinancialResultEvent.id),
                    func.count(func.distinct(EventResearchInstrument.isin)),
                )
                .join(EventResearchInstrument, EventResearchInstrument.id == FinancialResultEvent.instrument_id)
            ).one()
            exception_count = session.execute(select(func.count(EventDataException.id))).scalar_one()
            return {
                "events": event_count,
                "issuers_with_events": issuer_count,
                "cohort_members": cohort_members or None,
                "cohort_members_without_events": (
                    cohort_members - issuer_count if cohort_id else None
                ),
                "exceptions": exception_count,
                "exceptions_by_type": {name: count for name, count in exceptions_by_type},
                "by_year": [
                    {
                        "year": int(row.year),
                        "events": row.events,
                        "with_basic_eps": row.with_basic_eps,
                        "primary_eligible": int(row.primary_eligible or 0),
                        "primary_with_eps": int(row.primary_with_eps or 0),
                        "missing_available_at": int(row.missing_available_at or 0),
                        "validation_status": status_by_year.get(int(row.year), {}),
                    }
                    for row in by_year
                ],
                "by_issuer": [
                    {
                        "nse_symbol": row.nse_symbol,
                        "isin": row.isin,
                        "events": row.events,
                        "primary_with_eps": int(row.primary_with_eps or 0),
                    }
                    for row in by_issuer
                ],
            }
        finally:
            session.close()

    def import_universe_member(self, row: dict[str, Any]) -> bool:
        """Store an ex-ante pilot-cohort member; current lists must not be substituted."""
        session = self._session()
        try:
            existing = session.execute(
                select(EligibleUniverseSnapshot).where(
                    EligibleUniverseSnapshot.cohort_id == row["cohort_id"],
                    EligibleUniverseSnapshot.as_of_date == row["as_of_date"],
                    EligibleUniverseSnapshot.isin == row["isin"],
                )
            ).scalar_one_or_none()
            if existing:
                return False
            session.add(EligibleUniverseSnapshot(**row))
            session.commit()
            return True
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
