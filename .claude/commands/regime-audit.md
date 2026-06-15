<!-- Recommended model: /model opus -->
<!-- Usage: /project:regime-audit <period name> -->
<!-- Example: /project:regime-audit "Bull 2019–2020" -->
<!-- Use when the regime classifier is over-firing on one label or allocations look wrong. -->
<!-- This is the deepest reasoning task — run with Opus, not Sonnet. -->

You are a regime classifier auditor for a quantitative trading system that uses GPT-4o-mini to allocate weights across 5 strategies based on market regime labels. Your job is to identify whether the classifier is misbehaving and which rule is responsible.

## Period to Audit

$ARGUMENTS

## Regime System Overview

**Classifier** (`app/meta/adaptive_selector.py` lines 114–165):
- Deterministically outputs one of 8 labels: `CRASH_HIGHVOL`, `TRANSITION_UP`, `BEAR_CONFIRMED`, `BEAR_EARLY`, `RECOVERY`, `BULL_SUSTAINED`, `BULL_LOWVOL`, `BULL_MEDVOL`, `MIXED`
- Based on: pct_downtrend, pct_uptrend, avg_atr_pct, pct_high_vol thresholds

**LLM allocation** (`app/meta/adaptive_selector.py` lines 173–252):
- `_REGIME_ALLOCATION_RULES`: prose constraints passed to GPT-4o-mini per regime
- `_REGIME_WEIGHT_BOUNDS`: hard bounds applied post-LLM to clamp any drift

**Known failure modes from this project's history:**
- BULL_SUSTAINED over-fires when vol-swap boundary is too loose (~95–100% of RCA weeks)
- Clamp activates most on the dominant regime — if it's firing >20% of decisions it's a signal the LLM is drifting outside bounds
- Raw→clamped drift >0.10 on any strategy in any regime = the prose rule and the bound are fighting each other

## Steps

1. Read `issues/<period>_regime_labels.jsonl` (fuzzy-match the period name to the filename). If it doesn't exist, note that and stop — the diagnostic data isn't available for this period.

2. Read `app/meta/adaptive_selector.py` lines 100–260 (regime rules + weight bounds).

3. From the JSONL, compute:
   - Regime label frequency (count + % of total rebalance dates)
   - `clamp_active` firing rate overall and per label
   - For each rebalance date: `raw_weights` vs `final_weights` delta per strategy — average the drift per strategy per regime

4. Cross-reference: for each label that fired ≥20% of the time, check whether its `_REGIME_ALLOCATION_RULES` prose and `_REGIME_WEIGHT_BOUNDS` are consistent (the prose says X, the bound allows Y — are they aligned?).

5. Identify the single most actionable finding.

## Output Format

### 1. Regime Frequency
| Label | Count | % of period | Expected? |
(Flag any label at >40% as potentially over-firing)

### 2. Clamp Activity
| Label | Clamp fired | % of decisions | Most clamped strategy |

### 3. Allocation Drift (raw → clamped, averaged per regime)
| Label | DualMA Δ | Breakout Δ | QuietBrk Δ | TrendPB Δ | RSI-MR Δ |
(Highlight cells where |Δ| > 0.10)

### 4. Rule Consistency Check
For each regime firing ≥20%:
- Prose constraint (from `_REGIME_ALLOCATION_RULES`)
- Hard bound (from `_REGIME_WEIGHT_BOUNDS`)
- Conflict: yes/no — if yes, describe the tension in one sentence

### 5. Primary Finding
```
FINDING: <label> is <over-firing / under-firing / producing allocation drift>
MECHANISM: <which rule or threshold is responsible>
SUGGESTED FIX: <specific line or value to change in adaptive_selector.py>
RISK: <what second-order effect to watch for if this is changed>
```
