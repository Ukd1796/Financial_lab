from app.universe.models import UniverseCandidate


class UniverseSelectionAgent:
    """
    Stateless filter that narrows the broad candidate list produced by
    DynamicUniverseAgent down to the final high-opportunity symbols.

    Receives a List[UniverseCandidate] — already carrying precomputed
    metrics — and applies two hard threshold filters:

    Filter 1 — Volume spike
        relative_volume > volume_threshold  (default 1.5)

    Filter 2 — Price movement
        abs(daily_return) > volatility_threshold  (default 2%)

    Survivors are re-ranked by the same composite score already computed
    by DynamicUniverseAgent and truncated to top_n.

    No DB access, no preloading, no internal cache.
    """

    def __init__(
        self,
        volume_threshold:     float = 1.5,
        volatility_threshold: float = 0.02,
        top_n:                int   = 20,
    ):
        self.volume_threshold     = volume_threshold
        self.volatility_threshold = volatility_threshold
        self.top_n                = top_n

    def select_universe(
        self,
        candidates: list[UniverseCandidate],
    ) -> list[UniverseCandidate]:
        """
        Apply threshold filters to the incoming candidates and return the
        top_n survivors ranked by their existing opportunity score.
        """
        filtered = [
            c for c in candidates
            if c.relative_volume > self.volume_threshold
            and abs(c.daily_return) > self.volatility_threshold
        ]

        filtered.sort(key=lambda c: c.score, reverse=True)
        return filtered[: self.top_n]

    def select_symbols(
        self,
        candidates: list[UniverseCandidate],
    ) -> list[str]:
        """Convenience wrapper — returns symbol strings from select_universe()."""
        return [c.symbol for c in self.select_universe(candidates)]
