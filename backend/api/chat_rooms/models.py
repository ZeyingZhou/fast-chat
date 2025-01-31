from sqlalchemy import Boolean, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base

class ChatRoom(Base):
    __tablename__ = "chat_rooms"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    is_direct_message = Column(Boolean, default=False)
    last_message = Column(String)
    last_sender_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    messages = relationship("Message", back_populates="chat_room")
    members = relationship("ChatMember", back_populates="chat_room")
