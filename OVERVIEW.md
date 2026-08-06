# Financial Lab — Systematic Trading & Strategy Research Platform

> A production systematic-trading system for **NSE (Indian) equities**: a five-strategy
> momentum / mean-reversion ensemble with an **LLM-assisted regime brain**, a
> **walk-forward backtesting engine** validated across six market regimes, a deterministic
> risk layer, and a **live paper-trading loop**. Built solo, end-to-end — from the market
> math to the data pipeline to the API to the mobile app.

*All results are net of realistic costs (0.10% commission + 0.05% slippage per side).
Paper trading only — no live capital at risk.*

---

## What problem this solves

Discretionary trading doesn't scale and can't be tested. Financial Lab turns "what should I
buy today?" into a **reproducible pipeline**: rank a universe, generate signals from
multiple strategies, weight them by the current market regime, size positions by risk, and
execute — with every decision logged and every change validated against six historical
regimes *before* it ships. The guiding principle throughout is **correctness first**: if a
result can't be reproduced or could be contaminated by look-ahead, it doesn't count.

---

## System architecture

Each layer has **one responsibility** and a **typed hand-off** to the next. Crucially, the
same domain code (`app/`) runs in both the **backtest** and the **live** path — only the
data source and the execution adapter change. That's what makes the backtest trustworthy.

```mermaid
flowchart TB
    subgraph DATA["📥 Data Layer"]
        MD[("Postgres<br/>Market OHLCV<br/>~150 NSE symbols")]
        YF["YFinance Provider<br/>+ NSE Calendar"]
        YF --> MD
    end

    subgraph SELECT["🎯 Selection Layer"]
        UA["<b>DynamicUniverseAgent</b><br/>cross-sectional opportunity score<br/>look-ahead-safe (shift+1)<br/>150 → top 80"]
        UF["<b>UnionUniverseFilter</b><br/>5 per-strategy gates<br/>80 → per-strategy subsets"]
        UA --> UF
    end

    subgraph BRAIN["🧠 Regime Brain (weekly)"]
        RC["<b>RegimeContextAgent</b><br/>150-symbol breadth + trend<br/>→ regime label"]
        AS["<b>AdaptiveStrategySelector</b><br/>GPT-4o-mini proposes weights<br/>behind a prompt-hash cache<br/>→ code-owned bounds clamp them"]
        RC --> AS
    end

    subgraph SIGNAL["⚡ Signal Layer"]
        OBS["<b>MarketObserverAgent</b><br/>per-symbol indicators → MarketState"]
        RT["<b>MultiStrategyRouter</b><br/>5 strategies · conflict resolution<br/>ownership model · weight contest"]
        OBS --> RT
    end

    subgraph RISK["🛡️ Risk & Execution"]
        RA["<b>RiskAgent</b> — 7-layer kill chain<br/>breadth circuit-breaker · ATR sizing<br/>trailing stop · cost gate · cash gate"]
        EX["<b>ExecutionAgent / PaperAdapter</b><br/>cost-adjusted fills at next-day open"]
        RA --> EX
    end

    MD --> UA
    UF --> OBS
    AS -.->|weights| RT
    RC -.->|regime label| RA
    RT --> RA
    EX --> PORT[("Portfolio State<br/>reconstructed from<br/>filled-order event log")]

    style DATA fill:#e3f2fd,stroke:#1976d2
    style SELECT fill:#f3e5f5,stroke:#7b1fa2
    style BRAIN fill:#fff3e0,stroke:#f57c00
    style SIGNAL fill:#e8f5e9,stroke:#388e3c
    style RISK fill:#ffebee,stroke:#c62828
```

**The five strategies** (`app/strategy/`): DualMA (golden-cross trend), Breakout &
QuietBreakout (momentum), TrendPullback (buy-the-dip in an uptrend), RSI Mean-Reversion
(oversold-in-uptrend). Each implements a uniform `decide()` interface, so the ensemble is
pluggable and every strategy is testable in isolation.

---

## The two data stores (two concerns)

| Store | Holds | Why |
|---|---|---|
| **PostgreSQL** (managed) | Market OHLCV, signals, paper-trade sessions, positions, push tokens | Shared source of truth — read by the API, cron jobs, and the mobile/web frontend; connection-pooled for the hot path |
| **SQLite** (`api_state.db`) | Strategy configs, backtest run records, LLM weight decisions | Local operational state for the API layer — simple, no HA needed |

Portfolio state is **event-sourced**: there is no authoritative positions table — it's
reconstructed on demand from `FILLED` order rows. Append-only, auditable, no dual-write
consistency bugs.

---

## Live trading lifecycle

The paper-trading loop runs as scheduled cron jobs against the shared Postgres store,
walking the *same* pipeline the backtest uses.

```mermaid
sequenceDiagram
    autonumber
    participant FE as 📱 Frontend
    participant DB as 🗄️ Postgres
    participant SIG as run_paper_signals<br/>(10:35 UTC)
    participant ORD as run_paper_orders<br/>(10:45 UTC)
    participant PNL as run_daily_pnl<br/>(10:15 UTC)
    participant U as 🔔 User

    FE->>DB: create paper_trade_session
    Note over SIG: end of trading day
    SIG->>DB: load active sessions + EOD data
    SIG->>SIG: Router → RiskAgent → cash gate
    SIG->>DB: write PENDING signals to queue
    Note over ORD: next morning
    ORD->>DB: read yesterday's PENDING
    ORD->>ORD: fill at next-day open (PaperAdapter)
    ORD->>DB: mark FILLED
    PNL->>DB: price FILLED positions
    PNL->>U: push notification — P&L summary
```

---

## How research works (the part that matters most)

A trading idea is worthless until it survives validation. The backtest engine
(`app/backtest/engine.py`) is a **daily event loop** with three correctness guarantees:

```mermaid
flowchart LR
    A["💡 Idea"] --> B["Walk-forward<br/>6 regimes<br/>Bull · Crash · Recovery<br/>Bear · Recent · Live"]
    B --> C{"Improves<br/>ALL regimes?"}
    C -->|"helps one,<br/>hurts another"| D["❌ Reject<br/>(overfit)"]
    C -->|"holds everywhere"| E["✅ Ship"]
    B --> F["Deterministic<br/>PYTHONHASHSEED=0<br/>+ LLM prompt-hash cache"]
    F -.->|"clean A/B:<br/>code change vs<br/>model noise"| B

    style D fill:#ffebee,stroke:#c62828
    style E fill:#e8f5e9,stroke:#388e3c
    style F fill:#fff3e0,stroke:#f57c00
```

1. **Walk-forward across six regimes** — a change must not help one market and quietly hurt
   another. The recurring failure mode ("improves the historical backtest, regresses the
   live-forward period") is exactly what this catches.
2. **Look-ahead prevention** — every feature uses completed bars only (`shift(1)`), and the
   engine replays day-by-day via `asof` lookups, so no code path can see the future in
   backtest *or* live.
3. **Reproducibility** — runs are deterministic; the only LLM call sits behind a SHA-256
   prompt-hash cache, so a code change can be A/B-tested without the model's randomness
   polluting the comparison.

---

## Where AI is used (and where it is deliberately *not*)

**"Model proposes, code disposes."** LLMs are used for *judgment under ambiguity*, never as
a system of record or a numerical ranker:

- **AdaptiveStrategySelector** — GPT-4o-mini re-weights the five strategies every five days
  from a regime snapshot. Its output is **clamped by code-owned per-regime bounds** and each
  strategy has a regime allowlist. The LLM never touches money directly — a bad response
  degrades to a bounded weight, never an unbounded trade.
- **Narrative service** — Claude generates plain-English explanations of signals and
  regime, with a template fallback if the key is absent.

---

## Tech stack

| Layer | Technology |
|---|---|
| API | **FastAPI** (async, Pydantic-typed contracts, shared Python domain code) |
| Data | **PostgreSQL** (SQLAlchemy 2.0) · SQLite (config) · YFinance (market data) |
| AI | **OpenAI GPT-4o-mini** (regime weights) · **Anthropic Claude** (narrative) |
| Execution | Paper adapter → Zerodha Kite adapter (path to live) |
| Clients | React web terminal · React Native mobile app |
| Ops | Scheduled cron jobs · push notifications (Expo) · email (Resend) |

---

## Design principles

- **Single-responsibility layers, typed hand-offs** — any one layer can be swapped or
  A/B-tested without the others moving.
- **Same code in backtest and live** — the paper results are trustworthy because there is no
  separate research codebase to drift out of sync.
- **Correctness over cleverness** — reproducibility, look-ahead prevention, and cost-adjusted
  fills come before any performance number.
- **Deterministic core, isolated AI** — the LLM is bounded, cached, and never on the money
  path unsupervised.

---

## Repository map

```
app/
├── universe/     # DynamicUniverseAgent + per-strategy filters (selection)
├── strategy/     # 5 strategies + MultiStrategyRouter (signals)
├── meta/         # AdaptiveStrategySelector + RegimeContextAgent (regime brain)
├── risk/         # RiskAgent — position sizing, circuit-breakers, stops
├── backtest/     # BacktestEngine — walk-forward daily event loop
├── execution/    # cost-adjusted fill simulation
├── data/         # MarketDataRepository, providers, NSE calendar
└── analytics/    # diagnostics: opportunity quality, ensemble, universe stability

api/               # FastAPI app (routers, services) + cron scripts (deployed)
docs/              # architecture reports, experiment logs, research write-ups
```

---

*Built to answer one question rigorously: **is the number on the screen actually right?***
