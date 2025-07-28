from fastapi import FastAPI, Request, Response
from twilio.twiml.messaging_response import MessagingResponse
from backend.openai_client import get_ai_response

app = FastAPI()


@app.post("/webhook")
async def webhook(request: Request) -> Response:
    # Get form data from Twilio
    form_data = await request.form()
    
    # Extract sender and message
    sender = form_data.get("From")
    message_body = form_data.get("Body")
    
    # Print received message for logging
    print(f"Message from {sender}: {message_body}")
    
    # Get AI response from OpenAI
    ai_response = await get_ai_response(message_body)
    
    # Create TwiML response with AI-generated content
    twiml_response = MessagingResponse()
    twiml_response.message(ai_response)
    
    # Return XML response
    return Response(content=str(twiml_response), media_type="application/xml") 