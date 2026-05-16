# 🐦 Sunbird AI Assistant — Speak Local.

A Generative AI web application built on top of the **Sunbird AI API**. It takes English text or an English audio file, summarizes it, translates the summary into a chosen Ugandan local language, and generates a playable audio clip of the translation — all in one pipeline. Built with Python and Streamlit as part of the Sunbird AI Internship Assessment.

**Live Demo:** https://huggingface.co/spaces/ixmwiin3/sunbird-ai-assistant

---

## 🏗️ Architecture Overview

The application follows a linear 4-step pipeline:

```
User Input (Text or Audio)
        │
        ▼
[Step 1] STT — If audio is uploaded, Sunbird Modal STT (Whisper large-v3)
         transcribes it to English text. Text input skips this step.
        │
        ▼
[Step 2] Summarize — The English text is sent to Sunbird Sunflower Simple
         (Qwen model) which rewrites or condenses it into clear English.
         This step also corrects any transcription noise from the STT step.
        │
        ▼
[Step 3] Translate — The English summary is translated into the user's
         chosen local language using Sunbird's NLLB translation endpoint.
        │
        ▼
[Step 4] TTS — The translated text is converted to speech using Sunbird
         Modal TTS (Whisper-based), returning a signed GCP audio URL.
        │
        ▼
Output — UI displays the original text, English summary, translated
         summary, and a playable audio player.
```

### Sunbird API Endpoints Used

| Step | Endpoint | Format |
|------|----------|--------|
| Speech-to-Text | `POST /tasks/modal/stt` | multipart/form-data |
| Summarization | `POST /tasks/sunflower_simple` | application/x-www-form-urlencoded |
| Translation | `POST /tasks/translate` | application/json |
| Text-to-Speech | `POST /tasks/modal/tts` | application/json |

---

## 🛠️ Local Setup

### Prerequisites
- Python 3.10 or higher
- A Sunbird AI API token from https://api.sunbird.ai

### Steps

**1. Clone the repository**
```bash
git clone <your-repo-url>
cd internship-assessment/sunbird-app
```

**2. Create and activate a virtual environment**
```bash
python -m venv venv

# Windows
.\venv\Scripts\Activate.ps1

# Linux/Mac
source venv/bin/activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Configure environment variables**

Create a `.env` file in the `sunbird-app` folder based on `.env.example`:
```bash
cp .env.example .env
```

Then open `.env` and add your token:
```env
SUNBIRD_API_TOKEN=your_actual_token_here
```

**5. Run the app**
```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`.

---

## 🔑 Environment Variables

| Variable | Description |
|----------|-------------|
| `SUNBIRD_API_TOKEN` | Your personal API token from the Sunbird AI portal at https://api.sunbird.ai. Required for all API calls. Never commit this to git. |

---

## 📁 Project Structure

```
sunbird-app/
├── app.py                        # Main Streamlit UI and pipeline orchestration
├── backend/
│   ├── pipeline.py               # Initializes and exposes the SunbirdClient
│   ├── sunbird_client.py         # Wrapper around all Sunbird API endpoints
│   └── tests/                   # Standalone test scripts used during development
│       ├── stt_test.py           # Tests the original /tasks/stt endpoint
│       ├── modal_stt_test.py     # Tests the Modal STT endpoint (Whisper)
│       ├── translation_test.py   # Tests the /tasks/translate endpoint
│       ├── tts_test.py           # Tests /tasks/modal/tts
│       ├── tts_test2.py          # Tests /tasks/runpod/tts (failed)
│       ├── tts_test3.py          # Tests modal TTS with correct speaker_id
│       ├── sunflower_simple.py   # Tests the summarization endpoint
│       ├── sum_test.py           # Tests the English-forced summarization instruction
│       ├── language_test.py      # Tests the /tasks/language_id endpoint
│       └── check_token.py        # Decodes and validates the JWT API token
├── requirements.txt
├── .env.example
├── .gitignore
└── PROJECT_README.md
```

---

## 🧪 Test Scripts

During development, every API endpoint was tested in isolation before being wired into the main pipeline. Each script in `backend/tests/` targets a specific endpoint and prints the raw response so the exact field names and response structure could be confirmed before writing the client code.

| Script | What it tests |
|--------|---------------|
| `stt_test.py` | Original STT endpoint with hardcoded English language — later replaced by Modal STT |
| `modal_stt_test.py` | Modal Whisper STT which auto-detects audio language |
| `translation_test.py` | Confirms `/tasks/translate` works and shows the correct response structure |
| `tts_test.py` | First TTS attempt using `/tasks/modal/tts` — returned 500 due to wrong speaker_id |
| `tts_test2.py` | Tested `/tasks/runpod/tts` as an alternative — timed out consistently |
| `tts_test3.py` | Fixed TTS test using speaker_id 241 instead of 248 — returned 200 |
| `sunflower_simple.py` | Initial summarization test that confirmed form data format requirement |
| `sum_test.py` | Tests the updated English-forced instruction to prevent Swahili responses |
| `language_test.py` | Confirms `/tasks/language_id` returns `{"language": "lug"}` format |
| `check_token.py` | Decodes the JWT token to confirm it's valid and not expired |

---

## 🖥️ Usage

### Text Input
1. Select **Text Input** under 01 — Input
2. Choose a target language under 02 — Translate To
3. Type or paste your English text in the text area
4. Click **Process with Sunbird AI**
5. Results appear showing the original text, English summary, translated summary, and an audio player

### Audio Upload
1. Select **Audio Upload** under 01 — Input
2. Choose a target language under 02 — Translate To
3. Upload an MP3, WAV, or M4A file under 5 minutes
4. Click **Process with Sunbird AI**
5. Results appear showing the transcript, English summary, translated summary, and an audio player

---

## 🚧 Development Challenges and How They Were Solved

Building this app involved a significant amount of trial and error with the Sunbird API. Here is an honest account of the obstacles encountered and how each one was resolved.

**1. API token not loading in Streamlit context**
Plain `load_dotenv()` couldn't find the `.env` file when Streamlit ran the app from a different working directory. Fixed by using `load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))` to resolve the path relative to the client file itself.

**2. `/tasks/summarise` endpoint was deprecated and timing out**
The original summarization endpoint consistently timed out after 60 seconds. After checking the API docs, `/tasks/sunflower_simple` was identified as the replacement. However, this endpoint required form data (`data=`) instead of JSON (`json=`), which caused 422 validation errors until the docs were read carefully.

**3. Sunflower model responding in Swahili**
Even when given English input, the Sunflower model would sometimes respond in Swahili because Swahili is well-represented in its training data. Fixed by prepending `"You must respond in English only. Do not translate."` to every summarization instruction.

**4. Wrong speaker_id causing 500 errors on TTS**
The original code used `speaker_id=248` which consistently returned a 500 server error. After checking the API docs example response which showed `speaker_id: 241`, switching to 241 fixed the issue immediately.

**5. `/tasks/runpod/tts` timing out**
The RunPod TTS endpoint timed out on every attempt. The Modal TTS endpoint at `/tasks/modal/tts` was used instead and worked reliably.

**6. STT rejecting audio files with 422 errors**
The original STT call sent the file without a MIME type. The API couldn't determine the file format and rejected it. Fixed by using the tuple format `("filename.mp3", file_object, "audio/mpeg")` in the files parameter.

**7. Audio binary file blocking Hugging Face deployment**
A test audio file (`audio_test _0.mp3`) that was committed to the repository blocked the push to Hugging Face Spaces because binary files are not allowed in Space repositories. Resolved by removing the file from git history using `git filter-branch`.

---

## 💡 Ideas Explored and Their Limitations

**Bidirectional translation (Local → English and Local → Local)**
An attempt was made to support translating from local languages back to English, and between two local languages. The language detection endpoint (`/tasks/language_id`) was integrated to auto-detect the input language. However, the Sunbird translation model only supports translation to or from English — direct local-to-local translation is not supported. A pivot-through-English approach was implemented but the Sunflower summarization model produced unreliable output when given local language text, sometimes responding in Swahili or a mix of languages. This feature was removed from the final version to keep the app reliable and predictable.

**Live microphone translation**
A real-time push-to-talk feature was considered where the user could speak into their microphone and receive an instant translation. This is not feasible in Streamlit because Streamlit operates on a request-response model and does not support continuous audio streaming from the browser. This would require a proper WebRTC-based web application to implement correctly.

**Audio duration check using actual duration**
The assessment requires rejecting audio files longer than 5 minutes. The implementation uses file size as a proxy for duration (approximately 4.8MB for 5 minutes of 128kbps MP3) because checking actual duration requires `pydub` and `ffmpeg`. While ffmpeg is available on Hugging Face Spaces by default, it adds setup complexity. A proper duration check using `pydub` is planned as a future improvement.

---

## ⚠️ Known Limitations

- The app only accepts English as the input language. Uploading or typing in a local language will produce unreliable results because the summarization model is not reliable for non-English input.
- Audio files are limited to approximately 5 minutes, validated by file size rather than actual duration.
- The Sunflower summarization step can take 30–60 seconds depending on text length, which means the full pipeline can take 2–3 minutes to complete.
- TTS audio URLs expire after 30 minutes as they are signed GCP storage links.
- Translation accuracy for minority languages like Ateso and Lugbara is limited by the amount of training data available for those languages in Sunbird's models.
- The app requires an active internet connection at all times since all AI processing happens on Sunbird's servers.

---

## 🔧 Requirements

```
streamlit
requests
python-dotenv
```

---

*Built for the Sunbird AI Internship Assessment.*