from contextlib import asynccontextmanager
from fastapi import FastAPI

from core.config import Settings
from api.routes import users
from app.db.session import close_db, init_db
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="My First FastAPI Backend")


# Lifespan context manager for startup and shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage Fast api application lifecycle"""

    # Startup code
    print("Starting up...")
    await init_db()
    yield
    # Shutdown code
    print("Shutting down...")
    await close_db()


# create the FastAPI app with metadata
app = FastAPI(
    title="Fintrac Backend",
    description="Backend API for Fintrac application",
    version="1.0.0",
    lifespan=lifespan,
)


# configure the CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# include the user routes
app.include_router(users.router)


# Root endpoint
@app.get("/", tags=["Root"], summary="Root endpoint", description="Welcome message")
async def root():
    """
    Root endpoint welcome message.

    **Returns:**
    - **message**: Welcome message
    - **docs_url**: API documentation URL
    """
    return {
        "message": f"Welcome to {Settings.APP_NAME}! 🎉",
        "docs_url": "/docs",
        "version": "1.0.0",
    }
