from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from .user import UserResponse

# Add a new model for file data
class FileData(BaseModel):
    file_url: str
    file_type: str
    file_name: str
    file_size: Optional[int] = None

class MessageBase(BaseModel):
    body: Optional[str] = None
    image: Optional[str] = None
    conversationId: str

class MessageCreate(BaseModel):
    conversationId: str
    content: str
    
    # Keep original fields for backward compatibility
    file_url: Optional[str] = None
    file_type: Optional[str] = None  
    file_name: Optional[str] = None
    file_size: Optional[int] = None
    
    # Add new field for multiple files
    files: Optional[List[FileData]] = None

class FileResponse(BaseModel):
    file_url: str
    file_type: str
    file_name: str
    file_size: Optional[int] = None

class MessageResponse(BaseModel):
    id: str
    body: Optional[str] = None
    image: Optional[str] = None
    senderId: str
    conversationId: str
    createdAt: str  # ISO format string
    sender: Optional[UserResponse] = None  # Fetched from users table
    
    # Single file fields (for backward compatibility)
    file_url: Optional[str] = None
    file_type: Optional[str] = None
    file_name: Optional[str] = None
    file_size: Optional[int] = None
    
    # Multiple files
    files: Optional[List[FileResponse]] = None