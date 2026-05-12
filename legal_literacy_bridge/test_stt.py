import os
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("SUNBIRD_API_KEY")
base_url = "https://api.sunbird.ai"

url = f"{base_url}/tasks/stt"
headers = {"Authorization": f"Bearer {api_key}"}

# Use the file the user uploaded
file_path = "Molly K...a case.m4a"

if not os.path.exists(file_path):
    print(f"File {file_path} not found.")
else:
    with open(file_path, "rb") as f:
        files = {"audio": ("audio.m4a", f, "audio/mp4")}
        data = {"language": "eng"}
        response = requests.post(url, headers=headers, files=files, data=data)
        
    print(f"Status Code: {response.status_code}")
    print(f"Response Body: {response.text}")
