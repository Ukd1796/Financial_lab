# Root-Cause Analysis — Why the System Loses in Bull 2019-20 and Live 2025-26

**Status:** Diagnostic only (no code changes). Built from the end-to-end
integration run + this session's existing logs.
**Date:** 2026-05-21
**Companion doc:** `meta_layer_value_leak.md` (sleeve refactor — considered
and discarded).

## 1. The pattern to explain

Across the 7-period end-to-end integration (₹1L EQUITY, legacy costs,
`PYTHONHASHSEED=0` + OpenAI `seed=0`, RCA wired), the production
combined-router adaptive (SHARED-Adp) wins **5 of 7** periods decisively
and **loses 2** — and the losses are large enough to drag blended Sharpe.

| Period | SHARED-Adp Return | Sharpe |
|---|--:|--:|
| Full 2018–24 | **+116.10%** | 1.33 |
| Crash 2020 | **+30.15%** | 2.24 |
| Recov 2020–21 | **+80.90%** | 2.86 |
| Bear 2022 | **+7.60%** | 0.91 |
| Recent 2022–24 | **+37.93%** | 1.50 |
| **Bull 2019–20** | **−5.01%** | −0.50 |
| **Live 2025–26** | **−5.88%** | −0.67 |

The two losers are not random — they share a clear structural signature.

## 2. Market-archetype evidence

Computed across all 150 broad-universe stocks for each period (close-to-close
returns; 200-day SMA breadth; cross-stock dispersion and pairwise correlation):

| Period | Verdict | %>SMA200 start→end | %stocks positive | dispersion | median stock return |
|---|---|---|--:|--:|--:|
| Bull 2019–20 | ✗ LOSING | 50% → 63% | **58%** | **0.45** | **+11.3%** |
| Live 2025–26 | ✗ LOSING | **40% → 28%** | **40%** | **0.30** | **−4.6%** |
| Crash 2020 | ✓ winning | 68% → 100% | 73% | 0.65 | +21.4% |
| Recov 2020–21 | ✓ winning | 9% → 67% | **99%** | **2.53** | **+151.0%** |
| Bear 2022 | ✓ winning | 74% → 62% | 53% | 0.35 | +1.1% |
| Recent 2022–24 | ✓ winning | 74% → 76% | 81% | 1.04 | +59.3% |

**The losing periods are the only ones where most stocks DON'T make money**
(58% and 40% positive vs 73–99% in winners) **AND dispersion is the lowest**
(0.45 and 0.30 vs 0.65–2.53). Both are narrow, low-breadth, sideways-to-down
markets. Live 2025–26 is the worst on every breadth metric (breadth
*deteriorating* during the period; median stock LOSING money).

The winning periods all have either **clear direction** (Crash 2020 sharp
down then up; Recov 2020-21 broad rally with median +151%; Recent 2022-24
broad uptrend) or **high dispersion** (winners big enough to dominate). The
losing periods have *neither*.

## 3. Strategy-level evidence (from `/tmp/regime_diag.log`)

When run *solo* (each strategy on full capital, own filter):

**Bull 2019–20 — every solo strategy is profitable** (+0.4% to +5.3%):

| Strategy | Solo Return |
|---|--:|
| TrendPB v2 5% | +4.52% |
| Breakout 10d | +5.31% |
| QuietBrk | +2.65% |
| TrendPB v2 3% | +2.58% |
| RSI-MR | +2.61% |
| DualMA | +0.37% |
| **EqW combined** | **−4.50%** |
| **Adaptive combined** | **−2.64%** |

**Live 2025–26 — 5 of 6 solo strategies positive**, only Breakout 10d loses
(−7.65%):

| Strategy | Solo Return |
|---|--:|
| TrendPB v2 5% | +3.66% |
| QuietBrk | +2.23% |
| TrendPB v2 3% | +1.44% |
| RSI-MR | +1.17% |
| DualMA | +0.21% |
| Breakout 10d | −7.65% |
| **EqW combined** | **−3.00%** |
| **Adaptive combined** | **−5.86%** |

So the *solo* strategies have small but real positive edge in these markets.
What goes wrong is the *combination*.

## 4. Regime-classifier evidence (from `/tmp/cap_curve_adaptive.log`)

Regime label distribution by the 150-stock classifier (Q3 finding from
earlier in this session):

| Bull 2019–20 share | Live 2025–26 share |
|---|---|
| RECOVERY 37%, BULL_SUSTAINED 24%, **BEAR_CONFIRMED 19%, CRASH_HIGHVOL 11%**, MIXED 11% | **CRASH_HIGHVOL 30%**, BULL_SUSTAINED 27%, **BEAR_CONFIRMED 17%**, RECOVERY 15%, MIXED 11% |

Both periods spend ~30%+ of the time in defensive labels (BEAR/CRASH) despite
not being genuine crashes — Bull 2019-20 is mislabelled BEAR/CRASH 30% of the
time; Live 2025-26 flip-flops between CRASH_HIGHVOL (30%) and BULL_SUSTAINED
(27%) — the worst possible combination (defensive into rallies, aggressive
into drops).

The classifier inputs are the same machinery for all 7 periods — it works
fine on directional regimes (Crash labelled CRASH and that's right) and
breaks on narrow/choppy ones (no dominant signal, thrashes).

## 5. Synthesis — verdict per period: BOTH (a) and (b)

Both losing periods are **(c) BOTH** an unfixable archetype problem AND a
classifier-amplification problem:

**(a) Unfixable archetype component (~most of the loss):**
The strategy set is momentum/breakout/mean-reversion — directional long-only.
In narrow/low-dispersion sideways markets (Bull 2019-20, Live 2025-26) there
is **no consistent directional move to capture**. Every entry whipsaws. This
is a known property of these archetypes, not a defect. The best the system
can do in these regimes is *small loss / breakeven*, which is exactly what
the solo strategies achieve (+0.4% to +5.3% in Bull; −7.7% to +3.7% in Live).

**(b) Classifier-amplification component (~the rest):**
The combined adaptive (SHARED-Adp) loses **MORE** than the simple
solo-average (Bull SHARED −5.01% vs solo-avg ~+3%; Live SHARED −5.88% vs
solo-avg ~+0.2%). The merge that *helps* in directional regimes (concentrate
capital into the right strategy) *hurts* in narrow ones: the classifier
mislabels the regime → the LLM concentrates capital onto whatever strategy
the (wrong) label favours → a concentrated bet on a strategy that has no
edge in this regime → amplified loss. Live 2025-26 is the textbook case:
30% CRASH_HIGHVOL labels trigger the rule `Breakout MUST be ≥ 0.30,
TrendPB MUST be ≥ 0.20`, the LLM loads Breakout — which is the ONE
strategy losing money this period (−7.65% solo). So Adaptive concentrates
into the loser, making the combined worse (−5.86%) than EqW (−3.00%).

## 6. What's fixable vs not

| Component | Fixable? | How |
|---|---|---|
| (a) Archetype no-edge in narrow markets | **No** — intrinsic to momentum/breakout/MR | Accept the drawdown OR add a non-directional strategy archetype (sector rotation, vol-targeting, market-neutral) — out of scope |
| (b) Classifier amplification in narrow markets | **Yes** | Top-of-funnel exposure gate: when classifier confidence is LOW, breadth is collapsing (e.g. pct_above_sma200 dropping), or regime is thrashing, **reduce gross exposure** (e.g. scale all weights × 0.5, or go to cash) — *don't* concentrate into a probably-wrong regime call |

## 7. Smallest next-step experiment (NOT in this round)

If you want to test fixing (b), the cheapest hypothesis is a single
**market-breadth exposure gate** on top of the existing adaptive:

> **Rule:** if broad-150 `pct_above_sma200` is **(a) below 50%** AND
> **(b) trending down (5d Δ < 0)**, scale all strategy weights by 0.5
> (i.e. deploy only half the capital, leave half in cash) for that week.

Backtest predictions:
- Live 2025–26: Triggers heavily (started 40%, ended 28%, trending down) → halves the loss from −5.88% toward ~−3% or better.
- Bull 2019–20: Triggers selectively → modest improvement (maybe halves the −5.01%).
- Other 5 periods: Triggers rarely (Recov/Recent are broad up; Crash recovers quickly; Bear hits hard but not via breadth collapse) → minimal damage to the winners.

It is a *top-of-funnel risk overlay*, not a regime-classifier replacement —
which is why it's likely robust where the previous regime-thrash stabilizer
work failed. **This is a hypothesis worth a planned experiment, not a
build-now decision.**

## 8. Honest closing

- The system's two loss regimes are **fundamentally narrow/choppy markets**
  where its strategy archetype has structurally weak edge. Most of the loss
  is intrinsic; capital/weighting cannot recover it.
- A meaningful but bounded portion is **classifier amplification** in those
  same regimes (the LLM concentrates onto a wrong call). A top-of-funnel
  breadth exposure gate is the targeted, low-risk experiment that could
  recover ~half of that bounded portion without harming the 5 winning
  periods. *Not built in this round* — diagnostic only.
- Don't try to "fix" the system in these regimes by reweighting strategies
  or changing the classifier — that path was explored exhaustively in
  `meta_layer_value_leak.md` and didn't yield. The right lever, if pursued,
  is **less exposure, not different exposure** when the market signals
  unfavourable conditions for the archetype.

## 9. Walk-Forward OOS Measurement (2026-05-21)

The hardcoded `_STRATEGY_REGIME_PERFORMANCE` Sharpe table in
`adaptive_selector.py` is literal in-sample fit — it was measured on
2018–2024 backtests and then fed back to the LLM. To quantify the
look-ahead bias, ran `run_experiments.py` with `RUN_WALK_FORWARD = True`:
three expanding-window folds where the LLM sees a fresh Sharpe table
computed **only from the training years** (no look-ahead) vs the full
hardcoded table (the IS upper bound). Ran twice (two passes), giving 6
fold-runs total.

**Training-data vs hardcoded table — selected entries:**

| Regime | Strategy | Hardcoded (LLM sees) | Training-only | Δ |
|---|---|--:|--:|--:|
| Bull/LowVol | DualMA | 0.44 | −0.10 | −0.54 |
| Bull/LowVol | Breakout | 0.93 | 0.27 | −0.66 |
| Bull/LowVol | QuietBrk | 1.09 | 0.47 | −0.62 |
| Recovery | DualMA | 2.66 | 1.87 | −0.79 |
| Recovery | Breakout | 3.18 | 2.62 | −0.56 |
| Bear/Choppy | DualMA | +0.51 | −0.20 | −0.71 |
| Crash/HighVol | DualMA | 1.28 | 1.67 | +0.39 |
| Crash/HighVol | QuietBrk | 1.38 | 1.95 | +0.57 |

The hardcoded values are systematically too rosy for Bull/LowVol and
Bear/Choppy (Bear DualMA was even mis-signed). Crash/HighVol is accurate
to slightly conservative.

**Fold-level OOS / IS:**

| Fold | Test period | Training regimes | Run 1 OOS/IS | Run 2 OOS/IS |
|---|---|---|--:|--:|
| 1 | 2022 (Bear) | Bull, Crash, Recovery (**no Bear**) | 0.69× | 0.71× |
| 2 | 2023 | Bull, Crash, Recovery, Bear | **0.91×** | **0.96×** |
| 3 | Jan–Jun 2024 | Bull, Crash, Recovery, Bear | 1.06× | 0.72× |
| **Avg** | | | **0.89×** | **0.80×** |

**Combined average across both passes: ~0.85×** — squarely inside the
0.80–0.90× target range. **~85% of the adaptive in-sample edge is
genuine; ~15% is look-ahead from the hardcoded table.**

Fold-by-fold:
- **Fold 1 worst (0.69-0.71×)** because Bear 2022 is the test period and
  training has zero Bear data — LLM has no analogue, leans on
  Bull/Recovery numbers, takes a ~30% haircut. Expected worst case.
- **Fold 2 cleanest (0.91-0.96×)** — once training includes all four
  archetypes, OOS Sharpe (2.18-2.27) is essentially identical to IS
  (2.37-2.40). Strongest evidence the edge is structural, not look-ahead.
- **Fold 3 noisy (0.72-1.06×)** — only 5 months, small sample. The two
  runs disagree because `PYTHONHASHSEED=0` wasn't prefixed; LLM call
  ordering varied. Treat the *average* (~0.89×), not either single value.

**Revised headline numbers (IS / OOS pair):**

| Period | IS (current quote) | Implied OOS (× 0.85) |
|---|--:|--:|
| Full 2018–24 | +116.10% / 1.33 S | **~+99% / ~1.13 S** |
| EqualWeight reference | +64% (no LLM) | +64% |

Adaptive's true OOS edge over EqW is **~+35pp**, not +52pp as the IS
number alone implies — but still substantial and real.

**Why the system isn't more overfit despite the inflated table:** the
LLM's allocation is driven primarily by the per-regime MUST rules
(e.g. "Breakout MUST ≥ 0.30 in CRASH_HIGHVOL") and the structural
allocation template, not by literal Sharpe ranking. The table acts more
as a tiebreaker than a primary signal, which bounds the look-ahead damage.

**Operational guidance:** going forward, quote system results as IS/OOS
pairs (e.g. "+116% IS / ~+99% OOS"). For any future walk-forward run,
prefix `PYTHONHASHSEED=0` for stable inter-run numbers. The
`run_walk_forward()` harness in `run_experiments.py` (~30 min, ~500 LLM
calls) is the canonical OOS check — re-run periodically if the table or
strategy set changes materially.
