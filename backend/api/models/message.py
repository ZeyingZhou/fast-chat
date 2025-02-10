from pydantic import BaseModel
from pydantic import ConfigDict
from typing import Optional
from datetime import datetime

class MessageBase(BaseModel):
    content: str
    role: str
    conversationId: str

class MessageCreate(MessageBase):
    id: str
    userId: str
    createdAt: datetime
    updatedAt: datetime

class MessageUpdate(BaseModel):
    content: Optional[str] = None
    updatedAt: datetime

class MessageResponse(MessageCreate):
    pass