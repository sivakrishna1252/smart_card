from sqlalchemy.orm import Session
from app.models.order import Order
from app.models.order_product import OrderProduct
from app.schemas.order import OrderCreate
from app.schemas.product import OrderProductResponse

def create_order(db: Session, order_data: OrderCreate):
    from app.services.discount_service import get_active_discounts

    # 1. Fetch Configuration
    active_discounts = get_active_discounts(db)
    sorted_rules = sorted(active_discounts, key=lambda r: r.minimum_threshold)

    # 2. Calculate Totals
    current_total = sum(p.price * p.quantity for p in order_data.products)
    
    # Identify the value of the very first item added to the cart
    if not order_data.products:
        first_item_value = 0
    else:
        first_product = order_data.products[0]
        first_item_value = first_product.price * first_product.quantity
        
    last_product = order_data.products[-1] if order_data.products else None
    last_item_value = last_product.price * last_product.quantity if last_product else 0
    previous_total = current_total - last_item_value
    
    # 3. Apply Status Logic
    final_percent = 0.0
    message = "Order placed successfully!"
    
    # Find current eligible discount (Highest r where current >= threshold and first_item < threshold)
    eligible_rules = [r for r in sorted_rules if current_total >= (r.minimum_threshold - 0.1) 
                     and first_item_value < (r.minimum_threshold - 0.1)]
    
    best_current_rule = None
    if eligible_rules:
        best_current_rule = max(eligible_rules, key=lambda r: r.discount_percent)
        final_percent = best_current_rule.discount_percent

    # Messaging Logic:
    # 1. Check if we JUST crossed a threshold that gave us a better discount
    newly_unlocked = False
    for rule in sorted_rules:
        # If we just crossed this threshold (prev was below, current is above)
        # AND it was a valid incremental move (first item was below)
        if (previous_total < (rule.minimum_threshold - 0.1) and 
            current_total >= (rule.minimum_threshold - 0.1) and 
            first_item_value < (rule.minimum_threshold - 0.1)):
            
            message = f"You unlocked {int(rule.discount_percent)}% discount 🎉"
            newly_unlocked = True
            # We continue checking in case multiple tiers crossed, but we want the highest current percent
            if rule.discount_percent > 0:
                final_percent = rule.discount_percent

    # 2. If not newly unlocked, show Motivator for the NEXT tier
    if not newly_unlocked:
        next_rule = None
        for rule in sorted_rules:
            if rule.minimum_threshold > (current_total + 0.1):
                next_rule = rule
                break
                
        if next_rule:
            needed = next_rule.minimum_threshold - current_total
            message = f"Add ₹{needed:.0f} more to unlock {int(next_rule.discount_percent)}% discount."
        else:
            message = "Order placed successfully!"

    # 4. Calculate Final Values
    discount_amount = (current_total * final_percent) / 100
    final_amount = current_total - discount_amount
    
    # Create DB Record
    db_order = Order(
        user_id=order_data.user_id,
        total_amount=current_total,
        discount_amount=discount_amount,
        discount_percent=final_percent,
        final_amount=final_amount,
        product_count=len(order_data.products)
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    
    # Add Products
    order_products = []
    for product in order_data.products:
        db_order_product = OrderProduct(
            order_id=db_order.id,
            product_name=product.name,
            product_price=product.price,
            quantity=product.quantity
        )
        db.add(db_order_product)
        order_products.append(db_order_product)
        
    db.commit()
    
    # Response Construction
    products_response = []
    receipt_lines = []
    
    for idx, op in enumerate(order_products):
        line_subtotal = op.product_price * op.quantity
        products_response.append({
            "product_number": idx + 1,
            "product_name": op.product_name,
            "product_price": op.product_price,
            "quantity": op.quantity,
            "subtotal": line_subtotal
        })
        receipt_lines.append(f"{idx+1}. {op.product_name} (x{op.quantity}): ₹{line_subtotal}")

    receipt_lines.append("-" * 20)
    receipt_lines.append(f"Total Amount: ₹{current_total:.1f}")
    if discount_amount > 0:
        receipt_lines.append(f"Discount ({int(final_percent)}%): -₹{discount_amount:.0f}")
    else:
        receipt_lines.append("Discount: ₹0")
    receipt_lines.append("-" * 20)
    receipt_lines.append(f"Payable Amount: ₹{final_amount:.1f}")
    
    # User stats
    user_orders = db.query(Order).filter(Order.user_id == order_data.user_id).all()
    
    return {
        "user_id": db_order.user_id,
        "total_amount": db_order.total_amount,
        "discount_percent": db_order.discount_percent,
        "discount_amount": db_order.discount_amount,
        "payable_amount": db_order.final_amount,
        "product_count": db_order.product_count,
        "products": products_response,
        "message": message,
        "receipt_text": receipt_lines,
        "user_total_orders": len(user_orders)
    }
