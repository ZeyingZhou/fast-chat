from pydantic import BaseModel
from pydantic import ConfigDict
from enum import Enum
from typing import List, Optional

class ClerkWebhookEvent(str, Enum):
    USER_CREATED = "user.created"
    USER_DELETED = "user.deleted"
    USER_UPDATED = "user.updated"
    # USER_EMAIL_CHANGED = "user.email_changed"
    # USER_PHONE_CHANGED = "user.phone_changed"
    
class EmailAddress(BaseModel):
    email_address: str

class ClerkWebhook(BaseModel):
    object: str = "event"
    type: ClerkWebhookEvent
    data: dict
    
    