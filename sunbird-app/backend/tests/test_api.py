# This is a basic test script I used early on to verify the old summarise endpoint was working before I switched to the faster sunflower_simple endpoint.

import requests
import os
from dotenv import load_dotenv

# Loading the .env file so I can grab my secret token securely.
load_dotenv()

# Retrieving the Sunbird API token from the environment variables.
token = os.getenv("SUNBIRD_API_TOKEN")

# Printing a small chunk of the token just to make sure it loaded properly.
print(f"Token: {token[:15]}...")

# Making a POST request to the summarise endpoint to test the model.
response = requests.post(
    "https://api.sunbird.ai/tasks/summarise",
    
    # Sending a quick test sentence as JSON data.
    json={"text": "Hello my name is John. I am from Uganda."},
    
    # Passing the Bearer token for authentication and explicitly setting the Content-Type to application/json.
    headers={
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    },
    
    # Giving it a 30-second timeout just in case the server is slow.
    timeout=30
)

# Printing the final status code and response body to see the summary result.
print(f"Status: {response.status_code}")
print(f"Response: {response.text}")