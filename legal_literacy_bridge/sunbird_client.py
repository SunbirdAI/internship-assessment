import os
import time
import requests
from dotenv import load_dotenv
from typing import Dict, Optional

# Load environment variables from .env file
load_dotenv()

SUPPORTED_LANGUAGES: Dict[str, str] = {
    "English": "eng",
    "Luganda": "lug",
    "Runyankole": "nyn",
    "Ateso": "teo",
    "Lugbara": "lgg",
    "Acholi": "ach",
}

class SunbirdClient:
    """
    Client for interacting with the Sunbird AI API.
    """

    def __init__(self):
        """
        Initialize the Sunbird client and verify configuration.
        
        Raises:
            EnvironmentError: If SUNBIRD_API_KEY or SUNBIRD_BASE_URL is missing.
        """
        self.api_key = os.getenv("SUNBIRD_API_KEY")
        self.base_url = os.getenv("SUNBIRD_BASE_URL", "https://api.sunbird.ai")

        if not self.api_key:
            raise EnvironmentError("SUNBIRD_API_KEY is missing from environment variables.")
        
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def transcribe_audio(self, audio_bytes: bytes, language: str = "eng") -> str:
        """
        Transcribe audio bytes to text using Sunbird STT.
        
        Args:
            audio_bytes: The raw audio file bytes.
            language: Language of the audio (default is "eng").
            
        Returns:
            The transcribed text string.
            
        Raises:
            RuntimeError: If all retries fail or an API error occurs.
        """
        url = f"{self.base_url}/tasks/stt"
        files = {"audio": ("audio.wav", audio_bytes, "audio/wav")}
        data = {"language": language}
        
        # Exponential back-off retry logic
        retries = 4
        delays = [1, 2, 4, 8]
        
        for i in range(retries):
            try:
                response = requests.post(
                    url, 
                    headers={"Authorization": f"Bearer {self.api_key}"}, # Multipart handles its own Content-Type
                    files=files, 
                    data=data
                )
                
                if response.status_code == 200:
                    data = response.json()
                    # Debug: Print the raw response to help identify the correct key
                    print(f"DEBUG STT Response: {data}")
                    # Check multiple common keys for the transcription
                    return data.get("text") or data.get("transcript") or data.get("transcription") or ""
                
                if response.status_code >= 500 or response.status_code == 429:
                    # Retry on server errors or rate limits
                    if i < retries - 1:
                        time.sleep(delays[i])
                        continue
                
                raise RuntimeError(f"STT API failed with status {response.status_code}: {response.text}")
                
            except requests.exceptions.RequestException as e:
                if i < retries - 1:
                    time.sleep(delays[i])
                    continue
                raise RuntimeError(f"STT API connection failed: {str(e)}")
        
        raise RuntimeError("STT API failed after all retries.")

    def simplify_legal_text(self, text: str) -> str:
        """
        Simplify complex legal text using Sunbird Sunflower LLM.
        
        Args:
            text: The original legal text.
            
        Returns:
            A simplified English version of the text.
            
        Raises:
            RuntimeError: If the API call fails.
        """
        if not text.strip():
            raise ValueError("Input text for simplification is empty.")

        url = f"{self.base_url}/tasks/sunflower_inference"
        payload = {
            "messages": [
                {
                    "role": "system",
                    "content": "You are a legal aid assistant. Rewrite the following legal text in plain, simple English that a person with a primary school education can understand. Use short sentences. Avoid jargon. Preserve all key facts, rights, and obligations."
                },
                {
                    "role": "user",
                    "content": text
                }
            ]
        }
        
        response = requests.post(url, headers=self.headers, json=payload)
        
        if response.status_code == 200:
            data = response.json()
            print(f"DEBUG LLM Response: {data}")
            # Robust extraction: check multiple possible keys
            return (
                data.get("summary") or 
                (data.get("choices", [{}])[0].get("message", {}).get("content")) or 
                data.get("text") or 
                data.get("content") or 
                ""
            )

        
        raise RuntimeError(f"Simplification API failed: {response.status_code} - {response.text}")

    def translate_text(self, text: str, target_language: str) -> str:
        """
        Translate simplified English text into a local Ugandan language.
        
        Args:
            text: The simplified English text.
            target_language: The target language name (e.g., 'Luganda').
            
        Returns:
            The translated text string.
            
        Raises:
            RuntimeError: If the API call fails.
        """
        if not text.strip():
            raise ValueError("Input text for translation is empty.")

        url = f"{self.base_url}/tasks/sunflower_inference"
        lang_code = SUPPORTED_LANGUAGES.get(target_language, "lug")
        payload = {
            "messages": [
                {
                    "role": "system",
                    "content": f"You are a professional translator. Translate the following simplified English text accurately into {target_language}. Preserve the meaning exactly. Do not add commentary."
                },
                {
                    "role": "user",
                    "content": text
                }
            ]
        }
        
        response = requests.post(url, headers=self.headers, json=payload)
        
        if response.status_code == 200:
            data = response.json()
            print(f"DEBUG Translation Response: {data}")
            # Robust extraction: check multiple possible keys
            return (
                data.get("translation") or 
                (data.get("choices", [{}])[0].get("message", {}).get("content")) or 
                data.get("text") or 
                data.get("content") or 
                ""
            )

        
        raise RuntimeError(f"Translation API failed: {response.status_code} - {response.text}")

    def synthesize_speech(self, text: str, language: str) -> bytes:
        """
        Convert text to speech using Sunbird TTS.
        
        Args:
            text: The text to synthesize.
            language: The language code (e.g., 'lug').
            
        Returns:
            The raw audio bytes.
            
        Raises:
            RuntimeError: If the API call fails or the audio cannot be fetched.
        """
        url = f"{self.base_url}/tasks/tts"
        payload = {
            "text": text,
            "language": language
        }
        
        response = requests.post(url, headers=self.headers, json=payload)
        
        if response.status_code == 200:
            data = response.json()
            audio_url = data.get("output", {}).get("audio_url")
            
            if not audio_url:
                raise RuntimeError(f"TTS API failed: No audio_url found in response. {data}")
            
            # Fetch the actual audio bytes from the signed URL
            audio_response = requests.get(audio_url)
            if audio_response.status_code == 200:
                return audio_response.content
            
            raise RuntimeError(f"Failed to fetch audio from URL: {audio_response.status_code}")
        
        raise RuntimeError(f"TTS API failed: {response.status_code} - {response.text}")
