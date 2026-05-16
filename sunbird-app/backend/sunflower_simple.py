# This is a standalone test script I created to test the Sunflower Simple endpoint. I like to test individual API calls in isolation before plugging them into the main app.py pipeline because this helps me ensure the API is returning what I expect without the overhead of Streamlit.

import requests
import os
from dotenv import load_dotenv

# I'm loading the .env file explicitly using its absolute path here. Since I'm running this script directly from the backend folder, I want to make absolutely sure it finds the .env file which is located one directory up in the sunbird-app folder.
load_dotenv(dotenv_path=r"C:\Users\CLIENT\Documents\SUNBIRD AI\internship-assessment\sunbird-app\.env")

# Grabbing the API token securely from the environment variables.
token = os.getenv("SUNBIRD_API_TOKEN")

# Making a POST request to the sunflower_simple endpoint which is powered by the Qwen model and is much faster than the older /tasks/summarise endpoint.
response = requests.post(
    "https://api.sunbird.ai/tasks/sunflower_simple",
    
    # CRITICAL: I use `data=` here instead of `json=`. I learned the hard way that this specific endpoint expects application/x-www-form-urlencoded format. If I sent JSON, it would fail with a 422 Unprocessable Entity error.
    data={
        # The instruction tells the model exactly what to do with the text.
        "instruction": "Summarize in one sentence: The rain in Uganda falls mostly between March and May.",
        # Specifying the underlying model.
        "model_type": "qwen",
        # I set the temperature to 0.3 to keep the model's response focused and deterministic.
        "temperature": 0.3
    },
    
    # Adding the Bearer token to the Authorization header so Sunbird knows it's me.
    headers={
        "Authorization": f"Bearer {token}"
    },
    
    # Setting a 60-second timeout because language models can sometimes take a while to generate text, especially for longer prompts, so giving it enough time is important to prevent false failures.
    timeout=60
)

# Printing the raw status code and text response so I can inspect exactly what the API sent back.
print(response.status_code, response.text)