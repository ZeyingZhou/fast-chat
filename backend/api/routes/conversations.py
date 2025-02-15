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
    users_table = get_table('users')
    current_time = datetime.utcnow().isoformat()

    try:
        if data.isGroup:
            conversation_id = str(uuid.uuid4())
            all_user_ids = [str(member['value']) for member in data.members]
            all_user_ids.append(str(current_user.user_id))
            
            # Get all users' details for denormalization
            users_data = []
            for user_id in all_user_ids:
                user_response = users_table.get_item(Key={'id': user_id})
                if 'Item' in user_response:
                    user = user_response['Item']
                    users_data.append({
                        'id': user['id'],
                        'email': user.get('email'),
                        'name': user.get('name'),
                        'image': user.get('image')
                    })
            
            conversation_data = {
                'id': conversation_id,
                'createdAt': current_time,
                'lastMessageAt': current_time,
                'name': data.name,
                'isGroup': 'true',
                'messagesIds': [],
                'messages': [],
                'userIds': all_user_ids,
                'users': users_data,
            }

            for participant in all_user_ids:
                conversation_copy = {
                    **conversation_data,
                    'userId': participant
                }
                conversations_table.put_item(Item=conversation_copy)

            return conversation_data

        else:

            # Try to find existing direct conversation
            print("data.userId", data.userId)
            other_user_id = data.userId
            user_ids = sorted([str(current_user.user_id), other_user_id])
            
            # Check for existing conversation
            response = conversations_table.query(
                IndexName='user-direct-conversations-index',
                KeyConditionExpression='userId = :uid AND isGroup = :is_group',
                FilterExpression='userIds = :all_uids',
                ExpressionAttributeValues={
                    ':uid': str(current_user.user_id),
                    ':is_group': 'false',  # Changed from False to 'false' string
                    ':all_uids': user_ids
                }
            )

            if response['Items']:
                return response['Items'][0]

            # Get both users' data for denormalization
            conversation_id = str(uuid.uuid4())

            users_data = []
            for user_id in user_ids:
                user_response = users_table.get_item(Key={'id': user_id})
                if 'Item' in user_response:
                    user = user_response['Item']
                    users_data.append({
                        'id': user['id'],
                        'email': user.get('email'),
                        'name': user.get('name'),
                        'image': user.get('image')
                    })
            

            conversation_data = {
                'id': conversation_id,
                'createdAt': current_time,
                'lastMessageAt': current_time,
                'name': None,
                'isGroup': 'false',
                'messagesIds': [],
                'messages': [],
                'userIds': user_ids,
                'users': users_data
            }

            # Create entries for both participants
            for participant_id in user_ids:
                conversation_copy = {
                    **conversation_data,
                    'userId': participant_id
                }
                conversations_table.put_item(Item=conversation_copy)

            return conversation_data

    except ClientError as e:
        print(e.response['Error']['Message'])
        raise HTTPException(status_code=500, detail="Failed to process conversation")



@router.get("/conversations")
async def get_conversations(
    current_user = Depends(get_current_user),
):
    if not current_user.user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    conversations_table = get_table('conversations')
    
    try:
        # Query using GSI instead of scan
        response = conversations_table.query(
            IndexName='user-conversations-index',
            KeyConditionExpression='userId = :uid',
            ExpressionAttributeValues={
                ':uid': str(current_user.user_id)
            },
            ScanIndexForward=False  # Get newest first
        )
        
        return response['Items']
        
    except ClientError as e:
        print(e.response['Error']['Message'])
        raise HTTPException(status_code=500, detail="Failed to fetch conversations")
        
  