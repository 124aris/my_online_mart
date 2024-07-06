from datetime import datetime, timezone
from typing import Optional
from sqlmodel import Field, SQLModel

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