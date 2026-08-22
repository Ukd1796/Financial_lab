# 02 — Filings and XBRL: what was announced, and exactly when

## The regulatory shape

SEBI-listed Indian companies must publish quarterly financial results. Each filing is
disseminated through the exchange, which timestamps it and publishes it to an archive.
Two properties make this the backbone of the V2 signal:

- It is **as-filed**. Nobody has restated it since.
- It carries an **exact publication timestamp**, so we know the precise moment the
  information became public.

Almost no free data source has either property. This one is free and has both.

## XBRL

**eXtensible Business Reporting Language** — an XML dialect for financial reports.
Think of it as a typed, machine-readable financial statement: instead of a PDF where
"Revenue: 1,234" is text on a page, you get an element whose *tag* names the accounting
concept and whose *attributes* say which period and which entity it belongs to.

An **instance document** is one filing. It contains:

- **Facts** — the numbers. `<in-bse-fin:RevenueFromOperations contextRef="OneD">1234</...>`
- **Contexts** — the metadata each fact points at, via `contextRef`.
- **Units** — rupees, shares, pure ratios.
- A reference to a **taxonomy**, the shared dictionary defining what
  `RevenueFromOperations` means.

### Contexts — the part that actually matters

A **context** is *"who, when, and along what breakdown"*. A duration context:

```xml
<context id="OneD">
  <entity><identifier>...</identifier></entity>
  <period>
    <startDate>2023-01-01</startDate>
    <endDate>2023-03-31</endDate>
  </period>
</context>
```

Every fact carries a `contextRef` pointing at one of these. **A number without a
resolvable context is meaningless** — 12.93 could be this quarter's EPS, last year's,
or the full year's.

**Dimensional contexts** add a breakdown axis (by business segment, by geography). Our
parser deliberately ignores these: a segment's revenue is not the company's revenue,
and they share the same dates as the headline figure, so mistaking one for the other is
easy and silent.

**Instant vs duration.** Balance-sheet items ("cash on 31 March") are instants; income
items ("revenue during Jan–Mar") are durations. Our fields are durations.

### The `OneD` / `FourD` defect

The single biggest data problem in V2, and worth understanding in detail.

NSE result instances conventionally define contexts named `OneD` (the quarter, "one"
quarter of data) and `FourD` (the cumulative year-to-date figure). **In filings before
~2023, facts reference these contexts and the document never defines them.** The
`contextRef` points at nothing.

The parser could guess — assume `OneD` means the quarter and move on. It deliberately
does not, and returns `UNRESOLVED_CONTEXT` instead, because the guess is unsafe in a
specific direction: an instance may hold both the reported quarter and other periods,
so a wrong assignment doesn't produce noise, it produces a **sign-inverted surprise**.
The signal would be confidently backwards.

#### But the convention can be *proved* from the document (measured 2026-08-18)

The caution above is right about an unvalidated guess. It is not the last word, because
the document carries enough internal evidence to settle the question without assuming
anything. Two independent checks, run over all 439 `UNRESOLVED_CONTEXT` filings:

**1. The magnitude test.** The Indian fiscal year runs Apr–Mar, so a year-to-date figure
at fiscal quarter *N* spans *N* quarters. If `FourD` is cumulative, `FourD / OneD` on a
large additive flow item (`Income`, `Expenses`, `RevenueFromOperations`,
`ProfitBeforeTax`) should track *N*:

| Fiscal quarter | Expected ratio | Observed median | n |
|---|---|---|---|
| Q2 | 2 | **1.92** | 109 |
| Q3 | 3 | **2.89** | 127 |
| Q4 | 4 | **3.87** | 99 |

**2. The sibling-context test.** These documents *do* define dimensional contexts —
`OneOperatingExpenses01D`, `FourReportableSegmentRevenue02D` — and every one of them
carries the reported quarter's dates. Only the bare, non-dimensional `OneD` / `FourD`
are left undefined.

So `OneD` is the discrete quarter and `FourD` is the year-to-date cumulative, and it is
**measured rather than assumed**. Note the test is a *discriminating* one, not a
precision one: quarters are unequal, so the ratio never lands exactly on *N*. The only
question that needs answering is whether `FourD` spans more than one quarter — is the
ratio closer to *N* than to 1? — which is a wide and robust decision.

Recovery on the pilot corpus: **316 of 439 (72%) resolve**, 19 stay genuinely ambiguous,
and 104 carry only `OneD` with no `FourD` to compare against (for those the corpus-wide
convention is evidence, but weaker than a per-document proof).

#### Now APPLIED, opt-in, with its own status (2026-08-18, later)

Implemented as `resolve_undefined_period_convention` in `app/event_research/xbrl_parser.py`,
reached by `parse_result_xbrl(..., resolve_conventions=True)`. Three deliberate choices:

- **Off by default.** The strict reading stays the default so a corpus is never
  half-parsed under two rules by accident.
- **Its own status, `RECOVERED_CONVENTION` — not `VALID`.** These filings are usable, but
  their period was *proved from the values* rather than *read from a defined context*.
  Keeping the status separate means any result can be re-run with them excluded, which
  is the only way to show the finding does not depend on them.
- **Re-parsing happens after all fetching, never during**, via
  `scripts/event_research/reparse_corpus.py`. Facts are re-derived from the immutable
  archived documents — that is what `parser_version` is for. Verified faithful: re-parsing
  the 7,771-filing corpus with recovery *off* changed **0 values and 0 statuses**.

With recovery on, 139 filings in the current corpus move `UNRESOLVED_CONTEXT →
RECOVERED_CONVENTION`. The larger gain arrives with the 2022 filings, which are the
year-ago comparatives fold A needs.

**An earlier claim here was wrong and is corrected.** This section previously said the
recovered filings were unusable because the price panel starts 2023-03-15. That is true
for *evaluating* a 2019–2022 event, but **not** for using a 2022 filing as a year-ago
comparative: the comparative supplies a single EPS number and nothing else
(`build_event_features.py` reads `prior["eps"]`; prices are fetched only for the current
event). No price backfill is required to extend the comparatives.

Measured across the pilot cohort by dissemination year:

| Year | Usable |
|---|---|
| 2019 | 0% |
| 2020 | 0% |
| 2021 | 0% |
| 2022 | 0% |
| 2023 | 65% |
| 2024 | 100% |
| 2025 | 100% |

This is an **era boundary**, not a per-filer quirk — everything before 2023 is
uniformly broken, everything after is uniformly clean, and 2023 is the single mixed
transition year. It is what forced the charter's study window to be rewritten: the
originally planned 2018–2022 development block is 100% unusable.

### A second defect, found 2026-08-13

Even in the clean era, `OneD` and `FourD` are frequently **both defined with identical
dates** — the same three-month period — while carrying different values: the quarterly
EPS and the year-to-date EPS respectively (median ratio ≈ 2.95). Measured on our 226
usable filings, 190 carry `basic_eps` on more than one context.

So the declared period does *not* distinguish the quarter from the year-to-date
figure. Only the context *naming convention* does — and a convention is not data.

The parser currently picks the right one in 226 of 226 cases, but only because `OneD`
happens to be defined first in document order every time, and the selection falls
through to "first match". Nothing enforces it. A filer emitting `FourD` first would
silently store a ~3× inflated "quarterly" EPS. See `docs/research_log.md` 2026-08-13.

## iXBRL

**Inline XBRL** — the same tagged facts, but embedded in an HTML document so it renders
as a human-readable report while remaining machine-parseable. Tags live in
`<ix:nonFraction>` elements rather than as standalone XML.

Relevant because NSE's newer **integrated filing** endpoint serves iXBRL, not plain
XBRL. Our parser handles plain XBRL only, so **everything from 2025 H2 onward is
currently unreadable** — which is why building this path is a top-three priority.

## Taxonomy

The shared dictionary defining every valid element name. Two filings using
`RevenueFromOperations` mean the same thing only if they reference the same taxonomy
version. Worth checking when numbers look wrong across an era — though in our case both
sides of the break reference `2020-03-31`, which is how we know the `OneD`/`FourD`
problem is *not* a taxonomy-version issue.

## Dissemination time

`exchdisstime` in the NSE filing index: the moment the exchange published the filing,
to the second, in Asia/Kolkata. Present on **every** filing — zero missing across
2,328 and 3,230 record samples.

This is the causal clock and it is non-negotiable. An earnings study measures the
market's reaction to an announcement, so the announcement moment must be known exactly,
not inferred from a quarter-end date. A filing disseminated at 17:15 was not tradeable
at that day's close; the first tradeable price is the next session's open. Getting this
wrong is **look-ahead bias** (file 04) and it manufactures profits that don't exist.

In our schema: `disseminated_at` is what the exchange said, `available_at` is when we
consider the information actionable.

## Filing attributes you must not ignore

**Consolidated vs standalone.** Standalone is the parent company alone; consolidated
includes subsidiaries. A company files both, with materially different EPS. Mixing them
across quarters creates a fake surprise. Pick one convention and hold it.

**Cumulative (year-to-date) vs discrete.** A Q2 filing often reports the six months to
date rather than the three-month quarter. Comparing a cumulative figure against a
discrete one is roughly a 2× fake surprise. Stored as `is_cumulative`.

**Audited vs unaudited.** Quarterly results are typically unaudited; annual ones are
audited. Numbers can move between them.

**Revisions.** A company can refile. The original is never overwritten — a revision is
stored as a new record pointing at what it supersedes. For point-in-time work you want
the number as originally published, because that is what the market actually traded on.

## Where the filings come from

| Endpoint | Covers | Status |
|---|---|---|
| `/api/corporates-financial-results` | bulk filings, ~2019 → Feb 2025 | works, but **stopped carrying bulk filings after ~Feb 2025** |
| `/api/integrated-filing-results` | Feb 2025 → present | exists, paginated at 20 rows, serves **iXBRL** — **not built** |

The first endpoint went from 3,776 rows for a quarter to essentially nothing —
consistent with SEBI's Integrated Filing regime relocating quarterly results. Same
pattern as the bhavcopy migration in file 01: **the old endpoint didn't error, it just
went quiet.**

## Our validation statuses

From `app/event_research/xbrl_parser.py`:

| Status | Meaning |
|---|---|
| `VALID` | every headline fact resolved to a proven period |
| `UNRESOLVED_CONTEXT` | facts reference contexts the document never defines — values withheld |
| `NO_MATCHING_PERIOD` | contexts resolve, but none matches the expected reporting period |
| `UNPARSEABLE` | not well-formed XML |

The design principle throughout: **withhold rather than approximate.** Every failure is
recorded as an `event_data_exception` and reported *before* any outcome is computed,
because dropping unparseable filings silently would preferentially delete the companies
that failed — see *missing-data bias* in file 04.


---

## Chaining, and why the fetch window is a research decision

*Added 2026-08-18, after this cost fold A four of its six quarters.*

No filing contains its own year-ago comparative — measured, 226 of 226 (see
`docs/research_log.md`, 2026-08-13). A filing carries the current quarter and the current
year-to-date figure, and nothing else.

So a seasonal surprise is always built from **two separately fetched filings twelve months
apart**, and that has a consequence which is easy to miss:

> **A download window starting on date D does not give you events from date D.
> It gives you events from D + 12 months.**

Everything in the first year of a window has a current filing and no comparative, so it
cannot be chained at all.

Measured on the real corpus: the main fetch began 2023-06-01, and fold A spans reaction
sessions Jul 2023 – Dec 2024. Six quarters fall in that window; only **two** had their
comparative. Charter v3 §4 requires four. Fold A was therefore INCONCLUSIVE **by
construction** — decided by a fetch parameter before a single return existed.

The corollary is a rule worth keeping:

- **Fetch a full year earlier than the earliest event you intend to study.**
- The extra year needs **filings only, not prices** — comparatives contribute an EPS number.
- If that extra year sits in the broken-XBRL era, it needs `--resolve-conventions` to be
  usable at all, which is why the two fixes travel together
  (`scripts/event_research/extend_backwards.sh`).
