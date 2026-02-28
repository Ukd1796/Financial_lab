from app.meta.strategy_mode import StrategyMode


class MetaReflectionAgent:

    def __init__(
        self,
        performance_monitor,
        regime_monitor,
        llm_recommender=None
    ):
        self.performance_monitor = performance_monitor
        self.regime_monitor = regime_monitor
        self.llm_recommender = llm_recommender

    # ==================================================
    # MAIN EVALUATION
    # ==================================================
    def evaluate(self, rolling_equity: list, regime_metrics: dict = None):

        # ------------------------------------------
        # 1️⃣ Analyze Performance
        # ------------------------------------------
        performance_summary = self.performance_monitor.analyze(
            rolling_equity
        )

        # ------------------------------------------
        # 2️⃣ Analyze Regime Fragility
        # ------------------------------------------
        regime_metrics = regime_metrics or {}
        regime_summary = self.regime_monitor.analyze(regime_metrics)

        # ------------------------------------------
        # 3️⃣ Deterministic Baseline
        # ------------------------------------------
        deterministic_decision = self._deterministic_decision(
            performance_summary,
            regime_summary
        )

        # ------------------------------------------
        # 4️⃣ LLM Override (If Available)
        # ------------------------------------------
        if self.llm_recommender:

            llm_decision = self.llm_recommender.recommend(
                performance_summary,
                regime_summary
            )

            # If LLM fails validation, fallback safely
            if llm_decision:
                return llm_decision

        return deterministic_decision

    # ==================================================
    # DETERMINISTIC MODE LOGIC
    # ==================================================
    def _deterministic_decision(self, performance, regime):

        perf_state = performance.get("performance_state", "NEUTRAL")
        fragile = regime.get("regime_fragile", False)

        # ---- BROKEN → Defensive
        if perf_state == "BROKEN":
            return {
                "mode": StrategyMode.DEFENSIVE,
                "allocation_multiplier": 0.8,
                "reasoning": "Performance broken",
                "confidence": 1.0
            }

        # ---- Weak OR Fragile → Defensive
        if perf_state == "WEAK" or fragile:
            return {
                "mode": StrategyMode.DEFENSIVE,
                "allocation_multiplier": 0.9,
                "reasoning": "Weak performance or regime fragile",
                "confidence": 0.9
            }

        # ---- Strong AND Stable → Aggressive
        if perf_state == "STRONG" and not fragile:
            return {
                "mode": StrategyMode.AGGRESSIVE,
                "allocation_multiplier": 1.1,
                "reasoning": "Strong performance and stable regime",
                "confidence": 0.95
            }

        # ---- Default
        return {
            "mode": StrategyMode.BALANCED,
            "allocation_multiplier": 1.0,
            "reasoning": "Neutral state",
            "confidence": 0.8
        }