"""Create the isolated local database used by the Phase-1 event-data pilot.

By default this creates ``data/event_research/event_research.sqlite``.  It
does not read ``DATABASE_URL`` and never modifies the production data store.

Usage:
  finance/bin/python3 -m scripts.event_research.init_research_db
  EVENT_RESEARCH_DATABASE_URL=postgresql://... finance/bin/python3 -m scripts.event_research.init_research_db
"""

from dotenv import load_dotenv


def main() -> None:
    load_dotenv()
    from app.event_research.database import initialize_schema

    print(f"Initialised event-research schema at {initialize_schema()}")


if __name__ == "__main__":
    main()
