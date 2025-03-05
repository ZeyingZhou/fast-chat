from fastapi import APIRouter, Depends, HTTPException, Header, Request
from typing import Optional, List

from api.models.conversation import ConversationCreate

from ..database import get_table
from ..auth import get_current_user
import boto3
from botocore.exceptions import ClientError
import uuid
from datetime import datetime
import httpx

router = APIRouter()


@router.post("/conversations")
async def create_or_get_conversation(
    data: ConversationCreate,
    current_user = Depends(get_current_user),
):
    if not current_user.user_id:
        raise HTTPException(status_code=400, detail="Unauthorized")

    conversations_table = get_table('conversations')
    conversation_users_table = get_table('conversation_users')
    current_time = datetime.utcnow().isoformat()

    try:
        if data.isGroup:
            # Create group conversation
            conversation_id = str(uuid.uuid4())
            all_user_ids = [str(member['value']) for member in data.members]
            all_user_ids.append(str(current_user.user_id))
            
            # Create conversation - use 'true' string instead of True boolean
            conversation_data = {
                'id': conversation_id,
                'createdAt': current_time,
                'lastMessageAt': current_time,
                'name': data.name,
                'isGroup': 'true'  # Changed to string
            }
            conversations_table.put_item(Item=conversation_data)
            
            # Create conversation_users entries
            for user_id in all_user_ids:
                conversation_users_table.put_item(Item={
                    'conversationId': conversation_id,
                    'userId': user_id,
                    'joinedAt': current_time
                })

            # Get full conversation data for response
            return await get_conversation_with_details(conversation_id)

        else:
            # Try to find existing direct conversation
            other_user_id = data.userId
            
            # First, get all conversations for the current user
            current_user_convs = conversation_users_table.query(
                IndexName='by-user',
                KeyConditionExpression='userId = :uid',
                ExpressionAttributeValues={
                    ':uid': str(current_user.user_id)
                }
            ).get('Items', [])

            # Then, get all conversations for the other user
            other_user_convs = conversation_users_table.query(
                IndexName='by-user',
                KeyConditionExpression='userId = :uid',
                ExpressionAttributeValues={
                    ':uid': str(other_user_id)
                }
            ).get('Items', [])

            # Find common conversations
            current_user_conv_ids = set(item['conversationId'] for item in current_user_convs)
            other_user_conv_ids = set(item['conversationId'] for item in other_user_convs)
            common_conv_ids = current_user_conv_ids.intersection(other_user_conv_ids)

            # Check if any common conversation is a direct message (not a group)
            for conv_id in common_conv_ids:
                conv = conversations_table.get_item(Key={'id': conv_id})['Item']
                if conv['isGroup'] == 'false':  # Remember we're using string 'false'
                    return await get_conversation_with_details(conv_id)

            # If no existing direct conversation found, create new one
            conversation_id = str(uuid.uuid4())
            conversation_data = {
                'id': conversation_id,
                'createdAt': current_time,
                'lastMessageAt': current_time,
                'name': None,
                'isGroup': 'false'  # Changed to string
            }
            
            conversations_table.put_item(Item=conversation_data)
            
            # Add both users to conversation
            for user_id in [str(current_user.user_id), other_user_id]:
                conversation_users_table.put_item(Item={
                    'conversationId': conversation_id,
                    'userId': user_id,
                    'joinedAt': current_time
                })

            return await get_conversation_with_details(conversation_id)

    except Exception as e:
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to process conversation")


@router.get("/conversations")
async def get_conversations(
    current_user = Depends(get_current_user),
):
    if not current_user.user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    conversation_users_table = get_table('conversation_users')
    
    try:
        # Get all conversations for user
        response = conversation_users_table.query(
            IndexName='by-user',
            KeyConditionExpression='userId = :uid',
            ExpressionAttributeValues={
                ':uid': str(current_user.user_id)
            }
        )

        # Get full details for each conversation
        conversations = []
        for item in response.get('Items', []):
            conv_details = await get_conversation_with_details(item['conversationId'])
            conversations.append(conv_details)
        
        # Sort by lastMessageAt
        conversations.sort(key=lambda x: x['lastMessageAt'], reverse=True)
        return conversations
        
    except Exception as e:
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch conversations")

async def get_conversation_with_details(conversation_id: str):
    """Helper function to get conversation with all related data"""
    conversations_table = get_table('conversations')
    conversation_users_table = get_table('conversation_users')
    users_table = get_table('users')
    
    # Get base conversation
    conversation = conversations_table.get_item(Key={'id': conversation_id})['Item']
    
    # Get participants
    participants = conversation_users_table.query(
        KeyConditionExpression='conversationId = :cid',
        ExpressionAttributeValues={
            ':cid': conversation_id
        }
    )
    
    # Get user details
    users = []
    for participant in participants.get('Items', []):
        user_data = users_table.get_item(Key={'id': participant['userId']})
        if 'Item' in user_data:
            users.append(user_data['Item'])
    
    # Combine data
    conversation['users'] = users
    return conversation

@router.get("/conversations/{conversation_id}")
async def get_conversation(
    conversation_id: str,
    current_user = Depends(get_current_user),
):
    if not current_user.user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")

    try:

        conv_details = await get_conversation_with_details(conversation_id)
        return conv_details

    except ClientError as e:
        print(e.response['Error']['Message'])
        raise HTTPException(status_code=500, detail="Failed to fetch conversation")
