from fastapi import APIRouter
from app.api.v1.endpoints import auth, trading, portfolio, betting, leaderboard

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(trading.router, prefix="/trading", tags=["trading"])
api_router.include_router(portfolio.router, prefix="/portfolio", tags=["portfolio"])
api_router.include_router(betting.router, prefix="/betting", tags=["betting"])
api_router.include_router(leaderboard.router, prefix="/leaderboard", tags=["leaderboard"])
