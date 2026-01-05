import requests
import json
import time

BASE_URL = "http://localhost:8080"

def test_flow():
    print("Starting verification mowa...")
    
    # 1. Create a Discount
    discount_data = {
        "min_unique_products": 3,
        "target_amount": 10000,
        "discount_percent": 10,
        "max_discount_cap": 800,
        "active": True
    }
    
    try:
        # Create
        print("\n1. Creating discount rule (3 prods, 10k target, 10% disc, 800 cap)...")
        resp = requests.post(f"{BASE_URL}/discounts/", json=discount_data)
        print(f"Status: {resp.status_code}")
        discount = resp.json()
        print(json.dumps(discount, indent=2))
        discount_id = discount['id']

        # 2. Get All
        print("\n2. Getting all discounts...")
        resp = requests.get(f"{BASE_URL}/discounts/")
        print(f"Status: {resp.status_code}")
        print(f"Count: {len(resp.json())}")

        # 3. Get One
        print(f"\n3. Getting discount with ID {discount_id}...")
        resp = requests.get(f"{BASE_URL}/discounts/{discount_id}")
        print(f"Status: {resp.status_code}")
        print(json.dumps(resp.json(), indent=2))

        # 4. Check Smart Cart - Scenario 1: Missing Products
        print("\n4. Scenario 1: 2 products, 11000 total (Missing 1 product)...")
        cart_data = {
            "user_id": "mowa123",
            "unique_products_count": 2,
            "cart_total": 11000
        }
        resp = requests.post(f"{BASE_URL}/cart/check", json=cart_data)
        print(f"Status: {resp.status_code}")
        print(json.dumps(resp.json(), indent=2))
        
        # 5. Check Smart Cart - Scenario 2: Missing Amount
        print("\n5. Scenario 2: 3 products, 9000 total (Missing 1000 amount)...")
        cart_data = {
            "unique_products_count": 3,
            "cart_total": 9000,
            "user_id": "mowa123"
        }
        resp = requests.post(f"{BASE_URL}/cart/check", json=cart_data)
        print(f"Status: {resp.status_code}")
        print(json.dumps(resp.json(), indent=2))

        # 6. Check Smart Cart - Scenario 3: Success with Cap
        print("\n6. Scenario 3: 3 products, 12000 total (Should get 800 cap discount)...")
        cart_data = {
            "unique_products_count": 3,
            "cart_total": 12000,
            "user_id": "mowa123"
        }
        resp = requests.post(f"{BASE_URL}/cart/check", json=cart_data)
        print(f"Status: {resp.status_code}")
        print(json.dumps(resp.json(), indent=2))

        # 7. Update Discount
        print(f"\n7. Updating discount ID {discount_id} to 20%...")
        update_data = {"discount_percent": 20}
        resp = requests.put(f"{BASE_URL}/discounts/{discount_id}", json=update_data)
        print(f"Status: {resp.status_code}")
        print(json.dumps(resp.json(), indent=2))

        # 8. Delete
        print(f"\n8. Deleting discount ID {discount_id}...")
        resp = requests.delete(f"{BASE_URL}/discounts/{discount_id}")
        print(f"Status: {resp.status_code}")
        print(f"Deleted: {resp.json().get('id') == discount_id}")

    except Exception as e:
        print(f"Error during verification: {e}")

if __name__ == "__main__":
    test_flow()
