from fastapi import HTTPException, Depends, Header, Request, Query
from clerk_backend_api import Clerk
from clerk_backend_api.models import ClerkErrors, SDKError
import os
from dotenv import load_dotenv

from .database import get_table

load_dotenv(".env.local")
CLERK_SECRET_KEY = os.getenv('CLERK_SECRET_KEY')
clerk_client = Clerk(bearer_auth=CLERK_SECRET_KEY)

    
async def get_current_user(request: Request, session_id: str = Query(...)):
    # Get the session token from the Authorization header
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        raise HTTPException(status_code=401, detail='Authorization header missing')
 
    # Expected format: 'Bearer <session_token>'
    if not auth_header.startswith('Bearer '):
        raise HTTPException(status_code=401, detail='Invalid authorization header format')

    session_token = auth_header[7:]  # Remove 'Bearer ' prefix

    try:
        # Verify the session with Clerk
        # Note: We're using the synchronous `get` method here. Consider using the async version in production.
        res = clerk_client.sessions.get(session_id=session_id)            
        # Return the session object
        return res

    except ClerkErrors as e:
        # Handle Clerk-specific errors
        raise HTTPException(status_code=401, detail='Invalid or expired session token')
    except SDKError as e:
        # Handle general SDK errors
        raise HTTPException(status_code=500, detail='Internal server error')


