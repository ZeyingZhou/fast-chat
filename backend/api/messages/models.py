from sqlalchemy import Boolean, Column, Integer, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base

class Message(Base):
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text)
    sender_id = Column(Integer, ForeignKey("users.id"))
    chat_room_id = Column(Integer, ForeignKey("chat_rooms.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    read = Column(Boolean, default=False)

    # Relationships
    sender = relationship("User", back_populates="messages")
    chat_room = relationship("ChatRoom", back_populates="messages")
    reactions = relationship("Reaction", back_populates="message")
