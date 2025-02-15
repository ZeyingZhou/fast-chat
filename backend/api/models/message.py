from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from .user import UserResponse  # You'll need to import your user model

class MessageBase(BaseModel):
    body: Optional[str] = None
    image: Optional[str] = None
    conversationId: str
    senderId: str
    seenIds: List[str] = []

class MessageCreate(MessageBase):
    id: str
    createdAt: datetime = datetime.now()

class MessageUpdate(BaseModel):
    body: Optional[str] = None
    image: Optional[str] = None
    seenIds: Optional[List[str]] = None

class MessageResponse(MessageCreate):
    sender: UserResponse
    seen: List[UserResponse]
