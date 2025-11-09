from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean, Text, Enum
from sqlalchemy.sql import func
import enum
from app.db.session import Base


class BetType(str, enum.Enum):
    POPULARITY = "popularity"
    PRICE = "price"
    AVAILABILITY = "availability"


class BetOutcome(str, enum.Enum):
    PENDING = "pending"
    WON = "won"
    LOST = "lost"


class FuturesBet(Base):
    __tablename__ = "futures_bets"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    bet_type = Column(Enum(BetType), nullable=False)
    target_strain_id = Column(Integer, ForeignKey("strains.id"), nullable=False, index=True)
    prediction = Column(Text, nullable=False)
    stake = Column(Float, nullable=False)
    odds = Column(Float, nullable=False)
    potential_payout = Column(Float, nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False, index=True)
    settled = Column(Boolean, default=False, nullable=False)
    outcome = Column(Enum(BetOutcome), default=BetOutcome.PENDING, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class HeadToHeadBet(Base):
    __tablename__ = "head_to_head_bets"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    strain_a_id = Column(Integer, ForeignKey("strains.id"), nullable=False)
    strain_b_id = Column(Integer, ForeignKey("strains.id"), nullable=False)
    metric = Column(String(50), nullable=False)
    prediction = Column(String(50), nullable=False)
    stake = Column(Float, nullable=False)
    odds = Column(Float, nullable=False)
    potential_payout = Column(Float, nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False, index=True)
    settled = Column(Boolean, default=False, nullable=False)
    outcome = Column(Enum(BetOutcome), default=BetOutcome.PENDING, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class PropBet(Base):
    __tablename__ = "prop_bets"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    bet_description = Column(Text, nullable=False)
    bet_type = Column(String(50), nullable=False)
    stake = Column(Float, nullable=False)
    odds = Column(Float, nullable=False)
    potential_payout = Column(Float, nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False, index=True)
    settled = Column(Boolean, default=False, nullable=False)
    outcome = Column(Enum(BetOutcome), default=BetOutcome.PENDING, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
