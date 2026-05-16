# ============================================================
# sunbird_client.py — Written by Irwin Mwiine
# This file is the engine of the whole app. It handles all
# direct communication with the Sunbird AI API. Every time
# the app needs to transcribe, summarize, translate, or generate
# audio, it comes through here.
# ============================================================

import requests
import os
from dotenv import load_dotenv

# I'm loading the .env file using its path relative to this file's location.
# I had to do it this way because when Streamlit runs the app it starts
# from a different folder, and plain load_dotenv() couldn't find the .env file.
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))


class SunbirdClient:
    """
    This class is my wrapper around the Sunbird AI API. Instead of writing
    the same request setup over and over, I put everything in one place so
    the pipeline can just call simple methods like client.transcribe_audio()
    or client.translate_text().
    """

    def __init__(self):
        # First thing I do is grab the API token from the environment.
        # The token is stored in the .env file and never hardcoded in the
        # source code — that's a basic security practice.
        self.api_token = os.getenv("SUNBIRD_API_TOKEN")

        if not self.api_token:
            # If the token is missing, I print a clear error message so I know
            # exactly what went wrong instead of getting a confusing timeout later.
            print("ERROR: SUNBIRD_API_TOKEN not found in environment!")
        else:
            # I only print the first 10 characters for debugging — enough to
            # confirm it loaded, not enough to expose the full token.
            print(f"DEBUG: API Token loaded (starts with {self.api_token[:10]}...)")

        # Base URL for all Sunbird API endpoints. Stored here so if it ever
        # changes, I only need to update it in one place.
        self.base_url = "https://api.sunbird.ai"

        # Authorization header that goes with every request to the API.
        self.headers = {
            "Authorization": f"Bearer {self.api_token}"
        }

    def transcribe_audio(self, audio_file_path):
        """
        Takes an audio file and converts it to text using Sunbird's Modal STT
        endpoint which runs on Whisper large-v3. I chose this over the regular
        STT endpoint because Whisper auto-detects the audio language, so I don't
        have to hardcode 'eng' and risk getting garbled output if someone uploads
        audio in a different language.
        """
        print(f"DEBUG: Transcribing {audio_file_path}...")

        url = f"{self.base_url}/tasks/modal/stt"
        filename = os.path.basename(audio_file_path)

        with open(audio_file_path, "rb") as audio_file:
            response = requests.post(
                url,
                # The tuple format (filename, file_object, mime_type) tells the API
                # exactly what kind of file it's receiving. Without the mime_type,
                # the API was rejecting the file with a 422 validation error.
                files={"audio": (filename, audio_file, "audio/mpeg")},
                headers=self.headers,
                # 180 seconds because audio transcription can take a while
                # depending on the length and quality of the file.
                timeout=180
            )

        print(f"DEBUG: STT Response Status: {response.status_code}")
        response.raise_for_status()
        data = response.json()

        # The API can return the transcription under different field names depending
        # on the endpoint version, so I check all possibilities and take the first
        # one that has a value.
        transcription = (
            data.get("audio_transcription") or
            data.get("text") or
            data.get("transcription", "")
        )

        # If transcription comes back empty, I raise a clear error instead of
        # passing an empty string through the rest of the pipeline which would
        # produce confusing results downstream.
        if not transcription or transcription.strip() == "":
            raise ValueError(
                "Audio transcription returned empty. The audio may be too short or unclear."
            )

        return transcription

    def summarize_text(self, text):
        """
        Takes English text and returns a cleaned-up, readable English version of it.

        This step serves two purposes. First, if the input was audio and the
        transcription had any mumbling or unclear words, the summary corrects
        and clarifies what was meant to be said. Second, if the input text is
        long, it gets condensed before being sent to translation — which makes
        translation faster and the final output cleaner.

        I'm using the Sunflower Simple endpoint instead of the deprecated
        /tasks/summarise endpoint because the old one was timing out consistently.
        One important discovery I made: this endpoint expects form data (data=)
        not JSON (json=), which caused 422 errors until I checked the docs.

        I also explicitly tell the model to respond in English only, because
        during testing it would sometimes respond in Swahili even when given
        English input — Swahili is well-represented in its training data so
        it defaulted to it. Adding the explicit English instruction fixed that.
        """
        print("DEBUG: Summarizing text...")

        url = f"{self.base_url}/tasks/sunflower_simple"

        response = requests.post(
            url,
            # Using data= here, not json= — this sends as form data which is
            # what this specific endpoint expects according to the API docs.
            data={
                "instruction": (
                    f"You must respond in English only. Do not translate. "
                    f"If the following text is short or already clear, rewrite it clearly in English. "
                    f"If it is long, summarize it in 2 concise English sentences. "
                    f"Text: {text}"
                ),
                "model_type": "qwen",
                # Temperature of 0.3 keeps the output focused and consistent.
                # Higher values make the model more creative but less predictable.
                "temperature": 0.3
            },
            headers=self.headers,
            # 120 seconds because the model can take up to 40+ seconds
            # for longer texts — I confirmed this during my testing phase.
            timeout=180
        )

        response.raise_for_status()
        return response.json()["response"]

    def translate_text(self, text, target_language_code):
        """
        Translates English text into one of the supported local Ugandan languages.

        Supported target language codes:
        - lug (Luganda)
        - nyn (Runyankole)
        - teo (Ateso)
        - lgg (Lugbara)
        - ach (Acholi)

        One limitation I found is that Sunbird's translation model only supports
        translation to or from English. You cannot go directly from one local language
        to another — that would require pivoting through English as a middle step,
        which I decided not to implement in this version to keep the app reliable.
        """
        print(f"DEBUG: Translating to {target_language_code}...")

        url = f"{self.base_url}/tasks/translate"

        response = requests.post(
            url,
            # This endpoint uses JSON unlike sunflower_simple which uses form data.
            # I always check the docs for each endpoint because they don't all
            # follow the same format.
            json={
                "text": text,
                "source_language": "eng",
                "target_language": target_language_code
            },
            headers={**self.headers, "Content-Type": "application/json"},
            timeout=60
        )

        print(f"DEBUG: Translate Response Status: {response.status_code}")
        response.raise_for_status()
        return response.json()["output"]["translated_text"]

    def text_to_speech(self, text, speaker_id=241):
        """
        Converts text to speech and returns a signed GCP URL pointing to
        the generated audio file. The URL expires after 30 minutes so it's
        only suitable for immediate playback in the app.

        I'm using the Modal TTS endpoint after testing showed that /tasks/tts
        and /tasks/runpod/tts were either timing out or returning 500 errors.
        The Modal endpoint was the only one that worked reliably.

        Speaker ID 241 is the default I settled on after finding that speaker 248
        (which I originally tried) was causing consistent 500 server errors.
        ID 241 corresponds to an Acholi female voice according to the API docs.
        """
        print("DEBUG: Generating speech...")

        url = f"{self.base_url}/tasks/modal/tts"

        response = requests.post(
            url,
            json={
                "text": text,
                "speaker_id": speaker_id,
                # "url" mode tells the API to upload the audio to GCP storage
                # and return a signed URL rather than streaming raw audio bytes.
                "response_mode": "url"
            },
            headers={**self.headers, "Content-Type": "application/json"},
            timeout=120
        )

        print(f"DEBUG: TTS Response Status: {response.status_code}")
        response.raise_for_status()

        # The audio URL lives directly in the response root, not nested under
        # an "output" key like the translation endpoint. Each Sunbird endpoint
        # has its own response structure so I always verify the exact field names.
        return response.json()["audio_url"]