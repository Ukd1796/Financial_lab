"""Parse NSE-hosted financial-result XBRL into Phase-1 facts.

The parser resolves every fact to an explicit reporting period.  This matters
more than the numbers: NSE result instances carry both the reported quarter
and the same quarter a year earlier, and a fact whose period cannot be proved
would silently invert the seasonal comparison the charter's primary signal is
built on.

Observed defect (see docs/research_log.md): some instances reference base
contexts such as ``OneD`` / ``FourD`` that the document never defines.  When
that happens the facts are returned with ``UNRESOLVED_CONTEXT`` rather than
being assigned to a period by convention.  The charter treats an unprovable
value as a reviewable exception, not something to approximate.
"""

from __future__ import annotations

import statistics
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Any


XBRLI_NS = "http://www.xbrl.org/2003/instance"
XBRLDI_NS = "http://xbrl.org/2006/xbrldi"

PARSER_VERSION = "phase1-xbrl-v1"

VALIDATION_VALID = "VALID"
VALIDATION_UNRESOLVED_CONTEXT = "UNRESOLVED_CONTEXT"
VALIDATION_NO_MATCHING_PERIOD = "NO_MATCHING_PERIOD"
VALIDATION_UNPARSEABLE = "UNPARSEABLE"
VALIDATION_AMBIGUOUS_PERIOD = "AMBIGUOUS_PERIOD"
# Distinct from VALID on purpose: the facts are usable, but the period was
# proved from the values rather than read from a defined context.  Keeping the
# status separate means any result can be re-run with these filings excluded.
VALIDATION_RECOVERED_CONVENTION = "RECOVERED_CONVENTION"

# NSE result instances routinely define several duration contexts carrying
# IDENTICAL dates that differ only by id: ``OneD`` holds the discrete reporting
# period and ``FourD`` the cumulative year-to-date figure.  Measured 2026-08-13
# across the 226 usable filings on disk: ``OneD`` appears in 226 and always
# carries ``basic_eps``; ``FourD`` appears in 190 and also carries it; the
# median FourD/OneD ratio is 2.95 (range -70 to +61).  No other context id ever
# carries a headline EPS.
#
# The declared period does NOT distinguish them -- only the id does.  Before
# this rule the parser matched on period alone, both contexts matched equally,
# and selection fell through to whichever the document defined first.  That
# happened to be ``OneD`` in 226 of 226 files, so the stored values are correct
# -- but by document order, not by rule.  A filer emitting ``FourD`` first would
# have stored a ~3x inflated "quarterly" EPS, and a seasonal surprise built on
# it would be fabricated rather than merely noisy.
_DISCRETE_CONTEXT_IDS = ("OneD",)
_CUMULATIVE_CONTEXT_IDS = ("TwoD", "ThreeD", "FourD")

# Element local-names, in preference order, for each Phase-1 numeric field.
_FIELD_TAGS: dict[str, tuple[str, ...]] = {
    "basic_eps": (
        "BasicEarningsLossPerShareFromContinuingAndDiscontinuedOperations",
        "BasicEarningsLossPerShareFromContinuingOperations",
        "BasicEarningsPerShareAfterExtraordinaryItems",
        "BasicEarningsPerShareBeforeExtraordinaryItems",
    ),
    "diluted_eps": (
        "DilutedEarningsLossPerShareFromContinuingAndDiscontinuedOperations",
        "DilutedEarningsLossPerShareFromContinuingOperations",
        "DilutedEarningsPerShareAfterExtraordinaryItems",
    ),
    "revenue": (
        "RevenueFromOperations",
        "IncomeFromOperations",
    ),
    "operating_profit": (
        "ProfitBeforeInterestTaxDepreciationAndAmortisation",
        "ProfitBeforeExceptionalItemsAndTax",
        "ProfitLossFromOperatingActivitiesBeforeOtherIncomeFinanceCostsAndExceptionalItems",
    ),
    "profit_after_tax": (
        "ProfitLossForPeriod",
        "ProfitLossForPeriodFromContinuingOperations",
        "NetProfitLossForPeriodFromContinuingOperations",
    ),
}


@dataclass(frozen=True)
class XBRLContext:
    context_id: str
    start_date: date | None
    end_date: date | None
    dimensions: tuple[tuple[str, str], ...]

    @property
    def is_dimensional(self) -> bool:
        """True when the context is a segment/breakdown rather than a headline period."""
        return bool(self.dimensions)


@dataclass
class XBRLParseResult:
    facts: dict[str, float | None]
    period_start: date | None
    period_end: date | None
    validation_status: str
    notes: list[str] = field(default_factory=list)
    unresolved_context_refs: tuple[str, ...] = ()

    @property
    def is_usable(self) -> bool:
        return self.validation_status == VALIDATION_VALID


def _local_name(tag: str) -> str:
    return tag.split("}")[-1]


def _parse_iso_date(value: str | None) -> date | None:
    if not value:
        return None
    try:
        return date.fromisoformat(value.strip())
    except ValueError:
        return None


def read_contexts(root: ET.Element) -> dict[str, XBRLContext]:
    """Index every context the instance actually defines."""
    contexts: dict[str, XBRLContext] = {}
    for element in root.iter(f"{{{XBRLI_NS}}}context"):
        context_id = element.get("id")
        if not context_id:
            continue
        period = element.find(f"{{{XBRLI_NS}}}period")
        start = end = None
        if period is not None:
            start = _parse_iso_date(getattr(period.find(f"{{{XBRLI_NS}}}startDate"), "text", None))
            end = _parse_iso_date(getattr(period.find(f"{{{XBRLI_NS}}}endDate"), "text", None))
            if end is None:
                end = _parse_iso_date(getattr(period.find(f"{{{XBRLI_NS}}}instant"), "text", None))
        dimensions = tuple(
            (
                (member.get("dimension") or "").split(":")[-1],
                (member.text or "").split(":")[-1],
            )
            for member in element.iter(f"{{{XBRLDI_NS}}}explicitMember")
        )
        contexts[context_id] = XBRLContext(context_id, start, end, dimensions)
    return contexts


def _collect_candidates(
    root: ET.Element, contexts: dict[str, XBRLContext]
) -> tuple[dict[str, list[tuple[str, str, str]]], set[str]]:
    """Map each field to its (tag, context_ref, raw_value) candidates.

    Also returns the set of context refs used by headline facts but never
    defined by the document.
    """
    wanted = {tag: field_name for field_name, tags in _FIELD_TAGS.items() for tag in tags}
    candidates: dict[str, list[tuple[str, str, str]]] = {name: [] for name in _FIELD_TAGS}
    undefined: set[str] = set()
    for element in root.iter():
        tag = _local_name(element.tag)
        field_name = wanted.get(tag)
        if field_name is None:
            continue
        context_ref = element.get("contextRef")
        text = (element.text or "").strip()
        if not context_ref or not text:
            continue
        if context_ref not in contexts:
            undefined.add(context_ref)
        candidates[field_name].append((tag, context_ref, text))
    return candidates, undefined


def _to_float(value: str) -> float | None:
    try:
        return float(value.replace(",", ""))
    except (TypeError, ValueError):
        return None


def _value_for_context(
    candidates: dict[str, list[tuple[str, str, str]]], field_name: str, context_id: str
) -> float | None:
    """One field's value under one context, honouring the tag preference order."""
    for tag in _FIELD_TAGS[field_name]:
        for candidate_tag, context_ref, raw in candidates[field_name]:
            if candidate_tag != tag or context_ref != context_id:
                continue
            value = _to_float(raw)
            if value is not None:
                return value
    return None


def _contexts_disagree(
    candidates: dict[str, list[tuple[str, str, str]]], contexts: list[XBRLContext]
) -> bool:
    """True when the given contexts report different numbers for any headline field."""
    for field_name in _FIELD_TAGS:
        seen = {
            value
            for value in (
                _value_for_context(candidates, field_name, c.context_id) for c in contexts
            )
            if value is not None
        }
        if len(seen) > 1:
            return True
    return False


# --- Recovering an undefined OneD/FourD pair -------------------------------
#
# Filings before ~2023 reference bare `OneD` / `FourD` and never define them, so
# the period cannot be read off the document directly.  Guessing "OneD is the
# quarter" is unsafe: a wrong assignment does not add noise, it inverts the
# seasonal surprise.
#
# But the document can *prove* the convention.  The Indian fiscal year runs
# Apr-Mar, so a year-to-date figure at fiscal quarter N spans N quarters.  If
# FourD is cumulative, FourD/OneD tracks N on a large additive flow.  Measured
# 2026-08-18 over 439 such filings: median 1.92 at Q2, 2.89 at Q3, 3.87 at Q4.
#
# The test is DISCRIMINATING, not precise.  Quarters are unequal, so the ratio
# never lands exactly on N; the only question is whether FourD spans more than
# one quarter -- is the ratio nearer N than 1?  That is a wide, robust decision.
# Where it cannot be answered the status stays UNRESOLVED_CONTEXT.
_RATIO_PROBE_TAGS = ("Income", "Expenses", "RevenueFromOperations", "ProfitBeforeTax")
_RATIO_MIN_MAGNITUDE = 1e6
_FISCAL_QUARTER_INDEX = {6: 1, 9: 2, 12: 3, 3: 4}


def _fiscal_quarter_index(period_end: date | None) -> int | None:
    return _FISCAL_QUARTER_INDEX.get(period_end.month) if period_end else None


def resolve_undefined_period_convention(
    root: ET.Element, period_end: date | None
) -> tuple[str | None, list[str]]:
    """Which undefined context holds the discrete quarter, proved from the values.

    Returns the context id to treat as the quarter, or None when the document
    cannot settle it.  Never assumes; a filing that fails the test keeps its
    UNRESOLVED_CONTEXT status.
    """
    quarter_index = _fiscal_quarter_index(period_end)
    if quarter_index is None:
        return None, ["Period end is not a standard Indian fiscal quarter end"]
    if quarter_index == 1:
        # Q1 year-to-date IS the quarter, so the ratio is ~1 either way.  The
        # test cannot discriminate -- but neither can the assignment change any
        # value, so taking the discrete-named context is harmless here.
        return "OneD", ["Q1: year-to-date equals the quarter, assignment is value-neutral"]

    paired: dict[str, dict[str, float]] = {}
    for element in root.iter():
        ref = element.get("contextRef")
        if ref not in ("OneD", "FourD"):
            continue
        name = _local_name(element.tag)
        if name not in _RATIO_PROBE_TAGS:
            continue
        value = _to_float((element.text or "").strip())
        if value is not None:
            paired.setdefault(name, {})[ref] = value

    ratios = [
        pair["FourD"] / pair["OneD"]
        for pair in paired.values()
        if "OneD" in pair and "FourD" in pair and abs(pair["OneD"]) > _RATIO_MIN_MAGNITUDE
    ]
    if not ratios:
        return None, ["No comparable OneD/FourD flow pair; convention cannot be proved"]

    observed = statistics.median(ratios)
    if abs(observed - quarter_index) < abs(observed - 1.0):
        return "OneD", [
            f"FourD/OneD = {observed:.2f} against {quarter_index} year-to-date quarters: "
            "FourD is cumulative, OneD is the discrete quarter (proved from the document)"
        ]
    return None, [
        f"FourD/OneD = {observed:.2f} is nearer 1 than {quarter_index}; the periods "
        "cannot be told apart from the values"
    ]


def _select_period_context(
    pool: list[XBRLContext],
    candidates: dict[str, list[tuple[str, str, str]]],
    notes: list[str],
) -> XBRLContext | None:
    """Pick the discrete reporting period from contexts sharing the same dates.

    Returns ``None`` when the choice cannot be justified, which the caller turns
    into ``AMBIGUOUS_PERIOD``.  Selection is never left to document order: see
    :data:`_DISCRETE_CONTEXT_IDS`.
    """
    if len(pool) == 1:
        return pool[0]

    discrete = [c for c in pool if c.context_id in _DISCRETE_CONTEXT_IDS]
    if len(discrete) == 1:
        notes.append(
            f"{len(pool)} contexts share the reported period; selected "
            f"'{discrete[0].context_id}' as the discrete period by NSE naming convention"
        )
        return discrete[0]

    remaining = [c for c in pool if c.context_id not in _CUMULATIVE_CONTEXT_IDS]
    if len(remaining) == 1:
        notes.append(
            f"{len(pool)} contexts share the reported period; excluded known "
            f"cumulative contexts and selected '{remaining[0].context_id}'"
        )
        return remaining[0]

    # No convention resolves it.  Identical numbers make the choice harmless;
    # differing numbers mean picking one would invent a fact.
    contenders = remaining or pool
    if not _contexts_disagree(candidates, contenders):
        chosen = min(contenders, key=lambda c: c.context_id)
        notes.append(
            f"{len(pool)} contexts share the reported period but report identical "
            f"values; selected '{chosen.context_id}' deterministically"
        )
        return chosen

    notes.append(
        "Multiple contexts share the reported period and report different values "
        f"({', '.join(sorted(c.context_id for c in contenders))}); the discrete "
        "period cannot be proved from the filing"
    )
    return None


def parse_result_xbrl(
    source: str | Path | bytes,
    *,
    expected_period_start: date | None = None,
    expected_period_end: date | None = None,
    resolve_conventions: bool = False,
) -> XBRLParseResult:
    """Extract Phase-1 facts for one reporting period from an XBRL instance.

    ``expected_period_start``/``expected_period_end`` come from the NSE filing
    index (``fromDate``/``toDate``).  They select the reported quarter among the
    several periods an instance contains; they are never used to relabel a fact
    whose own context is missing.

    ``resolve_conventions`` opts in to recovering an undefined ``OneD``/``FourD``
    pair from the values (see
    :func:`resolve_undefined_period_convention`).  Off by default so the strict
    reading stays the default, and so a corpus is never half-parsed under two
    rules by accident.
    """
    try:
        if isinstance(source, bytes):
            root = ET.fromstring(source)
        else:
            root = ET.parse(str(source)).getroot()
    except ET.ParseError as exc:
        return XBRLParseResult(
            facts={name: None for name in _FIELD_TAGS},
            period_start=None,
            period_end=None,
            validation_status=VALIDATION_UNPARSEABLE,
            notes=[f"XBRL could not be parsed: {exc}"],
        )

    contexts = read_contexts(root)
    candidates, undefined_refs = _collect_candidates(root, contexts)
    notes: list[str] = []

    # Headline periods are the non-dimensional durations; segment breakdowns
    # share the same dates and must not be mistaken for the headline figure.
    durations = [
        context for context in contexts.values()
        if not context.is_dimensional and context.start_date and context.end_date
    ]

    # Every context sharing the reported period is a candidate, not just the
    # first one found: NSE defines the quarter and the year-to-date figure with
    # identical dates, so "the first match" is not a selection rule at all.
    pool: list[XBRLContext] = []
    if expected_period_start and expected_period_end:
        pool = [
            c for c in durations
            if c.start_date == expected_period_start and c.end_date == expected_period_end
        ]
    if not pool and durations:
        # Fall back to the most recent period the document defines -- and take
        # every context declaring it, so the tie is resolved by rule below.
        latest = max((c.end_date, c.start_date) for c in durations)
        pool = [c for c in durations if (c.end_date, c.start_date) == latest]
        notes.append(
            f"Reported period not matched exactly; used the latest defined period "
            f"{latest[1]}..{latest[0]}"
        )

    ambiguous = False
    chosen: XBRLContext | None = None
    if pool:
        chosen = _select_period_context(pool, candidates, notes)
        ambiguous = chosen is None

    if chosen is None:
        if ambiguous:
            # `_select_period_context` already recorded which contexts collided.
            status = VALIDATION_AMBIGUOUS_PERIOD
        elif undefined_refs:
            recovered, why = (
                resolve_undefined_period_convention(root, expected_period_end)
                if resolve_conventions else (None, [])
            )
            if recovered and recovered in undefined_refs:
                notes.extend(why)
                notes.append(
                    f"Recovered '{recovered}' as the discrete period; the document "
                    "never defines it, so the period is proved from the values, not read"
                )
                facts = {
                    name: _value_for_context(candidates, name, recovered)
                    for name in _FIELD_TAGS
                }
                return XBRLParseResult(
                    facts=facts,
                    period_start=expected_period_start,
                    period_end=expected_period_end,
                    validation_status=VALIDATION_RECOVERED_CONVENTION,
                    notes=notes,
                )
            status = VALIDATION_UNRESOLVED_CONTEXT
            notes.extend(why)
            notes.append(
                "Headline facts reference contexts the document never defines "
                f"({', '.join(sorted(undefined_refs))}); period cannot be proved from the filing"
            )
        else:
            status = VALIDATION_NO_MATCHING_PERIOD
            notes.append("No non-dimensional duration context was defined")
        return XBRLParseResult(
            facts={name: None for name in _FIELD_TAGS},
            period_start=None,
            period_end=None,
            validation_status=status,
            notes=notes,
            unresolved_context_refs=tuple(sorted(undefined_refs)),
        )

    # Tag order encodes preference: the most specific concept wins.
    facts: dict[str, float | None] = {
        field_name: _value_for_context(candidates, field_name, chosen.context_id)
        for field_name in _FIELD_TAGS
    }

    status = VALIDATION_VALID
    if undefined_refs:
        # The document defined a usable period, but some headline facts still
        # point at contexts that do not exist. Those values are not trusted.
        status = VALIDATION_UNRESOLVED_CONTEXT
        notes.append(
            "Some headline facts reference undefined contexts "
            f"({', '.join(sorted(undefined_refs))}); affected values were not used"
        )
    elif facts.get("basic_eps") is None:
        notes.append("basic_eps absent for the reported period")

    return XBRLParseResult(
        facts=facts,
        period_start=chosen.start_date,
        period_end=chosen.end_date,
        validation_status=status,
        notes=notes,
        unresolved_context_refs=tuple(sorted(undefined_refs)),
    )


def to_fact_payload(result: XBRLParseResult, *, reporting_scope: str, is_cumulative: bool,
                    audit_status: str, currency: str = "INR",
                    unit_scale: str = "UNKNOWN") -> dict[str, Any]:
    """Shape a parse result into the repository's fact fields."""
    return {
        "reporting_scope": reporting_scope,
        "is_cumulative": is_cumulative,
        "audit_status": audit_status.upper(),
        "basic_eps": result.facts.get("basic_eps"),
        "diluted_eps": result.facts.get("diluted_eps"),
        "revenue": result.facts.get("revenue"),
        "operating_profit": result.facts.get("operating_profit"),
        "profit_after_tax": result.facts.get("profit_after_tax"),
        "currency": currency.upper(),
        "unit_scale": unit_scale.upper(),
        "parser_version": PARSER_VERSION,
        "validation_status": result.validation_status,
        "validation_notes": "; ".join(result.notes) or None,
    }
