from backend.errors import PipelineError, SunbirdAPIError
from backend.pipeline import run_pipeline

import io
import sys
import types
import unittest
import wave
from unittest.mock import patch

dotenv_stub = types.ModuleType("dotenv")
setattr(dotenv_stub, "load_dotenv", lambda: None)
sys.modules.setdefault("dotenv", dotenv_stub)


def make_wav_bytes(duration_seconds: int = 1) -> bytes:
    with io.BytesIO() as buffer:
        with wave.open(buffer, "wb") as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(8_000)
            wav_file.writeframes(b"\x00\x00" * 8_000 * duration_seconds)
        return buffer.getvalue()


class PipelineErrorHandlingTests(unittest.TestCase):
    @patch("backend.pipeline.transcribe_audio")
    def test_transcription_error_has_correct_stage_label(self, mock_transcribe) -> None:
        mock_transcribe.side_effect = SunbirdAPIError("network down")
        audio_bytes = make_wav_bytes()

        with self.assertRaises(PipelineError) as error:
            list(run_pipeline(target_language="Luganda", audio_input=audio_bytes))

        self.assertEqual(str(error.exception), "Transcription failed")

    @patch("backend.pipeline.summarise_text")
    @patch("backend.pipeline.translate_text")
    def test_unsupported_language_fails_before_translation(
        self, mock_translate, mock_summarise
    ) -> None:
        mock_summarise.return_value = "short summary"

        with self.assertRaises(PipelineError) as error:
            list(run_pipeline(target_language="French", text_input="hello"))

        self.assertEqual(str(error.exception), "No TTS voice configured for: French")
        mock_summarise.assert_called_once()
        mock_translate.assert_not_called()

    @patch("backend.pipeline.summarise_text")
    @patch("backend.pipeline.translate_text")
    @patch("backend.pipeline.synthesize_speech")
    def test_yields_are_snapshots_not_mutated(
        self, mock_synthesize, mock_translate, mock_summarise
    ) -> None:
        mock_summarise.return_value = "summary"
        mock_translate.return_value = "translated"
        mock_synthesize.return_value = "https://audio.example"

        updates = list(run_pipeline(target_language="Luganda", text_input="hello"))

        self.assertEqual(updates[0]["current_state"], "summarization")
        self.assertEqual(updates[0]["results"]["summary"], "summary")
        self.assertEqual(updates[0]["results"]["translation"], "")
        self.assertEqual(updates[0]["results"]["audio"], "")

        self.assertEqual(updates[1]["current_state"], "translation")
        self.assertEqual(updates[1]["results"]["translation"], "translated")
        self.assertEqual(updates[1]["results"]["audio"], "")


if __name__ == "__main__":
    unittest.main()
