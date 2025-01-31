from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from .. import models, schemas
from ..auth import get_current_user

router = APIRouter(
    prefix="/chat-rooms",
    tags=["chat-rooms"]
)

@router.post("/", response_model=schemas.ChatRoomResponse)
def create_chat_room(
    chat_room: schemas.ChatRoomCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    # Create new chat room
    db_chat_room = models.ChatRoom(
        name=chat_room.name,
        is_direct_message=chat_room.is_direct_message
    )
    db.add(db_chat_room)
    db.commit()
    db.refresh(db_chat_room)
    
    # Add members to the chat room
    member_ids = set(chat_room.member_ids + [current_user.id])
    for user_id in member_ids:
        chat_member = models.ChatMember(
            user_id=user_id,
            chat_room_id=db_chat_room.id
        )
        db.add(chat_member)
    
    db.commit()
    db.refresh(db_chat_room)
    return db_chat_room

@router.get("/", response_model=List[schemas.ChatRoomResponse])
def get_chat_rooms(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    # Get all chat rooms where the user is a member
    chat_members = db.query(models.ChatMember).filter(
        models.ChatMember.user_id == current_user.id
    ).all()
    return [member.chat_room for member in chat_members]

@router.get("/{chat_room_id}", response_model=schemas.ChatRoomResponse)
def get_chat_room(
    chat_room_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    # Check if user is a member of the chat room
    chat_member = db.query(models.ChatMember).filter(
        models.ChatMember.chat_room_id == chat_room_id,
        models.ChatMember.user_id == current_user.id
    ).first()
    
    if not chat_member:
        raise HTTPException(status_code=403, detail="Not a member of this chat room")
    
    return chat_member.chat_room

@router.post("/{chat_room_id}/members/{user_id}")
def add_member_to_chat_room(
    chat_room_id: int,
    user_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    # Check if the current user is a member
    current_member = db.query(models.ChatMember).filter(
        models.ChatMember.chat_room_id == chat_room_id,
        models.ChatMember.user_id == current_user.id
    ).first()
    
    if not current_member:
        raise HTTPException(status_code=403, detail="Not a member of this chat room")
    
    # Check if the chat room exists and is not a DM
    chat_room = db.query(models.ChatRoom).filter(models.ChatRoom.id == chat_room_id).first()
    if not chat_room:
        raise HTTPException(status_code=404, detail="Chat room not found")
    if chat_room.is_direct_message:
        raise HTTPException(status_code=400, detail="Cannot add members to direct message chat")
    
    # Check if the user is already a member
    existing_member = db.query(models.ChatMember).filter(
        models.ChatMember.chat_room_id == chat_room_id,
        models.ChatMember.user_id == user_id
    ).first()
    
    if existing_member:
        raise HTTPException(status_code=400, detail="User is already a member")
    
    # Add new member
    new_member = models.ChatMember(
        user_id=user_id,
        chat_room_id=chat_room_id
    )
    db.add(new_member)
    db.commit()
    
    return {"status": "success"}