from fastapi import APIRouter, Depends, HTTPException, Header, Request
from typing import Optional

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
    print("data", data)
    print("current_user", current_user)
    
    if not current_user.user_id:
        raise HTTPException(status_code=400, detail="Unauthorized")

    conversations = get_table('conversations')
    users_table = get_table('users')
    isGroup = data.isGroup
    members = data.members
    name = data.name
    userId = data.userId

    # Validate group chat requirements
    if isGroup and (not members or len(members) < 2 or not name):
        raise HTTPException(status_code=400, detail="Invalid data")

    current_time = datetime.utcnow().isoformat()

    try:
        if isGroup:
            conversation_id = str(uuid.uuid4())
            all_user_ids = [str(member['value']) for member in members]
            all_user_ids.append(str(current_user.user_id))
            
            # Get all users' details for denormalization
            users_data = []
            for user_id in all_user_ids:
                user_response = users_table.get_item(Key={'id': user_id})
                if 'Item' in user_response:
                    user = user_response['Item']
                    users_data.append({
                        'id': user['id'],
                        'username': user.get('username'),
                        'email': user.get('email'),
                        'image': user.get('image')
                    })
            
            conversation_data = {
                'id': conversation_id,
                'userId': str(current_user.user_id),
                'lastMessageAt': current_time,
                'createdAt': current_time,
                'userIds': all_user_ids,
                'users': users_data,  # Denormalized user data
                'isGroup': True,
                'name': name,
                'messageIds': [],
                'lastMessage': None
            }
            
            conversations.put_item(Item=conversation_data)



            return conversation_data

        else:
            # Try to find existing direct conversation
            response = conversations.scan(
                FilterExpression='userIds = :uids AND isGroup = :is_group',
                ExpressionAttributeValues={
                    ':uids': sorted([str(current_user.user_id), str(userId)]),
                    ':is_group': False
                }
            )

            # If conversation exists, return it
            if response['Items']:
                return response['Items'][0]

            # Create new direct conversation
            conversation_id = str(uuid.uuid4())
            user_ids = sorted([str(current_user.user_id), str(userId)])
            
            # Get both users' details for denormalization
            users_data = []
            for user_id in user_ids:
                user_response = users_table.get_item(Key={'id': user_id})
                if 'Item' in user_response:
                    user = user_response['Item']
                    users_data.append({
                        'id': user['id'],
                        'name': user.get('name'),
                        'email': user.get('email'),
                        'imageUrl': user.get('imageUrl')
                    })
            
            conversation_data = {
                'id': conversation_id,
                'userId': user_ids[0],
                'lastMessageAt': current_time,
                'createdAt': current_time,
                'userIds': user_ids,
                'users': users_data,  # Denormalized user data
                'isGroup': False,
                'name': None,
                'messageIds': [],
                'lastMessage': None
            }
            
            conversations.put_item(Item=conversation_data)

 

            return conversation_data

    except ClientError as e:
        print(e.response['Error']['Message'])
        raise HTTPException(status_code=500, detail="Failed to process conversation")




@router.get("/conversations")
async def get_conversations(
    current_user = Depends(get_current_user),
):
    if not current_user.user_id:
        return []
    
    conversations = get_table('conversations')
    user_id = str(current_user.user_id)
    
    try:
        response = conversations.scan(
            FilterExpression='contains(userIds, :uid)',
            ExpressionAttributeValues={
                ':uid': user_id
            }
        )
        
        conversations_list = sorted(
            response['Items'],
            key=lambda x: x.get('lastMessageAt', ''),
            reverse=True
        )
        
        return conversations_list
        
    except ClientError as e:
        print(e.response['Error']['Message'])
        return []

