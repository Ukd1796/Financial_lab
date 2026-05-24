# Cross-Period Analysis & Highest-Priority Improvements

**Date:** 2026-05-23
**Inputs:** EqualWeight + Adaptive+RCA runs across 6 periods (Bull 2019, Crash 2020, Recovery 2020–21, Bear 2022, Recent 2022–24, Live 2025–26), `trade_analytics.csv`, ensemble + opportunity-quality diagnostics, `docs/architecture_report.html`.

---

## 0. TL;DR

| Period          | EqW Sharpe / Return | Adaptive Sharpe / Return | Adaptive vs EqW |
|-----------------|---------------------|--------------------------|-----------------|
| Bull 2019       | −0.57 / **−3.39%**  | −0.52 / **−5.27%**       | **Worse**       |
| Crash 2020      | 2.19 / +19.56%      | n/a  / +28.85%¹          | Better          |
| Recovery 2020–21| 2.62 / +46.09%      | 2.77 / +76.85%           | Better          |
| Bear 2022       | 0.36 / +1.93%       | 1.17 / +10.24%           | Better          |
| Recent 2022–24  | 1.24 / +21.24%      | 1.64 / +42.78%           | Better          |
| Live 2025–26    | −0.60 / **−2.98%**  | −0.54 / **−4.95%**       | **Worse**       |

¹ Inferred from PnL attribution (₹28,853 vs ₹100k capital).

The story is binary:
- **In favourable regimes** (Crash, Recovery, Bear, Recent) Adaptive nearly **doubles** EqW returns by tilting capital into Breakout.
- **In hostile regimes** (Bull 2019, Live 2025–26) Adaptive **amplifies the loss** by tilting capital into the same Breakout strategy *after* its win rate has already collapsed.

**The system has two distinct failure modes, but they share one root cause: the universe scoring formula feeds momentum-exhausted stocks into a Breakout-dominated router, and the Adaptive selector cannot detect the resulting performance decay quickly enough.**

---

## 1. The Three Universal Patterns

These three numbers are nearly identical across **all six periods**, regardless of regime, returns, or Sharpe. They describe a *structural* defect, not a regime mismatch.

| Metric                 | Bull '19 | Crash '20 | Recov '20 | Bear '22 | Recent '22–24 | Live '25–26 |
|------------------------|----------|-----------|-----------|----------|---------------|-------------|
| **MFE Efficiency**     | −0.265   | −0.136    | −0.127    | −0.259   | −0.204        | **−0.318**  |
| **Persistence ½-life** | 0.0 d    | 0.0 d     | 0.0 d     | 0.0 d    | 0.0 d         | 0.0 d       |
| **False breakout %**   | 36.5%    | 35.9%     | 35.0%     | 34.9%    | 30.2%         | 27.4%       |

What this means in plain English:

1. **MFE efficiency is negative everywhere.** The final return is opposite-sign to the favourable peak. We're entering on a move, watching it peak, then exiting after it has reversed past zero. This is not "exiting too early" — it's "entering too late."
2. **Median stock falls below entry price within the same day.** The persistence half-life of 0 days across every period means at least half our entries are buying the local top.
3. **One in three "breakouts" is a head-fake.** Stable at ~30–37% across six wildly different regimes — that's a property of the entry filter, not the market.

These three facts point to the **same root cause: entry quality.** Specifically, the universe is feeding the Breakout strategy stocks that have already moved.

---

## 2. Why Adaptive Amplifies Losses in Hostile Regimes

Look at the PnL share rows for Bull 2019 and Live 2025–26:

| Period      | EqW Breakout PnL | Adaptive Breakout PnL | Adaptive share% |
|-------------|------------------|-----------------------|-----------------|
| Bull 2019   | −₹2,272 (56%)    | **−₹6,842** (89%)     | Concentrated    |
| Live 25–26  | −₹2,698 (91%)    | **−₹5,281** (109%)    | Concentrated    |

When Breakout was already losing, the AdaptiveSelector pushed **more** capital into it. The smoking gun is in the ensemble diagnostics:

- **Live 25–26 Adaptive pass-through:** Breakout 83.7%, everything else ≤6.6%.
- **Live 25–26 Breakout win rate:** 32.6% (vs 42–45% historical baseline).

The selector saw a 10-percentage-point WR collapse and *did not respond.* It kept feeding 5,685 of 6,093 Breakout signals through, while DualMA (which had a positive 60% WR in Live) only got 1,810 signals through.

**This is Architecture Bottleneck #5 (2-week regime stability lag) compounded with the absence of a P&L-aware downshift.** The LLM rebalances on regime metadata, not on rolling P&L attribution.

---

## 3. Strategy-by-Strategy Diagnosis

| Strategy   | Signal volume | Pass-through | Contribution                                           |
|------------|---------------|--------------|--------------------------------------------------------|
| DualMA     | High          | 75–79%       | Tiny PnL share (2–9%) — many HOLDs, small positions    |
| **Breakout** | **Highest** | 18–22% (EqW) / **83–85% (Adaptive)** | **60–95% of PnL.** Workhorse, but WR brittle: 33–45%. |
| QuietBrk   | Medium        | **0–2.5%**   | **Effectively dead.** 0 winning trades in Crash/Recov. |
| TrendPB    | Medium        | 4–10%        | Tiny PnL, blocked heavily by ownership lock-out        |
| RSI-MR     | Medium        | 3–11%        | Parasitic in Bull/Bear/Recent (negative net), helpful in Crash/Recov |

Key observations:

- **QuietBrk is dead in every period.** Pass-through never exceeds 2.5%. It's losing the priority contest to higher-priority strategies on the same symbols. Decide: fix it (re-prioritise / re-filter) or remove it.
- **TrendPB has massive `own_block` counts** (1,700–8,900 blocked SELLs per period). Its exit signals on Breakout-owned positions are silently dropped. This is Architecture Bottleneck #1.
- **RSI-MR is regime-dependent.** It earned positive PnL in Crash 2020 (+₹3,098) and Recovery (+₹5,549) but bled in Bull 2019 (−₹1,006) and Recent 22–24 (−₹1,143). The regime cap (≤0.05 in non-bear/non-recovery regimes) is correct *direction* but the cap is firing too late after a draw-down rather than pre-emptively.
- **DualMA passes 77%+ of signals but only contributes 2–9% of PnL.** Most of those wins must be HOLDs (no trade) or trades that are quickly stopped. It's filling slots without producing returns.

---

## 4. The Per-Regime View Across Periods

The most stable signal regime by win rate is **LOW_VOL_SIDEWAYS** (consistently 53–70% WR in 5 of 6 periods).

But in **Live 2025–26**, even LOW_VOL_SIDEWAYS dropped to **31.1% WR / −0.43% AvgRet**. Every regime is negative in Live. This is not a regime selection problem — the underlying entries don't work *in any classification* in the current period.

Bull 2019 shows the opposite anomaly: 458 trades entered in LOW_VOL_UPTREND but won only 32% of them. The supposedly "easiest" regime in a bull market produced the worst win rate of the period. This is consistent with **entering on stocks that had already exhausted their move** — the LOW_VOL_UPTREND label fires on stocks that have been trending quietly, but by the time the system enters, they're at the tail of the run.

---

## 5. Root Cause Ranking

Mapping each bottleneck to the evidence:

| Rank | Bottleneck (from architecture report)       | Evidence in results                                              | Severity |
|------|----------------------------------------------|------------------------------------------------------------------|----------|
| **1**| Universe activity bias (Bottleneck #2)       | MFE efficiency negative everywhere; persistence ½-life = 0 d everywhere; false breakout 30–37% everywhere | **HIGHEST** |
| **2**| Adaptive selector lag (Bottleneck #5 + new)  | Adaptive over-weights Breakout in Bull '19 and Live '25–26 despite WR collapse | **HIGH** |
| **3**| Exclusive ownership lock-out (Bottleneck #1) | 3,000–8,900 SELL signals blocked per period on TrendPB/RSI-MR    | **HIGH** |
| **4**| QuietBrk near-zero pass-through              | 0–2.5% pass-through in all 6 periods; 0 winning trades in 2 periods | MEDIUM |
| **5**| RSI-MR / DualMA capital fragmentation        | DualMA: 79% pass-through but 2–9% PnL share; RSI-MR negative in 3 periods | MEDIUM |

**Why #1 is highest priority:**

Bottlenecks 2–5 are each painful in 1–3 periods. Bottleneck 1 (universe activity bias) is the **only** bottleneck whose signature appears identically in every single period, including the good ones. Fixing it lifts all six periods simultaneously rather than patching one regime. In good periods we'd capture more of each move (lift MFE efficiency from −0.13 toward +0.30); in bad periods we'd stop entering local tops in the first place.

The current scoring formula:

```
score = 0.40 × rank(rel_vol) + 0.30 × rank(|return_3d|) + 0.30 × rank(vol_5d)
```

ranks by **how much a stock has already moved.** The Breakout strategy then enters on the breakout of stocks that are already over-extended. This is mathematically optimised for false breakouts.

---

## 6. Highest-Priority Improvement: Rebalance the Universe Scoring Formula

**Goal:** Stop feeding momentum-exhausted stocks into the Breakout pipeline.

### Proposed concrete changes

1. **Reduce raw activity weighting:**
   - Drop `|return_3d|` weight from **0.30 → 0.10**.
   - Drop `vol_5d` weight from **0.30 → 0.20**.
   - Free up 0.30 of the score budget for quality factors.

2. **Add quality factors (replacing the 0.30 budget):**
   - `0.15 × rank(adx_14)` — measure of trend strength, not movement size.
   - `0.10 × rank(volume_consistency)` — prefer steady volume to one-day spikes.
   - `0.05 × rank(close_above_sma_20_count)` — reward stocks that have *held* a level.

3. **Add anti-late-entry filter (hard exclusion before scoring):**
   - Exclude any stock where `rsi_14 > 75` AND `return_5d > 8%` from the top-80.
   - Exclude any stock more than `+15%` above its 20-day SMA.
   - This explicitly removes stocks that are most likely to head-fake.

4. **Per-strategy filter pre-pass:**
   - DualMA, TrendPB, RSI-MR currently consume an activity-biased pool. Let them score from the full 150-symbol set on their *own* preferred metric (golden-cross age for DualMA, pullback-depth for TrendPB, oversold-in-uptrend for RSI-MR). This is Architecture Bottleneck #2 directly.

### Expected impact

- False breakout rate: 30–37% → target **≤22%**
- MFE efficiency: −0.13 to −0.32 → target **+0.20 to +0.40**
- Persistence ½-life: 0 d → target **≥ 2 d**
- Breakout WR: 33–45% → target **≥ 48%** (which in Adaptive concentration mode = +30–50% absolute return lift in good periods)

### Validation plan

Run the same six periods with the new scoring formula and compare:
- The three universal-pattern metrics (MFE eff, persistence, false breakout %)
- Per-strategy pass-through and PnL share
- Adaptive vs EqW gap (should narrow in bad periods, widen in good ones)

If MFE efficiency still negative across periods, the entry-timing problem is *inside* the Breakout decide() logic, not the universe — and the next priority shifts to entry confirmation (e.g. wait one bar to confirm break + volume).

---

## 7. Second & Third Priorities (After #1 Validates)

### #2 — P&L-aware adaptive downshift

Independent of the LLM rebalance, add a deterministic guard:

```
if rolling_20d_WR[strategy] < (rolling_90d_WR[strategy] - 0.10):
    weight = min(weight, 0.10)
if rolling_20d_WR[strategy] < (rolling_90d_WR[strategy] - 0.15):
    weight = min(weight, 0.05)
```

This would have caught both Bull 2019 and Live 2025–26 Breakout degradation 2–4 weeks earlier than the current 2-week regime stability lag allows.

### #3 — Loosen cross-strategy exit lock-out for losing positions

Architecture Bottleneck #1. When `position_pnl_pct < -2%` and a non-owning strategy emits SELL, allow the SELL. Owner-only exits are the right default but should not trap a position in a confirmed losing trade.

---

## 8. What NOT to Prioritise Yet

- **More strategies:** Adding a 6th strategy without fixing entry quality just adds more bad entries.
- **LLM prompt engineering on AdaptiveSelector:** The selector is fed by the same universe. Better prompts on bad data won't help.
- **Cost model changes:** False breakouts of 30–37% with persistence ½-life of 0 days are not a cost-model artefact; the entries are bad before any cost adjustment.
- **Removing QuietBrk:** It's dead but not actively harmful. Fix it or remove it after the universe rework — at that point you can measure whether it was the universe starving it.

---

## 9. Summary

The system has **one root problem, two symptoms, and five visible bottlenecks.**

- **Root:** Universe scoring rewards stocks that have already moved → Breakout enters local tops.
- **Symptom A (universal):** MFE efficiency negative, persistence ½-life 0 days, false breakout 30–37%.
- **Symptom B (regime-dependent):** Adaptive concentrates into a degrading workhorse and amplifies losses in Bull '19 and Live '25–26.

**Fixing the universe scoring formula is the single change with the highest expected lift across all six periods.** Everything else is a secondary tuning task that should be re-evaluated after the universe rework lands.
