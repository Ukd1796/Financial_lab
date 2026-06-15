# Regime-Classifier Diagnostic — Bull  2019–2020

**Generated:** 2026-05-31 00:42  
**Log:** `issues/Bull_2019_2020_regime_labels.jsonl`  
**Date range:** 2019-01-01 → 2020-01-26  
**Rebalances logged:** 116 raw / 58 unique dates  
**Note on broad-implied labels (§1, §4b):** the broad downtrend signal is approximated as `1 - pct_above_sma50_broad`, which includes SIDEWAYS stocks (not only DOWNTREND). This *overstates* BEAR_* counts in the broad-implied column. BULL_SUSTAINED / TRANSITION_UP / RECOVERY counts are robust (their rules don't depend on the down proxy).

---

## 1. Label distribution

Source split: **58** plain-Adaptive (narrow snapshot) + **58** Adaptive+RCA (broad snapshot enrichments).

| Regime | Adaptive (narrow) | Adaptive+RCA (narrow) | **Broad-implied** if classifier read broad keys |
|---|---|---|---|
| `BEAR_CONFIRMED` | 0 (0%) | 0 (0%) | **19 (33%)** |
| `BEAR_EARLY` | 0 (0%) | 0 (0%) | **8 (14%)** |
| `BULL_SUSTAINED` | 0 (0%) | 0 (0%) | **19 (33%)** |
| `CRASH_HIGHVOL` | 22 (38%) | 22 (38%) | **2 (3%)** |
| `MIXED` | 3 (5%) | 3 (5%) | **0 (0%)** |
| `RECOVERY` | 33 (57%) | 33 (57%) | **0 (0%)** |
| `TRANSITION_UP` | 0 (0%) | 0 (0%) | **10 (17%)** |

> The right column is the dispositive evidence. It applies the same `_REGIME_RULES` logic to the broad-universe inputs (`pct_above_sma50_broad`, `avg_rolling_vol_5d`, derived broad downtrend) — i.e. what the classifier would have labelled if it read the 150-stock breadth instead of the 80-stock active subset.

## 2. Boundary cases — weeks sitting near a classifier threshold

Weeks within ±3% of a breadth threshold or ±0.3% of an ATR threshold. High count here means small input changes are flipping labels — classifier is sensitive at the boundary.

**Total boundary weeks: 23 / 116 (20%)**

| Date | Label | Near-threshold values |
|---|---|---|
| 2019-01-01 | `RECOVERY` | pct_downtrend=0.190 (≈0.200) |
| 2019-01-06 | `RECOVERY` | pct_downtrend=0.208 (≈0.200) |
| 2019-01-20 | `RECOVERY` | pct_uptrend=0.610 (≈0.600) |
| 2019-02-03 | `RECOVERY` | pct_downtrend=0.327 (≈0.350) |
| 2019-02-24 | `CRASH_HIGHVOL` | pct_downtrend=0.467 (≈0.450) |
| 2019-04-29 | `RECOVERY` | pct_uptrend=0.603 (≈0.600) |
| 2019-05-05 | `RECOVERY` | pct_uptrend=0.527 (≈0.550) |
| 2019-05-19 | `MIXED` | pct_uptrend=0.552 (≈0.550) |
| 2019-06-02 | `RECOVERY` | pct_downtrend=0.195 (≈0.200) |
| 2019-06-09 | `RECOVERY` | pct_downtrend=0.182 (≈0.200) |
| 2019-06-16 | `RECOVERY` | pct_downtrend=0.463 (≈0.450) |
| 2019-06-30 | `CRASH_HIGHVOL` | pct_uptrend=0.558 (≈0.550) |
| 2019-07-14 | `CRASH_HIGHVOL` | pct_downtrend=0.357 (≈0.350) |
| 2019-07-21 | `CRASH_HIGHVOL` | pct_downtrend=0.364 (≈0.350) |
| 2019-09-02 | `CRASH_HIGHVOL` | pct_downtrend=0.429 (≈0.450) |
| 2019-09-29 | `CRASH_HIGHVOL` | pct_downtrend=0.221 (≈0.200) |
| 2019-10-06 | `CRASH_HIGHVOL` | pct_downtrend=0.439 (≈0.450) |
| 2019-10-13 | `CRASH_HIGHVOL` | pct_downtrend=0.349 (≈0.350) |
| 2019-12-08 | `RECOVERY` | pct_downtrend=0.229 (≈0.200); pct_uptrend=0.625 (≈0.600) |
| 2019-12-15 | `RECOVERY` | pct_uptrend=0.591 (≈0.600) |
| 2019-12-29 | `RECOVERY` | avg_atr_pct=0.025 (≈0.022); avg_atr_pct=0.025 (≈0.023) |
| 2020-01-05 | `RECOVERY` | pct_downtrend=0.197 (≈0.200); pct_uptrend=0.557 (≈0.550) |
| 2020-01-19 | `RECOVERY` | pct_uptrend=0.603 (≈0.600) |

## 3. Narrow vs broad universe agreement

Compared **pct_uptrend** (active 80) vs **pct_above_sma50_broad** (150) across 58 rebalances:

- Mean signed Δ (narrow − broad): **-0.008**
- Mean abs Δ: **0.065**
- Max abs Δ: **0.268**
- Weeks where narrow exceeds broad by >5pp (upward bias): **24%**
- Weeks where broad exceeds narrow by >5pp: **26%**

## 4. Narrow vs broad LABEL disagreement (regime vs broad_regime)

**16 rebalances** had different labels between the narrow-keyed classifier (`regime`) and the broad-snapshot classifier (`broad_regime`):

| Date | Narrow label | Broad label | pct_uptrend | pct_above_sma50_broad |
|---|---|---|---:|---:|
| 2019-01-27 | `RECOVERY` | `CRASH_HIGHVOL` | 0.292 | 0.303 |
| 2019-02-03 | `RECOVERY` | `TRANSITION_UP` | 0.442 | 0.380 |
| 2019-02-10 | `RECOVERY` | `CRASH_HIGHVOL` | 0.345 | 0.324 |
| 2019-03-04 | `CRASH_HIGHVOL` | `MIXED` | 0.449 | 0.634 |
| 2019-03-10 | `CRASH_HIGHVOL` | `RECOVERY` | 0.662 | 0.775 |
| 2019-04-29 | `RECOVERY` | `BULL_MEDVOL` | 0.597 | 0.634 |
| 2019-05-05 | `RECOVERY` | `MIXED` | 0.519 | 0.486 |
| 2019-05-26 | `MIXED` | `RECOVERY` | 0.730 | 0.606 |
| 2019-06-16 | `RECOVERY` | `CRASH_HIGHVOL` | 0.400 | 0.444 |
| 2019-06-30 | `CRASH_HIGHVOL` | `TRANSITION_UP` | 0.551 | 0.549 |
| 2019-09-15 | `CRASH_HIGHVOL` | `TRANSITION_UP` | 0.462 | 0.497 |
| 2019-09-22 | `CRASH_HIGHVOL` | `RECOVERY` | 0.667 | 0.731 |
| 2019-09-29 | `CRASH_HIGHVOL` | `MIXED` | 0.515 | 0.697 |
| 2019-10-21 | `CRASH_HIGHVOL` | `RECOVERY` | 0.750 | 0.752 |
| 2019-12-15 | `RECOVERY` | `BULL_MEDVOL` | 0.591 | 0.586 |
| 2020-01-05 | `RECOVERY` | `BULL_MEDVOL` | 0.557 | 0.493 |

## 4b. Per-week narrow vs **broad-implied** label disagreement

For each Adaptive+RCA rebalance, compare the actual label (derived from narrow-universe inputs as the live classifier does today) against the label this rebalance *would have received* if `_REGIME_RULES` consumed broad inputs.

**57 of 58 RCA rebalances** (98%) would be labelled differently under broad inputs.

| Date | Narrow label | Broad-implied | pct_uptrend / pct_above_sma50 | atr / vol_5d |
|---|---|---|---|---|
| 2019-01-01 | `RECOVERY` | `BULL_SUSTAINED` | 0.69 / 0.72 | 0.031 / 0.014 |
| 2019-01-06 | `RECOVERY` | `BULL_SUSTAINED` | 0.69 / 0.67 | 0.032 / 0.014 |
| 2019-01-13 | `RECOVERY` | `BEAR_EARLY` | 0.64 / 0.57 | 0.029 / 0.013 |
| 2019-01-20 | `RECOVERY` | `BEAR_CONFIRMED` | 0.61 / 0.49 | 0.027 / 0.014 |
| 2019-01-27 | `RECOVERY` | `BEAR_CONFIRMED` | 0.29 / 0.30 | 0.033 / 0.019 |
| 2019-02-03 | `RECOVERY` | `TRANSITION_UP` | 0.44 / 0.38 | 0.034 / 0.019 |
| 2019-02-10 | `RECOVERY` | `BEAR_CONFIRMED` | 0.34 / 0.32 | 0.037 / 0.020 |
| 2019-02-17 | `CRASH_HIGHVOL` | `BEAR_CONFIRMED` | 0.26 / 0.22 | 0.036 / 0.019 |
| 2019-02-24 | `CRASH_HIGHVOL` | `TRANSITION_UP` | 0.38 / 0.39 | 0.035 / 0.014 |
| 2019-03-04 | `CRASH_HIGHVOL` | `BEAR_EARLY` | 0.45 / 0.63 | 0.032 / 0.018 |
| 2019-03-10 | `CRASH_HIGHVOL` | `TRANSITION_UP` | 0.66 / 0.78 | 0.031 / 0.019 |
| 2019-03-17 | `RECOVERY` | `BULL_SUSTAINED` | 0.73 / 0.79 | 0.032 / 0.016 |
| 2019-03-24 | `RECOVERY` | `BULL_SUSTAINED` | 0.63 / 0.73 | 0.033 / 0.015 |
| 2019-03-31 | `RECOVERY` | `BULL_SUSTAINED` | 0.75 / 0.85 | 0.031 / 0.021 |
| 2019-04-07 | `RECOVERY` | `BULL_SUSTAINED` | 0.76 / 0.80 | 0.032 / 0.014 |
| 2019-04-14 | `RECOVERY` | `BULL_SUSTAINED` | 0.89 / 0.88 | 0.029 / 0.013 |
| 2019-04-21 | `RECOVERY` | `BULL_SUSTAINED` | 0.77 / 0.77 | 0.031 / 0.016 |
| 2019-04-29 | `RECOVERY` | `BEAR_EARLY` | 0.60 / 0.63 | 0.029 / 0.015 |
| 2019-05-05 | `RECOVERY` | `BEAR_CONFIRMED` | 0.52 / 0.49 | 0.028 / 0.016 |
| 2019-05-12 | `MIXED` | `BEAR_CONFIRMED` | 0.22 / 0.22 | 0.035 / 0.016 |
| 2019-05-19 | `MIXED` | `CRASH_HIGHVOL` | 0.50 / 0.49 | 0.037 / 0.026 |
| 2019-05-26 | `MIXED` | `BEAR_EARLY` | 0.73 / 0.61 | 0.038 / 0.021 |
| 2019-06-02 | `RECOVERY` | `BULL_SUSTAINED` | 0.64 / 0.68 | 0.036 / 0.017 |
| 2019-06-09 | `RECOVERY` | `BEAR_EARLY` | 0.70 / 0.59 | 0.034 / 0.018 |
| 2019-06-16 | `RECOVERY` | `BEAR_CONFIRMED` | 0.40 / 0.44 | 0.033 / 0.014 |
| 2019-06-23 | `CRASH_HIGHVOL` | `BEAR_CONFIRMED` | 0.48 / 0.45 | 0.030 / 0.017 |
| 2019-06-30 | `CRASH_HIGHVOL` | `TRANSITION_UP` | 0.55 / 0.55 | 0.030 / 0.014 |
| 2019-07-07 | `CRASH_HIGHVOL` | `BEAR_CONFIRMED` | 0.43 / 0.39 | 0.033 / 0.020 |
| 2019-07-14 | `CRASH_HIGHVOL` | `TRANSITION_UP` | 0.39 / 0.40 | 0.032 / 0.017 |
| 2019-07-21 | `CRASH_HIGHVOL` | `BEAR_CONFIRMED` | 0.24 / 0.26 | 0.034 / 0.018 |
| 2019-07-28 | `CRASH_HIGHVOL` | `BEAR_CONFIRMED` | 0.18 / 0.26 | 0.034 / 0.020 |
| 2019-08-04 | `CRASH_HIGHVOL` | `BEAR_CONFIRMED` | 0.24 / 0.18 | 0.041 / 0.021 |
| 2019-08-18 | `CRASH_HIGHVOL` | `BEAR_CONFIRMED` | 0.42 / 0.35 | 0.036 / 0.021 |
| 2019-08-25 | `CRASH_HIGHVOL` | `BEAR_CONFIRMED` | 0.10 / 0.37 | 0.043 / 0.023 |
| 2019-09-02 | `CRASH_HIGHVOL` | `BEAR_CONFIRMED` | 0.44 / 0.35 | 0.039 / 0.020 |
| 2019-09-08 | `CRASH_HIGHVOL` | `BEAR_CONFIRMED` | 0.32 / 0.46 | 0.035 / 0.019 |
| 2019-09-15 | `CRASH_HIGHVOL` | `TRANSITION_UP` | 0.46 / 0.50 | 0.033 / 0.016 |
| 2019-09-22 | `CRASH_HIGHVOL` | `TRANSITION_UP` | 0.67 / 0.73 | 0.037 / 0.036 |
| 2019-09-29 | `CRASH_HIGHVOL` | `BULL_SUSTAINED` | 0.52 / 0.70 | 0.041 / 0.021 |
| 2019-10-06 | `CRASH_HIGHVOL` | `BEAR_CONFIRMED` | 0.46 / 0.52 | 0.047 / 0.019 |
| … | … | … | … | (+17 more — see JSONL) |

## 5. Regime transitions (week-over-week label changes)

**Total transitions: 6** across 58 unique-date rebalances (stability = 89%)

| Date | From | To |
|---|---|---|
| 2019-02-17 | `RECOVERY` | `CRASH_HIGHVOL` |
| 2019-03-17 | `CRASH_HIGHVOL` | `RECOVERY` |
| 2019-05-12 | `RECOVERY` | `MIXED` |
| 2019-06-02 | `MIXED` | `RECOVERY` |
| 2019-06-23 | `RECOVERY` | `CRASH_HIGHVOL` |
| 2019-10-26 | `CRASH_HIGHVOL` | `RECOVERY` |

## 6. What to look for in this report

- **Distribution skew** (§1): if a period everyone calls a 'bull' is labelled MIXED 70% of the time, the classifier is mis-labelling.
- **High boundary count** (§2): means small noise flips labels — the threshold values may need adjustment.
- **Narrow vs broad mean delta** (§3): if narrow is consistently higher than broad, the active-80 upward-bias hypothesis is confirmed and switching the classifier to broad keys is justified.
- **Label disagreement count** (§4): direct evidence of narrow vs broad divergence — each row is a week the two universes saw different markets.
- **Many transitions** (§5): if labels flip > 30% of weeks, the `regime_stability_weeks=2` gate may be masking real instability.
