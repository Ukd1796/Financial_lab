"""Frozen-rule feature computation for the V2 earnings-response sleeve.

Everything here implements a rule that charter v3 fixed **before any return
existed**.  Nothing in this module chooses a parameter; where a number appears
it is quoted from the charter and the section is named.

The functions are deliberately pure -- they take resolved inputs and return
values -- so the rules can be tested without a database, a network call or a
price panel.  `scripts/event_research/build_event_features.py` is the only
place that does I/O.

Charter references:
  §2  the causal clock (dissemination -> reaction -> entry -> exit)
  §3  the seasonal EPS surprise and the initial response
  v3 §1  the peer-basket benchmark
  v3 §3  the cost model and the participation cap
  v3 §4  book size and the minimum sample
"""

from __future__ import annotations

import math
import statistics
from bisect import bisect_right
from dataclasses import dataclass
from datetime import date, datetime, time
from zoneinfo import ZoneInfo

IST = ZoneInfo("Asia/Kolkata")

# NSE's continuous session opens at 09:15 IST.  A filing disseminated at 09:00
# and one disseminated at 18:00 are treated differently only in which session
# counts as the first to *begin* after it -- charter §2's universal one-session
# reaction delay does the rest.
NSE_OPEN = time(9, 15)

FEATURE_VERSION = "v1-hybrid"
CHARTER_VERSION = "v3"

HOLDING_SESSIONS = 20          # charter §3.4 primary horizon
PEER_BASKET_SIZE = 20          # charter v3 §1
BOOK_SIZE = 40                 # charter v3 §4
MIN_EVENTS_PER_QUARTER = 15    # charter v3 §4
MIN_QUARTERS_PER_FOLD = 4      # charter v3 §4

# Charter v3 §3.  Applied once, at aggregation, so the model lives in one place.
ROUND_TRIP_COST = 0.0055
PASS_BAR = 2 * ROUND_TRIP_COST

# Charter v3 §3's participation cap needs a book notional to be expressible as
# a rupee position.  A Rs 10 crore sleeve over 40 equal positions is Rs 25 lakh
# each; against the cohort's minimum 60-session traded value (~Rs 70 crore/day)
# that is a 0.36% participation rate, comfortably inside the 1% cap.
BOOK_NOTIONAL_INR = 10_00_00_000
MAX_PARTICIPATION = 0.01

# The hybrid standardisation the operator chose on 2026-08-17: use the issuer's
# own seasonal history when there is enough of it, otherwise standardise against
# the quarter's cross-section.  Recorded consequence: fold A can reach at most 4
# prior differences and fold B reaches 5-8, so the folds resolve to different
# methods and §7 condition 2 compares them.  Both values are stored on every
# event so that confound stays measurable rather than hidden.
MIN_TIME_SERIES_HISTORY = 4

METHOD_TIME_SERIES = "TIME_SERIES"
METHOD_CROSS_SECTIONAL = "CROSS_SECTIONAL"


# --------------------------------------------------------------------------
# The causal clock (charter §2)
# --------------------------------------------------------------------------

@dataclass(frozen=True)
class EventClock:
    """Resolved sessions for one event.

    Stored rather than derived at read time: a later calendar correction must
    not be able to move an entry that was already recorded.
    """

    prior_session: date      # the close the reaction is measured against
    reaction_session: date   # first full session beginning after available_at
    entry_session: date      # fill at this session's open, never at a known close
    exit_session: date


def resolve_clock(
    available_at: datetime,
    sessions: list[date],
    *,
    horizon: int = HOLDING_SESSIONS,
) -> EventClock | None:
    """Walk charter §2's clock, or return None if the calendar runs out.

    `sessions` must be the exchange's own recorded trading days in order.
    Deriving them from weekdays is wrong -- NSE holds Budget, Muhurat and
    disaster-recovery sessions on weekends, and missing one corrupts both the
    length of an N-session window and the prior-close reference.

    The reaction session is the first that *begins* strictly after
    dissemination, so a filing released mid-session does not get credit for
    that session's move.
    """
    if available_at.tzinfo is None:
        raise ValueError("available_at must be timezone-aware; never infer the offset")
    available_ist = available_at.astimezone(IST)

    # The first session whose opening bell is after dissemination.
    index = bisect_right(
        sessions,
        available_ist,
        key=lambda session: datetime.combine(session, NSE_OPEN, tzinfo=IST),
    )
    if index == 0 or index >= len(sessions):
        # index 0 means the filing predates the panel: there is no prior close
        # to measure the reaction against.
        return None

    reaction_index = index
    entry_index = reaction_index + 1
    exit_index = entry_index + horizon
    if exit_index >= len(sessions):
        return None

    return EventClock(
        prior_session=sessions[reaction_index - 1],
        reaction_session=sessions[reaction_index],
        entry_session=sessions[entry_index],
        exit_session=sessions[exit_index],
    )


# --------------------------------------------------------------------------
# The seasonal surprise (charter §3.2)
# --------------------------------------------------------------------------

def seasonal_difference(eps_current: float, eps_year_ago: float) -> float:
    """EPS less the same fiscal quarter one year earlier.

    No filing in the clean era defines a prior-year duration context (226 of
    226 checked), so `eps_year_ago` can only come from a second, separately
    ingested filing -- which is why the caller stores `prior_event_id`.
    """
    return eps_current - eps_year_ago


def standardise_time_series(
    surprise_raw: float, prior_differences: list[float]
) -> float | None:
    """Standardise against the issuer's own prior seasonal differences.

    Returns None when the history is too short to define a dispersion, which
    is the normal case in fold A: its first quarter has no prior differences at
    all and its best has four.
    """
    if len(prior_differences) < MIN_TIME_SERIES_HISTORY:
        return None
    spread = statistics.pstdev(prior_differences)
    if spread == 0:
        return None
    return (surprise_raw - statistics.mean(prior_differences)) / spread


def standardise_cross_sectional(
    scaled_surprise: float, quarter_scaled_surprises: list[float]
) -> float | None:
    """Standardise against the same quarter's cross-section.

    The input must already be scale-free across issuers -- a rupee EPS change
    is not comparable between a Rs 50 share and a Rs 25,000 share -- so the
    caller divides by price first.  Uses only data from the same quarter, so it
    needs no history and treats every fold identically.
    """
    if len(quarter_scaled_surprises) < 2:
        return None
    spread = statistics.pstdev(quarter_scaled_surprises)
    if spread == 0:
        return None
    return (scaled_surprise - statistics.mean(quarter_scaled_surprises)) / spread


def select_standardisation(
    time_series: float | None, cross_sectional: float | None
) -> tuple[float | None, str | None]:
    """The hybrid rule: the issuer's own history when available, else the cross-section."""
    if time_series is not None:
        return time_series, METHOD_TIME_SERIES
    if cross_sectional is not None:
        return cross_sectional, METHOD_CROSS_SECTIONAL
    return None, None


# --------------------------------------------------------------------------
# The peer basket (charter v3 §1)
# --------------------------------------------------------------------------

def peer_basket(
    target_isin: str,
    candidates: dict[str, float],
    *,
    size: int = PEER_BASKET_SIZE,
) -> list[str]:
    """The `size` cohort members closest to the target by traded value.

    Distance is measured in **log** traded value.  The cohort spans roughly two
    orders of magnitude (Rs 70 crore to Rs 2,500 crore a day), and on a raw
    scale every mid-cap's nearest neighbours would be the same cluster of
    smallest names -- log distance is what "closest traded value" has to mean
    for a size-matched basket.

    `candidates` maps issuer prefix to traded value and must come from the
    dated cohort snapshot, so membership is point-in-time.  The target is
    excluded from its own benchmark.
    """
    target_prefix = target_isin[:9]
    target_value = candidates.get(target_prefix)
    if not target_value or target_value <= 0:
        return []

    target_log = math.log(target_value)
    ranked = sorted(
        (
            (abs(math.log(value) - target_log), prefix)
            for prefix, value in candidates.items()
            if prefix != target_prefix and value and value > 0
        )
    )
    return [prefix for _, prefix in ranked[:size]]


# --------------------------------------------------------------------------
# Returns and admissibility
# --------------------------------------------------------------------------

def simple_return(start_price: float | None, end_price: float | None) -> float | None:
    if not start_price or not end_price or start_price <= 0:
        return None
    return end_price / start_price - 1.0


def equal_weight_mean(values: list[float]) -> float | None:
    usable = [v for v in values if v is not None]
    if not usable:
        return None
    return statistics.mean(usable)


def participation_ok(
    adv_60d: float | None,
    *,
    book_notional: float = BOOK_NOTIONAL_INR,
    book_size: int = BOOK_SIZE,
    cap: float = MAX_PARTICIPATION,
) -> bool | None:
    """Whether one equal-weight position fits inside the ADV participation cap.

    None means the traded value could not be measured, which is not the same as
    a failure and must not be counted as one.
    """
    if not adv_60d or adv_60d <= 0:
        return None
    return (book_notional / book_size) / adv_60d <= cap


# --------------------------------------------------------------------------
# Folds (charter v2 §2, restated in v3 §7)
# --------------------------------------------------------------------------

FOLD_WINDOWS = (
    ("A", date(2023, 7, 1), date(2024, 12, 31)),
    ("B", date(2025, 1, 1), date(2025, 12, 31)),
    ("C", date(2026, 1, 1), date(2099, 12, 31)),
)


def fold_for(session: date) -> str | None:
    """Which fold an event belongs to, assigned from when it became knowable."""
    for label, start, end in FOLD_WINDOWS:
        if start <= session <= end:
            return label
    return None
