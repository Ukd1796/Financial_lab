"""Database boundary for the analysis fact store.

The default is a local SQLite file.  Point ``ANALYSIS_DATABASE_URL`` at another
database only when the store needs to be shared.  This module never falls back
to the live ``DATABASE_URL``: research ingestion must not be able to write to
production tables by misconfiguration, which is the same rule
``app/event_research/database.py`` follows.
"""

from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.analysis.models import AnalysisBase


DEFAULT_ANALYSIS_DATABASE_URL = "sqlite:///data/analysis/analysis.sqlite"

# Raw payloads live outside the database, content-addressed, so a re-parse never
# costs an API call and the stored bytes can be re-checked against their hash.
DEFAULT_RAW_DIR = Path("data/analysis/raw")


def database_url() -> str:
    return os.environ.get("ANALYSIS_DATABASE_URL", DEFAULT_ANALYSIS_DATABASE_URL)


def raw_dir() -> Path:
    return Path(os.environ.get("ANALYSIS_RAW_DIR", str(DEFAULT_RAW_DIR)))


@lru_cache(maxsize=4)
def _engine(url: str):
    return create_engine(url, echo=False)


@lru_cache(maxsize=4)
def session_factory(url: str):
    return sessionmaker(
        autocommit=False, autoflush=False, expire_on_commit=False, bind=_engine(url)
    )


def new_session(url: str | None = None):
    return session_factory(url or database_url())()


# ``create_all`` creates missing tables but never alters an existing one, so a
# column added to a model stays invisible on an already-populated file until it
# is deleted.  Only *additive* changes belong here — anything else (a type
# change, a dropped column, a new constraint) is a rebuild, and these tables are
# cheap to rebuild because they are derived.
_ADDITIVE_COLUMNS: dict[str, dict[str, str]] = {
    "delisting_outcomes": {"listed_elsewhere": "VARCHAR NOT NULL DEFAULT 'UNCHECKED'"},
}


def _apply_additive_columns(engine) -> None:
    from sqlalchemy import inspect, text

    inspector = inspect(engine)
    existing_tables = set(inspector.get_table_names())
    with engine.begin() as connection:
        for table, columns in _ADDITIVE_COLUMNS.items():
            if table not in existing_tables:
                continue  # create_all just built it from the model, definition included
            present = {column["name"] for column in inspector.get_columns(table)}
            for name, definition in columns.items():
                if name not in present:
                    connection.execute(text(f"ALTER TABLE {table} ADD COLUMN {name} {definition}"))


def initialize_schema(url: str | None = None) -> str:
    resolved = url or database_url()
    if resolved.startswith("sqlite:///") and not resolved.startswith("sqlite:////"):
        Path(resolved.removeprefix("sqlite:///")).parent.mkdir(parents=True, exist_ok=True)
    AnalysisBase.metadata.create_all(bind=_engine(resolved))
    _apply_additive_columns(_engine(resolved))
    return resolved
