import streamlit as st
import os
import sys
from pipeline import LegalBridgePipeline
from utils import validate_audio_file, format_error
from sunbird_client import SUPPORTED_LANGUAGES

# Ensure local directory is in PATH for FFmpeg detection if binaries were downloaded locally
sys.path.append(os.getcwd())
if os.path.exists("ffmpeg.exe"):
    os.environ["PATH"] += os.pathsep + os.getcwd()

# 1. Page Configuration
st.set_page_config(
    page_title="Legal Literacy Bridge",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Modern Professional Facelift (CSS) - PRESERVING ALL ORIGINAL TEXT SLOTS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    /* Global Body */
    [data-testid="stAppViewContainer"] {
        background-color: #0F111A; /* Deep Professional Charcoal */
        color: #E2E8F0;
        font-family: 'Inter', sans-serif;
    }
    
    [data-testid="stHeader"] {
        background: rgba(15, 17, 26, 0.8);
        backdrop-filter: blur(12px);
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #161B22;
        border-right: 1px solid #30363D;
    }
    
    .sidebar-card {
        background: #0D1117;
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 20px;
        border: 1px solid #30363D;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    }
    
    .sidebar-tagline {
        color: #8B949E;
        font-size: 13px;
        line-height: 1.5;
        margin-top: 10px;
    }

    /* Main Area Headers */
    .header-container {
        text-align: center;
        margin-bottom: 3rem;
    }
    
    h1 {
        color: #FFFFFF !important;
        font-weight: 700 !important;
        letter-spacing: -0.02em;
    }
    
    .subtitle {
        color: #8B949E;
        font-size: 16px;
    }

    /* Original 3-Column Feature Strip */
    .feature-card {
        background: #161B22;
        border-radius: 12px;
        padding: 24px;
        text-align: center;
        border: 1px solid #30363D;
        height: 100%;
        transition: transform 0.2s;
    }
    
    .feature-card:hover {
        border-color: #58A6FF;
        background: #1C2128;
        box-shadow: 0 0 20px rgba(88, 166, 255, 0.1);
    }
    
    .feature-icon-circle {
        width: 48px;
        height: 48px;
        background: rgba(88, 166, 255, 0.1);
        border: 1px solid #58A6FF;
        color: #58A6FF;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 15px;
        font-size: 1.25rem;
    }

    /* Labels & Badges */
    .gold-label {
        color: #58A6FF !important; /* Electric Blue Accent */
        font-size: 12px;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        font-weight: 700;
        margin-bottom: 12px;
        display: block;
    }

    /* Input Controls */
    .stRadio > div {
        background-color: #161B22;
        padding: 6px;
        border-radius: 10px;
        border: 1px solid #30363D;
    }
    
    /* Text Inputs - Fixed Spacing for Selectboxes */
    textarea {
        background-color: #0D1117 !important;
        color: #F0F6FC !important;
        border: 1px solid #30363D !important;
        border-radius: 10px !important;
        padding: 16px !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    /* Small inputs (like selectbox search) should have normal padding */
    input {
        background-color: #0D1117 !important;
        color: #F0F6FC !important;
        border: 1px solid #30363D !important;
        border-radius: 6px !important;
    }
    
    textarea:focus {
        border-color: #58A6FF !important;
        box-shadow: 0 0 0 3px rgba(88, 166, 255, 0.1) !important;
    }

    /* Action Buttons */
    div.stButton > button {
        background-color: #238636 !important; /* Professional Success Green */
        color: #FFFFFF !important;
        font-weight: 600 !important;
        border-radius: 8px !important;
        padding: 14px 28px !important;
        border: 1px solid rgba(240, 246, 252, 0.1) !important;
        width: 100%;
    }
    
    div.stButton > button:hover {
        background-color: #2EA043 !important;
        border-color: #3FB950 !important;
        box-shadow: 0 0 20px rgba(46, 160, 67, 0.2);
    }

    /* Results Card / Expander */
    .stExpander {
        background-color: #161B22 !important;
        border: 1px solid #30363D !important;
        border-radius: 12px !important;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.4);
    }
    
    .stExpander details summary {
        background-color: #161B22 !important;
        color: #F0F6FC !important;
        font-weight: 600 !important;
        padding: 15px !important;
    }

    /* Download Buttons */
    div.stDownloadButton > button {
        background-color: transparent !important;
        color: #58A6FF !important;
        border: 1px solid #58A6FF !important;
        border-radius: 6px !important;
        font-size: 13px !important;
    }
    
    div.stDownloadButton > button:hover {
        background-color: #58A6FF !important;
        color: #FFFFFF !important;
    }

    /* Success Message */
    .success-badge {
        background: rgba(35, 134, 54, 0.15);
        color: #3FB950;
        padding: 12px 20px;
        border-radius: 8px;
        border: 1px solid #238636;
        margin-bottom: 25px;
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 10px;
    }

    /* Process Badge Circle */
    .step-circle {
        width: 24px;
        height: 24px;
        border-radius: 50%;
        background: #58A6FF;
        color: #0D1117;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-size: 12px;
        font-weight: 800;
        margin-right: 12px;
    }

    /* Custom Scrollbar */
    ::-webkit-scrollbar { width: 8px; }
    ::-webkit-scrollbar-track { background: #0D1117; }
    ::-webkit-scrollbar-thumb { background: #30363D; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# 3. Sidebar Layout (RESTORING ALL ORIGINAL CONTENT)
with st.sidebar:
    st.markdown("""
        <div class="sidebar-card">
            <h2 style='margin:0; font-size:1.5rem; color:white;'>⚖️ Legal Literacy</h2>
            <p class="sidebar-tagline">Bridging the gap between law and citizens.</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<p class="gold-label">Select Target Language</p>', unsafe_allow_html=True)
    target_lang = st.selectbox(
        "Target Language",
        options=list(SUPPORTED_LANGUAGES.keys()),
        index=1,
        label_visibility="collapsed"
    )
    
    st.markdown('<hr style="border-color:#30363D;">', unsafe_allow_html=True)
    
    # Original "How it works" roadmap
    st.markdown("""
        <div class="sidebar-card">
            <p style="color:#58A6FF; font-weight:700; margin-bottom:15px; font-size:14px;">🛠️ How it works</p>
            <p style="margin-bottom:12px;"><span class="step-circle">1</span> <span style="color:white; font-size:14px;">Input</span><br><small style="color:#8B949E; margin-left:36px;">Provide text or audio</small></p>
            <p style="margin-bottom:12px;"><span class="step-circle">2</span> <span style="color:white; font-size:14px;">STT</span><br><small style="color:#8B949E; margin-left:36px;">Audio Transcription</small></p>
            <p style="margin-bottom:12px;"><span class="step-circle">3</span> <span style="color:white; font-size:14px;">Simplify</span><br><small style="color:#8B949E; margin-left:36px;">Jargon removal</small></p>
            <p style="margin-bottom:12px;"><span class="step-circle">4</span> <span style="color:white; font-size:14px;">Translate</span><br><small style="color:#8B949E; margin-left:36px;">Local language</small></p>
            <p><span class="step-circle">5</span> <span style="color:white; font-size:14px;">Narrate</span><br><small style="color:#8B949E; margin-left:36px;">Audio narration</small></p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br><p style='text-align:center; color:#484F58; font-size:11px;'>Powered by Sunbird AI</p>", unsafe_allow_html=True)

# 4. Main Area Header (RESTORING ORIGINAL TEXT)
st.markdown("""
    <div class="header-container">
        <h1>⚖️ Legal Literacy Bridge</h1>
        <p class="subtitle">Breaking down legal barriers for every Ugandan citizen</p>
        <div style="width: 60px; height: 2px; background: #58A6FF; margin: 20px auto;"></div>
    </div>
""", unsafe_allow_html=True)

# 5. Original 3-Column Feature Strip (RESTORING ALL ORIGINAL TEXT)
fcol1, fcol2, fcol3 = st.columns(3)
with fcol1:
    st.markdown("""
        <div class="feature-card">
            <div class="feature-icon-circle">🎙️</div>
            <p style="font-weight:700; color:white; margin:0;">Speech to Text</p>
            <p style="color:#8B949E; font-size:12px;">Audio transcription in seconds</p>
        </div>
    """, unsafe_allow_html=True)
with fcol2:
    st.markdown("""
        <div class="feature-card">
            <div class="feature-icon-circle">📖</div>
            <p style="font-weight:700; color:white; margin:0;">Plain English</p>
            <p style="color:#8B949E; font-size:12px;">Legal jargon simplified</p>
        </div>
    """, unsafe_allow_html=True)
with fcol3:
    st.markdown("""
        <div class="feature-card">
            <div class="feature-icon-circle">🌍</div>
            <p style="font-weight:700; color:white; margin:0;">5 Languages</p>
            <p style="color:#8B949E; font-size:12px;">Luganda · Runyankole · Ateso · Lugbara · Acholi</p>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# 6. Session State Initialization
if "text_result" not in st.session_state:
    st.session_state["text_result"] = None
if "audio_result" not in st.session_state:
    st.session_state["audio_result"] = None

# 7. Input Mode Selection
st.markdown('<p class="gold-label">Select Input Mode</p>', unsafe_allow_html=True)
input_mode = st.radio(
    "Input Method Selection",
    ["📝 Paste Legal Text", "🎙️ Upload Audio Recording"],
    horizontal=True,
    label_visibility="collapsed"
)

st.markdown("<br>", unsafe_allow_html=True)

# 8. Main Logic & Display
if input_mode == "📝 Paste Legal Text":
    st.markdown('<p class="gold-label">📄 Legal Text</p>', unsafe_allow_html=True)
    legal_text = st.text_area(
        "Legal Text Input", 
        placeholder="Paste your legal document, contract clause, or court notice here...",
        height=200,
        label_visibility="collapsed"
    )
    
    if st.button("Analyse & Translate", type="primary"):
        if not legal_text.strip():
            st.warning("Please provide some text to analyse.")
        else:
            with st.spinner("⚖️ Processing through 4 AI phases..."):
                try:
                    pipeline = LegalBridgePipeline()
                    st.session_state["text_result"] = pipeline.run_from_text(legal_text, target_lang)
                except Exception as e:
                    st.error(format_error(e))

    # Display Text Results
    if st.session_state["text_result"]:
        res = st.session_state["text_result"]
        st.markdown('<div class="success-badge"><span>✅</span> Analysis Complete!</div>', unsafe_allow_html=True)
        st.markdown('<p class="gold-label">Analysis Results</p>', unsafe_allow_html=True)
        
        with st.expander("📖 Phase 2 — Plain English Summary", expanded=True):
            st.markdown(res["simplified"])
            st.download_button("Download Summary (TXT)", res["simplified"], "summary.txt", key="dl_text_s")
            
        with st.expander(f"🌍 Phase 3 — {res['target_language']} Translation", expanded=True):
            st.markdown(res["translated"])
            st.download_button(f"Download {res['target_language']} Translation", res["translated"], "trans.txt", key="dl_text_t")
            
        with st.expander("🔊 Phase 4 — Audio Narration", expanded=True):
            st.audio(res["audio_bytes"])
            st.download_button("Download Narration (WAV)", res["audio_bytes"], "audio.wav", key="dl_text_a")

else:
    # Audio Mode
    col_a1, col_a2 = st.columns(2)
    with col_a1:
        st.markdown('<p class="gold-label">Audio Language (Source)</p>', unsafe_allow_html=True)
        source_lang = st.selectbox(
            "Source Lang",
            options=list(SUPPORTED_LANGUAGES.keys()),
            index=0,
            label_visibility="collapsed"
        )
    
    st.markdown('<p class="gold-label">Audio File</p>', unsafe_allow_html=True)
    uploaded_audio = st.file_uploader(
        "Upload", type=["mp3", "wav", "ogg", "m4a"], label_visibility="collapsed"
    )
    st.info("Limit: 5 minutes. Support: MP3, WAV, OGG, M4A.")
    
    if st.button("Transcribe, Analyse & Translate", type="primary"):
        if uploaded_audio is None:
            st.warning("Please upload an audio file first.")
        else:
            with st.spinner("⚖️ Processing through 4 AI phases..."):
                try:
                    audio_bytes, fmt = validate_audio_file(uploaded_audio)
                    pipeline = LegalBridgePipeline()
                    st.session_state["audio_result"] = pipeline.run_from_audio(
                        audio_bytes, fmt, target_lang, source_lang=source_lang
                    )
                except Exception as e:
                    st.error(format_error(e))

    # Display Audio Results
    if st.session_state["audio_result"]:
        res = st.session_state["audio_result"]
        st.markdown('<div class="success-badge"><span>✅</span> Analysis Complete!</div>', unsafe_allow_html=True)
        st.markdown('<p class="gold-label">Analysis Results</p>', unsafe_allow_html=True)
        
        with st.expander("📋 Phase 1 — Transcript", expanded=True):
            st.text_area("Transcript", res["transcript"], height=100, disabled=True)
            
        with st.expander("📖 Phase 2 — Plain English Summary", expanded=True):
            st.markdown(res["simplified"])
            st.download_button("Download Summary (TXT)", res["simplified"], "summary.txt", key="dl_audio_s")
            
        with st.expander(f"🌍 Phase 3 — {res['target_language']} Translation", expanded=True):
            st.markdown(res["translated"])
            st.download_button(f"Download {res['target_language']} Translation", res["translated"], "trans.txt", key="dl_audio_t")
            
        with st.expander("🔊 Phase 4 — Audio Narration", expanded=True):
            st.audio(res["audio_bytes"])
            st.download_button("Download Narration (WAV)", res["audio_bytes"], "audio.wav", key="dl_audio_a")
