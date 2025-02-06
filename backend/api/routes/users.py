from fastapi import APIRouter, HTTPException
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
    response = users.query(
        KeyConditionExpression=Key('id').eq(user_id)
    )
    
    items = response.get('Items', [])
    if not items:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Return first item directly since it's already in the correct format
    return items[0]
