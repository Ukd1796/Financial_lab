"""Pure validation for manually normalised NSE financial-result filings."""

from __future__ import annotations

import hashlib
import shutil
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Any, Mapping
from urllib.parse import urlparse
from zoneinfo import ZoneInfo


IST = ZoneInfo("Asia/Kolkata")
PARSER_VERSION = "phase1-manual-v1"


@dataclass(frozen=True)
class ValidationResult:
    normalized: dict[str, Any]
    errors: list[str]
    warnings: list[str]

    @property
    def is_valid(self) -> bool:
        return not self.errors


def sha256_file(path: str | Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def archive_raw_filing(raw_file: str | Path, destination_dir: str | Path, source_hash: str) -> Path:
    """Copy an immutable source file to content-addressed research storage."""
    source = Path(raw_file)
    destination = Path(destination_dir) / f"{source_hash}{source.suffix.lower()}"
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists():
        if sha256_file(destination) != source_hash:
            raise ValueError(f"Existing raw archive hash mismatch: {destination}")
        return destination
    shutil.copy2(source, destination)
    if sha256_file(destination) != source_hash:
        destination.unlink(missing_ok=True)
        raise ValueError(f"Raw archive verification failed: {destination}")
    return destination


def _parse_date(value: Any, field: str, errors: list[str]) -> date | None:
    try:
        return date.fromisoformat(str(value))
    except (TypeError, ValueError):
        errors.append(f"{field} must be an ISO date (YYYY-MM-DD)")
        return None


def _parse_timestamp(value: Any, field: str, errors: list[str]) -> datetime | None:
    try:
        parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except (TypeError, ValueError):
        errors.append(f"{field} must be an ISO 8601 timestamp with an offset")
        return None
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        errors.append(f"{field} must include a timezone offset; never infer it from a date")
        return None
    return parsed.astimezone(IST)


def _optional_float(value: Any, field: str, errors: list[str]) -> float | None:
    if value is None or value == "":
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        errors.append(f"{field} must be numeric when supplied")
        return None


def validate_filing_payload(payload: Mapping[str, Any], raw_file: str | Path) -> ValidationResult:
    """Validate an import payload without database or network access.

    The importer accepts normalised numeric facts only after an operator has
    retained the original NSE document.  Missing EPS is a reviewable coverage
    issue, not a reason to silently discard the filing.
    """
    errors: list[str] = []
    warnings: list[str] = []
    event = dict(payload.get("event") or {})
    facts = dict(payload.get("facts") or {})
    raw_path = Path(raw_file)

    if not raw_path.is_file() or raw_path.stat().st_size == 0:
        errors.append("raw_file must be a non-empty original filing saved locally")

    required = ("isin", "nse_symbol", "issuer_name", "result_period_end", "fiscal_quarter",
                "source_url", "source_format", "disseminated_at")
    for field in required:
        if not event.get(field):
            errors.append(f"event.{field} is required")

    source_url = str(event.get("source_url", ""))
    parsed_url = urlparse(source_url)
    if parsed_url.scheme != "https" or not parsed_url.netloc:
        errors.append("event.source_url must be an https URL")
    elif not (parsed_url.hostname or "").endswith("nseindia.com"):
        errors.append("Phase-1 primary source_url must be hosted by NSE India")

    source_exchange = str(event.get("source_exchange", "NSE")).upper()
    if source_exchange != "NSE":
        errors.append("Phase-1 primary imports must use source_exchange=NSE")
    is_revision = event.get("is_revision", False)
    if not isinstance(is_revision, bool):
        errors.append("event.is_revision must be a boolean")
    # `or ""` before str(), not str(... , "") -- a caller that sets the key
    # explicitly to None yields the literal string "None", which is truthy and
    # sends every non-revision into the revision-linking branch downstream.
    # That silently rejected all 3,127 filings of the 2025+ integrated era.
    supersedes_source_sha256 = str(event.get("supersedes_source_sha256") or "")
    if is_revision and len(supersedes_source_sha256) != 64:
        errors.append("a revision must provide event.supersedes_source_sha256")

    period_end = _parse_date(event.get("result_period_end"), "event.result_period_end", errors)
    disseminated_at = _parse_timestamp(event.get("disseminated_at"), "event.disseminated_at", errors)
    received_at = None
    if event.get("received_at"):
        received_at = _parse_timestamp(event["received_at"], "event.received_at", errors)
    if received_at and disseminated_at and received_at > disseminated_at:
        warnings.append("received_at is later than disseminated_at; verify exchange field semantics")
    if period_end and disseminated_at and period_end > disseminated_at.date():
        errors.append("result_period_end cannot be later than dissemination date")

    scope = str(facts.get("reporting_scope", "")).lower()
    if scope not in {"consolidated", "standalone"}:
        errors.append("facts.reporting_scope must be consolidated or standalone")
    if not isinstance(facts.get("is_cumulative"), bool):
        errors.append("facts.is_cumulative must be a boolean")
    if not facts.get("audit_status"):
        errors.append("facts.audit_status is required")

    numeric_fields = ("basic_eps", "diluted_eps", "revenue", "operating_profit", "profit_after_tax")
    normalized_facts = {
        field: _optional_float(facts.get(field), f"facts.{field}", errors)
        for field in numeric_fields
    }
    if normalized_facts["basic_eps"] is None:
        warnings.append("basic_eps is missing; event is retained but cannot enter the primary EPS study")

    raw_hash = sha256_file(raw_path) if raw_path.is_file() and raw_path.stat().st_size else ""
    normalized = {
        "event": {
            "isin": str(event.get("isin", "")).upper(),
            "nse_symbol": str(event.get("nse_symbol", "")).upper(),
            "issuer_name": str(event.get("issuer_name", "")).strip(),
            "instrument_valid_from": event.get("instrument_valid_from") or str(period_end or ""),
            "instrument_source_url": event.get("instrument_source_url") or source_url,
            "result_period_end": period_end,
            "fiscal_quarter": str(event.get("fiscal_quarter", "")).upper(),
            "source_exchange": source_exchange,
            "source_url": source_url,
            "source_format": str(event.get("source_format", "")).lower(),
            "received_at": received_at,
            "disseminated_at": disseminated_at,
            "available_at": disseminated_at,
            "is_revision": is_revision,
            "supersedes_source_sha256": supersedes_source_sha256 or None,
            "raw_sha256": raw_hash,
        },
        "facts": {
            "reporting_scope": scope,
            "is_cumulative": facts.get("is_cumulative"),
            "audit_status": str(facts.get("audit_status", "")).upper(),
            **normalized_facts,
            "currency": str(facts.get("currency", "INR")).upper(),
            "unit_scale": str(facts.get("unit_scale", "UNKNOWN")).upper(),
            "parser_version": str(facts.get("parser_version", PARSER_VERSION)),
            "validation_status": "VALID" if not errors else "INVALID",
            "validation_notes": "; ".join(warnings) or None,
        },
    }
    return ValidationResult(normalized=normalized, errors=errors, warnings=warnings)
