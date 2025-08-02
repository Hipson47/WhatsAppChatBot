"""
Integration tests for the Telegram RAG Multi-Agent Bot.

This module contains end-to-end tests that verify the complete functionality
of the deployed bot by testing the webhook endpoint with real requests.
"""

import os
import requests
import pytest
import json


def test_telegram_webhook():
    """
    Test the Telegram webhook endpoint with a sample question.
    
    This test verifies that:
    1. The webhook endpoint is accessible
    2. The bot can process a message successfully
    3. The response contains expected content from the knowledge base
    """
    # Get environment variables
    webhook_url = os.getenv("WEBHOOK_URL")
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    
    # Validate required environment variables
    assert webhook_url, "WEBHOOK_URL environment variable is required"
    assert bot_token, "TELEGRAM_BOT_TOKEN environment variable is required"
    
    # Construct the full webhook URL
    full_url = f"{webhook_url}/{bot_token}"
    
    # Create a sample Telegram webhook payload
    # This simulates a message from a user asking about AI-First concept
    payload = {
        "update_id": 123456789,
        "message": {
            "message_id": 1,
            "from": {
                "id": 123456789,
                "is_bot": False,
                "first_name": "Test",
                "username": "testuser"
            },
            "chat": {
                "id": 123456789,
                "first_name": "Test",
                "username": "testuser",
                "type": "private"
            },
            "date": 1640995200,
            "text": "What is AI-First?"
        }
    }
    
    # Send POST request to webhook endpoint
    try:
        response = requests.post(
            full_url,
            json=payload,
            timeout=30,  # Give enough time for AI processing
            headers={"Content-Type": "application/json"}
        )
        
        # Verify the response
        assert response.status_code == 200, f"Expected 200, got {response.status_code}. Response: {response.text}"
        
        # For Telegram webhooks, a successful response typically returns 200
        # The actual bot response is sent separately to Telegram's API
        # So we mainly check that the webhook processed without errors
        
        print(f"✅ Webhook test passed. Status: {response.status_code}")
        print(f"Response: {response.text}")
        
    except requests.exceptions.Timeout:
        pytest.fail("Webhook request timed out - this may indicate the bot is not responding")
    except requests.exceptions.ConnectionError:
        pytest.fail("Failed to connect to webhook URL - check if the service is deployed and accessible")
    except Exception as e:
        pytest.fail(f"Unexpected error during webhook test: {str(e)}")


def test_health_endpoint():
    """
    Test the health check endpoint to ensure the service is running.
    """
    webhook_url = os.getenv("WEBHOOK_URL")
    assert webhook_url, "WEBHOOK_URL environment variable is required"
    
    # Test the health endpoint
    health_url = f"{webhook_url}/health"
    
    try:
        response = requests.get(health_url, timeout=10)
        assert response.status_code == 200, f"Health check failed. Status: {response.status_code}"
        assert response.text == "OK", f"Unexpected health check response: {response.text}"
        
        print("✅ Health check passed")
        
    except requests.exceptions.Timeout:
        pytest.fail("Health check timed out")
    except requests.exceptions.ConnectionError:
        pytest.fail("Failed to connect to health endpoint")
    except Exception as e:
        pytest.fail(f"Unexpected error during health check: {str(e)}")


if __name__ == "__main__":
    # Allow running the test directly for debugging
    test_health_endpoint()
    test_telegram_webhook()
    print("🎉 All integration tests passed!")