import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.core.database import engine
from app.data.models import Base  # imports all models including SignalQueue, LivePosition


def init_db():
    """
    Create all tables defined in app/data/models.py.
    Safe to re-run — only creates tables that do not yet exist.

    Tables created:
      market_ohlc      — historical OHLC data
      decision_logs    — backtest decision log
      signal_queue     — live/paper trading signals (NEW)
      live_positions   — live/paper trading open positions (NEW)

    The selector_state table is created separately via:
      scripts/create_live_tables.sql  (or psql directly)
    because SQLAlchemy raw-SQL upsert is used for it in run_signals.py.
    """
    Base.metadata.create_all(bind=engine)
    print("Database tables created / verified.")


if __name__ == "__main__":
    init_db()
