from mutagen import File as MutaFile

from .sunbird_client import transcribe_audio, sunflower_simple, synthesise_speech

MAX_AUDIO_SECONDS = 300  # 5 minutes

LANGUAGES: dict[str, int] = {
    "Luganda": 248,
    "Runyankole": 243,
    "Ateso": 242,
    "Lugbara": 245,
    "Acholi": 241,
}


def _check_audio_duration(path: str) -> None:
    audio = MutaFile(path)
    if audio is None:
        return
    duration = audio.info.length
    if duration > MAX_AUDIO_SECONDS:
        mins = int(duration // 60)
        secs = int(duration % 60)
        raise ValueError(
            f"Audio is {mins}m {secs}s — maximum allowed is 5 minutes. "
            "Please trim the file and try again."
        )


def run_pipeline(
    text: str | None,
    audio_path: str | None,
    target_language: str,
) -> dict:
    if target_language not in LANGUAGES:
        raise ValueError(f"Unsupported language: {target_language!r}")

    transcript: str | None = None

    if audio_path:
        _check_audio_duration(audio_path)
        transcript = transcribe_audio(audio_path)
        source_text = transcript
    else:
        source_text = text

    summary = sunflower_simple(
        f"Summarise the following text concisely in 3-5 sentences:\n\n{source_text}"
    )

    translation = sunflower_simple(
        f"Translate the following text into {target_language}. "
        f"Output only the translation with no extra commentary:\n\n{summary}"
    )

    speaker_id = LANGUAGES[target_language]
    audio_url = synthesise_speech(translation, speaker_id)

    return {
        "transcript": transcript,
        "summary": summary,
        "translation": translation,
        "audio_url": audio_url,
    }
