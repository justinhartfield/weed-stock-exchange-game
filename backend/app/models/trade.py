from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Enum
from sqlalchemy.sql import func
import enum
from app.db.session import Base


class TradeType(str, enum.Enum):
    BUY = "buy"
    SELL = "sell"


class OrderType(str, enum.Enum):
    MARKET = "market"
    LIMIT = "limit"
    STOP = "stop"


class OrderStatus(str, enum.Enum):
    PENDING = "pending"
    EXECUTED = "executed"
    CANCELLED = "cancelled"


class Trade(Base):
    __tablename__ = "trades"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    strain_id = Column(Integer, ForeignKey("strains.id"), nullable=False, index=True)
    type = Column(Enum(TradeType), nullable=False)
    shares = Column(Float, nullable=False)
    price = Column(Float, nullable=False)
    total_cost = Column(Float, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)


class TradeOrder(Base):
    __tablename__ = "trade_orders"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    strain_id = Column(Integer, ForeignKey("strains.id"), nullable=False, index=True)
    order_type = Column(Enum(OrderType), nullable=False)
    trade_type = Column(Enum(TradeType), nullable=False)
    shares = Column(Float, nullable=False)
    target_price = Column(Float, nullable=True)
    status = Column(Enum(OrderStatus), default=OrderStatus.PENDING, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)
    executed_at = Column(DateTime(timezone=True), nullable=True)
