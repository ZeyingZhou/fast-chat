from fastapi import APIRouter, Depends, HTTPException
from typing import Optional

from backend.api.database import get_table
from ..dependencies import get_current_user
from ..models import User
import boto3
from botocore.exceptions import ClientError
import uuid
from datetime import datetime

router = APIRouter()


@router.post("/conversations")
async def create_or_get_conversation(
    data: dict,
    current_user: User = Depends(get_current_user),
):
    conversations = get_table('conversations')
    user_ids = sorted([str(current_user.id), str(data['userId'])])
    current_time = datetime.utcnow().isoformat()
    
    try:
        # Try to get existing conversation
        response = conversations.query(
            IndexName='user-conversations-index',
            KeyConditionExpression='userId = :u1 AND lastMessageAt = :u2',
            ExpressionAttributeValues={
                ':u1': user_ids[0],
                ':u2': user_ids[1]
            }
        )
        
        # If conversation exists, return it
        if response['Items']:
            return {"id": response['Items'][0]['id']}
            
        # If not, create new conversation
        conversation_id = str(uuid.uuid4())
        
        conversations.put_item(
            Item={
                'id': conversation_id,
                'userId': user_ids[0],
                'lastMessageAt': user_ids[1],
                'createdAt': current_time,
                'userIds': user_ids,  # Store all participating user IDs
                'isGroup': False,     # Default to direct message
                'name': None,         # Optional name for group chats
                'messagesIds': [],    # Initialize empty messages array
            }
        )
        
        return {"id": conversation_id}
        
    except ClientError as e:
        print(e.response['Error']['Message'])
        raise HTTPException(status_code=500, detail="Failed to process conversation")
