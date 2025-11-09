from sqlalchemy.orm import Session
from app.models.user import User
from app.models.bet import FuturesBet, HeadToHeadBet, PropBet, BetType, BetOutcome
from typing import Dict
from datetime import datetime


class BettingEngine:
    """Handles betting operations for futures, head-to-head, and prop bets."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def place_futures_bet(
        self,
        user_id: int,
        bet_type: BetType,
        target_strain_id: int,
        prediction: str,
        stake: float,
        odds: float,
        expires_at: datetime
    ) -> Dict:
        """Place a futures bet."""
        if stake <= 0:
            raise ValueError("Stake must be greater than 0")
        
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise ValueError("User not found")
        
        if user.weedcoins_balance < stake:
            raise ValueError("Insufficient WeedCoins balance")
        
        # Deduct stake
        user.weedcoins_balance -= stake
        
        # Calculate potential payout
        potential_payout = stake * odds
        
        # Create bet
        bet = FuturesBet(
            user_id=user_id,
            bet_type=bet_type,
            target_strain_id=target_strain_id,
            prediction=prediction,
            stake=stake,
            odds=odds,
            potential_payout=potential_payout,
            expires_at=expires_at
        )
        self.db.add(bet)
        self.db.commit()
        
        return {
            "bet_id": bet.id,
            "type": "futures",
            "stake": stake,
            "odds": odds,
            "potential_payout": potential_payout,
            "new_balance": user.weedcoins_balance
        }
    
    def place_head_to_head_bet(
        self,
        user_id: int,
        strain_a_id: int,
        strain_b_id: int,
        metric: str,
        prediction: str,
        stake: float,
        odds: float,
        expires_at: datetime
    ) -> Dict:
        """Place a head-to-head bet."""
        if stake <= 0:
            raise ValueError("Stake must be greater than 0")
        
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise ValueError("User not found")
        
        if user.weedcoins_balance < stake:
            raise ValueError("Insufficient WeedCoins balance")
        
        # Deduct stake
        user.weedcoins_balance -= stake
        
        # Calculate potential payout
        potential_payout = stake * odds
        
        # Create bet
        bet = HeadToHeadBet(
            user_id=user_id,
            strain_a_id=strain_a_id,
            strain_b_id=strain_b_id,
            metric=metric,
            prediction=prediction,
            stake=stake,
            odds=odds,
            potential_payout=potential_payout,
            expires_at=expires_at
        )
        self.db.add(bet)
        self.db.commit()
        
        return {
            "bet_id": bet.id,
            "type": "head_to_head",
            "stake": stake,
            "odds": odds,
            "potential_payout": potential_payout,
            "new_balance": user.weedcoins_balance
        }
    
    def place_prop_bet(
        self,
        user_id: int,
        bet_description: str,
        bet_type: str,
        stake: float,
        odds: float,
        expires_at: datetime
    ) -> Dict:
        """Place a proposition bet."""
        if stake <= 0:
            raise ValueError("Stake must be greater than 0")
        
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise ValueError("User not found")
        
        if user.weedcoins_balance < stake:
            raise ValueError("Insufficient WeedCoins balance")
        
        # Deduct stake
        user.weedcoins_balance -= stake
        
        # Calculate potential payout
        potential_payout = stake * odds
        
        # Create bet
        bet = PropBet(
            user_id=user_id,
            bet_description=bet_description,
            bet_type=bet_type,
            stake=stake,
            odds=odds,
            potential_payout=potential_payout,
            expires_at=expires_at
        )
        self.db.add(bet)
        self.db.commit()
        
        return {
            "bet_id": bet.id,
            "type": "prop",
            "stake": stake,
            "odds": odds,
            "potential_payout": potential_payout,
            "new_balance": user.weedcoins_balance
        }
    
    def settle_bet(self, bet_id: int, bet_type: str, won: bool) -> Dict:
        """Settle a bet and distribute winnings if applicable."""
        bet_model = {
            "futures": FuturesBet,
            "head_to_head": HeadToHeadBet,
            "prop": PropBet
        }.get(bet_type)
        
        if not bet_model:
            raise ValueError("Invalid bet type")
        
        bet = self.db.query(bet_model).filter(bet_model.id == bet_id).first()
        if not bet:
            raise ValueError("Bet not found")
        
        if bet.settled:
            raise ValueError("Bet already settled")
        
        # Mark as settled
        bet.settled = True
        bet.outcome = BetOutcome.WON if won else BetOutcome.LOST
        
        # If won, add payout to user balance
        if won:
            user = self.db.query(User).filter(User.id == bet.user_id).first()
            if user:
                user.weedcoins_balance += bet.potential_payout
        
        self.db.commit()
        
        return {
            "bet_id": bet_id,
            "outcome": "won" if won else "lost",
            "payout": bet.potential_payout if won else 0
        }
