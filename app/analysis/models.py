"""Persistence models for the indianapi.in fact store.

These tables are separate from the live signal/position tables and from the
event-research pilot.  Two properties drive the whole design:

**Append-only vintages.**  The source is restated and carries no publication
timestamp, so ``is_point_in_time`` is False and nothing here can measure a
historical edge.  But every fetch is stored with its own ``retrieved_at`` and
never overwrites an earlier one, so the store accumulates its own vintage
history going forward.  After several quarters, any value that moved between
vintages is a visible restatement.  Elapsed time is the only thing that can
produce that record, which is why the collection starts now.

**Failures are rows, not silence.**  A symbol that errors or returns nothing
becomes an :class:`IngestionException`.  Dropping unparseable records would
preferentially delete the companies that are deteriorating — the exact
population the red-flag work is trying to see.
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
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
    Uuid,
)
from sqlalchemy.orm import declarative_base, relationship


AnalysisBase = declarative_base()


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class ApiCallLedger(AnalysisBase):
    """One row per attempted call, whether or not it reached the network.

    The ledger is the budget.  ``cache_hit`` rows cost nothing and exist so a
    re-run is provably free; the non-cache-hit count is what should reconcile
    against the provider's consumed credits.  A drift between the two means
    calls are escaping the client, which is the failure mode that silently
    burns a quota.
    """

    __tablename__ = "api_call_ledger"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    called_at = Column(DateTime(timezone=True), nullable=False, default=_utcnow, index=True)
    endpoint = Column(String, nullable=False, index=True)
    # Credentials are never written here; the client strips them before saving.
    params_json = Column(Text, nullable=False)
    http_status = Column(Integer)
    response_sha256 = Column(String(64))
    response_bytes = Column(Integer)
    cache_hit = Column(Boolean, nullable=False, default=False, index=True)
    # Provider quotas reset monthly, so spend is counted per YYYY-MM.
    budget_period = Column(String, nullable=False, index=True)
    error = Column(Text)


class FetchSnapshot(AnalysisBase):
    """One (symbol, endpoint, fetch) — a vintage, never updated in place."""

    __tablename__ = "fetch_snapshots"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    symbol = Column(String, nullable=False, index=True)
    endpoint = Column(String, nullable=False, index=True)
    # The `stats` discriminator for /historical_stats and /statement; the empty
    # string keeps the uniqueness constraint usable for endpoints without one.
    stats = Column(String, nullable=False, default="")
    retrieved_at = Column(DateTime(timezone=True), nullable=False, default=_utcnow, index=True)
    raw_sha256 = Column(String(64), nullable=False)
    raw_storage_path = Column(Text, nullable=False)
    http_status = Column(Integer, nullable=False)
    source = Column(String, nullable=False, default="indianapi")
    is_point_in_time = Column(Boolean, nullable=False, default=False)

    facts = relationship("FundamentalFact", back_populates="snapshot")

    __table_args__ = (
        UniqueConstraint(
            "symbol", "endpoint", "stats", "raw_sha256",
            name="uq_fetch_snapshot_payload",
        ),
        Index("ix_fetch_snapshot_lookup", "symbol", "endpoint", "stats", "retrieved_at"),
    )


class FundamentalFact(AnalysisBase):
    """Long/EAV facts.

    All seven ``/historical_stats`` vocabularies share one transposed shape —
    ``{metric: {"Jun 2024": value}}`` — differing only in which metric names
    appear.  Storing them as (period, metric, value) triples means a new
    vocabulary needs no migration, and a metric this project has never heard of
    is retained rather than discarded at parse time.

    ``value`` is nullable on purpose: a reported-but-null cell is a different
    fact from an absent one, and only the former proves the period exists.
    """

    __tablename__ = "fundamental_facts"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    snapshot_id = Column(
        Uuid(as_uuid=True), ForeignKey("fetch_snapshots.id"), nullable=False, index=True
    )
    symbol = Column(String, nullable=False, index=True)
    endpoint = Column(String, nullable=False)
    stats = Column(String, nullable=False, default="")
    period_end = Column(Date, nullable=False, index=True)
    # Monotonic calendar-quarter index; a gap in this sequence IS the missing
    # quarter.  Never address quarters by list position.
    bucket = Column(Integer, nullable=False, index=True)
    metric = Column(String, nullable=False, index=True)
    value = Column(Float)
    raw_value = Column(Text)

    snapshot = relationship("FetchSnapshot", back_populates="facts")

    __table_args__ = (
        UniqueConstraint(
            "snapshot_id", "period_end", "metric", name="uq_fundamental_fact_cell"
        ),
        Index("ix_fundamental_fact_series", "symbol", "stats", "metric", "bucket"),
    )


class CohortSnapshot(AnalysisBase):
    """Point-in-time universe membership, reconstructed from NSE bhavcopy.

    Selection uses only what actually traded on or before ``as_of_date``, so
    names that later delisted are included on equal terms.  This is also where
    the red-flag lane gets its outcome labels: a symbol present in an older
    cohort and absent from a newer one stopped trading, with a date.
    """

    __tablename__ = "cohort_snapshots"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cohort_id = Column(String, nullable=False, index=True)
    as_of_date = Column(Date, nullable=False, index=True)
    symbol = Column(String, nullable=False, index=True)
    isin = Column(String)
    rank = Column(Integer, nullable=False)
    avg_daily_value_60d = Column(Float)
    sessions_traded = Column(Integer)
    selection_reason = Column(String, nullable=False)
    source_url = Column(Text)
    created_at = Column(DateTime(timezone=True), nullable=False, default=_utcnow)

    __table_args__ = (
        UniqueConstraint("cohort_id", "symbol", name="uq_cohort_snapshot_member"),
    )


class DelistingOutcome(AnalysisBase):
    """Per-ISIN exit record derived from bhavcopy alone.

    This is the **outcome** side of the dataset, and it exists because the
    vendor feed cannot supply it: indianapi stops returning a dead company
    silently and undated, so a model trained only on it would never see a
    single failure.

    The classification deliberately does not read a delisting *reason*.  A
    merger at a premium and a bankruptcy both remove a ticker but are opposite
    outcomes to hold, and the price path into the last trade discriminates them
    directly — it measures what an owner experienced rather than the legal
    category.  Raw inputs are stored alongside the label so a later screen can
    re-threshold without re-deriving anything.
    """

    __tablename__ = "delisting_outcomes"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    isin = Column(String, nullable=False, index=True)
    symbol = Column(String, nullable=False, index=True)
    window_start = Column(Date, nullable=False)
    window_end = Column(Date, nullable=False)
    first_seen = Column(Date, nullable=False)
    last_seen = Column(Date, nullable=False, index=True)
    months_observed = Column(Integer, nullable=False)
    # A name can vanish and return; a gap is a suspension, not a death.
    gap_months = Column(Integer, nullable=False, default=0)
    last_close = Column(Float)
    close_12m_before = Column(Float)
    close_6m_before = Column(Float)
    return_12m = Column(Float)
    return_6m = Column(Float)
    peak_close = Column(Float)
    drawdown_from_peak = Column(Float)
    status = Column(String, nullable=False, index=True)
    # Whether the instrument still trades elsewhere (BSE).  Deliberately NOT
    # folded into `status`: "what a holder experienced" and "did the instrument
    # stop existing" are independent facts that disagree for 111 of the 231
    # collapses.  Charter amendment v2 §4 defines delisted as absent from both.
    listed_elsewhere = Column(String, nullable=False, default="UNCHECKED", index=True)
    notes = Column(Text, nullable=False, default="")
    computed_at = Column(DateTime(timezone=True), nullable=False, default=_utcnow)

    __table_args__ = (
        UniqueConstraint("isin", "window_start", "window_end", name="uq_delisting_outcome"),
    )


class IngestionException(AnalysisBase):
    """A fetch or parse that did not yield facts, kept as evidence."""

    __tablename__ = "ingestion_exceptions"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    symbol = Column(String, index=True)
    endpoint = Column(String, nullable=False)
    stats = Column(String, nullable=False, default="")
    failure_type = Column(String, nullable=False, index=True)
    http_status = Column(Integer)
    details = Column(Text, nullable=False)
    disposition = Column(String, nullable=False, default="OPEN")
    created_at = Column(DateTime(timezone=True), nullable=False, default=_utcnow)
