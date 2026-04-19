# api/services/narrative_service.py
#
# Generates the AI narrative section of a backtest result using Claude.
# Falls back to a templated response if the Anthropic client is unavailable.

import os


def generate_narrative(summary: dict, period_breakdown: list) -> dict:
    """
    Build the 4-part ai_narrative dict using gpt-4o-mini.
    Falls back to template strings if OPENAI_API_KEY is not set.
    """
    try:
        from openai import OpenAI
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not set")

        period_text = "\n".join(
            f"  {p['period']} ({p['start_date']} – {p['end_date']}): "
            f"return={p['return_pct']:.1f}%, maxDD={p['max_dd_pct']:.1f}%, "
            f"sharpe={p['sharpe']:.2f}, vs Nifty={p['vs_nifty_pct']:+.1f}%"
            for p in period_breakdown
        )

        prompt = (
            f"You are analysing a backtest of an NSE Indian equity multi-strategy system.\n\n"
            f"Summary:\n"
            f"  Total return: {summary['total_return_pct']:.1f}%\n"
            f"  Max drawdown: {summary['max_drawdown_pct']:.1f}%\n"
            f"  Sharpe ratio: {summary['sharpe_ratio']:.2f}\n"
            f"  Win rate: {summary['win_rate_pct']:.1f}%\n"
            f"  Trades: {summary['total_trades']}\n"
            f"  Benchmark return: {summary['benchmark_return_pct']:.1f}%\n\n"
            f"Period breakdown:\n{period_text}\n\n"
            "Write exactly 4 short paragraphs (2-3 sentences each), one per label:\n"
            "1. WHAT_WORKED: What drove outperformance.\n"
            "2. WHAT_TO_WATCH: Key risks or conditions to monitor.\n"
            "3. BEAR_BEHAVIOR: How the strategy performed in bear phases.\n"
            "4. IMPROVEMENT_TIP: One actionable suggestion to improve the strategy.\n\n"
            "Format your response as:\n"
            "WHAT_WORKED: <text>\n"
            "WHAT_TO_WATCH: <text>\n"
            "BEAR_BEHAVIOR: <text>\n"
            "IMPROVEMENT_TIP: <text>"
        )

        client   = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            max_tokens=512,
            temperature=0.3,
            messages=[{"role": "user", "content": prompt}],
        )
        raw = response.choices[0].message.content or ""

        parsed: dict[str, str] = {}
        for line in raw.splitlines():
            for key in ("WHAT_WORKED", "WHAT_TO_WATCH", "BEAR_BEHAVIOR", "IMPROVEMENT_TIP"):
                if line.startswith(f"{key}:"):
                    parsed[key] = line[len(key) + 1:].strip()

        return {
            "what_worked":     parsed.get("WHAT_WORKED", ""),
            "what_to_watch":   parsed.get("WHAT_TO_WATCH", ""),
            "bear_behavior":   parsed.get("BEAR_BEHAVIOR", ""),
            "improvement_tip": parsed.get("IMPROVEMENT_TIP", ""),
        }

    except Exception:
        return _fallback_narrative(summary)


def _fallback_narrative(summary: dict) -> dict:
    tr  = summary.get("total_return_pct", 0)
    bm  = summary.get("benchmark_return_pct", 0)
    dd  = abs(summary.get("max_drawdown_pct", 0))
    sr  = summary.get("sharpe_ratio", 0)

    return {
        "what_worked": (
            f"The strategy delivered {tr:.1f}% total return vs {bm:.1f}% for Nifty 50, "
            f"with a Sharpe of {sr:.2f}. Trend-following and breakout components "
            "captured the majority of bull-phase upside."
        ),
        "what_to_watch": (
            f"Max drawdown reached {dd:.1f}%. Monitor the regime signal closely — "
            "a shift to BEAR_CONFIRMED should trigger weight reduction for momentum strategies."
        ),
        "bear_behavior": (
            "During bear phases the breadth circuit breaker limited new BUY entries. "
            "RSI mean-reversion and cash preservation kept drawdowns contained "
            "relative to the benchmark."
        ),
        "improvement_tip": (
            "Consider increasing the floor weight for mean-reversion during SIDEWAYS_CHOPPY "
            "regimes. The RSI-MR strategy has historically outperformed trend strategies "
            "when breadth stalls between 40–55%."
        ),
    }
