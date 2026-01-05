from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.schemas.discount import DiscountCreate, DiscountUpdate, DiscountResponse
from app.services import discount_service

router = APIRouter(prefix="/discounts", tags=["discounts"])

@router.post("/", response_model=DiscountResponse, status_code=status.HTTP_201_CREATED)
def create_new_discount(discount: DiscountCreate, db: Session = Depends(get_db)):
    return discount_service.create_discount(db, discount)

@router.get("/", response_model=List[DiscountResponse])
def read_discounts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return discount_service.get_discounts(db, skip, limit)

@router.get("/{discount_id}", response_model=DiscountResponse)
def read_discount(discount_id: int, db: Session = Depends(get_db)):
    db_discount = discount_service.get_discount(db, discount_id)
    if db_discount is None:
        raise HTTPException(status_code=404, detail="Discount not found")
    return db_discount

@router.put("/{discount_id}", response_model=DiscountResponse)
def update_existing_discount(discount_id: int, discount: DiscountUpdate, db: Session = Depends(get_db)):
    db_discount = discount_service.update_discount(db, discount_id, discount)
    if db_discount is None:
        raise HTTPException(status_code=404, detail="Discount not found")
    return db_discount

@router.delete("/{discount_id}", response_model=DiscountResponse)
def delete_existing_discount(discount_id: int, db: Session = Depends(get_db)):
    db_discount = discount_service.delete_discount(db, discount_id)
    if db_discount is None:
        raise HTTPException(status_code=404, detail="Discount not found")
    return db_discount
