# This script uses a GET request to test if the NLLB translate endpoint is reachable and to see what response it gives when accessed without a payload.

import requests
import os
from dotenv import load_dotenv

# Loading the .env file so the script can access my secret tokens.
load_dotenv()

# Grabbing the Sunbird API token from the environment variables.
token = os.getenv("SUNBIRD_API_TOKEN")

# Making a simple GET request to the NLLB translate endpoint just to check its status.
response = requests.get(
    "https://api.sunbird.ai/tasks/nllb_translate",
    
    # Adding the Bearer token for authentication.
    headers={"Authorization": f"Bearer {token}"},
    
    # Giving it a 30-second timeout.
    timeout=30
)

# Printing the status code and response body to see how the API handles a GET request to this endpoint.
print(f"Status: {response.status_code}")
print(f"Response: {response.text}")