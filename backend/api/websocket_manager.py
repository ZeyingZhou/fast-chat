from fastapi import WebSocket
from typing import Dict, Any
from .database import get_table


class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, user_id: str):
        await websocket.accept()
        self.active_connections[user_id] = websocket
        print(f"User {user_id} connected. Total connections: {len(self.active_connections)}")

    def disconnect(self, user_id: str):
        if user_id in self.active_connections:
            del self.active_connections[user_id]
            print(f"User {user_id} disconnected. Total connections: {len(self.active_connections)}")

    async def broadcast_to_conversation(
        self, 
        message: Dict[str, Any], 
        conversation_id: str,
        exclude_user: str = None
    ):
        # Get conversation participants from conversation_users table
        conv_users_table = get_table('conversation_users')
        participants = conv_users_table.query(
            KeyConditionExpression='conversationId = :cid',
            ExpressionAttributeValues={
                ':cid': conversation_id
            }
        )
        
        if 'Items' in participants:
            for participant in participants['Items']:
                user_id = participant['userId']
                if user_id != exclude_user and user_id in self.active_connections:
                    try:
                        await self.active_connections[user_id].send_json(message)
                    except Exception as e:
                        print(f"Error sending message to user {user_id}: {str(e)}")
                        self.disconnect(user_id)

    async def send_personal_message(self, message: dict, user_id: str):
        if user_id in self.active_connections:
            try:
                await self.active_connections[user_id].send_json(message)
            except Exception as e:
                print(f"Error sending personal message to user {user_id}: {str(e)}")
                self.disconnect(user_id)

manager = ConnectionManager()