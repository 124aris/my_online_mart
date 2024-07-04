from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from pydantic import EmailStr

class User(SQLModel, table = True):
    id: Optional[int] = Field(default = None, primary_key = True)
    name: str
    email: EmailStr
    password: str
    phone_number: int = Field(max_digits = 11)

class UserUpdate():
    id: Optional[int] = None
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    phone_number: Optional[int] = Field(default = None, max_digits = 11)