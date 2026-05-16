# This script tests the Modal Speech-to-Text (STT) endpoint to make sure audio file uploads are working correctly. I use this to verify the API can actually transcribe my test audio files before integrating it into the main app.

import requests
import os
from dotenv import load_dotenv

# Loading the .env file using its absolute path so the script can find it regardless of where I run it from.
load_dotenv(dotenv_path=r"C:\Users\CLIENT\Documents\SUNBIRD AI\internship-assessment\sunbird-app\.env")

# Grabbing the API token securely from the environment variables.
token = os.getenv("SUNBIRD_API_TOKEN")

# Printing a small piece of the token just to confirm it loaded correctly without exposing the whole thing.
print(f"Token: {token[:20]}...")

# Storing the absolute path to my test audio file so I don't have to worry about relative path issues.
AUDIO_FILE = r"C:\Users\CLIENT\Documents\SUNBIRD AI\internship-assessment\sunbird-app\backend\tests\audio_test _0.mp3"

# Opening the audio file in binary read mode ('rb') which is required when sending files over HTTP.
with open(AUDIO_FILE, "rb") as audio_file:
    # Making the POST request to the modal STT endpoint.
    response = requests.post(
        "https://api.sunbird.ai/tasks/modal/stt",
        
        # Sending the file using the files parameter and explicitly setting the MIME type to audio/mpeg so the API knows exactly what format it's receiving.
        files={"audio": ("test_audio.mp3", audio_file, "audio/mpeg")},
        
        # Adding the Bearer token to the Authorization header.
        headers={"Authorization": f"Bearer {token}"},
        
        # Setting a generous timeout of 180 seconds because transcribing audio is computationally heavy and can take a long time for larger files.
        timeout=180
    )

# Printing the final status code and response text so I can verify the transcription worked.
print(f"Status: {response.status_code}")
print(f"Response: {response.text}")