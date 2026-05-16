# ============================================================
# sum_test.py — Written by Irwin Mwiine
# This is a standalone test script I used to verify that the
# updated summarization instruction works correctly and responds
# in English instead of defaulting to Swahili.
#
# Context: During testing I noticed the Sunflower model was
# responding in Swahili even when given English input. I added
# explicit English-only instructions to fix that, and I'm using
# this script to confirm the fix works before running the full app.
# ============================================================

import requests
import os
from dotenv import load_dotenv

# Loading the .env file using the full absolute path because this script
# lives inside backend/tests/ and a relative path wouldn't find the .env
# file which sits at the root of the sunbird-app folder.
load_dotenv(dotenv_path=r"C:\Users\CLIENT\Documents\SUNBIRD AI\internship-assessment\sunbird-app\.env")

token = os.getenv("SUNBIRD_API_TOKEN")

response = requests.post(
    "https://api.sunbird.ai/tasks/sunflower_simple",
    data={
        # This is the updated instruction I use in the main app.
        # The key additions are "You must respond in English only" and
        # "Do not translate" at the start — these stop the model from
        # defaulting to Swahili which it was doing during earlier testing.
        # The instruction also handles both short and long text so I don't
        # need separate logic for each case in the pipeline.
        "instruction": (
            "You must respond in English only. Do not translate. "
            "If the following text is short or already clear, rewrite it clearly in English. "
            "If it is long, summarize it in 2 concise English sentences. "
            "Text: Uganda is a landlocked country in East Africa known for its diverse wildlife."
        ),
        "model_type": "qwen",
        "temperature": 0.3
    },
    headers={"Authorization": f"Bearer {token}"},
    # 120 seconds because the model can take 40+ seconds on longer inputs
    # as I found out during testing with the main pipeline.
    timeout=120
)

# Printing both the status code and full response so I can see exactly
# what the model returned and confirm it's in English this time.
print(response.status_code, response.text)