# V2 Event Research Charter — Amendment v3

**Dated: 2026-08-17.** Amends `docs/v2_event_research_charter.md` under its §9, and
supersedes nothing in `v2_event_research_charter_v2.md` — v2's fold structure, universe
scope and rejected changes all stand.

**Status when written: NO surprise, response, forward return or score has been computed.**
The corpus on disk holds 913 events / 474 VALID across **19 issuers** — the retired 2018
pilot. The 597-issuer rolled cohort has no filings behind it yet. This amendment is
therefore written *before* any result it could be tuned against, which is the only
condition under which it means anything.

v2 §2 said "the exact cost model and minimum sample count will be frozen after Phase 1
coverage is measured, before forward-return analysis." Coverage is measured. This is that
freeze.

---

## Summary

| # | Item | Status before v3 | Decision |
|---|---|---|---|
| 1 | Peer-basket benchmark rule | Chosen 2026-08-15, unspecified | **FROZEN** — 20 nearest by traded value, equal-weight |
| 2 | §8 cond.3 sector half | Known unenforceable, not written down | **AMENDED** — calendar half only, loss stated |
| 3 | Round-trip cost model | Never fixed | **FROZEN** — 0.55%, so the §8 cond.1 bar is 1.10% |
| 4 | Book size and minimum sample | Never fixed | **FROZEN** — K=40, ≥15 events/quarter, ≥4 quarters/fold |
| 5 | Verdict vocabulary | PASS / FAIL only | **AMENDED** — INCONCLUSIVE added as a distinct outcome |

Items 3 and 4 were chosen against a power calculation run on the price panel alone,
before any signal existed. That calculation is §6 below.

---

## 1. Peer-basket benchmark — FROZEN

Charter §3.3 requires the initial response to be measured "less its pre-assigned sector
index return", falling back to Nifty 500. **Neither input exists point-in-time and free.**

- Sector labels: the `sector` column is populated in **0 of 300** rows in every quarterly
  cohort snapshot. There is no free PIT sector classification for this universe.
- Nifty 500 constituent history: charter §7 item 4 already records this as unavailable
  without a licence, and prohibits projecting today's list backward.

**Replacement rule.** For an event on issuer *i* with reaction session *t*:

> Peers are the **20 issuers in the same quarterly cohort snapshot whose 20-day traded
> value is closest to *i*'s**, measured at that snapshot's as-of date, excluding *i*.
> The benchmark return is their **equal-weight** mean corporate-action-adjusted return
> over the identical session span.

Every event stores the peer ISINs it actually used, per charter §6's benchmark-leakage
gate ("every event records the benchmark used").

**Why traded value and not something better.** It is the only issuer attribute in the
cohort snapshot that is ex-ante, free, and already point-in-time — it is the same quantity
the eligibility rule is built on. It is a **size proxy, not a sector proxy**, and it will
not remove sector co-movement. That is a real weakness, recorded here rather than
discovered later.

**Cost of the rule: one free parameter** — the peer count, fixed at 20. It is not to be
varied. If a later version wants a different peer count it is a new charter version with a
new pass bar, per §9 of the base charter.

## 2. §8 condition 3 — AMENDED, and the loss is stated

Original: *"not derive more than 40% of its aggregate result from one sector or one
calendar year."* v2 tightened "year" to "quarter". Without sector labels (§1 above) the
sector half **cannot be checked at all**.

**Amended condition 3:** no more than **40% of the aggregate fold result may come from one
calendar quarter**. A concentration table by issuer is reported alongside but does **not**
gate.

**This is a weakening of the evidence standard, not an improvement to it.** A sleeve could
pass this amended condition while being entirely one sector's story, and this charter
would not detect it. That risk is accepted for V2.0 because the alternative is to block
the study on a data purchase; it is named here so the eventual result is read with it in
view. Restoring the sector half is a V2.1 precondition for any production allocation.

## 3. Cost model — FROZEN

```
round_trip = 0.25%  fixed     (STT 0.20% + stamp duty + exchange txn + SEBI + GST)
           + 2 x 0.15%  impact  (next-session-open fill, participation capped at 1% of ADV)
           = 0.55%
```

**§8 condition 1 bar: net 20-session peer-adjusted return must be ≥ 2 × 0.55% = 1.10% per
quarter.**

The 1% ADV participation cap is enforced per event against prior-60-session traded value
from the exchange panel. **An event that cannot be filled inside the cap is dropped before
any return is computed**, and the dropped count is reported per quarter. This satisfies
charter §6's execution-cost gate ("costs depend on prior ADV and participation; no fixed
15 bp assumption once the universe broadens") — the 15bp figure here is the *impact*
component for a top-300-by-liquidity universe with a hard participation cap, not a blanket
all-in assumption.

Rejected as too lenient: brokerage-free delivery with no impact term (~0.25% round trip).
Real fills at the open in 300-name mid-liquidity NSE names are not free.

## 4. Book construction and minimum sample — FROZEN

Charter §3.4's primary bucket is unchanged: **positive standardised seasonal EPS surprise,
with an initial response below the positive-surprise cohort median for that quarter**,
held 20 sessions.

| Parameter | Frozen value |
|---|---|
| Book size *K* | **40**, equal-weight, taken as the 40 largest standardised surprises inside the bucket |
| Minimum events per quarter | **15**. Below that the quarter is excluded and reported as excluded |
| Minimum usable quarters per fold | **4**. Below that the fold is INCONCLUSIVE, not failed |
| Horizon | 20 sessions (primary). 5 and 60 reported, never optimised |

Fixed *K* rather than "all qualifying events" so that the standard error is constant across
quarters and the folds are like-for-like. With variable *K* a fold's result is dominated by
its fattest quarters, and §8 condition 3 becomes uninterpretable.

*K* = 40 is what the funnel is expected to yield, not an aspiration:

```
~300 cohort names per quarter
  x ~65%  have a VALID discrete filing at q and at q-4   -> ~195
  x ~50%  positive surprise                              ->  ~98
  x ~50%  response below the positive-surprise median    ->  ~49
  -> 40 taken, ~9 discarded
```

If the realised funnel is materially thinner than this, the quarter fails the 15-event
minimum and is excluded. **The funnel is not to be widened to reach K=40.**

## 5. Verdict vocabulary — AMENDED

The base charter admits only pass and failure. A third outcome is now named, because with
~11 independent quarters it is the single most likely one:

- **PASS** — every condition in §7 holds.
- **FAIL** — any condition in §7 is violated on sufficient data. V2.0 ends.
- **INCONCLUSIVE** — the sample was too thin to decide (a fold with fewer than 4 usable
  quarters, or a bucket that never reaches 15 events). V2.0 ends *for this sample*; the
  forward shadow run continues and may revisit it with more quarters.

**INCONCLUSIVE is not a pass, and it is not a licence to widen the search.** It is
specifically not grounds for relaxing K, the peer rule, the horizon, or the bucket
definition in order to obtain a decidable number. Recording it in advance is the point.

## 6. The power calculation this freeze is based on

Run 2026-08-17 on `data/analysis/prices.sqlite` and the 13 cohort snapshots. It uses
**only return dispersion** — no filing, no surprise, no signal-return relationship — so it
spends none of the pre-registration.

Cross-sectional standard deviation of 20-session peer-de-meaned return, per cohort quarter:

| Quarter | SD | Quarter | SD |
|---|---|---|---|
| 2023-06-30 | 9.76% | 2025-03-31 | 9.56% |
| 2023-09-30 | 8.93% | 2025-06-30 | 8.90% |
| 2023-12-31 | **16.36%** | 2025-09-30 | 9.25% |
| 2024-03-31 | 9.77% | 2025-12-31 | 9.57% |
| 2024-06-30 | 9.57% | 2026-03-31 | **13.62%** |
| 2024-09-30 | 10.55% | 2026-06-30 | 10.24% |
| 2024-12-31 | 11.32% | **median** | **9.76%** |

Standard error of the mean of a random *K*-name equal-weight book, measured empirically
over 3,000 draws per quarter (so residual within-quarter correlation is captured, not
assumed away):

| *K* | SE per quarter | naive √K | fold A (~6q) | t=2 needs |
|---|---|---|---|---|
| 20 | 2.13% | 2.18% | 0.87% | 1.74% |
| 30 | 1.69% | 1.78% | 0.69% | 1.38% |
| **40** | **1.42%** | 1.54% | **0.58%** | **1.16%** |
| 60 | 1.10% | 1.26% | 0.45% | 0.90% |

Two consequences, both recorded before any result:

1. **At K=40 the economic bar and the statistical bar coincide** — 1.10% required by cost,
   1.16% required for t=2 over fold A. The test is coherent: an effect that clears
   economics will be roughly detectable, and one that is detectable will be roughly
   economic. This is why K=40 was chosen over 20 or 60.
2. **The design is at the edge of its power.** Published emerging-market post-earnings
   drift over 20 days runs roughly 1.5–3% gross per quarter; after 0.55% costs the plausible
   net range straddles the bar. **A negative or inconclusive result is the expected
   outcome** (v2 §2 said this already) and a positive result near the bar should be
   treated as weak evidence, not a finding.

Two quarters — 2023-12-31 (16.36%) and 2026-03-31 (13.62%) — carry far more dispersion than
the rest. With so few quarters, §7 condition 3's 40% concentration limit may fail on
dispersion alone, independent of whether the signal works. That is a known and accepted
way for this test to return FAIL.

## 7. The consolidated decision table

This replaces §8 of the base charter and §2's amended list in v2. Fold A is evaluated
first. **All conditions must hold. Any single failure ends V2.0.**

| # | Condition | Pass | Fail |
|---|---|---|---|
| 1 | Net 20-session peer-adjusted return, mean per quarter | ≥ **1.10%** | < 1.10% |
| 2 | Sign, in fold A and fold B independently, fold B run exactly once | positive in both | negative in either |
| 3 | Concentration | ≤ 40% of the aggregate from any one calendar quarter | > 40% |
| 4 | Fold C confirmation | retains its sign | sign flips |
| 5 | Survivorship | reported **with and without** the delisted/collapsed population; sign holds both ways | holds only when failures are excluded |
| — | Sufficiency (precondition) | ≥ 4 usable quarters per fold, ≥ 15 events per quarter | otherwise **INCONCLUSIVE** |

Fold windows are unchanged from v2 §2: **A** = 2023 H2 – 2024 H2 (development, every
design choice fixed here), **B** = 2025 H1 – 2025 H2 (validation, one pass only),
**C** = 2026 H1 – forward (confirmation and ongoing shadow run).

**Fold B's single pass is enforced in code, not by discipline.** The evaluation script
writes a run token on its first fold-B invocation and refuses a second without an explicit
override flag whose use must be recorded in `docs/research_log.md`.

Passing produces a standalone backtest only. It does not authorise production allocation —
unchanged from the base charter.

---

## What is still deferred, and stays deferred

Nothing in this amendment admits new work into V2.0. Still out, per v2:

- Half-yearly balance-sheet and cash-flow parsing from NSE filings (v2 open item) — V2.1.
- The governance red-flag exclusion gate (v2 §3) — V2.1, and only if V2.0 clears its bar.
- Actual-vs-consensus surprise (v2 §1) — rejected; Indian quarterly analyst coverage is too
  thin to define a market expectation.
- Any additional feature, exit variant or universe change — a new charter version, per §9.

## Addendum — decisions taken during implementation, same day, before any result

All four were settled on 2026-08-17 while building the pipeline, and all are
recorded before a single fold verdict existed. Three were **forced** by rules
already frozen; one was an operator choice, and its cost is stated.

### A1. Surprise standardisation is HYBRID — operator decision, with a known cost

§3.2 of the base charter standardises the seasonal difference against the issuer's
own prior seasonal differences. That is unachievable in fold A: its first chainable
quarter has **zero** prior differences and its best has **four**, against the eight
the literature uses.

| Quarter | Prior seasonal differences available | Fold |
|---|---|---|
| 2023-12-31 | 0 | A |
| 2024-03-31 → 2024-12-31 | 1 → 4 | A |
| 2025-03-31 → 2025-12-31 | 5 → 8 | B |
| 2026-03-31 → 2026-06-30 | 9 → 10 | C |

**Rule adopted:** use the issuer's own history when at least **4** prior differences
exist; otherwise standardise against the cross-section. `MIN_TIME_SERIES_HISTORY = 4`.

**Stated cost, accepted by the operator:** fold A resolves almost entirely to the
cross-sectional method and fold C entirely to the time-series method, so §7
condition 2 compares two folds whose signals were constructed differently. A
disagreement between them is therefore **not** cleanly attributable to the
hypothesis. First measured run confirms the split: fold A 100% cross-sectional,
fold B 80% time-series, fold C 100% time-series.

**Mitigation, pre-registered here:** every event stores *both* standardisations
(`surprise_std_time_series`, `surprise_std_cross_sectional`) and which one the rule
used (`surprise_method`), and every fold report breaks results down by method. If
A and B disagree, the method-split table is what distinguishes a signal difference
from a method artefact. This is a declared diagnostic, not a second hypothesis.

### A2. Cross-sectional statistics come from the PRIOR completed quarter — forced by §6

§3.4 compares an event to "the positive-surprise cohort median for that quarter",
and A1's fallback is also cross-sectional. At the moment any single event becomes
actionable, most of its quarter has not reported. Three options existed:

- the completed quarter — **look-ahead, which §6 classes as a hard failure**;
- season-to-date — systematically drops each quarter's earliest reporters, which
  skew large and well-resourced: a size-correlated exclusion, the defect shape this
  project has hit five times;
- **the immediately preceding completed quarter — adopted.** Point-in-time, stable
  at ~200 names, applied identically to every event.

Cost: the first chainable quarter has no predecessor and is recorded ineligible.

### A3. Peer distance is measured in LOG traded value — clarification, not a change

§1 says the peers are those "closest" in 20-day traded value. The cohort spans
roughly ₹70 crore to ₹2,500 crore a day. On a raw scale every mid-cap's nearest
neighbours collapse onto the same cluster of smallest names, which is not a
size-matched basket. Distance is therefore `|log(adv_i) − log(adv_target)|`. This is
what "closest traded value" has to mean across two orders of magnitude.

### A4. Book notional fixed at ₹10 crore — needed to make §3's cap expressible

§3's 1%-of-ADV participation cap cannot be evaluated without a rupee position size.
**₹10 crore sleeve ÷ K=40 = ₹25 lakh per position.** Against the cohort's *minimum*
60-session traded value (~₹70 crore/day) that is a 0.36% participation rate, so the
cap is **non-binding across all 3,900 cohort rows** — measured, not assumed. It is
still evaluated and reported per event, so it would become visible if a later
cohort were thinner.

## Reproducibility notes attached to this amendment

- The power calculation in §6 is reproducible from `data/analysis/prices.sqlite` and
  `data/event_research/cohort_*.csv` with a fixed seed; it reads no filing table.
- Prices are joined on **ISIN issuer prefix (first 9 characters)**, never full ISIN: 44 of
  the 597 cohort issuers carry more than one ISIN in the panel because a face-value change
  mints a new one, and a full-ISIN join truncates their series mid-window. This is the
  fourth independent occurrence of that rule in this project.
- The trading calendar is `price_sessions` where `status = 'LOADED'`, which includes the
  six recovered weekend special sessions. Deriving the calendar from weekdays is wrong and
  has already manufactured ~9,800 false corporate actions once.
- Returns are corporate-action adjusted from the announcement feed, using only the 281 of
  286 validated actions; the 5 stored `DISAGREE` are excluded from adjustment rather than
  smoothed.
