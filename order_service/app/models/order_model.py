from datetime import datetime, timezone
from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship

class Order(SQLModel, table=True):
    id: Optional[int] = Field(default = None, primary_key = True)
    order_id: int
    user_id: int
    product_id: int
    quantity: int
    address: str = Field(max_length = 60)
    total_price: float
    advance_price: Optional[float]
    type: str
    date: datetime = Field(default = datetime.now(timezone.utc))
    status: str = Field(default = "pending")
    items: List["OrderItem"] = Relationship(back_populates="order")

class OrderItem(SQLModel, table=True):
    order_item_id: Optional[int] = Field(default = None, primary_key = True)
    order_id: int
    product_id: int
    product_item_id: int
    product_size_id: int
    quantity: int = Field(gt = 0)
    order: Optional[Order] = Relationship(back_populates="items")

class OrderUpdate(SQLModel):
    order_id: Optional[int] = None
    user_id: Optional[int] = None
    product_id: Optional[int] = None
    quantity: Optional[int] = None
    address: Optional[str] = Field(default = None, max_length = 60)
    total_price: Optional[float] = None
    advance_price: Optional[float] = None
    type: Optional[str] = None
    date: Optional[datetime] = Field(default = datetime.now(timezone.utc))
    status: Optional[str] = Field(default = "pending")