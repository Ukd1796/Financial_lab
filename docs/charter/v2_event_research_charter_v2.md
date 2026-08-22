# V2 Event Research Charter — Amendment v2

**Dated: 2026-08-12.** Amends `docs/v2_event_research_charter.md` under its §9.

**Status when written: NO surprise, response, forward return or score has been computed.**
Phase-1 work to date is data-quality only (coverage, timestamps, parser accuracy, outcome
labels). This amendment is therefore written *before* any result it could be tuned against,
which is the only condition under which it means anything.

Evidence for every claim below is in `docs/research_log.md`, entries dated 2026-08-10 to
2026-08-12.

---

## Summary

| # | Change | Verdict |
|---|---|---|
| 1 | §3 primary signal: seasonal surprise → actual-vs-consensus | **REJECTED** — the data does not exist at this universe size |
| 2 | §6 fold structure | **AMENDED** — the original is impossible; the dev block is 0% usable |
| 3 | Governance red-flag gate | **REJECTED for V2.0** — conflicts with §3's anti-fishing clause |
| 4 | §7 universe scope: NSE-only → NSE ∪ BSE | **AMENDED** — for delisting labels only |

Two of four proposed changes are rejected. That is the point of writing it down first.

---

## 1. §3 primary signal — NO CHANGE. Seasonal surprise stands.

**What was proposed.** §3 freezes the primary input as *"seasonally differenced EPS from the
same fiscal quarter one year earlier."* It was proposed to replace this with actual-vs-consensus
surprise (SUE), on the grounds that the seasonal definition was a workaround for having no
analyst estimates, and that `/stock_forecasts` now supplies them with `SurprisePercent`,
`StandardizedUnexpectedEarnings` and a report timestamp.

**Why it is rejected.** Measured 2026-08-12 on 20 cohort members sampled across the whole
liquidity range (ranks 1–500), one `/stock_forecasts` call each, `period_type=Interim`:

| | |
|---|---|
| Names with **zero** usable quarterly surprises | **10 of 20 (50%)** — including **HDFCBANK, rank 1** |
| Median usable quarters per name | **2** |
| Median analysts per quarterly estimate | **3** |
| Best observed depth (RELIANCE) | 9 usable quarters, 4–7 analysts |

Indian quarterly analyst coverage is too thin to define a market expectation. A "consensus" of
three analysts is not the market's view; it is three people's view, and standardising against
it would inject more noise than it removes. It would also cut the tradeable universe roughly
in half and shorten the usable history from 13 quarters to about 8.

**Conclusion: the charter's original definition was not a compromise — it is the only
expectation model that works at this universe size.** The seasonal method needs nothing but
the issuer's own history, which is available 13 quarters deep for essentially every name
(8/8 in the source test, 95% coverage even on delisted names).

**Recorded as a rejected alternative** so it is not re-proposed: annual consensus *is* well
covered (29–31 analysts), but an annual signal cannot drive a 20-session event sleeve.

## 2. §6 fold structure — AMENDED, because the original is impossible

**Original.** Development 2018–2022 / validation 2023–2024 / confirmation 2025–2026.

**Why it cannot stand.** The full-window XBRL sweep (2026-08-10, 663 events, 467 exceptions)
found usable-filing rates by dissemination year of **2019: 0%, 2020: 0%, 2021: 0%, 2022: 0%,
2023: 65%, 2024: 100%, 2025: 100%**. The entire development block is unusable — NSE instances
reference base contexts (`OneD`, `FourD`) the documents never define, so headline EPS cannot be
tied to a period from the filing itself.

**Replacement.** Point-in-time evidence is restricted to what the filings actually support:

| Fold | Window | Role |
|---|---|---|
| A | 2023 H2 – 2024 H2 | Development. Every design choice is fixed here |
| B | 2025 H1 – 2025 H2 | Validation. One pass only |
| C | 2026 H1 – forward | Confirmation, and the ongoing forward shadow run |

**Consequences stated in advance, not after a disappointing result:**

- This is **~10–12 quarters, not five folds.** §8's "positive in at least four of five
  chronological folds" is unachievable and is replaced in §3 below.
- The binding constraint is the number of **independent time periods (~10)**, not the number of
  events (~500 names × ~13 quarters). Earnings cluster into the same six-week windows, so
  events within a season share market conditions and do not count as independent observations.
- The window contains **only survivors of a cohort formed at its start**, by construction.
  Cohorts must be rebuilt as-of the window start or rolled per quarter.
- **A negative or inconclusive result on this sample is the expected outcome and must be
  reported as such.** A short sample is a reason to disbelieve a positive result, not a reason
  to relax the bar.

**Amended §8 pass bar.** Replacing conditions 2 and 3, leaving 1 and 4 intact:

1. *(unchanged)* Exceed **2× modelled round-trip cost** in net 20-session sector-adjusted return.
2. *(amended)* Positive in **fold A and fold B independently**, with fold B run exactly once.
3. *(amended)* No more than **40% of the aggregate result from one sector or one calendar
   quarter** (was: one calendar year — tightened because the sample is shorter).
4. *(unchanged)* Retain its sign in the fold-C confirmation period.
5. *(new)* Report the result **with and without** the delisted/collapsed population. A sleeve
   that only works when failures are excluded has not been demonstrated.

Failure on any condition ends V2.0, as before.

## 3. Governance red-flag gate — REJECTED for V2.0

**What was proposed.** An exclusion gate built on `ratios`, `cashflow` and quarterly
shareholding — e.g. skip the long side where working-capital days or cash-conversion cycle are
deteriorating.

**Why it is rejected.** §3 already anticipates precisely this:

> Revenue, EBITDA/PBIT and PAT will be stored during Phase 1 as data-quality fields. They are
> not allowed in the primary score. This avoids silently trying many "fundamental quality"
> combinations until one wins.

A gate is not the primary score, but it is adjacent to it and introduces exactly the degrees of
freedom that clause exists to prevent — every threshold is a free parameter, and a short sample
cannot pay for them. The supporting data is also **annual**, so on a 20-session horizon it
would be up to twelve months stale at the moment of use.

**Deferred to V2.1**, admissible only if V2.0 clears its bar first, and then only with
thresholds fixed and dated before evaluation. The data continues to be collected and stored
meanwhile; nothing is lost by waiting.

## 4. §7 universe scope — AMENDED for outcome labels

Delisting labels were derived from NSE bhavcopies alone. Measured 2026-08-12 against a BSE
bhavcopy: of 662 NSE exits, **288 (44%) still trade on BSE under the same ISIN** and 52 (8%)
under a successor ISIN — only **322 (49%) are genuinely absent from both**.

Amendment: **"delisted" means absent from NSE *and* BSE.** BSE publishes a free, unauthenticated
bhavcopy in the identical UDiFF schema, so this costs nothing but the union.

Unchanged: the **collapse label is drawdown-based and measures price experience**, so it is
unaffected — a −90% fall is a −90% fall wherever the name later trades. Only the mortality
statistic was overstated.

---

## Reproducibility notes attached to this amendment

- Identity is keyed on **ISIN issuer prefix (first 9 chars) plus a surviving sibling
  instrument**, not on symbol and not on full ISIN. Symbol alone misreads 102 renames as
  deaths; full ISIN alone misread 318 face-value changes as deaths.
- A surviving issuer code does **not** rescue a name whose exit was a collapse. DHFL's prefix
  now belongs to PIRAMALFIN, which absorbed it through insolvency: the entity continued, the
  equity was destroyed. We label what a holder experienced, not legal identity.
- `INF*` ISINs are mutual-fund and ETF units and are excluded from the equity universe.
- Vendor fundamentals are restated and carry no publication timestamp
  (`is_point_in_time=False`). They are admissible for the forward run and for data-quality
  work, and **inadmissible for measuring a historical edge**. The NSE filing archive remains
  the only point-in-time source.

## Open item, deliberately not decided here

Half-yearly balance-sheet and cash-flow items **are** present in NSE filings
(`TradeReceivablesCurrent`, `Inventories`, `TradePayablesCurrent`, `Borrowings*`,
`CashAndCashEquivalents`, full cash-flow statement — 215 elements observed). That is twice the
vendor's annual resolution *and* genuinely as-filed. Whether to build that parse path is a
V2.1 question and is not part of the V2.0 pass bar.
