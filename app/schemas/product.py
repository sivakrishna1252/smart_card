from pydantic import BaseModel
from datetime import datetime

class ProductCreate(BaseModel):
    name: str
    price: float

class ProductResponse(BaseModel):
    id: int
    name: str
    price: float
    created_at: datetime

    class Config:
        from_attributes = True

class OrderProductInput(BaseModel):
    name: str
    price: float
    quantity: int = 1

class OrderProductResponse(BaseModel):
    id: int
    product_name: str
    product_price: float
    quantity: int

    class Config:
        from_attributes = True
