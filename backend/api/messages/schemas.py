from pydantic import BaseModel
from datetime import datetime
from typing import List
from ..reactions.schemas import ReactionResponse

class MessageBase(BaseModel):
    content: str

class MessageCreate(MessageBase):
    chat_room_id: int

class MessageResponse(MessageBase):
    id: int
    sender_id: int
    chat_room_id: int
    created_at: datetime
    read: bool
    reactions: List[ReactionResponse]

    class Config:
        from_attributes = True
