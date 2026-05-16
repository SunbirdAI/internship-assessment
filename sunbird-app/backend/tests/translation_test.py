# This script tests the translation endpoint to make sure I can successfully translate English text into a local Ugandan language. I run this to confirm the payload format is correct before hooking it up to the main pipeline.

import requests, os
from dotenv import load_dotenv

# Loading the .env file using its absolute path so the script can find it regardless of where I run it from.
load_dotenv(dotenv_path=r"C:\Users\CLIENT\Documents\SUNBIRD AI\internship-assessment\sunbird-app\.env")

# Grabbing the API token securely from the environment variables.
token = os.getenv("SUNBIRD_API_TOKEN")

# Making a POST request to the translation endpoint.
response = requests.post(
    "https://api.sunbird.ai/tasks/translate",
    
    # The payload requires the text, the source language, and the target language. I'm testing English to Luganda here.
    json={"text": "Hello my name is John.", "source_language": "eng", "target_language": "lug"},
    
    # Passing the Bearer token for authentication and explicitly setting the Content-Type to application/json.
    headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
    
    # Setting a 60-second timeout because translation models can sometimes take a little while to process longer sentences.
    timeout=60
)

# Printing the raw status code and the response body so I can verify the translated text looks correct.
print(response.status_code, response.text)