from fastapi import HTTPException, Depends, Header
from jose import jwt
import httpx
import os
from dotenv import load_dotenv

load_dotenv()

async def verify_clerk_token(authorization: str = Header(...)) -> dict:
    try:
        token = authorization.replace('Bearer ', '')
        
        # Verify token with Clerk API
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"https://api.clerk.dev/v1/session",
                headers={"Authorization": f"Bearer {token}"}
            )
            
            if response.status_code != 200:
                raise HTTPException(status_code=401, detail="Invalid session")
                
            return response.json()
            
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))