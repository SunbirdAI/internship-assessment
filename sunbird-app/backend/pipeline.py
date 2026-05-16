# This file contains the SunbirdPipeline class which orchestrates the entire data flow through the Sunbird API. I built this so the Streamlit frontend only has to call one simple method instead of managing all the API steps individually.

from backend.sunbird_client import SunbirdClient
import os

class SunbirdPipeline:
    def __init__(self):
        # I initialize the SunbirdClient here so the pipeline has access to all the individual API methods like transcribe_audio and summarize_text.
        self.client = SunbirdClient()

    def run_pipeline(self, input_data, input_type, target_language):
        # This is the main method that executes the full pipeline from input to final translated audio.
        
        # I set up an empty dictionary to hold all the intermediate results so I can display them later in the UI.
        results = {
            "original_text": "",
            "summary": "",
            "translated_summary": "",
            "audio_url": ""
        }

        # Step 1: I check if the input is audio, and if so, I transcribe it using the STT endpoint. If it's already text, I just use it directly.
        if input_type == "audio":
            results["original_text"] = self.client.transcribe_audio(input_data)
        else:
            results["original_text"] = input_data

        # Step 2: I send the original text (or transcript) to the summarize endpoint to get a concise version of it.
        results["summary"] = self.client.summarize_text(results["original_text"])

        # Step 3: I take that short summary and translate it into the local Ugandan language the user selected.
        results["translated_summary"] = self.client.translate_text(
            results["summary"], 
            target_language
        )

        # Step 4: Finally, I convert the translated text into an audio file so the user can listen to it, and I store the URL.
        results["audio_url"] = self.client.text_to_speech(results["translated_summary"])

        # Returning the dictionary with all the collected data so the Streamlit app can render the results UI.
        return results
