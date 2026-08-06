# Tactiq — Interview Deep-Dive & Role Mapping (TradePolaris)

*Prep doc. Everything here is grounded in the actual codebase (`app/`, `api/`). Where the
job description assumes something Tactiq doesn't have, that's flagged honestly with a
bridge answer — do not claim capabilities the code doesn't support; a founding-engineer
interviewer will ask you to walk through the code.*

---

## 0. The 30-second pitch (memorize this)

> "Tactiq is a systematic equity trading system for NSE (Indian) equities. It runs a
> 5-strategy momentum/mean-reversion ensemble over a ~150-symbol universe, with an
> LLM-assisted meta-layer that re-weights strategies by market regime. It has a
> walk-forward backtest harness across six historical regimes, a deterministic risk
> layer, and a live paper-trading loop running on cron against a Postgres market-data
> store. What I'm proudest of isn't the strategies — it's the **research discipline**: a
> reproducible backtest engine and an experiment log where I've falsified most of my own
> ideas with data instead of shipping them."

That last sentence is your single strongest line for *this* role. Lead with it.

---

## 1. Architecture (the whole map)

Tactiq is a **layered pipeline** — each layer has one job and a typed hand-off to the next.
The same `app/` domain code is shared by both the backtest harness and the live cron jobs;
only the data source and execution adapter differ. That "same code in backtest and live"
property is the thing that makes the paper results trustworthy.

```
                         ┌─────────────────────────────────────────┐
Market data (OHLCV) ───► │ 1. DynamicUniverseAgent                 │  150 → top-80
  Supabase Postgres      │    app/universe/dynamic_agent.py        │  cross-sectional
                         │    opportunity_score, look-ahead-safe   │  activity score
                         └───────────────────┬─────────────────────┘
                                             │ UniverseCandidate[]
                         ┌───────────────────▼─────────────────────┐
                         │ 2. UnionUniverseFilter                  │  per-strategy
                         │    app/universe/filters.py (5 filters)  │  second-stage gates
                         └───────────────────┬─────────────────────┘
                         ┌───────────────────▼─────────────────────┐
                         │ 3. MarketObserverAgent                  │  indicators per
                         │    app/backtest/observer.py             │  symbol → MarketState
                         └───────────────────┬─────────────────────┘
                         ┌───────────────────▼─────────────────────┐
                         │ 4. RegimeContextAgent                   │  150-symbol breadth
                         │    app/meta/regime_context_agent.py     │  → regime label
                         └───────────────────┬─────────────────────┘
                         ┌───────────────────▼─────────────────────┐
                         │ 5. AdaptiveStrategySelector (weekly)    │  LLM proposes
                         │    app/meta/adaptive_selector.py        │  weights; code
                         │    GPT-4o-mini, behind a hash cache     │  disposes (bounds)
                         └───────────────────┬─────────────────────┘
                         ┌───────────────────▼─────────────────────┐
                         │ 6. MultiStrategyRouter                  │  5 strategies →
                         │    app/strategy/multi_router.py         │  merge, conflict
                         │    ownership model, weight contest      │  resolve, weight-tag
                         └───────────────────┬─────────────────────┘
                         ┌───────────────────▼─────────────────────┐
                         │ 7. RiskAgent (7-layer kill chain)       │  breadth CB, ATR
                         │    app/risk/agent.py                    │  sizing, trailing
                         │                                         │  stop, cash gate
                         └───────────────────┬─────────────────────┘
                         ┌───────────────────▼─────────────────────┐
                         │ 8. ExecutionAgent / PaperAdapter        │  cost-adjusted fills
                         │    app/execution/agent.py, app/broker/  │  next-day open
                         └─────────────────────────────────────────┘
```

**The one architectural principle to state out loud:** *single-responsibility layers with
typed hand-offs, and a deterministic core with the only LLM call isolated behind a cache.*
That's what lets you A/B any single layer without the others moving.

---

## 2. Data flow (two concerns, two stores)

Be precise here — the two-database split is a real design decision you can defend.

| Store | What lives there | Access |
|---|---|---|
| **Supabase Postgres** | Market OHLCV, signals, paper-trade sessions, positions, push tokens | `app/core/database.py` → SQLAlchemy `SessionLocal`; bulk reads via `MarketDataRepository.get_ohlc_bulk` |
| **SQLite (`api_state.db`)** | Strategy configs, backtest run records, LLM weight decisions | `api/db/store.py` (lightweight KV) |

**Why the split (your answer):** "The Postgres store is the shared source of truth for
market and account state — it's read by the API, the cron jobs, and the frontend via
Supabase's client. The SQLite store is local operational state for the API layer —
config and run history — that doesn't need to be shared or highly available. Splitting
them kept the hot market-data path on a proper connection-pooled Postgres while keeping
config trivially simple. If I were scaling it, the SQLite state would fold into Postgres."

**Live data flow (paper trading), the lifecycle to narrate:**
1. Frontend writes a session row to `paper_trade_sessions` (Supabase JS + user JWT).
2. `api/run_paper_signals.py` (cron, 10:35 UTC): loads active sessions → EOD data →
   `Router → RiskAgent → cash gate` → writes `PENDING` rows to `signal_queue`.
3. `api/run_paper_orders.py` (10:45 UTC): fills yesterday's `PENDING` at next-day open via
   `PaperAdapter` → `FILLED`.
4. `api/run_daily_pnl.py` (10:15 UTC): prices `FILLED` rows, sends push P&L summary.
5. Portfolio state is **reconstructed on-demand from `FILLED` rows** — there is no
   authoritative positions table. (Be ready to defend this — see §7 "challenges".)

**The point-in-time / look-ahead discipline** (this is the term the job cares about):
Every rolling feature in `dynamic_agent.py` uses `.shift(1)` before rolling — today's SMA
is computed from *completed* bars only, never today's close. The backtest engine loops
`for current_date in historical_dates` and uses `df.index.asof(current_date)` so a symbol
only ever sees data up to the decision date. **Say this explicitly**: "I prevent
look-ahead structurally at the feature layer with `shift(1)`, and the backtest replays
day-by-day using `asof` lookups, so the same code path can't see the future in backtest
or live."

---

## 3. Portfolio construction

How capital actually gets allocated, layer by layer:

- **Strategy weights** (`MultiStrategyRouter`): each strategy carries a capital weight
  (equal by default, or LLM-set). A strategy at weight 0.30 sizes positions to 30% of
  full deployment. Weights normalize to 1.0.
- **Conflict resolution + ownership** (`multi_router.py`): when two strategies act on the
  same symbol, the higher-priority/higher-weight decision wins. **Ownership model:** only
  the strategy that *opened* a position may close it (`dropped_ownership` counter tracks
  the SELLs this silently drops — a known bottleneck, §8).
- **Position sizing** (`RiskAgent._size_position`): ATR-based volatility sizing —
  `risk_budget = equity × risk_frac × strategy_weight`, quantity backed out from the
  ATR stop distance, then **capped to available cash** (`portfolio.cash // price` — you
  cannot spend unrealized gains). Falls back to a fixed max-position-% when ATR is absent.
- **Risk gates** (the "7-layer kill chain"): breadth circuit-breaker (suppress BUYs when
  >N% of the universe is in a downtrend), min-ATR-vs-cost gate (skip trades where the
  expected move can't cover round-trip cost), ATR trailing stop from the high-watermark,
  and a sequential cash gate.

**Honest framing for the interview:** Tactiq does **rule-based, volatility-scaled position
sizing with a regime overlay** — it is *not* mean-variance / covariance-based portfolio
optimization. Don't oversell it. See §10 for how to bridge to the factor-risk world the
role lives in.

---

## 4. Backtesting engine (your strongest technical overlap with the role)

`app/backtest/engine.py` — a daily event loop that walks the same pipeline live uses:

- **Walk-forward across six regimes:** Bull 2019–20, Crash 2020, Recovery 2020–21, Bear
  2022, Recent 2022–24, Live 2025–26. Every change is judged on *all six* — a lever that
  helps one regime and hurts another is rejected. This is the "walk-forward testing" and
  "been burned by it" the JD names explicitly.
- **Determinism:** runs under `PYTHONHASHSEED=0`; the LLM meta-layer sits behind a
  SHA-256 prompt-hash disk cache (`app/meta/llm_cache.py`) so non-prompt code changes are
  bit-reproducible run-to-run. **This is a great story** — "I made an LLM-in-the-loop
  system reproducible by hashing the prompt and freezing the response stream, so I could
  A/B deterministic code changes without the model's noise polluting the comparison."
- **EqualWeight vs Adaptive dual-track:** `run_ujjwal_baseline.py --equal-weight-only`
  gives a deterministic, no-LLM baseline; the full run adds the LLM meta-layer. You always
  validate deterministic first, then layer the LLM.
- **Cost-adjusted fills:** `ExecutionAgent` simulates next-day-open fills with commission,
  so backtest P&L reflects real friction.
- **Survivorship bias — know this cold, it's named in the JD.** The universe is a
  **static, present-day** hardcoded list (`run_ujjwal_baseline.py:74-110`): today's Nifty
  50 + Next 50 + Midcap 50, applied backward to 2018. That creates *two* distinct biases,
  and the precise version is the impressive answer:
  - **Survivorship (NOT mitigated — the real hole):** large caps that collapsed and were
    dropped from the index (NSE's Yes Bank / DHFL / Vodafone-Idea equivalents) are simply
    absent. The backtest never holds a former Nifty name that went to near-zero — every
    symbol is one that survived to today, which inflates results.
  - **Look-ahead index-inclusion (partially, *accidentally* mitigated):** the list also
    holds recent winners (ETERNAL/Zomato, ADANIGREEN, DIXON). Running "Bull 2019" on
    today's winners would be look-ahead — but those names have no 2019 price history and
    the preloader skips any symbol with insufficient history
    (`dynamic_agent.py`, `len(records) < vol_avg_window+5 → skip`), so they're not actually
    traded early. Accidental, not designed — and it does nothing for the survivorship hole.
  - **Partial real mitigants:** large-cap liquid names delist far less than small caps, and
    momentum + ATR stops cut losers mechanically rather than holding to zero. Weak defenses
    — mention, don't lean on them.
  - **The correct fix (= this role's core problem):** point-in-time index constituents —
    reconstruct actual index membership per rebalance date, include delisted names with real
    price history to delisting, add `universe_as_of(date)`. Say: *"My number is optimistic
    and I know why and roughly which direction — I'd rather tell you that than show a clean
    backtest. The fix is exactly the point-in-time data problem this role owns."*

### 4.1 Correctness caveats to volunteer (this is the "is the number right?" section)

An interviewer at a factor-risk shop will probe these. Volunteering them unprompted is the
single strongest signal you "care whether the number on the screen is actually right." Each
has an honest one-liner:

1. **"Walk-forward" — be precise about what you actually did.** You test on six *fixed
   regime buckets* (out-of-sample by period), **not** classic anchored/rolling walk-forward
   with parameter re-fitting on each window. Say: *"It's regime-stratified out-of-sample
   testing, not walk-forward with re-optimization — I fix parameters and check robustness
   across regimes rather than re-fitting a rolling window. True walk-forward with per-window
   refit is the upgrade."* Getting this distinction right matters — the JD names walk-forward
   explicitly and a sharp interviewer will catch an overclaim.

2. **Multiple-testing / holdout contamination — the mature research point.** You've run
   dozens of experiments against the same six periods, and the "Live" period has now been
   looked at many times, so it's no longer a clean holdout — that's data-snooping /
   multiple-hypothesis testing, and it inflates any apparent edge. Say: *"I'm aware my
   in-sample Sharpe is optimistic from repeated testing on a fixed set — the honest number
   needs a deflated Sharpe (Bailey / López de Prado) or a genuinely fresh holdout."* This
   maps directly to "been burned by it in real systems."

3. **Corporate actions / adjusted prices (JD nice-to-have).** Market data comes from
   yfinance, which returns split/dividend-*adjusted* prices by default. Be honest about the
   edge cases: adjustment handling is the vendor's, not yours; you don't independently
   reconcile a corporate-actions feed. At scale you'd want a real corporate-actions pipeline
   so a 1:5 split isn't misread as a −80% return.

4. **Cost model is simplified for Indian frictions.** You charge 0.10% commission + 0.05%
   slippage per side. Real NSE trading also has STT, stamp duty, exchange txn charges, SEBI
   fees, and GST on brokerage. Say: *"My friction is a reasonable round-number proxy, not a
   full Indian-market cost stack — so net returns are slightly optimistic on the cost side
   too."*

5. **Data vendor quality (JD nice-to-have).** yfinance is a free, unofficial source with
   known gaps and occasional bad ticks; production needs a real vendor with SLAs and a
   point-in-time guarantee. You know the difference — that's the honest framing.

6. **Capacity / market impact.** Position sizing models risk (ATR) but not *liquidity impact*
   — at real AUM, would these fills move the market? Not a concern at paper scale, but naming
   it shows quant hygiene.

7. **Point-in-time everywhere, not just prices.** The regime label (RegimeContextAgent) and
   every feature must be computed from completed bars only — you enforce this with `shift(1)`
   / `asof`, but be ready to say you audited the *regime* path for leakage too, not just the
   price features.

**How to use this list:** don't recite all seven. Pick survivorship + one of {walk-forward
precision, multiple-testing} as your lead, and keep the rest in your pocket for "what else
would you worry about?" The meta-message is: *you have a mental map of exactly where your own
numbers are optimistic and by which direction.* That is the founding-quant-engineer signal.

---

## 5. AI components

Two distinct, deliberately-bounded uses of LLMs — and the discipline around them is the
point:

1. **AdaptiveStrategySelector** (`app/meta/adaptive_selector.py`) — GPT-4o-mini re-weights
   the 5 strategies every 5 trading days from a regime snapshot. **"Model proposes, code
   disposes":** the LLM's output is clamped by `_REGIME_WEIGHT_BOUNDS` (code-owned per-
   regime allow-bands) and each strategy has a regime allowlist. The LLM never touches
   money directly — it emits weights that deterministic code validates and bounds.
2. **Narrative / feedback services** (`api/services/narrative_service.py`) — Anthropic
   (Claude) generates human-readable explanations of signals/regime, with a template
   fallback if the key is absent.

**The principle to articulate:** "LLMs are used for *judgment under ambiguity* — regime
interpretation and narrative — never for numerical ranking or as a system of record. They
sit behind a cache for reproducibility and behind code-owned bounds for safety. A bad LLM
response degrades to a template or a clamped weight, never to an unbounded trade."

That framing maps *exactly* to the role's "AI analyst that reasons over fundamentals,
positioning, and market data" — you've already built the safe pattern for putting an LLM
next to money.

---

## 6. "Why FastAPI, PostgreSQL, AWS" — answer honestly

**FastAPI** (true, defend it): async-native, Pydantic request/response typing (so the API
contract is validated at the boundary — "I care whether the number on the screen is
right"), automatic OpenAPI docs, and it shares Python domain code with the backtest and
cron layers — one language, one set of strategy code, no reimplementation between research
and production. This is a strong, honest answer.

**PostgreSQL** (true): needed a real relational store with connection pooling for the
concurrent API + cron read path; used via SQLAlchemy 2.0. Supabase gave managed Postgres +
JWT auth + a client the frontend uses directly.

**AWS — be honest.** The deployment is **Railway**, not AWS, and market data comes from
**yfinance**, not a vendor tick feed. Don't fake this. Say:

> "Full transparency — I deployed on Railway, not AWS, because as a solo builder I
> optimized for shipping speed: managed Postgres, cron, and deploys with near-zero infra
> overhead. I understand the AWS/Modal equivalents — Modal for the compute-heavy
> walk-forward sweeps, S3/a data lake for point-in-time storage, ECS/Lambda for the API
> and cron — and moving to them is exactly the kind of scaling work this role is. What I
> can defend is the *architecture*: stateless API, idempotent cron jobs, and a domain
> layer that's deployment-agnostic, so the substrate is a swap, not a rewrite."

That turns a gap into a maturity signal. Interviewers respect "here's what I actually did
and here's what I'd do at your scale" far more than a bluff.

---

## 7. Biggest engineering challenges (pick 2–3, tell them as stories)

1. **Look-ahead prevention across a shared backtest/live codebase.** The hard part wasn't
   one `shift(1)` — it was guaranteeing the *same* feature code produces the same values
   in a day-by-day backtest replay and in a live cron with only completed bars. Solved by
   making every feature completed-bar-only and replaying via `asof`. *"Been burned by":*
   an early version leaked today's close into the SMA and inflated backtest returns —
   caught it because live diverged from backtest.

2. **Making an LLM-in-the-loop system reproducible.** LLM nondeterminism made it impossible
   to tell whether a code change or the model moved the results. Built a SHA-256
   prompt-hash cache (`llm_cache.py`) that freezes the response stream, so deterministic
   code A/Bs are clean and only prompt changes re-hit the model.

3. **Reconstructing portfolio state from an event log.** There's no authoritative positions
   table — state is rebuilt on demand from `FILLED` signal rows. Trade-off: append-only,
   auditable, no dual-write consistency bugs; cost: reconstruction logic must be exactly
   right and every read pays to replay. Defensible as event-sourcing, and you should name
   both sides.

4. **The research problem itself: distinguishing signal from overfit.** Across dozens of
   experiments, the recurring failure mode was "improves the historical backtest, regresses
   the live-forward period." Building the six-regime walk-forward harness + deterministic
   baseline was what let you *reject your own ideas* with evidence. This is the story that
   matches this role best.

---

## 8. Known bottlenecks (naming them is a strength, not a weakness)

From `docs/architecture_report.html`:
- **Ownership lock-out:** only the opening strategy can exit a position; other strategies'
  exit signals are dropped (~3,600/period). Capital stays committed until the ATR stop.
- **Universe activity bias:** the opportunity score ranks on activity (volume + move + vol),
  which starves the 3 non-breakout strategies and collapses the ensemble toward Breakout
  (~85% of trades).
- **Meta-layer lag:** 2-week regime-stability requirement + 5-day rebalance ⇒ 10–15 trading
  days of effective lag.

Being able to enumerate your own system's weaknesses precisely is exactly the "you care
whether the number is right" signal.

---

## 9. What you'd improve next (this is a live, evidence-backed answer)

You have a *real* research narrative here, not a hand-wave. Recent work systematically
tested and **falsified** the universe-stability hypothesis:
- EMA-smoothing the ranking features reduced churn (54%→48%) but **regressed returns across
  all six periods** — the churn→return causal chain is disproven.
- Ranking-axis experiments (momentum/blend/twostage) either regressed everywhere or helped
  the backtest-middle while hurting the live-forward period (the overfit signature).

**So "what next" has an honest, senior answer:** "I proved the universe/selection layer is
*not* the return bottleneck, which means more tuning of the existing momentum archetype is
the wrong move. The evidence points to two directions: a **capital-preservation exposure
throttle** for the regimes where the archetype has no edge, and adding a **non-directional
strategy archetype** (the current stack is all directional/long-only momentum, which
structurally can't win choppy markets). The meta-lesson — knowing when to *stop*
optimizing an architecture and change the objective — is what I'd bring to a founding role."

That answer demonstrates research maturity, which is worth more than another feature.

---

## 10. Role mapping — Tactiq → TradePolaris (overlaps and honest gaps)

| JD requirement | Your evidence | Strength |
|---|---|---|
| Walk-forward backtesting infra | Six-regime harness, deterministic, cost-adjusted | **Strong — direct** |
| Declarative strategy layer | 5 pluggable strategies, uniform `decide()` interface, weight/regime config | **Strong** |
| Strategy research lifecycle, "been burned by" | The falsification log — you reject your own ideas with data | **Strong — your best asset** |
| Point-in-time data / survivorship / look-ahead | `shift(1)` discipline, `asof` replay; can speak to survivorship in the fixed universe | **Good — you know the traps** |
| Signal generation + paper trading → live | Full paper loop on cron, `PaperAdapter` → path to `kite_adapter` (real broker present) | **Strong** |
| Strong Python + production backend | FastAPI + SQLAlchemy + cron, live with users | **Strong** |
| "Care whether the number is right" | Reproducibility cache, deterministic baseline, look-ahead prevention | **Strong** |
| Factor risk models, covariance estimation | ❌ Not built. You do vol-scaled sizing + regime overlay, not factor/covariance | **GAP — prep below** |
| Point-in-time lake at 2T-row scale | ❌ 150 symbols, yfinance, Railway/Supabase | **GAP — prep below** |
| Next.js / TS web terminal | Frontend exists (React web + mobile); depth unknown | **Partial** |

**How to handle the two real gaps — do not bluff, pre-empt them:**

- **Factor risk / covariance:** "I haven't built a factor risk model — Tactiq does
  volatility-scaled sizing with a regime overlay, not covariance-based optimization. But I
  understand the shape: factor exposures as a loadings matrix, a covariance estimator
  (sample, shrinkage à la Ledoit-Wolf, or factor-structured), and portfolio risk as
  `wᵀΣw`. It's the natural next layer above what I built, and it's exactly the kind of
  math-to-pipeline-to-API ownership I want." — *Do a half-day of reading on Ledoit-Wolf
  shrinkage, Barra-style factor models, and PCA covariance before the interview so this is
  concrete, not memorized.*
- **2T-row point-in-time scale:** "I've built the *correctness* discipline of point-in-time
  data at small scale — the hard part conceptually. Scaling it to a 2T-row lake is an
  infra problem (columnar storage, partitioning by date, Modal for parallel replay) that I
  haven't done at that size but understand the architecture of."

**The line that ties it together:** "I haven't built factor models at fund scale, but I've
built the *research and correctness infrastructure* around a live systematic system solo —
the backtester, the look-ahead discipline, the reproducibility, the paper-to-live path, and
the judgment to kill my own ideas. That's the foundation the specialized quant math sits on,
and it's the part that's hardest to teach."

---

## 11. Rapid-fire prep (likely questions)

- *"Walk me through what happens from market close to a paper trade."* → §2 lifecycle.
- *"How do you prevent look-ahead bias?"* → `shift(1)` + `asof`, same code backtest & live.
- *"How do you know a backtest improvement is real?"* → six-regime walk-forward + deterministic
  baseline + LLM cache; reject anything that helps backtest-middle but hurts live-forward.
- *"Where does the LLM touch money?"* → It doesn't — it proposes bounded weights; code disposes.
- *"What's wrong with your system?"* → §8, said crisply and unprompted.
- *"Why should we hire you over a quant with factor-model experience?"* → §10 closing line.
- *"What would you build first here?"* → The correctness/backtest infra and the point-in-time
  guarantees, because that's what everything else's trustworthiness depends on — and it's what
  you've done before.

---

*Bottom line for you: don't walk in as "a quant." Walk in as "the engineer who built a
correct, reproducible, live systematic trading system solo, and who knows how to tell a real
edge from an overfit one." That's the founding-engineer profile, and it's true.*
