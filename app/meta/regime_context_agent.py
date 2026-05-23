# app/meta/regime_context_agent.py
#
# RegimeContextAgent — enhanced regime snapshot using broad-universe breadth signals.
#
# Augments build_regime_snapshot() (active 24-80 symbols) with signals computed
# from DynamicUniverseAgent's full 150-symbol cache, giving a market-wide view.
#
# New signals:
#   pct_above_sma50_broad   — % of 150-symbol universe where close > SMA_50 today
#   advance_decline_ratio   — % of broad universe with positive daily return
#   avg_rolling_vol_5d      — mean 5-day realised vol across broad universe
#   trend                   — IMPROVING / DETERIORATING / STABLE (5-day direction)
#   broad_regime            — synthesised regime label (TRANSITION_UP etc.)
#
# Drop-in replacement for build_regime_snapshot() — same output dict, extra keys added.

import pandas as pd
from datetime import datetime

from app.meta.regime_snapshot import build_regime_snapshot
from app.meta.adaptive_selector import _classify_regime as _shared_classify


class RegimeContextAgent:

    def __init__(self, dynamic_agent):
        self.dynamic_agent = dynamic_agent
        self._history: list = []   # [(date, snapshot_dict), ...] — last 20 days

    # ------------------------------------------------------------------
    # PUBLIC API
    # ------------------------------------------------------------------
    def build_snapshot(
        self,
        daily_symbol_states: dict,
        current_date: datetime,
        capital: float | None = None,
    ) -> dict:
        """
        Build enriched regime snapshot for current_date.
        Drop-in replacement for build_regime_snapshot().
        """
        base  = build_regime_snapshot(daily_symbol_states, current_date, capital)
        broad = self._compute_broad_breadth(current_date)
        trend = self._detect_trend()
        # Use the shared classifier so broad_regime and selector._confirmed_regime
        # always use the same label set.
        merged = {**base, **broad, "trend": trend}
        broad_regime, _, _ = _shared_classify(merged)

        snapshot = {**base, **broad, "trend": trend, "broad_regime": broad_regime}

        self._history.append((current_date, snapshot))
        if len(self._history) > 20:
            self._history.pop(0)

        return snapshot

    # ------------------------------------------------------------------
    def _compute_broad_breadth(self, current_date: datetime) -> dict:
        """
        Compute breadth signals across all symbols in DynamicUniverseAgent cache.
        Uses asof lookup — handles UTC-stored timestamps correctly.
        """
        above_sma50 = []
        advances    = []
        vols        = []

        for df in self.dynamic_agent._cache.values():
            loc_key = df.index.asof(current_date)
            if pd.isnull(loc_key):
                continue
            row = df.loc[loc_key]

            close = row.get("close")
            sma50 = row.get("sma_50")
            ret   = row.get("daily_return")
            vol   = row.get("rolling_vol_5d")

            if close is not None and sma50 is not None and not pd.isna(sma50):
                above_sma50.append(1 if float(close) > float(sma50) else 0)
            if ret is not None and not pd.isna(ret):
                advances.append(1 if float(ret) > 0 else 0)
            if vol is not None and not pd.isna(vol):
                vols.append(float(vol))

        n_b = max(len(above_sma50), 1)
        n_a = max(len(advances), 1)
        return {
            "pct_above_sma50_broad": round(sum(above_sma50) / n_b, 3),
            "advance_decline_ratio": round(sum(advances)    / n_a, 3),
            "broad_universe_size":   len(above_sma50),
            "avg_rolling_vol_5d":    round(sum(vols) / max(len(vols), 1), 6),
        }

    # ------------------------------------------------------------------
    def _detect_trend(self) -> str:
        """
        5-day direction of pct_above_sma50_broad and pct_downtrend.
        IMPROVING  — breadth rising ≥5 pp AND downtrend falling ≥4 pp
        DETERIORATING — breadth falling ≥5 pp AND downtrend rising ≥4 pp
        STABLE     — everything else (or fewer than 5 days of history)
        """
        if len(self._history) < 5:
            return "STABLE"

        recent = self._history[-5:]
        breadth   = [s["pct_above_sma50_broad"] for _, s in recent]
        downtrend = [s["pct_downtrend"]          for _, s in recent]

        bd = breadth[-1]   - breadth[0]
        dd = downtrend[-1] - downtrend[0]

        if bd > 0.05 and dd < -0.04:
            return "IMPROVING"
        if bd < -0.05 and dd > 0.04:
            return "DETERIORATING"
        return "STABLE"

