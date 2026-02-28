# app/meta — Meta-Layer Strategy Controller

The `meta` module is a portfolio-level intelligence layer that sits **above** the core trading pipeline. Its job is to periodically assess portfolio health and market conditions, then switch the system into one of three operating modes: `AGGRESSIVE`, `BALANCED`, or `DEFENSIVE`. Everything downstream—position sizing, regime filters, risk limits—responds to this mode.

---

## Architecture Overview

```
BacktestEngine (every N days)
        │
        ▼
MetaReflectionAgent          ← orchestrator
   ├── PerformanceMonitor     ← how is the portfolio doing?
   ├── RegimeFragilityMonitor ← how fragile is the market?
   └── LLMConfigurationRecommender (optional)
        │
        ▼
   StrategyMode  →  CrossSectionalMomentumStrategy
                →  RiskAgent
```

The backtest engine calls `meta_agent.evaluate()` every **30 trading days** using the last **60 days** of equity history. The resulting `StrategyMode` is picked up by the strategy and risk agent to adjust behavior for the next period.

---

## File-by-File Breakdown

### `strategy_mode.py` — Core Types

Defines the two core data structures shared across the whole system.

| Symbol | Purpose |
|---|---|
| `StrategyMode` | Enum: `AGGRESSIVE`, `BALANCED`, `DEFENSIVE` |
| `ModePolicy` | Dataclass holding `max_position_pct`, `atr_multiplier`, `allowed_regimes` per mode |

`StrategyMode` is imported by the strategy, risk agent, and meta layer. `ModePolicy` is currently defined but not instantiated anywhere.

---

### `models.py` — MetaDecision Dataclass

```python
@dataclass
class MetaDecision:
    action: str                  # "INCREASE", "REDUCE", "MAINTAIN"
    allocation_multiplier: float
    reasoning: str
    diagnostics: Optional[Dict]
```

Intended to be the canonical return type of the meta layer. Currently not used—`MetaReflectionAgent.evaluate()` returns plain `dict` instead.

---

### `performance_monitor.py` — Portfolio Health

Consumes a `rolling_equity` list and produces a structured performance summary.

**Metrics computed:**
- **Sharpe Ratio** — calculated on rolling-smoothed returns (window=10), annualized, clamped to [-3, 3]
- **Max Drawdown** — peak-to-trough decline over the full equity curve
- **Volatility** — annualized standard deviation of daily returns
- **Trend Slopes** — linear slope of equity over 10, 30, and 60 day windows

**State classification (`performance_state`):**

| State | Condition |
|---|---|
| `INSUFFICIENT` | Fewer than 60 observations |
| `BROKEN` | Drawdown ≤ -30% **or** Sharpe < -0.2 |
| `WEAK` | Sharpe < 0.5 |
| `MODERATE` | 0.5 ≤ Sharpe < 1.0 |
| `STRONG` | Sharpe ≥ 1.0 |

---

### `regime_monitor.py` — Market Fragility

Consumes a `regime_metrics` dict (keyed by symbol, each with a `dependency_score` float) and detects whether the broader market is in a fragile state.

**Thresholds:**

| Threshold | Default | Meaning |
|---|---|---|
| `dependency_high` | 0.8 | Symbol is "fragile" |
| `dependency_moderate` | 0.6 | Symbol is "moderate risk" |
| `fragile_fraction_trigger` | 0.3 | If ≥30% of symbols are fragile → regime is fragile |

**Output fields:** `regime_fragile`, `avg_dependency`, `fragile_symbols`, `moderate_symbols`, `fragile_fraction`, `symbol_count_evaluated`.

> `dependency_score` is produced by `RegimeAnalysisAgent` in `app/analysis/regime_agent.py` and passed in by the backtest engine.

---

### `meta_reflection.py` — Orchestrator

The main agent. Combines performance and regime signals to decide strategy mode.

**Decision flow:**

```
1. PerformanceMonitor.analyze(rolling_equity)   → performance_summary
2. RegimeFragilityMonitor.analyze(regime_metrics) → regime_summary
3. _deterministic_decision(...)                 → rule-based baseline
4. LLMConfigurationRecommender.recommend(...)   → LLM override (if enabled)
```

**Deterministic rules (`_deterministic_decision`):**

| Condition | Mode | Multiplier |
|---|---|---|
| `BROKEN` | DEFENSIVE | 0.8× |
| `WEAK` or regime fragile | DEFENSIVE | 0.9× |
| `STRONG` and regime stable | AGGRESSIVE | 1.1× |
| Everything else (`MODERATE`, `INSUFFICIENT`) | BALANCED | 1.0× |

If `llm_recommender` is provided and returns a decision, it **replaces** the deterministic decision entirely.

---

### `llm_recommender.py` — LLM Strategy Selector

Calls OpenAI (default: `gpt-4o-mini`) with the performance and regime summaries. Returns a JSON decision with `mode`, `reasoning`, and `confidence`.

**Guardrails applied after LLM response:**
- `mode` must be one of the three valid values, else defaults to `BALANCED`
- `confidence` is clamped to [0.0, 1.0]
- **Stability bias:** if `confidence < 0.6` → mode is overridden to `BALANCED`

**Fallback:** On any API error, returns `StrategyMode.BALANCED` with `confidence=0.0`.

---

## Data Flow Summary

```
rolling_equity (list[float])  ──► PerformanceMonitor
                                        │
regime_metrics (dict[str, dict])  ──► RegimeFragilityMonitor
                                        │
                                  MetaReflectionAgent
                                        │
                              deterministic_decision
                                        │
                         (optional) LLM override
                                        │
                              { mode: StrategyMode,
                                allocation_multiplier: float,
                                reasoning: str,
                                confidence: float }
                                        │
                     CrossSectionalMomentumStrategy + RiskAgent
```

---

## Suggested Improvements

### 1. `MetaDecision` model is unused — return type is inconsistent
`models.py` defines `MetaDecision` but `meta_reflection.py` returns a plain `dict`. The LLM path also omits `allocation_multiplier`. Fix: make `evaluate()` always return a `MetaDecision` (or a typed `TypedDict`) and populate all fields on both paths.

### 2. LLM fallback always fires — deterministic baseline is effectively dead when LLM is enabled
`_fallback_decision` returns a valid dict (with `confidence=0.0`), so the `if llm_decision:` check in `evaluate()` is always truthy. The deterministic rule-based logic is completely bypassed whenever `llm_recommender` is set. Consider checking confidence or using the deterministic result as a sanity check rather than a pure override.

### 3. `ModePolicy` is dead code
`ModePolicy` in `strategy_mode.py` is never instantiated or used. Either wire it into `RiskAgent` / `CrossSectionalMomentumStrategy` to replace hardcoded per-mode parameters, or remove it.

### 4. No mode persistence / hysteresis
The meta agent re-evaluates from scratch every 30 days. A portfolio recovering from a brief dip could oscillate between DEFENSIVE and BALANCED rapidly. Consider adding a minimum hold period (e.g., hold DEFENSIVE for at least 2 cycles) or requiring a sustained improvement before upgrading the mode.

### 5. Bare `except:` clauses suppress unexpected errors
`regime_monitor.py` and `llm_recommender.py` use bare `except:` blocks that catch everything including `KeyboardInterrupt` and `SystemExit`. Replace with `except (ValueError, TypeError):` or `except Exception:` with explicit logging.

### 6. Missing `allocation_multiplier` in LLM decision path
The deterministic path sets `allocation_multiplier` (0.8–1.1) but the LLM path does not. Any downstream code reading `allocation_multiplier` from the result will raise a `KeyError` when LLM is enabled.

### 7. Sharpe uses smoothed returns — can inflate the ratio
The rolling mean smoothing before computing Sharpe reduces apparent volatility. This is not a standard annualized Sharpe and produces higher values than a naive calculation would. Worth documenting the intentional deviation, or computing both for comparison.

### 8. OpenAI key failure is silent at init time
If `OPENAI_API_KEY` is not set, `LLMConfigurationRecommender.__init__` succeeds silently and only fails at the first `recommend()` call, which is then caught and swallowed by the fallback. Consider asserting the key exists at construction time to fail fast with a clear error message.
