"""
OpenAI Client Module.

This module handles all communication with the OpenAI API for generating
AI responses to user messages.
"""

import os
import logging
import openai
from dotenv import load_dotenv

# Configure logging
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()


async def get_ai_response(user_prompt: str, max_tokens: int = 150) -> str:
    """
    Generate an AI response using OpenAI's GPT-4o-mini model.
    
    This function takes a user prompt and generates a response using OpenAI's
    chat completions API with the gpt-4o-mini model.
    
    Args:
        user_prompt (str): The user's message to generate a response for.
        max_tokens (int): Maximum number of tokens in the response.
        
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
            max_tokens=max_tokens,
            temperature=0.7
        )
        
        # Extract and return the AI response content
        ai_response = response.choices[0].message.content
        return ai_response if ai_response else "I'm sorry, I couldn't generate a response."
        
    except openai.APIError as e:
        logger.error(f"OpenAI API error: {str(e)}")
        return "I'm experiencing technical difficulties. Please try again later."
        
    except openai.RateLimitError as e:
        logger.warning(f"OpenAI rate limit exceeded: {str(e)}")
        return "I'm currently busy. Please try again in a moment."
        
    except openai.AuthenticationError as e:
        logger.error(f"OpenAI authentication error: {str(e)}")
        return "There's a configuration issue. Please contact support."
        
    except Exception as e:
        logger.error(f"Unexpected error while getting AI response: {str(e)}", exc_info=True)
        return "I encountered an unexpected error. Please try again." 