from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
#from pydantic import EmailStr

class User(SQLModel, table = True):
    id: Optional[int] = Field(default = None, primary_key = True)
    name: str
    email: str
    password: str
    phone_number: int
    
class UserUpdate(SQLModel):
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    phone_number: Optional[int] = None