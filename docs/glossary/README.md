# Glossary — the domain vocabulary behind V2

Written for a software engineer who knows how to build systems but not the Indian
equity-market plumbing they're being built on. Every term here appears somewhere in
`app/`, `scripts/`, `docs/charter/` or `docs/research_log.md`.

Read in order the first time; after that use it as a lookup.

| File | Covers |
|---|---|
| [01-market-data.md](01-market-data.md) | bhavcopy, UDiFF, ISIN, series, OHLC, corporate actions, delisting, the trading calendar |
| [02-filings-and-xbrl.md](02-filings-and-xbrl.md) | XBRL, iXBRL, contexts, taxonomies, dissemination time, consolidated vs standalone, our parser |
| [03-accounting-and-signal.md](03-accounting-and-signal.md) | EPS, revenue, PAT, seasonal surprise, SUE, consensus, PEAD, sector-adjusted return |
| [04-research-methodology.md](04-research-methodology.md) | point-in-time, survivorship bias, look-ahead, restatement, folds, pre-registration |
| [05-codebase-map.md](05-codebase-map.md) | which module owns which concept |

---

## The one-paragraph version

We are testing whether an **earnings surprise** predicts a stock's return over the
following month. To do that honestly you need four things, and each has its own
vocabulary:

1. **What was announced, and exactly when** — the filing (XBRL) and its
   dissemination timestamp. → file 02
2. **What was expected** — here, the same quarter one year earlier, because Indian
   analyst coverage is too thin for a consensus. → file 03
3. **What happened next** — daily prices for the following ~20 trading sessions.
   → file 01
4. **Proof you didn't cheat** — that you only used information available at the
   time, and didn't quietly delete the companies that failed. → file 04

## How the pieces connect

```
  NSE filing archive                    NSE/BSE bhavcopy
  (what was announced)                  (what happened next)
         │                                      │
    XBRL document                     one CSV per trading day,
    + dissemination                   every listed instrument
      timestamp                                 │
         │                                      │
         ▼                                      ▼
   EPS for a quarter  ──── surprise ────►  20-session return
         │              (vs same quarter         │
         │               one year earlier)       │
         ▼                                      ▼
              does surprise predict return?
                  (charter §8 pass bar)
```

The left branch is built (`app/event_research/`). The right branch is **not built** —
that is the current top priority.

## Two ideas worth absorbing before anything else

**"Free" data is not the same as "usable" data.** Nearly everything in this project is
free and unauthenticated. The cost is that it arrives undocumented, changes schema
without notice, and fails by returning nothing rather than by erroring. See
`docs/research_log.md` 2026-08-12: a dead URL was read by our own code as *"the
exchange held no trading sessions for 400 days."*

**The hard part is not the prediction, it's the honesty.** Most of the vocabulary in
file 04 exists to name a specific way a backtest can lie to you. A model that looks
profitable because it quietly used tomorrow's information, or because the companies
that went bankrupt were dropped from the dataset, is the default outcome — not an
unusual failure.
