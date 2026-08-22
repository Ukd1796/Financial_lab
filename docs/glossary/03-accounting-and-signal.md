# 03 — Accounting terms and the signal we're building

## The line items we extract

Reading down a quarterly income statement:

**Revenue** (`RevenueFromOperations`) — money from selling things, before any costs.
Also called the top line.

**Operating profit** — revenue minus the costs of running the business, before
financing and tax. Appears under several names with slightly different boundaries;
`EBITDA` (Earnings Before Interest, Tax, Depreciation and Amortisation) is the common
one. Measures whether the *business* works, independent of how it's financed.

**PAT** (Profit After Tax) — the bottom line, what's left for shareholders. Also called
net profit or net income.

**EPS** (Earnings Per Share) — PAT divided by shares outstanding.

- **Basic EPS** uses shares actually outstanding.
- **Diluted EPS** also counts shares that *could* exist (options, convertibles), so
  it's slightly lower and slightly more conservative.

**EPS is the primary signal input.** The reason is share-count normalisation: PAT
alone isn't comparable across time if the company issued shares, and isn't comparable
across companies at all. EPS is per-share, so it's a like-for-like measure. It's also
the number the market itself quotes and reacts to.

The caveat, which corporate actions make concrete: EPS is per-share, so a stock split
mechanically changes it. This is the same adjustment problem as file 01, on the
fundamentals side.

## Fiscal quarters

India's fiscal year runs **April to March**. So:

| Quarter | Months | Ends |
|---|---|---|
| Q1 | Apr–Jun | 30 June |
| Q2 | Jul–Sep | 30 September |
| Q3 | Oct–Dec | 31 December |
| Q4 | Jan–Mar | 31 March |

"FY25" means the year ending March 2025. A filing with `result_period_end =
2024-03-31` is Q4 of FY24 — *not* Q1 of anything. Getting this off by one quarter
would compare a company against the wrong season entirely.

## Seasonality — why the comparison is year-over-year

Most businesses have a natural annual rhythm: festival-season retail, monsoon-dependent
agriculture, March fiscal-year-end effects. Comparing Q3 to Q2 measures the calendar,
not performance.

So the comparison is always **the same quarter one year earlier** — Q3 FY25 against
Q3 FY24. That cancels the seasonal pattern and leaves the change in the business.

This is exactly why file 02 dwells so much on proving which period a number belongs to.
Compare Q4 against Q1 by accident and you get a large, confident, entirely fictional
number. Our own yfinance work hit this: with one quarter missing from the series,
counting *rows* backwards compared Reliance's Q4 against its Q1 and reported growth
where the true year-over-year change was a decline. **Address quarters by calendar
bucket, never by list position.**

## Earnings surprise

The core concept. Markets are forward-looking, so the *level* of earnings is mostly
priced in already. What moves a stock is the **difference between what was reported and
what was expected**.

Everything hinges on how you define "expected", and there are two options.

### Option A — consensus surprise (SUE)

Take the average of analyst forecasts, and measure how far the actual result landed
from it. **SUE** (Standardized Unexpected Earnings) divides that gap by its historical
standard deviation, making surprises comparable across companies:

```
SUE = (actual EPS − consensus EPS) / stdev(past surprises)
```

This is the textbook definition and it is what academic literature uses.

**We rejected it, on measurement.** Testing 20 companies across the whole liquidity
range via the vendor's `/stock_forecasts` endpoint:

| | |
|---|---|
| Names with zero usable quarterly surprises | **10 of 20 (50%)** — including the single largest, HDFCBANK |
| Median usable quarters per name | 2 |
| Median analysts per estimate | 3 |

Indian *quarterly* analyst coverage is too thin to represent a market expectation. A
consensus of three analysts is three people's opinion, not the market's. Standardising
against it would inject more noise than it removes, halve the tradeable universe, and
cut usable history from 13 quarters to about 8.

(Indian *annual* consensus is well covered — 29 to 31 analysts. But an annual forecast
cannot drive a 20-session event.)

### Option B — seasonal surprise ← what we use

Use the company's **own result from the same quarter one year earlier** as the
expectation:

```
surprise = EPS(Q3 FY25) − EPS(Q3 FY24)
```

It needs nothing but the issuer's own filing history, which we have ~13 quarters deep
for essentially every name, including 95% of the ones that later collapsed.

It is a genuinely weaker proxy — it doesn't know what the market expected, only what
the company did last year. The charter is explicit that this is not a compromise but
**the only expectation model that works at this universe size**, and records the SUE
rejection so it isn't re-proposed.

**Measured 2026-08-13:** the year-ago figure is *not* present inside the current
filing — 226 of 226 usable filings define no prior-year context. So a surprise requires
**chaining two separately-ingested filings** four quarters apart, and both must parse
cleanly. This is what makes the pre-2023 unusable era so expensive: it doesn't just
delete those quarters, it deletes the *following* year's surprises too.

### Guard: the non-positive base

Percentage growth from a loss-making quarter is meaningless — going from −0.01 to
+5.00 is not "50,000% growth". Our code returns `UNDEFINED_BASE` rather than a number.
Without that guard, the largest apparent surprises in the dataset would all be
artefacts, concentrated exactly where earnings are most volatile.

## PEAD

**Post-Earnings-Announcement Drift** — the empirical finding that after a surprise,
prices keep drifting in the same direction for weeks rather than jumping once and
stopping. It's one of the most-replicated anomalies in finance, and it is the entire
premise of the ~20-session holding period.

Two honest caveats the charter records up front: PEAD has **decayed substantially in
developed markets** as it became well known, and it may be weaker or absent here. That
is why §8's pass bar is deliberately strict.

## Horizon: why ~20 sessions

Roughly one calendar month of trading. The band is chosen from what the data can
actually support:

- **1–5 days** is not reachable from fundamental data — that horizon belongs to order
  flow and microstructure, which we have no access to.
- **Months to years** would make this a factor fund, not an event strategy, and would
  need a completely different design.
- **5–40 sessions, anchored to an event** is the achievable band.

Between events the strategy holds **nothing**. That episodic quality is what
distinguishes it from an always-invested smart-beta fund — a distinction the project
drifted across once already and had to correct.

## Sector-adjusted return

If IT stocks rise 8% in a month and our IT holding rises 9%, the *strategy* earned 1%,
not 9%. Sector adjustment subtracts the sector's return over the same window so what
remains is attributable to the event rather than to being in a lucky industry.

Two consequences worth tracking:

1. It requires a **sector label per company** — which is why the vendor's `/stock`
   endpoint is load-bearing. It is the only tested source that populates one;
   `/industry_search` returned nulls in 20 of 20 rows.
2. Charter §8 also caps any single sector at **40% of the aggregate result**, so a
   "signal" that is really one sector's good year gets caught rather than shipped.

## Round-trip cost

Everything it costs to enter and exit: brokerage, exchange fees, STT, stamp duty, plus
**slippage** (you don't transact at the quoted price) and the **bid-ask spread**.

Charter §8 demands the sleeve clear **2× modelled round-trip cost**, not merely
positive return. A strategy that earns less than it costs to trade is a way to convert
capital into fees, and at this horizon the tax drag is real too — Indian short-term
capital gains run 20%.
