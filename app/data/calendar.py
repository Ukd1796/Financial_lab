# app/data/calendar.py
#
# NSE trading calendar.
# Source: NSE India official holiday list (published annually).
# Update NSE_HOLIDAYS each year when NSE releases the new list.
#
# Usage:
#   from app.data.calendar import NSECalendar
#   cal = NSECalendar()
#   if not cal.is_trading_day(date.today()):
#       sys.exit(0)

from datetime import date, timedelta

# ---------------------------------------------------------------------------
# NSE exchange holidays (NOT trading days).
# Weekends (Sat/Sun) are handled separately — only add weekday holidays here.
# ---------------------------------------------------------------------------
_NSE_HOLIDAYS: set[date] = {
    # ---- 2025 ----
    date(2025, 1, 26),   # Republic Day
    date(2025, 2, 19),   # Chhatrapati Shivaji Maharaj Jayanti
    date(2025, 3, 14),   # Holi
    date(2025, 3, 31),   # Id-Ul-Fitr (Ramzan Id) — provisional
    date(2025, 4, 10),   # Shri Ram Navami
    date(2025, 4, 14),   # Dr. Baba Saheb Ambedkar Jayanti
    date(2025, 4, 18),   # Good Friday
    date(2025, 5, 1),    # Maharashtra Day
    date(2025, 8, 15),   # Independence Day
    date(2025, 8, 27),   # Ganesh Chaturthi
    date(2025, 10, 2),   # Mahatma Gandhi Jayanti / Dussehra
    date(2025, 10, 20),  # Diwali – Laxmi Puja (provisional)
    date(2025, 10, 21),  # Diwali – Balipratipada (provisional)
    date(2025, 11, 5),   # Prakash Gurpurb Sri Guru Nanak Dev Ji
    date(2025, 12, 25),  # Christmas

    # ---- 2026 ----
    date(2026, 1, 26),   # Republic Day
    date(2026, 3, 2),    # Mahashivratri (provisional)
    date(2026, 3, 20),   # Holi (provisional)
    date(2026, 4, 3),    # Good Friday
    date(2026, 4, 14),   # Dr. Baba Saheb Ambedkar Jayanti
    date(2026, 5, 1),    # Maharashtra Day
    date(2026, 8, 15),   # Independence Day
    date(2026, 10, 2),   # Mahatma Gandhi Jayanti
    date(2026, 12, 25),  # Christmas
    # Diwali 2026 dates TBD — update when NSE publishes official list
}


class NSECalendar:
    """
    Determines whether a given date is an NSE trading day.

    Trading days: Monday–Friday, excluding NSE exchange holidays.
    """

    def is_trading_day(self, d: date) -> bool:
        """Return True if the NSE is open on the given date."""
        if d.weekday() >= 5:          # Saturday=5, Sunday=6
            return False
        return d not in _NSE_HOLIDAYS

    def next_trading_day(self, d: date) -> date:
        """Return the next trading day strictly after d."""
        candidate = d + timedelta(days=1)
        while not self.is_trading_day(candidate):
            candidate += timedelta(days=1)
        return candidate

    def previous_trading_day(self, d: date) -> date:
        """Return the most recent trading day strictly before d."""
        candidate = d - timedelta(days=1)
        while not self.is_trading_day(candidate):
            candidate -= timedelta(days=1)
        return candidate

    def trading_days_between(self, start: date, end: date) -> list[date]:
        """Return sorted list of trading days in [start, end] inclusive."""
        days = []
        current = start
        while current <= end:
            if self.is_trading_day(current):
                days.append(current)
            current += timedelta(days=1)
        return days
