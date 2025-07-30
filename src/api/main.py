"""
FastAPI Application for WhatsApp RAG Multi-Agent Bot.

This module contains the main FastAPI application with health check endpoint
and future webhook endpoints for Twilio integration and agent orchestration.
"""

import logging
import sys
from contextlib import asynccontextmanager
from typing import Dict, Any

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import structlog

# Configure structured logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager for startup and shutdown events."""
    # Startup
    logger.info("Starting WhatsApp RAG Multi-Agent Bot API")
    
    # Initialize any required services here
    # - Vector database connections
    # - Agent initialization
    # - Knowledge base loading
    
    yield
    
    # Shutdown
    logger.info("Shutting down WhatsApp RAG Multi-Agent Bot API")
    # Cleanup resources here


# Create FastAPI application
app = FastAPI(
    title="WhatsApp RAG Multi-Agent Bot",
    description="Production-ready RAG-powered multi-agent system for WhatsApp integration via Twilio",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add rate limiting
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler for unhandled exceptions."""
    logger.error(
        "Unhandled exception occurred",
        exc_info=exc,
        path=request.url.path,
        method=request.method
    )
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )


@app.get("/health")
async def health_check() -> Dict[str, Any]:
    """
    Health check endpoint for monitoring and load balancing.
    
    Returns:
        Dict[str, Any]: Health status information including service status,
                       timestamp, and system information.
    """
    logger.info("Health check requested")
    
    return {
        "status": "ok",
        "service": "WhatsApp RAG Multi-Agent Bot",
        "version": "2.0.0",
        "python_version": sys.version,
        "environment": "production"  # This should come from environment variable
    }


@app.get("/")
async def root() -> Dict[str, str]:
    """
    Root endpoint providing basic API information.
    
    Returns:
        Dict[str, str]: Basic API information and status.
    """
    return {
        "message": "WhatsApp RAG Multi-Agent Bot API",
        "status": "running",
        "docs": "/docs",
        "health": "/health"
    }


# Future endpoints will be added here:
# - POST /webhook/twilio - Twilio webhook handler
# - POST /agents/query - Direct agent query endpoint
# - GET /knowledge/status - Knowledge base status
# - POST /knowledge/update - Update knowledge base
# - GET /agents/list - List available agents
# - POST /agents/create - Create new agent