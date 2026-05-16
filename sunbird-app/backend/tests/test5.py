# Another quick test script for the translation endpoint to verify I can translate a short English greeting into Luganda.

import requests, os
from dotenv import load_dotenv

# Loading the .env file securely.
load_dotenv()

# Grabbing the API token from the environment.
token = os.getenv("SUNBIRD_API_TOKEN")

# Making a POST request to the translation endpoint.
response = requests.post(
    "https://api.sunbird.ai/tasks/translate",
    
    # Providing the English text and specifying I want it translated to Luganda (lug).
    json={"text": "Hello my name is John.", "source_language": "eng", "target_language": "lug"},
    
    # Including the Bearer token and specifying the content type as JSON.
    headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
    
    # Setting a 60-second timeout for the translation task.
    timeout=60
)

# Printing out the status code and the API's response to check the output.
print(response.status_code, response.text)