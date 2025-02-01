from sqlalchemy import Boolean, Column, Integer, String, DateTime
from datetime import datetime
from ..database import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String, nullable=True)
    image = Column(String, nullable=True)
    is_social = Column(Boolean, default=False)
    social_provider = Column(String, nullable=True)
    social_id = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    # Relationships
    messages = relationship("Message", back_populates="sender")
    reactions = relationship("Reaction", back_populates="user")
    chat_memberships = relationship("ChatMember", back_populates="user")
