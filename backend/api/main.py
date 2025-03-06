from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import boto3
import os
from api.database import create_tables
from api.routes import messages, webhooks
from api.routes import users, conversations
from api.socketio_manager import socket_app
import socketio

app = FastAPI(title="Real-time Messenger API")

# Initialize as None, will be set during startup
s3_client = None

# Configure CORS only once for the entire application
origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include webhook routes
app.include_router(webhooks.router, prefix="/api", tags=["webhooks"])
app.include_router(users.router, prefix="/api", tags=["users"])
app.include_router(conversations.router, prefix="/api", tags=["conversations"])
app.include_router(messages.router, prefix="/api", tags=["messages"])

# Mount Socket.IO app
app.mount("/socket.io", socket_app)

# Print confirmation that CORS is configured
print(f"CORS configured with allowed origins: {origins}")

# Create DynamoDB tables and initialize S3 client on startup
@app.on_event("startup")
async def startup_event():
    create_tables()
    init_s3_client()


@app.get("/")
def read_root():
    return {"message": "Welcome to Real-time Messenger API"}

def init_s3_client():
    global s3_client
    s3_client = boto3.client(
        's3',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        region_name=os.getenv('AWS_REGION')
    )

# Make sure your Socket.IO server also has CORS configured
sio = socketio.AsyncServer(
    async_mode='asgi',
    cors_allowed_origins=["http://localhost:3000"]  # Match your frontend URL
)
