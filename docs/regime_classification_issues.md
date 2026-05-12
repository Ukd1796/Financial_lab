# Regime Classification Issues & Improvement Backlog

**Context:** During the May 2026 meta-layer review, backtesting the weight-ordering fix
(`engine.py` BUY sort, 2026-05-13) against `_ADAPTIVE_BASELINE` revealed that the
Recent 2022–2024 period regressed by -0.21 Sharpe. Investigation traced this to the
regime classifier calling `RECOVERY` in July 2022 while the Indian market was still in
a broad decline. Three structural causes were identified.

---

## Root Cause 1 — Small internal universe biases `pct_downtrend` upward

**File:** `app/meta/regime_snapshot.py`

The regime snapshot computes `pct_downtrend` from the active trading universe (~20
symbols after DynamicUniverse + UnionFilter). This is a survivorship-biased sample:
only stocks that passed momentum and liquidity screens make it into the 20, so the
active universe systematically skews toward relative winners even during a broad
market decline. A falling market can therefore look like RECOVERY simply because the
screener filtered out the worst performers.

**Evidence:** In the Recent 2022–2024 backtest, `CRASH_HIGHVOL` is correctly detected
Jan–Jun 2022, but the regime flips to `RECOVERY` by late July 2022 despite the Nifty
being ~15% below its Jan 2022 high at that point.

**Fix:** Use the broad 150-symbol universe from `RegimeContextAgent` for regime
detection, not the filtered ~20. `RegimeContextAgent` already tracks 150 symbols and
computes a trend signal (`IMPROVING` / `DETERIORATING` / `STABLE`). The live cron
already wires this up. The issue is that `run_ujjwal_baseline.py --adaptive` does
**not** pass a `regime_context_agent` to the backtest engine — so the test runner is
measuring a strictly worse configuration than what runs in production.

**Priority:** HIGH  
**Effort:** Low — wire `RegimeContextAgent` into `run_ujjwal_baseline.py --adaptive`  
**Expected impact:** Removes the primary cause of RECOVERY mislabels; aligns test with live

---

## Root Cause 2 — DOWNTREND classification uses short lookback (SMA-20 / short-term)

**File:** `app/meta/regime_snapshot.py`, `app/backtest/observer.py`

Each symbol is classified `DOWNTREND` based on short-term momentum indicators. When
the market bounces for even 2–3 weeks, enough symbols cross above their short-term MA
that `pct_downtrend` drops below the `CRASH_HIGHVOL` threshold, flipping the regime.
A 2–3 week bear market rally inside a year-long downtrend is not a recovery, but the
classifier treats it as one.

**Fix options (pick one):**

| Option | Description | Tradeoff |
|--------|-------------|----------|
| A | Use SMA-50 instead of SMA-20 for DOWNTREND classification | Slower to flip on genuine recoveries; more stable labels |
| B | Require `pct_downtrend` to stay below threshold for 2+ weeks before exiting CRASH (hysteresis band) | Targeted; minimal change to detection speed |
| C | Combine both: SMA-50 for label, 1-week hysteresis for CRASH→non-CRASH transitions | Most robust; more complex |

Recommended: **Option B** (hysteresis) as the lowest-risk change. The stability gate
(`regime_stability_weeks`) already handles entry into a new regime but does not apply
to exiting CRASH specifically.

**Priority:** HIGH  
**Effort:** Medium — modify `build_regime_snapshot()` or add hysteresis in `rebalance()`  
**Expected impact:** Reduces bear-market-rally mislabels; directly targets Recent 2022–2024 regression

---

## Root Cause 3 — LLM allocates at full weight immediately on week 1 of a new regime

**File:** `app/meta/adaptive_selector.py`

The `_confirmed_weeks` hint added in May 2026 tells the LLM "Week 1 = stay close to
equal weight." However the LLM does not apply this strictly — in the weight logs,
week-1 RECOVERY allocations are `Breakout=0.37, QuietBrk=0.26`, essentially the same
as a mature RECOVERY allocation. When the regime switch is a mislabel (e.g. a bear
rally), this full allocation is immediately harmful.

The issue is that a text hint is advisory; the LLM can and does ignore it.

**Fix:** Enforce the regime age constraint in code (hard blend) rather than as a
prompt hint. When `_confirmed_weeks == 1`, blend the LLM's proposed weights 50% toward
equal weight before passing them to the router:

```python
# In AdaptiveStrategySelector.rebalance(), after parsing LLM weights:
if self._confirmed_weeks == 1:
    n   = len(weights)
    eq  = 1.0 / n
    weights = {k: 0.5 * v + 0.5 * eq for k, v in weights.items()}
    weights = self._normalise(weights)
```

This is a guaranteed damp on week-1 allocations, regardless of what the LLM returned.
Week 2+ proceeds with full LLM weights as normal.

**Priority:** HIGH  
**Effort:** Very low — 4 lines in `rebalance()`  
**Expected impact:** Reduces week-1 misallocation damage; low downside (slight upside
reduction on correct regime switches, which is acceptable given asymmetric loss profile)

---

## Secondary Improvement 1 — Max weight cap per strategy

**File:** `app/meta/adaptive_selector.py`

Currently the LLM can assign 0.40–0.45 to a single strategy (seen in CRASH_HIGHVOL
with TrendPB). Combined with weight-ordering, this concentrates a large fraction of
available cash into one strategy. If that strategy's regime assumption is wrong, the
impact is outsized.

**Fix:** Hard cap in `_normalise()` or after LLM parsing:

```python
MAX_STRATEGY_WEIGHT = 0.35
weights = {k: min(v, MAX_STRATEGY_WEIGHT) for k, v in weights.items()}
weights = self._normalise(weights)  # re-normalise after capping
```

0.35 still allows a 3.5× spread between the highest and lowest weight (e.g. 0.35 vs
0.10), which is meaningful differentiation, but prevents extreme concentration.

**Priority:** MEDIUM  
**Effort:** Very low  
**Expected impact:** Reduces tail risk from both wrong and right calls; modest improvement
expected on Recent/choppy periods; small Sharpe cost on well-classified regimes

---

## Secondary Improvement 2 — Regime-specific stability gates

**File:** `app/meta/adaptive_selector.py`, `AdaptiveStrategySelector.__init__()`

Currently `regime_stability_weeks=2` applies uniformly to all regime transitions. But
transitions are not symmetric in risk:

- Exiting `CRASH_HIGHVOL` → `RECOVERY` is the most dangerous mislabel (high weight
  momentum strategies deployed into a declining market). Should require 3 weeks.
- Entering `CRASH_HIGHVOL` should be fast (1 week) to protect capital quickly.
- `BULL_*` → `BULL_*` (sub-label changes within bull) are low risk, 1 week is fine.

**Fix:** Replace the single `regime_stability_weeks` integer with a transition matrix:

```python
_STABILITY_WEEKS = {
    ("CRASH_HIGHVOL", "RECOVERY"):   3,  # most dangerous mislabel
    ("CRASH_HIGHVOL", "BEAR_EARLY"): 2,
    ("RECOVERY",      "BULL_MEDVOL"): 2,
    "_default":                       2,
    "_to_crash":                      1,  # fast entry into protection
}
```

**Priority:** LOW  
**Effort:** Medium — requires changes to the stability gate logic and testing  
**Note:** A simpler version already tested (uniform stability=3) showed marginal gains
in Bull/Live but hurt Bear 2022 (-0.12). The asymmetric version should do better.

---

## Implementation Order

1. **Wire RCA into `--adaptive` backtest** (Root Cause 1) — zero strategy code change, just test config. Do this first to establish an accurate baseline that matches production.
2. **Week-1 hard blend** (Root Cause 3) — 4 lines, very low risk, test immediately after step 1.
3. **SMA-50 hysteresis for CRASH exit** (Root Cause 2) — more involved, test against updated baseline.
4. **Max weight cap 0.35** (Secondary 1) — test alongside step 3 to see if they compound.
5. **Asymmetric stability gates** (Secondary 2) — last, as it depends on all prior changes being stable.

---

## Acceptance Criteria

All changes measured as `--adaptive` run vs `_ADAPTIVE_BASELINE` (post weight-ordering fix, 2026-05-13):

| Change | Pass criterion |
|--------|---------------|
| RCA wired into test | Recent 2022–2024 Sharpe recovers toward 1.78 (pre weight-order) or better |
| Week-1 hard blend | No regression in ≥5/7 periods vs updated baseline |
| SMA-50 hysteresis | Recent 2022–2024 improves; ≥4/7 overall |
| Max weight cap | Recent 2022–2024 improves or neutral; no regression >0.10 in other periods |
