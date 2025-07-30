"""
WhatsApp Bot FastAPI Application.

This module contains the main FastAPI application for handling WhatsApp webhooks
through Twilio integration with proper validation and error handling.
"""

import os
import logging
from fastapi import FastAPI, Response, Form, HTTPException, Request
from pydantic import BaseModel, Field, validator
from twilio.twiml.messaging_response import MessagingResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from openai_client import get_ai_response

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration from environment variables
MAX_MESSAGE_LENGTH = int(os.getenv("MAX_MESSAGE_LENGTH", "1000"))
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "150"))
RATE_LIMIT = os.getenv("RATE_LIMIT_PER_MINUTE", "10/minute")

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title="WhatsApp Bot API",
    description="Production-ready FastAPI application for WhatsApp chatbot using Twilio",
    version="1.0.0"
)

# Add rate limiting middleware
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


class TwilioRequest(BaseModel):
    """
    Pydantic model for validating incoming Twilio webhook data.
    
    Attributes:
        Body (str): The message content sent by the user.
        From (str): The phone number of the message sender.
    """
    Body: str = Field(..., max_length=MAX_MESSAGE_LENGTH, min_length=1)
    From: str = Field(..., regex=r'^whatsapp:\+\d{1,15}$')
    
    @validator('Body')
    def validate_message_content(cls, v):
        """Validate message content for security."""
        if not v.strip():
            raise ValueError('Message cannot be empty')
        # Basic XSS prevention
        dangerous_chars = ['<script', 'javascript:', 'data:', 'vbscript:']
        v_lower = v.lower()
        for char in dangerous_chars:
            if char in v_lower:
                raise ValueError('Message contains potentially dangerous content')
        return v.strip()


@app.get("/")
async def root() -> dict[str, str]:
    """
    Root endpoint for health check.
    
    Returns:
        dict[str, str]: Simple health check message confirming API is running.
    """
    return {"message": "WhatsApp Bot API is running", "status": "healthy"}


@app.post("/webhook")
@limiter.limit(RATE_LIMIT)
async def webhook(request: Request, data: TwilioRequest = Form(...)) -> Response:
    """
    Handle incoming WhatsApp messages from Twilio webhook.
    
    This endpoint processes incoming WhatsApp messages sent via Twilio's webhook,
    validates the form data using Pydantic models, generates an AI response using 
    OpenAI, and returns a TwiML response back to the sender.
    
    Args:
        data (TwilioRequest): Validated form data containing message body and sender
                            phone number from Twilio webhook.
        
    Returns:
        Response: XML response containing TwiML for replying to the message.
        
    Raises:
        HTTPException: 500 if there's an internal server error processing the request.
    """
    try:
        # Log received message for debugging (only log first 100 chars for security)
        safe_message = data.Body[:100] + "..." if len(data.Body) > 100 else data.Body
        logger.info(f"Message from {data.From}: {safe_message}")
        
        # Get AI response from OpenAI with configurable max_tokens
        ai_response = await get_ai_response(data.Body, max_tokens=MAX_TOKENS)
        
        # Create TwiML response with AI-generated content
        twiml_response = MessagingResponse()
        twiml_response.message(ai_response)
        
        logger.info(f"Sent response to {data.From} (length: {len(ai_response)})")
        
        # Return XML response
        return Response(
            content=str(twiml_response),
            media_type="application/xml"
        )
        
    except ValueError as e:
        # Handle validation errors
        logger.warning(f"Validation error from {data.From}: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail="Invalid message format or content"
        )
    except Exception as e:
        # Log the error for debugging
        logger.error(f"Unexpected error processing webhook from {data.From}: {str(e)}", exc_info=True)
        
        # Return a 500 error with a generic message
        raise HTTPException(
            status_code=500,
            detail="Internal server error processing your message. Please try again later."
        )


if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port) 