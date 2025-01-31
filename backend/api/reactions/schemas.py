from pydantic import BaseModel
from datetime import datetime

class ReactionBase(BaseModel):
    emoji: str
    message_id: int

class ReactionCreate(ReactionBase):
    pass

class ReactionResponse(ReactionBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True
