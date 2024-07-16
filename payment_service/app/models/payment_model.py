from typing import Optional
from sqlmodel import Relationship, SQLModel, Field

class RemainingPayment(SQLModel):
    order_id: int 
    total_price: int
    payment_method: Optional[str]
    payment_method_id: str
    remaining_balance: float

class PaymentForm(SQLModel):
    order_id: int
    total_price: int
    payment_method: Optional[str]
    payment_method_id: Optional[str]
    advance_payment: Optional["AdvancePayment"]

class Payment(SQLModel, table = True):
    order_id: int
    total_price: int
    payment_method: Optional[str]
    payment_id: int = Field(primary_key = True)
    payment_intent_id: Optional[str]
    payment_status: str
    remaining_balance: float = Field(default = 0)
    is_completed: bool = Field(default = False)
    advance_payment: Optional["AdvancePayment"] = Relationship(back_populates = "payment")

class AdvancePayment(SQLModel, table=True):
    advance_price: int
    advance_payment_method: str
    advance_payment_id: Optional[int] = Field(primary_key = True)
    payment_id: int = Field(foreign_key = "payment.payment_id")
    advance_payment_intent_id: str
    advance_payment_status: str
    payment: Optional[Payment] = Relationship(back_populates = "advance_payment")