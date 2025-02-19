from fastapi import WebSocket
from typing import Dict, Any
from .database import get_table


class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, user_id: str):
        await websocket.accept()
        self.active_connections[user_id] = websocket

    def disconnect(self, user_id: str):
        if user_id in self.active_connections:
            del self.active_connections[user_id]

    async def broadcast_to_conversation(
        self, 
        message: Dict[str, Any], 
        conversation_id: str,
        exclude_user: str = None
    ):
        # Get conversation participants from DynamoDB
        conversations_table = get_table('conversations')
        conversation = conversations_table.get_item(Key={'id': conversation_id})
        
        if 'Item' in conversation:
            user_ids = conversation['Item'].get('userIds', [])
            for user_id in user_ids:
                if user_id != exclude_user and user_id in self.active_connections:
                    await self.active_connections[user_id].send_json(message)

    async def send_personal_message(self, message: dict, user_id: str):
        if user_id in self.active_connections:
            await self.active_connections[user_id].send_json(message) 

manager = ConnectionManager()