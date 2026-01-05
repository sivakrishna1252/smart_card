# Smart Cart Backend - FastAPI

A rule-based discount system for e-commerce with dynamic cart calculations.

## Project Structure

```
smart_cart/
├── app/
│   ├── main.py              # Application entry point
│   ├── core/
│   │   ├── config.py        # Configuration settings
│   │   └── database.py      # Database connection
│   ├── models/              # SQLAlchemy models
│   ├── schemas/             # Pydantic schemas
│   ├── services/            # Business logic
│   ├── api/                 # API endpoints
│   └── utils/               # Utility functions
├── requirements.txt
└── README.md
```

## Setup Instructions

### 1. Install Dependencies

```bash
cd smart_cart
pip install -r requirements.txt
```

### 2. Run the Application

From the `smart_cart` directory:

```bash
uvicorn app.main:app --reload
```

The server will start at: `http://127.0.0.1:8000`

### 3. Access API Documentation

Once the server is running, visit:
- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

## API Endpoints

### Discount Management

#### Create Discount
```bash
POST /discounts
Content-Type: application/json

{
  "min_amount": 800,
  "max_amount": 1500,
  "discount_percent": 10,
  "active": true
}
```

#### Get All Discounts
```bash
GET /discounts
```

#### Update Discount
```bash
PUT /discounts/{id}
Content-Type: application/json

{
  "min_amount": 800,
  "max_amount": 1500,
  "discount_percent": 15,
  "active": true
}
```

#### Delete Discount
```bash
DELETE /discounts/{id}
```

### Smart Cart

#### Calculate Cart with Discounts
```bash
POST /cart/smart
Content-Type: application/json

{
  "user_id": "user_123",
  "cart_total": 1000
}
```

**Response:**
```json
{
  "cart_total": 1000,
  "current_discount_percent": 10,
  "discount_amount": 100,
  "payable_amount": 900,
  "next_discount_percent": 20,
  "add_amount": 500,
  "message": "Add ₹500 more to get 20% discount"
}
```

### Orders

#### Place Order
```bash
POST /orders
Content-Type: application/json

{
  "user_id": "user_123",
  "cart_total": 2000
}
```

## Testing the API

### Using cURL

1. **Create discount rules:**
```bash
curl -X POST http://127.0.0.1:8000/discounts/ -H "Content-Type: application/json" -d "{\"min_amount\": 800, \"max_amount\": 1500, \"discount_percent\": 10, \"active\": true}"

curl -X POST http://127.0.0.1:8000/discounts/ -H "Content-Type: application/json" -d "{\"min_amount\": 1500, \"max_amount\": null, \"discount_percent\": 20, \"active\": true}"
```

2. **Test smart cart (cart < 800):**
```bash
curl -X POST http://127.0.0.1:8000/cart/smart -H "Content-Type: application/json" -d "{\"user_id\": \"user_123\", \"cart_total\": 500}"
```

3. **Test smart cart (800 ≤ cart < 1500):**
```bash
curl -X POST http://127.0.0.1:8000/cart/smart -H "Content-Type: application/json" -d "{\"user_id\": \"user_123\", \"cart_total\": 1000}"
```

4. **Test smart cart (cart ≥ 1500):**
```bash
curl -X POST http://127.0.0.1:8000/cart/smart -H "Content-Type: application/json" -d "{\"user_id\": \"user_123\", \"cart_total\": 2000}"
```

5. **Place an order:**
```bash
curl -X POST http://127.0.0.1:8000/orders/ -H "Content-Type: application/json" -d "{\"user_id\": \"user_123\", \"cart_total\": 2000}"
```

### Using Python Script

Run the verification script from the parent directory:

```bash
cd ..
python verify.py
```

## Discount Rules

Default discount structure:
- **Cart < ₹800**: 0% discount
- **₹800 ≤ Cart < ₹1500**: 10% discount
- **Cart ≥ ₹1500**: 20% discount

All rules are data-driven and can be modified via the Discount CRUD APIs.

## Database

The application uses SQLite by default (`smart_cart.db`). To use PostgreSQL or MySQL, update the `DATABASE_URL` in `app/core/config.py` or set it as an environment variable.

## Features

✅ Data-driven discount rules  
✅ CRUD operations for discounts  
✅ Stateless smart cart calculations  
✅ Dynamic discount suggestions  
✅ Order placement with automatic discount application  
✅ Clean architecture with separation of concerns  
✅ Automatic API documentation (Swagger/ReDoc)

## Notes

- The Smart Cart API is stateless and recalculates on every request
- Discounts are sorted by `min_amount` to determine the best applicable discount
- The `max_amount` field can be `null` for unlimited upper bounds
- Orders automatically use the latest discount calculations
