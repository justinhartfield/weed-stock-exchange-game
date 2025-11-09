from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.user import User
from app.services.market_engine import MarketEngine
from app.api.v1.endpoints.auth import get_current_user

router = APIRouter()


@router.get("/portfolio")
def get_portfolio(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's current portfolio with total value."""
    engine = MarketEngine(db)
    portfolio = engine.calculate_portfolio_value(current_user.id)
    return portfolio


@router.get("/portfolio/performance")
def get_portfolio_performance(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get portfolio performance metrics."""
    engine = MarketEngine(db)
    portfolio = engine.calculate_portfolio_value(current_user.id)
    
    # Calculate best and worst performers
    holdings = portfolio.get("holdings", [])
    
    best_performer = None
    worst_performer = None
    
    if holdings:
        sorted_by_profit = sorted(holdings, key=lambda x: x["profit_loss_pct"], reverse=True)
        best_performer = sorted_by_profit[0] if sorted_by_profit else None
        worst_performer = sorted_by_profit[-1] if sorted_by_profit else None
    
    return {
        "total_value": portfolio["total_value"],
        "holdings_value": portfolio["holdings_value"],
        "weedcoins_balance": portfolio["weedcoins_balance"],
        "best_performer": best_performer,
        "worst_performer": worst_performer,
        "holdings_count": len(holdings)
    }
