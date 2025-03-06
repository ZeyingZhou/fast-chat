from typing import Dict, Any, Set
from .database import get_table
import socketio
from datetime import datetime
import uuid

# Create a Socket.IO server
sio = socketio.AsyncServer(
    async_mode='asgi',
    cors_allowed_origins=[]  # Configure this based on your needs
)

# Create an ASGI application
socket_app = socketio.ASGIApp(sio)

class SocketIOManager:
    def __init__(self):
        self.active_connections: Dict[str, str] = {}  # user_id -> sid mapping
        self.online_users: Set[str] = set()  # Set of online user IDs
        self.user_conversations: Dict[str, Set[str]] = {}  # user_id -> set of conversation_ids
        
    async def register_connection(self, user_id: str, sid: str):
        """Register a new Socket.IO connection"""
        self.active_connections[user_id] = sid
        self.online_users.add(user_id)
        
        # Join rooms for all conversations this user is part of
        conv_users_table = get_table('conversation_users')
        user_conversations = conv_users_table.scan(
            FilterExpression='userId = :uid',
            ExpressionAttributeValues={
                ':uid': user_id
            }
        )
        
        conversation_ids = set()
        if 'Items' in user_conversations:
            for conv in user_conversations['Items']:
                conv_id = conv['conversationId']
                conversation_ids.add(conv_id)
                # Add user's socket to the conversation room
                await sio.enter_room(sid, conv_id)
        
        # Store user's conversations for later use
        self.user_conversations[user_id] = conversation_ids
        
        print(f"User {user_id} connected. Total connections: {len(self.active_connections)}")
        
    async def disconnect(self, user_id: str):
        """Remove a Socket.IO connection"""
        if user_id in self.active_connections:
            sid = self.active_connections[user_id]
            
            # Leave all conversation rooms
            if user_id in self.user_conversations:
                for conv_id in self.user_conversations[user_id]:
                    await sio.leave_room(sid, conv_id)
                del self.user_conversations[user_id]
            
            del self.active_connections[user_id]
            self.online_users.discard(user_id)
            print(f"User {user_id} disconnected. Total connections: {len(self.active_connections)}")
    
    def is_user_online(self, user_id: str) -> bool:
        """Check if a user is online"""
        return user_id in self.online_users
    
    def get_online_users(self) -> Set[str]:
        """Get all online users"""
        return self.online_users
            
    async def broadcast_to_conversation(
        self, 
        message: Dict[str, Any], 
        conversation_id: str,
        exclude_user: str = None
    ):
        """Broadcast a message to all users in a conversation"""
        # Simply emit to the conversation room, excluding the sender if needed
        print(f"Broadcasting message to conversation {conversation_id}")
        if exclude_user and exclude_user in self.active_connections:
            # exclude_sid = self.active_connections[exclude_user]
            print(message)
            print(exclude_user)
            print(conversation_id)
            await sio.emit('message', message, room=conversation_id, skip_sid=exclude_user)
        else:
            await sio.emit('message', message, room=conversation_id)
    
    async def broadcast_user_status(self, user_id: str, is_online: bool):
        """Broadcast a user's online status to relevant users"""
        # Get all conversations this user is part of
        conv_users_table = get_table('conversation_users')
        user_conversations = conv_users_table.scan(
            FilterExpression='userId = :uid',
            ExpressionAttributeValues={
                ':uid': user_id
            }
        )
        
        # Collect all users who should be notified (users who share conversations with this user)
        users_to_notify = set()
        
        if 'Items' in user_conversations:
            for conv in user_conversations['Items']:
                conv_id = conv['conversationId']
                
                # Get all users in this conversation
                participants = conv_users_table.query(
                    KeyConditionExpression='conversationId = :cid',
                    ExpressionAttributeValues={
                        ':cid': conv_id
                    }
                )
                
                if 'Items' in participants:
                    for participant in participants['Items']:
                        participant_id = participant['userId']
                        if participant_id != user_id:  # Don't notify the user about their own status
                            users_to_notify.add(participant_id)
        
        # Send status update to all relevant users
        for notify_user_id in users_to_notify:
            if notify_user_id in self.active_connections:
                try:
                    await sio.emit('message', {
                        'type': 'USER_STATUS',
                        'userId': user_id,
                        'isOnline': is_online
                    }, room=self.active_connections[notify_user_id])
                except Exception as e:
                    print(f"Error sending status update to user {notify_user_id}: {str(e)}")
                    await self.disconnect(notify_user_id)
                        
    # async def send_personal_message(self, message: dict, user_id: str):
    #     """Send a message to a specific user"""
    #     print(f"Sending personal message to user {user_id}: {message}")
    #     if user_id in self.active_connections:
    #         try:
    #             await sio.emit('message', message, room=self.active_connections[user_id])
    #         except Exception as e:
    #             print(f"Error sending personal message to user {user_id}: {str(e)}")
    #             self.disconnect(user_id)

# Create a singleton instance
manager = SocketIOManager()

# Socket.IO event handlers
@sio.event
async def connect(sid, environ):
    print(f"Socket.IO connection established: {sid}")

@sio.event
async def disconnect(sid):
    # Find user_id by sid and remove from active connections
    user_ids = [uid for uid, s in manager.active_connections.items() if s == sid]
    for user_id in user_ids:
        # Broadcast offline status before disconnecting
        await manager.broadcast_user_status(user_id, False)
        await manager.disconnect(user_id)
    print(f"Socket.IO client disconnected: {sid}")

@sio.event
async def authenticate(sid, data):
    """Authenticate a user and associate their user_id with the socket id"""
    user_id = data.get('user_id')
    if user_id:
        await manager.register_connection(user_id, sid)
        # Broadcast online status after connecting
        await manager.broadcast_user_status(user_id, True)
        await sio.emit('authenticated', {'status': 'success'}, room=sid)
        return {'status': 'success'}
    return {'status': 'error', 'message': 'Authentication failed'}

@sio.event
async def typing(sid, data):
    """Handle typing events"""
    user_id = data.get('user_id')
    conversation_id = data.get('conversationId')
    
    if user_id and conversation_id:
        # Get conversation participants
        conv_users = get_table('conversation_users').query(
            KeyConditionExpression='conversationId = :cid',
            ExpressionAttributeValues={
                ':cid': conversation_id
            }
        )
        
        # Notify other participants
        for user in conv_users.get('Items', []):
            if user['userId'] != user_id and user['userId'] in manager.active_connections:
                await sio.emit('message', {
                    'type': 'typing',
                    'userId': user_id,
                    'conversationId': conversation_id
                }, room=manager.active_connections[user['userId']])

@sio.event
async def seen(sid, data):
    """Handle seen events"""
    user_id = data.get('user_id')
    conversation_id = data.get('conversationId')
    
    if user_id and conversation_id:
        # Get conversation participants
        conv_users = get_table('conversation_users').query(
            KeyConditionExpression='conversationId = :cid',
            ExpressionAttributeValues={
                ':cid': conversation_id
            }
        )
        
        # Notify other participants
        for user in conv_users.get('Items', []):
            if user['userId'] != user_id and user['userId'] in manager.active_connections:
                await sio.emit('message', {
                    'type': 'seen',
                    'userId': user_id,
                    'conversationId': conversation_id
                }, room=manager.active_connections[user['userId']])

# Add a new event to get online users
@sio.event
async def get_online_users(sid, data=None):
    """Return a list of online users"""
    return {'online_users': list(manager.online_users)}

@sio.event
async def join_conversation(sid, data):
    """Join a specific conversation room"""
    print(f"Joining conversation {data.get('conversationId')}")
    conversation_id = data.get('conversationId')
    if conversation_id:
        await sio.enter_room(sid, conversation_id)
        return {'status': 'success'}
    return {'status': 'error', 'message': 'Invalid conversation ID'}

@sio.event
async def leave_conversation(sid, data):
    """Leave a specific conversation room"""
    print(f"Leaving conversation {data.get('conversationId')}")
    conversation_id = data.get('conversationId')
    if conversation_id:
        await sio.leave_room(sid, conversation_id)
        return {'status': 'success'}
    return {'status': 'error', 'message': 'Invalid conversation ID'}

@sio.event
async def message(sid, data):
    """Handle new message events"""
    print(f"Received message: {data}")
    
    # Extract necessary data
    user_id = data.get('user_id')
    conversation_id = data.get('conversationId')
    
    if not user_id or not conversation_id:
        print(f"Invalid message data: {data}")
        return {'status': 'error', 'message': 'Missing user_id or conversationId'}
    
    try:
        # Simply broadcast the message to the conversation
        # The HTTP route will handle database operations
        await manager.broadcast_to_conversation(
            {
                'type': 'NEW_MESSAGE',
                'message': data
            },
            conversation_id,
            sid
        )
        
        return {'status': 'success'}
    except Exception as e:
        print(f"Error broadcasting message: {str(e)}")
        return {'status': 'error', 'message': str(e)}
