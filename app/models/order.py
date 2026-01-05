from sqlalchemy import Column, Integer, Float, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    total_amount = Column(Float, nullable=False)
    discount_amount = Column(Float, default=0.0)
    discount_percent = Column(Float, default=0.0)
    final_amount = Column(Float, nullable=False)
    product_count = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationship to OrderProduct
    products = relationship("OrderProduct", back_populates="order", cascade="all, delete-orphan")
