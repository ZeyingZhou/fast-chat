from sqlalchemy import Column, DateTime, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base

class ChatMember(Base):
    __tablename__ = "chat_members"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    chat_room_id = Column(Integer, ForeignKey("chat_rooms.id"))
    joined_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="chat_memberships")
    chat_room = relationship("ChatRoom", back_populates="members")