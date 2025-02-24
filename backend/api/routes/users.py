from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Dict
from boto3.dynamodb.conditions import Key

from ..auth import get_current_user
from ..database import get_table

router = APIRouter()

@router.get("/users")
async def get_users(current_user = Depends(get_current_user)):
    """
    Fetch all users except the current user
    """
    if not current_user.user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    users_table = get_table('users')
    try:
        response = users_table.scan()
        # Filter out current user
        users = [
            user for user in response.get('Items', [])
            if user['id'] != current_user.user_id
        ]
        return users
    except Exception as e:
        print(f"Error fetching users: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch users")

@router.get("/users/{user_id}")
async def get_user(user_id: str):
    """
    Fetch a single user by ID
    """
    users_table = get_table('users')
    try:
        response = users_table.get_item(Key={'id': user_id})
        if 'Item' not in response:
            raise HTTPException(status_code=404, detail="User not found")
        return response['Item']
    except Exception as e:
        print(f"Error fetching user: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch user")

@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: str):
    """
    Delete a user by ID
    """
    users = get_table('users')
    
    try:
        # First check if the user exists
        response = users.get_item(
            Key={'id': user_id}
        )
        
        if 'Item' not in response or not response['Item']:
            raise HTTPException(status_code=404, detail="User not found")
        
        # If user exists, delete them
        users.delete_item(
            Key={'id': user_id},
            # Add ReturnValues to confirm deletion
            ReturnValues='ALL_OLD'
        )
        return None
    
    except users.meta.client.exceptions.InternalServerError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database service is temporarily unavailable. Please try again later."
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete user: {str(e)}"
        )