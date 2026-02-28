from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.exception_handlers import (
    generic_exception_handler,
    http_exception_handler,
    starlette_exception_handler,
    validation_exception_handler,
    value_error_handler,
)
from api.routes import transaction
from api.routes import category
from core.config import settings
from api.routes import users
from app.db.session import close_db, init_db
from fastapi.middleware.cors import CORSMiddleware
from app.mcp_server import (
    mcp,
)  # Import your mcp instance form the app so that when we run inside the ap it will work


# Lifespan context manager for startup and shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage FastAPI application lifecycle"""
    print("Starting up...")
    await init_db()
    yield
    print("Shutting down...")
    await close_db()


# Create the FastAPI app with metadata (Only done ONCE)
app = FastAPI(
    title="Fintrac Backend",
    description="Backend API for Fintrac application",
    version="1.0.0",
    lifespan=lifespan,
)


# Configure the CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register the global exception handlers
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(StarletteHTTPException, starlette_exception_handler)
app.add_exception_handler(ValueError, value_error_handler)
app.add_exception_handler(Exception, generic_exception_handler)


# Include the user routes
app.include_router(users.router)
app.include_router(category.router)
app.include_router(transaction.router)


# Root endpoint
@app.get("/", tags=["Root"], summary="Root endpoint", description="Welcome message")
async def root():
    """
    Root endpoint welcome message.
    """
    return {
        "message": f"Welcome to {settings.APP_NAME}! 🎉",
        "docs_url": "/docs",
        "version": "1.0.0",
    }


# Mount the MCP server onto the FastAPI app
# This makes the MCP server available at http://localhost:8000/mcp
app.mount("/mcp", mcp.sse_app())
