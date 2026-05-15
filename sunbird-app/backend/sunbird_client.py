import os

import requests
from dotenv import load_dotenv

from backend.errors import SunbirdAPIError

load_dotenv()
TOKEN = os.getenv("SUNBIRD_API_TOKEN")
HEADERS = {"Authorization": f"Bearer {TOKEN}"}
BASE_URL = "https://api.sunbird.ai"
REQUEST_TIMEOUT_SECONDS = 600


def transcribe_audio(audio_bytes: bytes, language: str = "eng") -> str:
    """Send audio, get back transcript text."""
    files = {"audio": ("audio.wav", audio_bytes, "audio/wav")}
    payload = {"language": language} if language else {}
    try:
        response = requests.post(
            url=f"{BASE_URL}/tasks/modal/stt",
            data=payload,
            files=files,
            headers=HEADERS,
            timeout=REQUEST_TIMEOUT_SECONDS,
        )
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise SunbirdAPIError("STT request failed") from e

    transcription = response.json().get("audio_transcription")
    if not transcription:
        raise SunbirdAPIError("STT response did not include audio_transcription.")
    return transcription


def summarise_text(text: str) -> str:
    """Send text to Sunflower and get summary output back."""
    try:
        response = requests.post(
            url=f"{BASE_URL}/tasks/sunflower_simple",
            headers=HEADERS,
            data={"instruction": f"Summarize this text:\n\n{text}"},
            timeout=REQUEST_TIMEOUT_SECONDS,
        )
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise SunbirdAPIError("Summarization request failed") from e

    summary = response.json().get("response")
    if not summary:
        raise SunbirdAPIError("Sunflower response did not include response text.")
    return summary


def translate_text(
    text: str, target_language: str, source_language: str = "eng"
) -> str:
    """Translate text using Sunflower from English to target local language."""
    try:
        response = requests.post(
            url=f"{BASE_URL}/tasks/sunflower_simple",
            headers=HEADERS,
            data={"instruction": f"Translate '{text}' from {source_language} to {target_language}."},
            timeout=REQUEST_TIMEOUT_SECONDS,
        )
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise SunbirdAPIError("Translation request failed") from e

    translation = response.json().get("response")
    if not translation:
        raise SunbirdAPIError("Sunflower response did not include translated text.")
    return translation


def synthesize_speech(text: str, speaker_id: int = 248, response_mode: str = "url") -> str:
    """Send text and get back a signed audio URL."""
    payload = {
        "text": text,
        "speaker_id": speaker_id,
        "response_mode": response_mode,
    }
    try:
        response = requests.post(
            url=f"{BASE_URL}/tasks/modal/tts",
            json=payload,
            headers=HEADERS,
            timeout=REQUEST_TIMEOUT_SECONDS,
        )
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise SunbirdAPIError("TTS request failed") from e

    audio_url = response.json().get("audio_url")
    if not audio_url:
        raise SunbirdAPIError("TTS response did not include audio_url.")
    return audio_url
