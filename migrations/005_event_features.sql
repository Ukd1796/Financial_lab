-- Phase-2 derived features for the V2 earnings-response sleeve.
--
-- Charter §5 specified `event_feature_snapshot` in the Phase-1 data contract but
-- it was never built, because Phase 1 computed no surprise or response.  This is
-- that table.
--
-- It is append-only by design: `feature_version` plus `computed_at` mean a
-- recomputation writes a NEW row rather than updating one, so a past run stays
-- replayable.  This is the same lesson as the delisting labels, where an
-- upsert-only write could not express a shrinking universe and quietly served a
-- stale answer -- here the risk is a feature definition changing underneath a
-- result that was already reported.
--
-- Nothing in this table is a trading instruction.  It records what was knowable
-- at `available_at` and what the frozen rules made of it.

CREATE TABLE IF NOT EXISTS event_feature_snapshots (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  event_id UUID NOT NULL REFERENCES financial_result_events(id),

  -- Replay identity.  Charter §5: "permits exact replay and a complete audit trail".
  feature_version TEXT NOT NULL,
  computed_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

  -- The year-ago filing this surprise was chained from.  226 of 226 filings
  -- define no prior-year context, so the comparative can only come from a
  -- second separately-ingested filing -- and which one must be recoverable.
  prior_event_id UUID REFERENCES financial_result_events(id),

  -- Signal, per charter §3: seasonally differenced EPS, standardised on the
  -- issuer's own prior seasonal differences only.
  eps_current DOUBLE PRECISION,
  eps_year_ago DOUBLE PRECISION,
  surprise_raw DOUBLE PRECISION,     -- EPS_q - EPS_q-4, in rupees
  surprise_scaled DOUBLE PRECISION,  -- the same, divided by price at available_at
  -- Both standardisations are stored for every event, not only the one the
  -- frozen rule chose.  Fold A reaches at most 4 prior seasonal differences
  -- while fold B reaches 5-8, so the hybrid rule resolves to a different
  -- method in each fold; keeping both columns is what makes that confound
  -- visible when §7 condition 2 compares the folds.
  surprise_standardised DOUBLE PRECISION,
  surprise_std_time_series DOUBLE PRECISION,
  surprise_std_cross_sectional DOUBLE PRECISION,
  surprise_method TEXT,              -- TIME_SERIES | CROSS_SECTIONAL
  surprise_history_n INTEGER,

  -- The frozen clock (charter §2).  Stored as resolved sessions, not derived at
  -- read time, so a calendar change cannot retroactively move a past entry.
  available_at TIMESTAMPTZ,
  reaction_session DATE,
  entry_session DATE,
  exit_session DATE,

  -- Initial response and the 20-session outcome, both peer-adjusted.
  response_raw DOUBLE PRECISION,
  response_peer_adjusted DOUBLE PRECISION,
  forward_return_raw DOUBLE PRECISION,
  forward_return_peer_adjusted DOUBLE PRECISION,

  -- Charter §6 benchmark-leakage gate: "every event records the benchmark used".
  benchmark_rule TEXT,
  benchmark_peer_isins TEXT,
  benchmark_response_return DOUBLE PRECISION,
  benchmark_forward_return DOUBLE PRECISION,

  -- Liquidity/cost admissibility (charter v3 §3): an event that cannot be
  -- filled inside the 1%-of-ADV participation cap is excluded before returns
  -- are aggregated, and the exclusion is counted rather than silent.
  adv_60d DOUBLE PRECISION,
  participation_ok BOOLEAN,

  cohort_id TEXT,
  cohort_as_of DATE,
  fold_label TEXT,
  eligibility_decision TEXT NOT NULL,
  eligibility_reason TEXT NOT NULL,

  CONSTRAINT uq_event_feature_version UNIQUE (event_id, feature_version)
);

CREATE INDEX IF NOT EXISTS idx_event_feature_fold
  ON event_feature_snapshots (feature_version, fold_label);
CREATE INDEX IF NOT EXISTS idx_event_feature_decision
  ON event_feature_snapshots (feature_version, eligibility_decision);

-- One row per fold-B (and fold-C) evaluation, so charter v3 §7's "run exactly
-- once" is enforced by a uniqueness constraint rather than by memory.
CREATE TABLE IF NOT EXISTS fold_evaluation_runs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  fold_label TEXT NOT NULL,
  feature_version TEXT NOT NULL,
  charter_version TEXT NOT NULL,
  ran_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  result_summary TEXT NOT NULL,
  override_reason TEXT,
  CONSTRAINT uq_fold_evaluation UNIQUE (fold_label, feature_version)
);
