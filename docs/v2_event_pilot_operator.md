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
