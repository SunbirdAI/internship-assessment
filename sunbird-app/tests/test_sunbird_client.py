from backend import sunbird_client

import sys
import types
import unittest
from unittest.mock import Mock, patch

dotenv_stub = types.ModuleType("dotenv")
setattr(dotenv_stub, "load_dotenv", lambda: None)
sys.modules.setdefault("dotenv", dotenv_stub)


class SunbirdClientTests(unittest.TestCase):
    @patch("backend.sunbird_client.requests.post")
    def test_transcribe_audio_uses_multipart_upload(self, mock_post: Mock) -> None:
        mock_response = Mock()
        mock_response.json.return_value = {"audio_transcription": "hello world"}
        mock_post.return_value = mock_response

        output = sunbird_client.transcribe_audio(b"audio-bytes", "lug")

        self.assertEqual(output, "hello world")
        _, kwargs = mock_post.call_args
        self.assertEqual(kwargs["url"], "https://api.sunbird.ai/tasks/modal/stt")
        self.assertEqual(kwargs["data"], {"language": "lug"})
        self.assertEqual(kwargs["files"]["audio"][0], "audio.wav")
        self.assertEqual(kwargs["files"]["audio"][1], b"audio-bytes")
        self.assertEqual(kwargs["files"]["audio"][2], "audio/wav")

    @patch("backend.sunbird_client.requests.post")
    def test_translate_text_uses_sunflower_contract(self, mock_post: Mock) -> None:
        mock_response = Mock()
        mock_response.json.return_value = {"response": "Oli otya?"}
        mock_post.return_value = mock_response

        output = sunbird_client.translate_text("How are you?", "lug", "eng")

        self.assertEqual(output, "Oli otya?")
        _, kwargs = mock_post.call_args
        self.assertEqual(kwargs["url"], "https://api.sunbird.ai/tasks/sunflower_simple")
        self.assertEqual(
            kwargs["data"],
            {"instruction": "Translate 'How are you?' from eng to lug."},
        )

    @patch("backend.sunbird_client.requests.post")
    def test_synthesize_speech_uses_tts_request_fields(self, mock_post: Mock) -> None:
        mock_response = Mock()
        mock_response.json.return_value = {"success": True, "audio_url": "https://audio.example"}
        mock_post.return_value = mock_response

        output = sunbird_client.synthesize_speech("test text")

        self.assertEqual(output, "https://audio.example")
        _, kwargs = mock_post.call_args
        self.assertEqual(kwargs["url"], "https://api.sunbird.ai/tasks/modal/tts")
        self.assertEqual(
            kwargs["json"],
            {"text": "test text", "speaker_id": 248, "response_mode": "url"},
        )


if __name__ == "__main__":
    unittest.main()
