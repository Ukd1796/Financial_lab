# V2 Research Charter — Earnings-Response Sleeve

**Status:** Phase 0–1 approved; data audit and schema design only.  No event signal,
backtest, or production wiring is authorised by this document.

**Version:** 1.0
**Created:** 2026-08-09
**Owner:** Tactiq research

## 1. Decision being tested

### Hypothesis

In liquid NSE equities, a positive quarterly earnings surprise that receives a muted
initial market response may contain firm-specific information not present in the
current OHLCV-only Tactiq pipeline.  A deterministic, long-only portfolio of those
events may earn positive **net sector-adjusted** forward returns.

This is a research hypothesis, not a claim that post-earnings drift will exist in this
sample.  The result is useful either way: a failure closes this data lane without
adding an LLM, a new price indicator, or parameter tuning.

### What will be built if — and only if — the hypothesis passes

An independent **Earnings-Response Sleeve**:

```text
NSE result filing (timestamped, immutable)
  -> event normalisation + earnings surprise
  -> completed-session initial-response measurement
  -> deterministic event score
  -> separate sleeve / separate position ledger
  -> existing execution, cost and hard-risk controls
```

It is deliberately **not** a sixth input to `DynamicUniverseAgent`, a new
`MultiStrategyRouter` contestant, or an AdaptiveSelector/LLM input.  The existing
router has documented merge, ownership and cash-priority interference.  The event
sleeve must prove its return source alone before receiving any shared capital.

### Explicitly out of scope for V2.0

- More OHLCV-only factors, universe smoothing, regime labels, VIX/macro throttles,
  or LLM stock ranking.  These are already tested or falsified in `research_log.md`.
- Natural-language sentiment, call transcripts, analyst estimates, and alternative
  data.  They may be separate, pre-registered projects only after the numeric event
  signal is decided.
- Production trading, adaptive allocation, or a Nifty-500 backtest before the data
  provenance gates below pass.

## 2. Causal trading clock (frozen)

The timestamp is more important than the score.  Every event is in `Asia/Kolkata` and
uses the **NSE dissemination timestamp**, not the financial period end, board-meeting
date, website-upload date, or a vendor's later collection time.

| Name | Definition | Permitted information |
|---|---|---|
| `available_at` | NSE exchange dissemination timestamp of the original result filing | Filing and data visible at this instant only |
| `reaction_session` | First *full* NSE trading session beginning after `available_at` | Result data plus that session's completed OHLCV |
| `signal_ready_at` | Close of `reaction_session` | Surprise and one completed initial-response session |
| `entry_session` | Next valid NSE session after `reaction_session` | Order fills at that session's open, never at a known close |
| `exit_session` | Pre-specified holding-horizon open, or a pre-specified hard-risk exit | No later event values or revised statements |

The universal one-session reaction delay intentionally sacrifices speed.  A result
released at 10:00 and one released at 18:00 receive the same treatment: measure the
next complete session, enter at the following session's open.  That removes ambiguous
intraday availability and same-close fill assumptions.

## 3. Primary signal definition (frozen for Phase 2)

The sole primary research input is a seasonal EPS surprise plus the initial reaction.

1. Use the original, consolidated, non-cumulative quarterly result when available.
2. Compute an issuer's seasonally differenced EPS from the same fiscal quarter one
   year earlier.  Standardise it using only prior available seasonal differences.
3. Compute initial abnormal response as the `reaction_session` return less its
   pre-assigned sector index return; fall back to Nifty 500 only when a sector index
   was not available at the decision time.
4. The Phase-2 study will inspect the pre-declared grid of surprise quintile and
   response quintile.  Its **primary** candidate is positive surprise with an initial
   response below the positive-surprise cohort median (underreaction), evaluated at
   a 20-trading-session horizon.  Five- and sixty-session outcomes are secondary,
   reported but not optimised.

Revenue, EBITDA/PBIT and PAT will be stored during Phase 1 as data-quality fields.
They are not allowed in the primary score.  This avoids silently trying many
"fundamental quality" combinations until one wins.

## 4. Use in the eventual portfolio

If the event study clears its gate, V2.0 will begin as a standalone research portfolio:

- Equal-risk positions, with a fixed number of top eligible events at each rebalance.
- Fixed 20-session holding period; only a documented catastrophe/safety stop may exit
  earlier.  Profit targets, regime exits and adaptive exit variants are excluded.
- One issuer and a pre-defined sector cap; no averaging down and no reinvestment of
  unfilled allocations during the test.
- A fixed, small capital sleeve only after standalone validation.  It remains separate
  from the existing strategy router and reports its own P&L, turnover, fill quality,
  sector exposure and attribution.

The existing `RiskAgent`, execution adapter, NSE calendar and analytics can be reused
at the outer boundary.  `DynamicUniverseAgent`, per-strategy filters, router weights,
regime gates and the LLM selector are specifically not inputs to event eligibility.

## 5. Data contract

### Authoritative source hierarchy

1. **Primary:** NSE Corporate Filings — Financial Results, including XBRL where
   available and broadcast/dissemination time.
2. **Fallback/verification:** the result attachment filed with the same NSE event.
3. **Not a substitute:** a vendor's fundamental history may accelerate extraction, but
   it can only be used after its values and timestamps are reconciled to the primary
   filing for a representative sample.

The NSE page displays XBRL and broadcast date/time.  It also notes a filing-format
change from the March-2025 quarter onward, so the ingestion system must retain the
source format and parser version per event rather than assume a homogeneous series.

### New immutable records

| Record | Required fields | Why it exists |
|---|---|---|
| `instrument_identity` | ISIN, NSE symbol, issuer name, valid-from/to, corporate-action mapping | Symbol changes cannot silently join two issuers |
| `financial_result_event` | event id, ISIN, result period, fiscal-quarter label, original/revision flag, received/disseminated/available timestamps, source URL, source hash, source format | Replays exactly what was knowable and when |
| `financial_result_fact` | event id, consolidated/cumulative/audit flags, EPS, revenue, operating profit, PAT, units, currency, parser version, validation status | Separates original facts from derived features |
| `eligible_universe_snapshot` | effective date, ISIN, eligibility reason, 20/60-day traded value, price, listing status, source version | Prevents current-constituent and liquidity hindsight |
| `event_feature_snapshot` | event id, feature version, `computed_at`, source event ids, surprise, response, eligibility decision | Permits exact replay and a complete audit trail |
| `event_data_exception` | event id, failure type, disposition, reviewer, timestamp | Missing/ambiguous filings are visible rather than dropped invisibly |

Raw XBRL/attachment bytes are retained outside the database with a content hash; the
database holds the immutable reference.  Corrections create a new event linked by
`supersedes_event_id`.  They never overwrite the original filing.

### Current-code gap

`MarketOHLC` stores only `(symbol, timestamp, OHLCV)`.  The present Yahoo provider uses
`auto_adjust=True` and stores neither source provenance nor corporate-action factors.
It is adequate for the existing price research but not a sufficient source of truth for
event-time fundamental research.  Phase 1 therefore adds no data to `market_ohlc` and
does not alter live production tables.

## 6. Bias controls — release gates, not suggestions

| Risk | Mandatory control | Release gate |
|---|---|---|
| Look-ahead / timing | Use NSE dissemination time; enter only at the next session *after* a completed reaction session | 100% of sampled events have a timezone-aware timestamp and entry later than `signal_ready_at` |
| Revision bias | Preserve original facts; revisions are separate, never backfilled into original features | Any overwritten historical value is a hard failure |
| Survivorship / delisting | Build a dated eligibility snapshot including delisted, renamed and suspended names | No current constituent list may be projected backward |
| Universe-selection bias | Eligibility is an ex-ante liquidity/listing rule, stored every rebalance; no selection by later outcome | Coverage and exclusions are reported by year, sector and listing status |
| Corporate-action bias | Store ISIN, face value and action mapping; derive split-adjusted quantities only using actions known by the event time | Random sample reconciles price/EPS changes around actions |
| Filing-format / parser bias | Store original document, parser version and validation status; dual-validate a random sample against the filing | Numeric fields must meet the pre-set reconciliation tolerance |
| Missing-data bias | Log every missing/unparseable filing; report coverage before outcomes | No dropping names/events solely because their future return is inconvenient |
| Multiple testing | One primary score, one primary 20-session horizon, one pre-specified pass bar | New feature/exit/universe variants require a new charter version |
| Benchmark leakage | Sector benchmark membership and return must be available before the event; use fixed fallback hierarchy | Every event records the benchmark used |
| Execution/cost bias | Next-session-open fill, no same-close fills; costs depend on prior ADV and participation | No fixed 15 bp assumption once the universe broadens |
| Model-selection bias | Development 2018–2022, validation 2023–2024; 2025–2026 is confirmation but not pristine; forward paper is the decisive test | Results cannot be selected on 2025–2026 then described as out-of-sample |

## 7. Phase 1 audit and blockers

### What is confirmed

- NSE's Financial Results filings expose broadcast date/time and XBRL links.
- NSE's research-data catalogue lists a financial-results calendar.
- Nifty 500 is a plausible future breadth expansion, but its historical constituent
  history and corporate-action lineage are not present in this repository.

**Audit references:** [NSE Financial Results](https://www.nseindia.com/companies-listing/corporate-filings-financial-results),
[NSE data-sharing catalogue](https://nsearchives.nseindia.com/web/sites/default/files/inline-files/Data%20list%20under%20NSE%20Data%20Sharing%20Policy%20for%20Research%20and%20Analysis_20250728.pdf),
and [NSE Index Data Subscription](https://www.nseindia.com/static/nse-indices/index-data-subscription).
These confirm the public filing fields and the availability of licensed index data;
they do **not** prove that the required 2018-to-present archive can be bulk-replayed
without an acquisition or licensing arrangement.

### What must be proved before any event study

1. **Historical coverage:** obtain or verify 2018 onward result events, original
   attachments/XBRL and dissemination timestamps for a representative Nifty 150 sample.
2. **Field completeness:** measure quarter-by-quarter consolidated, non-cumulative EPS
   coverage; do not assume all companies report a comparable field.
3. **Identity coverage:** establish ISIN-to-symbol history, including delistings and
   symbol changes, for the intended universe.
4. **Point-in-time universe:** obtain licensed historical Nifty constituent records or
   construct a daily, rules-based liquid NSE universe from historical listings and ADV.
   Today's Nifty 150/500 lists are prohibited for historical selection.
5. **Price reconciliation:** select a price source with auditable corporate-action
   handling for event fills; reconcile it against a sample of official EOD data.
6. **Cost calibration:** decide a prior-ADV participation limit and impact model before
   testing Nifty 250/500.  Wider-universe gross returns are not enough.

If any item is unavailable, the outcome is **blocked**, not "approximated."  The next
action is to change the data plan or purchase/license the missing history—not to loosen
the research definition.

### Cheapest defensible acquisition path

**Track A — zero-cost historical feasibility pilot (data quality only).**  Use a fixed,
historically dated sample of 20 liquid non-financial issuers and gather 2019–2024
quarterly results.  The sample must be chosen from an archived NSE snapshot before any
outcomes are viewed; it is not a current-members-only sample.

| Need | Free source | Permitted use | Not permitted |
|---|---|---|---|
| Filing clock and original document | NSE Financial Results/XBRL page and attached result filing | Source URL, content hash, exchange dissemination time and original reported facts | Assuming every historic filing is bulk-accessible or scraping at production scale |
| Timestamp cross-check / attachment discovery | Official BSE corporate-announcement pages | Independently compare a sample of filing times and documents | Replacing NSE time with a later vendor collection time |
| Numeric-field convenience check | Screener.in company quarterly page, manually sampled | Reconcile EPS/PAT/revenue to the primary filing | Treating its current/revised history as point-in-time or relying on an undocumented API |
| Historical cohort snapshot | NSE historical monthly/daily index reports | Fix the pilot cohort at the past report date | Using today's Nifty 50/150/500 list in the past |
| Price feasibility only | Existing Yahoo OHLCV cache, reconciled to a small sample of exchange EOD data | Confirm date/symbol/corporate-action handling | Declaring investable backtest returns from it |

The pilot has a **data-only** report: coverage, timestamp completeness, parser accuracy,
ISIN mapping and exceptions.  It must not calculate or rank forward returns.  That keeps
the eventual Phase-2 outcomes unseen while we decide whether the free source is reliable.

**Track B — zero-cost clean forward shadow feed.**  Starting immediately, snapshot a
fixed current liquid cohort daily and ingest each new NSE result filing with its source
document and dissemination time.  Generate shadow event eligibility but submit no
orders.  This is slow, but it is the only completely uncontaminated evidence stream if
the historical archive proves incomplete.

**First paid step, only if Track A passes:** request an NSE Corporate Data / historical
index-constituent quote.  This buys reproducible breadth and point-in-time membership;
it is preferable to paying for a convenient vendor whose timestamp/revision policy cannot
be audited.  BSE corporate-data subscriptions are a secondary comparison source, not a
replacement for the primary exchange clock.

## 8. Pre-registered evidence standard for Phase 2

The exact cost model and minimum sample count will be frozen after Phase 1 coverage is
measured, before forward-return analysis.  The primary event bucket must then:

1. exceed **two times its modeled round-trip cost** in net 20-session sector-adjusted
   return;
2. be positive in at least four of five chronological folds and in both the Nifty-150
   and newly added liquid-universe cohorts;
3. not derive more than 40% of its aggregate result from one sector or one calendar
   year; and
4. retain its sign in the 2025–2026 confirmation period.

Failure on any condition ends V2.0.  Passing produces a standalone backtest only; it
does not authorise production allocation.

## 9. Amendments and evidence log

This file is the Phase-0 baseline.  Any change to the primary score, timing, universe,
cost model or pass bar requires a dated `v2_event_research_charter_vN.md` amendment
explaining why it was made **before** results from that change are inspected.  Results,
coverage reports and failed variants belong in `docs/research_log.md`.

The no-return Phase-1 operating procedure is in
[v2_event_pilot_operator.md](v2_event_pilot_operator.md).
