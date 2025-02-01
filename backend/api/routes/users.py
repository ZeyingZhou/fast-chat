import shutil
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session
from typing import List

from ..auth import get_current_user
from ..database import get_db
from ..users import models as users_models
from ..users import schemas as users_schemas
from ..utils import get_password_hash
import os
from uuid import uuid4

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

UPLOAD_DIR = "uploads/profile_images"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/", response_model=users_schemas.UserResponse)
def create_user(user: users_schemas.UserCreate, db: Session = Depends(get_db)):
    # Check if user exists
    db_user = db.query(users_models.User).filter(users_models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create new user
    hashed_password = get_password_hash(user.password)
    db_user = users_models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/", response_model=List[users_schemas.UserResponse])
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = db.query(users_models.User).offset(skip).limit(limit).all()
    return users

@router.get("/{user_id}", response_model=users_schemas.UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(users_models.User).filter(users_models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.post("/me/image", response_model=users_schemas.UserResponse)
async def update_user_image(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: users_models.User = Depends(get_current_user)
):
    # Validate file type
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    # Generate unique filename
    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid4()}{file_extension}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)
    
    # Save the file
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Could not upload image")
    
    # Delete old image if it exists
    if current_user.image:
        old_image_path = os.path.join(UPLOAD_DIR, os.path.basename(current_user.image))
        if os.path.exists(old_image_path):
            os.remove(old_image_path)
    
    # Update user's image path in database
    current_user.image = f"/uploads/profile_images/{unique_filename}"
    db.commit()
    db.refresh(current_user)
    
    return current_user

@router.patch("/me", response_model=users_schemas.UserResponse)
def update_user_profile(
    user_update: users_schemas.UserUpdate,
    db: Session = Depends(get_db),
    current_user: users_models.User = Depends(get_current_user)
):
    for field, value in user_update.dict(exclude_unset=True).items():
        setattr(current_user, field, value)
    
    db.commit()
    db.refresh(current_user)
    return current_user

@router.get("/me", response_model=users_schemas.UserResponse)
def get_current_user_profile(current_user: users_models.User = Depends(get_current_user)):
    return current_user

@router.get("/{user_id}", response_model=users_schemas.UserResponse)
def get_user_profile(
    user_id: int,
    db: Session = Depends(get_db)
):
    user = db.query(users_models.User).filter(users_models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user