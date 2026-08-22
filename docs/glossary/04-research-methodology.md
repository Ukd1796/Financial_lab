# 04 — Research methodology: the vocabulary of not fooling yourself

Every term here names a specific mechanism by which a backtest reports a profit that
does not exist. They are not exotic edge cases — they are the **default** outcome of
naive backtesting. This project has an unusually long graveyard of falsified ideas
(`docs/research_log.md`) largely because these controls are enforced.

## Point-in-time (PIT)

A dataset is **point-in-time** if you can reconstruct exactly what was knowable on a
given past date — no later corrections, no later additions, no hindsight.

Most financial data is *not* PIT. A vendor serving "Reliance Q3 FY24 revenue" gives you
today's best understanding of that number, including any restatement made since. If you
backtest with it, your 2024 strategy trades on a figure published in 2025.

This is the reason for the split running through the whole project:

| Source | PIT? | Admissible for |
|---|---|---|
| NSE filing archive | **Yes** — as-filed, timestamped | measuring a historical edge |
| indianapi (vendor) | **No** — restated, no publication timestamp | the forward run, data-quality work, sector labels |

`is_point_in_time=False` is stamped on every vendor record. The charter's language is
deliberately absolute: vendor fundamentals are **inadmissible for measuring a
historical edge**. Not "use with caution" — inadmissible.

**Forward runs create their own PIT record.** The vendor store is append-only and
vintage-stamped, so from today onward it accumulates a genuine history of what was
known when. That record starts now and cannot be backfilled. This is why a shadow run
has value even before any edge is demonstrated.

## Look-ahead bias

Using information that was not yet available at the moment you claim to have traded.
The most common form is subtle and arithmetic rather than dramatic:

- Trading a result at the *close* of the day it was announced at 17:15 — after the
  close.
- Using a quarter-end date instead of the dissemination date, buying yourself weeks of
  free hindsight.
- Ranking a universe by full-year turnover and then trading January.

This is why file 02 treats `exchdisstime` as non-negotiable. A backtest with look-ahead
bias doesn't look broken — it looks **excellent**, which is what makes it dangerous.

## Survivorship bias

Building a dataset from companies that exist *today* silently deletes every company
that failed.

We measured it here rather than assuming: **643 of 3,411 ISINs (19%) stopped trading
between 2018 and 2026, and 212 of those died ≥70% below their peak.** Any study built
on today's index constituents excludes all of them, and so systematically overstates
returns — most severely for strategies that buy beaten-down stocks, because the ones
that never recovered are missing.

The fix is the PIT cohort from file 01: rebuild the universe from what actually traded
on the date in question. The validation that it worked is satisfying — the top-20 by
turnover as of 2018-12-31 contains **DHFL and JETAIRWAYS**, both of which collapsed in
2019. No list of current constituents could ever produce them.

**A structural trap specific to V2.** The usable filing window (2023 onward) contains
only companies that survived *to* 2023. So the window is survivorship-selected by
construction, no matter how carefully the cohort is built. Hence charter §8's new
condition 5: report results **with and without** the delisted population. A sleeve that
only works when the failures are excluded has not been demonstrated.

## Missing-data bias

Subtler than survivorship, and it bit us directly. If parse failures are **correlated
with outcomes**, dropping unparseable records is equivalent to deleting the failures.

JETAIRWAYS — the pilot cohort member that was grounded and delisted — had the *worst*
filing coverage of any name: 3 events, 0 usable. Quietly dropping bad parses would have
removed the single most informative company in the sample and biased everything upward.

Hence the design rule from file 02: every failure is stored as an
`event_data_exception` and reported by year and issuer **before** any outcome is
computed. You cannot rationalise a coverage gap you haven't looked at yet.

## Restatement and vintage

A **restatement** is a company revising a previously published figure. **Vintage** is
*when* a particular version of a number was published.

A PIT store keeps every vintage, so you can ask "what did we believe on 2024-06-01?"
A vendor typically keeps only the latest, which is why it can't answer that question at
all.

## Folds — development, validation, confirmation

The discipline for not fitting noise. Split history into chronological blocks with
different, non-negotiable roles:

| Fold | Window | Role |
|---|---|---|
| A | 2023 H2 – 2024 H2 | **Development.** Every design choice is fixed here |
| B | 2025 | **Validation.** Run exactly once |
| C | 2026 → forward | **Confirmation** and ongoing forward run |

The split is **chronological, never random**. Random splits leak: market conditions are
shared across nearby dates, so a randomly held-out day sits between two training days
that already reveal the answer.

"Run exactly once" is the whole point of fold B. If you look, adjust, and look again,
it has silently become development data and you no longer have a validation set.

## Independent observations — the binding constraint

The most important sentence in the charter amendment: the binding constraint is the
number of **independent time periods (~10)**, not the number of events (~500 companies
× ~13 quarters ≈ 6,500).

Earnings cluster into the same six-week windows each quarter. Every company reporting
in one season shares the same market conditions, the same macro backdrop, the same
sentiment. They are not 500 independent draws — they are closer to **one** observation
with 500 correlated parts.

So the honest sample size is roughly 10, not 6,500. This is stated in advance precisely
because a disappointing result invites recalculating it upward afterwards.

## Pre-registration

Writing down the hypothesis, the method, and the **pass/fail bar** *before* seeing the
result — and dating it.

Without it, "the strategy works" is unfalsifiable: there is always another parameter,
window, or subset that rescues a bad result, and after the twentieth attempt you've
found noise and named it a discovery. Charter §9 requires amendments to be written and
dated before any result they could be tuned against.

The charter amendment (2026-08-12) is the format working correctly: **two of four
proposed changes were rejected on measurement**, including one the author had argued
for. Rejecting your own proposal in writing, before the data could talk back, is the
only evidence that the procedure is real.

## Multiple testing

Test twenty ideas at a 5% significance threshold and one will look significant by pure
chance. This project has tested many levers — the graveyard in `docs/research_log.md`
lists them — which means the bar for the next one must be *higher*, not lower.

It is also why charter §3 forbids storing revenue/EBITDA/PAT and then trying
combinations until one works. They are collected as data-quality fields and explicitly
barred from the primary score.

## Overfitting, and its favourite disguise

Fitting the noise rather than the signal. Its most convincing disguise is a parameter
that "makes sense": regime-specific ATR multipliers *sounded* principled and cost 10
percentage points of return.

The countermeasure used throughout: parameters chosen **a priori**, reported at their
a-priori values — not at the best value found in a sweep. Robustness across nearby
settings is reported as a sanity check, never as the headline.

## Falsification, and why the graveyard is an asset

The research log keeps a permanent record of every idea that **failed**, so no dead
experiment is re-run. That list is more valuable than the list of successes: it is the
map of where the edge isn't.

Its deepest entry is worth reading in full — after testing six leading-indicator
candidates, the finding was that *no price-derived signal predicts forward returns at
this scale*, which retrospectively explains why every earlier lever failed. That single
negative result is what redirected the whole project toward fundamental event data, and
it is the reason V2 exists.

---

## The V2 test in one page — what passes, what fails

*Added 2026-08-18. This is the whole experiment stated plainly, so the verdict is
readable without holding the charter in your head.*

### What we are claiming

> When an Indian company reports quarterly earnings **better than the same quarter a
> year earlier**, and the market's **immediate reaction is muted** relative to its
> peers, the stock outperforms its peers over the **next 20 trading sessions** —
> by enough to beat trading costs.

That is one sentence and it is the entire hypothesis. Every piece of machinery in
`app/event_research/` exists to measure it without fooling ourselves.

### How one event works, start to finish

```
1. A company files results with NSE at a timestamped moment (available_at)
2. Surprise = EPS this quarter  -  EPS same quarter last year
                                   ^^^^^^^^^^^^^^^^^^^^^^^^^
                                   needs a SECOND filing from 12 months earlier
3. Reaction  = the first full trading session AFTER the filing
               ... measured against 20 peers of similar traded value
4. Qualify   = surprise positive  AND  reaction below the peer median
5. Buy       = at the OPEN of the next session (never at a known close)
6. Sell      = at the OPEN, 20 sessions later
7. Score     = our return  -  the peer basket's return  -  0.55% costs
```

Each quarter we take the **40 largest qualifying surprises**, equally weighted.

### The verdicts

There are **three** outcomes, and the third is not a softer version of failing.

| Verdict | Meaning |
|---|---|
| **PASS** | Every condition below holds. Produces a standalone backtest — **not** permission to trade real money. |
| **FAIL** | Any condition is violated on sufficient data. V2.0 ends. |
| **INCONCLUSIVE** | The sample was too thin to decide. V2.0 ends *for this sample*. **Not a pass, and explicitly not a licence to loosen the rules until a number appears.** |

### The conditions (charter v3 §7)

Checked on fold A first. **Any single failure ends it.**

| # | Condition | Passes if | Fails if |
|---|---|---|---|
| 0 | **Sufficiency** — checked first | ≥4 usable quarters per fold, ≥15 qualifying events per quarter | otherwise **INCONCLUSIVE** |
| 1 | **Return clears cost** | net ≥ **1.10%** per quarter | below it |
| 2 | **Both folds agree** | positive in fold A *and* fold B, B run once | negative in either |
| 3 | **Not one lucky quarter** | ≤40% of the total from any single quarter | above it |
| 4 | **Holds up in 2026** | fold C keeps the same sign | sign flips |
| 5 | **Survives its failures** | works with *and* without the collapsed/delisted names | only works when failures are excluded |

### Why 1.10%, and why it is not arbitrary

Two completely independent numbers landed on top of each other:

- **Economics.** Round-trip cost is 0.55% (STT, stamp, fees, plus 15bp/side impact).
  The charter demands **2× cost**, so **1.10%**.
- **Statistics.** A 40-name book has a measured standard error of 1.42% per quarter
  (`scripts/event_research/power_calculation.py` — 3,000 random draws per quarter, so
  correlation is measured, not assumed). Over fold A's ~6 quarters, a t-statistic of 2
  needs **1.16%**.

An effect that pays for itself is therefore also, roughly, an effect we can detect.
That coincidence is why the book is 40 names and not 20 (which would need 1.74%,
making statistics the binding constraint) or 60 (0.90%, making cost the binding one).

### What "at the edge of power" means

Published post-earnings drift in emerging markets runs roughly 1.5–3% gross per
quarter over 20 days. After 0.55% of costs, the plausible net range **straddles** the
1.10% bar. So:

- a clear pass would be a genuine, if surprising, result;
- a clear fail is entirely expected and closes the lane cheaply;
- **a result hovering near the bar is weak evidence, not a finding** — and must be
  reported as such rather than rounded up.

This was written down before any return was computed. It is not a hedge added after
seeing a disappointing number.

### The one thing that can still make this meaningless

**Quarters, not events, are the binding constraint** (see *Independent observations*
above). Earnings cluster into the same six-week windows, so 500 companies reporting in
the same season is closer to one observation than five hundred. The whole design is
sized around having roughly 11 independent quarters.

That is why the fetch window matters so much, and why a missing year of *comparative*
filings — not of returns, of comparatives — can decide the outcome before the test
runs. See `02-filings-and-xbrl.md` on chaining.
