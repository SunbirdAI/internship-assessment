# This is a quick test script to verify that the language identification endpoint is working properly. I use this to make sure the API can correctly detect local Ugandan languages from raw text.

import requests, os
from dotenv import load_dotenv

# Loading the .env file using its absolute path so the script can find it regardless of where I run it from.
load_dotenv(dotenv_path=r"C:\Users\CLIENT\Documents\SUNBIRD AI\internship-assessment\sunbird-app\.env")

# Grabbing the API token securely from the environment variables.
token = os.getenv("SUNBIRD_API_TOKEN")

# Making a POST request to the language_id endpoint to see if it can figure out what language my test string is written in.
response = requests.post(
    "https://api.sunbird.ai/tasks/language_id",
    
    # Sending the raw text in JSON format since that is what this specific endpoint expects.
    json={"text": "mwasuzye mutya ba seebo nne ba nyabo"},
    
    # Passing the Bearer token for authentication and explicitly setting the Content-Type to application/json.
    headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
    
    # Setting a 30-second timeout which should be more than enough time for a simple text classification task.
    timeout=30
)

# Printing the raw status code and the response body so I can see what language the model guessed.
print(response.status_code, response.text)