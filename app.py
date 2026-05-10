import streamlit as st
import requests
from backend.pipeline import run_pipeline

# ── Page config ──────────────────────────────────────────────
st.set_page_config(
    page_title="Sunbird AI App",
    page_icon="🐦",
    layout="centered"
)

# ── Title ─────────────────────────────────────────────────────
st.title("🐦 Sunbird AI — Transcribe, Summarise & Translate")
st.markdown("Convert audio or text into a summarised, translated audio in your local language.")

st.divider()

# ── Input Mode ────────────────────────────────────────────────
input_mode = st.radio(
    "Choose your input type:",
    ["Text", "Audio File"],
    horizontal=True
)

text_input = None
audio_input = None

if input_mode == "Text":
    text_input = st.text_area(
        "Paste or type your text here:",
        height=200,
        placeholder="Enter your text here..."
    )

else:
    audio_input = st.file_uploader(
        "Upload an audio file (MP3, WAV, OGG, M4A — max 5 minutes):",
        type=["mp3", "wav", "ogg", "m4a", "aac"]
    )

st.divider()

# ── Language Picker ───────────────────────────────────────────
language = st.selectbox(
    "Choose target language for translation:",
    ["Luganda", "Runyankole", "Acholi", "Ateso", "Lugbara"]
)

st.divider()

# ── Run Button ────────────────────────────────────────────────
if st.button("Run Pipeline", type="primary", use_container_width=True):

    # Validate inputs
    if input_mode == "Text" and not text_input:
        st.error("Please enter some text before running.")

    elif input_mode == "Audio File" and audio_input is None:
        st.error("Please upload an audio file before running.")

    else:
        with st.spinner("Processing... please wait"):
            try:
                if input_mode == "Text":
                    result = run_pipeline(language=language, text=text_input)
                else:
                    # Check audio duration — reject anything over 5 minutes
                    if audio_input.size > 50_000_000:
                        st.error("Audio file is too large. Maximum allowed is 5 minutes.")
                        st.stop()

                    result = run_pipeline(language=language, audio_file=audio_input)

                st.success("Done!")
                st.divider()

                # ── Show Results ──────────────────────────────
                if result["transcript"]:
                    st.subheader("📝 Transcript")
                    st.write(result["transcript"])
                    st.divider()

                st.subheader("📋 Summary")
                st.write(result["summary"])
                st.divider()

                st.subheader(f"🌍 Translation ({language})")
                st.write(result["translation"])
                st.divider()

                st.subheader("🔊 Generated Audio")
                audio_response = requests.get(result["audio_url"])
                st.audio(audio_response.content, format="audio/wav")

            except Exception as e:
                st.error(f"Something went wrong: {str(e)}")