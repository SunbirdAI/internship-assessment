import os
import requests

BASE_URL = "https://api.sunbird.ai/tasks"


def _token() -> str:
    token = os.environ.get("SUNBIRD_API_TOKEN")
    if not token:
        raise EnvironmentError("SUNBIRD_API_TOKEN environment variable is not set.")
    return token


def transcribe_audio(audio_path: str) -> str:
    with open(audio_path, "rb") as f:
        resp = requests.post(
            f"{BASE_URL}/stt",
            headers={"Authorization": f"Bearer {_token()}"},
            files={"audio": f},
            timeout=360,
        )
    resp.raise_for_status()
    return resp.json()["output"]["text"]


def sunflower_simple(instruction: str) -> str:
    # API expects application/x-www-form-urlencoded (not JSON)
    # Actual response shape: {"response": "...", "success": true, ...}
    resp = requests.post(
        f"{BASE_URL}/sunflower_simple",
        headers={"Authorization": f"Bearer {_token()}"},
        data={"instruction": instruction},
        timeout=360,
    )
    resp.raise_for_status()
    return resp.json()["response"]


def synthesise_speech(text: str, speaker_id: int) -> str:
    # Actual response shape: {"success": true, "audio_url": "..."}
    resp = requests.post(
        f"{BASE_URL}/modal/tts",
        headers={
            "Authorization": f"Bearer {_token()}",
            "Content-Type": "application/json",
        },
        json={"text": text, "speaker_id": speaker_id},
        timeout=360,
    )
    resp.raise_for_status()
    return resp.json()["audio_url"]
