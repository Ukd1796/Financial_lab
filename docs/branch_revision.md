# `feature/experiment_v1` vs `main` — Architecture Revision

Quick map of what this branch changed relative to production (`main`).
**8 commits ahead, 0 behind.** ~3,400 insertions / ~370 deletions across `app/`.

## Committed changes (the substance of the branch)

Commits: `refactor(strategy): unify multi-symbol decide()`, `cleaned up universe agent`,
`regime no-atr fix`, `feat(analytics): post-hoc analytics layer`,
`feat: experiment v1 — Adaptive+RCA baseline, local cache`, + gitignore/fix chores.

### 1. Meta / adaptive layer — the biggest change
- **`adaptive_selector.py` (+484)** — deterministic regime classifier feeding the LLM; per-regime **hard weight bounds** (`_apply_regime_bounds`); 2-week regime **stability gate**; capital tiers; feedback-agent hook. This is the "LLM at the edge, code enforces the bounds" design.
- **`llm_cache.py` (NEW)** — SHA-256(model+prompt) **determinism cache** so backtests are reproducible.
- **`regime_context_agent.py`, `regime_snapshot.py`, `capital_profile.py`** — RCA broad-breadth enrichment (150-symbol) + capital tier (MICRO/SMALL/NORMAL).

### 2. Strategy / router
- **`multi_router.py` (+199)** — ownership model, exclusive-strategy gating, cross-exit infrastructure, diagnostic drop-counters.
- **`dual_ma.py` (+84)** rewrite; **`base.py` / `rule_based.py` removed** — the unified multi-symbol `decide()` interface.

### 3. Universe
- **`filters.py` (+408)** — `UnionUniverseFilter` + per-strategy filters (Breakout / ActivityTail / Pullback / MeanReversion / DualMA).
- **`dynamic_agent.py` (+117)** — activity scoring, price feed, preload.
- **`agent.py` (−56)** — dead code removed.

### 4. Risk / execution / backtest
- **`risk/agent.py` (+55)** — ATR **trailing stop** (high-watermark, entry-ATR lock, regime-multiplier hook), vol-based sizing.
- **`strategy_pnl_tracker.py` (NEW +152)** — per-strategy rolling realised-P&L attribution (feeds the feedback agent).
- **`backtest/engine.py` (+197)** — regime-snapshot wiring, capital tier, breadth-CB relaxation.
- **`execution/agent.py` (+31)** — cost-adjusted fills tweaks.

### 5. Analytics — entirely new package (`app/analytics/`)
- `trade_annotator.py`, `opportunity_quality.py`, `universe_tracker.py`, `ensemble_diagnostics.py`, `cqe.py` — post-hoc trade enrichment (MFE/MAE/efficiency, post-exit drift), per-regime breakdowns, universe stability/turnover, ensemble participation + HHI concentration.

### 6. Data / infra
- **`data/local_cache.py` (NEW +249)** — local SQLite OHLC cache (the backtest fast-path; `main` pulls Supabase every run).
- **Runners** — `run_experiments.py` (+728) and `run_ujjwal_baseline.py` (+303): RCA legs, `ADAPTIVE_ONLY`/`EQW_ONLY` modes, analytics integration.
- **Scripts** — `cache_market_data_locally.py`, `diagnose_regime_labels.py`.

## Uncommitted changes (working tree)

**Pre-existing (before this session):**
- `app/risk/agent.py` — removed the `allow_min_one_share` low-capital 1-share floor (param + logic).
- `app/backtest/engine.py` — comment-only tweak (capital_tier wording; no logic change).

**From this session:**
- `app/meta/adaptive_selector.py` — **Gemini provider switch** (`LLM_PROVIDER=gemini` → OpenAI-compat endpoint), `seed` guard, rate-limit retry.
- `run_ujjwal_baseline.py`, `run_experiments.py` — model switched **gpt-4o → gpt-4o-mini** (7 spots).
- NEW untracked: `scripts/analyze_portfolios.py` (live diagnosis), `scripts/run_paper_window.py` (paper-window backtest runner), `docs/portfolio_analysis_system_diagnosis.md`, `docs/series/` (the "Designing an Adaptive System" article set + diagram).

## One-line summary

`main` = simpler production system (basic adaptive selector, no cache, no analytics, Supabase-only data). This branch layers on **RCA + deterministic regime bounds + reproducibility cache + a full analytics/attribution stack + local data cache**, plus a strategy-interface refactor and richer router/universe logic.
