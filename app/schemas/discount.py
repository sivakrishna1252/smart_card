from pydantic import BaseModel

class DiscountBase(BaseModel):
    min_unique_products: int = 3
    target_amount: float = 10000
    discount_percent: float = 10
    max_discount_cap: float = 800
    active: bool = True

class DiscountCreate(DiscountBase):
    pass

class DiscountUpdate(DiscountBase):
    pass

class DiscountResponse(DiscountBase):
    id: int

    class Config:
        from_attributes = True

