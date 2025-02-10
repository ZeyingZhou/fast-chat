from pydantic import BaseModel
from pydantic import ConfigDict
from typing import Optional
from typing import List
from datetime import datetime

class ConversationBase(BaseModel):
    name: str
    userId: str

class ConversationCreate(ConversationBase):
    id: str
    messageIds: List[str] = []
    createdAt: datetime
    updatedAt: datetime

class ConversationUpdate(BaseModel):
    name: Optional[str] = None
    messageIds: Optional[List[str]] = None
    updatedAt: datetime

class ConversationResponse(ConversationCreate):
    pass