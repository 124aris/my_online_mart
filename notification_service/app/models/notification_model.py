from pydantic import BaseModel, EmailStr
from typing import List, Optional

class Email(BaseModel):
    email: List[EmailStr]
    notification_type: Optional[str]