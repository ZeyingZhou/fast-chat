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
        user_conversations = conv_users_table.query(
            IndexName='by-user',
            KeyConditionExpression='userId = :uid',
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
                print("conv_id: ", conv_id)
                await sio.enter_room(sid, conv_id)
                print("rooms: ", sio.rooms(sid))
                print(f"User {user_id} joined room {conv_id}")
                sio.emit("room count", {"count": len(sio.rooms(sid))})
        
        # Store user's conversations for later use
        self.user_conversations[user_id] = conversation_ids
        
        print(f"User {user_id} connected. Total connections: {len(self.active_connections)}")
        
    def disconnect(self, user_id: str):
        """Remove a Socket.IO connection"""
        if user_id in self.active_connections:
            sid = self.active_connections[user_id]
            
            # Leave all conversation rooms
            if user_id in self.user_conversations:
                for conv_id in self.user_conversations[user_id]:
                    sio.leave_room(sid, conv_id)
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
        exclude_user: str = None,
        sid: str = None
    ):
        """Broadcast a message to all users in a conversation"""
        # Simply emit to the conversation room, excluding the sender if needed
        # print(f"Broadcasting message to conversation {conversation_id}: {message}")
        # print("message: ", message.get('senderId'))
        print("exclude_user: ", exclude_user)
        print("active_connections: ", self.active_connections)
        # print("rooms: ", sio.rooms(sid))
        if exclude_user and exclude_user in self.active_connections:
            for user in self.active_connections:
                print("rooms: ", sio.rooms(self.active_connections[user]))
                if user != exclude_user:
                    print("sid: ", sid)
                    print("sid: ", self.active_connections[user], "exclude_sid: ", self.active_connections[exclude_user])
                    await sio.emit('message received', message, room=conversation_id)

        # if exclude_user and exclude_user in self.active_connections:
        #     exclude_sid = self.active_connections.get(exclude_user)
        #     print(f"Excluding user {exclude_user} with sid {exclude_sid}")
        #     print(self.active_connections)
        #     for user in self.active_connections:
        #         if user != exclude_user:
        #             print("sid: ", self.active_connections[user], "exclude_sid: ", exclude_sid)
        #             await sio.emit('message received', message, to=self.active_connections[user])
        else:
            print("No exclude_user specified")
            await sio.emit('message', message, room=conversation_id)
        
        print(f"Broadcast complete to room {conversation_id}")
    
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
                    self.disconnect(notify_user_id)
                        


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
        manager.disconnect(user_id)
    print(f"Socket.IO client disconnected: {sid}")

@sio.event
async def authenticate(sid, data):
    """Authenticate a user and associate their user_id with the socket id"""
    user_id = data.get('user_id')
    if user_id:
        await manager.register_connection(user_id, sid)
        # Broadcast online status after connecting
        await manager.broadcast_user_status(user_id, True)
        print(f"User {user_id} authenticated with sid {sid}")
        return {'status': 'success'}
    return {'status': 'error', 'message': 'Authentication failed'}



# Add a new event to get online users
@sio.event
async def get_online_users(sid, data=None):
    """Return a list of online users"""
    return {'online_users': list(manager.online_users)}

# @sio.event
# async def join_conversation(sid, data):
#     """Join a specific conversation room"""
#     print(f"Joining conversation {data.get('conversationId')}")
#     conversation_id = data.get('conversationId')
#     if conversation_id:
#         sio.enter_room(sid, conversation_id)
#         print(f"Successfully joined room {conversation_id} for sid {sid}")
#         return {'status': 'success'}
#     return {'status': 'error', 'message': 'Invalid conversation ID'}

@sio.event
async def leave_conversation(sid, data):
    """Leave a specific conversation room"""
    print(f"Leaving conversation {data.get('conversationId')}")
    conversation_id = data.get('conversationId')
    if conversation_id:
        sio.leave_room(sid, conversation_id)
        return {'status': 'success'}
    return {'status': 'error', 'message': 'Invalid conversation ID'}



@sio.on("new message")
async def message(sid, data):
    """Handle new message events"""
    # Extract necessary data
    user_id = data.get('user_id')
    conversation_id = data.get('conversationId')
    messages_table = get_table('messages')
    
    if not user_id or not conversation_id:
        print(f"Invalid message data: {data}")
        return {'status': 'error', 'message': 'Missing user_id or conversationId'}
    
    try:
        current_time = datetime.now().isoformat()
        message_id = str(uuid.uuid4())

        files_url = data.get('filesUrl', [])
        if not isinstance(files_url, list):
            files_url = []
        message_data = {
            'id': message_id,
            'conversationId': conversation_id,
            'senderId': user_id,
            'body': data.get('content', ''),
            'files': files_url,  # Using get() with default empty list
            'createdAt': current_time
        }
        try:
            messages_table.put_item(Item=message_data)
        except Exception as db_error:
            print(f"DynamoDB error: {str(db_error)}")
            # Check if table exists
            print(f"Table info: {messages_table.table_status if hasattr(messages_table, 'table_status') else 'Unknown'}")
            return {'status': 'error', 'message': f'Database error: {str(db_error)}'}
        
        users_table = get_table('users')
        sender_response = users_table.get_item(Key={'id': data['user_id']})
        sender = sender_response.get('Item', {})
        formatted_message = {
            **message_data,
            'sender': sender
        }
        # Broadcast the message to the conversation
        await manager.broadcast_to_conversation(
            formatted_message,
            data['conversationId'],
            user_id,  # Changed from sid to user_id
            sid
        )

        return {'status': 'success'}
    except Exception as e:
        print(f"Error broadcasting message: {str(e)}")
        return {'status': 'error', 'message': str(e)}

@sio.event
async def get_room_info(sid, data=None):
    """Return information about rooms and users"""
    try:
        # Get rooms this socket is in
        socket_rooms = sio.rooms(sid)
        
        # Get all active connections
        active_users = {user_id: s_id for user_id, s_id in manager.active_connections.items()}
        
        # Get room membership for all rooms
        room_info = {}
        for room in manager.user_conversations.values():
            for room_id in room:
                if room_id not in room_info:
                    room_info[room_id] = []
                
                # Find users in this room
                for user_id, user_rooms in manager.user_conversations.items():
                    if room_id in user_rooms:
                        room_info[room_id].append(user_id)
        
        return {
            'status': 'success',
            'socket_id': sid,
            'socket_rooms': list(socket_rooms),
            'active_users': active_users,
            'room_info': room_info,
            'online_users': list(manager.online_users)
        }
    except Exception as e:
        print(f"Error getting room info: {str(e)}")
        return {'status': 'error', 'message': str(e)}


@sio.event
async def list_rooms(sid):
    """Return the number of rooms a user is in"""
    for user_id, sid  in manager.active_connections.items():
        print("user_id: ", user_id)
        print("sid: ", sid)
        print("rooms: ", sio.rooms(sid))
