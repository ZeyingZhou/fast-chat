from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from ..chat_members.schemas import ChatMemberResponse

class ChatRoomBase(BaseModel):
    name: str
    is_direct_message: bool = False

class ChatRoomCreate(ChatRoomBase):
    member_ids: List[int]

class ChatRoomResponse(ChatRoomBase):
    id: int
    created_at: datetime
    last_message: Optional[str] = None
    last_sender_id: Optional[int] = None
    members: List[ChatMemberResponse]

    class Config:
        from_attributes = True
