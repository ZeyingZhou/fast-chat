from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import HttpUrl
from typing import Optional
from typing import List
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    username: str = ""
    name: str = ""
    image: Optional[str] = None

class UserCreate(UserBase):
    id: str
    conversationIds: List[str] = []
    seenMessageIds: List[str] = []
    createdAt: str
    updatedAt: str

class UserUpdate(UserBase):
    updatedAt: str

UserResponse = UserCreate
