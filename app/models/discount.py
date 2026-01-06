from sqlalchemy import Column, Integer, Float, Boolean
from app.core.database import Base



class Discount(Base):
    __tablename__ = "discounts"

    id = Column(Integer, primary_key=True, index=True)
    min_unique_products = Column(Integer, nullable=False, default=3)
    target_amount = Column(Float, nullable=False, default=10000)
    discount_percent = Column(Float, nullable=False, default=10)
    max_discount_cap = Column(Float, nullable=False, default=800)
    active = Column(Boolean, default=True)

