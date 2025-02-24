from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from .user import UserResponse

class MessageBase(BaseModel):
    body: Optional[str] = None
    image: Optional[str] = None
    conversationId: str

class MessageCreate(BaseModel):
    content: str  # Changed to match frontend expectation
    image: Optional[str] = None
    conversationId: str

class MessageResponse(BaseModel):
    id: str
    body: Optional[str] = None
    image: Optional[str] = None
    senderId: str
    conversationId: str
    createdAt: str  # ISO format string
    sender: Optional[UserResponse] = None  # Fetched from users table
