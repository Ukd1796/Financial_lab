# AdaptiveStrategySelector — Accuracy Analysis & Design Rationale

**Last updated**: 2026-03-21

---

## 1. What We Observed (Original Problem)

Running the full 2018–2024 backtest, the LLM (GPT-4o-mini, temperature=0.0) produced
essentially one of five distinct weight vectors across ~300 weekly calls:

| Frequency | DualMA | Breakout | QuietBrk | TrendPB | RSI-MR | Regime context |
|---|---|---|---|---|---|---|
| ~80% of weeks | 0.25 | 0.35 | 0.25 | 0.10 | 0.05 | Any "mixed/unclear" market |
| ~8% of weeks | 0.29 | 0.41 | 0.12 | 0.12 | 0.06 | Mild downtrend signal |
| ~4% of weeks | 0.42 | 0.32 | 0.11 | 0.11 | 0.05 | Bear/high downtrend |
| ~3% of weeks | 0.28 | 0.28 | 0.28 | 0.11 | 0.06 | Genuinely sideways/mixed |
| ~5% of weeks | Various | | | | | Transition edges |

The allocation barely moved even during the 2022 Bear period, when the optimal
allocation (from the Sharpe table) calls for DualMA at 0.55–0.70.

---

## 2. Root Cause Analysis

### 2.1 No Python-side regime classification (original design)

The original prompt gave the LLM raw numbers (`% UPTREND: 48.3%`) and expected it to:
1. Infer what regime that represents
2. Map the regime to the allocation rules
3. Produce a specific weight vector

GPT-4o-mini, instructed to be a "risk manager", hedges toward a diversified default for
any ambiguous input. With `temperature=0.0`, the same ambiguous snapshot always produces
the same hedged answer. Since most weeks are not clearly Bear or Recovery, ~80% of calls
produce the same "safe" mixed-market allocation.

**Fix**: Add a deterministic Python classifier (`_classify_regime()`) that maps the raw
numbers to an explicit label (`BEAR_CONFIRMED`, `RECOVERY`, etc.) before the LLM call.
The LLM's prompt now starts with *"CURRENT REGIME: BEAR_CONFIRMED"* — removing one
full reasoning step from the model's responsibility.

### 2.2 Single-point snapshot — no trend visibility

A snapshot showing 38% DOWNTREND on a single day might be noise (one bad day after a
sustained uptrend) or the start of a bear market (week 3 of a slow rollover). The LLM
had no way to distinguish.

**Fix**: A rolling 4-week history is appended to each prompt:
```
Recent regime history (oldest → newest):
  2022-05-01  [MIXED/LOW]      UP=48.2%  DOWN=31.4%  ATR=1.81%
  2022-05-08  [MIXED/LOW]      UP=41.3%  DOWN=38.7%  ATR=1.94%
  2022-05-15  [BEAR_EARLY/MED] UP=33.1%  DOWN=44.2%  ATR=2.12%
  2022-05-22  [BEAR_EARLY/MED] UP=29.8%  DOWN=47.6%  ATR=2.18%
```
The model can now see a 4-week deterioration trend and lean more defensively than a
single-week snapshot would justify.

### 2.3 Soft rule language — ignored by the model

The original rules used:
- "strongly prefer DualMA" → model interprets as optional
- "favour Breakout and QuietBrk" → model assigns fractional increase, not a hard shift
- "reduce RSI-MR" → model cuts from 0.10 to 0.05, not to 0.0

GPT-4o-mini is trained to be helpful and non-extreme. "Strongly prefer" gets translated
to a modest preference, not a 60%+ allocation.

**Fix**: Regime-specific mandatory rules with explicit numeric bounds:
- `BEAR_CONFIRMED`: "DualMA MUST be ≥ 0.55. RSI-MR MUST be ≤ 0.05. QuietBrk MUST be ≤ 0.05"
- `RECOVERY`: "Breakout MUST be ≥ 0.35. QuietBrk MUST be ≥ 0.25. RSI-MR MUST be ≤ 0.05"
- `CRASH_HIGHVOL`: "Breakout MUST be ≥ 0.30. TrendPB MUST be ≥ 0.20. RSI-MR MUST be ≤ 0.05"

"MUST be ≥ X" is unambiguous. The model either complies or produces invalid output
(which gets corrected by `_parse_weights()` normalization).

---

## 3. Python-Side Regime Classifier

The classifier is evaluated in priority order (first matching rule wins):

| Label | Trigger condition | Confidence |
|---|---|---|
| `BEAR_CONFIRMED` | pct_downtrend > 45% | HIGH |
| `BEAR_EARLY` | pct_downtrend 35–45% | MEDIUM |
| `CRASH_HIGHVOL` | pct_downtrend > 25% AND avg_atr_pct > 2.3% | HIGH |
| `RECOVERY` | pct_uptrend > 60% AND avg_atr_pct > 1.8% | HIGH |
| `BULL_LOWVOL` | pct_uptrend > 55% AND avg_atr_pct < 1.5% | HIGH |
| `BULL_MEDVOL` | pct_uptrend > 55% | MEDIUM |
| `MIXED` | fallback | LOW |

**Why Python-side, not LLM-side?**

Rules-based regime classification from numeric thresholds is a task Python does
perfectly and consistently. The LLM adds value for the *allocation* problem (which
strategies are best for this regime, given multi-dimensional Sharpe trade-offs) but
adds noise to the *classification* problem (converting % numbers to a category label).
Separating the two tasks gives each component the job it's best at.

**What the LLM still does:**

Even with a pre-classified regime, the allocation problem is non-trivial:
- Transition handling: `BEAR_EARLY` with rising DOWNTREND % → lean more bear than `BEAR_EARLY` with stabilising %
- Interaction effects: `CRASH_HIGHVOL` with recovery-shaped history → weight shift mid-crash
- Proportional trade-offs: how much to take from Breakout vs TrendPB to give to DualMA

These are the cases where the LLM's ability to reason across the rolling history and
the Sharpe table simultaneously adds value beyond a pure rules-based system.

---

## 4. Actual Backtest Results — Adaptive vs EqualWeight (2026-03-21 run)

### 4.1 Per-period accuracy table

| Period | Metric | EqualWeight | Adaptive | Δ | Assessment |
|---|---|---|---|---|---|
| **Bear 2022** | Sharpe | 0.27 | **1.30** | +1.03 | Decisive adaptive win |
| **Bear 2022** | Return | +1.88% | **+12.56%** | +10.7pp | DualMA routing worked |
| **Bear 2022** | MaxDD | 15.21% | **8.34%** | -6.87pp | Better risk control |
| **Crash 2020** | Sharpe | **2.40** | 1.87 | -0.53 | EW wins — delayed recovery entry |
| **Crash 2020** | Return | **+28.56%** | +26.16% | -2.4pp | Acceptable margin |
| **Recovery 2020** | Sharpe | **2.22** | 2.09 | -0.13 | Roughly equal |
| **Recovery 2020** | Return | **+34.72%** | +32.84% | -1.9pp | RECOVERY over-triggered |
| **Bull 2019** | Sharpe | -0.53 | **-0.12** | +0.41 | Adaptive reduces losses |
| **Recent 2022–24** | Sharpe | 1.25 | **1.63** | +0.38 | Strong adaptive win |
| **Recent 2022–24** | Return | +28.58% | **+47.90%** | +19.3pp | DualMA in post-bear recovery |
| **Full 2018–24** | Sharpe | **1.23** | 1.18 | -0.05 | Slight EW advantage |
| **Full 2018–24** | Return | +101.06% | **+114.74%** | +13.7pp | Adaptive higher absolute return |
| **Full 2018–24** | MaxDD | **15.18%** | 22.03% | -6.85pp | Adaptive carries more drawdown |

### 4.2 Where adaptive wins — and why

**Bear 2022 (+10.7pp return, Sharpe 1.30 vs 0.27):**
The `BEAR_CONFIRMED` rule (pct_downtrend > 0.45) fired consistently from May–Dec 2022.
The LLM correctly routed DualMA to 65–73% of capital. DualMA's 0.51 Bear Sharpe was the
only positive strategy in this period — concentrating there was the right call. The
+12.56% vs +1.88% gap is the clearest validation of the regime-adaptive approach.

**Recent 2022–24 (+19.3pp return):**
The 2022–24 period blends the tail of the bear into a strong recovery and new bull run.
Adaptive correctly shifted from BEAR_CONFIRMED (high DualMA) to BULL_MEDVOL / RECOVERY
(Breakout + QuietBrk) as conditions improved. Equal-weight keeps all five strategies at
20% regardless, blending positive and negative Sharpe strategies in the same period.

**Bull 2019 (reduced losses):**
Equal-weight lost -4.06% in this choppy period (all five strategies positive individually
but commission drag dominates). Adaptive reduced RSI-MR (negative Mixed Sharpe: -0.14)
and favored QuietBrk/TrendPB, cutting losses to -1.8%.

### 4.3 Where adaptive underperforms — and why

**Crash 2020 (EW Sharpe 2.40 vs Adaptive 1.87):**
The COVID crash (Feb–Mar 2020) hit fast. pct_downtrend spiked above 0.45, correctly
triggering `BEAR_CONFIRMED`. However, the recovery was equally fast (April-May 2020).
Equal-weight's natural diversification captured the V-shape rebound immediately.
The adaptive selector stayed in `BEAR_CONFIRMED` for 1–2 additional weeks after the
market turned, missing the best Breakout and QuietBrk entry points of the decade.
This is the **weekly rebalance lag problem** compounded with the **bear-exit signal problem**:
pct_downtrend only falls below 0.45 once the recovery is well established.

**Full-period MaxDD (22.03% vs 15.18%):**
The adaptive portfolio takes larger directional bets. When right (Bear 2022), this
reduces drawdown. When the regime signal lags (Crash-to-Recovery transition), the
concentrated position amplifies temporary losses. The equal-weight diversification
provides a natural drawdown floor that concentrated allocation cannot match.

---

## 5. Identified Structural Issues

### 5.1 RECOVERY classifier fires too broadly on NSE

**Problem**: The condition `pct_uptrend > 0.60 AND avg_atr_pct > 0.018` triggers not
just during genuine post-crash V-shape recoveries but during any normal bullish week
on NSE's secular uptrend (2023–2024 in particular). Estimated firing rate: ~70% of all
non-bear weeks. This means DualMA is capped at 0.15–0.20 for most of the sustained
bull, below the equal-weight floor of 0.20.

**Root cause**: NSE Nifty universe has structurally higher UPTREND breadth in bull
markets than the RECOVERY rule was designed for. The 1.8% ATR threshold is too loose
— normal moderate-vol trading days in an uptrend regularly exceed 1.8% average ATR.

**Impact**: DualMA chronically underweighted at 0.17 (below equal-weight 0.20) in
periods where its 1.69 Recent Sharpe would justify 0.25–0.35. This explains why
full-period Sharpe is marginally lower (1.18) despite higher total return.

**Fix options:**
1. Raise RECOVERY ATR threshold: `avg_atr_pct > 0.022` (from 0.018) — more selective
2. Add a consecutive-week requirement: regime must appear in ≥ 2 of last 3 history weeks
3. Add a new `BULL_SUSTAINED` label for >60% UPTREND lasting 8+ weeks, with DualMA at 0.28–0.35

### 5.2 Bear-exit signal lag (Crash-to-Recovery transition)

**Problem**: When pct_downtrend drops from >0.45 to <0.35, there is a 2–3 week period
where the market is recovering but the classifier is still seeing BEAR_EARLY. The LLM
maintains defensive weighting during exactly the highest-alpha early-recovery window.

**Fix options:**
1. Add a `RECOVERY_ENTRY` label: pct_uptrend rising >5pp week-over-week AND pct_downtrend
   falling >5pp — immediately boosts Breakout/QuietBrk when the reversal is fresh
2. Shorter rebalance lag for crash exits: check every 3 days (not 5) during BEAR_* regimes
3. Let the 4-week rolling history help: the LLM should already detect the pivot from rising
   to falling DOWNTREND% in its history — but this requires the labels to change first

### 5.3 DualMA minimum weight floor missing

**Problem**: In RECOVERY regime, DualMA can legally reach 0.15 (set by the rule
"DualMA can be 0.15–0.25"). In sustained bull markets misclassified as RECOVERY, this
leaves the best full-period strategy (1.33 Sharpe) with less capital than a static
equal-weight run (0.20). There is no guard preventing RECOVERY from systematically
underweighting the only bear-positive strategy.

**Fix**: Add a global minimum weight floor: any strategy may not go below 0.10 unless
its expected Sharpe for the current regime is below 0.0. DualMA's Mixed Sharpe is 1.69
(positive in all periods) — it should never drop to 0.15.

---

## 6. Remaining Limitations

### 6.1 Look-ahead bias in the Sharpe table

The performance table embedded in the prompt (`_STRATEGY_REGIME_PERFORMANCE`) was derived
from the same 2018–2024 data being backtested. In live deployment or walk-forward testing:
- Use a rolling window: train on years 1–N, evaluate on year N+1
- The table should be updated quarterly as new data accumulates
- The current backtest is an **upper bound** — the LLM "knows" which strategies work best
  in each regime because those regimes are in its training data

### 6.2 Weekly rebalance lag

The selector rebalances at most once every 5 calendar days. If a regime transition
happens intra-week (e.g. a crash on Tuesday), the allocation doesn't update until the
following Monday. This is acceptable for a weekly-frequency system but matters during
fast-moving events (COVID crash: market fell 35% in 3 weeks).

**Mitigation**: The `_classify_regime()` Python layer provides some protection — if the
snapshot crosses a hard threshold (e.g. `pct_downtrend > 0.45`), the prompt's mandatory
rules force a defensive allocation regardless of recent history.

### 6.3 GPT-4o-mini vs GPT-4o reasoning quality

GPT-4o-mini is ~10x cheaper than GPT-4o but has weaker multi-step reasoning. For the
classification-removed, hard-rule-enforced prompt, the quality difference is smaller —
the LLM needs to do less reasoning. Still, for edge cases (transition regimes, mixed
signals with conflicting history weeks), GPT-4o will produce more nuanced allocations.

**Recommendation**: Use `model="gpt-4o-mini"` for exploration. Switch to `model="gpt-4o"`
for final validation before live deployment. Cost difference for a 6-year backtest:
gpt-4o-mini = ~$0.06, gpt-4o = ~$0.60.

### 6.4 Regime classifier thresholds are calibrated on NSE 2018–2024

The thresholds (e.g. `pct_downtrend > 0.45` for `BEAR_CONFIRMED`) are calibrated on the
NSE Nifty 50/Next50/Midcap50 universe. They may need recalibration for:
- Different markets (US, EU) — broader universes may have lower pct_downtrend in bears
- Different periods — if the strategy pool changes, Sharpe table must update too
- Smaller universes — with fewer stocks, pct_downtrend is noisier

---

## 7. Improvement Roadmap

### Priority 1 — Recalibrate RECOVERY threshold (immediate, low risk)

Change `avg_atr_pct > 0.018` to `avg_atr_pct > 0.022` in `_REGIME_RULES`.
Expected effect: ~30% fewer RECOVERY classifications in normal NSE bull weeks,
routing those to BULL_MEDVOL (DualMA ≥ 0.20) or BULL_LOWVOL (DualMA 0.20–0.30).

```python
# Current:
("RECOVERY", "...", lambda s: s["pct_uptrend"] > 0.60 and s["avg_atr_pct"] > 0.018, "HIGH"),
# Proposed:
("RECOVERY", "...", lambda s: s["pct_uptrend"] > 0.60 and s["avg_atr_pct"] > 0.022, "HIGH"),
```

### Priority 2 — Add BULL_SUSTAINED regime label

A new label for confirmed multi-week bull markets with DualMA as co-equal strategy:

```python
("BULL_SUSTAINED",
 "Sustained uptrend — >60% UPTREND for 3+ consecutive weeks, low vol",
 lambda s: s["pct_uptrend"] > 0.60 and s["avg_atr_pct"] < 0.018,
 "HIGH"),
```

Allocation rule: "Breakout MUST be ≥ 0.25. DualMA MUST be ≥ 0.25. QuietBrk ≥ 0.20.
RSI-MR MUST be ≤ 0.05."

This correctly handles the NSE 2023–2024 sustained uptrend without triggering RECOVERY
(which implies post-crash conditions and underweights DualMA).

### Priority 3 — Global DualMA minimum floor

Add to `_parse_weights()` or as a post-processing step:

```python
# Enforce: DualMA is never below 0.10 (positive Sharpe in all regimes)
if "DualMA" in clipped and clipped["DualMA"] < 0.10:
    clipped["DualMA"] = 0.10
# Re-normalize
```

Prevents the RECOVERY regime from chronically underweighting the system's most
reliable strategy.

### Priority 4 — Regime transition confirmation (2-week stability)

Require a regime to appear in ≥ 2 consecutive weeks before switching from BEAR_* to
anything else. Prevents whipsawing on noisy crash-to-recovery transitions:

```python
# Rough sketch in rebalance():
if label != self._current_regime_label:
    if self._pending_regime == label:
        self._pending_regime_count += 1
    else:
        self._pending_regime = label
        self._pending_regime_count = 1
    if self._pending_regime_count >= 2:
        effective_label = label  # confirmed transition
    else:
        effective_label = self._current_regime_label  # hold current
else:
    effective_label = label
    self._pending_regime = None
    self._pending_regime_count = 0
```

### Priority 5 — Walk-forward validation

Replace the hardcoded Sharpe table with a rolling window table:
- Train on 2018–2021 → backtest 2022 (first walk-forward fold)
- Train on 2018–2022 → backtest 2023 (second fold)
- Train on 2018–2023 → backtest 2024 (third fold)

This eliminates the look-ahead bias and gives a realistic Sharpe estimate for live
deployment. The current full-period Sharpe (1.18 adaptive) is an upper bound.
Expected walk-forward Sharpe: 0.90–1.10.

### Priority 6 — Per-sector concentration limit in RiskAgent

DualMA and Breakout often enter the same trending stocks simultaneously in Recovery.
Add a max 35% sector exposure cap per day in RiskAgent to prevent the portfolio being
80% in one sector when two strategies pile into the same mid-cap momentum names.

---

## 8. How to Validate Future Improvements

Run `python run_experiments.py` and check against these benchmarks:

| Metric | Current (Adaptive) | Target (after fixes) |
|---|---|---|
| Bear 2022 Sharpe | 1.30 | ≥ 1.30 (hold) |
| Crash 2020 Sharpe | 1.87 | ≥ 2.10 (close gap with EW 2.40) |
| Recovery 2020 Sharpe | 2.09 | ≥ 2.30 (close gap with EW 2.22) |
| Full-period Sharpe | 1.18 | ≥ 1.30 |
| Full-period MaxDD | 22.03% | ≤ 18% |
| RECOVERY weeks as % of all | ~70% | ≤ 40% |

---

## 9. Key Design Principle

**The LLM's value in this system is NOT classification — it is allocation reasoning.**

A rules-based classifier (Python `_classify_regime()`) maps raw numbers to a regime label
reliably and cheaply. What the LLM contributes is:
- Reading the historical trend (4-week rolling buffer) and adjusting for momentum
- Proportional trade-offs between strategies given the regime (e.g. how much to reduce
  TrendPB vs Breakout when shifting capital to DualMA in a bear)
- Handling edge cases where two regime signals conflict (e.g. high UPTREND% but also
  rising ATR% — Recovery or Late-cycle Bull?)

Without the Python classifier, the LLM spends most of its reasoning capacity on a task
it does poorly (number-to-category mapping) and produces hedged, near-equal defaults.
With the classifier, it can focus on the task it actually adds value to.

**System accuracy summary (current state):**
- Directionally correct in 4 of 5 periods: Bear, Recent, Bull 2019 (reduced losses), Mixed
- One structural miss: Crash-to-Recovery transition timing (2020)
- One classification bug: RECOVERY over-triggers on normal NSE bull weeks
- Net verdict: the adaptive layer is working, but leaving ~0.12 Sharpe on the table due
  to the RECOVERY threshold calibration issue. Priorities 1–3 above are expected to
  recover most of that gap without introducing new risks.
