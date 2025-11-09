from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.user import User
from app.models.strain import Strain, PriceHistory
from app.models.portfolio import Portfolio
from app.models.trade import Trade, TradeType
from typing import Dict, Optional
from datetime import datetime


class MarketEngine:
    """Core trading logic for buying and selling strain stocks."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def execute_market_buy(self, user_id: int, strain_id: int, shares: float) -> Dict:
        """
        Execute a market buy order.
        
        Args:
            user_id: User ID
            strain_id: Strain ID
            shares: Number of shares to buy
        
        Returns:
            Dict with trade details
        
        Raises:
            ValueError: If insufficient funds or invalid parameters
        """
        if shares <= 0:
            raise ValueError("Shares must be greater than 0")
        
        # Get user and strain
        user = self.db.query(User).filter(User.id == user_id).first()
        strain = self.db.query(Strain).filter(Strain.id == strain_id).first()
        
        if not user:
            raise ValueError("User not found")
        if not strain:
            raise ValueError("Strain not found")
        
        # Calculate total cost
        total_cost = strain.current_price * shares
        
        # Check user balance
        if user.weedcoins_balance < total_cost:
            raise ValueError("Insufficient WeedCoins balance")
        
        # Deduct WeedCoins
        user.weedcoins_balance -= total_cost
        
        # Update or create portfolio entry
        portfolio = self.db.query(Portfolio).filter(
            Portfolio.user_id == user_id,
            Portfolio.strain_id == strain_id
        ).first()
        
        if portfolio:
            # Update existing position
            total_shares = portfolio.shares_owned + shares
            total_invested = portfolio.total_invested + total_cost
            portfolio.shares_owned = total_shares
            portfolio.avg_buy_price = total_invested / total_shares
            portfolio.total_invested = total_invested
        else:
            # Create new position
            portfolio = Portfolio(
                user_id=user_id,
                strain_id=strain_id,
                shares_owned=shares,
                avg_buy_price=strain.current_price,
                total_invested=total_cost
            )
            self.db.add(portfolio)
        
        # Record trade
        trade = Trade(
            user_id=user_id,
            strain_id=strain_id,
            type=TradeType.BUY,
            shares=shares,
            price=strain.current_price,
            total_cost=total_cost
        )
        self.db.add(trade)
        
        self.db.commit()
        
        return {
            "trade_id": trade.id,
            "type": "buy",
            "shares": shares,
            "price": strain.current_price,
            "total_cost": total_cost,
            "new_balance": user.weedcoins_balance
        }
    
    def execute_market_sell(self, user_id: int, strain_id: int, shares: float) -> Dict:
        """
        Execute a market sell order.
        
        Args:
            user_id: User ID
            strain_id: Strain ID
            shares: Number of shares to sell
        
        Returns:
            Dict with trade details
        
        Raises:
            ValueError: If insufficient shares or invalid parameters
        """
        if shares <= 0:
            raise ValueError("Shares must be greater than 0")
        
        # Get user, strain, and portfolio
        user = self.db.query(User).filter(User.id == user_id).first()
        strain = self.db.query(Strain).filter(Strain.id == strain_id).first()
        portfolio = self.db.query(Portfolio).filter(
            Portfolio.user_id == user_id,
            Portfolio.strain_id == strain_id
        ).first()
        
        if not user:
            raise ValueError("User not found")
        if not strain:
            raise ValueError("Strain not found")
        if not portfolio or portfolio.shares_owned < shares:
            raise ValueError("Insufficient shares to sell")
        
        # Calculate proceeds
        proceeds = strain.current_price * shares
        
        # Add WeedCoins
        user.weedcoins_balance += proceeds
        
        # Update portfolio
        portfolio.shares_owned -= shares
        portfolio.total_invested -= (portfolio.avg_buy_price * shares)
        
        # Delete portfolio entry if no shares left
        if portfolio.shares_owned <= 0:
            self.db.delete(portfolio)
        
        # Record trade
        trade = Trade(
            user_id=user_id,
            strain_id=strain_id,
            type=TradeType.SELL,
            shares=shares,
            price=strain.current_price,
            total_cost=proceeds
        )
        self.db.add(trade)
        
        self.db.commit()
        
        return {
            "trade_id": trade.id,
            "type": "sell",
            "shares": shares,
            "price": strain.current_price,
            "proceeds": proceeds,
            "new_balance": user.weedcoins_balance
        }
    
    def calculate_portfolio_value(self, user_id: int) -> Dict:
        """
        Calculate total portfolio value for a user.
        
        Args:
            user_id: User ID
        
        Returns:
            Dict with portfolio value breakdown
        """
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise ValueError("User not found")
        
        # Get all holdings
        portfolios = self.db.query(Portfolio).filter(Portfolio.user_id == user_id).all()
        
        holdings_value = 0.0
        holdings = []
        
        for portfolio in portfolios:
            strain = self.db.query(Strain).filter(Strain.id == portfolio.strain_id).first()
            if strain:
                current_value = strain.current_price * portfolio.shares_owned
                profit_loss = current_value - portfolio.total_invested
                profit_loss_pct = (profit_loss / portfolio.total_invested * 100) if portfolio.total_invested > 0 else 0
                
                holdings_value += current_value
                holdings.append({
                    "strain_id": strain.id,
                    "strain_name": strain.name,
                    "shares": portfolio.shares_owned,
                    "avg_buy_price": portfolio.avg_buy_price,
                    "current_price": strain.current_price,
                    "current_value": current_value,
                    "profit_loss": profit_loss,
                    "profit_loss_pct": round(profit_loss_pct, 2)
                })
        
        total_value = user.weedcoins_balance + holdings_value
        
        return {
            "weedcoins_balance": user.weedcoins_balance,
            "holdings_value": holdings_value,
            "total_value": total_value,
            "holdings": holdings
        }
