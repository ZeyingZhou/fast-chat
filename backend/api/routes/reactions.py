from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..reactions import models as reactions_models
from ..reactions import schemas as reactions_schemas
from ..users import models as users_models
from ..auth import get_current_user

router = APIRouter(
    prefix="/reactions",
    tags=["reactions"]
)

@router.post("/", response_model=reactions_schemas.ReactionResponse)
def create_reaction(
    reaction: reactions_schemas.ReactionCreate,
    db: Session = Depends(get_db),
    current_user: users_models.User = Depends(get_current_user)
):
    # Check if message exists
    message = db.query(reactions_models.Message).filter(reactions_models.Message.id == reaction.message_id).first()
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    
    # Check if user is in the chat room
    if current_user not in message.chat_room.users:
        raise HTTPException(status_code=403, detail="Not a member of this chat room")
    
    # Check if user already reacted with the same reaction
    existing_reaction = db.query(reactions_models.Reaction).filter(
        reactions_models.Reaction.message_id == reaction.message_id,
        reactions_models.Reaction.user_id == current_user.id,
        reactions_models.Reaction.reaction_type == reaction.reaction_type
    ).first()
    
    if existing_reaction:
        raise HTTPException(status_code=400, detail="Reaction already exists")
    
    # Create new reaction
    db_reaction = reactions_models.Reaction(
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
    current_user: users_models.User = Depends(get_current_user)
):
    reaction = db.query(reactions_models.Reaction).filter(reactions_models.Reaction.id == reaction_id).first()
    if not reaction:
        raise HTTPException(status_code=404, detail="Reaction not found")
    if reaction.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this reaction")
    
    db.delete(reaction)
    db.commit()
    return {"status": "success"}

@router.get("/message/{message_id}", response_model=List[reactions_schemas.ReactionResponse])
def get_message_reactions(
    message_id: int,
    db: Session = Depends(get_db),
    current_user: users_models.User = Depends(get_current_user)
):
    message = db.query(reactions_models.Message).filter(reactions_models.Message.id == message_id).first()
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    if current_user not in message.chat_room.users:
        raise HTTPException(status_code=403, detail="Not a member of this chat room")
    
    return message.reactions