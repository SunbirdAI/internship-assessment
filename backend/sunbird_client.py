import requests
import os
from dotenv import load_dotenv

load_dotenv()

SUNBIRD_API_TOKEN = os.getenv("SUNBIRD_API_TOKEN")

BASE_URL = "https://api.sunbird.ai"

HEADERS = {
    "Authorization": f"Bearer {SUNBIRD_API_TOKEN}",
    "Content-Type": "application/json"
}

LANGUAGE_SPEAKER_IDS = {
    "Luganda": 248,
    "Acholi": 241,
    "Ateso": 242,
    "Runyankole": 243,
    "Lugbara": 245
}


def transcribe_audio(audio_file):
    """Send audio file to Sunbird STT and return transcribed text."""
    url = f"{BASE_URL}/tasks/stt"
    headers = {"Authorization": f"Bearer {SUNBIRD_API_TOKEN}"}
    files = {
        "audio": (
            audio_file.name,
            audio_file.read(),
            audio_file.type
        )
    }
    response = requests.post(url, files=files, headers=headers)
    response.raise_for_status()
    return response.json()["audio_transcription"]  # ← fixed key


def summarise_text(text):
    """Send text to Sunflower and return a summary."""
    url = f"{BASE_URL}/tasks/sunflower_simple"
    headers = {"Authorization": f"Bearer {SUNBIRD_API_TOKEN}"}
    payload = {
        "instruction": f"""You are a text summariser. Your job is to summarise the text below.
Do not introduce yourself. Do not say anything else.
Just return a summary of the text in 3 clear sentences.

Text to summarise:
{text}

Summary:""",
        "model_type": "qwen",
        "temperature": 0.3
    }
    response = requests.post(url, data=payload, headers=headers)
    response.raise_for_status()
    return response.json()["response"]


def translate_text(text, language):
    """Translate text into the chosen Ugandan language."""
    url = f"{BASE_URL}/tasks/sunflower_simple"
    headers = {"Authorization": f"Bearer {SUNBIRD_API_TOKEN}"}
    payload = {
        "instruction": f"""You are a translator. Translate the text below to {language}.
Do not introduce yourself. Do not explain anything.
Just return the translated text and nothing else.

Text to translate:
{text}

Translation:""",
        "model_type": "qwen",
        "temperature": 0.3
    }
    response = requests.post(url, data=payload, headers=headers)
    response.raise_for_status()
    return response.json()["response"]


def text_to_speech(text, language):
    """Convert translated text to audio and return the audio URL."""
    url = f"{BASE_URL}/tasks/tts"
    speaker_id = LANGUAGE_SPEAKER_IDS[language]
    payload = {
        "text": text,
        "speaker_id": speaker_id
    }
    response = requests.post(url, json=payload, headers=HEADERS)
    print("TTS STATUS:", response.status_code)
    print("TTS RESPONSE:", response.text)
    response.raise_for_status()
    return response.json()["output"]["audio_url"]