from fastapi import HTTPException
from sqlmodel import Session, select
from app.models.order_model import Order, OrderUpdate

def add_new_order(order_data: Order, session: Session):
    session.add(order_data)
    session.commit()
    session.refresh(order_data)
    return order_data

def get_all_orders(session: Session):
    all_orders = session.exec(select(Order)).all()
    return all_orders

def get_order_by_id(order_id: int, session: Session):
    order = session.exec(select(Order).where(Order.id == order_id)).one_or_none()
    if order is None:
        raise HTTPException(status_code = 404, detail = "Order Not Found")
    return order

def delete_order_by_id(order_id: int, session: Session):
    order = session.exec(select(Order).where(Order.id == order_id)).one_or_none()
    if order is None:
        raise HTTPException(status_code = 404, detail = "Order Not Found")
    session.delete(order)
    session.commit()
    return{"message": "Order Deleted Successfully"}

def update_order_by_id(order_id: int, to_update_order_data: OrderUpdate, session: Session):
    order = session.exec(select(Order).where(Order.id == order_id)).one_or_none()
    if order is None:
        raise HTTPException(status_code = 404, detail = "Order Not Found")
    hero_data = to_update_order_data.model_dump(exclude_unset = True)
    order.sqlmodel_update(hero_data)
    session.add(order)
    session.commit()
    return order