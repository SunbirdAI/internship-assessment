import os
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("SUNBIRD_API_KEY")
base_url = "https://api.sunbird.ai"

url = f"{base_url}/tasks/sunflower_inference"
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

payload = {
    "messages": [
        {"role": "system", "content": "Simplify this text."},
        {"role": "user", "content": "The doctrine of Res Sub Judice originates from the Latin maxim..."}
    ]
}

response = requests.post(url, headers=headers, json=payload)

print(f"Status Code: {response.status_code}")
print(f"Response Body: {response.text}")
