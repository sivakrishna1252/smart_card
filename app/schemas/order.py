from pydantic import BaseModel
from typing import List
from app.schemas.product import OrderProductInput

class OrderCreate(BaseModel):
    user_id: str
    products: List[OrderProductInput]

class OrderResponse(BaseModel):
    user_id: str
    total_amount: float
    discount_percent: float
    discount_amount: float
    payable_amount: float
    product_count: int
    products: List[dict]  # Simple dict with product_number, name, price, quantity, subtotal
    message: str
    receipt_text: List[str]  # Visual breakdown of the bill
    user_total_orders: int

    class Config:
        from_attributes = True

