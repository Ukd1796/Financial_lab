# Next Explorations — Synthesis After Sleeve + PAA Investigations

**Status:** Strategic assessment. No code changes proposed here — this is a
roadmap of what to look at next, what to skip, and where to spend engineering
effort given current results.
**Date:** 2026-05-22
**Companion docs:**
- `meta_layer_value_leak.md` (sleeve work — considered & rejected)
- `underperforming_periods_rca.md` (Bull 2019-20 / Live 2025-26 RCA)
- `adaptive_system_flow.md` (system explainer)
- `low_capital_adaptation.md` (ETF profile + Zerodha cost model)

## 1. The recurring theme across all failed attempts

Two major rounds of investigation tried to fix the same fundamental problem
("the combined system underperforms individually-positive solo strategies in
narrow markets like Bull 2019-20 and Live 2025-26"). Both hit the same wall
in different ways:

| Attempt | What was tried | Why it failed |
|---|---|---|
| **Sleeves** | Bypass merge mechanism entirely; run isolated portfolios | Killed concentration alpha in 5 winning periods; net −19pp on Full 2018-24 |
| **PAA — LLM prompt feedback** | Give the LLM recent strategy P&L (5d/10d/30d) in prompt | LLM concentrated worse than baseline; the prompt block itself was noise |
| **PAA — Deterministic cap** | Hard-cap any 30d-bleeder at 0.10 post-LLM | Threshold rarely fires (slow grinds < −3%/30d); when it does fire, caps the wrong strategy in directional regimes (Breakout in Bull) |

### The shared root cause every attempt kept hitting

**The regime MUST rules + the hardcoded cheat sheet are too rigid and frozen
in time.** The cheat sheet was measured from 2018-2024 backtests. CRASH_HIGHVOL
says Breakout has Sharpe 1.72 historically → the MUST rule forces Breakout
≥ 0.30 in CRASH regimes → in Live 2025-26 where Breakout is the worst solo
strategy (−10.61%), the system is still forced to load it heavily by advice
from data that no longer applies.

Every "fix" attempted (sleeves, PAA, deterministic cap) was downstream of
this rule. Sleeves bypassed the merge entirely. PAA tried to override the
allocation via LLM judgment or hard caps. None touched the rule itself.

## 2. Why solo strategies are positive but combined is negative — the mechanical answer

The merge mechanism in `MultiStrategyRouter` + `RiskAgent` introduces three
specific value leaks that DROP signals the solo strategies would have taken:

| Leak | Where | Effect |
|---|---|---|
| **SELL > BUY priority** | `app/strategy/multi_router.py:223-235` | When Strategy A wants to hold TCS and Strategy B wants to sell it, SELL wins. A's profitable hold is liquidated by B's exit signal. |
| **Position ownership rule** | `app/strategy/multi_router.py:141-144` | Only the OPENING strategy can SELL. If Breakout opens TCS and TrendPB's logic says "TCS overextended, exit", TrendPB can't sell it. |
| **Sequential cash gate** | `app/backtest/engine.py:196-217` | Decisions sorted by `strategy_weight` descending. Highest-weight strategies claim cash first. Lower-weight strategies get HOLD rejections when cash depletes. |

Solo Breakout in Bull 2019-20 takes 387 trades. Combined Breakout at weight
0.30 takes substantially fewer trades because of router/cash conflicts.
**Combined Breakout doesn't capture Breakout's full edge — it captures a
filtered subset, plus interference patterns.**

This is unavoidable if you want strategy combination. But how much value is
LOST to interference vs the merge's positive contribution (concentration alpha
in directional regimes) is **currently invisible** — we have zero
instrumentation on which signals get dropped and why. The first concrete next
step (see §5) is adding that visibility.

## 3. Is Live 2025-26 worth fixing before deploying real capital?

**Honest answer: probably not in the equity system. Deploy the ETF book
instead.**

Reasons:

| Consideration | What it suggests |
|---|---|
| ETF profile already shows **+11.1% net of Zerodha costs** (`low_capital_adaptation.md` §9) | A real shippable result, validated end-to-end |
| Live equity Adp+RCA is **~−2.5%** legacy, **~−3%** with deterministic PAA | Both barely above breakeven in a narrow market — this isn't "broken", just "narrow-market drag" |
| Walk-forward retention **0.98×** (post-fix) | The system is structurally sound, not overfit |
| Solo strategies in Live: 5 of 6 positive (Breakout the outlier at −10.61%) | Issue is concentrated in one strategy in one regime — not systemic |
| Bull 2019-20 and Live 2025-26 are **archetype-hostile markets** per `underperforming_periods_rca.md` §6 | Narrow/choppy markets where momentum/breakout/MR have no consistent edge. No router/weight tweak recovers what archetype can't capture |

**The most operationally honest move:** deploy the ETF profile to live paper
trading with real-time data, see how it actually behaves, and let real data
inform whether the equity-system issues matter for your deployment goal.

The equity system's underperformance in two narrow historical periods is a
research data point, not a deployment blocker if you're targeting the
low-capital ETF path.

## 4. Three explorations worth time (if equity system stays in scope)

Ranked by leverage / effort ratio.

### Exploration A — Conditional MUST floors (small surgical change)

The smallest possible change with potentially meaningful upside. Modify
`_apply_regime_bounds()` to make floors *conditional* on recent performance:

> "Breakout MUST ≥ 0.30 UNLESS its rolling 90-day Sharpe is < 0"

This is essentially what PAA tried to do, but with a longer window (90d, not
30d) that actually captures slow grinds — the failure shape PAA missed.

- **Where:** `app/meta/adaptive_selector.py:_apply_regime_bounds()`
- **Engineering:** ~half day
- **Risk:** low — surgical, only modifies the MUST clamp behavior
- **Why it might work:** directly addresses the root cause (rigid floors) while
  staying within the existing architecture

### Exploration B — Top-of-funnel exposure gate (revisit cleanly)

The breadth-collapse gate from `underperforming_periods_rca.md` §7 — when
broad market breadth is genuinely deteriorating (`pct_above_sma200 < 50%
AND trending down`), scale all strategy weights by 0.5 (deploy half capital,
half cash).

We rejected this earlier on weak analysis (only checked detector trigger
rates, never actually A/B'd it). Worth revisiting properly: implement,
flag-gate, full 2-period A/B.

- **Where:** new wrapper in `app/meta/adaptive_selector.py` or new agent
- **Engineering:** ~1 day
- **Risk:** low — flag-gated default-off, doesn't touch existing rules
- **Why it might work:** sidesteps the "which strategy" problem; just deploys
  less capital when macro is hostile

### Exploration C — Rolling / regenerated cheat sheet (highest leverage, most engineering)

Recompute the Sharpe table quarterly on the last 12-24 months of data,
replacing the hardcoded values. If market microstructure shifts (which it
has — momentum quality in Indian equities 2025 is different from
2018-2024), the table self-updates and the MUST rules derived from it
naturally adapt.

- **Where:** `_STRATEGY_REGIME_PERFORMANCE` becomes a generated string,
  not a hardcoded one. Plus a refresh job or load-from-DB pattern.
- **Engineering:** ~1 week, plus a periodic refresh job
- **Risk:** medium — could introduce noise if window too short; needs careful
  validation
- **Why it might work:** addresses the root cause directly. The current table
  is frozen 2018-2024; the world has moved on.

## 5. The single highest-ROI diagnostic — measure the signal-drop leak

Before any of A/B/C, **we have zero visibility into how often each strategy's
signals get dropped by the merge mechanism**, or why. A half-day
instrumentation add gives massive insight:

In `app/strategy/multi_router.py:_merge_into()` + `app/backtest/engine.py:196-217`,
add per-strategy counters for:

- **`signals_issued`** — total decisions the strategy issued per period
- **`won_merge`** — decisions that made it through the router
- **`dropped_priority`** — decisions overridden by a higher-priority or
  higher-weighted strategy on the same symbol
- **`dropped_ownership`** — SELL decisions skipped because the strategy
  didn't own that position
- **`buy_rejected`** — BUYs that came out of the router but didn't execute
  (cash starvation / breadth CB / ATR-to-cost)

Print per-strategy at end of each period. Reveals:
- Which strategies are most "drowned out" by the merge
- Whether cash starvation or priority loss dominates
- Whether ownership block is meaningful or rare

This is being added in the same session as this doc — see commit log.

## 6. What to skip

| Skip | Why |
|---|---|
| More PAA variants (different prompts, thresholds, windows) | Both LLM-only and deterministic falsified the "feed recent P&L → better weights" hypothesis. Diminishing returns. |
| Sleeve revisits | Conclusively rejected by 7-period data (`meta_layer_value_leak.md`). |
| Upgrading the LLM model (gpt-4o, Claude Opus) | gpt-4o-mini handled the cheat-sheet+rules prompt fine (WF 0.98× retention). The issue isn't model capability — it's that the cheat sheet is stale and the LLM is following it correctly. |
| Adding more LLM-driven feedback agents (trade quality, regime accuracy, etc.) | Same "more prompt = more noise" failure mode as PAA. |

## 7. The meta-observation worth holding onto

The 5-strategy + adaptive selector + RCA combination is **a sound system
that captures genuine alpha in directional regimes**:
- Full 2018-24: +116% IS / ~+99% estimated OOS
- Walk-forward 0.98× OOS retention (post-fix) — not overfit
- 5 of 7 historical periods are clear wins

It **structurally struggles in narrow markets** (Bull 2019-20, Live 2025-26)
for **archetype reasons that no router/weight/feedback tweak has fixed**
across two major investigations.

Three honest paths from here:

| Path | Description |
|---|---|
| **A. Accept the weakness** | Deploy with awareness. Reduce exposure or pause in narrow-market conditions (manual or via Exploration B). |
| **B. Add a non-directional strategy** | Sector rotation, vol-targeting, market-neutral pairs. Covers the narrow-market gap that momentum/breakout/MR can't. Substantial research project. |
| **C. Focus on regimes where the system works** | ETF book at low capital (already validated +11% net). Deploy that, accept equity system as a research project for later. |

**Path C is the cheapest path to actually trading real money.** A and B are
worthwhile research projects but not blockers for deployment.

## 8. The artifacts worth keeping from the PAA round

Even though PAA didn't ship, the work produced:

- ✅ **The capital-tier backtest-correctness fix** (`engine.py` — pins capital
  to initial value, not live equity). Latent bug that would have hit any
  drawdown backtest. Production (`api/run_paper_signals.py`) was never
  affected because it never wired `capital` into the snapshot, but worth
  knowing about.
- ✅ **Clean reusable FeedbackAgent architecture** — `PerformanceFeedbackAgent`
  and `DeterministicPerformanceFeedbackAgent` in
  `app/meta/performance_feedback_agent.py`. Removable any time via the agent
  constructor arg.
- ✅ **Per-strategy P&L attribution tracker** —
  `app/risk/strategy_pnl_tracker.py`. Useful infrastructure even if PAA
  itself doesn't ship — same machinery could feed other diagnostics.
- ✅ **Walk-forward retention measurement** — 0.98× post-fix confirms the
  system is NOT meaningfully overfit. Major confidence input for live deploy.

## 9. Bottom line

If picking up this thread later:
1. **Don't iterate on PAA further** — falsified across 4 variants.
2. **Look at Exploration A or B first** if you stay in the equity system.
3. **Ship the ETF book** if your goal is "trade real money soon".
4. **Run the diagnostic instrumentation** (§5) before any further architecture
   work — gives data we currently lack about where the merge actually leaks.
