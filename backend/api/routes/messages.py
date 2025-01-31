from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from .. import models, schemas
from ..auth import get_current_user

router = APIRouter(
    prefix="/messages",
    tags=["messages"]
)

@router.post("/", response_model=schemas.MessageResponse)
def create_message(
    message: schemas.MessageCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    # Create the message
    db_message = models.Message(
        content=message.content,
        sender_id=current_user.id,
        chat_room_id=message.chat_room_id
    )
    db.add(db_message)
    
    # Update the chat room's last message
    chat_room = db.query(models.ChatRoom).filter(
        models.ChatRoom.id == message.chat_room_id
    ).first()
    
    chat_room.last_message = message.content
    chat_room.last_sender_id = current_user.id
    
    db.commit()
    db.refresh(db_message)
    return db_message

@router.get("/", response_model=List[schemas.MessageResponse])
def get_messages(
    other_user_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    messages = db.query(models.Message).filter(
        (
            (models.Message.sender_id == current_user.id) & 
            (models.Message.receiver_id == other_user_id)
        ) |
        (
            (models.Message.sender_id == other_user_id) & 
            (models.Message.receiver_id == current_user.id)
        )
    ).order_by(models.Message.created_at.desc()).all()
    return messages

@router.put("/{message_id}/read")
def mark_message_as_read(
    message_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    message = db.query(models.Message).filter(models.Message.id == message_id).first()
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    if message.receiver_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to mark this message as read")
    
    message.read = True
    db.commit()
    return {"status": "success"}