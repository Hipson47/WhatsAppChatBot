"""
WhatsApp Bot FastAPI Application.

This module contains the main FastAPI application for handling WhatsApp webhooks
through Twilio integration with proper validation and error handling.
"""

from fastapi import FastAPI, Request, Response, Form, HTTPException
from pydantic import BaseModel
from twilio.twiml.messaging_response import MessagingResponse
from backend.openai_client import get_ai_response
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="WhatsApp Bot API",
    description="Production-ready FastAPI application for WhatsApp chatbot using Twilio",
    version="1.0.0"
)


class TwilioRequest(BaseModel):
    """
    Pydantic model for validating incoming Twilio webhook data.
    
    Attributes:
        Body (str): The message content sent by the user.
        From (str): The phone number of the message sender.
    """
    Body: str
    From: str


@app.get("/")
async def root() -> dict[str, str]:
    """
    Root endpoint for health check.
    
    Returns:
        dict[str, str]: Simple health check message confirming API is running.
    """
    return {"message": "WhatsApp Bot API is running", "status": "healthy"}


@app.post("/webhook")
async def webhook(data: TwilioRequest = Form(...)) -> Response:
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
        # Log received message for debugging
        logger.info(f"Message from {data.From}: {data.Body}")
        print(f"Message from {data.From}: {data.Body}")
        
        # Get AI response from OpenAI
        ai_response = await get_ai_response(data.Body)
        
        # Create TwiML response with AI-generated content
        twiml_response = MessagingResponse()
        twiml_response.message(ai_response)
        
        logger.info(f"Sending response to {data.From}: {ai_response}")
        
        # Return XML response
        return Response(
            content=str(twiml_response),
            media_type="application/xml"
        )
        
    except Exception as e:
        # Log the error for debugging
        error_message = f"Unexpected error processing webhook: {str(e)}"
        logger.error(error_message)
        
        # Return a 500 error with a generic message
        raise HTTPException(
            status_code=500,
            detail="Internal server error processing your message. Please try again later."
        ) 