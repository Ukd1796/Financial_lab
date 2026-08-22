-- Phase-1 V2 research data only.  Do not run this against production until the
-- historical-source audit has passed.  It does not alter any live trading table.

CREATE TABLE IF NOT EXISTS event_research_instruments (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  isin TEXT NOT NULL,
  nse_symbol TEXT NOT NULL,
  issuer_name TEXT NOT NULL,
  valid_from DATE NOT NULL,
  valid_to DATE,
  source_url TEXT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  CONSTRAINT uq_event_research_instrument_version UNIQUE (isin, valid_from)
);

CREATE TABLE IF NOT EXISTS financial_result_events (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  instrument_id UUID NOT NULL REFERENCES event_research_instruments(id),
  result_period_end DATE NOT NULL,
  fiscal_quarter TEXT NOT NULL,
  source_exchange TEXT NOT NULL,
  source_url TEXT NOT NULL,
  source_sha256 CHAR(64) NOT NULL UNIQUE,
  raw_storage_path TEXT NOT NULL,
  source_format TEXT NOT NULL,
  received_at TIMESTAMPTZ,
  disseminated_at TIMESTAMPTZ NOT NULL,
  available_at TIMESTAMPTZ NOT NULL,
  is_revision BOOLEAN NOT NULL DEFAULT FALSE,
  supersedes_event_id UUID REFERENCES financial_result_events(id),
  ingested_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_financial_result_events_instrument_time
  ON financial_result_events (instrument_id, disseminated_at);

CREATE TABLE IF NOT EXISTS financial_result_facts (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  event_id UUID NOT NULL UNIQUE REFERENCES financial_result_events(id),
  reporting_scope TEXT NOT NULL,
  is_cumulative BOOLEAN NOT NULL,
  audit_status TEXT NOT NULL,
  basic_eps DOUBLE PRECISION,
  diluted_eps DOUBLE PRECISION,
  revenue DOUBLE PRECISION,
  operating_profit DOUBLE PRECISION,
  profit_after_tax DOUBLE PRECISION,
  currency TEXT NOT NULL DEFAULT 'INR',
  unit_scale TEXT NOT NULL DEFAULT 'UNKNOWN',
  parser_version TEXT NOT NULL,
  validation_status TEXT NOT NULL,
  validation_notes TEXT
);

CREATE TABLE IF NOT EXISTS eligible_universe_snapshots (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  cohort_id TEXT NOT NULL,
  as_of_date DATE NOT NULL,
  isin TEXT NOT NULL,
  nse_symbol TEXT NOT NULL,
  sector TEXT,
  selection_reason TEXT NOT NULL,
  source_url TEXT NOT NULL,
  avg_daily_value_20d DOUBLE PRECISION,
  avg_daily_value_60d DOUBLE PRECISION,
  listing_status TEXT NOT NULL DEFAULT 'ACTIVE',
  source_hash CHAR(64),
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  CONSTRAINT uq_event_universe_snapshot UNIQUE (cohort_id, as_of_date, isin)
);

CREATE TABLE IF NOT EXISTS event_data_exceptions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  source_url TEXT,
  event_id UUID REFERENCES financial_result_events(id),
  exception_type TEXT NOT NULL,
  disposition TEXT NOT NULL DEFAULT 'OPEN',
  details TEXT NOT NULL,
  reviewer TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
