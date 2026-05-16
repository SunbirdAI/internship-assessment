# This script tests the alternative RunPod TTS endpoint to compare its performance and reliability against the Modal endpoint.

import requests, os
from dotenv import load_dotenv

# Loading the .env file using its absolute path.
load_dotenv(dotenv_path=r"C:\Users\CLIENT\Documents\SUNBIRD AI\internship-assessment\sunbird-app\.env")

# Grabbing the API token from the environment variables.
token = os.getenv("SUNBIRD_API_TOKEN")

# Making a POST request to the RunPod TTS endpoint to see if it works better for speaker 248.
response = requests.post(
    "https://api.sunbird.ai/tasks/runpod/tts",
    
    # Passing the Luganda text and speaker ID as JSON.
    json={
        "text": "Mwasuze mutya, amannya gange nze John.",
        "speaker_id": 248
    },
    
    # Including the Bearer token and specifying the content type as JSON.
    headers={
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    },
    
    # Setting a 60-second timeout.
    timeout=60
)

# Printing the status code and response body.
print(response.status_code, response.text)