# This is an older test script I used to test the standard STT endpoint before I upgraded to the Modal Whisper endpoint. I'm keeping it around for reference.

import requests
import os
from dotenv import load_dotenv

# Loading the .env file using its absolute path to avoid missing file errors.
load_dotenv(dotenv_path=r"C:\Users\CLIENT\Documents\SUNBIRD AI\internship-assessment\sunbird-app\.env")

# Retrieving the Sunbird API token from the environment variables.
token = os.getenv("SUNBIRD_API_TOKEN")

# Printing a small chunk of the token just to make sure it loaded properly.
print("Token:", token[:20])

# Opening my test audio file in binary read mode so I can send it over HTTP.
with open(r"C:\Users\CLIENT\Documents\SUNBIRD AI\internship-assessment\sunbird-app\backend\audio_test _0.mp3", "rb") as audio_file:
    # Making the POST request to the standard STT endpoint.
    response = requests.post(
        "https://api.sunbird.ai/tasks/stt",
        
        # Attaching the file and manually setting the MIME type to audio/mpeg.
        files={"audio": ("audio_test.mp3", audio_file, "audio/mpeg")},
        
        # Passing extra form data specifying the language and adapter since this older endpoint requires it unlike the Modal version.
        data={
            "language": "eng",
            "adapter": "eng"
        },
        
        # Passing the Bearer token for authentication.
        headers={"Authorization": f"Bearer {token}"},
        
        # Setting a long 180-second timeout since STT can take a while to process.
        timeout=180
    )

# Printing the final status code and response body to check the transcription output.
print(response.status_code, response.text)