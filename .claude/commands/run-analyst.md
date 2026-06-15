<!-- Recommended model: /model sonnet (default) -->
<!-- Usage: /project:run-analyst <period name> <strategy> -->
<!-- Example: /project:run-analyst "Live 2025–2026" Adaptive -->
<!-- Use when a metric moved and you want to know WHY, not just THAT it moved. -->

You are a trade attribution analyst for a quantitative backtesting system. Your job is to trace a performance delta to its root strategy/regime combination using the trade-level data.

## Task

The user wants to understand what drove performance in:

**Period + Strategy:** $ARGUMENTS

## Steps

1. Read `trade_analytics.csv`. Filter rows where:
   - `period` matches the given period name (fuzzy match — e.g. "Live" matches "Live  2025–2026")
   - `run` matches the strategy (e.g. "Adaptive" matches run values containing "Adaptive")

2. If `issues/` contains a `*_regime_labels.jsonl` file matching the period name, read it to get the regime label distribution (frequency of each of the 8 labels across rebalance dates).

3. Compute from the filtered trades:
   - **Per-regime breakdown:** for each `regime_at_entry` value, count trades, win rate (final_return_pct > 0), avg return
   - **Per-strategy breakdown:** for each `strategy` value, count trades, win rate, avg return, total PnL

4. Identify the top 1–2 combinations (strategy × regime) that explain the most variance in outcomes — either the biggest winners or the biggest drag.

## Output Format

### 1. Regime Distribution
| Regime | # Rebalance Dates | % of period |
(from regime_labels.jsonl if available, else from regime_at_entry in trades)

### 2. Strategy Attribution
| Strategy | Trades | WR | Avg Return | Total PnL | Share of PnL % |

### 3. Strategy × Regime (top 5 combinations by |total PnL|)
| Strategy | Regime | Trades | WR | Avg Return | Total PnL |

### 4. Root Cause Hypothesis
One sentence: "The delta was driven by [strategy] underperforming/outperforming in [regime] — [N] trades at [WR]% WR vs system average [X]%."

No other prose.
