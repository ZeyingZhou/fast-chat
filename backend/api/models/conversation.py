from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List, Dict
from .user import UserResponse
from .message import MessageResponse

class ConversationBase(BaseModel):
    name: Optional[str] = None
    isGroup: str = 'false'  # Changed to string to match DynamoDB

class ConversationCreate(BaseModel):
    isGroup: bool = False  # Keep as bool for API input
    members: List[Dict[str, str]] = []  # For group members
    name: Optional[str] = None
    userId: Optional[str] = None  # For direct messages

class ConversationUpdate(BaseModel):
    name: Optional[str] = None
    lastMessageAt: datetime = datetime.now()
    messagesIds: Optional[List[str]] = None

class ConversationResponse(BaseModel):
    id: str
    createdAt: str  # ISO format string
    lastMessageAt: str  # ISO format string
    name: Optional[str] = None
    isGroup: str = 'false'  # String to match DynamoDB
    users: List[UserResponse]  # Users are fetched through conversation_users table