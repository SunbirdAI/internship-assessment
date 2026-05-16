# This script tests the NLLB translation endpoint directly. I use this to make sure English to Luganda translation is working correctly before updating the main pipeline.

import requests
import os
from dotenv import load_dotenv

# Loading the .env file so I can access the API token securely.
load_dotenv()

# Retrieving the Sunbird API token from the environment variables.
token = os.getenv("SUNBIRD_API_TOKEN")

# Making a POST request to the NLLB translate endpoint.
response = requests.post(
    "https://api.sunbird.ai/tasks/nllb_translate",
    
    # Sending the text, source language, and target language as a JSON payload.
    json={
        "text": "Hello my name is John.",
        "source_language": "eng",
        "target_language": "lug"
    },
    
    # Adding the Bearer token for authentication and explicitly setting the Content-Type.
    headers={
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    },
    
    # Setting a 60-second timeout.
    timeout=60
)

# Printing the final status code and response body to verify the translated text.
print(f"Status: {response.status_code}")
print(f"Response: {response.text}")