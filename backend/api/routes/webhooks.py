from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from svix.webhooks import Webhook, WebhookVerificationError
from api.database import get_table
from datetime import datetime, timezone
import os
from dotenv import load_dotenv
import logging

from api.models.webhook import ClerkWebhook, ClerkWebhookEvent
from api.models.user import UserCreate, UserUpdate

# Load environment variables
load_dotenv('.env.local')

router = APIRouter()

WEBHOOK_SECRET = os.getenv('SIGNING_SECRET')

async def verify_clerk_webhook(request: Request):
    headers = request.headers
    payload = await request.body()

    try:
        wh = Webhook(WEBHOOK_SECRET)
        msg = wh.verify(payload, headers)
        return ClerkWebhook.model_validate(msg)
    except WebhookVerificationError as e:
        print("Webhook verification failed:", e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid webhook signature"
        )
    except Exception as e:
        raise e
    
@router.post("/webhooks", status_code=status.HTTP_200_OK)
async def clerk_webhook(event: ClerkWebhook = Depends(verify_clerk_webhook)):
    try:
        if event.type in [
            ClerkWebhookEvent.USER_CREATED,
            ClerkWebhookEvent.USER_UPDATED,
            ClerkWebhookEvent.USER_DELETED
        ]:
            await handle_user_event(event)
            return {"status": "success", "message": f"Processed {event.type} event"}
        
        # Log unhandled event types for monitoring
        logging.info(f"Unhandled webhook event type: {event.type}")
        return {"status": "success", "message": f"Ignored {event.type} event"}
        
    except Exception as e:
        logging.error(f"Error processing webhook: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error processing webhook"
        )

async def handle_user_event(event: ClerkWebhook):
    users_table = get_table('users')
    data = event.data

    if event.type == ClerkWebhookEvent.USER_CREATED:
        user = UserCreate(
            id=data.get('id'),
            email=data.get('email_addresses')[0].get('email_address'),
            name=f"{data.get('first_name') or ''} {data.get('last_name') or ''}".strip(),
            image=data.get('image_url'),
            conversationIds=[],
            seenMessageIds=[],
            createdAt=datetime.now(timezone.utc).isoformat(),
            updatedAt=datetime.now(timezone.utc).isoformat()
        )
        users_table.put_item(Item=user.model_dump())
        logging.info(f"User created: {data.get('id')}")
        
    elif event.type == ClerkWebhookEvent.USER_UPDATED:
        user_update = UserUpdate(
            email=data.get('email_addresses')[0].get('email_address'),
            name=f"{data.get('first_name') or ''} {data.get('last_name') or ''}".strip(),
            image=data.get('image_url'),
            updatedAt=datetime.now(timezone.utc).isoformat()
        )
        
        update_data = user_update.model_dump(exclude_unset=True)
        update_expression = "SET " + ", ".join(f"#{k} = :{k}" for k in update_data.keys())
        expression_attribute_names = {f"#{k}": k for k in update_data.keys()}
        expression_attribute_values = {f":{k}": v for k, v in update_data.items()}
        
        users_table.update_item(
            Key={'id': data.get('id')},
            UpdateExpression=update_expression,
            ExpressionAttributeNames=expression_attribute_names,
            ExpressionAttributeValues=expression_attribute_values
        )
        logging.info(f"User updated: {data.get('id')}")
        
    elif event.type == ClerkWebhookEvent.USER_DELETED:
        users_table.delete_item(Key={'id': data.get('id')})
        logging.info(f"User deleted: {data.get('id')}")

    return {"status": "success", "message": "Webhook processed"} 