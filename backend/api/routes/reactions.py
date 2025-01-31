from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from .. import models, schemas
from ..auth import get_current_user

router = APIRouter(
    prefix="/reactions",
    tags=["reactions"]
)

@router.post("/", response_model=schemas.ReactionResponse)
def create_reaction(
    reaction: schemas.ReactionCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    # Check if message exists
    message = db.query(models.Message).filter(models.Message.id == reaction.message_id).first()
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    
    # Check if user is in the chat room
    if current_user not in message.chat_room.users:
        raise HTTPException(status_code=403, detail="Not a member of this chat room")
    
    # Check if user already reacted with the same reaction
    existing_reaction = db.query(models.Reaction).filter(
        models.Reaction.message_id == reaction.message_id,
        models.Reaction.user_id == current_user.id,
        models.Reaction.reaction_type == reaction.reaction_type
    ).first()
    
    if existing_reaction:
        raise HTTPException(status_code=400, detail="Reaction already exists")
    
    # Create new reaction
    db_reaction = models.Reaction(
        reaction_type=reaction.reaction_type,
        user_id=current_user.id,
        message_id=reaction.message_id
    )
    db.add(db_reaction)
    db.commit()
    db.refresh(db_reaction)
    return db_reaction

@router.delete("/{reaction_id}")
def delete_reaction(
    reaction_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    reaction = db.query(models.Reaction).filter(models.Reaction.id == reaction_id).first()
    if not reaction:
        raise HTTPException(status_code=404, detail="Reaction not found")
    if reaction.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this reaction")
    
    db.delete(reaction)
    db.commit()
    return {"status": "success"}

@router.get("/message/{message_id}", response_model=List[schemas.ReactionResponse])
def get_message_reactions(
    message_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    message = db.query(models.Message).filter(models.Message.id == message_id).first()
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    if current_user not in message.chat_room.users:
        raise HTTPException(status_code=403, detail="Not a member of this chat room")
    
    return message.reactions