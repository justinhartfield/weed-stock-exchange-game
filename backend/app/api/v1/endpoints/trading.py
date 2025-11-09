from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.db.session import get_db
from app.models.user import User
from app.models.strain import Strain, PriceHistory
from app.models.trade import Trade
from app.services.market_engine import MarketEngine
from app.api.v1.endpoints.auth import get_current_user
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, timedelta

router = APIRouter()


class TradeRequest(BaseModel):
    strain_id: int
    shares: float


class StrainResponse(BaseModel):
    id: int
    name: str
    slug: str
    current_price: float
    favorite_count: int
    pharmacy_count: int
    change_24h: Optional[float] = None
    
    class Config:
        from_attributes = True


class TradeResponse(BaseModel):
    id: int
    strain_id: int
    type: str
    shares: float
    price: float
    total_cost: float
    timestamp: datetime
    
    class Config:
        from_attributes = True


@router.get("/strains", response_model=List[StrainResponse])
def list_strains(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db)
):
    """List all tradable strains with current prices."""
    strains = db.query(Strain).offset(skip).limit(limit).all()
    
    # Calculate 24h change for each strain
    result = []
    for strain in strains:
        # Get price from 24 hours ago
        yesterday = datetime.utcnow() - timedelta(hours=24)
        old_price_record = db.query(PriceHistory).filter(
            PriceHistory.strain_id == strain.id,
            PriceHistory.timestamp >= yesterday
        ).order_by(PriceHistory.timestamp).first()
        
        change_24h = None
        if old_price_record and old_price_record.price > 0:
            change_24h = ((strain.current_price - old_price_record.price) / old_price_record.price) * 100
        
        strain_dict = {
            "id": strain.id,
            "name": strain.name,
            "slug": strain.slug,
            "current_price": strain.current_price,
            "favorite_count": strain.favorite_count,
            "pharmacy_count": strain.pharmacy_count,
            "change_24h": round(change_24h, 2) if change_24h is not None else None
        }
        result.append(strain_dict)
    
    return result


@router.get("/strains/{strain_id}")
def get_strain_detail(strain_id: int, db: Session = Depends(get_db)):
    """Get detailed strain data with price history."""
    strain = db.query(Strain).filter(Strain.id == strain_id).first()
    if not strain:
        raise HTTPException(status_code=404, detail="Strain not found")
    
    # Get price history (last 90 days)
    ninety_days_ago = datetime.utcnow() - timedelta(days=90)
    price_history = db.query(PriceHistory).filter(
        PriceHistory.strain_id == strain_id,
        PriceHistory.timestamp >= ninety_days_ago
    ).order_by(PriceHistory.timestamp).all()
    
    return {
        "id": strain.id,
        "name": strain.name,
        "slug": strain.slug,
        "current_price": strain.current_price,
        "base_price": strain.base_price,
        "popularity_score": strain.popularity_score,
        "volatility_score": strain.volatility_score,
        "favorite_count": strain.favorite_count,
        "pharmacy_count": strain.pharmacy_count,
        "price_history": [
            {
                "price": ph.price,
                "volume": ph.volume,
                "timestamp": ph.timestamp
            }
            for ph in price_history
        ]
    }


@router.post("/trades/buy")
def buy_shares(
    trade_request: TradeRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Execute a market buy order."""
    engine = MarketEngine(db)
    
    try:
        result = engine.execute_market_buy(
            user_id=current_user.id,
            strain_id=trade_request.strain_id,
            shares=trade_request.shares
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/trades/sell")
def sell_shares(
    trade_request: TradeRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Execute a market sell order."""
    engine = MarketEngine(db)
    
    try:
        result = engine.execute_market_sell(
            user_id=current_user.id,
            strain_id=trade_request.strain_id,
            shares=trade_request.shares
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/trades/history", response_model=List[TradeResponse])
def get_trade_history(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's trade history with pagination."""
    trades = db.query(Trade).filter(
        Trade.user_id == current_user.id
    ).order_by(desc(Trade.timestamp)).offset(skip).limit(limit).all()
    
    return trades
