# System Diagnosis: Why Both Paper Portfolios Underperform

Read-only analysis of live Supabase paper-trading data, 2026-04 to 2026-07.
Reproduce with `finance/bin/python3 scripts/analyze_portfolios.py`.

Subjects (two independent samples of the same system):

| Portfolio | session | total return | win rate | realised | unrealised |
|---|---|---|---|---|---|
| Ujjwal's Portfolio | pt_ujjwal | **+2.2%** | 34% | +₹1,186 | +₹1,026 |
| Shubham1 | pt_4765a5 | **−2.6%** | 27% | −₹3,452 | +₹847 |

Both are weak: win rates in the low 30s / high 20s, carried (in ujjwal's case) by a
handful of outliers. Ujjwal only stays positive because of DualMA (+₹2,867) and a
BEAR_CONFIRMED cluster (+₹4,713); Shubham is nearly pure Breakout and sinks with it.

## The user's lead: "we exit too late" — partly true, but not the main driver

Exit quality is genuinely poor:

| metric | Ujjwal | Shubham |
|---|---|---|
| median MFE efficiency (captured ÷ peak) | −0.27 | −0.84 |
| median give-back of the peak move | 127% | 184% |
| median trading days from peak to exit | 3.5 | 3.0 |
| ATR-stop exits: give-back / win rate | 222% / 29% | 396% / 0% |

Negative MFE efficiency and >100% give-back mean the median trade **peaks in profit,
then round-trips all the way back through the entry** before we exit, ~3 days after the
peak. When the trailing ATR stop is the exit, it surrenders 2–4× the peak move.

**Code cause of the lateness (confirmed):** live paper runs a **flat 2.5× ATR trailing
stop across every regime**, verified from the exit notes (2.5× appears even in
HIGH_VOL_DOWNTREND). The regime multiplier table in `app/risk/agent.py:6-16` (which
intends 1.0× in downtrends) is disabled, and paper passes `atr_multiplier=2.5`
(`api/run_paper_signals.py:464`) while the **validated backtest uses 2.0×**
(`api/services/backtest_service.py:343`). Paper's stop is 25% wider than the config we
actually validated, so it exits later by construction.

## The disambiguation: late exit vs bad entry

"Exit late" and "enter badly" look identical in P&L but need opposite fixes. The MFE
distribution separates them:

| signal | Ujjwal | Shubham | pooled |
|---|---|---|---|
| reached ≥1 ATR in profit at some point | 52% | 43% | — |
| went ≥1 ATR green **then closed red** (late-exit) | 18% | 17% | **17%** |
| never meaningfully green (MFE ≤ 0.5%) | 17% | 26% | 21% |
| **underwater by end of day 1 (bad-entry)** | 51% | 64% | **57%** |

**Verdict: both are real, but bad entries dominate.** 57% of trades are already
underwater one day after entry. About half the trades do present a real profit that we
then give back (the 17% late-exit bucket plus the negative MFE efficiency), so the exit
problem is not imaginary — but it is the smaller lever.

This reconciles with prior backtest history (`docs/architecture_report.html` Finding 10,
the MFE-lock battery): tightening exits regressed the backtest because you can't rescue a
trade that goes negative on day one, and winners (held ~13 td here) need room.

## Where the losses actually live

By entry strategy (both portfolios are ~85% Breakout by trade count — the "5-strategy"
ensemble has collapsed into a Breakout portfolio):

| strategy | Ujjwal P&L | Shubham P&L |
|---|---|---|
| Breakout | **−₹1,492** | **−₹3,323** |
| DualMA | +₹2,867 | −₹211 |
| TrendPB | −₹195 | +₹88 |
| RSI-MR | +₹6 | −₹6 |

By entry regime, losses concentrate in the momentum regimes Breakout lives in:

- CRASH_HIGHVOL: −₹1,909 (U) / −₹1,787 (S)
- RECOVERY: −₹1,059 (U) / −₹1,395 (S)
- BEAR_CONFIRMED: **+₹4,713 (U)** — the DualMA-heavy bear allocation is the only real winner.

**The ujjwal-vs-shubham gap is mostly allocation luck, not a different system:** ujjwal
got meaningful DualMA participation and a BEAR_CONFIRMED win; Shubham is almost entirely
Breakout. Same failure mode, different mix.

## Ranked improvement hypotheses

1. **[config · HIGH confidence · LOW risk] Align paper `atr_multiplier` 2.5 → 2.0.**
   Paper drifted off the validated backtest value. Directly narrows the ATR-stop
   give-back. *Risk:* the commit that introduced 2.5 claimed a MaxDD improvement, and a
   prior memo says flat 2.0× is correct — settle with a clean A/B backtest before
   shipping, don't just flip it.

2. **[system · HIGH confidence · HIGH value] Break the Breakout monopoly.** Breakout is
   ~85% of trades and net negative in both portfolios; the profitable contribution came
   from the strategies it crowds out (DualMA, bear allocation). This is the ensemble-collapse
   finding, now confirmed on live money. Highest-value lever.

3. **[entry · HIGH confidence · known-hard] Entries are regime-bound.** 57% day-1-negative,
   losses concentrated in CRASH_HIGHVOL / RECOVERY. Momentum entries are getting chopped.
   This is the structural entry-quality problem; exit changes cannot fix it.

4. **[exit · MEDIUM confidence · HIGH risk] The SMA-fade exits lag the peak.** Breakout
   exits only when price < SMA_10, structurally ~3 days after the peak, compounded by the
   wide stop. Real, but tightening exits regressed the backtest before and would cut the
   13-day winners — do not touch without a careful A/B.

## Root-cause suspect (per the root-cause skill)

```
SYMPTOM: both live paper portfolios underperform; exits appear late.

RULED OUT (backtest-run phantoms — N/A, this is live paper data not a run-to-run delta):
- PYTHONHASHSEED / LLM cache / shared-leg state / mode flip / regime-window change.

SUSPECT (for the "late exit" symptom):
  File:       api/run_paper_signals.py:464  (atr_multiplier=2.5, flat; regime table off)
  Mechanism:  trailing ATR stop is 25% wider than the validated 2.0x backtest and
              never tightens by regime, so exits fire ~3 td past the peak and ATR-stop
              exits give back 220-400% of the peak move.
  Confidence: HIGH that it causes late exits; MEDIUM that it is the primary P&L driver.

ALTERNATIVE (larger driver):
  File:       app/strategy/multi_router.py + Breakout dominance (ensemble collapse)
  Mechanism:  ~85% of trades are Breakout, net negative; 57% of all trades are underwater
              by day 1. The entry/regime problem outweighs the exit-width problem.

VERIFICATION COMMAND:
  finance/bin/python3 scripts/analyze_portfolios.py    # re-derives every number above
```
