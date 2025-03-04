from datetime import datetime
import uuid
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from typing import List
from ..models.message import MessageCreate, FileData
from ..database import get_table
from ..auth import get_current_user
from boto3.dynamodb.conditions import Key
import os
from ..websocket_manager import manager


router = APIRouter()

@router.get("/messages/{conversation_id}")
async def get_messages(
    conversation_id: str,
    current_user = Depends(get_current_user)
):
    if not current_user.user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")

    messages_table = get_table('messages')
    try:
        # Query messages using the conversation GSI
        response = messages_table.query(
            IndexName='by-conversation',
            KeyConditionExpression='conversationId = :cid',
            ExpressionAttributeValues={
                ':cid': conversation_id
            }
        )
  
        if not response['Items']:
            return []

        # Get sender details for each message
        messages = []
        users_table = get_table('users')
        
        for message in response['Items']:
            # Get sender info
            sender_response = users_table.get_item(Key={'id': message['senderId']})
            sender = sender_response.get('Item', {})
            
            # Format message to match frontend expectations
            formatted_message = {
                'id': message['id'],
                'conversationId': message['conversationId'],
                'senderId': message['senderId'],
                'body': message.get('body'),
                'image': message.get('image'),
                'createdAt': message['createdAt'],
                'sender': {
                    'id': sender.get('id'),
                    'name': sender.get('name'),
                    'email': sender.get('email'),
                    'image': sender.get('image')
                }
            }
            
            # Add file data if present
            if 'file_url' in message:
                formatted_message['file_url'] = message['file_url']
                formatted_message['file_type'] = message.get('file_type')
                formatted_message['file_name'] = message.get('file_name')
                formatted_message['file_size'] = message.get('file_size')
            
            # Add multiple files if present
            if 'files' in message:
                formatted_message['files'] = message['files']
            
            messages.append(formatted_message)
            
        return messages

    except Exception as e:
        print(f"Error fetching messages: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch messages")

@router.post("/messages")
async def create_message(
    data: MessageCreate,
    current_user = Depends(get_current_user)
):
    print(data)
    if not current_user.user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")

    messages_table = get_table('messages')
    conversations_table = get_table('conversations')
    current_time = datetime.now().isoformat()

    try:
        message_id = str(uuid.uuid4())
        message_data = {
            'id': message_id,
            'conversationId': data.conversationId,
            'body': data.content,
            'senderId': current_user.user_id,
            'createdAt': current_time
        }
        
        # Handle backward compatibility for single file
        if data.file_url:
            message_data['file_url'] = data.file_url
            message_data['file_type'] = data.file_type
            message_data['file_name'] = data.file_name
            message_data['file_size'] = data.file_size
        
        # Handle multiple files
        if data.files and len(data.files) > 0:
            # Convert Pydantic models to dictionaries for DynamoDB
            message_data['files'] = [file.dict() for file in data.files]
        
        # Create message
        messages_table.put_item(Item=message_data)

        # Update conversation's lastMessageAt
        conversations_table.update_item(
            Key={'id': data.conversationId},
            UpdateExpression='SET lastMessageAt = :time',
            ExpressionAttributeValues={
                ':time': current_time
            }
        )

        # Get conversation participants to notify
        conv_users = get_table('conversation_users').query(
            KeyConditionExpression='conversationId = :cid',
            ExpressionAttributeValues={
                ':cid': data.conversationId
            }
        )

        # Notify other participants
        for user in conv_users.get('Items', []):
            if user['userId'] != current_user.user_id:
                await manager.send_personal_message({
                    'type': 'NEW_MESSAGE',
                    'message': message_data
                }, user['userId'])

        return message_data

    except Exception as e:
        print(f"Error creating message: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to create message")

