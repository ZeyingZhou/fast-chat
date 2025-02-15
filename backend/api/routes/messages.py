from datetime import datetime
import uuid
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from ..models.message import MessageCreate, MessageUpdate, MessageResponse
from ..database import get_table
from ..auth import get_current_user
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key

router = APIRouter()

@router.post("/messages")
async def create_message(
    data: MessageCreate,
    current_user = Depends(get_current_user)
):
    if not current_user.user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")

    messages_table = get_table('messages')
    conversations_table = get_table('conversations')
    users_table = get_table('users')
    current_time = datetime.utcnow().isoformat()

    try:
        # Get sender's data for denormalization
        sender_response = users_table.get_item(Key={'id': current_user.user_id})
        if 'Item' not in sender_response:
            raise HTTPException(status_code=404, detail="Sender not found")
        
        sender_data = {
            'id': sender_response['Item']['id'],
            'name': sender_response['Item'].get('name'),
            'image': sender_response['Item'].get('image')
        }

        # Create message with denormalized sender data
        message_id = str(uuid.uuid4())
        message_data = {
            'id': message_id,
            'conversationId': data.conversationId,
            'content': data.content,
            'senderId': current_user.user_id,
            'sender': sender_data,
            'seenIds': [current_user.user_id],
            'seen': [sender_data],
            'createdAt': current_time
        }

        # Update conversation's last message
        conversation_update = {
            'lastMessage': message_data,
            'lastMessageAt': current_time,
            'updatedAt': current_time
        }

        # Use transaction to update both tables
        conversations_table.update_item(
            Key={'id': data.conversationId},
            UpdateExpression='SET lastMessage = :msg, lastMessageAt = :time, updatedAt = :time',
            ExpressionAttributeValues={
                ':msg': message_data,
                ':time': current_time
            }
        )

        messages_table.put_item(Item=message_data)
        return message_data

    except ClientError as e:
        raise HTTPException(status_code=500, detail=str(e))

