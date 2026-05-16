# I wrote this script to decode the JWT payload of my Sunbird API token. This helps me verify the token's expiration date and contents without needing a third-party website.

import base64, json, os
from dotenv import load_dotenv

# Loading the .env file so I can access the API token securely.
load_dotenv()

# Grabbing the API token from the environment variables.
token = os.getenv("SUNBIRD_API_TOKEN")

# The payload is the middle section of the JWT string, so I split the token by periods and grab index 1.
parts = token.split('.')
payload = parts[1]

# Base64 strings need to be padded correctly to be decoded, so I add the missing equals signs if necessary.
payload += '=' * (4 - len(payload) % 4)

# Decoding the base64 payload back into a regular Python dictionary so I can read it.
decoded = json.loads(base64.b64decode(payload))

# Pretty-printing the decoded JWT payload to the console so it's easy to read.
print(json.dumps(decoded, indent=2))