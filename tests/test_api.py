import requests
import json
import time

BASE_URL = "http://127.0.0.1:8000"

def generate_user_id():
    """Generate unique user ID for each test run"""
    timestamp = int(time.time())
    return f"user_{timestamp}"

def test_dynamic_deficit_logic():
    """Verify: Dynamic Target Logic still holds"""
    print("\n" + "="*60)
    print("TEST 1: Dynamic Deficit Logic")
    print("="*60)
    
    # Case A: 1000 + 700 = 1700. Last Item = 700 (<1000). Deficit = 300.
    # Target = max(1000, 1700 + 300) = 2000.
    # Current 1700. Needed 300.
    
    order_a = {
        "user_id": generate_user_id() + "_A",
        "products": [
            {"name": "Item 1", "price": 1000, "quantity": 1},
            {"name": "Item 2", "price": 700, "quantity": 1}
        ]
    }
    res_a = requests.post(f"{BASE_URL}/orders/", json=order_a).json()
    print(f"\nCase A (1700 -> Target 2000): {res_a['message']}")
    # Exp: Add products worth 300

def test_rich_cart_success():
    """Verify: 1200 + 1200 (Total 2400) -> DISOUNT UNLOCKED (No 3 item rule)"""
    print("\n" + "="*60)
    print("TEST 2: Rich Cart (2400) -> Success (Discount)")
    print("="*60)
    
    order_c = {
        "user_id": generate_user_id() + "_C",
        "products": [
            {"name": "Rich Item 1", "price": 1200, "quantity": 1},
            {"name": "Rich Item 2", "price": 1200, "quantity": 1}
        ]
    }
    # Distinct Items = 2.
    # Target = 1000 (No deficit). Total 2400.
    # Logic 3.0: Should succeed.
    
    res_c = requests.post(f"{BASE_URL}/orders/", json=order_c).json()
    print(f"Total: {res_c['total_amount']}")
    print(f"Message: {res_c['message']}")
    if 'discount_amount' in res_c:
        print(f"Discount: {res_c['discount_amount']}")
    # Exp: Congratulations!

def test_single_high_value_no_discount():
    """Verify: Single Item > 1000 -> Success but NO Discount"""
    print("\n" + "="*60)
    print("TEST 3: Single High Value (No Discount)")
    print("="*60)
    
    order_d = {
        "user_id": generate_user_id() + "_D",
        "products": [
            {"name": "Luxury", "price": 1400, "quantity": 1}
        ]
    }
    res_d = requests.post(f"{BASE_URL}/orders/", json=order_d).json()
    print(f"Message: {res_d['message']}")
    print(f"Discount Percent: {res_d.get('discount_percent', 0)}")
    # Exp: Order placed successfully! (0% discount)

def test_quantity_ignored():
    """Verify: Qty 2 of same item -> No Discount (Single Distinct Item)"""
    print("\n" + "="*60)
    print("TEST 4: Quantity 2 (Same Item) -> No Discount")
    print("="*60)
    
    order_e = {
        "user_id": generate_user_id() + "_E",
        "products": [
            {"name": "Item A", "price": 600, "quantity": 2}
        ]
    }
    # Total 1200. Distinct Count = 1.
    # Logic: Single Item > 1000 -> Success (No Discount).
    
    res_e = requests.post(f"{BASE_URL}/orders/", json=order_e).json()
    print(f"Total: {res_e['total_amount']}")
    print(f"Message: {res_e['message']}")
    print(f"Discount Percent: {res_e.get('discount_percent', 0)}")
    # Exp: Order placed successfully! (0% discount)


if __name__ == "__main__":
    test_dynamic_deficit_logic()
    test_rich_cart_success()
    test_single_high_value_no_discount()
    test_quantity_ignored()
