import os
import tempfile

import gradio as gr
import requests
from dotenv import load_dotenv

from backend.pipeline import run_pipeline, LANGUAGES

load_dotenv()


def _download_audio(url: str) -> str:
    resp = requests.get(url, timeout=60)
    resp.raise_for_status()
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        f.write(resp.content)
        return f.name


def handle_text(text: str, language: str):
    if not text or not text.strip():
        raise gr.Error("Please enter some text before processing.")
    try:
        result = run_pipeline(text=text.strip(), audio_path=None, target_language=language)
        audio_path = _download_audio(result["audio_url"])
        return (
            gr.update(value="", visible=False),
            result["summary"],
            result["translation"],
            audio_path,
        )
    except gr.Error:
        raise
    except Exception as e:
        raise gr.Error(str(e))


def handle_audio(audio_path: str | None, language: str):
    if audio_path is None:
        raise gr.Error("Please upload an audio file before processing.")
    try:
        result = run_pipeline(text=None, audio_path=audio_path, target_language=language)
        tts_path = _download_audio(result["audio_url"])
        return (
            gr.update(value=result["transcript"], visible=True),
            result["summary"],
            result["translation"],
            tts_path,
        )
    except gr.Error:
        raise
    except Exception as e:
        raise gr.Error(str(e))


with gr.Blocks(title="Sunbird AI Pipeline") as demo:
    gr.Markdown(
        """
        # Sunbird AI — Summarise & Translate
        Provide text or an audio file. The app will summarise it, translate the summary
        into a Ugandan local language, and play back the translation as speech.
        """
    )

    with gr.Row():
        language = gr.Dropdown(
            choices=list(LANGUAGES.keys()),
            value="Luganda",
            label="Target language",
            scale=1,
        )

    with gr.Tabs():
        with gr.Tab("Text input"):
            text_input = gr.Textbox(
                label="Text",
                lines=8,
                placeholder="Paste or type your text here…",
            )
            text_btn = gr.Button("Summarise & Translate", variant="primary")

        with gr.Tab("Audio upload"):
            gr.Markdown("Upload an MP3, WAV, OGG, M4A, or AAC file. Maximum duration: **5 minutes**.")
            audio_input = gr.Audio(
                label="Audio file",
                type="filepath",
                sources=["upload"],
            )
            audio_btn = gr.Button("Transcribe, Summarise & Translate", variant="primary")

    gr.Markdown("---")
    gr.Markdown(
        "## Output\n"
        "> **Note:** Each pipeline run calls the Sunbird LLM twice (summarise + translate) "
        "and the TTS service once. Allow **3–6 minutes** for results — the button will spin while processing."
    )

    transcript_out = gr.Textbox(
        label="Transcript",
        interactive=False,
        visible=False,
        lines=4,
    )
    summary_out = gr.Textbox(label="Summary", interactive=False, lines=4)
    translation_out = gr.Textbox(label="Translated summary", interactive=False, lines=4)
    audio_out = gr.Audio(label="Synthesised speech", type="filepath")

    text_btn.click(
        handle_text,
        inputs=[text_input, language],
        outputs=[transcript_out, summary_out, translation_out, audio_out],
    )
    audio_btn.click(
        handle_audio,
        inputs=[audio_input, language],
        outputs=[transcript_out, summary_out, translation_out, audio_out],
    )

if __name__ == "__main__":
    demo.launch(theme=gr.themes.Soft())
