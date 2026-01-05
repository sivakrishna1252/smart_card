from sqlalchemy.orm import Session
from app.services.discount_service import get_active_discounts
from app.schemas.cart import CartResponse

def calculate_cart(db: Session, unique_products_count: int, cart_total: float) -> CartResponse:
    discounts = get_active_discounts(db)
    
    applicable_discount = None
    
    # Sort discounts by target_amount descending to find the best applicable one first
    sorted_discounts = sorted(discounts, key=lambda x: x.target_amount, reverse=True)
    
    # 1. Check for the best applicable discount
    for d in sorted_discounts:
        if unique_products_count >= d.min_unique_products and cart_total >= d.target_amount:
            applicable_discount = d
            break
            
    if applicable_discount:
        discount_percent = applicable_discount.discount_percent
        discount_amount = (cart_total * discount_percent) / 100
        # Apply cap (max amount mowa)
        if discount_amount > applicable_discount.max_discount_cap:
            discount_amount = applicable_discount.max_discount_cap
            
        payable_amount = cart_total - discount_amount
        message = f"You unlocked {int(discount_percent)}% discount 🎉"
        
        return CartResponse(
            cart_total=cart_total,
            unique_products_count=unique_products_count,
            discount_percent=discount_percent,
            discount_amount=discount_amount,
            payable_amount=payable_amount,
            message=message
        )

    # 2. If no discount applied, find the closest one to suggest
    # Sort by target_amount ascending to find the smallest threshold they haven't reached
    sorted_asc = sorted(discounts, key=lambda x: x.target_amount)
    
    for d in sorted_asc:
        # Scenario 1: Missing products
        if cart_total >= d.target_amount and unique_products_count < d.min_unique_products:
            missing_prods = d.min_unique_products - unique_products_count
            message = f"Add {missing_prods} more product{'s' if missing_prods > 1 else ''} to get discount"
            return CartResponse(
                cart_total=cart_total,
                unique_products_count=unique_products_count,
                discount_percent=0,
                discount_amount=0,
                payable_amount=cart_total,
                message=message
            )
        # Scenario 2: Missing amount
        if cart_total < d.target_amount:
            missing_amount = d.target_amount - cart_total
            message = f"Add ₹{int(missing_amount)} to get {int(d.discount_percent)}% discount"
            return CartResponse(
                cart_total=cart_total,
                unique_products_count=unique_products_count,
                discount_percent=0,
                discount_amount=0,
                payable_amount=cart_total,
                message=message
            )

    # Default if no discounts configured or nothing matches
    return CartResponse(
        cart_total=cart_total,
        unique_products_count=unique_products_count,
        discount_percent=0,
        discount_amount=0,
        payable_amount=cart_total,
        message="Add products and build your cart to unlock discounts!"
    )
