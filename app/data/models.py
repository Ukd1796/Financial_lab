# app/data/models.py

from sqlalchemy import Column, String, Float, DateTime, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base
import uuid

Base = declarative_base()


class MarketOHLC(Base):
    __tablename__ = "market_ohlc"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    symbol = Column(String, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    open = Column(Float, nullable=False)
    high = Column(Float, nullable=False)
    low = Column(Float, nullable=False)
    close = Column(Float, nullable=False)
    volume = Column(Float, nullable=False)

    __table_args__ = (
        UniqueConstraint("symbol", "timestamp", name="uix_symbol_timestamp"),
    )

class DecisionLog(Base):
    __tablename__ = "decision_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    timestamp = Column(DateTime, nullable=False)
    symbol = Column(String, nullable=False)
    action = Column(String, nullable=False)
    quantity = Column(Float)
    price = Column(Float)
    reasoning = Column(String)
    portfolio_before = Column(String)  # store JSON string
    portfolio_after = Column(String)


