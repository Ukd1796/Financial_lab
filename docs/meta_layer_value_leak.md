# Meta-Layer Investigation — Considered & Rejected

**Status:** Closed. Sleeve isolation + regime-thrash stabilizers investigated,
backtested across 7 periods, and **rejected by data**. Production-current
combined-router adaptive (SHARED-Adp) stays as the default.
**Date:** 2026-05-21
**Successor doc:** `underperforming_periods_rca.md` (the real next problem).

This doc exists so the next person who proposes "let's isolate the
strategies into independent sleeves" can read why we already tried it and
why it lost. It is intentionally short.

---

## 1. The diagnosis (real, but local)

`MultiStrategyRouter` merges all 5 strategies onto one shared symbol space +
one shared portfolio via lossy rules (one decision per symbol, position
ownership). In specific *bad* regimes (Bull 2019-20) the merge was shown to
turn +positive solo strategies into a negative combined portfolio:
1-strat-in-router = +3.80%; +2nd strat = −0.66% (a cliff). Diagnostic was
sound.

## 2. The proposed fix (sleeve isolation + 6 stabilizers + broad-150 A/B)

Capital-sleeve isolation: each strategy runs as an independent engine +
portfolio + own filtered universe; aggregate sleeve equity curves. Then
6 stabilizer levers (week-1 hard blend, max-weight cap, asymmetric dwell
gate, input smoothing, hysteresis deadband) and a measured A/B for true
broad-150 reclassification. All flag-gated default-off; legacy path
unaffected unless explicitly enabled.

## 3. The verdict (end-to-end 7-period integration, deterministic)

`PYTHONHASHSEED=0` + OpenAI `seed=0`, RCA wired (matches live):

| Period | SHARED-Adp (current) | Best SLEEVE-Adp | Winner |
|---|--:|--:|---|
| Full 2018–24 | **+116.10% / 1.33 S** | +96.96% / 1.10 | **SHARED +19.1pp** |
| Crash 2020 | **+30.15% / 2.24** | +23.56% / 1.85 | SHARED +6.6pp |
| Recov 2020–21 | **+80.90% / 2.86** | +68.01% / 2.49 | SHARED +12.9pp |
| Bear 2022 | **+7.60% / 0.91** | −0.66% / −0.02 | SHARED +8.3pp |
| Recent 2022–24 | **+37.93% / 1.50** | +19.76% / 0.89 | SHARED +18.2pp |
| Bull 2019–20 | −5.01% / −0.50 | **−0.68% / −0.03** | Sleeves +4.3pp |
| Live 2025–26 | −5.88% / −0.67 | **+5.32% / 0.54** | Sleeves +11.2pp |

**SHARED wins 5/7 periods, including the aggregate Full +19pp.** Sleeves
help only in the two narrow-breadth regimes where the merge actively hurts
— and by less than they cost elsewhere. The same merge that "destroys
value" in choppy regimes is *also* doing real portfolio work (regime-driven
concentration + cross-strategy synergy) in directional ones. Sleeves
discard both indiscriminately.

The diagnostic was right about a *local* defect; the proposed fix's *net*
effect across the full history is hugely negative.

## 4. What was kept (independently valuable)

- **Deterministic rule-clamp** (`_REGIME_WEIGHT_BOUNDS` +
  `_apply_regime_bounds` in `app/meta/adaptive_selector.py`). Validated as
  performance-neutral; programmatically enforces the per-regime MUST bounds
  that the LLM sometimes violates (e.g. `QuietBrk=0` in BULL_SUSTAINED
  where the rule says ≥0.20; `DualMA` omitted in BULL_MEDVOL). Pure
  correctness fix, no perf trade.
- **OpenAI `seed=0`** in `_call_llm` (best-effort API determinism).
- **`PYTHONHASHSEED=0` discipline** for validation runs (kills the engine
  `set()`-ordering noise we documented).
- **The underperforming-period diagnosis** itself — see
  `underperforming_periods_rca.md`.

## 5. What was discarded

- `run_sleeve_validation.py` (deleted).
- All A–F stabilizer flags + helpers in `AdaptiveStrategySelector`
  (week1_hard_blend, max_strategy_weight, dwell_matrix, smooth_window,
  hysteresis, broad_breadth_classify; `_required_dwell`,
  `_apply_hysteresis`, `_HYST_BAND`, `_DANGER`, `_raw_label_history`,
  `_input_history`, the `import math`).
- The plan to productionise sleeve-mode in the engine/harness.
- The plan to re-base regime classification onto broad-150 (the only
  adjacent thing tried — the RCA overlay — empirically hurt Bull/Live).

The selector code is restored to its pre-investigation shape **plus** the
rule-clamp and the OpenAI seed param.

## 6. Sanity / no-harm

Single-period regression smoke after the revert (Crash 2020, EqW ₹1L,
legacy costs) **matches `_VOLFILTER_RESULTS["Crash 2020"]` byte-for-byte**:
Sharpe 2.19 / +19.56% / MaxDD 4.71% / PF 1.83 / WR 51.2% / 1040 trades.
Live path (`api/run_paper_signals.py`) imports unchanged. Production is
unaffected.

## 7. Lessons for next time

1. **Don't validate a meta-layer fix on a 2-period gate.** The sleeve
   thesis was decided on Bull 2019-20 + Live 2025-26 alone; we missed that
   the merge's "lossy" behaviour in those choppy regimes is the *same
   mechanism* that captures concentration alpha in the 5 directional ones.
   The honest gate was the full-period aggregate.
2. **The regime classifier is fine for directional regimes; what fails is
   narrow-breadth ones** — that's an *archetype* problem, not a
   classifier problem (see `underperforming_periods_rca.md` §6). A
   top-of-funnel exposure gate (reduce gross exposure when breadth is
   collapsing) is the targeted lever to consider next, *not* a refactor of
   the router.
3. **Measurement determinism is a prerequisite, not an afterthought.**
   `PYTHONHASHSEED=0` + OpenAI `seed=0` should be the default for any
   validation run; without them earlier "gate" verdicts were noise-flips.
