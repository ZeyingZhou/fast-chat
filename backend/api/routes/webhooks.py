from fastapi import APIRouter, Depends, HTTPException, Request, status
from svix.webhooks import Webhook, WebhookVerificationError
from api.database import get_table
from datetime import datetime, timezone
import os
from dotenv import load_dotenv
import logging

from api.models.webhook import ClerkWebhook, ClerkWebhookEvent

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
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Invalid webhook signature"
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
    current_time = datetime.now(timezone.utc).isoformat()

    if event.type == ClerkWebhookEvent.USER_CREATED:
        # Create new user with minimal required data
        user_data = {
            'id': data.get('id'),
            'email': data.get('email_addresses')[0].get('email_address'),
            'name': f"{data.get('first_name') or ''} {data.get('last_name') or ''}".strip(),
            'image': data.get('image_url'),
            'createdAt': current_time
        }
        users_table.put_item(Item=user_data)
        logging.info(f"User created: {data.get('id')}")
        
    elif event.type == ClerkWebhookEvent.USER_UPDATED:
        # Update only the fields that can change
        update_attrs = {}
        if data.get('email_addresses'):
            update_attrs['email'] = data['email_addresses'][0]['email_address']
        if data.get('first_name') is not None or data.get('last_name') is not None:
            update_attrs['name'] = f"{data.get('first_name') or ''} {data.get('last_name') or ''}".strip()
        if data.get('image_url') is not None:
            update_attrs['image'] = data['image_url']
        
        if update_attrs:
            update_expression = "SET " + ", ".join(f"#{k} = :{k}" for k in update_attrs.keys())
            expression_attribute_names = {f"#{k}": k for k in update_attrs.keys()}
            expression_attribute_values = {f":{k}": v for k, v in update_attrs.items()}
            
            users_table.update_item(
                Key={'id': data.get('id')},
                UpdateExpression=update_expression,
                ExpressionAttributeNames=expression_attribute_names,
                ExpressionAttributeValues=expression_attribute_values
            )
            logging.info(f"User updated: {data.get('id')}")
        
    elif event.type == ClerkWebhookEvent.USER_DELETED:
        # Delete user and their conversation associations
        users_table.delete_item(Key={'id': data.get('id')})
        
        # Clean up conversation_users entries
        conv_users_table = get_table('conversation_users')
        response = conv_users_table.query(
            IndexName='by-user',
            KeyConditionExpression='userId = :uid',
            ExpressionAttributeValues={
                ':uid': data.get('id')
            }
        )
        
        # Delete all conversation associations for this user
        for item in response.get('Items', []):
            conv_users_table.delete_item(
                Key={
                    'conversationId': item['conversationId'],
                    'userId': data.get('id')
                }
            )
            
        logging.info(f"User and their conversation associations deleted: {data.get('id')}")

    return {"status": "success", "message": "Webhook processed"} 