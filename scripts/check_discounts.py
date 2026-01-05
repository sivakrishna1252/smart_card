import sys
import os

# Add the parent directory to sys.path to import app
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.core.database import SessionLocal
from app.models.discount import Discount

def check_discounts():
    db = SessionLocal()
    try:
        discounts = db.query(Discount).filter(Discount.active == True).order_by(Discount.minimum_threshold).all()
        print(f"Total Active Discounts: {len(discounts)}")
        for d in discounts:
            print(f"ID: {d.id}, Threshold: {d.minimum_threshold}, Percent: {d.discount_percent}")
    finally:
        db.close()

if __name__ == "__main__":
    check_discounts()
