# 🐦 Sunbird AI — Transcribe, Summarise & Translate

A Generative AI web application powered by **Sunbird AI's Sunflower LLM** and Speech APIs. The app accepts English text or audio input, summarises it, translates the summary into a Ugandan local language, and generates a spoken audio output of the translation.

Built as part of the **Sunbird AI Internship Assessment**.

---

## 🌍 Live Demo

👉 **[Try the app here](https://huggingface.co/spaces/your-username/sunbird-ai-app)**

> Replace the link above with your actual Hugging Face Spaces URL after deployment.

---

## 📌 Project Description

This application solves a real communication problem in Uganda — making English content accessible to people who speak local languages. 

A user can:
- Type or paste English text, **or** upload a voice recording
- Select a target Ugandan language (Luganda, Runyankole, Acholi, Ateso, or Lugbara)
- Receive a summarised translation **and** a generated audio clip in that language

All AI capabilities are powered exclusively by **Sunbird AI** — no OpenAI or Anthropic APIs are used.

---

## 🏗️ Architecture Overview

The application follows a 4-step pipeline:

```
Input (Text or Audio)
        ↓
[Step 1] Speech-to-Text — Sunbird STT API
         Only runs if audio is uploaded
         Endpoint: /tasks/stt
        ↓
[Step 2] Summarisation — Sunflower LLM
         Shortens the text to 3 key sentences
         Endpoint: /tasks/sunflower_simple
        ↓
[Step 3] Translation — Sunflower LLM
         Translates summary to chosen Ugandan language
         Endpoint: /tasks/sunflower_simple
        ↓
[Step 4] Text-to-Speech — Sunbird TTS API
         Converts translated text to spoken audio
         Endpoint: /tasks/tts
        ↓
Output (Transcript + Summary + Translation + Audio Player)
```

### File Structure

```
internship-assessment/
│
├── backend/
│   ├── __init__.py          # Makes backend a Python module
│   ├── sunbird_client.py    # All Sunbird API calls (STT, Sunflower, TTS)
│   └── pipeline.py          # Orchestrates the 4-step pipeline
│
├── exercises/
│   ├── __init__.py
│   └── basics.py            # Part 1: Python programming exercises
│
├── tests/
│   └── test_basics.py       # Pytest tests for Part 1
│
├── app.py                   # Streamlit frontend — the user interface
├── .env                     # Secret API token (not committed to Git)
├── .env.example             # Template showing required env variables
├── requirements.txt         # Python dependencies
└── README.md                # This file
```

---

## ⚙️ Local Setup

Follow these steps exactly to run the app on your machine.

### Prerequisites
- Python 3.10 or higher
- A Sunbird AI API token (see below)
- Git

### Step 1 — Clone the Repository

```bash
git clone https://github.com/<your-username>/internship-assessment.git
cd internship-assessment
```

### Step 2 — Create a Virtual Environment

```bash
python -m venv venv
```

Activate it:

- **Windows (PowerShell):**
```bash
.\venv\Scripts\Activate.ps1
```

- **Mac/Linux:**
```bash
source venv/bin/activate
```

You will see `(venv)` appear in your terminal when it is active.

### Step 3 — Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4 — Set Up Environment Variables

Create a `.env` file in the root folder:

```bash
cp .env.example .env
```

Open `.env` and add your Sunbird API token:

```
SUNBIRD_API_TOKEN=your_actual_token_here
```

See the **Environment Variables** section below for how to get your token.

### Step 5 — Run the App

```bash
streamlit run app.py
```

The app will open automatically at `http://localhost:8501`

---

## 🔑 Environment Variables

| Variable | Description | Required |
|---|---|---|
| `SUNBIRD_API_TOKEN` | Your Sunbird AI Bearer token for all API calls | ✅ Yes |

### How to Get Your Token

1. Go to [https://platform.sunbird.ai](https://platform.sunbird.ai)
2. Create a free account with your email
3. After logging in, copy your access token
4. Paste it into your `.env` file as shown above

> ⚠️ **Never commit your `.env` file to GitHub.** It is listed in `.gitignore` to protect your token.

---

## 🧪 Running the Tests (Part 1)

Part 1 of the assessment required implementing two Python functions — `collatz` and `distinct_numbers`.

To verify they work:

```bash
pytest
```

Expected output:
```
5 passed in 0.15s
```

---

## 🖥️ Usage Walkthrough

### Text Input Mode

1. Open the app at `http://localhost:8501`
2. Select **Text** as your input type
3. Paste or type English text in the text area

   Example:
   > *"Uganda is a landlocked country in East Africa with a population of about 45 million people. The capital city is Kampala. Uganda is known for its mountain gorillas and diverse wildlife found in national parks like Bwindi and Queen Elizabeth."*

4. Choose a target language from the dropdown (e.g. **Luganda**)
5. Click **Run Pipeline**
6. Wait for processing (10–20 seconds)
7. View the **Summary**, **Translation**, and play the **Generated Audio**

---

### Audio Input Mode

1. Select **Audio File** as your input type
2. Upload a voice recording (MP3, WAV, OGG, M4A — maximum 5 minutes)
3. Choose a target language
4. Click **Run Pipeline**
5. View the **Transcript**, **Summary**, **Translation**, and play the **Generated Audio**

---

## 🌐 Supported Languages

| Language | Code | TTS Speaker ID |
|---|---|---|
| Luganda | lug | 248 |
| Acholi | ach | 241 |
| Ateso | teo | 242 |
| Runyankole | nyn | 243 |
| Lugbara | lgg | 245 |

---

## 🔌 Sunbird AI API Reference

| Step | Endpoint | Method | Purpose |
|---|---|---|---|
| Speech-to-Text | `/tasks/stt` | POST | Transcribe audio to text |
| Summarise | `/tasks/sunflower_simple` | POST | Summarise text with Sunflower LLM |
| Translate | `/tasks/sunflower_simple` | POST | Translate text to local language |
| Text-to-Speech | `/tasks/tts` | POST | Convert text to spoken audio |

Full API documentation: [https://docs.sunbird.ai](https://docs.sunbird.ai)

---

## ⚠️ Known Limitations

| Limitation | Detail |
|---|---|
| Audio must be speech | STT is optimised for human voice. Uploading music will produce inaccurate transcripts |
| 5-minute audio cap | Audio files longer than 5 minutes are rejected with a clear error message |
| Short text inputs | Very short inputs like single words may cause the Sunflower model to respond unexpectedly |
| Temporary audio URLs | The generated TTS audio URL expires after 30 minutes — play it immediately |
| Free tier cold starts | On Hugging Face Spaces free tier, the app may take 30–60 seconds to wake up after inactivity |
| Language accuracy | Translation quality varies by language — Luganda performs best as it is Sunflower's strongest local language |

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend / UI | Streamlit |
| Backend | Python |
| AI APIs | Sunbird AI (STT, Sunflower LLM, TTS) |
| Deployment | Hugging Face Spaces |
| Environment | python-dotenv |
| HTTP Requests | requests |
| Testing | pytest |

---

## 👨‍💻 About the Developer

**Kennedy Mutebi**
BSc Computer Science — Makerere University, Kampala Uganda

Full-stack developer with experience in React.js, Django, Python, and Flutter. Passionate about building technology that solves real African problems.

- GitHub: [github.com/your-username](https://github.com/your-username)
- Email: kennedymutebi7@gmail.com
