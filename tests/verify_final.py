import requests
import json
import time

BASE_URL = "http://127.0.0.1:8002"

def generate_user_id():
    return f"user_{int(time.time())}"

def print_scenario(name, order_data, expected_msg, expected_discount=None):
    print("\n" + "="*80)
    print(f"SCENARIO: {name}")
    print("="*80)
    print(f"Items: {[p['name'] + ' (' + str(p['price']) + ')' for p in order_data['products']]}")
    
    response = requests.post(f"{BASE_URL}/orders/", json=order_data)
    result = response.json()
    
    print(f"Total Amount: ₹{result['total_amount']}")
    print(f"Message: {result['message']}")
    if 'discount_percent' in result:
        print(f"Discount: {result['discount_percent']}%")
        
    # Validation
    if expected_msg in result['message']:
        print(" Message Verified")
    else:
        print(f" Message Mismatch (Expected: '{expected_msg}')")
        
    if expected_discount is not None:
        actual_discount = result.get('discount_percent', 0)
        if actual_discount == expected_discount:
            print(f" Discount Verified ({actual_discount}%)")
        else:
            print(f" Discount Mismatch (Expected {expected_discount}%, Got {actual_discount}%)")

def verify_all():
    # 1. Single Item Below Target (<1000) -> Upsell
    print_scenario(
        "1. Single Item Below Target (600)",
        {
            "user_id": generate_user_id(),
            "products": [{"name": "Item A", "price": 600, "quantity": 1}]
        },
        "Add ₹400 more",
        expected_discount=0
    )

    # 2. Rich Purchase (>1000) -> Exceeded (No Discount)
    print_scenario(
        "2. Single Item Above Target (1500) - NO DISCOUNT",
        {
            "user_id": generate_user_id(),
            "products": [{"name": "Big Item", "price": 1500, "quantity": 1}]
        },
        "valid only before reaching",
        expected_discount=0
    )

    # 3. Successful Step-by-Step (500 + 500)
    # Previous (500) < Target (1000) -> Unlock
    print_scenario(
        "3. Success Step-by-Step (500 + 500) -> 1000 Exact",
        {
            "user_id": generate_user_id(),
            "products": [
                {"name": "Item A", "price": 500, "quantity": 1},
                {"name": "Item B", "price": 500, "quantity": 1}
            ]
        },
        "You unlocked 10% discount",
        expected_discount=10
    )
    
    # 4. Bulk Abuse (1000 via Single Item x 1 or x 2)
    # Total 1000. Unique 1.
    print_scenario(
        "4. Bulk Abuse (Item A 1000) -> NO DISCOUNT",
        {
            "user_id": generate_user_id(),
            "products": [{"name": "Item A", "price": 1000, "quantity": 1}]
        },
        "Bulk purchases are not eligible",
        expected_discount=0
    )

    # 5. Overshot Step (600 + 600 = 1200) -> Missed Target
    print_scenario(
        "5. Overshot Step (600 + 600 = 1200) -> NO DISCOUNT",
        {
            "user_id": generate_user_id(),
            "products": [
                {"name": "Item A", "price": 600, "quantity": 1},
                {"name": "Item B", "price": 600, "quantity": 1}
            ]
        },
        "valid only before reaching",
        expected_discount=0
    )

if __name__ == "__main__":
    verify_all()
