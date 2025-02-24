from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from api.websocket_manager import manager
from ..database import get_table
from datetime import datetime

router = APIRouter()

@router.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    await manager.connect(websocket, user_id)
    try:
        while True:
            data = await websocket.receive_json()
            
            if data.get('type') == 'typing':
                # Get conversation participants
                conv_users = get_table('conversation_users').query(
                    KeyConditionExpression='conversationId = :cid',
                    ExpressionAttributeValues={
                        ':cid': data['conversationId']
                    }
                )
                
                # Notify other participants
                for user in conv_users.get('Items', []):
                    if user['userId'] != user_id:
                        await manager.send_personal_message({
                            'type': 'typing',
                            'userId': user_id,
                            'conversationId': data['conversationId']
                        }, user['userId'])
                
    except WebSocketDisconnect:
        manager.disconnect(user_id) 