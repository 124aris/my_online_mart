from sqlmodel import SQLModel, Field, Relationship
from typing import Optional

class Product(SQLModel, table = True):
    id: Optional[int] = Field(default = None, primary_key = True)
    name: str
    description: str
    price: float
    expiry: Optional[str] = None
    brand: Optional[str] = None
    weight: Optional[float] = None
    category: str
    sku: Optional[str] = None
    # rating: list["ProductRating"] = Relationship(back_populates = 'product')
    # image: str
    # quantity: Optional[int] = None
    # color: Optional[str] = None
    # rating: Optional[float] = None

#class ProductRating(SQLModel, table = True):
#    id: Optional[int] = Field(default = None, primary_key = True)
#    product_id: int = Field(foreign_key = "product.id")
#    rating: int
#    review: Optional[str] = None
#    product = Relationship(back_populates = 'rating')
#     user_id: int

class ProductUpdate(SQLModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    expiry: Optional[str] = None
    brand: Optional[str] = None
    weight: Optional[float] = None
    category: Optional[str] = None
    sku: Optional[str] = None