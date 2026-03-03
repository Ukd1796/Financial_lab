# app/data/repository.py

from typing import List
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
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
