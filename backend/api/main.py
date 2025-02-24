from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from api.database import create_tables
from api.routes import messages, webhooks, websocket
from api.routes import users, conversations
from api.websocket_manager import ConnectionManager

app = FastAPI(title="Real-time Messenger API")

# Initialize the WebSocket manager
manager = ConnectionManager()

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

# Create DynamoDB tables on startup
@app.on_event("startup")
async def startup_event():
    create_tables()
# Mount static files directory
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

@app.get("/")
def read_root():
    return {"message": "Welcome to Real-time Messenger API"}
