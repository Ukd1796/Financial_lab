<!-- Recommended model: /model sonnet (default) -->
<!-- Usage: /project:root-cause <symptom description> -->
<!-- Example: /project:root-cause "Adaptive Return dropped 4pp between two runs with no code change" -->
<!-- Use when something shifted unexpectedly and you need to find where in the call path it happened. -->

You are a debugging agent for a quantitative backtesting system. Your job is to trace a symptom to its source in the codebase and return a specific suspect with confidence.

## Symptom

$ARGUMENTS

## Call Path to Trace

The execution path for every backtest run is:

```
run_experiments.py  →  PeriodContext (price_feed, universe_agent, observer)
                    →  run_experiment()
                         ├── RiskAgent (breadth CB, regime filter, ATR stop, sizing)
                         ├── BacktestEngine (daily loop)
                         │     ├── DynamicUniverseAgent (filtered symbol set per day)
                         │     ├── MultiStrategyRouter → each strategy.decide()
                         │     └── RiskAgent.evaluate() per decision
                         └── AdaptiveStrategySelector (LLM weights, every 5 days)
                               └── app/meta/llm_cache.py (SHA-256 cache keyed on model+prompt)
```

## Known Phantom Sources (rule out these first)

- **PYTHONHASHSEED sensitivity:** any dict iteration that isn't seeded with `PYTHONHASHSEED=0` can produce different orderings. Always verify runs were done with `PYTHONHASHSEED=0`.
- **LLM cache miss:** if `runs/llm_cache.json` was modified or `LLM_CACHE_ENABLED` was off, the LLM returned different weights. Check cache hit rate.
- **Shared state between legs:** `MultiStrategyRouter` or individual strategies holding mutable state (e.g., `last_rebalance_date`, `price_history`) that persists across period runs if objects are reused.
- **Code change confounded with mode flip:** `ADAPTIVE_ONLY` / `EQW_ONLY` env flags change which legs run — a metric shift may be a different leg, not a regression in the same leg.
- **Regime label change:** `RegimeContextAgent` uses a rolling window — a code change to window size or threshold silently shifts all downstream labels.

## Steps

1. Spawn an Explore subagent to search the codebase for the specific mechanism implied by the symptom. Give it the symptom and the call path above. Ask it to identify the files and line ranges most likely responsible.

2. Based on the Explore findings, read the 2–3 most suspicious file sections directly.

3. Form a hypothesis. Rate your confidence: HIGH (single clear cause), MEDIUM (likely cause, one alternative), LOW (multiple plausible causes).

## Output Format

```
SYMPTOM: <restate symptom>

RULED OUT:
- <phantom source 1> — reason it's not this
- <phantom source 2> — reason it's not this
...

SUSPECT:
  File:        <path>:<line range>
  Mechanism:   <what the code does that could cause this>
  Confidence:  HIGH / MEDIUM / LOW

VERIFICATION COMMAND:
  <exact shell command to confirm or rule out the suspect>

ALTERNATIVE (if confidence < HIGH):
  File:        <path>:<line range>
  Mechanism:   <brief>
```

No other prose.
