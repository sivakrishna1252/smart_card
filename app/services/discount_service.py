from sqlalchemy.orm import Session
from app.models.discount import Discount
from app.schemas.discount import DiscountCreate, DiscountUpdate

def get_discount(db: Session, discount_id: int):
    return db.query(Discount).filter(Discount.id == discount_id).first()

def get_discounts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Discount).offset(skip).limit(limit).all()

def get_active_discounts(db: Session):
    return db.query(Discount).filter(Discount.active == True).order_by(Discount.target_amount).all()

def create_discount(db: Session, discount: DiscountCreate):
    # Find the smallest available ID (fill the "holes")
    existing_ids = db.query(Discount.id).order_by(Discount.id).all()
    existing_ids = [id_tuple[0] for id_tuple in existing_ids]
    
    new_id = 1
    for eid in existing_ids:
        if eid == new_id:
            new_id += 1
        elif eid > new_id:
            break
            
    db_discount = Discount(id=new_id, **discount.model_dump())
    db.add(db_discount)
    db.commit()
    db.refresh(db_discount)
    return db_discount

def update_discount(db: Session, discount_id: int, discount: DiscountUpdate):
    db_discount = get_discount(db, discount_id)
    if not db_discount:
        return None
    update_data = discount.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_discount, key, value)
    db.add(db_discount)
    db.commit()
    db.refresh(db_discount)
    return db_discount

def delete_discount(db: Session, discount_id: int):
    db_discount = get_discount(db, discount_id)
    if db_discount:
        db.delete(db_discount)
        db.commit()
    return db_discount
