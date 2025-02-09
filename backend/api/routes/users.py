from fastapi import APIRouter, HTTPException, status
from typing import List, Dict
from boto3.dynamodb.conditions import Key
from ..database import get_table

router = APIRouter()

@router.get("/users", response_model=List[Dict])
async def get_users():
    """
    Fetch all users
    """
    users = get_table('users')
    response = users.scan()
    items = response.get('Items', [])
    # Return items directly since they're already in the correct format
    return items

@router.get("/users/{user_id}", response_model=Dict)
async def get_user(user_id: str):
    """
    Fetch a single user by ID
    """
    users = get_table('users')
    response = users.get_item(
        Key={'id': user_id}
    )
    print(response['Item'])
    if not response['Item']:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Return first item directly since it's already in the correct format
    return response['Item']

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