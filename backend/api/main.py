from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from .database import engine
from . import models
from .routes import users, messages, chat_rooms, reactions

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Real-time Messenger API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Add your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files directory
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Include routers
app.include_router(users.router)
app.include_router(messages.router)
app.include_router(chat_rooms.router)
app.include_router(reactions.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Real-time Messenger API"}