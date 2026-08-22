# V2 Event Pilot — Operator Workflow

This is the Phase-1 data audit only. It stores a result filing exactly as it
was available, and reports coverage. It does not calculate a score, forward
return, order, or backtest result.

The local default database is `data/event_research/event_research.sqlite`; raw
documents go to `data/event_research/raw/`. Both are ignored by Git. The pilot
does not use `DATABASE_URL` or touch the live/paper database.

## 1. Create the isolated store

```bash
finance/bin/python3 -m scripts.event_research.init_research_db
```

Do not run `migrations/004_event_research.sql` against Supabase for this
pilot. It exists only for a later, explicit move to a dedicated Postgres
research database.

## 2. Create the dated cohort manifest

```bash
finance/bin/python3 -m scripts.event_research.create_pilot_manifest \
  --output data/event_research/pilot_manifest.csv
```

Fill the CSV from one archived NSE index report dated before the pilot's
research interval. Use 20 liquid, non-financial issuers for the initial audit.
Every row requires its ISIN, NSE symbol, the report's `as_of_date`, a sector,
and the original report URL. Do not copy the current Nifty 150/500 list.

First check it without writing:

```bash
finance/bin/python3 -m scripts.event_research.import_pilot_manifest \
  --manifest data/event_research/pilot_manifest.csv
```

After downloading the original cohort report locally, persist the immutable
snapshot and its file hash:

```bash
finance/bin/python3 -m scripts.event_research.import_pilot_manifest \
  --manifest data/event_research/pilot_manifest.csv \
  --source-file /path/to/original-nse-cohort-report.pdf --commit
```

## 3. Import a financial-result filing

Download the original NSE XBRL or attachment first. Build one JSON payload
from the filing itself; this is an example shape, not market data:

```json
{
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
    "is_revision": false
  },
  "facts": {
    "reporting_scope": "consolidated",
    "is_cumulative": false,
    "audit_status": "UNAUDITED",
    "basic_eps": 12.5,
    "revenue": 1000.0,
    "operating_profit": 180.0,
    "profit_after_tax": 120.0,
    "currency": "INR",
    "unit_scale": "CRORE"
  }
}
```

Always dry-run first:

```bash
finance/bin/python3 -m scripts.event_research.import_filing \
  --payload /path/to/filing.json --raw-file /path/to/original-filing.html
```

Only after checking the source URL, timestamp, scope, cumulative flag and
numeric values should the record be committed:

```bash
finance/bin/python3 -m scripts.event_research.import_filing \
  --payload /path/to/filing.json --raw-file /path/to/original-filing.html --commit
```

The commit writes a SHA-256-named copy of the raw filing. An identical document
is a no-op. A revision needs `is_revision: true` and the already-imported
original filing's `supersedes_source_sha256`; the original is never overwritten.

## 4. Audit coverage, not performance

```bash
finance/bin/python3 -m scripts.event_research.coverage_report
```

The target report contains only event/issuer counts, EPS completeness and
exceptions by year. Stop and fix coverage, identity or timestamp failures
before writing a return study. The full no-bias rules and pre-registered
decision standard are in [v2_event_research_charter.md](v2_event_research_charter.md).

---

## Corpus build run — 2026-08-22

The run that takes the corpus from "fold A INCONCLUSIVE by construction, folds
B and C empty" to a decidable state. Recorded here because it is long, staged,
and the last attempt failed silently.

### What is running

| | Stage | Command | Log |
|---|---|---|---|
| 1 | Integrated fetch, 2025-01-01 → 2026-08-14, all 597 cohort issuers | `fetch_cohort_integrated_filings --cohort-id <13 cohorts> --from 2025-01-01 --to 2026-08-14 --commit` | `data/event_research/integrated_20260822_213729.log` |
| 2 | Backwards extension — fold A's missing 2022 comparatives | `extend_backwards.sh --commit` | `data/event_research/extend_*.log` |
| 3 | Re-parse the whole corpus under one convention | `reparse_corpus.py --resolve-conventions --commit` | chain log |
| 4 | Rebuild event features (signal-blind) | `build_event_features.py --commit` | chain log |

Stages 2–4 are driven by `run_overnight_chain.sh`, launched at 21:54 while
stage 1 was still running. It waits stage 1 out, then verifies it ingested
before continuing. Chain log: `data/event_research/chain_20260822_215413.log`.
Corpus at chain start: **7,774 filings**.

Both are wrapped in `caffeinate -dimsu`, which does **not** survive a lid
close. Leave the lid open. Every stage resumes, so an interruption costs
elapsed time and nothing else.

### Watching it

```bash
# stage 1 progress (597 issuers indexed, then documents downloaded)
grep -c 'filings,' data/event_research/integrated_20260822_213729.log

# where the chain is
tail -5 data/event_research/chain_20260822_215413.log

# did the corpus actually grow?  this is the question that matters
finance/bin/python3 -c "import sqlite3;d=sqlite3.connect('data/event_research/event_research.sqlite');\
print(d.execute(\"SELECT COUNT(*) FROM financial_result_events\").fetchone()[0])"

# anything being rejected today, and under what name
finance/bin/python3 -c "import sqlite3;d=sqlite3.connect('data/event_research/event_research.sqlite');\
print([r for r in d.execute(\"SELECT exception_type,COUNT(*) FROM event_data_exceptions \
WHERE created_at>=date('now') GROUP BY 1\")])"
```

### What it does NOT do

It computes no surprise, response, forward return or fold verdict. Fetching is
signal-blind and spends none of the pre-registration — charter v3 §7 gates
*evaluation*, not ingestion. **`run_fold --fold A` is run by hand, afterwards,
and only once the sufficiency floor is actually met.** Fold B stays untouched
until A is decided; its single pass is enforced by a database constraint, not
by discipline.

### The failure mode this run is built around

The 2026-08-18 attempt reported no error and produced nothing: 3,127 filings
fetched, 0 stored, each logged under a plausible-sounding name. Stage 1's
ingest is now asserted before stages 2–4 run, and a fetch stage that stores
nothing aborts the chain. **If this run ends quietly, check the corpus count
before believing it.**
