---
title: Sunbird AI Pipeline
emoji: 🐦
colorFrom: green
colorTo: yellow
sdk: gradio
sdk_version: 6.14.0
app_file: app.py
pinned: false
---

# Sunbird AI Pipeline

A Gradio web application that accepts text or audio...
(rest of your existing README stays the same)

# Sunbird AI Pipeline

A Gradio web application that accepts text or audio, then runs it through a four-step AI pipeline — entirely powered by [Sunbird AI](https://sunbird.ai/) — to produce a translated, spoken summary in a Ugandan local language.

---

## Project description

This app lets a user provide either typed/pasted text or an uploaded audio file. If audio is supplied, it is first transcribed to text using Sunbird's Speech-to-Text API. The text (typed or transcribed) is then summarised using the Sunflower LLM, and the summary is translated into a chosen Ugandan local language — Luganda, Runyankole, Ateso, Lugbara, or Acholi — using the same LLM. Finally, the translated summary is synthesised as a playable audio clip via Sunbird's Text-to-Speech API. All four intermediate outputs (transcript, summary, translated summary, and audio player) are displayed directly in the UI, so the user can inspect every stage of the pipeline.

---

## Architecture overview

```
User input
  │
  ├─ Text (typed / pasted) ──────────────────────────────┐
  │                                                       │
  └─ Audio file (.mp3 / .wav / .ogg / .m4a / .aac)       │
         │                                                │
         ▼  [audio path only]                             │
  ┌──────────────────────┐                                │
  │  Sunbird STT         │                                │
  │  POST /tasks/stt     │                                │
  │  multipart `audio`   │                                │
  └────────┬─────────────┘                                │
           │ transcript text                              │
           └──────────────────────────────────────────► ──┘
                                                          │
                                                          ▼
                                        ┌─────────────────────────────┐
                                        │  Sunflower LLM — summarise  │
                                        │  POST /tasks/sunflower_     │
                                        │        simple               │
                                        │  form-encoded `instruction` │
                                        └───────────────┬─────────────┘
                                                        │ summary
                                                        ▼
                                        ┌─────────────────────────────┐
                                        │  Sunflower LLM — translate  │
                                        │  POST /tasks/sunflower_     │
                                        │        simple               │
                                        │  form-encoded `instruction` │
                                        └───────────────┬─────────────┘
                                                        │ translated summary
                                                        ▼
                                        ┌─────────────────────────────┐
                                        │  Sunbird TTS                │
                                        │  POST /tasks/modal/tts      │
                                        │  JSON `text` + `speaker_id` │
                                        └───────────────┬─────────────┘
                                                        │ signed audio URL
                                                        ▼
                                                  Audio player
```

| Step | Endpoint | Format |
|---|---|---|
| Speech-to-Text | `POST /tasks/stt` | `multipart/form-data`, field: `audio` |
| Summarise | `POST /tasks/sunflower_simple` | `application/x-www-form-urlencoded`, field: `instruction` |
| Translate | `POST /tasks/sunflower_simple` | same endpoint, different instruction prompt |
| Text-to-Speech | `POST /tasks/modal/tts` | `application/json`, fields: `text`, `speaker_id` |

---

## Local setup

```bash
# 1. Clone the repository
git clone https://github.com/GeorgeLukaanya/internship-assessment.git
cd internship-assessment

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate          # Linux / macOS
# venv\Scripts\activate.bat       # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment variables
cp .env.example .env
# Edit .env and replace the placeholder with your real Sunbird AI API token

# 5. Run the app
python app.py
# Opens at http://127.0.0.1:7860
```

---

## Environment variables

| Variable | Required | Description |
|---|---|---|
| `SUNBIRD_API_TOKEN` | **Yes** | Bearer token for all Sunbird AI API calls. Get one at [api.sunbird.ai](https://api.sunbird.ai/). |

Copy `.env.example` to `.env` and paste your token. The `.env` file is listed in `.gitignore` — never commit it.

```
# .env.example
SUNBIRD_API_TOKEN=your_token_here
```

---

## Usage

### Text input

1. Open the app (`http://127.0.0.1:7860` locally, or the deployed link below).
2. Select the **Text input** tab.
3. Pick a **Target language** from the dropdown (Luganda, Runyankole, Ateso, Lugbara, or Acholi).
4. Paste or type your text into the text box.
5. Click **Summarise & Translate**.
6. After 3–6 minutes the results appear:
   - **Summary** — concise English summary from the Sunflower LLM
   - **Translated summary** — the summary in the chosen language
   - **Synthesised speech** — an inline audio player for the translated summary

### Audio upload

1. Select the **Audio upload** tab.
2. Pick a **Target language**.
3. Upload an audio file (MP3, WAV, OGG, M4A, or AAC). Files longer than **5 minutes** are rejected immediately with an error message.
4. Click **Transcribe, Summarise & Translate**.
5. After 3–6 minutes the results appear:
   - **Transcript** — the text returned by Sunbird STT
   - **Summary**, **Translated summary**, and **Synthesised speech** as above

> The Gradio button shows a spinner while the pipeline runs. Each run makes three sequential API calls (two LLM + one TTS), which accounts for the latency.

---

## Deployed link

**[https://huggingface.co/spaces/musheijaa/sunbird-ai-pipeline](https://huggingface.co/spaces/musheijaa/sunbird-ai-pipeline)**

The app is hosted on Hugging Face Spaces (Gradio SDK). The `SUNBIRD_API_TOKEN` is stored as a Space secret and is never exposed in the repository.

---

## Known limitations

- **Slow inference** — The Sunflower LLM is called twice (summarise + translate) and TTS once per run. Total latency is typically **3–6 minutes**; this reflects the Sunbird API's inference speed, not the application itself.
- **5-minute audio cap** — Audio longer than 300 seconds is rejected client-side before any API call is made.
- **Supported languages** — Luganda, Runyankole, Ateso, Lugbara, Acholi. Swahili has a TTS voice (`speaker_id` 246) but is not a Ugandan local language and is excluded from the picker.
- **English source text recommended** — The Sunflower LLM summarises most reliably from English. Quality may vary for other input languages.
- **Free-tier account** — The `SUNBIRD_API_TOKEN` is a free-tier token; rate limits or quotas imposed by Sunbird AI may apply.
- **Audio format detection** — Duration checking relies on `mutagen`. Uncommon or DRM-protected formats may bypass the local check; the Sunbird API enforces its own 100 MB / 10-minute limits as a fallback.
