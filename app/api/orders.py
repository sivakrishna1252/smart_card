from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.order import OrderCreate, OrderResponse
from app.services import order_service

router = APIRouter(prefix="/orders", tags=["orders"])

@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def place_order(order: OrderCreate, db: Session = Depends(get_db)):
    try:
        return order_service.create_order(db, order)
    except Exception as e:
        import traceback
        print(f"Error placing order: {e}")
        traceback.print_exc()
        raise e
