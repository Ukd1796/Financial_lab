# Regime-Classifier Diagnostic — Recent2022–2024

**Generated:** 2026-05-31 00:42  
**Log:** `issues/Recent2022_2024_regime_labels.jsonl`  
**Date range:** 2022-01-02 → 2024-05-26  
**Rebalances logged:** 252 raw / 126 unique dates  
**Note on broad-implied labels (§1, §4b):** the broad downtrend signal is approximated as `1 - pct_above_sma50_broad`, which includes SIDEWAYS stocks (not only DOWNTREND). This *overstates* BEAR_* counts in the broad-implied column. BULL_SUSTAINED / TRANSITION_UP / RECOVERY counts are robust (their rules don't depend on the down proxy).

---

## 1. Label distribution

Source split: **126** plain-Adaptive (narrow snapshot) + **126** Adaptive+RCA (broad snapshot enrichments).

| Regime | Adaptive (narrow) | Adaptive+RCA (narrow) | **Broad-implied** if classifier read broad keys |
|---|---|---|---|
| `BEAR_CONFIRMED` | 0 (0%) | 0 (0%) | **29 (23%)** |
| `BEAR_EARLY` | 0 (0%) | 0 (0%) | **16 (13%)** |
| `BULL_SUSTAINED` | 0 (0%) | 0 (0%) | **49 (39%)** |
| `CRASH_HIGHVOL` | 37 (29%) | 31 (25%) | **9 (7%)** |
| `MIXED` | 4 (3%) | 8 (6%) | **0 (0%)** |
| `RECOVERY` | 85 (67%) | 85 (67%) | **1 (1%)** |
| `TRANSITION_UP` | 0 (0%) | 2 (2%) | **22 (17%)** |

> The right column is the dispositive evidence. It applies the same `_REGIME_RULES` logic to the broad-universe inputs (`pct_above_sma50_broad`, `avg_rolling_vol_5d`, derived broad downtrend) — i.e. what the classifier would have labelled if it read the 150-stock breadth instead of the 80-stock active subset.

## 2. Boundary cases — weeks sitting near a classifier threshold

Weeks within ±3% of a breadth threshold or ±0.3% of an ATR threshold. High count here means small input changes are flipping labels — classifier is sensitive at the boundary.

**Total boundary weeks: 54 / 252 (21%)**

| Date | Label | Near-threshold values |
|---|---|---|
| 2022-01-02 | `MIXED` | pct_uptrend=0.533 (≈0.550) |
| 2022-01-16 | `RECOVERY` | pct_uptrend=0.603 (≈0.600) |
| 2022-02-06 | `CRASH_HIGHVOL` | pct_downtrend=0.321 (≈0.350); pct_uptrend=0.554 (≈0.550) |
| 2022-04-03 | `CRASH_HIGHVOL` | pct_uptrend=0.558 (≈0.550) |
| 2022-04-17 | `CRASH_HIGHVOL` | pct_downtrend=0.172 (≈0.200) |
| 2022-04-24 | `CRASH_HIGHVOL` | pct_downtrend=0.366 (≈0.350) |
| 2022-07-03 | `CRASH_HIGHVOL` | pct_downtrend=0.474 (≈0.450) |
| 2022-07-17 | `CRASH_HIGHVOL` | pct_uptrend=0.612 (≈0.600) |
| 2022-09-25 | `RECOVERY` | pct_uptrend=0.574 (≈0.550); pct_uptrend=0.574 (≈0.600) |
| 2022-10-02 | `RECOVERY` | pct_downtrend=0.200 (≈0.200); pct_uptrend=0.545 (≈0.550) |
| 2022-10-09 | `RECOVERY` | pct_downtrend=0.171 (≈0.200) |
| 2022-10-16 | `RECOVERY` | pct_downtrend=0.341 (≈0.350) |
| 2022-11-27 | `RECOVERY` | pct_uptrend=0.608 (≈0.600); avg_atr_pct=0.026 (≈0.023) |
| 2022-12-04 | `RECOVERY` | avg_atr_pct=0.023 (≈0.022); avg_atr_pct=0.023 (≈0.023) |
| 2022-12-11 | `RECOVERY` | avg_atr_pct=0.025 (≈0.023) |
| 2023-01-01 | `RECOVERY` | pct_downtrend=0.370 (≈0.350); pct_uptrend=0.593 (≈0.600) |
| 2023-01-08 | `RECOVERY` | pct_uptrend=0.595 (≈0.600) |
| 2023-01-15 | `RECOVERY` | pct_uptrend=0.545 (≈0.550); avg_atr_pct=0.024 (≈0.022); avg_atr_pct=0.024 (≈0.023) |
| 2023-01-22 | `MIXED` | pct_uptrend=0.547 (≈0.550); avg_atr_pct=0.024 (≈0.022); avg_atr_pct=0.024 (≈0.023) |
| 2023-02-12 | `CRASH_HIGHVOL` | pct_downtrend=0.323 (≈0.350) |
| 2023-02-19 | `CRASH_HIGHVOL` | pct_downtrend=0.367 (≈0.350) |
| 2023-03-05 | `CRASH_HIGHVOL` | pct_downtrend=0.222 (≈0.200); pct_uptrend=0.528 (≈0.550) |
| 2023-03-12 | `CRASH_HIGHVOL` | pct_downtrend=0.460 (≈0.450) |
| 2023-04-02 | `CRASH_HIGHVOL` | pct_downtrend=0.469 (≈0.450); avg_atr_pct=0.026 (≈0.023) |
| 2023-04-09 | `CRASH_HIGHVOL` | avg_atr_pct=0.025 (≈0.023) |
| 2023-04-16 | `CRASH_HIGHVOL` | pct_uptrend=0.578 (≈0.550); pct_uptrend=0.578 (≈0.600); avg_atr_pct=0.025 (≈0.023) |
| 2023-04-23 | `CRASH_HIGHVOL` | avg_atr_pct=0.023 (≈0.022); avg_atr_pct=0.023 (≈0.023) |
| 2023-05-01 | `RECOVERY` | avg_atr_pct=0.023 (≈0.022); avg_atr_pct=0.023 (≈0.023) |
| 2023-05-07 | `RECOVERY` | avg_atr_pct=0.023 (≈0.022); avg_atr_pct=0.023 (≈0.023) |
| 2023-05-14 | `RECOVERY` | avg_atr_pct=0.024 (≈0.022); avg_atr_pct=0.024 (≈0.023) |
| … | … | (+24 more — see JSONL for full list) |

## 3. Narrow vs broad universe agreement

Compared **pct_uptrend** (active 80) vs **pct_above_sma50_broad** (150) across 126 rebalances:

- Mean signed Δ (narrow − broad): **+0.034**
- Mean abs Δ: **0.085**
- Max abs Δ: **0.318**
- Weeks where narrow exceeds broad by >5pp (upward bias): **44%**
- Weeks where broad exceeds narrow by >5pp: **17%**

> ⚠️ Mean delta is **+0.034** — the active-80 universe is systematically biased. If positive, the classifier sees a brighter market than the broad universe actually shows.

## 4. Narrow vs broad LABEL disagreement (regime vs broad_regime)

**30 rebalances** had different labels between the narrow-keyed classifier (`regime`) and the broad-snapshot classifier (`broad_regime`):

| Date | Narrow label | Broad label | pct_uptrend | pct_above_sma50_broad |
|---|---|---|---:|---:|
| 2022-01-09 | `MIXED` | `RECOVERY` | 0.691 | 0.718 |
| 2022-01-23 | `RECOVERY` | `CRASH_HIGHVOL` | 0.129 | 0.275 |
| 2022-02-06 | `CRASH_HIGHVOL` | `TRANSITION_UP` | 0.554 | 0.396 |
| 2022-04-03 | `CRASH_HIGHVOL` | `BULL_MEDVOL` | 0.558 | 0.772 |
| 2022-04-10 | `CRASH_HIGHVOL` | `RECOVERY` | 0.683 | 0.859 |
| 2022-04-17 | `CRASH_HIGHVOL` | `MIXED` | 0.508 | 0.685 |
| 2022-05-01 | `CRASH_HIGHVOL` | `TRANSITION_UP` | 0.509 | 0.557 |
| 2022-07-10 | `CRASH_HIGHVOL` | `TRANSITION_UP` | 0.411 | 0.651 |
| 2022-07-17 | `CRASH_HIGHVOL` | `RECOVERY` | 0.612 | 0.758 |
| 2022-09-25 | `RECOVERY` | `BULL_MEDVOL` | 0.567 | 0.389 |
| 2022-10-02 | `RECOVERY` | `MIXED` | 0.545 | 0.396 |
| 2022-10-16 | `RECOVERY` | `MIXED` | 0.489 | 0.409 |
| 2022-11-20 | `RECOVERY` | `MIXED` | 0.466 | 0.497 |
| 2022-12-25 | `RECOVERY` | `MIXED` | 0.400 | 0.309 |
| 2023-01-01 | `RECOVERY` | `CRASH_HIGHVOL` | 0.593 | 0.376 |
| 2023-01-08 | `RECOVERY` | `BULL_MEDVOL` | 0.595 | 0.450 |
| 2023-01-15 | `RECOVERY` | `MIXED` | 0.545 | 0.389 |
| 2023-01-29 | `MIXED` | `CRASH_HIGHVOL` | 0.228 | 0.228 |
| 2023-02-12 | `CRASH_HIGHVOL` | `MIXED` | 0.433 | 0.349 |
| 2023-02-26 | `MIXED` | `CRASH_HIGHVOL` | 0.306 | 0.268 |
| 2023-03-05 | `MIXED` | `TRANSITION_UP` | 0.514 | 0.409 |
| 2023-03-12 | `MIXED` | `CRASH_HIGHVOL` | 0.388 | 0.289 |
| 2023-04-09 | `CRASH_HIGHVOL` | `TRANSITION_UP` | 0.500 | 0.510 |
| 2023-04-23 | `TRANSITION_UP` | `RECOVERY` | 0.661 | 0.671 |
| 2023-06-18 | `RECOVERY` | `BULL_SUSTAINED` | 0.887 | 0.872 |
| 2023-10-08 | `RECOVERY` | `BULL_MEDVOL` | 0.600 | 0.510 |
| 2023-10-22 | `RECOVERY` | `MIXED` | 0.390 | 0.376 |
| 2023-10-29 | `RECOVERY` | `CRASH_HIGHVOL` | 0.462 | 0.356 |
| 2024-03-17 | `RECOVERY` | `MIXED` | 0.489 | 0.450 |
| 2024-03-25 | `RECOVERY` | `TRANSITION_UP` | 0.610 | 0.523 |

## 4b. Per-week narrow vs **broad-implied** label disagreement

For each Adaptive+RCA rebalance, compare the actual label (derived from narrow-universe inputs as the live classifier does today) against the label this rebalance *would have received* if `_REGIME_RULES` consumed broad inputs.

**117 of 126 RCA rebalances** (93%) would be labelled differently under broad inputs.

| Date | Narrow label | Broad-implied | pct_uptrend / pct_above_sma50 | atr / vol_5d |
|---|---|---|---|---|
| 2022-01-02 | `MIXED` | `BEAR_EARLY` | 0.53 / 0.56 | 0.031 / 0.014 |
| 2022-01-09 | `MIXED` | `TRANSITION_UP` | 0.69 / 0.72 | 0.027 / 0.015 |
| 2022-01-16 | `RECOVERY` | `BULL_SUSTAINED` | 0.60 / 0.76 | 0.027 / 0.015 |
| 2022-01-23 | `RECOVERY` | `BEAR_CONFIRMED` | 0.13 / 0.28 | 0.038 / 0.021 |
| 2022-02-06 | `CRASH_HIGHVOL` | `TRANSITION_UP` | 0.55 / 0.40 | 0.040 / 0.021 |
| 2022-02-20 | `CRASH_HIGHVOL` | `TRANSITION_UP` | 0.38 / 0.24 | 0.039 / 0.020 |
| 2022-03-06 | `CRASH_HIGHVOL` | `BEAR_CONFIRMED` | 0.11 / 0.09 | 0.048 / 0.022 |
| 2022-03-13 | `CRASH_HIGHVOL` | `TRANSITION_UP` | 0.28 / 0.26 | 0.042 / 0.018 |
| 2022-03-20 | `CRASH_HIGHVOL` | `BEAR_CONFIRMED` | 0.22 / 0.37 | 0.039 / 0.022 |
| 2022-03-27 | `CRASH_HIGHVOL` | `BEAR_CONFIRMED` | 0.38 / 0.41 | 0.034 / 0.014 |
| 2022-04-03 | `CRASH_HIGHVOL` | `TRANSITION_UP` | 0.56 / 0.77 | 0.030 / 0.017 |
| 2022-04-10 | `CRASH_HIGHVOL` | `BULL_SUSTAINED` | 0.68 / 0.86 | 0.029 / 0.017 |
| 2022-04-17 | `CRASH_HIGHVOL` | `BULL_SUSTAINED` | 0.51 / 0.69 | 0.032 / 0.017 |
| 2022-04-24 | `CRASH_HIGHVOL` | `BEAR_CONFIRMED` | 0.47 / 0.52 | 0.035 / 0.020 |
| 2022-05-01 | `CRASH_HIGHVOL` | `TRANSITION_UP` | 0.51 / 0.56 | 0.034 / 0.020 |
| 2022-05-08 | `CRASH_HIGHVOL` | `BEAR_CONFIRMED` | 0.15 / 0.17 | 0.041 / 0.020 |
| 2022-06-05 | `CRASH_HIGHVOL` | `BEAR_CONFIRMED` | 0.41 / 0.26 | 0.038 / 0.017 |
| 2022-06-12 | `CRASH_HIGHVOL` | `BEAR_CONFIRMED` | 0.16 / 0.15 | 0.037 / 0.017 |
| 2022-06-19 | `CRASH_HIGHVOL` | `BEAR_CONFIRMED` | 0.03 / 0.07 | 0.042 / 0.020 |
| 2022-06-26 | `CRASH_HIGHVOL` | `TRANSITION_UP` | 0.14 / 0.21 | 0.038 / 0.021 |
| 2022-07-03 | `CRASH_HIGHVOL` | `TRANSITION_UP` | 0.34 / 0.34 | 0.035 / 0.018 |
| 2022-07-10 | `CRASH_HIGHVOL` | `TRANSITION_UP` | 0.41 / 0.65 | 0.029 / 0.016 |
| 2022-07-17 | `CRASH_HIGHVOL` | `BULL_SUSTAINED` | 0.61 / 0.76 | 0.028 / 0.017 |
| 2022-07-24 | `RECOVERY` | `BULL_SUSTAINED` | 0.75 / 0.85 | 0.029 / 0.016 |
| 2022-07-31 | `RECOVERY` | `BULL_SUSTAINED` | 0.86 / 0.93 | 0.028 / 0.019 |
| 2022-08-07 | `RECOVERY` | `BULL_SUSTAINED` | 0.79 / 0.91 | 0.028 / 0.015 |
| 2022-08-15 | `RECOVERY` | `BULL_SUSTAINED` | 0.88 / 0.95 | 0.029 / 0.016 |
| 2022-08-21 | `RECOVERY` | `BULL_SUSTAINED` | 0.78 / 0.90 | 0.030 / 0.019 |
| 2022-08-28 | `RECOVERY` | `BULL_SUSTAINED` | 0.81 / 0.86 | 0.029 / 0.015 |
| 2022-09-04 | `RECOVERY` | `BULL_SUSTAINED` | 0.95 / 0.86 | 0.030 / 0.018 |
| 2022-09-11 | `RECOVERY` | `BULL_SUSTAINED` | 0.90 / 0.89 | 0.028 / 0.014 |
| 2022-09-18 | `RECOVERY` | `BEAR_EARLY` | 0.73 / 0.63 | 0.030 / 0.019 |
| 2022-09-25 | `RECOVERY` | `BEAR_CONFIRMED` | 0.57 / 0.39 | 0.036 / 0.020 |
| 2022-10-02 | `RECOVERY` | `BEAR_CONFIRMED` | 0.55 / 0.40 | 0.038 / 0.019 |
| 2022-10-09 | `RECOVERY` | `BEAR_CONFIRMED` | 0.67 / 0.49 | 0.033 / 0.020 |
| 2022-10-16 | `RECOVERY` | `BEAR_CONFIRMED` | 0.49 / 0.41 | 0.032 / 0.016 |
| 2022-10-23 | `RECOVERY` | `BEAR_CONFIRMED` | 0.79 / 0.47 | 0.029 / 0.014 |
| 2022-10-30 | `RECOVERY` | `TRANSITION_UP` | 0.68 / 0.61 | 0.028 / 0.015 |
| 2022-11-06 | `RECOVERY` | `BULL_SUSTAINED` | 0.77 / 0.70 | 0.026 / 0.015 |
| 2022-11-13 | `RECOVERY` | `BEAR_EARLY` | 0.67 / 0.60 | 0.029 / 0.020 |
| … | … | … | … | (+77 more — see JSONL) |

## 5. Regime transitions (week-over-week label changes)

**Total transitions: 6** across 126 unique-date rebalances (stability = 95%)

| Date | From | To |
|---|---|---|
| 2022-01-16 | `MIXED` | `RECOVERY` |
| 2022-01-30 | `RECOVERY` | `CRASH_HIGHVOL` |
| 2022-07-24 | `CRASH_HIGHVOL` | `RECOVERY` |
| 2023-01-22 | `RECOVERY` | `MIXED` |
| 2023-02-05 | `MIXED` | `CRASH_HIGHVOL` |
| 2023-05-01 | `CRASH_HIGHVOL` | `RECOVERY` |

## 6. What to look for in this report

- **Distribution skew** (§1): if a period everyone calls a 'bull' is labelled MIXED 70% of the time, the classifier is mis-labelling.
- **High boundary count** (§2): means small noise flips labels — the threshold values may need adjustment.
- **Narrow vs broad mean delta** (§3): if narrow is consistently higher than broad, the active-80 upward-bias hypothesis is confirmed and switching the classifier to broad keys is justified.
- **Label disagreement count** (§4): direct evidence of narrow vs broad divergence — each row is a week the two universes saw different markets.
- **Many transitions** (§5): if labels flip > 30% of weeks, the `regime_stability_weeks=2` gate may be masking real instability.
