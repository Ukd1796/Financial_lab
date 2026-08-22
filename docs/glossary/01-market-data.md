# 01 — Market data: prices, identity, and the trading calendar

## Exchanges

**NSE** (National Stock Exchange) and **BSE** (Bombay Stock Exchange) are India's two
equity exchanges. Most liquid names trade on both. This matters more than it sounds:
a company that stops trading on NSE has *not* necessarily died — it may still trade on
BSE. Measured on our own data, **44% of NSE exits still trade on BSE under the same
identifier**. Charter amendment §4 therefore defines "delisted" as absent from *both*.

## bhavcopy

The **end-of-day dump published by an exchange**: one file per trading day, containing
one row for every instrument that traded, with open/high/low/close, volume and
turnover.

The name is Hindi/Gujarati market slang — *bhav* means "price" or "rate", so it is
literally "the price copy". It predates electronic distribution; the term stuck.

Why it's the backbone of this project:

- **Free and unauthenticated.** A plain HTTPS GET, no key, no licence.
- **Complete.** Every listed instrument, not a curated index. Nobody decided which
  companies were interesting enough to include.
- **Point-in-time by construction.** The file published on 2019-03-14 contains what
  traded on 2019-03-14. It cannot have been retroactively edited to remove companies
  that later went bankrupt — which is exactly the bias that ruins backtests (file 04).
- **It doubles as the trading calendar.** If a bhavcopy exists for a date, the market
  was open. There is no separate holiday feed to trust.

That last property is elegant and once bit us badly — see *silent failure* below.

We currently hold only **month-end** bhavcopies (~159 files, `data/analysis/bhavcopy/`),
which were enough to build delisting labels. Measuring a 20-session return needs
**daily** ones. Same endpoint, same parser, just every session instead of every month.

## UDiFF

**Universal Data Interchange File Format** — the ISO-20022-flavoured schema NSE
migrated its bhavcopy to. The practical consequences are two:

1. **The URL changed.** Legacy `.../cm{DD}{MON}{YYYY}bhav.csv.zip` versus new
   `.../BhavCopy_NSE_CM_0_0_0_{YYYYMMDD}_F_0000.csv.zip`. The cutover is a *window*,
   not an instant — both worked in March 2024.
2. **The column names changed.** `TckrSymb`, `SctySrs`, `TtlTrfVal`, `TtlTradgVol`
   replace `SYMBOL`, `SERIES`, `TOTTRDVAL`, `TOTTRDQTY`.

`normalise_bhavcopy_row` in `app/analysis/delisting.py` renames the new columns to the
legacy names so callers see one schema across the cutover. BSE publishes in the
*identical* UDiFF schema, which is why the NSE∪BSE union costs nothing but the fetch.

### Silent failure — the lesson worth internalising

Our fetcher only knew the legacy URL. When NSE migrated, every request 404'd. But the
code treats "no bhavcopy for this date" as "the market was closed that day" — a
deliberate, correct-looking design decision. So a schema migration became, to our
system, *"the exchange has held no trading sessions in 400 days"*, reported with no
error at all.

The fix was to try every known URL template and only raise when **all** of them 404.
The generalisable rule, now in the research log: **treat any zero-row NSE result as a
suspected migration until proven otherwise.** NSE deprecates endpoints by deleting
files, not by returning an error code.

## ISIN vs symbol — instrument identity

**Symbol** is the ticker (`RELIANCE`, `TCS`). Human-readable, and **mutable**:
`PVR` became `PVRINOX`, `MCDOWELL-N` became `UNITDSPR`. Key your dataset on symbol and
every rename reads as one company dying and a new one being born.

**ISIN** (International Securities Identification Number, e.g. `INE002A01018`) is a
12-character global identifier. Structure matters here:

```
INE002A01018
├─ INE002A01  ── first 9 chars: the ISSUER (the company)
└─ 018        ── last 3: the INSTRUMENT (this specific share class / face value)
```

A stock split or face-value change issues a **new ISIN for the same company**
(`INE092B01017` → `INE092B01025`). Key on the full ISIN and *those* read as deaths too
— this inflated our delisting count by 318 names before it 
 caught.

The rule the project settled on: identity is **issuer prefix + a surviving sibling
instrument**. If the issuer prefix is still trading under some instrument code, the
company is alive.

With one deliberate exception. DHFL's issuer prefix now belongs to PIRAMALFIN, which
absorbed it through insolvency — the *legal entity* continued while the equity was
wiped out. So a surviving issuer code rescues a name **only if the exit wasn't a
collapse**. We label what a shareholder experienced, not what a registrar recorded.

**`INF*` prefixes** are mutual-fund and ETF units, not companies — 412 of them were
excluded from the universe. One asset manager's prefix can span dozens of products
(ICICI's `INF109K..` covers 29 ETFs), which breaks issuer-identity reasoning entirely.

## Series

A one-or-two letter code on each bhavcopy row describing *what kind of instrument* the
row is. `EQ` is ordinary equity with normal settlement; others cover trade-to-trade
segments, debt, rights entitlements. Filtering to `EQ` is how you avoid mixing bonds
and rights into an equity study.

## OHLC and PREVCLOSE

**Open, High, Low, Close** for one instrument on one day — the standard price bar.
`data_cache/market_ohlc.sqlite` holds these for V1's 150-symbol universe.

**PREVCLOSE** is the previous session's close as stated *in today's file* — and that is
all it is.

It is worth knowing what it is *not*, because this project believed otherwise for a day.
The idea that the exchange restates PREVCLOSE on an ex-date, making the adjustment ratio
readable straight off the price file, is appealing and wrong. Measured on RELIANCE's 1:1
bonus (ex-date 2024-10-28): close fell 2655.70 → 1334.35 while PREVCLOSE stayed
**2655.70**. Across the whole panel, adjacent sessions show zero restatements. Corporate
actions have to come from the announcement feed instead — see below.

## Corporate actions

Events that change the share count or price without changing company value:

- **Split** — one ₹1,000 share becomes ten ₹100 shares. Price drops ~90%.
- **Bonus issue** — free additional shares. A 1:1 bonus roughly halves the price.
- **Dividend** — cash out, price drops by roughly the dividend on the ex-date.
- **Ex-date** — the first day the stock trades *without* the entitlement. The
  mechanical price drop happens here.

**Why this is not a detail.** If a 1:2 split falls inside a 20-session window after an
earnings announcement, the raw price series shows −50% and the study records a
catastrophic reaction to good news. It's a fabricated signal, and it fires precisely on
the fast-growing companies most likely to split.

**Price data alone cannot identify one.** An earlier attempt inferred actions from
monthly close ratios and mislabelled RELIANCE's 1:1 bonus as 0.451 rather than 0.500,
because the stock also fell ~10% that month. Daily data does not rescue it either, since
PREVCLOSE is never restated: **a split and a crash produce the same observation** at any
resolution. That is an identification problem, not a tuning problem.

The solution is a second, independent source: NSE's public corporate-action feed
(`/api/corporates-corporateActions`), which is free and bulk and states the action in
words — `Bonus 1:1`, `Face Value Split (Sub-Division) - From Rs 10/- Per Share To Re 1/-
Per Share`. Parsing that gives an **announced** ratio, which is then checked against the
**observed** price move on the ex-date. Two unrelated systems agreeing is the evidence
that both the feed and the parse are right; we currently agree on 98.3% of 286 checkable
actions, and the handful that disagree are stored flagged rather than applied.

Two traps found doing this, both instances of the ISIN lesson above:

- **A face-value split issues a new ISIN.** All 174 splits in the window vanish from the
  panel under their announced code on the ex-date; 143 reappear under a sibling code.
- **The feed keeps quoting the retired ISIN forever.** Nestlé's 2025 bonus is still
  announced under `INE239A01016`, retired by its January-2024 split. Looking up prices
  under the announced code read a pre-split price and reported a 1:1 bonus as a 96% fall.

Both are fixed by keying on the **issuer prefix**, never the full ISIN.

## Turnover / traded value

`TOTTRDVAL` (legacy) or `TtlTrfVal` (UDiFF): the rupee value traded in a session. Used
as the liquidity ranking to build cohorts — "the 500 most-traded names as of date X".
Turnover is preferable to volume because volume is share-count and therefore not
comparable across stocks with wildly different prices.

## Delisting and the collapse label

**Delisting** = the instrument stops trading. Our labels are derived purely from
bhavcopy presence and absence, with no vendor involved:

| Label | Meaning |
|---|---|
| `ACTIVE` | still trading |
| `EXIT_AFTER_COLLAPSE` | stopped trading ≥70% below its lifetime peak |
| `EXIT_FLAT_OR_UP` | left in good health — usually a merger or buyout |
| `EXIT_AMBIGUOUS` | between −25% and −70% from peak |
| `INSTRUMENT_CHANGED` | ISIN reissued; the company is alive |

Measured across 2018–2026: **643 of 3,411 ISINs (19%) stopped trading on NSE**, of
which **212 died ≥70% below peak**. That population is invisible to any dataset built
from today's index constituents — and it's the population a strategy most needs to
avoid.

One subtlety worth the detour: the first version of this classifier measured
**trailing 12-month return** and labelled DHFL (+53%) and RCOM (+72%) as *benign*
exits. Both had already collapsed years earlier and spent their final year bouncing
around as penny stocks, so a one-year window measured the bounce, not the collapse.
Switching to **fall from lifetime peak** fixed both (DHFL −97%, RCOM −91%). The
measurement window silently encoded an assumption, and only checking known cases by
hand exposed it.
