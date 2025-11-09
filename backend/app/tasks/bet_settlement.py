from app.core.celery_app import celery_app
from app.db.session import SessionLocal
from app.models.bet import FuturesBet, HeadToHeadBet, PropBet, BetOutcome
from app.services.betting_engine import BettingEngine
from datetime import datetime


@celery_app.task
def settle_expired_bets_task():
    """
    Settle expired bets.
    This task runs every hour.
    
    In production, this would use actual market data to determine outcomes.
    For now, it randomly settles bets.
    """
    db = SessionLocal()
    engine = BettingEngine(db)
    
    try:
        now = datetime.utcnow()
        
        # Settle expired futures bets
        expired_futures = db.query(FuturesBet).filter(
            FuturesBet.expires_at <= now,
            FuturesBet.settled == False
        ).all()
        
        for bet in expired_futures:
            # In production, check actual outcome
            # For now, randomly determine outcome (50/50)
            import random
            won = random.choice([True, False])
            engine.settle_bet(bet.id, "futures", won)
        
        # Settle expired head-to-head bets
        expired_h2h = db.query(HeadToHeadBet).filter(
            HeadToHeadBet.expires_at <= now,
            HeadToHeadBet.settled == False
        ).all()
        
        for bet in expired_h2h:
            import random
            won = random.choice([True, False])
            engine.settle_bet(bet.id, "head_to_head", won)
        
        # Settle expired prop bets
        expired_prop = db.query(PropBet).filter(
            PropBet.expires_at <= now,
            PropBet.settled == False
        ).all()
        
        for bet in expired_prop:
            import random
            won = random.choice([True, False])
            engine.settle_bet(bet.id, "prop", won)
        
        print(f"Settled {len(expired_futures) + len(expired_h2h) + len(expired_prop)} bets at {datetime.utcnow()}")
        
    except Exception as e:
        print(f"Error settling bets: {e}")
        db.rollback()
    finally:
        db.close()
