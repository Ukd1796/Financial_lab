# app/data/repository.py

from collections import defaultdict
from typing import Dict, List, Set
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, distinct
from datetime import datetime
from app.core.database import SessionLocal
from app.data.models import MarketOHLC, OHLCRecord


import json
from app.data.models import DecisionLog


class MarketDataRepository:

    def bulk_upsert(self, records: List[OHLCRecord]):
        """
        Insert records while avoiding duplicates.
        Relies on unique constraint for safety.
        """
        session = SessionLocal()

        try:
            for record in records:
                db_record = MarketOHLC(
                    symbol=record.symbol,
                    timestamp=record.timestamp,
                    open=record.open,
                    high=record.high,
                    low=record.low,
                    close=record.close,
                    volume=record.volume
                )

                session.add(db_record)

            session.commit()

        except IntegrityError:
            session.rollback()
            # If duplicate occurs, ignore
            pass

        finally:
            session.close()

    def get_ingested_symbols(self) -> Set[str]:
        """Return the set of symbols that already have data in the database."""
        session = SessionLocal()
        try:
            stmt = select(distinct(MarketOHLC.symbol))
            results = session.execute(stmt).scalars().all()
            return set(results)
        finally:
            session.close()

    def get_ohlc(
        self,
        symbol: str,
        start: datetime,
        end: datetime
    ) -> List[MarketOHLC]:

        session = SessionLocal()

        try:
            stmt = (
                select(MarketOHLC)
                .where(MarketOHLC.symbol == symbol)
                .where(MarketOHLC.timestamp >= start)
                .where(MarketOHLC.timestamp <= end)
                .order_by(MarketOHLC.timestamp.asc())
            )

            results = session.execute(stmt).scalars().all()
            return results

        finally:
            session.close()
    
    def get_ohlc_bulk(
        self,
        symbols: List[str],
        start: datetime,
        end: datetime,
    ) -> Dict[str, List[MarketOHLC]]:
        """
        Fetch OHLCV data for multiple symbols in a single DB query.
        Returns a dict of symbol → sorted list of MarketOHLC records.
        Symbols with no data in the period are absent from the dict.
        """
        session = SessionLocal()
        try:
            stmt = (
                select(MarketOHLC)
                .where(MarketOHLC.symbol.in_(symbols))
                .where(MarketOHLC.timestamp >= start)
                .where(MarketOHLC.timestamp <= end)
                .order_by(MarketOHLC.symbol.asc(), MarketOHLC.timestamp.asc())
            )
            rows = session.execute(stmt).scalars().all()

            result: Dict[str, List[MarketOHLC]] = defaultdict(list)
            for row in rows:
                result[row.symbol].append(row)
            return dict(result)
        finally:
            session.close()

    def log_decision(
    self,
    timestamp,
    symbol,
    decision,
    execution_result
):

        session = SessionLocal()

        log_entry = DecisionLog(
            timestamp=timestamp,
            symbol=symbol,
            action=decision.action,
            quantity=decision.quantity,
            price=execution_result.price,
            reasoning=decision.reasoning,
            portfolio_before=json.dumps(execution_result.portfolio_before),
            portfolio_after=json.dumps(execution_result.portfolio_after)
        )

        session.add(log_entry)
        session.commit()
        session.close()
