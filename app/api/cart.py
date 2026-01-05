from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.cart import CartRequest, CartResponse
from app.services import cart_service

router = APIRouter(prefix="/cart", tags=["cart"])

@router.post("/check", response_model=CartResponse)
def check_smart_cart(request: CartRequest, db: Session = Depends(get_db)):
    return cart_service.calculate_cart(db, request.unique_products_count, request.cart_total)
