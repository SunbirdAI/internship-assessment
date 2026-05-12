from sunbird_client import SunbirdClient, SUPPORTED_LANGUAGES
from utils import truncate_text
from typing import Dict, Any, Optional

class LegalBridgePipeline:
    """
    Orchestrates the legal document processing pipeline: 
    STT -> Simplification -> Translation -> TTS.
    """

    def __init__(self):
        """
        Initialize the pipeline with a SunbirdClient.
        """
        self.client = SunbirdClient()

    def run_from_text(self, legal_text: str, target_language: str) -> Dict[str, Any]:
        """
        Process legal text through simplification, translation, and speech synthesis.
        
        Args:
            legal_text: The input legal text.
            target_language: The display name of the target language.
            
        Returns:
            A dictionary containing intermediate results and audio bytes.
            
        Raises:
            RuntimeError: If any phase of the pipeline fails.
        """
        lang_code = SUPPORTED_LANGUAGES.get(target_language, "lug")
        truncated_input = truncate_text(legal_text)

        # Phase 2: Simplification
        try:
            simplified = self.client.simplify_legal_text(truncated_input)
        except Exception as e:
            raise RuntimeError(f"Phase 2 failed: {str(e)}")

        # Phase 3: Translation
        try:
            translated = self.client.translate_text(simplified, target_language)
        except Exception as e:
            raise RuntimeError(f"Phase 3 failed: {str(e)}")

        # Phase 4: Speech Synthesis
        try:
            audio_bytes = self.client.synthesize_speech(translated, lang_code)
        except Exception as e:
            raise RuntimeError(f"Phase 4 failed: {str(e)}")

        return {
            "transcript": None,
            "simplified": simplified,
            "translated": translated,
            "audio_bytes": audio_bytes,
            "target_language": target_language,
        }

    def run_from_audio(self, audio_bytes: bytes, audio_format: str, target_language: str, source_lang: str = "English", progress_callback=None) -> dict:
        """
        Process audio input through transcription, simplification, translation, and speech synthesis.
        """
        from .utils import split_audio_into_chunks
        
        # 1. Chunk audio (10 min chunks)
        chunks = split_audio_into_chunks(audio_bytes)
        full_transcript = []
        
        # Map source language to code
        from .sunbird_client import SUPPORTED_LANGUAGES
        stt_lang_code = SUPPORTED_LANGUAGES.get(source_lang, "eng")
        
        # Phase 1: Transcription (Iterative)
        for idx, chunk in enumerate(chunks):
            if progress_callback:
                progress_callback(idx + 1, len(chunks), f"Transcribing part {idx+1}/{len(chunks)}...")
            
            try:
                transcript = self.client.transcribe_audio(chunk, language=stt_lang_code)
                if transcript and transcript.strip():
                    full_transcript.append(transcript)
            except Exception as e:
                raise RuntimeError(f"Phase 1 failed at chunk {idx+1}: {str(e)}")
        
        combined_transcript = " ".join(full_transcript)
        
        if not combined_transcript.strip():
            combined_transcript = "[No clear speech detected in recording]"
            
        # Continue with text pipeline using combined transcript
        results = self.run_from_text(combined_transcript, target_language)
        results["transcript"] = combined_transcript
        
        return results
