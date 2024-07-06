from sqlmodel import Session, select
from fastapi import HTTPException
from app.models.payment_model import Payment

def create_new_payment(payment: Payment, session: Session):
    session.add(payment)
    session.commit()
    session.refresh(payment)
    return payment

def get_payment_by_id(payment_id: int, session: Session):
    payment = session.exec(select(Payment).where(Payment.payment_id == payment_id)).one_or_none()
    if payment is None:
        raise HTTPException(status_code = 404, detail = "Payment Not Found")
    return payment