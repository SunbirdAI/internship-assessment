# Another early test script I made to experiment with the summarise endpoint, this time with a slightly longer sentence about a brown fox.

import requests
import os
from dotenv import load_dotenv

# Loading the .env file to securely access my API token.
load_dotenv()

# Grabbing the Sunbird API token from the environment variables.
token = os.getenv("SUNBIRD_API_TOKEN")

# Making a POST request to the summarise endpoint.
response = requests.post(
    "https://api.sunbird.ai/tasks/summarise",
    
    # Sending the test sentence as JSON to see how the model shortens it.
    json={"text": "The quick brown fox jumps over the lazy dog. This is a test sentence for summarization."},
    
    # Attaching the Bearer token and specifying JSON content type.
    headers={
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    },
    
    # Setting a 60-second timeout since longer sentences might take more time.
    timeout=60
)

# Printing the final status code and the response body.
print(f"Status: {response.status_code}")
print(f"Response: {response.text}")