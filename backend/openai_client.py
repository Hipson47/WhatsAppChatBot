"""
OpenAI Client Module.

This module handles all communication with the OpenAI API for generating
AI responses to user messages.
"""

import os
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


async def get_ai_response(user_prompt: str) -> str:
    """
    Generate an AI response using OpenAI's GPT-4o-mini model.
    
    This function takes a user prompt and generates a response using OpenAI's
    chat completions API with the gpt-4o-mini model.
    
    Args:
        user_prompt (str): The user's message to generate a response for.
        
    Returns:
        str: The AI-generated response content.
        
    Raises:
        Exception: If there's an error communicating with the OpenAI API.
    """
    try:
        # Initialize OpenAI client with API key from environment
        client = openai.AsyncOpenAI(
            api_key=os.getenv("OPENAI_API_KEY")
        )
        
        # Define system prompt
        system_prompt = "You are a helpful assistant."
        
        # Call OpenAI chat completions API
        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=150,
            temperature=0.7
        )
        
        # Extract and return the AI response content
        ai_response = response.choices[0].message.content
        return ai_response if ai_response else "I'm sorry, I couldn't generate a response."
        
    except openai.APIError as e:
        error_message = f"OpenAI API error: {str(e)}"
        print(error_message)
        return "I'm experiencing technical difficulties. Please try again later."
        
    except openai.RateLimitError as e:
        error_message = f"OpenAI rate limit exceeded: {str(e)}"
        print(error_message)
        return "I'm currently busy. Please try again in a moment."
        
    except openai.AuthenticationError as e:
        error_message = f"OpenAI authentication error: {str(e)}"
        print(error_message)
        return "There's a configuration issue. Please contact support."
        
    except Exception as e:
        error_message = f"Unexpected error while getting AI response: {str(e)}"
        print(error_message)
        return "I encountered an unexpected error. Please try again." 