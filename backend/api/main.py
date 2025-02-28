from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import boto3
import os
from api.database import create_tables
from api.routes import messages, webhooks, websocket
from api.routes import users, conversations

app = FastAPI(title="Real-time Messenger API")


# Initialize as None, will be set during startup
s3_client = None

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Add your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*", "Authorization"],  # Explicitly include Authorization
)

# Include webhook routes
app.include_router(webhooks.router, prefix="/api", tags=["webhooks"])
app.include_router(users.router, prefix="/api", tags=["users"])
app.include_router(conversations.router, prefix="/api", tags=["conversations"])
app.include_router(messages.router, prefix="/api", tags=["messages"])
app.include_router(websocket.router, tags=["websocket"])

# Create DynamoDB tables and initialize S3 client on startup
@app.on_event("startup")
async def startup_event():
    create_tables()
    init_s3_client()

# Mount static files directory
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

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
