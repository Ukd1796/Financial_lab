import json
import os
from openai import OpenAI
from app.meta.strategy_mode import StrategyMode


class LLMConfigurationRecommender:

    def __init__(self, model="gpt-4o-mini"):
        self.client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY")
        )
        self.model = model

    # ======================================================
    # MAIN ENTRY
    # ======================================================
    def recommend(self, performance_summary: dict, regime_summary: dict):

        structured_input = {
            "performance_summary": performance_summary,
            "regime_summary": regime_summary,
            "available_modes": [
                "AGGRESSIVE",
                "BALANCED",
                "DEFENSIVE"
            ]
        }

        messages = [
            {
                "role": "system",
                "content": (
                    "You are an institutional portfolio-level strategy controller.\n\n"

                    "Your objective is to maximize long-term risk-adjusted return "
                    "while minimizing unnecessary regime switching.\n\n"

                    "You DO NOT adjust position size directly.\n"
                    "You ONLY select one of three STRATEGY MODES.\n\n"

                    "Strategy Modes:\n"
                    "AGGRESSIVE → Strong, stable environment.\n"
                    "BALANCED → Default state.\n"
                    "DEFENSIVE → Capital preservation during deterioration.\n\n"

                    "Interpret performance using multi-period stability.\n"
                    "Avoid reacting to single noisy data points.\n"
                    "If signals conflict → choose BALANCED.\n"
                    "Prefer persistence over snap reactions.\n\n"

                    "Return STRICT JSON only:\n"
                    "{\n"
                    '  "mode": "AGGRESSIVE | BALANCED | DEFENSIVE",\n'
                    '  "reasoning": string,\n'
                    '  "confidence": float between 0 and 1\n'
                    "}\n"
                )
            },
            {
                "role": "user",
                "content": (
                    "Current strategy state:\n\n"
                    + json.dumps(structured_input, indent=2)
                )
            }
        ]

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0,
                response_format={"type": "json_object"}
            )

            decision = json.loads(response.choices[0].message.content)

            decision = self._validate_and_normalize(decision)

            print(f"[LLM META NORMALIZED] {decision}")

            return decision

        except Exception as e:
            return self._fallback_decision(str(e))

    # ======================================================
    # VALIDATION + GUARDRAILS
    # ======================================================
    def _validate_and_normalize(self, decision: dict):

        mode_str = decision.get("mode", "BALANCED")
        reasoning = decision.get("reasoning", "")
        confidence = decision.get("confidence", 0.5)

        # -------- Mode Validation --------
        if mode_str not in ["AGGRESSIVE", "BALANCED", "DEFENSIVE"]:
            mode_str = "BALANCED"

        # -------- Confidence Validation --------
        try:
            confidence = float(confidence)
        except:
            confidence = 0.5

        confidence = max(0.0, min(1.0, confidence))

        # -------- Stability Bias --------
        if confidence < 0.6:
            mode_str = "BALANCED"

        return {
            "mode": StrategyMode(mode_str),
            "reasoning": reasoning,
            "confidence": round(confidence, 3)
        }

    # ======================================================
    # SAFE FALLBACK
    # ======================================================
    def _fallback_decision(self, error_message):

        print("[LLM META FALLBACK]", error_message)

        return {
            "mode": StrategyMode.BALANCED,
            "reasoning": f"Fallback triggered: {error_message}",
            "confidence": 0.0
        }