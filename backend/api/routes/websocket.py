from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from api.websocket_manager import manager  # Import the shared manager instance
from typing import Dict, Any

router = APIRouter()

@router.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    await manager.connect(websocket, user_id)
    try:
        while True:
            data = await websocket.receive_json()
            
            # Handle different types of WebSocket messages
            message_type = data.get('type')
            if message_type == 'typing':
                # Notify others in the conversation that user is typing
                conversation_id = data.get('conversationId')
                await manager.broadcast_to_conversation(
                    message={'type': 'typing', 'userId': user_id},
                    conversation_id=conversation_id,
                    exclude_user=user_id
                )
            elif message_type == 'seen':
                # Update message seen status
                conversation_id = data.get('conversationId')
                await manager.broadcast_to_conversation(
                    message={'type': 'seen', 'userId': user_id},
                    conversation_id=conversation_id,
                    exclude_user=user_id
                )
                
    except WebSocketDisconnect:
        manager.disconnect(user_id) 