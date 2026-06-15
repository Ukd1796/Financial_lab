# Regime-Classifier Diagnostic — Live  2025–2026

**Generated:** 2026-05-31 00:42  
**Log:** `issues/Live_2025_2026_regime_labels.jsonl`  
**Date range:** 2025-01-01 → 2026-03-22  
**Rebalances logged:** 132 raw / 66 unique dates  
**Note on broad-implied labels (§1, §4b):** the broad downtrend signal is approximated as `1 - pct_above_sma50_broad`, which includes SIDEWAYS stocks (not only DOWNTREND). This *overstates* BEAR_* counts in the broad-implied column. BULL_SUSTAINED / TRANSITION_UP / RECOVERY counts are robust (their rules don't depend on the down proxy).

---

## 1. Label distribution

Source split: **66** plain-Adaptive (narrow snapshot) + **66** Adaptive+RCA (broad snapshot enrichments).

| Regime | Adaptive (narrow) | Adaptive+RCA (narrow) | **Broad-implied** if classifier read broad keys |
|---|---|---|---|
| `BEAR_CONFIRMED` | 0 (0%) | 0 (0%) | **30 (45%)** |
| `BEAR_EARLY` | 0 (0%) | 0 (0%) | **8 (12%)** |
| `BULL_MEDVOL` | 3 (5%) | 3 (5%) | **0 (0%)** |
| `BULL_SUSTAINED` | 0 (0%) | 0 (0%) | **14 (21%)** |
| `CRASH_HIGHVOL` | 28 (42%) | 26 (39%) | **2 (3%)** |
| `MIXED` | 2 (3%) | 7 (11%) | **0 (0%)** |
| `RECOVERY` | 33 (50%) | 30 (45%) | **2 (3%)** |
| `TRANSITION_UP` | 0 (0%) | 0 (0%) | **10 (15%)** |

> The right column is the dispositive evidence. It applies the same `_REGIME_RULES` logic to the broad-universe inputs (`pct_above_sma50_broad`, `avg_rolling_vol_5d`, derived broad downtrend) — i.e. what the classifier would have labelled if it read the 150-stock breadth instead of the 80-stock active subset.

## 2. Boundary cases — weeks sitting near a classifier threshold

Weeks within ±3% of a breadth threshold or ±0.3% of an ATR threshold. High count here means small input changes are flipping labels — classifier is sensitive at the boundary.

**Total boundary weeks: 43 / 132 (33%)**

| Date | Label | Near-threshold values |
|---|---|---|
| 2025-01-01 | `CRASH_HIGHVOL` | pct_downtrend=0.432 (≈0.450); avg_atr_pct=0.026 (≈0.023) |
| 2025-01-06 | `CRASH_HIGHVOL` | pct_downtrend=0.438 (≈0.450) |
| 2025-03-23 | `CRASH_HIGHVOL` | pct_downtrend=0.174 (≈0.200); pct_uptrend=0.565 (≈0.550) |
| 2025-03-31 | `BULL_MEDVOL` | pct_uptrend=0.576 (≈0.550); pct_uptrend=0.576 (≈0.600) |
| 2025-04-14 | `BULL_MEDVOL` | pct_downtrend=0.178 (≈0.200) |
| 2025-04-20 | `RECOVERY` | pct_downtrend=0.186 (≈0.200) |
| 2025-06-01 | `RECOVERY` | avg_atr_pct=0.025 (≈0.022); avg_atr_pct=0.025 (≈0.023) |
| 2025-06-08 | `RECOVERY` | avg_atr_pct=0.023 (≈0.022); avg_atr_pct=0.023 (≈0.023) |
| 2025-06-15 | `RECOVERY` | avg_atr_pct=0.025 (≈0.022); avg_atr_pct=0.025 (≈0.023) |
| 2025-06-22 | `RECOVERY` | avg_atr_pct=0.026 (≈0.023) |
| 2025-06-29 | `RECOVERY` | avg_atr_pct=0.024 (≈0.022); avg_atr_pct=0.024 (≈0.023) |
| 2025-07-06 | `RECOVERY` | avg_atr_pct=0.023 (≈0.022); avg_atr_pct=0.023 (≈0.023) |
| 2025-07-13 | `RECOVERY` | avg_atr_pct=0.022 (≈0.022); avg_atr_pct=0.022 (≈0.023) |
| 2025-07-20 | `RECOVERY` | avg_atr_pct=0.021 (≈0.022); avg_atr_pct=0.021 (≈0.023) |
| 2025-07-27 | `RECOVERY` | avg_atr_pct=0.024 (≈0.022); avg_atr_pct=0.024 (≈0.023) |
| 2025-08-03 | `CRASH_HIGHVOL` | pct_downtrend=0.469 (≈0.450); avg_atr_pct=0.024 (≈0.022); avg_atr_pct=0.024 (≈0.023) |
| 2025-08-10 | `CRASH_HIGHVOL` | avg_atr_pct=0.026 (≈0.023) |
| 2025-08-17 | `CRASH_HIGHVOL` | pct_downtrend=0.444 (≈0.450); avg_atr_pct=0.026 (≈0.023) |
| 2025-08-24 | `CRASH_HIGHVOL` | pct_downtrend=0.351 (≈0.350); pct_uptrend=0.541 (≈0.550); avg_atr_pct=0.022 (≈0.022); avg_atr_pct=0.022 (≈0.023) |
| 2025-08-31 | `CRASH_HIGHVOL` | pct_downtrend=0.324 (≈0.350); pct_uptrend=0.529 (≈0.550); avg_atr_pct=0.024 (≈0.022); avg_atr_pct=0.024 (≈0.023) |
| 2025-09-07 | `CRASH_HIGHVOL` | pct_uptrend=0.605 (≈0.600); avg_atr_pct=0.023 (≈0.022); avg_atr_pct=0.023 (≈0.023) |
| 2025-09-14 | `CRASH_HIGHVOL` | avg_atr_pct=0.022 (≈0.022); avg_atr_pct=0.022 (≈0.023) |
| 2025-09-21 | `CRASH_HIGHVOL` | pct_uptrend=0.600 (≈0.600); avg_atr_pct=0.021 (≈0.022); avg_atr_pct=0.021 (≈0.023) |
| 2025-09-28 | `CRASH_HIGHVOL` | avg_atr_pct=0.023 (≈0.022); avg_atr_pct=0.023 (≈0.023) |
| 2025-10-05 | `MIXED` | pct_downtrend=0.191 (≈0.200); avg_atr_pct=0.024 (≈0.022); avg_atr_pct=0.024 (≈0.023) |
| 2025-10-12 | `MIXED` | avg_atr_pct=0.023 (≈0.022); avg_atr_pct=0.023 (≈0.023) |
| 2025-10-19 | `RECOVERY` | avg_atr_pct=0.023 (≈0.022); avg_atr_pct=0.023 (≈0.023) |
| 2025-10-26 | `RECOVERY` | avg_atr_pct=0.021 (≈0.022); avg_atr_pct=0.021 (≈0.023) |
| 2025-11-02 | `RECOVERY` | pct_downtrend=0.183 (≈0.200); avg_atr_pct=0.022 (≈0.022); avg_atr_pct=0.022 (≈0.023) |
| 2025-11-09 | `RECOVERY` | pct_downtrend=0.217 (≈0.200); avg_atr_pct=0.024 (≈0.022); avg_atr_pct=0.024 (≈0.023) |
| … | … | (+13 more — see JSONL for full list) |

## 3. Narrow vs broad universe agreement

Compared **pct_uptrend** (active 80) vs **pct_above_sma50_broad** (150) across 66 rebalances:

- Mean signed Δ (narrow − broad): **+0.015**
- Mean abs Δ: **0.066**
- Max abs Δ: **0.184**
- Weeks where narrow exceeds broad by >5pp (upward bias): **32%**
- Weeks where broad exceeds narrow by >5pp: **23%**

## 4. Narrow vs broad LABEL disagreement (regime vs broad_regime)

**23 rebalances** had different labels between the narrow-keyed classifier (`regime`) and the broad-snapshot classifier (`broad_regime`):

| Date | Narrow label | Broad label | pct_uptrend | pct_above_sma50_broad |
|---|---|---|---:|---:|
| 2025-03-23 | `CRASH_HIGHVOL` | `BULL_MEDVOL` | 0.565 | 0.678 |
| 2025-04-06 | `BULL_MEDVOL` | `CRASH_HIGHVOL` | 0.292 | 0.349 |
| 2025-04-14 | `BULL_MEDVOL` | `RECOVERY` | 0.733 | 0.678 |
| 2025-07-20 | `RECOVERY` | `BULL_SUSTAINED` | 0.810 | 0.678 |
| 2025-07-27 | `RECOVERY` | `CRASH_HIGHVOL` | 0.370 | 0.396 |
| 2025-08-24 | `CRASH_HIGHVOL` | `MIXED` | 0.537 | 0.450 |
| 2025-09-07 | `MIXED` | `BULL_MEDVOL` | 0.600 | 0.416 |
| 2025-09-21 | `MIXED` | `BULL_SUSTAINED` | 0.636 | 0.678 |
| 2025-10-05 | `MIXED` | `TRANSITION_UP` | 0.521 | 0.523 |
| 2025-10-12 | `MIXED` | `RECOVERY` | 0.644 | 0.611 |
| 2025-10-26 | `RECOVERY` | `BULL_SUSTAINED` | 0.814 | 0.691 |
| 2025-11-23 | `RECOVERY` | `MIXED` | 0.500 | 0.483 |
| 2025-11-30 | `RECOVERY` | `BULL_SUSTAINED` | 0.605 | 0.564 |
| 2025-12-07 | `RECOVERY` | `BEAR_EARLY` | 0.431 | 0.443 |
| 2025-12-14 | `RECOVERY` | `TRANSITION_UP` | 0.618 | 0.483 |
| 2025-12-21 | `RECOVERY` | `BEAR_EARLY` | 0.541 | 0.497 |
| 2025-12-28 | `RECOVERY` | `MIXED` | 0.545 | 0.436 |
| 2026-01-04 | `RECOVERY` | `BULL_SUSTAINED` | 0.635 | 0.664 |
| 2026-01-11 | `RECOVERY` | `MIXED` | 0.448 | 0.450 |
| 2026-01-18 | `RECOVERY` | `BULL_MEDVOL` | 0.596 | 0.443 |
| 2026-01-26 | `RECOVERY` | `CRASH_HIGHVOL` | 0.314 | 0.333 |
| 2026-02-08 | `CRASH_HIGHVOL` | `MIXED` | 0.543 | 0.587 |
| 2026-02-22 | `CRASH_HIGHVOL` | `RECOVERY` | 0.667 | 0.607 |

## 4b. Per-week narrow vs **broad-implied** label disagreement

For each Adaptive+RCA rebalance, compare the actual label (derived from narrow-universe inputs as the live classifier does today) against the label this rebalance *would have received* if `_REGIME_RULES` consumed broad inputs.

**64 of 66 RCA rebalances** (97%) would be labelled differently under broad inputs.

| Date | Narrow label | Broad-implied | pct_uptrend / pct_above_sma50 | atr / vol_5d |
|---|---|---|---|---|
| 2025-01-01 | `CRASH_HIGHVOL` | `BEAR_CONFIRMED` | 0.34 / 0.43 | 0.026 / 0.016 |
| 2025-01-06 | `CRASH_HIGHVOL` | `BEAR_CONFIRMED` | 0.44 / 0.32 | 0.028 / 0.020 |
| 2025-01-12 | `CRASH_HIGHVOL` | `BEAR_CONFIRMED` | 0.06 / 0.15 | 0.035 / 0.020 |
| 2025-01-19 | `CRASH_HIGHVOL` | `BEAR_CONFIRMED` | 0.22 / 0.20 | 0.033 / 0.017 |
| 2025-01-26 | `CRASH_HIGHVOL` | `BEAR_CONFIRMED` | 0.14 / 0.13 | 0.036 / 0.019 |
| 2025-01-31 | `CRASH_HIGHVOL` | `TRANSITION_UP` | 0.24 / 0.30 | 0.037 / 0.023 |
| 2025-02-05 | `CRASH_HIGHVOL` | `BEAR_CONFIRMED` | 0.21 / 0.32 | 0.035 / 0.023 |
| 2025-02-10 | `CRASH_HIGHVOL` | `BEAR_CONFIRMED` | 0.11 / 0.15 | 0.040 / 0.018 |
| 2025-02-16 | `CRASH_HIGHVOL` | `BEAR_CONFIRMED` | 0.18 / 0.17 | 0.042 / 0.019 |
| 2025-02-23 | `CRASH_HIGHVOL` | `BEAR_CONFIRMED` | 0.12 / 0.17 | 0.034 / 0.016 |
| 2025-03-02 | `CRASH_HIGHVOL` | `BEAR_CONFIRMED` | 0.11 / 0.09 | 0.039 / 0.020 |
| 2025-03-09 | `CRASH_HIGHVOL` | `TRANSITION_UP` | 0.04 / 0.19 | 0.035 / 0.019 |
| 2025-03-16 | `CRASH_HIGHVOL` | `BEAR_CONFIRMED` | 0.22 / 0.26 | 0.033 / 0.016 |
| 2025-03-23 | `CRASH_HIGHVOL` | `TRANSITION_UP` | 0.56 / 0.68 | 0.028 / 0.018 |
| 2025-03-31 | `BULL_MEDVOL` | `BEAR_EARLY` | 0.58 / 0.58 | 0.028 / 0.016 |
| 2025-04-06 | `BULL_MEDVOL` | `CRASH_HIGHVOL` | 0.29 / 0.35 | 0.037 / 0.025 |
| 2025-04-14 | `BULL_MEDVOL` | `RECOVERY` | 0.73 / 0.68 | 0.036 / 0.029 |
| 2025-04-20 | `RECOVERY` | `TRANSITION_UP` | 0.65 / 0.79 | 0.034 / 0.017 |
| 2025-04-27 | `RECOVERY` | `BULL_SUSTAINED` | 0.72 / 0.82 | 0.035 / 0.020 |
| 2025-05-04 | `RECOVERY` | `BULL_SUSTAINED` | 0.88 / 0.88 | 0.030 / 0.017 |
| 2025-05-18 | `RECOVERY` | `BULL_SUSTAINED` | 0.97 / 0.92 | 0.031 / 0.017 |
| 2025-05-25 | `RECOVERY` | `BULL_SUSTAINED` | 0.85 / 0.85 | 0.034 / 0.017 |
| 2025-06-01 | `RECOVERY` | `BULL_SUSTAINED` | 0.89 / 0.78 | 0.025 / 0.011 |
| 2025-06-08 | `RECOVERY` | `BULL_SUSTAINED` | 0.88 / 0.85 | 0.023 / 0.014 |
| 2025-06-15 | `RECOVERY` | `BULL_SUSTAINED` | 0.91 / 0.79 | 0.025 / 0.012 |
| 2025-06-22 | `RECOVERY` | `BULL_SUSTAINED` | 0.77 / 0.66 | 0.026 / 0.014 |
| 2025-06-29 | `RECOVERY` | `BULL_SUSTAINED` | 0.87 / 0.83 | 0.024 / 0.012 |
| 2025-07-06 | `RECOVERY` | `BULL_SUSTAINED` | 0.81 / 0.80 | 0.023 / 0.012 |
| 2025-07-13 | `RECOVERY` | `BEAR_EARLY` | 0.74 / 0.64 | 0.022 / 0.012 |
| 2025-07-20 | `RECOVERY` | `BULL_SUSTAINED` | 0.81 / 0.68 | 0.022 / 0.012 |
| 2025-07-27 | `RECOVERY` | `BEAR_CONFIRMED` | 0.37 / 0.40 | 0.024 / 0.013 |
| 2025-08-03 | `CRASH_HIGHVOL` | `BEAR_CONFIRMED` | 0.40 / 0.36 | 0.024 / 0.016 |
| 2025-08-10 | `CRASH_HIGHVOL` | `BEAR_CONFIRMED` | 0.29 / 0.35 | 0.026 / 0.014 |
| 2025-08-17 | `CRASH_HIGHVOL` | `BEAR_CONFIRMED` | 0.44 / 0.42 | 0.026 / 0.015 |
| 2025-08-24 | `CRASH_HIGHVOL` | `BEAR_CONFIRMED` | 0.54 / 0.45 | 0.022 / 0.012 |
| 2025-08-31 | `MIXED` | `BEAR_CONFIRMED` | 0.54 / 0.38 | 0.023 / 0.015 |
| 2025-09-07 | `MIXED` | `BEAR_CONFIRMED` | 0.60 / 0.42 | 0.023 / 0.012 |
| 2025-09-14 | `MIXED` | `BEAR_EARLY` | 0.54 / 0.56 | 0.022 / 0.011 |
| 2025-09-21 | `MIXED` | `TRANSITION_UP` | 0.64 / 0.68 | 0.021 / 0.012 |
| 2025-09-28 | `MIXED` | `BEAR_CONFIRMED` | 0.39 / 0.38 | 0.023 / 0.013 |
| … | … | … | … | (+24 more — see JSONL) |

## 5. Regime transitions (week-over-week label changes)

**Total transitions: 8** across 66 unique-date rebalances (stability = 88%)

| Date | From | To |
|---|---|---|
| 2025-03-31 | `CRASH_HIGHVOL` | `BULL_MEDVOL` |
| 2025-04-20 | `BULL_MEDVOL` | `RECOVERY` |
| 2025-08-03 | `RECOVERY` | `CRASH_HIGHVOL` |
| 2025-10-05 | `CRASH_HIGHVOL` | `MIXED` |
| 2025-10-19 | `MIXED` | `RECOVERY` |
| 2026-02-01 | `RECOVERY` | `CRASH_HIGHVOL` |
| 2026-02-15 | `CRASH_HIGHVOL` | `RECOVERY` |
| 2026-03-08 | `RECOVERY` | `CRASH_HIGHVOL` |

## 6. What to look for in this report

- **Distribution skew** (§1): if a period everyone calls a 'bull' is labelled MIXED 70% of the time, the classifier is mis-labelling.
- **High boundary count** (§2): means small noise flips labels — the threshold values may need adjustment.
- **Narrow vs broad mean delta** (§3): if narrow is consistently higher than broad, the active-80 upward-bias hypothesis is confirmed and switching the classifier to broad keys is justified.
- **Label disagreement count** (§4): direct evidence of narrow vs broad divergence — each row is a week the two universes saw different markets.
- **Many transitions** (§5): if labels flip > 30% of weeks, the `regime_stability_weeks=2` gate may be masking real instability.
