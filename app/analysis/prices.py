"""Daily price panel from NSE and BSE bhavcopy — the V2 outcome variable.

Charter §8 is stated in net 20-session sector-adjusted return, so a *daily*
price series for the whole traded universe is the dependent variable of the
entire study.  Nothing downstream is measurable without it.

Why bhavcopy rather than a vendor feed:

* **Point-in-time by construction.** The file published on a date lists what
  traded on that date.  It cannot have been retroactively edited to drop the
  companies that later collapsed -- which is exactly the bias that would make
  an event study look profitable when it is not.
* **Not back-adjusted.** A vendor price series is silently restated for splits
  and bonuses.  Back-adjustment is precisely what corrupts a 20-session event
  window: the response would be measured against a price rewritten after the
  fact.
* **One request per session covers every listed name**, versus one request per
  symbol from a metered vendor.

``PrvsClsgPric`` is stored deliberately.  On a normal session it equals the
previous close; on an ex-date the exchange restates it to the adjusted value.
The disagreement between the two therefore *is* the corporate-action ratio, so
recording it removes the need for a separate corporate-actions feed -- the
identification problem that monthly closes could not solve
(``docs/research_log.md`` 2026-08-12).

The store is append-only per (exchange, session, isin) and safe to resume: a
session already recorded is skipped without a request.
"""

from __future__ import annotations

import csv
import io
import sqlite3
import time
from dataclasses import dataclass, field
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Iterable, Iterator

import requests

from app.event_research.nse_client import (
    NSEDocumentNotFound,
    NSEUnavailable,
    normalise_bhavcopy_row,
)


DEFAULT_DB_PATH = Path("data/analysis/prices.sqlite")

BSE_BHAVCOPY_TEMPLATE = (
    "https://www.bseindia.com/download/BhavCopy/Equity/"
    "BhavCopy_BSE_CM_0_0_0_{ymd}_F_0000.CSV"
)
BSE_REFERER = "https://www.bseindia.com/"

# Measured 2026-08-13 by bisection: the BSE UDiFF archive begins 2024-01-01.
# Ask for 2023-12-29 and BSE answers **HTTP 200 with its HTML landing page** --
# it does not 404.  Requesting BSE before this date is therefore not "missing
# data", it is a request that cannot succeed, and the backfill skips it rather
# than recording false holidays.
BSE_UDIFF_FROM = date(2024, 1, 1)

# The first column of a valid UDiFF CSV.  Used to reject the HTML landing page:
# see BSE_UDIFF_FROM.  Without this check the page parses as CSV and yields
# nonsense rows rather than an error.
_UDIFF_FIRST_COLUMN = "TradDt"

_USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)

STATUS_LOADED = "LOADED"
STATUS_NO_SESSION = "NO_SESSION"
STATUS_FAILED = "FAILED"

# Equity ISINs begin INE.  INF* are mutual-fund and ETF units and are excluded
# from the equity universe for the same reason as in the delisting work: one AMC
# prefix spans dozens of products, which breaks issuer identity.
_EQUITY_ISIN_PREFIX = "INE"

# BSE lists debt and other non-equity instruments in the same file; these series
# codes are not ordinary equity.
_BSE_NON_EQUITY_SERIES = {"F", "G", "GB", "GS", "TB"}


_SCHEMA = """
CREATE TABLE IF NOT EXISTS daily_prices (
    exchange   TEXT NOT NULL,
    session    TEXT NOT NULL,
    isin       TEXT NOT NULL,
    symbol     TEXT NOT NULL,
    series     TEXT,
    open       REAL,
    high       REAL,
    low        REAL,
    close      REAL,
    prev_close REAL,
    volume     REAL,
    turnover   REAL,
    PRIMARY KEY (exchange, session, isin)
) WITHOUT ROWID;

CREATE INDEX IF NOT EXISTS ix_daily_prices_isin_session
    ON daily_prices (isin, session);
CREATE INDEX IF NOT EXISTS ix_daily_prices_session
    ON daily_prices (session);

-- Doubles as the trading calendar and as the resume marker.  Recording
-- NO_SESSION explicitly matters as much as recording the data: without it every
-- re-run re-walks every weekend and holiday.  It is only ever written when the
-- client has exhausted *all* known URL formats, so a schema migration cannot
-- masquerade as a market holiday.
CREATE TABLE IF NOT EXISTS price_sessions (
    exchange   TEXT NOT NULL,
    session    TEXT NOT NULL,
    status     TEXT NOT NULL,
    row_count  INTEGER NOT NULL DEFAULT 0,
    note       TEXT,
    fetched_at TEXT NOT NULL,
    PRIMARY KEY (exchange, session)
) WITHOUT ROWID;
"""


def connect(db_path: Path | str = DEFAULT_DB_PATH) -> sqlite3.Connection:
    path = Path(db_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.executescript(_SCHEMA)
    # A backfill is thousands of bulk inserts; the default sync mode dominates
    # runtime and the file is reproducible from the exchange anyway.
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=NORMAL")
    return conn


def _to_float(value: str | None) -> float | None:
    if value is None:
        return None
    text = str(value).replace(",", "").strip()
    if not text:
        return None
    try:
        return float(text)
    except ValueError:
        return None


def is_equity_isin(isin: str) -> bool:
    return isin.startswith(_EQUITY_ISIN_PREFIX) and len(isin) == 12


@dataclass(frozen=True)
class PriceRow:
    exchange: str
    session: date
    isin: str
    symbol: str
    series: str | None
    open: float | None
    high: float | None
    low: float | None
    close: float | None
    prev_close: float | None
    volume: float | None
    turnover: float | None


def nse_rows_to_prices(rows: Iterable[dict[str, str]], session: date) -> list[PriceRow]:
    """Normalised NSE bhavcopy rows -> price rows (EQ series, equity ISINs only)."""
    out: list[PriceRow] = []
    for row in rows:
        if (row.get("SERIES") or "").strip() != "EQ":
            continue
        isin = (row.get("ISIN") or "").strip()
        if not is_equity_isin(isin):
            continue
        out.append(
            PriceRow(
                exchange="NSE",
                session=session,
                isin=isin,
                symbol=(row.get("SYMBOL") or "").strip(),
                series="EQ",
                open=_to_float(row.get("OPEN")),
                high=_to_float(row.get("HIGH")),
                low=_to_float(row.get("LOW")),
                close=_to_float(row.get("CLOSE")),
                prev_close=_to_float(row.get("PREVCLOSE")),
                volume=_to_float(row.get("TOTTRDQTY")),
                turnover=_to_float(row.get("TOTTRDVAL")),
            )
        )
    return out


def bse_rows_to_prices(rows: Iterable[dict[str, str]], session: date) -> list[PriceRow]:
    """BSE UDiFF rows -> price rows.

    BSE publishes equity and debt in one file under ``FinInstrmTp='STK'``, so
    the instrument type alone does not separate them; the series code does.
    """
    out: list[PriceRow] = []
    for row in rows:
        if (row.get("FinInstrmTp") or "").strip().upper() != "STK":
            continue
        series = (row.get("SctySrs") or "").strip().upper()
        if series in _BSE_NON_EQUITY_SERIES:
            continue
        isin = (row.get("ISIN") or "").strip()
        if not is_equity_isin(isin):
            continue
        out.append(
            PriceRow(
                exchange="BSE",
                session=session,
                isin=isin,
                symbol=(row.get("TckrSymb") or "").strip(),
                series=series,
                open=_to_float(row.get("OpnPric")),
                high=_to_float(row.get("HghPric")),
                low=_to_float(row.get("LwPric")),
                close=_to_float(row.get("ClsPric")),
                prev_close=_to_float(row.get("PrvsClsgPric")),
                volume=_to_float(row.get("TtlTradgVol")),
                turnover=_to_float(row.get("TtlTrfVal")),
            )
        )
    return out


@dataclass
class BSEClient:
    """Paced BSE bhavcopy client.

    BSE serves a plain CSV (NSE serves a zip) and needs no cookie handshake, so
    this is deliberately simpler than :class:`NSEResearchClient` rather than a
    shared abstraction that would fit neither.
    """

    request_delay_seconds: float = 1.0
    timeout_seconds: float = 40.0
    max_attempts: int = 3
    _session: requests.Session | None = field(default=None, init=False, repr=False)
    _last_request_at: float = field(default=0.0, init=False, repr=False)

    def _pace(self) -> None:
        elapsed = time.monotonic() - self._last_request_at
        if elapsed < self.request_delay_seconds:
            time.sleep(self.request_delay_seconds - elapsed)
        self._last_request_at = time.monotonic()

    def _ensure_session(self) -> requests.Session:
        if self._session is None:
            session = requests.Session()
            session.headers.update(
                {"User-Agent": _USER_AGENT, "Accept-Language": "en-US,en;q=0.9"}
            )
            self._session = session
        return self._session

    def fetch_bhavcopy(self, trade_date: date) -> list[dict[str, str]]:
        url = BSE_BHAVCOPY_TEMPLATE.format(ymd=trade_date.strftime("%Y%m%d"))
        session = self._ensure_session()
        last_error: Exception | None = None
        for attempt in range(self.max_attempts):
            self._pace()
            try:
                response = session.get(
                    url, headers={"Referer": BSE_REFERER}, timeout=self.timeout_seconds
                )
            except requests.RequestException as exc:
                last_error = exc
                continue
            if response.status_code == 404:
                raise NSEDocumentNotFound(f"No BSE bhavcopy for {trade_date}")
            if response.status_code != 200:
                last_error = NSEUnavailable(
                    f"BSE returned HTTP {response.status_code} for {trade_date}"
                )
                time.sleep(1.5 * (attempt + 1))
                continue
            text = response.content.decode("utf-8", errors="replace")
            if not text.lstrip().startswith(_UDIFF_FIRST_COLUMN):
                # BSE serves its HTML landing page with HTTP 200 for dates it has
                # no file for.  This is raised as *unavailable*, never as
                # not-found: NSEDocumentNotFound means "the exchange held no
                # session", and letting a landing page claim that would write
                # false holidays into the trading calendar.
                raise NSEUnavailable(
                    f"BSE returned a non-CSV body for {trade_date} "
                    f"(starts {text.lstrip()[:20]!r}); the archive begins {BSE_UDIFF_FROM}"
                )
            return [
                {(k or "").strip(): (v or "").strip() for k, v in row.items()}
                for row in csv.DictReader(io.StringIO(text))
            ]
        raise NSEUnavailable(f"BSE bhavcopy for {trade_date} failed: {last_error}")


def recorded_sessions(conn: sqlite3.Connection, exchange: str) -> set[str]:
    """Sessions already attempted for this exchange -- the resume set."""
    rows = conn.execute(
        "SELECT session FROM price_sessions WHERE exchange = ? AND status IN (?, ?)",
        (exchange, STATUS_LOADED, STATUS_NO_SESSION),
    ).fetchall()
    return {row["session"] for row in rows}


def store_session(
    conn: sqlite3.Connection,
    exchange: str,
    session: date,
    rows: list[PriceRow],
    *,
    status: str = STATUS_LOADED,
    note: str | None = None,
) -> int:
    now = datetime.now(timezone.utc).isoformat()
    with conn:
        if rows:
            conn.executemany(
                """
                INSERT OR REPLACE INTO daily_prices
                    (exchange, session, isin, symbol, series,
                     open, high, low, close, prev_close, volume, turnover)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                [
                    (
                        r.exchange, r.session.isoformat(), r.isin, r.symbol, r.series,
                        r.open, r.high, r.low, r.close, r.prev_close, r.volume, r.turnover,
                    )
                    for r in rows
                ],
            )
        conn.execute(
            """
            INSERT OR REPLACE INTO price_sessions
                (exchange, session, status, row_count, note, fetched_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (exchange, session.isoformat(), status, len(rows), note, now),
        )
    return len(rows)


def daterange(start: date, end: date) -> Iterator[date]:
    from datetime import timedelta

    cursor = start
    while cursor <= end:
        yield cursor
        cursor += timedelta(days=1)


def coverage(conn: sqlite3.Connection) -> list[sqlite3.Row]:
    return conn.execute(
        """
        SELECT exchange,
               status,
               COUNT(*)        AS sessions,
               MIN(session)    AS first_session,
               MAX(session)    AS last_session,
               SUM(row_count)  AS rows_stored
        FROM price_sessions
        GROUP BY exchange, status
        ORDER BY exchange, status
        """
    ).fetchall()
