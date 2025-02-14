from pydantic import BaseModel
from pydantic import ConfigDict
from typing import Optional
from typing import List
from datetime import datetime

class ConversationBase(BaseModel):
    name: str
    userId: str

class ConversationCreate(BaseModel):
    userId: str
    isGroup: bool = False
    members: list = []
    name: Optional[str] = None

class ConversationUpdate(BaseModel):
    name: Optional[str] = None
    messageIds: Optional[List[str]] = None
    updatedAt: datetime

class ConversationResponse(ConversationCreate):
    pass