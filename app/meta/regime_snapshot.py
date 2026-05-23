# app/meta/regime_snapshot.py
#
# Builds a lightweight regime statistics dict from the daily symbol states
# that are already computed in BacktestEngine's daily loop.
# No additional DB access or data fetching required.
#
# Used by AdaptiveStrategySelector (step 12) to construct the LLM prompt,
# and independently useful for logging / analysis.

from datetime import datetime

from app.meta.capital_profile import EQUITY_FLOOR, SMALL_FLOOR


def _capital_tier(capital: float | None) -> str:
    """
    Map account capital to a tier the LLM uses to decide how concentrated the
    allocation must be. None → NORMAL so the default path is unchanged.

      MICRO  : < SMALL_FLOOR (₹25k)            — diversification impossible
      SMALL  : SMALL_FLOOR–EQUITY_FLOOR        — limited diversification
      NORMAL : ≥ EQUITY_FLOOR (₹1L, == EQUITY profile) — full allocation

    Thresholds come from app/meta/capital_profile.py so the tier never drifts
    from the profile boundary. NORMAL ≡ EQUITY profile by construction, so the
    ₹1L regression path is unaffected (still NORMAL, prompt byte-identical).
    """
    if capital is None:
        return "NORMAL"
    if capital < SMALL_FLOOR:
        return "MICRO"
    if capital < EQUITY_FLOOR:
        return "SMALL"
    return "NORMAL"


def build_regime_snapshot(
    daily_symbol_states: dict,
    current_date: datetime,
    capital: float | None = None,
) -> dict:
    """
    Compute regime statistics across the active universe for a single trading day.

    Parameters
    ----------
    daily_symbol_states : dict
        {symbol: MarketState} — already populated by BacktestEngine for the day.
    current_date : datetime
        The trading date being processed.

    Returns
    -------
    dict with keys:
        date            — ISO date string
        universe_size   — number of symbols with valid state today
        pct_uptrend     — fraction of symbols in any UPTREND regime
        pct_downtrend   — fraction of symbols in any DOWNTREND regime
        pct_sideways    — fraction of symbols in any SIDEWAYS regime
        pct_high_vol    — fraction of symbols in a HIGH_VOL regime
        avg_atr_pct     — mean ATR as % of price across the universe
        market_breadth  — same as pct_uptrend (alias used in the LLM prompt)
    """
    states  = list(daily_symbol_states.values())
    regimes = [str(s.indicators.get("regime", "")) for s in states]
    n       = max(len(regimes), 1)

    atr_pcts = [
        s.indicators["atr_14"] / s.latest_price
        for s in states
        if s.indicators.get("atr_14") and s.latest_price
    ]
    avg_atr_pct = sum(atr_pcts) / len(atr_pcts) if atr_pcts else 0.0

    pct_uptrend   = sum(1 for r in regimes if "UPTREND"   in r) / n
    pct_downtrend = sum(1 for r in regimes if "DOWNTREND" in r) / n
    pct_sideways  = sum(1 for r in regimes if "SIDEWAYS"  in r) / n
    pct_high_vol  = sum(1 for r in regimes if "HIGH_VOL"  in r) / n

    return {
        "date":           current_date.strftime("%Y-%m-%d"),
        "universe_size":  n,
        "pct_uptrend":    round(pct_uptrend,   3),
        "pct_downtrend":  round(pct_downtrend, 3),
        "pct_sideways":   round(pct_sideways,  3),
        "pct_high_vol":   round(pct_high_vol,  3),
        "avg_atr_pct":    round(avg_atr_pct,   4),
        "market_breadth": round(pct_uptrend,   3),  # alias for LLM prompt clarity
        "capital":        capital,
        "capital_tier":   _capital_tier(capital),
    }
