from dataclasses import dataclass
from typing import Dict


@dataclass
class RegimeThresholds:
    dependency_high: float = 0.8
    dependency_moderate: float = 0.6
    fragile_fraction_trigger: float = 0.3  # NEW


class RegimeFragilityMonitor:

    def __init__(self, thresholds: RegimeThresholds = None):
        self.thresholds = thresholds or RegimeThresholds()

    def analyze(self, regime_metrics: Dict) -> dict:

        if not regime_metrics:
            return self._empty_result()

        fragile_symbols = []
        moderate_symbols = []
        dependency_scores = []

        for symbol, metrics in regime_metrics.items():

            if not isinstance(metrics, dict):
                continue

            score = metrics.get("dependency_score")

            if score is None:
                continue

            try:
                score = float(score)
            except:
                continue

            dependency_scores.append(score)

            if score >= self.thresholds.dependency_high:
                fragile_symbols.append(symbol)

            elif score >= self.thresholds.dependency_moderate:
                moderate_symbols.append(symbol)

        symbol_count = len(dependency_scores)

        if symbol_count == 0:
            return self._empty_result()

        avg_dependency = sum(dependency_scores) / symbol_count

        fragile_fraction = len(fragile_symbols) / symbol_count

        # 🔥 NEW: require breadth of fragility
        regime_fragile = fragile_fraction >= self.thresholds.fragile_fraction_trigger

        return {
            "regime_fragile": regime_fragile,
            "avg_dependency": round(avg_dependency, 3),
            "fragile_symbols": fragile_symbols,
            "moderate_symbols": moderate_symbols,
            "fragile_fraction": round(fragile_fraction, 3),
            "symbol_count_evaluated": symbol_count
        }

    def _empty_result(self):
        return {
            "regime_fragile": False,
            "avg_dependency": 0.0,
            "fragile_symbols": [],
            "moderate_symbols": [],
            "fragile_fraction": 0.0,
            "symbol_count_evaluated": 0
        }