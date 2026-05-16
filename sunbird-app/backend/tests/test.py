# This is a very basic scratchpad script I used to quickly test the NLLB translation endpoint. It's not fully wired up to the .env file but it helps me check payload formats.

import requests

# Setting up the headers with a placeholder token to test the API request structure.
headers = {
    "Authorization": "Bearer YOUR_API_KEY",
    "Content-Type": "application/json"
}

# Creating the JSON payload to translate an English phrase into Luganda.
payload = {
    "text": "hello my name is john",
    "target_language": "lug"  # Adjust to match your actual param
}

# Sending the POST request to the NLLB translate endpoint.
response = requests.post(
    "https://api.sunbird.ai/tasks/nllb_translate",  # Verify the exact endpoint
    
    # Passing the headers and payload explicitly.
    headers=headers,
    json=payload,
    
    # Giving it a 30-second timeout.
    timeout=30
)

# Printing the final status code and the JSON response to see what the server returns.
print(response.status_code, response.json())