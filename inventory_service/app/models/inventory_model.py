from sqlmodel import SQLModel, Field, Relationship
from typing import Optional

class InventoryItem(SQLModel, table = True):
    id: Optional[int] = Field(default = None, primary_key = True)
    product_id: int
    variant_id: Optional[int] = None
    quantity: int
    status: str 

class InventoryItemUpdate(SQLModel):
    id: Optional[int] = None
    product_id: Optional[int] = None
    variant_id: Optional[int] = None
    quantity: Optional[int] = None
    status: Optional[str] = None 