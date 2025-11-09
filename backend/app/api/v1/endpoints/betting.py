from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.db.session import get_db
from app.models.user import User
from app.models.bet import FuturesBet, HeadToHeadBet, PropBet, BetType
from app.services.betting_engine import BettingEngine
from app.api.v1.endpoints.auth import get_current_user
from pydantic import BaseModel
from typing import List
from datetime import datetime

router = APIRouter()


class FuturesBetRequest(BaseModel):
    bet_type: BetType
    target_strain_id: int
    prediction: str
    stake: float
    odds: float
    expires_at: datetime


class HeadToHeadBetRequest(BaseModel):
    strain_a_id: int
    strain_b_id: int
    metric: str
    prediction: str
    stake: float
    odds: float
    expires_at: datetime


class PropBetRequest(BaseModel):
    bet_description: str
    bet_type: str
    stake: float
    odds: float
    expires_at: datetime


@router.post("/bets/futures")
def place_futures_bet(
    bet_request: FuturesBetRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Place a futures bet."""
    engine = BettingEngine(db)
    
    try:
        result = engine.place_futures_bet(
            user_id=current_user.id,
            bet_type=bet_request.bet_type,
            target_strain_id=bet_request.target_strain_id,
            prediction=bet_request.prediction,
            stake=bet_request.stake,
            odds=bet_request.odds,
            expires_at=bet_request.expires_at
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/bets/head-to-head")
def place_head_to_head_bet(
    bet_request: HeadToHeadBetRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Place a head-to-head bet."""
    engine = BettingEngine(db)
    
    try:
        result = engine.place_head_to_head_bet(
            user_id=current_user.id,
            strain_a_id=bet_request.strain_a_id,
            strain_b_id=bet_request.strain_b_id,
            metric=bet_request.metric,
            prediction=bet_request.prediction,
            stake=bet_request.stake,
            odds=bet_request.odds,
            expires_at=bet_request.expires_at
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/bets/prop")
def place_prop_bet(
    bet_request: PropBetRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Place a proposition bet."""
    engine = BettingEngine(db)
    
    try:
        result = engine.place_prop_bet(
            user_id=current_user.id,
            bet_description=bet_request.bet_description,
            bet_type=bet_request.bet_type,
            stake=bet_request.stake,
            odds=bet_request.odds,
            expires_at=bet_request.expires_at
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/bets/my-bets")
def get_my_bets(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's betting history."""
    futures_bets = db.query(FuturesBet).filter(
        FuturesBet.user_id == current_user.id
    ).order_by(desc(FuturesBet.created_at)).limit(limit).all()
    
    h2h_bets = db.query(HeadToHeadBet).filter(
        HeadToHeadBet.user_id == current_user.id
    ).order_by(desc(HeadToHeadBet.created_at)).limit(limit).all()
    
    prop_bets = db.query(PropBet).filter(
        PropBet.user_id == current_user.id
    ).order_by(desc(PropBet.created_at)).limit(limit).all()
    
    return {
        "futures_bets": [
            {
                "id": bet.id,
                "bet_type": bet.bet_type,
                "target_strain_id": bet.target_strain_id,
                "prediction": bet.prediction,
                "stake": bet.stake,
                "odds": bet.odds,
                "potential_payout": bet.potential_payout,
                "expires_at": bet.expires_at,
                "settled": bet.settled,
                "outcome": bet.outcome,
                "created_at": bet.created_at
            }
            for bet in futures_bets
        ],
        "head_to_head_bets": [
            {
                "id": bet.id,
                "strain_a_id": bet.strain_a_id,
                "strain_b_id": bet.strain_b_id,
                "metric": bet.metric,
                "prediction": bet.prediction,
                "stake": bet.stake,
                "odds": bet.odds,
                "potential_payout": bet.potential_payout,
                "expires_at": bet.expires_at,
                "settled": bet.settled,
                "outcome": bet.outcome,
                "created_at": bet.created_at
            }
            for bet in h2h_bets
        ],
        "prop_bets": [
            {
                "id": bet.id,
                "bet_description": bet.bet_description,
                "bet_type": bet.bet_type,
                "stake": bet.stake,
                "odds": bet.odds,
                "potential_payout": bet.potential_payout,
                "expires_at": bet.expires_at,
                "settled": bet.settled,
                "outcome": bet.outcome,
                "created_at": bet.created_at
            }
            for bet in prop_bets
        ]
    }
