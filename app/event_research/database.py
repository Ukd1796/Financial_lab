"""Dedicated database boundary for the V2 research pilot.

The default is a local SQLite file.  Point ``EVENT_RESEARCH_DATABASE_URL`` at
a dedicated Postgres database only when the pilot needs shared storage.  This
module never falls back to the live ``DATABASE_URL``.
"""

from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.event_research.models import EventResearchBase


DEFAULT_EVENT_RESEARCH_DATABASE_URL = "sqlite:///data/event_research/event_research.sqlite"


def database_url() -> str:
    return os.environ.get("EVENT_RESEARCH_DATABASE_URL", DEFAULT_EVENT_RESEARCH_DATABASE_URL)


@lru_cache(maxsize=4)
def _engine(url: str):
    return create_engine(url, echo=False)


@lru_cache(maxsize=4)
def session_factory(url: str):
    return sessionmaker(autocommit=False, autoflush=False, expire_on_commit=False, bind=_engine(url))


def new_session(url: str | None = None):
    return session_factory(url or database_url())()


def initialize_schema(url: str | None = None) -> str:
    resolved = url or database_url()
    if resolved.startswith("sqlite:///") and not resolved.startswith("sqlite:////"):
        relative_path = resolved.removeprefix("sqlite:///")
        Path(relative_path).parent.mkdir(parents=True, exist_ok=True)
    EventResearchBase.metadata.create_all(bind=_engine(resolved))
    return resolved
