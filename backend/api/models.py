from sqlalchemy import Boolean, Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    image = Column(String)
    hashed_password = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    messages = relationship("Message", back_populates="sender")
    reactions = relationship("Reaction", back_populates="user")
    chat_memberships = relationship("ChatMember", back_populates="user")

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

class ChatMember(Base):
    __tablename__ = "chat_members"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    chat_room_id = Column(Integer, ForeignKey("chat_rooms.id"))
    joined_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="chat_memberships")
    chat_room = relationship("ChatRoom", back_populates="members")

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

class Reaction(Base):
    __tablename__ = "reactions"

    id = Column(Integer, primary_key=True, index=True)
    emoji = Column(String)  # Store the raw emoji character
    user_id = Column(Integer, ForeignKey("users.id"))
    message_id = Column(Integer, ForeignKey("messages.id"))
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="reactions")
    message = relationship("Message", back_populates="reactions")