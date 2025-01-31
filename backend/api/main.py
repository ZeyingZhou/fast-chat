from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from api.database import engine
from api.chat_members import models as chat_members_models
from api.chat_rooms import models as chat_rooms_models
from api.messages import models as messages_models
from api.reactions import models as reactions_models
from api.users import models as users_models

# Import routes directly from their modules
from api.routes.users import router as users_router
from api.routes.messages import router as messages_router
from api.routes.chat_rooms import router as chat_rooms_router
from api.routes.reactions import router as reactions_router

# Create database tables
chat_members_models.Base.metadata.create_all(bind=engine)
chat_rooms_models.Base.metadata.create_all(bind=engine)
messages_models.Base.metadata.create_all(bind=engine)
reactions_models.Base.metadata.create_all(bind=engine)
users_models.Base.metadata.create_all(bind=engine)

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
app.include_router(users_router)
app.include_router(messages_router)
app.include_router(chat_rooms_router)
app.include_router(reactions_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Real-time Messenger API"}