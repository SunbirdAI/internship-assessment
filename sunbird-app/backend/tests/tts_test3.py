# This script tests the Modal Text-to-Speech (TTS) endpoint to verify that I can successfully convert text into an audio file. I use this to make sure I get a valid signed URL back before integrating it into the app.

import requests, os
from dotenv import load_dotenv

# Loading the .env file using its absolute path so the script can find it regardless of where I run it from.
load_dotenv(dotenv_path=r"C:\Users\CLIENT\Documents\SUNBIRD AI\internship-assessment\sunbird-app\.env")

# Grabbing the API token securely from the environment variables.
token = os.getenv("SUNBIRD_API_TOKEN")

# Making a POST request to the modal TTS endpoint because I found this one to be more reliable than the standard TTS endpoints.
response = requests.post(
    "https://api.sunbird.ai/tasks/modal/tts",
    
    # The payload requires the text and the speaker ID. I'm requesting a URL back instead of raw audio bytes so I can stream it directly in the frontend.
    json={
        "response_mode": "url",
        "speaker_id": 241,
        "text": "I am a nurse who takes care of many people."
    },
    
    # Passing the Bearer token for authentication and explicitly setting the Content-Type to application/json.
    headers={
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    },
    
    # Setting a generous timeout of 120 seconds because generating high-quality speech from text can be a slow process.
    timeout=120
)

# Printing the raw status code and the response body so I can grab the audio URL and test it in my browser.
print(response.status_code, response.text)