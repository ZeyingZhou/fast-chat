from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from .user import UserResponse
from .message import MessageResponse

class ConversationBase(BaseModel):
    name: Optional[str] = None
    isGroup: Optional[bool] = False
    userIds: List[str] = []
    messagesIds: List[str] = []

class ConversationCreate(BaseModel):
    isGroup: Optional[bool] = False
    members: List[str] = []
    name: Optional[str] = None
    userId: Optional[str] = None


class ConversationUpdate(BaseModel):
    name: Optional[str] = None
    lastMessageAt: datetime = datetime.now()
    messagesIds: Optional[List[str]] = None

class ConversationResponse(BaseModel):
    id: str
    createdAt: datetime
    lastMessageAt: datetime
    name: Optional[str] = None
    isGroup: Optional[bool] = False
    messagesIds: List[str] = []
    userIds: List[str]
    users: List[UserResponse]
    messages: Optional[List[MessageResponse]] = None