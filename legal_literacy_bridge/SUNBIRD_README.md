# Legal Literacy Bridge ⚖️

An AI-powered legal document simplification and translation web application designed to empower Ugandan citizens with accessible legal knowledge.

## Overview

The **Legal Literacy Bridge** helps users understand complex legal documents, court notices, or contracts by processing them through a 4-phase AI pipeline:
1. **Transcribe**: Converts legal audio recordings into English text (if audio input is used).
2. **Simplify**: Rewrites complex legal text into plain English for easier understanding.
3. **Translate**: Translates the simplified summary into one of five local Ugandan languages.
4. **Narrate**: Synthesizes the translated text into a playable audio clip.

All AI capabilities are powered by [Sunbird AI](https://sunbird.ai/).

## Prerequisites

- **Python 3.10+**
- **FFmpeg**: Required by the `pydub` library for audio processing.
  - **Windows**: Install via `choco install ffmpeg` or download from [ffmpeg.org](https://ffmpeg.org/download.html).
  - **Linux (Ubuntu/Debian)**: `sudo apt update && sudo apt install ffmpeg`
  - **macOS**: `brew install ffmpeg`

## Setup Instructions

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd legal_literacy_bridge
   ```

2. **Configure Environment Variables**:
   Copy the example environment file and add your Sunbird AI API key.
   ```bash
   cp .env.example .env
   ```
   Open `.env` and set `SUNBIRD_API_KEY=your_actual_key_here`.

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application**:
   ```bash
   streamlit run app.py
   ```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SUNBIRD_API_KEY` | Your Sunbird AI API token. | Required |
| `SUNBIRD_BASE_URL` | Base URL for Sunbird AI API. | `https://api.sunbird.ai/api/v1` |

## API Reference

The application interacts with the following Sunbird AI endpoints:
- **STT (`/stt`)**: Speech-to-text transcription.
- **Chat (`/chat`)**: Used for both text simplification and translation using the Sunflower LLM.
- **TTS (`/tts`)**: Text-to-speech synthesis for local Ugandan languages.

## Troubleshooting

- **Missing API Key**: Ensure your `.env` file exists and contains a valid `SUNBIRD_API_KEY`.
- **FFmpeg Not Found**: If you see an error related to `pydub` or `AudioSegment`, ensure FFmpeg is installed and added to your system PATH.
- **Audio Too Long**: The app enforces a 5-minute limit on audio uploads to ensure prompt processing.
- **API Failures**: Check your internet connection and API token quota. The app surfaces specific phase failures in the UI.

## License

This project is licensed under the [MIT License](LICENSE).
