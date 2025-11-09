from app.core.celery_app import celery_app
from app.db.session import SessionLocal
from app.models.strain import Strain, PriceHistory
from app.services.price_calculator import PriceCalculator
from datetime import datetime
import random


@celery_app.task
def sync_strain_data_task():
    """
    Sync strain data and update prices.
    This task runs every 5 minutes.
    
    In production, this would fetch real data from Metabase.
    For now, it simulates price updates.
    """
    db = SessionLocal()
    
    try:
        strains = db.query(Strain).all()
        calculator = PriceCalculator()
        
        for strain in strains:
            # Simulate small price fluctuations
            # In production, fetch real data from Metabase
            favorite_change = random.randint(-2, 5)
            strain.favorite_count = max(0, strain.favorite_count + favorite_change)
            
            # Recalculate price
            strain_data = {
                "avg_price_per_gram": strain.base_price / 10,
                "favorite_count": strain.favorite_count,
                "volatility_spread": strain.volatility_score
            }
            
            new_price = calculator.calculate_stock_price(strain_data)
            strain.current_price = new_price
            strain.last_updated = datetime.utcnow()
            
            # Record price history
            price_record = PriceHistory(
                strain_id=strain.id,
                price=new_price,
                volume=random.randint(0, 100)
            )
            db.add(price_record)
        
        db.commit()
        print(f"Synced {len(strains)} strains at {datetime.utcnow()}")
        
    except Exception as e:
        print(f"Error syncing strain data: {e}")
        db.rollback()
    finally:
        db.close()
