from fastapi import APIRouter, Request, Response, status
from svix.webhooks import Webhook, WebhookVerificationError
from api.database import get_table
from datetime import datetime
import os
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv('.env.local')

router = APIRouter()

WEBHOOK_SECRET = os.getenv('SIGNING_SECRET')

@router.post("/webhooks", status_code=status.HTTP_200_OK)
async def clerk_webhook(request: Request):
    headers = dict(request.headers)
    payload = await request.body()
    
    try:
        wh = Webhook(WEBHOOK_SECRET)
        event = wh.verify(payload, headers)
        
        # Debug logging
        print(f"Received event type: {event.get('type')}")
        print(f"Event data: {event.get('data')}")
        
        # Get the event type and data
        event_type = event.get("type")
        data = event.get("data")
        
        # Handle user creation
        if event_type == "user.created":
            # Get users table
            users_table = get_table('users')
            
            # Create user record
            user = {
                'id': data['id'],  # Clerk user ID
                'email': data['email_addresses'][0]['email_address'],
                'username': data.get('username', ''),  # Add username from Clerk
                'name': f"{data.get('first_name', '')} {data.get('last_name', '')}".strip(),
                'image': data.get('image_url'),
                'conversationIds': [],
                'seenMessageIds': [],
                'createdAt': datetime.utcnow().isoformat() + 'Z',
                'updatedAt': datetime.utcnow().isoformat() + 'Z'
            }
            
            print(f"Creating user: {user}")  # Debug log
            
            # Save to DynamoDB
            users_table.put_item(Item=user)
            print("User created successfully")  # Debug log
            
            return {"status": "success", "message": "User created successfully"}
            
        # Handle user updates
        elif event_type == "user.updated":
            users_table = get_table('users')
            
            # Prepare updated user data
            updated_data = {
                'email': data['email_addresses'][0]['email_address'],
                'username': data.get('username', ''),
                'name': f"{data.get('first_name', '')} {data.get('last_name', '')}".strip(),
                'image': data.get('image_url'),
                'updatedAt': datetime.utcnow().isoformat() + 'Z'
            }
            
            print(f"Updating user {data['id']}: {updated_data}")  # Debug log
            
            # Update user in DynamoDB
            update_expression = "SET " + ", ".join(f"#{k} = :{k}" for k in updated_data.keys())
            expression_attribute_names = {f"#{k}": k for k in updated_data.keys()}
            expression_attribute_values = {f":{k}": v for k, v in updated_data.items()}
            
            users_table.update_item(
                Key={'id': data['id']},
                UpdateExpression=update_expression,
                ExpressionAttributeNames=expression_attribute_names,
                ExpressionAttributeValues=expression_attribute_values
            )
            print("User updated successfully")  # Debug log
            
            return {"status": "success", "message": "User updated successfully"}
            
        # Handle user deletion
        elif event_type == "user.deleted":
            users_table = get_table('users')
            
            print(f"Deleting user: {data['id']}")  # Debug log
            
            # Delete user from DynamoDB
            users_table.delete_item(Key={'id': data['id']})
            print("User deleted successfully")  # Debug log
            
            return {"status": "success", "message": "User deleted successfully"}
            
    except WebhookVerificationError as e:
        print(f"Webhook verification error: {str(e)}")  # Debug log
        return Response(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"error": "Invalid webhook signature"}
        )
    except Exception as e:
        print(f"Error processing webhook: {str(e)}")  # Debug log
        raise
    
    return {"status": "success", "message": "Webhook processed"} 