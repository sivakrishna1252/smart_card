import sys
import os

# Add the parent directory to sys.path to import app
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.services.order_service import create_order
from app.schemas.order import OrderCreate, OrderProductCreate
from app.models.discount import Discount

def setup_test_discounts(db: Session):
    # Ensure we have tiered discount rules: 5000@10%, 10000@20%
    db.query(Discount).delete()
    rule1 = Discount(minimum_threshold=5000, discount_percent=10, active=True)
    rule2 = Discount(minimum_threshold=10000, discount_percent=20, active=True)
    db.add(rule1)
    db.add(rule2)
    db.commit()

def test_verification():
    db = SessionLocal()
    try:
        setup_test_discounts(db)
        
        print("--- Scenario: Start at 3200, Add 2000 (Total 5200, Target 5000) ---")
        order_data = OrderCreate(
            user_id="test_user_jump_5k",
            products=[
                OrderProductCreate(name="Item 1", price=3200, quantity=1),
                OrderProductCreate(name="Item 2", price=2000, quantity=1)
            ]
        )
        resp = create_order(db, order_data)
        print(f"Message: {resp['message']}")
        print(f"Discount %: {resp['discount_percent']}")
        # Should be granted because 1st item (3200) < 5000 and total 5200 >= 5000
        assert "You unlocked 10% discount" in resp['message']
        assert resp['discount_percent'] == 10
        
        print("\n--- Scenario: Bulk Start at 5200 (Total 5200, Target 5000) ---")
        order_data = OrderCreate(
            user_id="test_user_bulk_5k",
            products=[
                OrderProductCreate(name="Bulk Item", price=5200, quantity=1)
            ]
        )
        resp = create_order(db, order_data)
        print(f"Message: {resp['message']}")
        print(f"Discount %: {resp['discount_percent']}")
        # Should be BLOCKED because 1st item (5200) is NOT < 5000
        # And it should show motivator for NEXT tier (10000)
        assert "Add ₹4800 more to unlock 20% discount" in resp['message']
        assert resp['discount_percent'] == 0
        
        print("\n--- Scenario: Cross 10k from below (Total 11k, Target 10k) ---")
        order_data = OrderCreate(
            user_id="test_user_jump_10k",
            products=[
                OrderProductCreate(name="Item 1", price=9000, quantity=1),
                OrderProductCreate(name="Item 2", price=2000, quantity=1)
            ]
        )
        resp = create_order(db, order_data)
        print(f"Message: {resp['message']}")
        print(f"Discount %: {resp['discount_percent']}")
        assert "You unlocked 20% discount" in resp['message']
        assert resp['discount_percent'] == 20

        print("\nVerification Passed!")
        
    finally:
        db.close()

if __name__ == "__main__":
    test_verification()
