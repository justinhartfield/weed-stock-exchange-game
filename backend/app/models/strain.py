from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ForeignKey
from sqlalchemy.sql import func
from app.db.session import Base


class Strain(Base):
    __tablename__ = "strains"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, index=True, nullable=False)
    slug = Column(String(255), unique=True, index=True, nullable=False)
    current_price = Column(Float, nullable=False)
    base_price = Column(Float, nullable=False)
    popularity_score = Column(Float, default=0.0, nullable=False)
    volatility_score = Column(Float, default=0.0, nullable=False)
    favorite_count = Column(Integer, default=0, nullable=False)
    pharmacy_count = Column(Integer, default=0, nullable=False)
    last_updated = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class PriceHistory(Base):
    __tablename__ = "price_history"
    
    id = Column(Integer, primary_key=True, index=True)
    strain_id = Column(Integer, ForeignKey("strains.id"), nullable=False, index=True)
    price = Column(Float, nullable=False)
    volume = Column(Integer, default=0, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)


class MarketEvent(Base):
    __tablename__ = "market_events"
    
    id = Column(Integer, primary_key=True, index=True)
    strain_id = Column(Integer, ForeignKey("strains.id"), nullable=True, index=True)
    event_type = Column(String(50), nullable=False)
    description = Column(Text, nullable=False)
    impact = Column(Float, default=0.0, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)
