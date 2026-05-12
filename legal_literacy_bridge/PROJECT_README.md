# ⚖️ Legal Literacy Bridge

**Legal Literacy Bridge** is a premium AI-powered application designed to break down legal barriers for Ugandan citizens. The app transforms complex legal jargon—whether provided as text or via voice recordings—into simplified, understandable summaries in local Ugandan languages.

## 🚀 Key Features
- **Multimodal Input**: Accept typed legal text or high-capacity audio recordings.
- **Advanced Audio Processing**: Automatic voice normalization and high-pass filtering to clean up noisy recordings.
- **Long-Form Support**: Intelligent chunking that handles audio files longer than 2 hours.
- **Local Language Support**: Accurate translations into Luganda, Runyankole, Ateso, Lugbara, and Acholi.
- **Premium UI**: A law-firm inspired dark mode interface with real-time progress tracking.

---

## 🏗️ Architecture Overview

The application follows a modular 4-Phase pipeline:

1.  **Input Phase**: User provides text or uploads an audio file (up to 500MB).
2.  **Phase 1 — Transcription (STT)**: 
    - Audio is pre-processed for clarity.
    - Large files are split into 10-minute chunks.
    - **Endpoint**: Sunbird AI `/tasks/stt`
3.  **Phase 2 — Simplification (LLM)**: 
    - The legal text is analyzed and converted into "Plain English."
    - **Endpoint**: Sunbird AI `/tasks/sunflower_inference`
4.  **Phase 3 — Translation (LLM)**: 
    - The simplified summary is translated into the selected local language.
    - **Endpoint**: Sunbird AI `/tasks/sunflower_inference`
5.  **Phase 4 — Narration (TTS)**: 
    - The translation is converted back into speech for accessibility.
    - **Endpoint**: Sunbird AI `/tasks/tts`
6.  **Output Phase**: All intermediate results are displayed in expander cards for full transparency.

---

## 🛠️ Local Setup

### 1. Prerequisites
- Python 3.9+
- FFmpeg (Required for audio processing)

### 2. Installation
```bash
# Clone the repository
git clone https://github.com/<your-username>/internship-assessment.git
cd internship-assessment/legal_literacy_bridge

# Create and activate virtual environment
python -m venv venv
./venv/Scripts/activate  # Windows
source venv/bin/activate # Linux/Mac

# Install dependencies
pip install -r requirements.txt
```

### 3. Environment Configuration
Create a `.env` file in the `legal_literacy_bridge` directory:
```env
SUNBIRD_API_KEY=your_sunbird_api_key_here
SUNBIRD_BASE_URL=https://api.sunbird.ai/api/v1
```

### 4. Run the App
```bash
streamlit run app.py
```

---

## 🌍 Environment Variables

| Variable | Description |
| :--- | :--- |
| `SUNBIRD_API_KEY` | Your private API key from the Sunbird AI portal. |
| `SUNBIRD_BASE_URL` | The base URL for the Sunbird AI API (defaults to production). |

---

## ⚠️ Known Limitations
- **Background Noise**: While the app includes cleaning filters, extreme background music or very low-quality microphones may still impact STT accuracy.t
- **Processing Time**: Very long recordings (2+ hours) require sequential processing and may take several minutes to complete.
- **Character Limit**: Simplification is optimized for texts under 4,000 characters to ensure the best LLM response quality.

---

## ⚡ Powered by Sunbird AI
This project was built as part of the Sunbird AI Internship Assessment, utilizing the Sunbird STT, TTS, and Sunflower LLM models.
