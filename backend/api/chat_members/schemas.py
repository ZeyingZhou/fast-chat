from pydantic import BaseModel
from datetime import datetime
from ..users.schemas import UserResponse

class ChatMemberBase(BaseModel):
    user_id: int
    chat_room_id: int

class ChatMemberCreate(ChatMemberBase):
    pass

class ChatMemberResponse(ChatMemberBase):
    id: int
    joined_at: datetime
    user: UserResponse

    class Config:
        from_attributes = True
