"""Persistence models for the Phase-1 earnings-event data audit.

These tables intentionally do not share the live signal/position tables.  A
research event is immutable: later corrections are linked to, never written
over, the original filing.
"""

import uuid
from datetime import datetime, timezone

from sqlalchemy import (
    Boolean,
    Column,
    Date,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
    Uuid,
)
from sqlalchemy.orm import declarative_base, relationship


EventResearchBase = declarative_base()


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class EventResearchInstrument(EventResearchBase):
    __tablename__ = "event_research_instruments"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    isin = Column(String, nullable=False, index=True)
    nse_symbol = Column(String, nullable=False, index=True)
    issuer_name = Column(String, nullable=False)
    valid_from = Column(Date, nullable=False)
    valid_to = Column(Date)
    source_url = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, default=_utcnow)

    __table_args__ = (
        UniqueConstraint("isin", "valid_from", name="uq_event_research_instrument_version"),
    )


class FinancialResultEvent(EventResearchBase):
    __tablename__ = "financial_result_events"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    instrument_id = Column(
        Uuid(as_uuid=True), ForeignKey("event_research_instruments.id"), nullable=False, index=True
    )
    result_period_end = Column(Date, nullable=False, index=True)
    fiscal_quarter = Column(String, nullable=False)
    source_exchange = Column(String, nullable=False)
    source_url = Column(Text, nullable=False)
    source_sha256 = Column(String(64), nullable=False, unique=True)
    raw_storage_path = Column(Text, nullable=False)
    source_format = Column(String, nullable=False)
    received_at = Column(DateTime(timezone=True))
    disseminated_at = Column(DateTime(timezone=True), nullable=False, index=True)
    available_at = Column(DateTime(timezone=True), nullable=False, index=True)
    is_revision = Column(Boolean, nullable=False, default=False)
    supersedes_event_id = Column(Uuid(as_uuid=True), ForeignKey("financial_result_events.id"))
    ingested_at = Column(DateTime(timezone=True), nullable=False, default=_utcnow)

    instrument = relationship("EventResearchInstrument")
    facts = relationship("FinancialResultFact", back_populates="event", uselist=False)


class FinancialResultFact(EventResearchBase):
    __tablename__ = "financial_result_facts"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    event_id = Column(
        Uuid(as_uuid=True), ForeignKey("financial_result_events.id"), nullable=False, unique=True
    )
    reporting_scope = Column(String, nullable=False)  # consolidated | standalone
    is_cumulative = Column(Boolean, nullable=False)
    audit_status = Column(String, nullable=False)
    basic_eps = Column(Float)
    diluted_eps = Column(Float)
    revenue = Column(Float)
    operating_profit = Column(Float)
    profit_after_tax = Column(Float)
    currency = Column(String, nullable=False, default="INR")
    unit_scale = Column(String, nullable=False, default="UNKNOWN")
    parser_version = Column(String, nullable=False)
    validation_status = Column(String, nullable=False)
    validation_notes = Column(Text)

    event = relationship("FinancialResultEvent", back_populates="facts")


class EligibleUniverseSnapshot(EventResearchBase):
    __tablename__ = "eligible_universe_snapshots"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cohort_id = Column(String, nullable=False)
    as_of_date = Column(Date, nullable=False, index=True)
    isin = Column(String, nullable=False, index=True)
    nse_symbol = Column(String, nullable=False)
    sector = Column(String)
    selection_reason = Column(String, nullable=False)
    source_url = Column(Text, nullable=False)
    avg_daily_value_20d = Column(Float)
    avg_daily_value_60d = Column(Float)
    listing_status = Column(String, nullable=False, default="ACTIVE")
    source_hash = Column(String(64))
    created_at = Column(DateTime(timezone=True), nullable=False, default=_utcnow)

    __table_args__ = (
        UniqueConstraint("cohort_id", "as_of_date", "isin", name="uq_event_universe_snapshot"),
    )


class EventFeatureSnapshot(EventResearchBase):
    """One frozen-rule evaluation of one filing.

    Append-only: a recomputation writes a new `feature_version` rather than
    updating a row, so a result that was already reported stays replayable.
    Charter §5 calls for exactly this ("permits exact replay and a complete
    audit trail"); it was specified in Phase 1 and never built.
    """

    __tablename__ = "event_feature_snapshots"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    event_id = Column(
        Uuid(as_uuid=True), ForeignKey("financial_result_events.id"), nullable=False, index=True
    )
    feature_version = Column(String, nullable=False, index=True)
    computed_at = Column(DateTime(timezone=True), nullable=False, default=_utcnow)

    # The year-ago filing the seasonal surprise was chained from; no filing
    # carries its own prior-year comparative, so this link is the audit trail.
    prior_event_id = Column(Uuid(as_uuid=True), ForeignKey("financial_result_events.id"))

    eps_current = Column(Float)
    eps_year_ago = Column(Float)
    surprise_raw = Column(Float)          # EPS_q - EPS_q-4, in rupees
    surprise_scaled = Column(Float)       # the same, divided by price at available_at
    # Both standardisations are stored for every event, not just the one the
    # frozen rule selected.  Fold A can only reach 0-4 prior seasonal
    # differences while fold B reaches 5-8, so the hybrid rule uses a different
    # method in each -- storing both is what keeps that confound visible when
    # the folds are compared, instead of buried inside one column.
    surprise_standardised = Column(Float)      # the value the frozen rule used
    surprise_std_time_series = Column(Float)   # NULL when history is too short
    surprise_std_cross_sectional = Column(Float)
    surprise_method = Column(String)           # TIME_SERIES | CROSS_SECTIONAL
    surprise_history_n = Column(Integer)

    available_at = Column(DateTime(timezone=True))
    reaction_session = Column(Date)
    entry_session = Column(Date)
    exit_session = Column(Date)

    response_raw = Column(Float)
    response_peer_adjusted = Column(Float)
    forward_return_raw = Column(Float)
    forward_return_peer_adjusted = Column(Float)

    benchmark_rule = Column(String)
    benchmark_peer_isins = Column(Text)
    benchmark_response_return = Column(Float)
    benchmark_forward_return = Column(Float)

    adv_60d = Column(Float)
    participation_ok = Column(Boolean)

    cohort_id = Column(String)
    cohort_as_of = Column(Date)
    fold_label = Column(String, index=True)
    eligibility_decision = Column(String, nullable=False)
    eligibility_reason = Column(Text, nullable=False)

    __table_args__ = (
        UniqueConstraint("event_id", "feature_version", name="uq_event_feature_version"),
    )


class FoldEvaluationRun(EventResearchBase):
    """A record that a fold was evaluated, so "exactly once" is enforceable.

    Charter v3 §7 requires fold B to be run once.  A uniqueness constraint on
    (fold_label, feature_version) makes a second run fail loudly instead of
    depending on anyone remembering.
    """

    __tablename__ = "fold_evaluation_runs"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    fold_label = Column(String, nullable=False)
    feature_version = Column(String, nullable=False)
    charter_version = Column(String, nullable=False)
    ran_at = Column(DateTime(timezone=True), nullable=False, default=_utcnow)
    result_summary = Column(Text, nullable=False)
    override_reason = Column(Text)

    __table_args__ = (
        UniqueConstraint("fold_label", "feature_version", name="uq_fold_evaluation"),
    )


class EventDataException(EventResearchBase):
    __tablename__ = "event_data_exceptions"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_url = Column(Text)
    event_id = Column(Uuid(as_uuid=True), ForeignKey("financial_result_events.id"))
    exception_type = Column(String, nullable=False)
    disposition = Column(String, nullable=False, default="OPEN")
    details = Column(Text, nullable=False)
    reviewer = Column(String)
    created_at = Column(DateTime(timezone=True), nullable=False, default=_utcnow)
