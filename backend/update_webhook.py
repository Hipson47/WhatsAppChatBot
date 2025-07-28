import os
import time
import requests
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

# Load credentials from .env file
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")

# Function to get the ngrok public URL
def get_ngrok_url():
    for i in range(10): # Try for 10 seconds
        try:
            response = requests.get("http://127.0.0.1:4040/api/tunnels")
            response.raise_for_status()
            tunnels = response.json()["tunnels"]
            for tunnel in tunnels:
                if tunnel["proto"] == "https":
                    print(f"Discovered ngrok URL: {tunnel['public_url']}")
                    return tunnel["public_url"]
        except requests.exceptions.RequestException:
            print(f"Ngrok API not ready yet. Retrying in 1 second...")
            time.sleep(1)
    return None

# Function to update Twilio webhook
def update_twilio_webhook(ngrok_url):
    if not all([TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER]):
        print("Error: Twilio environment variables not set. Skipping webhook update.")
        return

    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

        # Find the sandbox phone number SID
        incoming_phone_numbers = client.incoming_phone_numbers.list(phone_number=TWILIO_PHONE_NUMBER.replace("whatsapp:", ""))

        if not incoming_phone_numbers:
            print(f"Error: Could not find sandbox number {TWILIO_PHONE_NUMBER} in your Twilio account.")
            return

        sandbox_sid = incoming_phone_numbers[0].sid

        client.incoming_phone_numbers(sandbox_sid).update(
            sms_url=f"{ngrok_url}/webhook"
        )
        print(f"Successfully updated Twilio webhook to: {ngrok_url}/webhook")
    except Exception as e:
        print(f"An error occurred while updating Twilio webhook: {e}")

if __name__ == "__main__":
    ngrok_public_url = get_ngrok_url()
    if ngrok_public_url:
        update_twilio_webhook(ngrok_public_url)
    else:
        print("Error: Could not get ngrok URL after multiple retries.") 