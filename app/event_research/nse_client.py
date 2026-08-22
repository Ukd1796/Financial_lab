"""Read-only NSE access for the Phase-1 data audit.

NSE serves its public JSON endpoints only to a session that has first been
issued cookies by the site root, so every request goes through one handshake
and reuses that session.  Requests are deliberately paced: the charter permits
retrieving the original filing, its source URL, its content hash and the
exchange dissemination time for a small pilot cohort, and explicitly does not
permit scraping at production scale.

This module fetches bytes and parses index metadata only.  It computes no
score, forward return, or trading decision.
"""

from __future__ import annotations

import csv
import io
import json
import time
import zipfile
from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Any
from zoneinfo import ZoneInfo

import requests


IST = ZoneInfo("Asia/Kolkata")

BASE = "https://www.nseindia.com"
RESULTS_ENDPOINT = f"{BASE}/api/corporates-financial-results"
RESULTS_REFERER = f"{BASE}/companies-listing/corporate-filings-financial-results"
# SEBI's Integrated Filing regime moved quarterly results off the legacy index,
# which stops carrying them after ~Feb 2025 (docs/research_log.md 2026-08-10).
# This endpoint carries them from there on.  Paginated at 20 rows via `page`,
# and it accepts `symbol`, which turns a whole-market page-walk into one request
# per cohort member.
INTEGRATED_FILING_ENDPOINT = f"{BASE}/api/integrated-filing-results"
INTEGRATED_FILING_PAGE_SIZE = 20
BHAVCOPY_TEMPLATE = (
    "https://nsearchives.nseindia.com/content/historical/EQUITIES/"
    "{year}/{month}/cm{day}{month}{year}bhav.csv.zip"
)
# NSE migrated the end-of-day file to a UDiFF (ISO-20022-style) layout with new
# column names.  Measured 2026-08-12: the legacy path serves 2019 and 2024 but
# 404s from 2025 on; UDiFF 404s in 2019 and serves 2024 onward.  Both answer in
# March 2024, so the cutover is a window rather than an instant.
BHAVCOPY_UDIFF_TEMPLATE = (
    "https://nsearchives.nseindia.com/content/cm/"
    "BhavCopy_NSE_CM_0_0_0_{ymd}_F_0000.csv.zip"
)
# The first date for which UDiFF is tried first.  Before it the legacy file is
# the only one that exists; after it the legacy file disappears.
BHAVCOPY_UDIFF_FROM = date(2024, 1, 1)

# UDiFF column name -> the legacy name the rest of the code already speaks, so a
# format migration stays inside this module.
_UDIFF_COLUMNS = {
    "TckrSymb": "SYMBOL",
    "SctySrs": "SERIES",
    "ISIN": "ISIN",
    "OpnPric": "OPEN",
    "HghPric": "HIGH",
    "LwPric": "LOW",
    "ClsPric": "CLOSE",
    "LastPric": "LAST",
    "PrvsClsgPric": "PREVCLOSE",
    "TtlTradgVol": "TOTTRDQTY",
    "TtlTrfVal": "TOTTRDVAL",
    "TtlNbOfTxsExctd": "TOTALTRADES",
    "TradDt": "TIMESTAMP",
}

_USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)
# NSE reports its filing clock as "30-Jul-2026 17:17:53" in Asia/Kolkata.
_NSE_TIMESTAMP_FORMATS = ("%d-%b-%Y %H:%M:%S", "%d-%b-%Y %H:%M")


class NSEUnavailable(RuntimeError):
    """NSE did not return a usable response; the caller must record an exception."""


class NSEDocumentNotFound(NSEUnavailable):
    """NSE reported that the document does not exist.

    Distinct from a transient failure: an absent bhavcopy means the exchange
    held no session that day, which is information rather than an error.
    """


def normalise_bhavcopy_row(row: dict[str, str]) -> dict[str, str]:
    """Rename UDiFF columns to the legacy names; leave legacy rows untouched.

    Detection is by the presence of ``TckrSymb``, which only the UDiFF layout
    has.  Unmapped UDiFF columns are kept under their original names rather than
    dropped, so a field we have not needed yet is still recoverable.
    """
    if "TckrSymb" not in row:
        return row
    out = {_UDIFF_COLUMNS.get(key, key): value for key, value in row.items()}
    # The legacy file wrote the series padded; downstream compares against "EQ".
    if "SERIES" in out:
        out["SERIES"] = out["SERIES"].strip()
    return out


def normalise_integrated_filing_row(row: dict[str, Any], *, isin: str) -> dict[str, Any]:
    """Rename integrated-filing fields to the legacy result-index names.

    Same containment strategy as :func:`normalise_bhavcopy_row`: an endpoint
    migration stays inside this module and callers keep speaking one schema.

    Two fields the legacy index supplied are genuinely absent here and must not
    be faked:

    * ``fromDate`` -- no period start.  Callers pass only the end date and let
      the parser resolve the period from the document, which is the stronger
      source anyway.
    * ``cumulative`` -- no discrete/cumulative flag.  Defaulting it would be
      actively harmful: the legacy caller reads *anything but* "Non-cumulative"
      as cumulative, so a missing field would silently mark every integrated
      filing cumulative and exclude it from seasonal chaining.  It is left
      absent so the caller must derive it from the parsed period span.

    ``isin`` is supplied by the caller because the record carries only a symbol,
    and symbols are mutable -- resolving identity from the cohort is correct.
    """
    return {
        "isin": isin.upper(),
        "symbol": (row.get("symbol") or "").upper(),
        "companyName": row.get("cmName") or row.get("smName"),
        "toDate": row.get("qe_Date"),
        # A revision leaves `broadcast_Date` null and carries its clock in
        # `revised_Date` instead (measured on LT's 2026-03-31 refilings).  The
        # dissemination timestamp is the charter's causal clock, so falling back
        # is required -- without it a revision has no time and is rejected.
        "exchdisstime": row.get("broadcast_Date") or row.get("revised_Date"),
        "xbrl": row.get("xbrl"),
        "consolidated": row.get("consolidated"),
        "audited": row.get("audited"),
        "relatingTo": None,
        "seqId": row.get("seq_Id"),
        # `type_Sub` carries at least {Original, New, Revised}.  "New" is NOT a
        # revision -- measured 2026-08-14, those rows point at
        # INTEGRATED_FILING_GOVERNANCE documents (no EPS, no revenue) rather
        # than the INDAS financial statement.  Only an explicit revision marker
        # counts, or the ingest would reject every governance row as a revision
        # with no predecessor.
        "isRevision": (row.get("type_Sub") or "").strip().lower().startswith("revis")
        or bool(row.get("revised_Date")),
        # A financial result always declares its reporting scope; the governance
        # filing leaves `consolidated` and `audited` null.  This is the semantic
        # discriminator, preferred over matching on the document URL.
        "isFinancialResult": bool((row.get("consolidated") or "").strip()),
        "revisionRemark": row.get("revision_Remark"),
        "ixbrl": row.get("ixbrl"),
        "pdfAttach": row.get("pdf_attach"),
    }


def parse_nse_timestamp(value: str | None) -> datetime | None:
    """Parse an NSE clock field into an aware Asia/Kolkata timestamp.

    A naive timestamp is never returned: the charter treats an unanchored
    filing time as a hard failure rather than something to infer.
    """
    if not value:
        return None
    text = str(value).strip()
    for fmt in _NSE_TIMESTAMP_FORMATS:
        try:
            return datetime.strptime(text, fmt).replace(tzinfo=IST)
        except ValueError:
            continue
    return None


@dataclass
class NSEResearchClient:
    """Paced, cookie-bearing NSE session for pilot-scale research retrieval."""

    request_delay_seconds: float = 1.5
    # (connect, read), split so a stalled connect fails fast while a slow
    # document still gets time to arrive.  A machine that sleeps mid-run wakes
    # with its sockets dead, and the 36 FETCH_FAILED exceptions recorded on
    # 2026-08-17 are that: a bounded connect turns them into a prompt retry
    # rather than a long wait on a connection that will never answer.
    timeout_seconds: tuple[float, float] = (15.0, 45.0)
    max_attempts: int = 3
    _session: requests.Session | None = field(default=None, init=False, repr=False)
    _last_request_at: float = field(default=0.0, init=False, repr=False)

    def _pace(self) -> None:
        elapsed = time.monotonic() - self._last_request_at
        if elapsed < self.request_delay_seconds:
            time.sleep(self.request_delay_seconds - elapsed)
        self._last_request_at = time.monotonic()

    def _ensure_session(self) -> requests.Session:
        if self._session is not None:
            return self._session
        session = requests.Session()
        session.headers.update({
            "User-Agent": _USER_AGENT,
            "Accept-Language": "en-US,en;q=0.9",
        })
        self._pace()
        # The root request is expected to be refused for content while still
        # setting the cookies the JSON endpoints require, so its status is
        # deliberately not asserted.
        try:
            session.get(BASE, headers={"Accept": "text/html"}, timeout=self.timeout_seconds)
        except requests.RequestException as exc:
            raise NSEUnavailable(f"NSE handshake failed: {exc}") from exc
        self._session = session
        return session

    def reset_session(self) -> None:
        """Drop cookies so the next call performs a fresh handshake."""
        if self._session is not None:
            self._session.close()
        self._session = None

    def _get(self, url: str, *, referer: str, accept: str, params: dict[str, Any] | None = None) -> bytes:
        last_error: str = ""
        for attempt in range(1, self.max_attempts + 1):
            session = self._ensure_session()
            self._pace()
            try:
                response = session.get(
                    url,
                    params=params,
                    headers={"Accept": accept, "Referer": referer},
                    timeout=self.timeout_seconds,
                )
            except requests.RequestException as exc:
                last_error = str(exc)
                # Rebuild the session on a transport failure too, not just on a
                # bad HTTP status.  A pooled keep-alive connection that dies --
                # a laptop suspending, a peer dropping the socket -- is dead for
                # the life of the pool, so without this every later request
                # times out forever and the process never recovers.  Observed
                # 2026-08-18: 27 consecutive 45s read timeouts while the same
                # URLs fetched in 2s from a fresh session.
                self.reset_session()
            else:
                if response.status_code == 200 and response.content:
                    return response.content
                if response.status_code == 404:
                    raise NSEDocumentNotFound(f"{url} does not exist (HTTP 404)")
                if response.status_code == 200:
                    # A 200 carrying nothing is not success, and reporting it as
                    # "HTTP 200" reads like one.  NSE and BSE both answer with a
                    # well-formed 200 when they have no content to give.
                    last_error = "HTTP 200 with an empty body"
                else:
                    last_error = f"HTTP {response.status_code}"
                # An expired or rejected cookie set is the usual cause; a new
                # handshake is the documented recovery.
                self.reset_session()
            if attempt < self.max_attempts:
                time.sleep(self.request_delay_seconds * attempt * 2)
        raise NSEUnavailable(f"{url} unavailable after {self.max_attempts} attempts ({last_error})")

    def fetch_result_index(self, from_date: date, to_date: date, period: str = "Quarterly") -> list[dict[str, Any]]:
        """Return raw result-filing index records disseminated in a date window.

        The window filters on NSE's own dissemination clock, so a filing is
        returned by the period in which the exchange published it, not by the
        financial period it describes.
        """
        payload = self._get(
            RESULTS_ENDPOINT,
            referer=RESULTS_REFERER,
            accept="*/*",
            params={
                "index": "equities",
                "period": period,
                "from_date": from_date.strftime("%d-%m-%Y"),
                "to_date": to_date.strftime("%d-%m-%Y"),
            },
        )
        try:
            records = json.loads(payload)
        except json.JSONDecodeError as exc:
            raise NSEUnavailable(f"Result index was not JSON for {from_date}..{to_date}: {exc}") from exc
        if not isinstance(records, list):
            raise NSEUnavailable(f"Unexpected result-index shape for {from_date}..{to_date}")
        return records

    def fetch_integrated_filing_index(
        self,
        from_date: date,
        to_date: date,
        *,
        symbol: str | None = None,
        max_pages: int = 200,
    ) -> list[dict[str, Any]]:
        """Result filings from the Integrated Filing endpoint, all pages.

        Covers ~Feb 2025 onward, where the legacy index stops carrying bulk
        filings.  Passing ``symbol`` filters server-side, which is the
        difference between one request and a walk over tens of thousands of
        market-wide rows.

        Paging stops when a page returns nothing, returns fewer rows than the
        page size, or repeats the previous page's identifiers -- the last guard
        matters because an endpoint that ignores an unrecognised page parameter
        would otherwise loop forever on page one.
        """
        collected: list[dict[str, Any]] = []
        seen_ids: set[str] = set()
        for page in range(1, max_pages + 1):
            query = (
                f"index=equities"
                f"&from_date={from_date.strftime('%d-%m-%Y')}"
                f"&to_date={to_date.strftime('%d-%m-%Y')}"
                f"&page={page}"
            )
            if symbol:
                query += f"&symbol={symbol}"
            payload = self._get(
                f"{INTEGRATED_FILING_ENDPOINT}?{query}",
                referer=RESULTS_REFERER,
                accept="application/json",
            )
            try:
                body = json.loads(payload)
            except json.JSONDecodeError as exc:
                raise NSEUnavailable(
                    f"Integrated filing index was not JSON for {from_date}..{to_date}: {exc}"
                ) from exc
            rows = body.get("data") if isinstance(body, dict) else body
            if not rows:
                break

            fresh = [r for r in rows if str(r.get("seq_Id")) not in seen_ids]
            if not fresh:
                break
            seen_ids.update(str(r.get("seq_Id")) for r in fresh)
            collected.extend(fresh)

            if len(rows) < INTEGRATED_FILING_PAGE_SIZE:
                break
        return collected

    def fetch_document(self, url: str) -> bytes:
        """Download an original filing document (XBRL or attachment)."""
        return self._get(url, referer=RESULTS_REFERER, accept="*/*")

    def _bhavcopy_urls(self, trade_date: date) -> list[str]:
        """Candidate URLs, likeliest format first, so a hit usually costs one call."""
        legacy = BHAVCOPY_TEMPLATE.format(
            year=trade_date.strftime("%Y"),
            month=trade_date.strftime("%b").upper(),
            day=trade_date.strftime("%d"),
        )
        udiff = BHAVCOPY_UDIFF_TEMPLATE.format(ymd=trade_date.strftime("%Y%m%d"))
        return [udiff, legacy] if trade_date >= BHAVCOPY_UDIFF_FROM else [legacy, udiff]

    def fetch_bhavcopy(self, trade_date: date) -> list[dict[str, str]]:
        """Return one historical end-of-day equity bhavcopy as row dicts.

        This is the point-in-time listing and traded-value record: it contains
        the securities that actually traded that day, including names that were
        later delisted or renamed.

        Two on-disk formats exist (see :data:`BHAVCOPY_UDIFF_FROM`).  Both are
        attempted and UDiFF rows are renamed to the legacy column names, so
        callers see one schema across the cutover.  ``NSEDocumentNotFound`` is
        raised only when **every** candidate 404s — otherwise a format
        migration would be indistinguishable from a market holiday, and a whole
        archive would silently read as "no sessions".
        """
        payload = None
        for url in self._bhavcopy_urls(trade_date):
            try:
                payload = self._get(url, referer=f"{BASE}/", accept="*/*")
                break
            except NSEDocumentNotFound:
                continue
        if payload is None:
            raise NSEDocumentNotFound(f"No bhavcopy published for {trade_date} in any format")

        try:
            archive = zipfile.ZipFile(io.BytesIO(payload))
        except zipfile.BadZipFile as exc:
            raise NSEUnavailable(f"Bhavcopy for {trade_date} was not a zip archive: {exc}") from exc
        name = next((n for n in archive.namelist() if n.lower().endswith(".csv")), None)
        if name is None:
            raise NSEUnavailable(f"Bhavcopy archive for {trade_date} contained no CSV")
        with archive.open(name) as handle:
            text = io.TextIOWrapper(handle, encoding="utf-8", errors="replace")
            rows = [
                {(k or "").strip(): (v or "").strip() for k, v in row.items()}
                for row in csv.DictReader(text)
            ]
        return [normalise_bhavcopy_row(row) for row in rows]
