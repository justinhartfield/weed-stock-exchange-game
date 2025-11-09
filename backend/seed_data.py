"""
Seed script to populate initial strain data.
Run this after database migrations to create sample strains.
"""
from app.db.session import SessionLocal
from app.models.strain import Strain
from app.models.gamification import Achievement
from app.services.price_calculator import PriceCalculator
import random


def create_sample_strains():
    """Create sample cannabis strains with realistic data."""
    db = SessionLocal()
    calculator = PriceCalculator()
    
    sample_strains = [
        {"name": "Pedanios 29/1 SRD-CA", "base_price_per_gram": 6.50, "favorites": 154, "pharmacies": 12},
        {"name": "enua 22/1 CA JFG", "base_price_per_gram": 7.20, "favorites": 132, "pharmacies": 15},
        {"name": "Bathera 22/1 PM", "base_price_per_gram": 6.80, "favorites": 98, "pharmacies": 10},
        {"name": "Canopy KMI 28", "base_price_per_gram": 8.50, "favorites": 76, "pharmacies": 8},
        {"name": "Pedanios 31/1 COS-CA", "base_price_per_gram": 7.00, "favorites": 154, "pharmacies": 14},
        {"name": "Aurora Pink Kush", "base_price_per_gram": 9.20, "favorites": 201, "pharmacies": 18},
        {"name": "Tilray Master Kush", "base_price_per_gram": 8.80, "favorites": 167, "pharmacies": 16},
        {"name": "Bedrocan Jack Herer", "base_price_per_gram": 10.50, "favorites": 234, "pharmacies": 20},
        {"name": "Spectrum Red No. 2", "base_price_per_gram": 7.90, "favorites": 112, "pharmacies": 11},
        {"name": "Aphria Rideau", "base_price_per_gram": 6.30, "favorites": 89, "pharmacies": 9},
        {"name": "Peace Naturals 20/1", "base_price_per_gram": 7.50, "favorites": 145, "pharmacies": 13},
        {"name": "Tweed Argyle", "base_price_per_gram": 8.20, "favorites": 178, "pharmacies": 17},
        {"name": "Broken Coast Galiano", "base_price_per_gram": 11.00, "favorites": 289, "pharmacies": 22},
        {"name": "Organigram Edison", "base_price_per_gram": 6.90, "favorites": 103, "pharmacies": 10},
        {"name": "Hexo Tsunami", "base_price_per_gram": 7.40, "favorites": 124, "pharmacies": 12},
    ]
    
    try:
        for strain_data in sample_strains:
            # Check if strain already exists
            existing = db.query(Strain).filter(Strain.name == strain_data["name"]).first()
            if existing:
                print(f"Strain '{strain_data['name']}' already exists, skipping...")
                continue
            
            # Generate slug
            slug = strain_data["name"].lower().replace(" ", "-").replace("/", "-")
            
            # Calculate volatility (random spread for demo)
            volatility_spread = random.uniform(0.5, 4.0)
            
            # Calculate initial price
            calc_data = {
                "avg_price_per_gram": strain_data["base_price_per_gram"],
                "favorite_count": strain_data["favorites"],
                "volatility_spread": volatility_spread
            }
            initial_price = calculator.calculate_stock_price(calc_data)
            
            # Create strain
            strain = Strain(
                name=strain_data["name"],
                slug=slug,
                current_price=initial_price,
                base_price=strain_data["base_price_per_gram"] * 10,
                popularity_score=strain_data["favorites"] / 10,
                volatility_score=volatility_spread,
                favorite_count=strain_data["favorites"],
                pharmacy_count=strain_data["pharmacies"]
            )
            
            db.add(strain)
            print(f"Created strain: {strain_data['name']} @ {initial_price} WC")
        
        db.commit()
        print(f"\n✓ Successfully seeded {len(sample_strains)} strains!")
        
    except Exception as e:
        print(f"Error seeding strains: {e}")
        db.rollback()
    finally:
        db.close()


def create_achievements():
    """Create achievement badges."""
    db = SessionLocal()
    
    achievements = [
        {"name": "First Trade", "description": "Execute your first trade", "criteria_type": "trades_count", "criteria_value": 1},
        {"name": "Diamond Hands", "description": "Hold a stock for 30+ days", "criteria_type": "hold_days", "criteria_value": 30},
        {"name": "Bull Run", "description": "5 consecutive profitable trades", "criteria_type": "consecutive_wins", "criteria_value": 5},
        {"name": "Sharp Shooter", "description": "Win 10 futures bets", "criteria_type": "futures_wins", "criteria_value": 10},
        {"name": "Oracle", "description": "Win a 3-bet parlay", "criteria_type": "parlay_wins", "criteria_value": 1},
        {"name": "Underdog", "description": "Win a bet with 10:1 odds or higher", "criteria_type": "high_odds_win", "criteria_value": 10},
        {"name": "WeedCoin Millionaire", "description": "Reach 10,000 WeedCoins", "criteria_type": "balance", "criteria_value": 10000},
        {"name": "Market Whale", "description": "Execute a trade worth over 5,000 WeedCoins", "criteria_type": "trade_value", "criteria_value": 5000},
    ]
    
    try:
        for ach_data in achievements:
            existing = db.query(Achievement).filter(Achievement.name == ach_data["name"]).first()
            if existing:
                print(f"Achievement '{ach_data['name']}' already exists, skipping...")
                continue
            
            achievement = Achievement(**ach_data)
            db.add(achievement)
            print(f"Created achievement: {ach_data['name']}")
        
        db.commit()
        print(f"\n✓ Successfully created {len(achievements)} achievements!")
        
    except Exception as e:
        print(f"Error creating achievements: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    print("Seeding database with initial data...\n")
    create_sample_strains()
    create_achievements()
    print("\n✓ Database seeding complete!")
