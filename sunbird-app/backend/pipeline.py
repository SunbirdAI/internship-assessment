from backend.sunbird_client import (
    transcribe_audio,
    translate_text,
    summarise_text,
    synthesize_speech,
)

import io
import wave

# import time
from typing import TypedDict, Literal, Generator  # ,Dict

from backend.errors import PipelineError, SunbirdAPIError

# because summarization can only be in English and Luganda(of which translation supports only English to local language and vice versa) I have to make the Input-transcribe/text-summarize part of the pipeline only use English. Translation and STT will use the langs common to both of them.
# won't include english because requirements state that the translation and TTS should be in a local language

VOICE_IDS = {
    "Acholi": 241,
    "Ateso": 242,
    "Runyankole": 243,
    "Lugbara": 245,
    "Swahili": 246,
    "Luganda": 248,
}

PipelineState = Literal[
    "transcription", "summarization", "translation", "audio_clip", "complete"
]


class PipelineResult(TypedDict):
    transcript: str
    summary: str
    translation: str
    truncated: bool
    audio: str
    # timing: Dict[str, float]


class PipelineYield(TypedDict):
    current_state: PipelineState
    results: PipelineResult


# generator function -> in order to store state for each step and output to UI once ready
def run_pipeline(
    target_language: str = "", text_input: str = "", audio_input: bytes = b""
) -> Generator[PipelineYield, None, None]:

    def check_audio_duration(audio_bytes: bytes) -> float:
        """Returns duration in seconds"""
        # open uploaded bytes as WAV stream to calculate duration directly
        # since I am using WAV only for this project... it's not flexible however to other formats

        try:
            with wave.open(io.BytesIO(audio_bytes), "rb") as wav_file:
                frame_count = wav_file.getnframes()
                frame_rate = wav_file.getframerate()

                # prevent division by zero if header is corrupted
                if frame_rate == 0:
                    # since it has no chance of successfully transcribing it and to avoid a later if statement
                    raise PipelineError("WAV header is corrupted.")

                return frame_count / float(frame_rate)

        except wave.Error as e:
            raise PipelineError("WAV data is corrupted.") from e

    # transport contract between pipeline and Streamlit
    results: PipelineResult = {
        "transcript": "",
        "summary": "",
        "translation": "",
        "truncated": False,
        "audio": "",
        # "timing": {
        #     "transcription": 0.0,
        #     "summarization": 0.0,
        #     "translation": 0.0,
        #     "audio_clip": 0.0,
        #     "total": 0.0
        # }
    }

    # find out the total timing
    # start = time.perf_counter()

    if audio_input != b"":
        # ensure audio length < 5 mins(300s)
        duration = check_audio_duration(audio_bytes=audio_input)

        if duration > 300:
            raise PipelineError(
                "Audio file exceeds 5 minutes. Please upload a shorter file."
            )

        try:
            # find out timing for each step
            # step_start = time.perf_counter()
            results["transcript"] = transcribe_audio(audio_bytes=audio_input)
            text = results["transcript"]
            # results["timing"]["transcription"] = time.perf_counter() - step_start
            yield {"current_state": "transcription", "results": results.copy()}

        except SunbirdAPIError as e:
            raise PipelineError("Transcription failed") from e

    else:
        text = text_input

    try:
        # step_start = time.perf_counter()
        results["summary"] = summarise_text(text=text)
        # results["timing"]["summarization"] = time.perf_counter() - step_start
        yield {"current_state": "summarization", "results": results.copy()}
    except SunbirdAPIError as e:
        raise PipelineError("Summarization failed") from e

    voice_id = VOICE_IDS.get(target_language)
    if not voice_id:
        raise PipelineError(f"No TTS voice configured for: {target_language}")

    try:
        # step_start = time.perf_counter()
        results["translation"] = translate_text(
            text=results["summary"], target_language=target_language
        )
        # results["timing"]["translation"] = time.perf_counter() - step_start
        yield {"current_state": "translation", "results": results.copy()}

    except SunbirdAPIError as e:
        raise PipelineError("Translation failed") from e

    # TTS can only accept string of length 1-10000
    if len(results["translation"]) > 10000:
        results["translation"] = (results["translation"])[:10000]
        results["truncated"] = True
    else:
        results["truncated"] = False

    try:
        # step_start = time.perf_counter()
        results["audio"] = synthesize_speech(
            text=results["translation"], speaker_id=voice_id
        )
        # results["timing"]["audio_clip"] = time.perf_counter() - step_start
        yield {"current_state": "audio_clip", "results": results.copy()}
    except SunbirdAPIError as e:
        raise PipelineError("Speech synthesis failed") from e

    # results["timing"]["total"] = time.perf_counter() - start
    yield {"current_state": "complete", "results": results.copy()}
