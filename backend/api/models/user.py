from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    email: str
    name: Optional[str] = None
    image: Optional[str] = None

class UserResponse(UserBase):
    id: str
    createdAt: Optional[str] = None  # ISO format string
