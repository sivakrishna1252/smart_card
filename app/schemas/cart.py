from pydantic import BaseModel
from typing import Optional

class CartRequest(BaseModel):
    user_id: str
    unique_products_count: int
    cart_total: float

class CartResponse(BaseModel):
    cart_total: float
    unique_products_count: int
    discount_percent: float
    discount_amount: float
    payable_amount: float
    message: str
