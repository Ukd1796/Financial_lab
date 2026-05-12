# app/meta/adaptive_selector.py
#
# AdaptiveStrategySelector — weekly LLM-driven capital allocation layer.
#
# Architecture:
#   daily  : build_regime_snapshot()  → regime dict (breadth, vol, ATR)
#   weekly : AdaptiveStrategySelector.rebalance()
#            ├── _classify_regime()        → deterministic Python regime label + confidence
#            ├── rolling snapshot history  → 4-week trend for the LLM
#            └── OpenAI API call           → normalised weight dict
#            → MultiStrategyRouter.update_weights()
#
# Key design decisions (see docs/adaptive_strategy_selector_analysis.md):
#   - Python-side regime classification removes LLM ambiguity for clear regimes
#   - 4-week rolling history shows trends (e.g. DOWNTREND slowly building)
#   - Hard numeric bounds in rules ("DualMA MUST be ≥ 0.55") prevent hedging
#   - Falls back to unchanged weights on any API or parse failure

import json
import os
from datetime import datetime
from typing import Callable, Optional

from openai import OpenAI


# ---------------------------------------------------------------------------
# Empirical Sharpe table — hard-coded from 2018–2024 backtests.
# (net of 0.10% commission + 0.05% slippage per side)
# Updated 2026-03-21 after MultiStrategyRouter + UnionUniverseFilter tuning.
# ---------------------------------------------------------------------------
_STRATEGY_REGIME_PERFORMANCE = """\
Strategy Sharpe ratios by market regime (NSE Indian equities, 2018–2024 backtests):

                  Bull/LowVol  Crash/HighVol  Recovery  Bear/Choppy  Mixed
DualMA SMA20/50      0.44          1.28         2.66        0.51      1.69
Breakout 10d         0.93          1.72         3.18       -0.05      1.06
QuietBrk 20d         1.09          1.38         2.33       -0.05      1.08
TrendPB 5%           0.97          1.81         1.19       -0.34      0.90
RSI-MR os=5          0.15          0.88         1.34       -0.65     -0.14

QuietBrk 20d is gated to confirmed UPTREND stocks only — its Bear/Crash exposure
is heavily filtered. RSI-MR is the only strategy with negative Sharpe in Mixed/Recent."""


# ---------------------------------------------------------------------------
# Deterministic Python-side regime classifier
#
# Produces a clear REGIME label + confidence from the snapshot numbers.
# This is passed directly into the prompt so the LLM does not need to infer
# the regime from raw percentages — it can focus purely on allocation.
# ---------------------------------------------------------------------------
_REGIME_RULES = [
    # (label, description, condition_fn, confidence)
    #
    # Rule ordering matters — first match wins.
    # CRASH_HIGHVOL must precede BEAR_CONFIRMED so that a high-vol deep crash
    # gets the breakout/trend-PB allocation (Sharpe 1.7–1.8) instead of the
    # DualMA-heavy bear allocation that is optimised for LOW-vol downtrends.
    # TRANSITION_UP must precede BEAR_CONFIRMED so that an improving bear gets
    # recovery allocation before the bear rule fires.
    ("CRASH_HIGHVOL",
     "Sharp selloff — >35% DOWNTREND and avg ATR% > 2.3%",
     lambda s: s["pct_downtrend"] > 0.35 and s["avg_atr_pct"] > 0.023,
     "HIGH"),
    ("TRANSITION_UP",
     "Breadth recovering — 5-day trend IMPROVING with >20% still in downtrend",
     lambda s: s.get("trend") == "IMPROVING" and s["pct_downtrend"] > 0.20,
     "MEDIUM"),
    ("BEAR_CONFIRMED",
     "Sustained downtrend — >45% stocks in DOWNTREND",
     lambda s: s["pct_downtrend"] > 0.45,
     "HIGH"),
    ("BEAR_EARLY",
     "Early/building downtrend — 35–45% in DOWNTREND",
     lambda s: 0.35 <= s["pct_downtrend"] <= 0.45,
     "MEDIUM"),
    ("RECOVERY",
     "Post-crash V-shape — >60% UPTREND and avg ATR% > 2.2%",
     lambda s: s["pct_uptrend"] > 0.60 and s["avg_atr_pct"] > 0.022,
     "HIGH"),
    ("BULL_SUSTAINED",
     "Sustained broad uptrend — >60% UPTREND and avg ATR% ≤ 2.2%",
     lambda s: s["pct_uptrend"] > 0.60 and s["avg_atr_pct"] <= 0.022,
     "HIGH"),
    ("BULL_LOWVOL",
     "Slow broad uptrend — >55% UPTREND and avg ATR% < 1.5%",
     lambda s: s["pct_uptrend"] > 0.55 and s["avg_atr_pct"] < 0.015,
     "HIGH"),
    ("BULL_MEDVOL",
     "Moderate uptrend — >55% UPTREND",
     lambda s: s["pct_uptrend"] > 0.55,
     "MEDIUM"),
    ("MIXED",
     "No dominant regime — moderate breadth on both sides",
     lambda s: True,    # fallback
     "LOW"),
]

# Per-regime HARD allocation constraints passed into the LLM prompt.
# "MUST be" language is intentional — prevents hedging.
_REGIME_ALLOCATION_RULES = {
    "TRANSITION_UP": (
        "TRANSITION / EARLY RECOVERY (breadth improving, downtrend declining). "
        "Market moving from bear to recovery. Early breakout and mean-reversion catch "
        "the first moves. Breakout MUST be ≥ 0.30. RSI-MR can be 0.10–0.20. "
        "DualMA MUST be ≥ 0.20. QuietBrk can be 0.15–0.20. TrendPB MUST be ≤ 0.15."
    ),
    "BEAR_CONFIRMED": (
        "BEAR CONFIRMED (>45% DOWNTREND). DualMA is the ONLY strategy with positive "
        "Bear Sharpe. DualMA MUST be ≥ 0.55. RSI-MR MUST be ≤ 0.05. "
        "QuietBrk MUST be ≤ 0.05 (or 0.0). TrendPB MUST be ≤ 0.10. "
        "Breakout can have 0.15–0.25 for short bursts."
    ),
    "BEAR_EARLY": (
        "BEAR EARLY (35–45% DOWNTREND). Regime is deteriorating — shift defensively. "
        "DualMA MUST be ≥ 0.40. RSI-MR MUST be ≤ 0.05. QuietBrk MUST be ≤ 0.15. "
        "TrendPB MUST be ≤ 0.15. Breakout can remain at 0.20–0.30."
    ),
    "CRASH_HIGHVOL": (
        "CRASH / HIGH VOL (>25% DOWNTREND, ATR>2.3%). High-vol moves favour Breakout "
        "(1.72) and TrendPB (1.81). Breakout MUST be ≥ 0.30. TrendPB MUST be ≥ 0.20. "
        "DualMA can be 0.20–0.30. RSI-MR MUST be ≤ 0.05. QuietBrk MUST be ≤ 0.10."
    ),
    "RECOVERY": (
        "RECOVERY (>60% UPTREND, high ATR). Breakout (3.18) and QuietBrk (2.33) dominate. "
        "Breakout MUST be ≥ 0.35. QuietBrk MUST be ≥ 0.25. "
        "DualMA can be 0.15–0.25. RSI-MR MUST be ≤ 0.05. TrendPB MUST be ≤ 0.15."
    ),
    "BULL_LOWVOL": (
        "BULL / LOW VOL (>55% UPTREND, ATR<1.5%). Slow trend favours QuietBrk (1.09) "
        "and TrendPB (0.97). QuietBrk MUST be ≥ 0.25. TrendPB MUST be ≥ 0.20. "
        "DualMA can be 0.20–0.30. RSI-MR MUST be ≤ 0.05 (Sharpe 0.15 — nearly useless here)."
    ),
    "BULL_SUSTAINED": (
        "BULL SUSTAINED (>60% UPTREND, normal vol). Multi-week broad uptrend — DualMA "
        "(1.69 Recent Sharpe) is co-equal with momentum strategies here. "
        "DualMA MUST be ≥ 0.25. Breakout MUST be ≥ 0.25. QuietBrk MUST be ≥ 0.20. "
        "RSI-MR MUST be ≤ 0.05. TrendPB can be 0.10–0.20."
    ),
    "BULL_MEDVOL": (
        "BULL / MODERATE VOL (>55% UPTREND). Balanced trending environment. "
        "Breakout MUST be ≥ 0.25. QuietBrk MUST be ≥ 0.20. DualMA MUST be ≥ 0.20. "
        "RSI-MR MUST be ≤ 0.05."
    ),
    "MIXED": (
        "MIXED regime. Diversify — no strategy should be below 0.10 unless its Sharpe "
        "is negative in this regime. RSI-MR can be ≤ 0.10 (negative Mixed Sharpe: -0.14). "
        "Balanced across DualMA, Breakout, QuietBrk, TrendPB."
    ),
}


def _classify_regime(snapshot: dict) -> tuple[str, str, str]:
    """
    Classify the current market regime from the snapshot.

    Returns
    -------
    (label, description, confidence)  — e.g. ("BEAR_CONFIRMED", "...", "HIGH")
    """
    for label, desc, condition, confidence in _REGIME_RULES:
        if condition(snapshot):
            return label, desc, confidence
    return "MIXED", "No dominant regime", "LOW"


class AdaptiveStrategySelector:
    """
    Weekly meta-layer that uses an LLM to allocate capital across strategies
    based on the current market regime.

    Improvements over naive single-snapshot approach:
    - Python-side _classify_regime() provides a deterministic regime label that the
      LLM uses directly, eliminating ambiguity about what the numbers mean.
    - 4-week rolling snapshot history lets the LLM see regime trends (e.g. downtrend
      building slowly) rather than reacting to a single noisy data point.
    - Hard numeric bounds ("DualMA MUST be ≥ 0.55") prevent the model from hedging
      toward a safe near-equal default in clearly asymmetric regimes.

    Parameters
    ----------
    strategy_names : list[str]
        Must match MultiStrategyRouter keys (e.g. ["DualMA", "Breakout", ...]).
    rebalance_frequency_days : int
        Minimum calendar days between LLM calls (default 5 ≈ one trading week).
    model : str
        OpenAI model. "gpt-4o-mini" for cost; "gpt-4o" for quality.
    verbose : bool
        Prints each weekly weight update to stdout if True.
    history_weeks : int
        Number of past weekly snapshots to include in each prompt (default 4).
    """

    def __init__(
        self,
        strategy_names: list[str],
        rebalance_frequency_days: int = 5,
        model: str = "gpt-4o-mini",
        verbose: bool = False,
        history_weeks: int = 4,
        regime_stability_weeks: int = 2,
        performance_table: str | None = None,
        on_rebalance: Optional[Callable] = None,
    ):
        self.client                   = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        self.strategy_names           = strategy_names
        self.rebalance_frequency_days = rebalance_frequency_days
        self.model                    = model
        self.verbose                  = verbose
        self.history_weeks            = history_weeks
        # Require a new regime to appear for this many consecutive weeks before
        # acting on it. Prevents whipsaw from 1-week regime spikes in choppy markets.
        self.regime_stability_weeks   = regime_stability_weeks
        # Injectable performance table — None means use the hardcoded full-history table.
        # Walk-forward validation injects a table computed from training data only.
        self._performance_table       = performance_table if performance_table is not None else _STRATEGY_REGIME_PERFORMANCE
        # Optional callback fired after each successful LLM rebalance.
        # Signature: on_rebalance(decided_at, regime, confidence, weights, snapshot, raw_response, model)
        self.on_rebalance             = on_rebalance

        n = max(len(strategy_names), 1)
        self.weights: dict[str, float]      = {s: 1.0 / n for s in strategy_names}
        self._last_updated: datetime | None = None
        self._call_count: int               = 0
        # Rolling buffer of (date_str, label, pct_uptrend, pct_downtrend, avg_atr_pct)
        self._snapshot_history: list[dict]  = []
        # Regime stability tracking
        self._confirmed_regime: str | None  = None   # last regime confirmed for ≥ stability_weeks
        self._pending_regime: str | None    = None   # candidate not yet confirmed
        self._pending_count: int            = 0      # consecutive weeks seen for pending
        # How many consecutive rebalances we have been in the confirmed regime.
        # Passed to the LLM so it knows whether to be cautious (week 1) or confident (week 3+).
        self._confirmed_weeks: int          = 0
        # Last raw LLM text response — captured in _call_llm, read by rebalance()
        self._last_raw_response: str | None = None

    # ------------------------------------------------------------------
    # PUBLIC API
    # ------------------------------------------------------------------
    def rebalance(
        self,
        current_date: datetime,
        regime_snapshot: dict,
    ) -> dict[str, float]:
        """
        Return the current weight dict, refreshing from the LLM if a full
        trading week has elapsed since the last call.
        """
        if self._last_updated is not None:
            elapsed = (current_date - self._last_updated).days
            if elapsed < self.rebalance_frequency_days:
                return self.weights

        # Classify regime deterministically before calling the LLM
        label, desc, confidence = _classify_regime(regime_snapshot)

        # Regime stability gate: require a new regime to appear for
        # `regime_stability_weeks` consecutive calls before switching allocation.
        # On first call (_confirmed_regime is None) act immediately.
        if self._confirmed_regime is None:
            self._confirmed_regime = label
            self._pending_regime   = None
            self._pending_count    = 0
            self._confirmed_weeks  = 1
            effective_label        = label
        elif label == self._confirmed_regime:
            # Still in the confirmed regime — reset any pending candidate
            self._pending_regime   = None
            self._pending_count    = 0
            self._confirmed_weeks += 1
            effective_label        = label
        else:
            # Different from confirmed — track as pending
            if label == self._pending_regime:
                self._pending_count += 1
            else:
                self._pending_regime = label
                self._pending_count  = 1

            if self._pending_count >= self.regime_stability_weeks:
                # Confirmed transition — promote pending to confirmed
                if self.verbose:
                    print(
                        f"  [AdaptiveSelector] Regime transition confirmed: "
                        f"{self._confirmed_regime} → {label} "
                        f"(after {self._pending_count} weeks)"
                    )
                self._confirmed_regime = label
                self._pending_regime   = None
                self._pending_count    = 0
                self._confirmed_weeks  = 1
                effective_label        = label
            else:
                # Not yet confirmed — hold the previous allocation
                effective_label = self._confirmed_regime
                if self.verbose:
                    print(
                        f"  [AdaptiveSelector] Regime pending: "
                        f"{label} ({self._pending_count}/{self.regime_stability_weeks} weeks) "
                        f"— holding {effective_label}"
                    )

        # Re-fetch desc/confidence for the effective label if it differs from raw label
        if effective_label != label:
            for lbl, d, _, conf in _REGIME_RULES:
                if lbl == effective_label:
                    desc, confidence = d, conf
                    break
            label = effective_label

        self._last_raw_response = None
        new_weights = self._call_llm(regime_snapshot, label, desc, confidence)
        if new_weights:
            self.weights = new_weights
            self._call_count += 1
            if self.verbose:
                w_str = "  ".join(f"{k}={v:.2f}" for k, v in self.weights.items())
                print(
                    f"  [AdaptiveSelector] {current_date.date()}"
                    f" [{label}/{confidence}] → {w_str}"
                )
            if self.on_rebalance is not None:
                try:
                    self.on_rebalance(
                        decided_at=current_date,
                        regime=label,
                        confidence=confidence,
                        weights=dict(self.weights),
                        snapshot=regime_snapshot,
                        raw_response=self._last_raw_response or "",
                        model=self.model,
                    )
                except Exception:
                    pass  # never let a logging callback break the backtest

        # Append this snapshot to rolling history (keep last history_weeks entries)
        self._snapshot_history.append({
            "date":          regime_snapshot.get("date", ""),
            "label":         label,
            "confidence":    confidence,
            "pct_uptrend":   regime_snapshot.get("pct_uptrend", 0),
            "pct_downtrend": regime_snapshot.get("pct_downtrend", 0),
            "avg_atr_pct":   regime_snapshot.get("avg_atr_pct", 0),
        })
        if len(self._snapshot_history) > self.history_weeks:
            self._snapshot_history.pop(0)

        self._last_updated = current_date
        return self.weights

    @property
    def call_count(self) -> int:
        """Total LLM API calls made (useful for cost estimation)."""
        return self._call_count

    # ------------------------------------------------------------------
    # PRIVATE
    # ------------------------------------------------------------------
    def _call_llm(
        self,
        regime_snapshot: dict,
        label: str,
        desc: str,
        confidence: str,
    ) -> dict[str, float] | None:
        """Make one OpenAI API call. Returns normalised weight dict or None on failure."""
        prompt = self._build_prompt(regime_snapshot, label, desc, confidence)
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                max_tokens=128,
                temperature=0.0,
                messages=[{"role": "user", "content": prompt}],
            )
            raw = response.choices[0].message.content.strip()
            self._last_raw_response = raw   # store before any stripping
            if raw.startswith("```"):
                parts = raw.split("```")
                raw = parts[1] if len(parts) > 1 else raw
                if raw.startswith("json"):
                    raw = raw[4:]
                raw = raw.strip()
            return self._parse_weights(raw)

        except Exception as exc:
            if self.verbose:
                print(f"  [AdaptiveSelector] LLM call failed ({exc}). Keeping weights.")
            return None

    def _parse_weights(self, raw: str) -> dict[str, float] | None:
        """Parse JSON, validate keys, clip negatives, normalise to sum=1.0."""
        try:
            parsed = json.loads(raw)
        except json.JSONDecodeError:
            return None

        clipped = {
            k: max(0.0, float(parsed[k]))
            for k in self.strategy_names
            if k in parsed
        }
        if not clipped:
            return None

        # DualMA floor: positive Sharpe in every regime — never below 0.10
        if "DualMA" in clipped and clipped["DualMA"] < 0.10:
            clipped["DualMA"] = 0.10

        total = sum(clipped.values())
        if total <= 0:
            return None

        return {k: clipped.get(k, 0.0) / total for k in self.strategy_names}

    def _build_prompt(
        self,
        snapshot: dict,
        label: str,
        desc: str,
        confidence: str,
    ) -> str:
        """Build the LLM prompt with regime classification + rolling history."""
        # --- Rolling history block with SWITCH annotations ---
        history_lines = []
        prev_label = None
        for h in self._snapshot_history:
            switch_tag = "  ← SWITCH" if (prev_label is not None and h["label"] != prev_label) else ""
            history_lines.append(
                f"  {h['date']}  [{h['label']}/{h['confidence']}]"
                f"  UP={h['pct_uptrend']:.1%}"
                f"  DOWN={h['pct_downtrend']:.1%}"
                f"  ATR={h['avg_atr_pct']:.2%}"
                + switch_tag
            )
            prev_label = h["label"]
        history_block = (
            "Recent regime history (oldest → newest):\n" + "\n".join(history_lines)
            if history_lines else "  (first rebalance — no history yet)"
        )

        # --- Inferred trend direction when RegimeContextAgent is absent ---
        inferred_trend = snapshot.get("trend")  # set by RegimeContextAgent if active
        if inferred_trend is None and len(self._snapshot_history) >= 2:
            delta = (self._snapshot_history[-1]["pct_downtrend"]
                     - self._snapshot_history[-2]["pct_downtrend"])
            if delta > 0.03:
                inferred_trend = "DETERIORATING"
            elif delta < -0.03:
                inferred_trend = "IMPROVING"
            else:
                inferred_trend = "STABLE"

        # --- Regime age context ---
        regime_age_note = (
            f"Regime confirmed for: {self._confirmed_weeks} rebalance(s)\n"
            f"  (Week 1 = just switched — stay close to equal weight until confirmed.\n"
            f"   Week 3+ = well-established — apply MANDATORY RULE fully.)"
        )

        # --- Hard rule for the classified regime ---
        regime_rule = _REGIME_ALLOCATION_RULES.get(label, _REGIME_ALLOCATION_RULES["MIXED"])

        expected_json = (
            "{"
            + ", ".join(f'"{n}": 0.XX' for n in self.strategy_names)
            + "}"
        )

        # --- Broad breadth block (only when RegimeContextAgent is active) ---
        broad_regime = snapshot.get("broad_regime")
        broad_block = ""
        if broad_regime:
            broad_block = (
                f"\nBROAD MARKET BREADTH (150-symbol universe):\n"
                f"  Broad regime:    {broad_regime}\n"
                f"  Trend direction: {snapshot.get('trend', 'N/A')}\n"
                f"  % above SMA_50:  {snapshot.get('pct_above_sma50_broad', 0):.1%}\n"
                f"  Adv/Dec ratio:   {snapshot.get('advance_decline_ratio', 0):.1%}\n"
            )
        elif inferred_trend:
            broad_block = f"\n  Inferred breadth trend: {inferred_trend} (computed from history)\n"

        return f"""You are allocating capital across five NSE Indian equity trading strategies for the next week.

CURRENT REGIME (Python-classified, confidence {confidence}):
  {label} — {desc}
  Date:        {snapshot.get('date', '?')}
  % UPTREND:   {snapshot.get('pct_uptrend', 0):.1%}
  % DOWNTREND: {snapshot.get('pct_downtrend', 0):.1%}
  % SIDEWAYS:  {snapshot.get('pct_sideways', 0):.1%}
  % HIGH_VOL:  {snapshot.get('pct_high_vol', 0):.1%}
  Avg ATR%:    {snapshot.get('avg_atr_pct', 0):.2%}
{broad_block}
{regime_age_note}

{history_block}

{self._performance_table}

MANDATORY ALLOCATION RULE FOR THIS REGIME:
{regime_rule}

GLOBAL RULES (always apply):
- Weights sum to 1.0 exactly. All values in [0.0, 1.0].
- Minimum viable weight: 0.05. Either 0.0 (disabled) or ≥ 0.05.
- Follow the MANDATORY RULE above. Do not soften it.
- If breadth trend is DETERIORATING, lean more defensively than the regime label alone suggests.
- If breadth trend is IMPROVING, you may lean slightly more offensively within rule bounds.
- Rows marked ← SWITCH in history indicate a regime change that week.

Respond ONLY with a JSON object, no explanation, no markdown:
{expected_json}"""
