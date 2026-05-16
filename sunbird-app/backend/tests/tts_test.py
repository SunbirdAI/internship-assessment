# This script tests the Modal Text-to-Speech (TTS) endpoint to see if it can convert a Luganda phrase into speech using speaker 248.

import requests, os
from dotenv import load_dotenv

# Loading the .env file using its absolute path to prevent any path resolution issues.
load_dotenv(dotenv_path=r"C:\Users\CLIENT\Documents\SUNBIRD AI\internship-assessment\sunbird-app\.env")

# Grabbing the API token from the environment variables.
token = os.getenv("SUNBIRD_API_TOKEN")

# Making a POST request to the modal TTS endpoint.
response = requests.post(
    "https://api.sunbird.ai/tasks/modal/tts",
    
    # Supplying the Luganda text, the specific speaker ID, and requesting a URL response instead of raw bytes.
    data={
        "text": "Mwasuze mutya, amannya gange nze John.",
        "speaker_id": 248,
        "response_mode": "url"
    },
    
    # Including the Bearer token for authentication.
    headers={"Authorization": f"Bearer {token}"},
    
    # Setting a 60-second timeout.
    timeout=60
)

# Printing the status code and the response body to capture the audio URL.
print(response.status_code, response.text)