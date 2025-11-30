from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from Database.dbConnect import get_db
from Database.dbModels import Order, OrderCreate, OrderItem, OrderItemCreate, OrderStatus, User

router = APIRouter()

@router.post("/")
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    if not order.items:
        raise HTTPException(status_code=400, detail="Order must contain items")

    user = db.query(User).filter(User.user_id == order.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    new_order = Order(
        status=OrderStatus.PENDING,
        user_id=user.user_id,
        phone_num=order.phone_num
    )
    db.add(new_order)
    db.flush()

    for item in order.items:
        order_item = OrderItem(
            order_id=new_order.id,
            item_id=item.item_id,
            quantity=item.quantity,
            price_at_order=db.query(Item).filter(Item.id==item.item_id).first().price
        )
        db.add(order_item)

    db.commit()
    return {"message": f"Order {new_order.id} created!"}

@router.get("/search/{phone}")
def search_orders(phone: str, db: Session = Depends(get_db)):
    orders = db.query(Order).filter(Order.phone_num==phone).all()
    if not orders:
        raise HTTPException(status_code=404, detail="No orders found")
    return orders
