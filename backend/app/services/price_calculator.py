from typing import Dict


class PriceCalculator:
    """Calculate strain stock prices based on market data."""
    
    @staticmethod
    def calculate_stock_price(strain_data: Dict) -> float:
        """
        Calculate stock price using the formula:
        Stock Price = (Base Price Component) + (Popularity Component) + (Volatility Component)
        
        Args:
            strain_data: Dict containing:
                - avg_price_per_gram: Average market price
                - favorite_count: Number of user favorites
                - volatility_spread: 30-day price range (max - min)
        
        Returns:
            Calculated stock price
        """
        # Base Price Component
        avg_price = strain_data.get("avg_price_per_gram", 10.0)
        base = avg_price * 10
        
        # Popularity Component (Favorite Counts)
        favorite_count = strain_data.get("favorite_count", 0)
        popularity_bonus = favorite_count / 10
        
        # Volatility Component
        volatility_spread = strain_data.get("volatility_spread", 0.0)
        volatility_modifier = 0
        
        if volatility_spread > 0:
            # Calculate volatility percentage
            if avg_price > 0:
                volatility_pct = (volatility_spread / avg_price) * 100
                
                # Apply volatility premium based on spread
                if volatility_pct > 50:
                    volatility_modifier = base * 0.05  # +5% for high volatility
                elif volatility_pct > 30:
                    volatility_modifier = base * 0.03  # +3% for medium volatility
                elif volatility_pct < 10:
                    volatility_modifier = base * -0.02  # -2% for low volatility
        
        # Final Price
        price = base + popularity_bonus + volatility_modifier
        return round(price, 2)
    
    @staticmethod
    def calculate_price_change_percentage(old_price: float, new_price: float) -> float:
        """Calculate percentage change between two prices."""
        if old_price == 0:
            return 0.0
        return round(((new_price - old_price) / old_price) * 100, 2)
