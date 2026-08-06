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

from app.meta.llm_cache import get_default_cache


# ---------------------------------------------------------------------------
# Empirical Sharpe table — derived mechanically from solo-strategy backtests.
# (net of 0.10% commission + 0.05% slippage per side)
#
# Recalibrated 2026-05-30 from no_atr_stop_adaptive_test.md / new_version_quiet.md.
# Each cell = solo-strategy Sharpe in the period whose dominant regime matches:
#   Bull/LowVol  = avg(Bull 2019, Live 2025-26)
#   Crash/HighVol = Crash 2020
#   Recovery     = Recov 2020-21
#   Bear/Choppy  = Bear 2022
#   Mixed        = avg(Recent 2022-24, Full 2018-24)
# Prior table (2026-03-21) preserved in PRIOR_STRATEGY_REGIME_PERFORMANCE below
# for rollback. Two prior cells flipped sign on real data — see the table.
# ---------------------------------------------------------------------------
_STRATEGY_REGIME_PERFORMANCE = """\
Strategy Sharpe ratios by market regime (NSE Indian equities, latest backtests):

                  Bull/LowVol  Crash/HighVol  Recovery  Bear/Choppy  Mixed
DualMA SMA20/50     -0.05         1.67         1.87       -0.20      0.64
Breakout 10d        -0.21         1.72         2.62        0.26      0.86
QuietBrk 20d         0.26         1.95         2.42       -0.22      0.81
TrendPB 5%           0.93         1.83         1.30       -0.40      0.84
RSI-MR os=5          0.14         1.05         1.31       -0.97     -0.06

Notable shifts vs the prior table:
  - DualMA Bear/Choppy flipped from +0.51 to -0.20 (Bear 2022 solo). The
    "DualMA is the only positive Bear strategy" claim is no longer true.
  - Breakout Bear/Choppy flipped from -0.05 to +0.26 — Breakout is now the
    best Bear performer.
  - DualMA Bull/LowVol fell from +0.44 to near zero (-0.05) on Bull '19 +
    Live '25-26 evidence — a low-vol uptrend bleeds the medium-term MA.
  - TrendPB Bull/LowVol confirmed strong (+0.93) — the only consistent
    positive strategy in narrow uptrends across both Bull '19 and Live."""


# Prior table kept for rollback / A-B comparison.
PRIOR_STRATEGY_REGIME_PERFORMANCE = """\
Strategy Sharpe ratios by market regime (NSE Indian equities, 2018–2024 backtests):

                  Bull/LowVol  Crash/HighVol  Recovery  Bear/Choppy  Mixed
DualMA SMA20/50      0.44          1.28         2.66        0.51      1.69
Breakout 10d         0.93          1.72         3.18       -0.05      1.06
QuietBrk 20d         1.09          1.38         2.33       -0.05      1.08
TrendPB 5%           0.97          1.81         1.19       -0.34      0.90
RSI-MR os=5          0.15          0.88         1.34       -0.65     -0.14"""


# ---------------------------------------------------------------------------
# Deterministic Python-side regime classifier
#
# Produces a clear REGIME label + confidence from the snapshot numbers.
# This is passed directly into the prompt so the LLM does not need to infer
# the regime from raw percentages — it can focus purely on allocation.
# ---------------------------------------------------------------------------


def _vol(s: dict) -> float:
    """
    Volatility signal used by the BULL_*/CRASH_HIGHVOL/RECOVERY rules.

    Prefers the broad-universe `avg_rolling_vol_5d` (computed by
    RegimeContextAgent across the 150-stock cache) when present. Falls back to
    the narrow-universe `avg_atr_pct` (computed across the active 24-80 set)
    when RCA isn't wired in.

    Why: the narrow universe is high-vol by construction (DynamicUniverseAgent
    ranks by activity, which selects volatile stocks). Per the per-period
    diagnostics under `issues/`, `avg_atr_pct` sat at 0.024-0.030 across the
    Bull/Recent/Live periods — above the 0.022 BULL_SUSTAINED threshold on
    essentially every week. That made the BULL_* family dead code in
    production. Broad `avg_rolling_vol_5d` runs ~0.014-0.020 over the same
    periods and properly fires BULL_SUSTAINED on the weeks the broad market
    is actually in a calm uptrend.

    Backward-compatible: plain Adaptive (no RCA) snapshots have no
    `avg_rolling_vol_5d` key → this helper falls back to `avg_atr_pct` and the
    classifier behaves byte-identically to before. The behaviour shift only
    fires on Adaptive+RCA runs.
    """
    # A/B toggle: META_VOL=narrow forces the pre-branch (main) behaviour of using
    # narrow avg_atr_pct for regime classification, so the broad-vol swap can be
    # isolated. Default (unset/broad) keeps the branch behaviour.
    if os.environ.get("META_VOL") == "narrow":
        return s.get("avg_atr_pct", 0.0)
    v = s.get("avg_rolling_vol_5d")
    if v is None:
        return s.get("avg_atr_pct", 0.0)
    return v


_REGIME_RULES = [
    # (label, description, condition_fn, confidence)
    #
    # Rule ordering matters — first match wins.
    # CRASH_HIGHVOL must precede BEAR_CONFIRMED so that a high-vol deep crash
    # gets the breakout/trend-PB allocation (Sharpe 1.7–1.8) instead of the
    # DualMA-heavy bear allocation that is optimised for LOW-vol downtrends.
    # TRANSITION_UP must precede BEAR_CONFIRMED so that an improving bear gets
    # recovery allocation before the bear rule fires.
    #
    # Vol input via _vol(s): broad rolling_vol_5d when RCA present, narrow
    # avg_atr_pct otherwise. Breadth (pct_uptrend / pct_downtrend) is
    # unchanged — narrow and broad breadth agreed in the diagnostics; only
    # volatility was the dominant defect. Thresholds retained — they were the
    # right values for the data scale, just applied to the wrong input.
    ("CRASH_HIGHVOL",
     "Sharp selloff — >35% DOWNTREND and avg vol > 2.3%",
     lambda s: s["pct_downtrend"] > 0.35 and _vol(s) > 0.023,
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
     "Post-crash V-shape — >60% UPTREND and avg vol > 2.2%",
     lambda s: s["pct_uptrend"] > 0.60 and _vol(s) > 0.022,
     "HIGH"),
    ("BULL_SUSTAINED",
     "Sustained broad uptrend — >60% UPTREND and avg vol ≤ 2.2%",
     lambda s: s["pct_uptrend"] > 0.60 and _vol(s) <= 0.022,
     "HIGH"),
    ("BULL_LOWVOL",
     "Slow broad uptrend — >55% UPTREND and avg vol < 1.5%",
     lambda s: s["pct_uptrend"] > 0.55 and _vol(s) < 0.015,
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
#
# Sharpe values referenced in prose come from _STRATEGY_REGIME_PERFORMANCE above
# (recalibrated 2026-05-30). MUST/cap statements mirror _REGIME_WEIGHT_BOUNDS
# below — both are derived from the same Sharpe-band rule (see module docstring).
_REGIME_ALLOCATION_RULES = {
    "TRANSITION_UP": (
        "TRANSITION / EARLY RECOVERY (breadth improving, downtrend declining). "
        "Treat like Recovery — momentum strategies regain edge first. "
        "Breakout MUST be ≥ 0.15. QuietBrk MUST be ≥ 0.15. TrendPB MUST be ≥ 0.15. "
        "DualMA MUST be ≥ 0.15. RSI-MR MUST be ≥ 0.10 (positive Sharpe in transitions)."
    ),
    "BEAR_CONFIRMED": (
        "BEAR CONFIRMED (>45% DOWNTREND). Breakout (+0.26) is the only positive-Sharpe "
        "strategy on Bear 2022 evidence. Breakout MUST be ≥ 0.15. "
        "DualMA cap ≤ 0.15 (Sharpe -0.20). QuietBrk cap ≤ 0.15 (Sharpe -0.22). "
        "TrendPB cap ≤ 0.10 (Sharpe -0.40). RSI-MR cap ≤ 0.05 (Sharpe -0.97)."
    ),
    "BEAR_EARLY": (
        "BEAR EARLY (35–45% DOWNTREND). Same shape as BEAR_CONFIRMED but less extreme. "
        "Breakout MUST be ≥ 0.15. DualMA cap ≤ 0.15. QuietBrk cap ≤ 0.15. "
        "TrendPB cap ≤ 0.10. RSI-MR cap ≤ 0.05."
    ),
    "CRASH_HIGHVOL": (
        "CRASH / HIGH VOL. All strategies show strong Sharpe on Crash 2020 — "
        "diversify aggressively. Breakout, QuietBrk, TrendPB, DualMA each MUST be ≥ 0.15. "
        "RSI-MR MUST be ≥ 0.10 (Sharpe 1.05). Avoid concentration in any single name."
    ),
    "RECOVERY": (
        "RECOVERY (>60% UPTREND, high ATR). Every strategy posted Sharpe > 1.20 on "
        "Recov 2020-21. Spread broadly: all five strategies MUST be ≥ 0.15. "
        "Breakout and QuietBrk lead but the regime rewards diversified momentum."
    ),
    "BULL_LOWVOL": (
        "BULL / LOW VOL (>55% UPTREND, ATR<1.5%). Narrow uptrends penalise momentum. "
        "TrendPB (+0.93) is the only consistent positive strategy here — TrendPB MUST be ≥ 0.15. "
        "DualMA cap ≤ 0.15 (Sharpe -0.05). Breakout cap ≤ 0.15 (Sharpe -0.21). "
        "QuietBrk and RSI-MR are free in the 0–0.30 range (mild positives)."
    ),
    "BULL_SUSTAINED": (
        "BULL SUSTAINED (>60% UPTREND, normal vol). Balanced uptrend — momentum + "
        "trend-following both work. Breakout MUST be ≥ 0.15. QuietBrk MUST be ≥ 0.15. "
        "TrendPB MUST be ≥ 0.15. DualMA MUST be ≥ 0.15. RSI-MR cap ≤ 0.15."
    ),
    "BULL_MEDVOL": (
        "BULL / MODERATE VOL (>55% UPTREND). Same shape as BULL_SUSTAINED. "
        "Breakout MUST be ≥ 0.15. QuietBrk MUST be ≥ 0.15. TrendPB MUST be ≥ 0.15. "
        "DualMA MUST be ≥ 0.15. RSI-MR cap ≤ 0.15."
    ),
    "MIXED": (
        "MIXED regime. Four of five strategies show Sharpe ≥ 0.60 on the Mixed bucket. "
        "Breakout MUST be ≥ 0.15. QuietBrk MUST be ≥ 0.15. TrendPB MUST be ≥ 0.15. "
        "DualMA MUST be ≥ 0.15. RSI-MR cap ≤ 0.15 (slightly negative Sharpe -0.06)."
    ),
}


# ---------------------------------------------------------------------------
# Machine-readable mirror of the HARD ("MUST") bounds in the prose rules above.
# Used by _apply_regime_bounds() to DETERMINISTICALLY enforce the constraints
# after the LLM responds — the prompt says "MUST" but gpt-4o-mini does not
# always comply (e.g. QuietBrk=0 in BULL_SUSTAINED where the rule says ≥0.20,
# or DualMA omitted in BULL_MEDVOL). Only "MUST" bounds are encoded; soft
# "can be" ranges are left to the LLM. (lo, hi); None = unbounded that side.
# Strategy keys must match strategy_names.
# ---------------------------------------------------------------------------
_REGIME_WEIGHT_BOUNDS: dict[str, dict[str, tuple]] = {
    "TRANSITION_UP":  {"Breakout": (0.30, None), "DualMA": (0.20, None),
                       "TrendPB": (None, 0.15)},
    "BEAR_CONFIRMED": {"DualMA": (0.55, None), "RSI-MR": (None, 0.05),
                       "QuietBrk": (None, 0.05), "TrendPB": (None, 0.10)},
    "BEAR_EARLY":     {"DualMA": (0.40, None), "RSI-MR": (None, 0.05),
                       "QuietBrk": (None, 0.15), "TrendPB": (None, 0.15)},
    "CRASH_HIGHVOL":  {"Breakout": (0.30, None), "TrendPB": (0.20, None),
                       "RSI-MR": (None, 0.05), "QuietBrk": (None, 0.10)},
    "RECOVERY":       {"Breakout": (0.35, None), "QuietBrk": (0.25, None),
                       "RSI-MR": (None, 0.05), "TrendPB": (None, 0.15)},
    "BULL_LOWVOL":    {"QuietBrk": (0.25, None), "TrendPB": (0.20, None),
                       "RSI-MR": (None, 0.05)},
    "BULL_SUSTAINED": {"DualMA": (0.25, None), "Breakout": (0.25, None),
                       "QuietBrk": (0.20, None), "RSI-MR": (None, 0.05)},
    "BULL_MEDVOL":    {"Breakout": (0.25, None), "QuietBrk": (0.20, None),
                       "DualMA": (0.20, None), "RSI-MR": (None, 0.05)},
    "MIXED":          {"RSI-MR": (None, 0.10)},
}


def _apply_regime_bounds(weights: dict, label: str | None) -> dict:
    """
    Deterministically enforce the HARD per-regime MUST bounds (the prose rules
    are advisory to the LLM; this guarantees compliance regardless of model).

    Loose constraints (sum of floors < 1, generous caps) → a few
    clamp→renormalise iterations converge to satisfy both floors and caps.
    Returns an un-normalised dict; the caller normalises to sum 1.
    """
    bounds = _REGIME_WEIGHT_BOUNDS.get(label or "")
    if not bounds:
        return weights
    w = dict(weights)
    for _ in range(4):
        for strat, (lo, hi) in bounds.items():
            if strat in w:
                if hi is not None:
                    w[strat] = min(w[strat], hi)
                if lo is not None:
                    w[strat] = max(w[strat], lo)
        s = sum(w.values())
        if s <= 0:
            return weights
        w = {k: v / s for k, v in w.items()}
    return w


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
        feedback_agent: object | None = None,
    ):
        # Provider switch: LLM_PROVIDER=gemini routes through Gemini's
        # OpenAI-compatible endpoint (free tier). Default = OpenAI.
        _provider = os.environ.get("LLM_PROVIDER", "openai").lower()
        if _provider == "gemini":
            self.client = OpenAI(
                base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
                api_key=os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY"),
            )
            self._provider = "gemini"
            self._use_seed = False   # Gemini's OpenAI-compat layer rejects `seed`
        else:
            self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
            self._provider = "openai"
            self._use_seed = True
        self.strategy_names           = strategy_names
        self.rebalance_frequency_days = rebalance_frequency_days
        # On Gemini, override the caller-supplied model with a Gemini id.
        self.model                    = (
            os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")
            if self._provider == "gemini" else model
        )
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
        # Optional pluggable agent that supplies an LLM-prompt feedback block.
        # Any object exposing `build_feedback_block(date) -> str | None` qualifies.
        # See app/meta/performance_feedback_agent.py (Phase 1: recent strategy P&L).
        # When None, _build_prompt emits a byte-identical prompt to the legacy
        # version — this preserves _ADAPTIVE_BASELINE regression equality.
        self.feedback_agent           = feedback_agent

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
        # Last LLM-parsed weights BEFORE any clamp (DualMA floor, regime bounds,
        # feedback agent). Captured in _parse_weights so the rebalance log can
        # compare raw LLM intent vs final-applied weights.
        self._last_raw_weights: dict[str, float] | None = None
        # Last prompt hash (= LLM cache key) — captured in _call_llm, dumped by
        # rebalance() when PROMPT_HASH_DUMP is set. Used to diff the Adaptive
        # prompt stream between ADAPTIVE_ONLY=1 and =0 runs.
        self._last_prompt_sha: str | None = None
        # Capital tier from the latest snapshot (MICRO/SMALL/NORMAL). Set in
        # rebalance(); read by _parse_weights() to relax the DualMA floor when
        # the low-capital concentration rule is active. Default NORMAL keeps
        # the original behaviour for accounts that never pass capital.
        self._capital_tier: str = "NORMAL"

        # Experiment toggle: when False, skip all post-LLM clamping
        # (DualMA floor, _apply_regime_bounds MUSTs, feedback_agent caps) so
        # the LLM's raw allocation flows through unchanged. Driven by env var
        # LLM_CLAMP_WEIGHTS so the harness/runners don't need any code changes
        # to A/B-test "is clamping helping?". Defaults to True (legacy behaviour).
        self.clamp_weights: bool = os.environ.get("LLM_CLAMP_WEIGHTS", "1") != "0"

        # Optional JSONL log of every rebalance (date, regime, raw_response,
        # pre-clamp weights, final weights, clamp_active flag). Set the path
        # via ADAPTIVE_LOG_PATH env var. None = no logging. File is opened in
        # append mode each rebalance so multiple periods accumulate in one file.
        self._log_path: str | None = os.environ.get("ADAPTIVE_LOG_PATH") or None

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

        # Capture capital tier for this rebalance so _parse_weights() can relax
        # the DualMA floor at concentration tiers.
        self._capital_tier = regime_snapshot.get("capital_tier", "NORMAL")

        self._last_raw_response = None
        self._last_raw_weights  = None
        new_weights = self._call_llm(regime_snapshot, label, desc, confidence)

        # ── PROMPT_HASH_DUMP diagnostic (env-gated; no-op unless set) ──────────
        # One record per rebalance (LLM call). Same code path in both modes —
        # the only difference between runs is the ADAPTIVE_ONLY env var — so any
        # divergence in prompt_sha for the same (period, date, leg) proves the
        # Adaptive prompt inputs leak from the solo/EqW legs. The leg is inferred
        # from a snapshot field only RCA populates (pct_above_sma50_broad).
        _dump = os.environ.get("PROMPT_HASH_DUMP")
        if _dump:
            try:
                leg = ("Adaptive+RCA"
                       if regime_snapshot.get("pct_above_sma50_broad") is not None
                       else "Adaptive")
                rec = {
                    "mode":       os.environ.get("ADAPTIVE_ONLY", "0"),
                    "period":     os.environ.get("PERIOD", ""),
                    "date":       str(current_date.date()),
                    "leg":        leg,
                    "regime":     label,
                    "prompt_sha": self._last_prompt_sha,
                }
                with open(_dump, "a") as f:
                    f.write(json.dumps(rec) + "\n")
            except Exception:
                pass

        if new_weights:
            self.weights = new_weights
            self._call_count += 1
            if self.verbose:
                w_str = "  ".join(f"{k}={v:.2f}" for k, v in self.weights.items())
                clamp_tag = "" if self.clamp_weights else "  [NO-CLAMP]"
                print(
                    f"  [AdaptiveSelector] {current_date.date()}"
                    f" [{label}/{confidence}] → {w_str}{clamp_tag}"
                )
                if not self.clamp_weights and self._last_raw_weights:
                    raw_str = "  ".join(
                        f"{k}={v:.2f}" for k, v in self._last_raw_weights.items()
                    )
                    print(f"  [AdaptiveSelector raw_llm] → {raw_str}")

            # Optional JSONL rebalance log — one record per LLM call. Append
            # mode so multiple periods write to the same file. Disable any
            # logging exception so a write failure never breaks the backtest.
            #
            # Snapshot fields (the classifier inputs) are included so a downstream
            # diagnostic can answer "why was this week labelled REGIME_X?" and
            # cross-check the narrow-universe pct_uptrend against the
            # broad-universe pct_above_sma50_broad (when RCA is active).
            if self._log_path:
                try:
                    entry = {
                        "date":         str(current_date.date()),
                        "period":       os.environ.get("PERIOD", ""),  # set by runner
                        "regime":       label,
                        "confidence":   confidence,
                        "clamp_active": bool(self.clamp_weights),
                        # --- Snapshot inputs that fed the classifier ---
                        "pct_uptrend":            regime_snapshot.get("pct_uptrend"),
                        "pct_downtrend":          regime_snapshot.get("pct_downtrend"),
                        "pct_sideways":           regime_snapshot.get("pct_sideways"),
                        "pct_high_vol":           regime_snapshot.get("pct_high_vol"),
                        "avg_atr_pct":            regime_snapshot.get("avg_atr_pct"),
                        "universe_size":          regime_snapshot.get("universe_size"),
                        # --- RCA-only broad-universe enrichments (None when RCA off) ---
                        "pct_above_sma50_broad":  regime_snapshot.get("pct_above_sma50_broad"),
                        "advance_decline_ratio":  regime_snapshot.get("advance_decline_ratio"),
                        "avg_rolling_vol_5d":     regime_snapshot.get("avg_rolling_vol_5d"),
                        "broad_universe_size":    regime_snapshot.get("broad_universe_size"),
                        "trend":                  regime_snapshot.get("trend"),
                        "broad_regime":           regime_snapshot.get("broad_regime"),
                        # --- LLM output + final weights ---
                        "raw_response": self._last_raw_response,
                        "raw_weights":  self._last_raw_weights,
                        "final_weights": dict(self.weights),
                    }
                    with open(self._log_path, "a") as f:
                        f.write(json.dumps(entry) + "\n")
                except Exception:
                    pass
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
        cache = get_default_cache()
        # Capture the prompt hash (= cache key) for the PROMPT_HASH_DUMP diagnostic.
        # This is byte-for-byte the same key the cache uses, so it directly answers
        # "would these two runs hit the same cached LLM response?".
        self._last_prompt_sha = cache.make_key(prompt, self.model)

        def _do_api_call() -> str:
            import time
            kwargs = dict(
                model=self.model,
                max_tokens=128,
                temperature=0.0,
                messages=[{"role": "user", "content": prompt}],
            )
            if self._use_seed:
                kwargs["seed"] = 0   # OpenAI-only: pins API-side sampling for
                                     # reproducibility (cf. meta_layer_value_leak §12b).
            if self._provider == "gemini":
                # gemini-2.5-* are thinking models: internal reasoning consumes the
                # output-token budget and truncates the JSON answer. Disable thinking
                # (reasoning_effort=none) and give ample budget so the full weight
                # dict is emitted.
                kwargs["max_tokens"] = 2048
                kwargs["extra_body"] = {"reasoning_effort": "none"}
            last_exc = None
            for attempt in range(4):
                try:
                    response = self.client.chat.completions.create(**kwargs)
                    return response.choices[0].message.content.strip()
                except Exception as e:  # noqa: BLE001
                    last_exc = e
                    if "429" in str(e) or "rate" in str(e).lower() or "quota" in str(e).lower():
                        time.sleep(2 * (attempt + 1))   # backoff on rate limit
                        continue
                    raise
            raise last_exc

        try:
            raw = cache.get_or_call(prompt, self.model, _do_api_call)
            self._last_raw_response = raw   # store before any stripping
            if raw.startswith("```"):
                parts = raw.split("```")
                raw = parts[1] if len(parts) > 1 else raw
                if raw.startswith("json"):
                    raw = raw[4:]
                raw = raw.strip()
            return self._parse_weights(raw, label)

        except Exception as exc:
            if self.verbose:
                print(f"  [AdaptiveSelector] LLM call failed ({exc}). Keeping weights.")
            return None

    def _parse_weights(self, raw: str, label: str | None = None) -> dict[str, float] | None:
        """Parse JSON, clip negatives, enforce per-regime MUST bounds, normalise.

        When self.clamp_weights is False, skip the post-LLM clamping path
        entirely (DualMA floor, _apply_regime_bounds MUSTs, feedback agent
        adjustments) — the LLM's raw allocation flows straight through, only
        normalized to sum=1.0. Use this to A/B-test whether the clamping is
        helping or constraining the LLM's actual judgment.
        """
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

        # Snapshot the raw LLM allocation (post-zero-clip, pre-clamp) so the
        # rebalance log can show what the LLM actually wanted vs what we sent
        # to the router. Normalize to 1.0 here so it's directly comparable to
        # `weights`. Skip strategies the LLM omitted (treat as 0.0).
        raw_materialised = {k: clipped.get(k, 0.0) for k in self.strategy_names}
        raw_total = sum(raw_materialised.values()) or 1.0
        self._last_raw_weights = {
            k: raw_materialised[k] / raw_total for k in self.strategy_names
        }

        if not self.clamp_weights:
            # Experiment path: no DualMA floor, no regime bounds, no feedback
            # caps. Just normalise the raw LLM output.
            total = sum(raw_materialised.values())
            if total <= 0:
                return None
            return {k: raw_materialised[k] / total for k in self.strategy_names}

        # DualMA floor: positive Sharpe in every regime — never below 0.10.
        # Skipped at concentration tiers (MICRO/SMALL): forcing DualMA back to
        # 0.10 would dilute the deliberate 1–2 strategy concentration the
        # low-capital rule requires (and re-add a strategy the LLM zeroed).
        if (
            self._capital_tier not in ("MICRO", "SMALL")
            and "DualMA" in clipped
            and clipped["DualMA"] < 0.10
        ):
            clipped["DualMA"] = 0.10

        # Materialise over ALL strategies (missing → 0.0) so a regime FLOOR
        # also lifts a strategy the LLM omitted entirely (e.g. DualMA absent
        # in BULL_MEDVOL where the rule says ≥ 0.20).
        weights = {k: clipped.get(k, 0.0) for k in self.strategy_names}

        # Deterministic MUST-bound enforcement — NORMAL tier only. At
        # MICRO/SMALL the capital rule deliberately concentrates into 1–2
        # strategies and MUST NOT be clamped back to the diversification
        # floors (this also keeps the §9 low-capital results unchanged).
        if self._capital_tier not in ("MICRO", "SMALL"):
            weights = _apply_regime_bounds(weights, label)

            # Optional post-LLM weight adjustment from a feedback agent
            # (e.g. DeterministicPerformanceFeedbackAgent caps bleeders).
            # Runs AFTER _apply_regime_bounds so the cap overrides the
            # regime MUST floor — that's the intended semantics: regime
            # floors assume the strategy is capturing its edge; a
            # 30d-bleeder isn't, so we override the floor for that strat.
            # When the agent has no adjust_weights method (e.g. the LLM
            # prompt-based PerformanceFeedbackAgent) this is a no-op.
            if self.feedback_agent is not None and hasattr(
                self.feedback_agent, "adjust_weights"
            ):
                adjusted = self.feedback_agent.adjust_weights(weights, label)
                if adjusted is not None:
                    weights = adjusted

        total = sum(weights.values())
        if total <= 0:
            return None

        return {k: weights[k] / total for k in self.strategy_names}

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

        # --- Capital concentration block (only at MICRO/SMALL tiers) ---
        # NORMAL tier (or no capital supplied) → both strings empty, so the
        # prompt is byte-identical to the pre-capital version. This is what
        # keeps the ₹1L _ADAPTIVE_BASELINE regression valid.
        capital      = snapshot.get("capital")
        capital_tier = snapshot.get("capital_tier", "NORMAL")
        capital_block = ""
        capital_rule  = ""
        if capital_tier == "MICRO":
            capital_block = (
                f"\nACCOUNT CAPITAL: ₹{capital:,.0f} (MICRO tier)\n"
                f"  This account is too small to diversify — split 5 ways, each strategy\n"
                f"  gets too little to buy even one share of most stocks. Concentrate.\n"
            )
            capital_rule = (
                "\n\nCAPITAL CONCENTRATION RULE (this OVERRIDES the diversification "
                "language in the regime rule above):\n"
                "- Allocate to AT MOST 2 strategies.\n"
                "- Put >= 0.60 on the single best strategy for this regime; the "
                "2nd-best may take the remainder.\n"
                "- ALL other strategies MUST be exactly 0.0.\n"
                "- Choose from the strategies the regime rule favours. Do NOT spread "
                "weight to satisfy minimums — minimums are waived at this tier."
            )
        elif capital_tier == "SMALL":
            capital_block = (
                f"\nACCOUNT CAPITAL: ₹{capital:,.0f} (SMALL tier)\n"
                f"  Limited capital — broad 5-way diversification wastes it on\n"
                f"  sub-one-share slots. Lean concentrated.\n"
            )
            capital_rule = (
                "\n\nCAPITAL CONCENTRATION RULE (this OVERRIDES the diversification "
                "language in the regime rule above):\n"
                "- Allocate to AT MOST 3 strategies.\n"
                "- Put >= 0.45 on the single best strategy for this regime.\n"
                "- Any strategy that would be below 0.15 MUST instead be 0.0."
            )

        # --- Optional feedback block (e.g. recent strategy P&L) -----------
        # When feedback_agent is None OR build_feedback_block() returns None
        # (not warm), `feedback_block` is "" and the substitution below is
        # byte-identical to the legacy prompt — guarantees _ADAPTIVE_BASELINE
        # regression equality at default-off.
        feedback_block = ""
        if self.feedback_agent is not None:
            # Pass the snapshot's string date (the snapshot dict carries
            # 'date' but not 'date_dt'). The PerformanceFeedbackAgent ignores
            # this argument anyway, but other future feedback agents may use it.
            block = self.feedback_agent.build_feedback_block(snapshot.get("date"))
            if block:
                feedback_block = "\n\n" + block
                # One-shot diagnostic so the operator can confirm the agent
                # is actually reaching the LLM during a backtest. Fires once
                # per selector instance the first time the block is injected
                # — regardless of self.verbose, because operators need this
                # confirmation even when running the (less chatty) RCA path.
                if not getattr(self, "_paa_announced", False):
                    print(
                        f"  [AdaptiveSelector] PAA feedback ACTIVE — first injection "
                        f"at {snapshot.get('date', '?')} (block_chars={len(block)})"
                    )
                    self._paa_announced = True

        return f"""You are allocating capital across five NSE Indian equity trading strategies for the next week.

CURRENT REGIME (Python-classified, confidence {confidence}):
  {label} — {desc}
  Date:        {snapshot.get('date', '?')}
  % UPTREND:   {snapshot.get('pct_uptrend', 0):.1%}
  % DOWNTREND: {snapshot.get('pct_downtrend', 0):.1%}
  % SIDEWAYS:  {snapshot.get('pct_sideways', 0):.1%}
  % HIGH_VOL:  {snapshot.get('pct_high_vol', 0):.1%}
  Avg ATR%:    {snapshot.get('avg_atr_pct', 0):.2%}
{broad_block}{capital_block}
{regime_age_note}

{history_block}

{self._performance_table}

MANDATORY ALLOCATION RULE FOR THIS REGIME:
{regime_rule}{capital_rule}{feedback_block}

GLOBAL RULES (always apply):
- Weights sum to 1.0 exactly. All values in [0.0, 1.0].
- Minimum viable weight: 0.05. Either 0.0 (disabled) or ≥ 0.05.
- Follow the MANDATORY RULE above. Do not soften it.
- If breadth trend is DETERIORATING, lean more defensively than the regime label alone suggests.
- If breadth trend is IMPROVING, you may lean slightly more offensively within rule bounds.
- Rows marked ← SWITCH in history indicate a regime change that week.

Respond ONLY with a JSON object, no explanation, no markdown:
{expected_json}"""
