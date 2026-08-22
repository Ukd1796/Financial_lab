"""Budget-enforcing HTTP client for indianapi.in.

A quota is spent permanently and cannot be refunded by fixing a bug afterwards,
so this client is built around three guarantees rather than convenience:

**A cached response costs nothing.**  Every payload is written to disk
content-addressed and keyed by ``(endpoint, params)``.  Re-running a report,
re-parsing a vocabulary, or restarting an interrupted backfill reads from disk
and never touches the network.  The only unrecoverable thing is a call that was
not made at a moment that has now passed.

**The cap is refused, not truncated.**  A run that would exceed its budget
raises :class:`BudgetExhausted` before the request is made.  Silently stopping
early would leave a half-filled store that looks complete.

**Every call is ledgered.**  Billed calls are counted per monthly period, and
that count is what should reconcile against the provider dashboard.  A drift
means requests are escaping this client — the failure mode that quietly drains
a quota.

The provider allows one request per second; the pacing floor here is slightly
above that so clock jitter cannot produce a 429.
"""

from __future__ import annotations

import hashlib
import json
import os
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from app.analysis.database import raw_dir
from app.analysis.repository import AnalysisRepository, budget_period


BASE_URL = "https://stock.indianapi.in"
API_KEY_ENV = "INDIAN_API_KEY"
BUDGET_ENV = "INDIAN_API_CALL_BUDGET"

# The provider documents 1 req/sec on both the free and hobby plans.  The extra
# 50ms absorbs clock jitter so pacing never trips a 429, which would cost a call
# and return nothing.
MIN_REQUEST_INTERVAL_SECONDS = 1.05

# Conservative default: the free tier's monthly allowance.  Raise it explicitly
# via INDIAN_API_CALL_BUDGET when on a paid plan, so an unset environment can
# never spend more than the smallest plan permits.
DEFAULT_CALL_BUDGET = 500

FAILURE_HTTP = "HTTP_ERROR"
FAILURE_TRANSPORT = "TRANSPORT_ERROR"
FAILURE_DECODE = "DECODE_ERROR"
FAILURE_EMPTY = "EMPTY_PAYLOAD"


class MissingAPIKey(RuntimeError):
    """Raised when the client is used without credentials."""


class BudgetExhausted(RuntimeError):
    """Raised before a call that would exceed the configured cap."""


class APIError(RuntimeError):
    """A call reached the provider and did not return a usable payload."""

    def __init__(self, message: str, *, failure_type: str, http_status: int | None = None):
        super().__init__(message)
        self.failure_type = failure_type
        self.http_status = http_status


def cache_key(endpoint: str, params: dict[str, Any]) -> str:
    """Stable identity for a request, independent of parameter ordering."""
    canonical = json.dumps(
        {"endpoint": endpoint, "params": {k: str(v) for k, v in sorted(params.items())}},
        sort_keys=True,
    )
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


@dataclass
class IndianAPIClient:
    """Paced, cached, ledgered access to indianapi.in.

    ``budget`` is the cap for the current monthly period, counted against calls
    already recorded in the ledger — so the limit survives process restarts
    rather than resetting with each run.
    """

    api_key: str | None = None
    base_url: str = BASE_URL
    budget: int | None = None
    timeout_seconds: float = 30.0
    min_interval_seconds: float = MIN_REQUEST_INTERVAL_SECONDS
    repository: AnalysisRepository | None = None
    cache_dir: Path | None = None
    # Set for planning runs: any cache miss raises instead of spending.
    dry_run: bool = False

    _last_request_at: float = field(default=0.0, init=False, repr=False)
    _session: Any = field(default=None, init=False, repr=False)
    planned: list[tuple[str, dict[str, Any]]] = field(default_factory=list, init=False)

    def __post_init__(self) -> None:
        self.api_key = self.api_key or os.environ.get(API_KEY_ENV)
        self.repository = self.repository or AnalysisRepository()
        self.cache_dir = Path(self.cache_dir) if self.cache_dir else raw_dir()
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        if self.budget is None:
            self.budget = int(os.environ.get(BUDGET_ENV, DEFAULT_CALL_BUDGET))

    # ------------------------------------------------------------------ budget

    def spent(self) -> int:
        return self.repository.calls_spent()

    def remaining(self) -> int:
        return max(0, int(self.budget) - self.spent())

    def _require_key(self) -> str:
        if not self.api_key:
            raise MissingAPIKey(
                f"set {API_KEY_ENV} in .env to query indianapi.in; "
                "the key is never written to the ledger or the raw store"
            )
        return self.api_key

    # ------------------------------------------------------------------- cache

    def _cache_path(self, key: str) -> Path:
        return self.cache_dir / f"{key}.json"

    def cached(self, endpoint: str, params: dict[str, Any]) -> Any | None:
        path = self._cache_path(cache_key(endpoint, params))
        if not path.exists():
            return None
        try:
            return json.loads(path.read_text())
        except json.JSONDecodeError:
            # A truncated file (killed mid-write) must not masquerade as a hit,
            # or the payload is lost until someone notices the parse failure.
            return None

    # ----------------------------------------------------------------- request

    def _pace(self) -> None:
        elapsed = time.monotonic() - self._last_request_at
        if self._last_request_at and elapsed < self.min_interval_seconds:
            time.sleep(self.min_interval_seconds - elapsed)
        self._last_request_at = time.monotonic()

    def _ensure_session(self):
        import requests

        if self._session is None:
            self._session = requests.Session()
        return self._session

    def get(
        self, endpoint: str, params: dict[str, Any] | None = None, *, refresh: bool = False
    ) -> tuple[Any, bool, str]:
        """Fetch one endpoint.

        Returns ``(payload, from_cache, sha256)``.  Raises :class:`APIError` on
        anything that reached the provider without yielding a usable payload —
        callers turn that into an ``ingestion_exception`` row so the failure is
        recorded rather than dropped.
        """
        params = dict(params or {})
        key = cache_key(endpoint, params)
        path = self._cache_path(key)

        if not refresh:
            hit = self.cached(endpoint, params)
            if hit is not None:
                self.repository.record_call(
                    endpoint=endpoint,
                    params=params,
                    http_status=200,
                    response_sha256=_sha256_file(path),
                    response_bytes=path.stat().st_size,
                    cache_hit=True,
                )
                return hit, True, _sha256_file(path)

        if self.dry_run:
            self.planned.append((endpoint, params))
            raise BudgetExhausted(
                f"dry run: {endpoint} {params} is a cache miss and would spend a call"
            )

        if self.remaining() <= 0:
            raise BudgetExhausted(
                f"call budget exhausted for {budget_period()}: "
                f"{self.spent()} of {self.budget} spent. "
                f"Raise {BUDGET_ENV} only if the plan genuinely allows it."
            )

        key_value = self._require_key()
        self._pace()

        import requests

        try:
            response = self._ensure_session().get(
                f"{self.base_url}{endpoint}",
                params=params,
                headers={"X-Api-Key": key_value, "Accept": "application/json"},
                timeout=self.timeout_seconds,
            )
        except requests.RequestException as exc:
            # A call that never reached the provider still gets a ledger row —
            # without it, the ledger and the dashboard drift for the wrong reason.
            self.repository.record_call(
                endpoint=endpoint, params=params, error=f"{type(exc).__name__}: {exc}"
            )
            raise APIError(str(exc), failure_type=FAILURE_TRANSPORT) from exc

        body = response.content
        digest = hashlib.sha256(body).hexdigest()
        self.repository.record_call(
            endpoint=endpoint,
            params=params,
            http_status=response.status_code,
            response_sha256=digest,
            response_bytes=len(body),
            cache_hit=False,
            error=None if response.ok else response.text[:500],
        )

        if not response.ok:
            raise APIError(
                f"HTTP {response.status_code} for {endpoint} {params}",
                failure_type=FAILURE_HTTP,
                http_status=response.status_code,
            )

        try:
            payload = response.json()
        except ValueError as exc:
            raise APIError(
                f"non-JSON response for {endpoint} {params}",
                failure_type=FAILURE_DECODE,
                http_status=response.status_code,
            ) from exc

        # Written only after a successful decode, so a cache file always holds a
        # payload that parses.
        path.write_text(json.dumps(payload, indent=1, sort_keys=True))
        return payload, False, digest


def _sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()
