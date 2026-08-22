"""Corporate actions from NSE's announcement feed, validated against prices.

A split, bonus or consolidation changes the quoted price without changing what
a holder owns.  Left uncorrected inside a 20-session event window a 1:2 split
reads as a -50% reaction to an earnings announcement -- a fabricated signal that
fires preferentially on fast-growing companies.

**A rejected approach, recorded so it is not retried.**  ``docs/research_log.md``
(2026-08-12) suggested recovering actions from daily data because "the ex-date's
adjusted PREVCLOSE settles it".  Measured 2026-08-14 on RELIANCE's 1:1 bonus
(ex-date 2024-10-28): close fell 2655.70 -> 1334.35 while ``PrvsClsgPric``
stayed **2655.70**.  Neither NSE nor BSE restates PREVCLOSE for corporate
actions -- it is simply the previous session's close.  Across the whole panel,
zero restatements exist between adjacent sessions.  The premise was wrong, and
daily prices alone cannot identify an action: a split and a crash still produce
the same observation, exactly as the monthly-close attempt found.

What works is the exchange's own announcement feed, which is free, bulk and
carries the ISIN, the ex-date and the action in words ("Bonus 1:1").  Two
independent facts are then available for every action:

* the **announced** ratio, parsed from the subject line, and
* the **observed** ratio, ``close(ex_date) / close(previous session)``.

They come from unrelated systems, so their agreement is the evidence that the
action is real and the parse is right.  A subject line we cannot parse is stored
as ``UNPARSED`` rather than skipped -- an unrecognised split silently dropped is
precisely the failure this module exists to prevent.
"""

from __future__ import annotations

import json
import re
import sqlite3
from dataclasses import dataclass
from datetime import date, datetime
from typing import Any, Iterable

CORPORATE_ACTIONS_PATH = "/api/corporates-corporateActions"
CORPORATE_ACTIONS_REFERER_PATH = "/companies-listing/corporate-filings-actions"

KIND_BONUS = "BONUS"
KIND_SPLIT = "SPLIT"
KIND_CONSOLIDATION = "CONSOLIDATION"
KIND_DIVIDEND = "DIVIDEND"
KIND_RIGHTS = "RIGHTS"
KIND_OTHER = "OTHER"
KIND_UNPARSED = "UNPARSED"

# Kinds that mechanically rescale the share count and therefore the price.
PRICE_SCALING_KINDS = (KIND_BONUS, KIND_SPLIT, KIND_CONSOLIDATION)

# How far the observed price move may sit from the announced ratio before the
# pair is called a disagreement.  Wide on purpose: the ex-date carries genuine
# trading on top of the mechanical adjustment, so an exact match is not expected.
VALIDATION_TOLERANCE = 0.08


_SCHEMA = """
CREATE TABLE IF NOT EXISTS corporate_actions (
    isin            TEXT NOT NULL,
    ex_date         TEXT NOT NULL,
    subject         TEXT NOT NULL,
    kind            TEXT NOT NULL,
    announced_ratio REAL,
    symbol          TEXT,
    series          TEXT,
    face_value      TEXT,
    observed_ratio  REAL,
    validation      TEXT,
    PRIMARY KEY (isin, ex_date, subject)
) WITHOUT ROWID;

CREATE INDEX IF NOT EXISTS ix_corporate_actions_isin ON corporate_actions (isin, ex_date);
CREATE INDEX IF NOT EXISTS ix_corporate_actions_kind ON corporate_actions (kind);
"""


@dataclass(frozen=True)
class CorporateAction:
    isin: str
    ex_date: str
    subject: str
    kind: str
    announced_ratio: float | None
    symbol: str | None = None
    series: str | None = None
    face_value: str | None = None
    observed_ratio: float | None = None
    validation: str | None = None


def ensure_schema(conn: sqlite3.Connection) -> None:
    conn.executescript(_SCHEMA)


_BONUS_RE = re.compile(r"bonus\s*(\d+)\s*:\s*(\d+)", re.I)
_RIGHTS_RE = re.compile(r"rights\s*(\d+)\s*:\s*(\d+)", re.I)
# "Rs 10/-" and "Re 1/-" both occur -- NSE uses the singular for one rupee, and
# missing it left every 10:1 split unparsed on the first pass.
_FACE_VALUE_RE = re.compile(
    r"face\s*value\s*(?:split|sub[\s-]*division|consolidation)?.*?"
    r"from\s*r[se][.\s]*([\d.]+).*?to\s*r[se][.\s]*([\d.]+)",
    re.I | re.S,
)


def parse_subject(subject: str) -> tuple[str, float | None]:
    """Classify an NSE corporate-action subject line and derive its price ratio.

    The ratio is the multiplier that converts a pre-action price to the
    post-action basis, i.e. ``price_after / price_before`` if nothing else moved.
    """
    text = (subject or "").strip()
    if not text:
        return KIND_UNPARSED, None

    lowered = text.lower()

    # A bonus of A:B issues A new shares for every B held, so B shares become
    # A+B and the price scales by B/(A+B).
    bonus = _BONUS_RE.search(text)
    if bonus:
        new, held = int(bonus.group(1)), int(bonus.group(2))
        total = new + held
        return (KIND_BONUS, held / total) if total else (KIND_UNPARSED, None)

    # A face-value change rescales the share count by old/new.
    face = _FACE_VALUE_RE.search(text)
    if face:
        try:
            old_value, new_value = float(face.group(1)), float(face.group(2))
        except ValueError:
            return KIND_UNPARSED, None
        if old_value <= 0 or new_value <= 0:
            return KIND_UNPARSED, None
        ratio = new_value / old_value
        kind = KIND_SPLIT if ratio < 1 else KIND_CONSOLIDATION
        return kind, ratio

    if _RIGHTS_RE.search(lowered):
        # A rights issue's price effect depends on the subscription price, which
        # the subject line does not reliably carry.  Recorded, not quantified.
        return KIND_RIGHTS, None

    if "dividend" in lowered:
        # Cash, not a share-count change.  The price effect needs the amount and
        # the prevailing price; it is small and is not applied here.
        return KIND_DIVIDEND, None

    if any(word in lowered for word in ("split", "sub-division", "subdivision")):
        return KIND_UNPARSED, None

    return KIND_OTHER, None


def _parse_ex_date(value: str | None) -> str | None:
    text = (value or "").strip()
    if not text or text == "-":
        return None
    for fmt in ("%d-%b-%Y", "%d-%m-%Y", "%Y-%m-%d"):
        try:
            return datetime.strptime(text, fmt).date().isoformat()
        except ValueError:
            continue
    return None


def fetch_corporate_actions(
    client: Any, from_date: date, to_date: date
) -> list[CorporateAction]:
    """Announced corporate actions for a window, from NSE's public feed.

    Bulk and free: one request covers every listed security, so there is no
    per-symbol cost and no vendor call.
    """
    from app.event_research.nse_client import BASE, NSEUnavailable

    url = (
        f"{BASE}{CORPORATE_ACTIONS_PATH}?index=equities"
        f"&from_date={from_date.strftime('%d-%m-%Y')}"
        f"&to_date={to_date.strftime('%d-%m-%Y')}"
    )
    payload = client._get(
        url,
        referer=f"{BASE}{CORPORATE_ACTIONS_REFERER_PATH}",
        accept="application/json",
    )
    try:
        body = json.loads(payload)
    except json.JSONDecodeError as exc:
        raise NSEUnavailable(
            f"Corporate-action index was not JSON for {from_date}..{to_date}: {exc}"
        ) from exc
    rows = body if isinstance(body, list) else body.get("data", [])

    actions: list[CorporateAction] = []
    for row in rows:
        isin = (row.get("isin") or "").strip().upper()
        ex_date = _parse_ex_date(row.get("exDate"))
        subject = (row.get("subject") or "").strip()
        if not isin or not ex_date or not subject:
            continue
        kind, ratio = parse_subject(subject)
        actions.append(
            CorporateAction(
                isin=isin,
                ex_date=ex_date,
                subject=subject,
                kind=kind,
                announced_ratio=ratio,
                symbol=(row.get("symbol") or "").strip() or None,
                series=(row.get("series") or "").strip() or None,
                face_value=(row.get("faceVal") or "").strip() or None,
            )
        )
    return actions


def observed_ratio(
    conn: sqlite3.Connection, isin: str, ex_date: str, *, exchange: str = "NSE"
) -> float | None:
    """``close(ex_date) / close(previous traded session)`` for one security.

    **A face-value split issues a new ISIN**, so on and after the ex-date the
    security trades under a different instrument code: measured 2026-08-14, all
    174 splits in the window had no row under their announced ISIN on the
    ex-date, and 143 traded under a sibling code sharing the issuer prefix.
    The post-action price is therefore looked up by issuer prefix (ISIN chars
    1-9) when the exact code is absent -- the same identity rule the delisting
    work arrived at, for the same reason.
    """
    prefix = isin[:9]

    # Both sides are resolved by ISSUER, never by the announced instrument code.
    # The feed keeps quoting an issuer's original ISIN indefinitely: NESTLEIND's
    # 2025-08-08 bonus is still announced under INE239A01016, retired by its
    # January-2024 split, while the shares trade as INE239A01024.  Reading the
    # prior close under the announced code therefore picked a price from before
    # the split and reported a 0.04 ratio for a 1:1 bonus.
    prior = conn.execute(
        """
        SELECT close FROM daily_prices
        WHERE exchange = ? AND substr(isin, 1, 9) = ? AND session < ? AND close > 0
        ORDER BY session DESC, turnover DESC LIMIT 1
        """,
        (exchange, prefix, ex_date),
    ).fetchone()
    if prior is None or not prior[0]:
        return None

    # Highest turnover on the day: an issuer can briefly carry more than one
    # line (partly-paid, post-split successor), and the main listing is the one
    # whose price the announced ratio describes.
    row = conn.execute(
        """
        SELECT close FROM daily_prices
        WHERE exchange = ? AND substr(isin, 1, 9) = ? AND session = ? AND close > 0
        ORDER BY turnover DESC LIMIT 1
        """,
        (exchange, prefix, ex_date),
    ).fetchone()
    if row is None or not row[0]:
        return None
    return row[0] / prior[0]


def validate_against_prices(
    conn: sqlite3.Connection, actions: Iterable[CorporateAction], *, exchange: str = "NSE"
) -> list[CorporateAction]:
    """Attach the observed price ratio and an agreement verdict to each action.

    Actions are validated as a **group per issuer and ex-date**, not one at a
    time.  A company routinely runs a bonus and a face-value split on the same
    ex-date, and the price adjusts once for their combined effect: AHCL's
    2026-04-24 bonus (0.50) and split (0.20) multiply to 0.10 against an
    observed 0.11, while each looked badly wrong on its own.  Checking them
    individually manufactures disagreements that are really arithmetic.

    Grouping is by issuer prefix because a face-value split changes the ISIN, so
    the bonus and the split on the same day can be announced under different
    instrument codes.

    Only share-count actions carry a predicted ratio.  ``NO_PRICE`` means the
    security did not trade on the ex-date in our panel -- information about
    coverage, not about the action.
    """
    actions = list(actions)
    groups: dict[tuple[str, str], list[CorporateAction]] = {}
    for action in actions:
        if action.kind in PRICE_SCALING_KINDS and action.announced_ratio is not None:
            groups.setdefault((action.isin[:9], action.ex_date), []).append(action)

    verdicts: dict[int, tuple[float | None, str]] = {}
    for (_prefix, ex_date), members in groups.items():
        combined = 1.0
        for member in members:
            combined *= member.announced_ratio  # type: ignore[operator]
        # Any member's ISIN resolves the same issuer; use the one that trades.
        seen = None
        for member in members:
            seen = observed_ratio(conn, member.isin, ex_date, exchange=exchange)
            if seen is not None:
                break
        if seen is None:
            verdict = "NO_PRICE"
        elif abs(seen - combined) <= VALIDATION_TOLERANCE:
            verdict = "AGREE"
        else:
            verdict = "DISAGREE"
        for member in members:
            verdicts[id(member)] = (seen, verdict)

    checked: list[CorporateAction] = []
    for action in actions:
        seen, verdict = verdicts.get(id(action), (None, "NOT_APPLICABLE"))
        checked.append(
            CorporateAction(
                **{**action.__dict__, "observed_ratio": seen, "validation": verdict}
            )
        )
    return checked


def store_actions(conn: sqlite3.Connection, actions: Iterable[CorporateAction]) -> int:
    ensure_schema(conn)
    payload = [
        (
            a.isin, a.ex_date, a.subject, a.kind, a.announced_ratio,
            a.symbol, a.series, a.face_value, a.observed_ratio, a.validation,
        )
        for a in actions
    ]
    with conn:
        conn.executemany(
            """
            INSERT OR REPLACE INTO corporate_actions
                (isin, ex_date, subject, kind, announced_ratio,
                 symbol, series, face_value, observed_ratio, validation)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            payload,
        )
    return len(payload)


def adjustment_factors(conn: sqlite3.Connection, isin: str) -> list[tuple[str, float]]:
    """Ex-dates and ratios that rescale one security's price series.

    Only share-count actions are returned.  Dividends are excluded: they are a
    cash payment rather than a rescaling, so applying them here would confuse a
    price series with a total-return series.

    Keyed on the **issuer prefix**, because the announcement feed keeps quoting
    an issuer's original ISIN long after a split has retired it, so matching the
    full code would silently find nothing.  Only actions whose announced ratio
    was confirmed by the observed price move are applied -- an unconfirmed ratio
    is exactly the thing that would fabricate a return.
    """
    placeholders = ",".join("?" for _ in PRICE_SCALING_KINDS)
    rows = conn.execute(
        f"""
        SELECT ex_date, announced_ratio FROM corporate_actions
        WHERE substr(isin, 1, 9) = substr(?, 1, 9)
          AND announced_ratio IS NOT NULL
          AND kind IN ({placeholders})
          AND validation = 'AGREE'
        ORDER BY ex_date
        """,
        (isin, *PRICE_SCALING_KINDS),
    ).fetchall()
    return [(row[0], row[1]) for row in rows]


def _back_adjust(
    closes: list[tuple[str, float]], actions: list[tuple[str, float]]
) -> list[tuple[str, float]]:
    """Express every close on the latest share basis.

    A price before an ex-date is multiplied by the ratio of every action at or
    after it, so any two points are directly comparable and a 20-session return
    spanning a split is the return a holder actually experienced.
    """
    out: list[tuple[str, float]] = []
    for session, close in closes:
        factor = 1.0
        for ex_date, ratio in actions:
            if ex_date > session:
                factor *= ratio
        out.append((session, close * factor))
    return out


def adjusted_close_series(
    conn: sqlite3.Connection,
    isin: str,
    start: date | str,
    end: date | str,
    *,
    exchange: str = "NSE",
) -> list[tuple[str, float]]:
    """Back-adjusted closes for one **instrument**.

    Scoped to a single ISIN, so it stops at a face-value change.  For a study
    series that must survive one, use `adjusted_close_series_by_issuer`.
    """
    start_s = start.isoformat() if isinstance(start, date) else start
    end_s = end.isoformat() if isinstance(end, date) else end

    closes = conn.execute(
        """
        SELECT session, close FROM daily_prices
        WHERE exchange = ? AND isin = ? AND session BETWEEN ? AND ? AND close > 0
        ORDER BY session
        """,
        (exchange, isin, start_s, end_s),
    ).fetchall()
    return _back_adjust(
        [(row[0], row[1]) for row in closes], adjustment_factors(conn, isin)
    )


def adjusted_close_series_by_issuer(
    conn: sqlite3.Connection,
    isin: str,
    start: date | str,
    end: date | str,
    *,
    exchange: str = "NSE",
    column: str = "close",
) -> list[tuple[str, float]]:
    """Back-adjusted prices for an **issuer**, across any ISIN change.

    `column` selects which price is adjusted -- "close" for measuring a
    session's move, "open" for a fill, since the charter's clock fills at the
    next session's open and never at a known close.

    A face-value split retires the old ISIN and issues a new one, so a series
    keyed on the full code truncates at the change and a window spanning it
    returns a partial series with no error.  44 of the 597 cohort issuers carry
    more than one ISIN in the panel, and because only long-lived companies have
    had face-value changes the loss is size- and age-correlated -- the same
    shape of defect the delisting labels, the corporate-action detector and the
    cohort rebuild each hit independently.

    Keying on the issuer prefix also matches `adjustment_factors`, which was
    already prefix-keyed; the two halves of the old function disagreed.

    The exchange retires one line the day it lists the other, so in practice
    there is no overlap.  Where one appears anyway the more heavily traded line
    wins, because that is the instrument the market is actually quoting.
    """
    if column not in ("open", "high", "low", "close", "prev_close"):
        raise ValueError(f"Unsupported price column: {column}")
    start_s = start.isoformat() if isinstance(start, date) else start
    end_s = end.isoformat() if isinstance(end, date) else end

    rows = conn.execute(
        f"""
        SELECT session, {column} FROM daily_prices
        WHERE exchange = ? AND substr(isin, 1, 9) = substr(?, 1, 9)
          AND session BETWEEN ? AND ? AND {column} > 0
        GROUP BY session
        HAVING turnover = MAX(turnover)
        ORDER BY session
        """,
        (exchange, isin, start_s, end_s),
    ).fetchall()
    return _back_adjust(
        [(row[0], row[1]) for row in rows], adjustment_factors(conn, isin)
    )
