from backend.sunbird_client import (
    transcribe_audio,
    summarise_text,
    translate_text,
    text_to_speech
)


def run_pipeline(language, text=None, audio_file=None):
    """
    Runs the full pipeline:
    1. Transcribe (if audio)
    2. Summarise
    3. Translate
    4. Text to Speech
    """

    result = {
        "transcript": None,
        "summary": None,
        "translation": None,
        "audio_url": None
    }

    # Step 1 — Transcribe audio if user uploaded a file
    if audio_file is not None:
        result["transcript"] = transcribe_audio(audio_file)
        text = result["transcript"]

    # Step 2 — Summarise the text
    result["summary"] = summarise_text(text)

    # Step 3 — Translate the summary
    result["translation"] = translate_text(result["summary"], language)

    # Step 4 — Convert translation to speech
    result["audio_url"] = text_to_speech(result["translation"], language)

    return result