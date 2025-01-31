from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..messages import models as messages_models
from ..messages import schemas as messages_schemas
from ..users import models as users_models

from ..auth import get_current_user

router = APIRouter(
    prefix="/messages",
    tags=["messages"]
)

@router.post("/", response_model=messages_schemas.MessageResponse)
def create_message(
    message: messages_schemas.MessageCreate,
    db: Session = Depends(get_db),
    current_user: users_models.User = Depends(get_current_user)
):
    # Create the message
    db_message = messages_models.Message(
        content=message.content,
        sender_id=current_user.id,
        chat_room_id=message.chat_room_id
    )
    db.add(db_message)
    
    # Update the chat room's last message
    chat_room = db.query(messages_models.ChatRoom).filter(
        messages_models.ChatRoom.id == message.chat_room_id
    ).first()
    
    chat_room.last_message = message.content
    chat_room.last_sender_id = current_user.id
    
    db.commit()
    db.refresh(db_message)
    return db_message

@router.get("/", response_model=List[messages_schemas.MessageResponse])
def get_messages(
    other_user_id: int,
    db: Session = Depends(get_db),
    current_user: users_models.User = Depends(get_current_user)
):
    messages = db.query(messages_models.Message).filter(
        (
            (messages_models.Message.sender_id == current_user.id) & 
            (messages_models.Message.receiver_id == other_user_id)
        ) |
        (
            (messages_models.Message.sender_id == other_user_id) & 
            (messages_models.Message.receiver_id == current_user.id)
        )
    ).order_by(messages_models.Message.created_at.desc()).all()
    return messages

@router.put("/{message_id}/read")
def mark_message_as_read(
    message_id: int,
    db: Session = Depends(get_db),
    current_user: users_models.User = Depends(get_current_user)
):
    message = db.query(messages_models.Message).filter(messages_models.Message.id == message_id).first()
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    if message.receiver_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to mark this message as read")
    
    message.read = True
    db.commit()
    return {"status": "success"}