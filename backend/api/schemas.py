from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class UserBase(BaseModel):
    username: str
    email: str
    image: Optional[str] = None 

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    username: Optional[str] = None
    email: Optional[str] = None
    image: Optional[str] = None

class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

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
        orm_mode = True

class ChatRoomBase(BaseModel):
    name: str
    is_direct_message: bool = False

class ChatRoomCreate(ChatRoomBase):
    member_ids: List[int]  # IDs of users to add to the chat room

class ChatRoomResponse(ChatRoomBase):
    id: int
    created_at: datetime
    last_message: Optional[str] = None
    last_sender_id: Optional[int] = None
    members: List[ChatMemberResponse]

    class Config:
        orm_mode = True

class MessageBase(BaseModel):
    content: str

class MessageCreate(MessageBase):
    chat_room_id: int

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
        orm_mode = True

class MessageResponse(MessageBase):
    id: int
    sender_id: int
    chat_room_id: int
    created_at: datetime
    read: bool
    reactions: List[ReactionResponse]

    class Config:
        orm_mode = True