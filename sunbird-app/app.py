
# This is the main entry point for the Sunbird AI Assistant.
# It handles everything the user sees and interacts with, and it calls the backend pipeline to do the actual AI work.

import streamlit as st
from backend.pipeline import SunbirdPipeline
import os
import tempfile

# Setting up the browser tab — title, icon, and centered layout.
st.set_page_config(
    page_title="Sunbird AI Assistant",
    page_icon="🐦",
    layout="centered"
)


# STYLING
# Streamlit doesn't give much design control out of the box, so I wrote custom CSS to get the dark theme and orange accents looking the way I wanted. I used CSS variables so all the colors are defined in one place and easy to change.

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

    :root {
        --orange: #FF6B00;
        --orange-glow: rgba(255, 107, 0, 0.15);
        --bg: #0A0A0A;
        --surface: #141414;
        --surface-2: #1E1E1E;
        --border: #2A2A2A;
        --text: #F0F0F0;
        --text-muted: #888888;
        --radius: 12px;
    }

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif !important;
        background-color: var(--bg) !important;
        color: var(--text) !important;
    }

    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 4rem !important;
        max-width: 720px !important;
    }

    /* Hiding Streamlit's default top menu, footer, and header so the app feels standalone. */
    #MainMenu, footer, header { visibility: hidden; }

    .hero {
        text-align: center;
        padding: 3rem 0 2.5rem;
        position: relative;
    }

    /* This creates the soft orange glow behind the hero title. */
    .hero::before {
        content: '';
        position: absolute;
        top: 0; left: 50%;
        transform: translateX(-50%);
        width: 300px; height: 200px;
        background: radial-gradient(ellipse at center, rgba(255,107,0,0.12) 0%, transparent 70%);
        pointer-events: none;
    }

    .hero-eyebrow {
        font-size: 0.7rem;
        font-weight: 500;
        letter-spacing: 0.25em;
        text-transform: uppercase;
        color: var(--orange);
        margin-bottom: 1rem;
    }

    /* I used Syne for the big title because it has a bold geometric feel that matches the brand. */
    .hero-title {
        font-family: 'Syne', sans-serif !important;
        font-size: 3.2rem !important;
        font-weight: 800 !important;
        letter-spacing: -0.03em;
        color: var(--text) !important;
        line-height: 1.1;
        margin-bottom: 1rem;
    }
    .hero-title span { color: var(--orange); }

    .hero-sub {
        font-size: 1rem;
        color: var(--text-muted);
        font-weight: 300;
        max-width: 420px;
        margin: 0 auto;
        line-height: 1.6;
    }

    /* A thin gradient line used to visually separate sections. */
    .section-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, var(--border), transparent);
        margin: 2rem 0;
    }

    /* Orange uppercase step labels like "01 — INPUT". */
    .panel-label {
        font-size: 0.7rem;
        font-weight: 600;
        letter-spacing: 0.15em;
        text-transform: uppercase;
        color: var(--orange);
        margin-bottom: 0.75rem;
    }

    .stRadio > div {
        background: var(--surface) !important;
        border: 1px solid var(--border) !important;
        border-radius: var(--radius) !important;
        padding: 1.25rem 1.5rem !important;
        gap: 1rem !important;
    }
    .stRadio label { color: var(--text) !important; font-size: 0.95rem !important; }

    div[data-baseweb="select"] > div {
        background: var(--surface) !important;
        border: 1px solid var(--border) !important;
        border-radius: var(--radius) !important;
        color: var(--text) !important;
    }
    div[data-baseweb="select"] > div:focus-within {
        border-color: var(--orange) !important;
        box-shadow: 0 0 0 2px var(--orange-glow) !important;
    }
    [data-baseweb="popover"] {
        background: var(--surface-2) !important;
        border: 1px solid var(--border) !important;
        border-radius: var(--radius) !important;
    }
    [role="option"] { background: var(--surface-2) !important; color: var(--text) !important; }
    [role="option"]:hover { background: var(--orange-glow) !important; }

    .stTextArea > div > div > textarea {
        background: var(--surface) !important;
        border: 1px solid var(--border) !important;
        border-radius: var(--radius) !important;
        color: var(--text) !important;
        font-family: 'DM Sans', sans-serif !important;
        font-size: 0.95rem !important;
        padding: 1rem !important;
        min-height: 120px !important;
        resize: vertical !important;
    }
    .stTextArea > div > div > textarea:focus {
        border-color: var(--orange) !important;
        box-shadow: 0 0 0 2px var(--orange-glow) !important;
    }
    .stTextArea > div > div > textarea::placeholder { color: var(--text-muted) !important; }

    section[data-testid="stFileUploadDropzone"] {
        background: var(--surface) !important;
        border: 2px dashed var(--border) !important;
        border-radius: var(--radius) !important;
        padding: 2rem !important;
    }
    section[data-testid="stFileUploadDropzone"]:hover {
        border-color: var(--orange) !important;
        background: var(--orange-glow) !important;
    }
    section[data-testid="stFileUploadDropzone"] * { color: var(--text-muted) !important; }

    .stButton > button {
        width: 100% !important;
        background: var(--orange) !important;
        color: #000000 !important;
        font-family: 'Syne', sans-serif !important;
        font-weight: 700 !important;
        font-size: 0.9rem !important;
        letter-spacing: 0.08em !important;
        text-transform: uppercase !important;
        border: none !important;
        border-radius: var(--radius) !important;
        height: 3.25rem !important;
        margin-top: 1.25rem !important;
        transition: all 0.2s ease !important;
        cursor: pointer !important;
    }
    .stButton > button:hover {
        background: #FF8C00 !important;
        box-shadow: 0 0 24px rgba(255, 107, 0, 0.4) !important;
        transform: translateY(-1px) !important;
    }
    .stButton > button:active { transform: translateY(0) !important; }

    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, var(--orange), #FF8C00) !important;
        border-radius: 4px !important;
    }
    .stProgress > div > div {
        background: var(--surface-2) !important;
        border-radius: 4px !important;
    }

    /* Each result is shown in a dark card with an orange left border to make them visually distinct. */
    .result-card {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: var(--radius);
        padding: 1.5rem;
        margin: 1rem 0;
        position: relative;
        overflow: hidden;
    }
    .result-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0;
        width: 3px; height: 100%;
        background: var(--orange);
    }
    .result-card-label {
        font-size: 0.65rem;
        font-weight: 600;
        letter-spacing: 0.2em;
        text-transform: uppercase;
        color: var(--orange);
        margin-bottom: 0.75rem;
        padding-left: 0.75rem;
    }
    .result-card-content {
        font-size: 0.95rem;
        color: var(--text);
        line-height: 1.7;
        padding-left: 0.75rem;
    }

    .stAlert {
        background: var(--surface) !important;
        border: 1px solid var(--border) !important;
        border-radius: var(--radius) !important;
        color: var(--text) !important;
    }

    /* The animated dot pulses orange during processing to show the user something is happening. */
    .step-indicator {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-size: 0.8rem;
        color: var(--text-muted);
        margin-bottom: 0.5rem;
        font-weight: 500;
    }
    .step-dot {
        width: 6px; height: 6px;
        background: var(--orange);
        border-radius: 50%;
        animation: pulse 1s infinite;
    }
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.3; }
    }

    .app-footer {
        text-align: center;
        font-size: 1.2rem;
        margin-top: 3rem;
        padding-top: 1.5rem;
        border-top: 1px solid var(--border);
    }

    label[data-testid="stWidgetLabel"] p,
    .stRadio label, div[class*="label"] {
        color: var(--text-muted) !important;
        font-size: 0.8rem !important;
        font-weight: 500 !important;
        letter-spacing: 0.05em !important;
        text-transform: uppercase !important;
    }

    audio {
        width: 100% !important;
        border-radius: 8px !important;
        margin-top: 0.5rem;
    }

    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: var(--bg); }
    ::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
    ::-webkit-scrollbar-thumb:hover { background: var(--orange); }
    </style>
""", unsafe_allow_html=True)


# HERO SECTION
# I used raw HTML here because Streamlit's built-in st.title() doesn't give enough control over fonts, sizing, or the glow effect.

st.markdown("""
    <div class='hero'>
        <div class='hero-eyebrow'>🐦 Powered by Sunbird AI</div>
        <div class='hero-title'>Speak <span>Local.</span></div>
        <div class='hero-sub'>
            Transcribe, summarize, and translate English into Ugandan languages — instantly.
        </div>
    </div>
    <div class='section-divider'></div>
""", unsafe_allow_html=True)


# PIPELINE INITIALIZATION
# This sets up the SunbirdClient which handles all API calls.
# It runs on every page reload which is fine for development, but in production I would wrap this with @st.cache_resource to avoid re-initializing on every user interaction.

pipeline = SunbirdPipeline()
client = pipeline.client


# INPUT TYPE SELECTION
# The user chooses between typing text or uploading an audio file. I used a radio button because it's a mutually exclusive choice.

st.markdown("<div class='panel-label'>01 — Input</div>", unsafe_allow_html=True)
input_type = st.radio(
    "Choose Input Type:",
    ("Text Input", "Audio Upload"),
    label_visibility="collapsed"
)


# TARGET LANGUAGE SELECTION
# The user picks which Ugandan language they want the output in.
# I store the display name and code together like "Luganda (lug)" so I can extract the code easily by splitting on the bracket.

st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
st.markdown("<div class='panel-label'>02 — Translate To</div>", unsafe_allow_html=True)
target_lang = st.selectbox(
    "Select Target Language:",
    ("Luganda (lug)", "Runyankole (nyn)", "Ateso (teo)", "Lugbara (lgg)", "Acholi (ach)"),
    label_visibility="collapsed"
)

# Extracting just the language code from the selection string, e.g. "Luganda (lug)" becomes "lug".
lang_code = target_lang.split("(")[1].strip(")")

st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)


# TEXT OR AUDIO INPUT
# Depending on what the user chose, I show either a text area or a file uploader. I also validate the audio file duration here before allowing the pipeline to run.

input_data = None
ready_to_process = False

if input_type == "Text Input":
    st.markdown("<div class='panel-label'>03 — Your Text</div>", unsafe_allow_html=True)
    input_data = st.text_area(
        "Enter text:",
        placeholder="Type or paste your English text here...",
        label_visibility="collapsed"
    )
    if input_data:
        ready_to_process = True

else:
    st.markdown("<div class='panel-label'>03 — Your Audio</div>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        "Upload audio:",
        type=['mp3', 'wav', 'm4a'],
        label_visibility="collapsed"
    )

    if uploaded_file:
        # The assessment requires rejecting audio files longer than 5 minutes.
        # I can't check the actual duration without loading the file into a library  like librosa or pydub, so I estimate it using file size instead.
        # At 128kbps (standard MP3 quality), 5 minutes ≈ 4.8MB, so I use that as the limit.
        MAX_FILE_SIZE_BYTES = 5 * 60 * 128 * 1000 // 8

        if uploaded_file.size > MAX_FILE_SIZE_BYTES:
            st.error("Your audio file is too long. Please upload a file under 5 minutes.")
            ready_to_process = False
        else:
            # Streamlit gives me the file as bytes in memory, but the Sunbird API needs an actual file on disk. I save it to a temporary file here and clean it up in the finally block after processing is done.
            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=os.path.splitext(uploaded_file.name)[1]
            ) as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                input_data = tmp_file.name
            ready_to_process = True


# PROCESS BUTTON AND PIPELINE EXECUTION
# When the user clicks this, the full 4-step pipeline runs.
# I show a progress bar and animated step indicator so the user knows what's happening since each step can take 30-120 seconds.

if st.button("Process with Sunbird AI"):

    if not ready_to_process:
        st.error("Please provide either text or an audio file before processing.")
    else:
        progress_bar = st.progress(0)

        # I use st.empty() for the status text so I can update it in place without adding a new line to the page on every step update.
        status_text = st.empty()

        try:
            type_key = "audio" if input_type == "Audio Upload" else "text"

            # STEP 1 — Handle input.
            # If the user uploaded audio, transcribe it to text first.
            # If they typed text, use it directly and skip transcription.
            progress_bar.progress(10)
            if type_key == "audio":
                status_text.markdown("<div class='step-indicator'><div class='step-dot'></div>Step 1 of 4 — Transcribing audio...</div>", unsafe_allow_html=True)
                original_text = client.transcribe_audio(input_data)
            else:
                status_text.markdown("<div class='step-indicator'><div class='step-dot'></div>Step 1 of 4 — Reading input...</div>", unsafe_allow_html=True)
                original_text = input_data

            # STEP 2 — Summarize the text.
            # I summarize before translating because it's more efficient to translate a short summary than a long block of text, and the output is cleaner for the user.
            status_text.markdown("<div class='step-indicator'><div class='step-dot'></div>Step 2 of 4 — Summarizing...</div>", unsafe_allow_html=True)
            progress_bar.progress(35)
            summary = client.summarize_text(original_text)

            # STEP 3 — Translate the summary into the chosen local language.
            status_text.markdown(f"<div class='step-indicator'><div class='step-dot'></div>Step 3 of 4 — Translating to {target_lang.split(' ')[0]}...</div>", unsafe_allow_html=True)
            progress_bar.progress(65)
            translated_summary = client.translate_text(summary, lang_code)

            # STEP 4 — Convert the translated text to speech.
            # This gives the user an audio clip they can play back in the local language.
            status_text.markdown("<div class='step-indicator'><div class='step-dot'></div>Step 4 of 4 — Generating audio...</div>", unsafe_allow_html=True)
            progress_bar.progress(85)
            audio_url = client.text_to_speech(translated_summary)

            progress_bar.progress(100)
            status_text.empty()

            # DISPLAY RESULTS
            # I show three cards — the original text, the English summary,and the translated summary — plus an audio player at the bottom.
            st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
            st.markdown("<div class='panel-label'>Results</div>", unsafe_allow_html=True)

            st.markdown(f"""
                <div class='result-card'>
                    <div class='result-card-label'>📝 Original Text / Transcript</div>
                    <div class='result-card-content'>{original_text}</div>
                </div>
            """, unsafe_allow_html=True)

            st.markdown(f"""
                <div class='result-card'>
                    <div class='result-card-label'>💡 Summary (English)</div>
                    <div class='result-card-content'>{summary}</div>
                </div>
            """, unsafe_allow_html=True)

            st.markdown(f"""
                <div class='result-card'>
                    <div class='result-card-label'>🌍 Translation — {target_lang.split(' ')[0]}</div>
                    <div class='result-card-content'>{translated_summary}</div>
                </div>
            """, unsafe_allow_html=True)

            st.markdown("<div class='panel-label' style='margin-top:1.5rem'>🔊 Generated Audio</div>", unsafe_allow_html=True)
            st.audio(audio_url)

        except Exception as e:
            # I catch all exceptions and show a clean error message instead of letting Streamlit display a raw Python traceback to the user.
            st.error(f"Something went wrong: {str(e)}")

        finally:
            # This block runs whether the pipeline succeeded or failed.
            # I clean up the temporary audio file here so files don't accumulate on disk after every upload session.
            if input_type == "Audio Upload" and input_data and os.path.exists(input_data):
                os.remove(input_data)

            # Small delay before clearing the progress bar so it doesn't vanish too abruptly.
            import time
            time.sleep(1)
            progress_bar.empty()
            status_text.empty()

# ============================================================
# FOOTER — just the Sunbird bird emoji, clean and minimal.
# ============================================================
st.markdown("<div class='app-footer'>🐦</div>", unsafe_allow_html=True)