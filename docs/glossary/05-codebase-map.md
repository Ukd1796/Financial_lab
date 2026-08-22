# 05 — Codebase map: which module owns which concept

Where each glossary concept actually lives. Paths are relative to the repo root.

## `app/event_research/` — the point-in-time filing lane

The only source admissible for measuring a historical edge.

| File | Owns |
|---|---|
| `nse_client.py` | Fetching the filing index and XBRL documents from NSE |
| `xbrl_parser.py` | XBRL → facts. Context resolution, the `OneD`/`FourD` defect, validation statuses |
| `models.py` | `financial_result_events`, `financial_result_facts`, `event_data_exceptions` |
| `repository.py` | Persistence. Append-only; revisions supersede rather than overwrite |
| `database.py` | Isolated SQLite at `data/event_research/event_research.sqlite` |
| `validation.py` | Pre-storage integrity checks |

**Deliberately isolated** from the production/paper database. Research work cannot
touch live trading state.

Current contents: 663 events, 226 `VALID`, 467 exceptions, across a 20-issuer pilot
cohort. See file 02 for why the pre-2023 rows are unusable.

## `app/analysis/` — the vendor and survivorship lane

Everything here is `is_point_in_time=False` except the bhavcopy-derived work.

| File | Owns |
|---|---|
| `indianapi_client.py` | Vendor HTTP client. Budget cap, disk cache, 1.05 s pacing, per-call ledger |
| `delisting.py` | Bhavcopy fetching, UDiFF normalisation, delisting/collapse labels |
| `fundamentals.py` | Vendor fundamentals, quarter addressing by calendar bucket |
| `metrics.py` | Derived measures. Returns a status plus its inputs, never a bare number |
| `sources.py` | Source registry with PIT flags |
| `repository.py` / `models.py` / `database.py` | Persistence to `data/analysis/analysis.sqlite` |

Two design choices worth noting as an engineer:

**The budget cap is mutation-tested.** A test deliberately removes the check and asserts
the suite fails. A spend limit that isn't tested is decoration — and the free tier is
500 calls total, of which **298 are already spent**.

**Metrics return status + inputs, not numbers.** `UNDEFINED_BASE` rather than a
nonsense percentage; `HAS_GAPS` rather than a quietly-interpolated series. Nothing is
imputed. This directly encodes the file 04 lesson: a silent default becomes a fake
signal downstream.

## `scripts/event_research/` — filing lane operations

| Script | Does |
|---|---|
| `init_research_db.py` | Create the isolated store |
| `build_pilot_cohort.py` | Reconstruct a PIT cohort from bhavcopy turnover |
| `fetch_cohort_filings.py` | Pull filings for a cohort over a window |
| `import_filing.py` | Import one filing. Dry-run by default; `--commit` to write |
| `coverage_report.py` | Coverage, completeness and exceptions — **no returns** |
| `probe_comparative_context.py` | Day-0 probe: is the year-ago figure inside the filing? (answer: no) |

## `scripts/analysis/` — vendor and survivorship operations

| Script | Does |
|---|---|
| `probe_schema.py` | Endpoint discovery, enum recovery via deliberate 422s |
| `build_cohort.py` | Build the 500-name liquidity cohort |
| `build_delisting_labels.py` | The 3,411-ISIN survivorship study |
| `probe_survivorship.py` | Does the vendor cover companies that died? (95% — yes) |
| `backfill.py` | Bulk vendor fundamentals fetch — **not yet run** |

## Data on disk

```
data/
├── event_research/
│   ├── event_research.sqlite     663 events, 226 VALID
│   └── raw/                      SHA-256-named original filings (immutable)
└── analysis/
    ├── analysis.sqlite           3,411 delisting labels, 500-name cohort
    ├── bhavcopy/                 159 MONTH-END files ← daily is the gap
    └── raw/                      cached vendor responses

data_cache/market_ohlc.sqlite     150 symbols — V1's universe, NOT usable for V2
```

Raw documents are stored **content-addressed by SHA-256**. Re-importing an identical
document is a no-op; a changed one cannot silently overwrite its predecessor. This is
what makes "as-filed" a verifiable claim rather than an assertion.

## Conventions worth knowing before you edit

**Always `finance/bin/python3`**, never system python. Scripts run as modules:
`finance/bin/python3 -m scripts.event_research.coverage_report`.

**Dry-run first.** Import scripts default to dry-run and require `--commit` to write.

**`api/` is off-limits during research.** That directory is the deployed FastAPI and
cron layer; production wiring is handled separately.

**`PYTHONHASHSEED=0`** for anything comparing backtest runs — set ordering leaks into
results otherwise.

## What is NOT built

Being explicit, since it's the actual roadmap:

| Missing | Blocks |
|---|---|
| **Sector labels** | §3 sector adjustment, §8's 40%-per-sector cap. Needs the paid vendor tier |
| **Price stitching across ISIN changes** | a split splits the price series in two; the adjustment ratio is known, the series are not yet joined |
| **Surprise / response / return computation** | everything — none of it has been written |
| **Scope convention** (standalone vs consolidated) | a decision, not code: every company-quarter currently yields both |

Built since this file was first written: the daily price panel
(`app/analysis/prices.py`), corporate actions (`app/analysis/corporate_actions.py`), and
the integrated-filing path (`fetch_cohort_integrated_filings.py`). No iXBRL parser was
needed — the endpoint publishes plain XBRL alongside it.

Worth repeating because the codebase looks further along than it is: **no surprise,
response, forward return, or score has ever been computed in this project.** Every
result to date is a data-quality measurement.
