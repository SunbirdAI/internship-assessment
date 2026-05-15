# LocGen (Sunbird AI Pipeline App)

## Project description
LocGen is a Streamlit web app that accepts either English text or an English WAV audio file, runs it through a Sunbird AI pipeline (speech-to-text when needed, summarization, translation to a selected local language, and text-to-speech), and displays intermediate and final outputs including transcript, summary, translated summary, and playable generated audio.

## Architecture overview

### Pipeline
1. **Input (UI)** → user provides text or uploads WAV audio.
2. **STT (audio only)** → `POST /tasks/modal/stt`
3. **Summarise** → `POST /tasks/sunflower_simple` (instruction: summarize)
4. **Translate** → `POST /tasks/sunflower_simple` (instruction: translate)
5. **TTS** → `POST /tasks/modal/tts`
6. **Output (UI)** → transcript (audio path), summary, translated text, and audio player.

### Code mapping
- `app.py` handles Streamlit UI input/output and renders each pipeline state.
- `backend/pipeline.py` orchestrates the stages and yields intermediate results.
- `backend/sunbird_client.py` wraps Sunbird endpoint calls.

## Local setup

Run the following from your terminal exactly as shown.

**Unix / macOS (bash/zsh):**

```bash
git clone https://github.com/delightaheebwa/internship-assessment.git
cd internship-assessment
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd sunbird-app
cp .env.example .env
```

**Windows (PowerShell):**

```powershell
git clone https://github.com/delightaheebwa/internship-assessment.git
cd internship-assessment
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
cd sunbird-app
Copy-Item .env.example .env
```

If you are working from your fork, replace the clone URL with your fork URL.

Then open `.env` and replace the placeholder token with your real Sunbird token:

```env
SUNBIRD_API_TOKEN=your_actual_token_here
```

Start the app:

```bash
streamlit run app.py
```

Open: `http://localhost:8501`

## Environment variables
- `SUNBIRD_API_TOKEN`: Bearer token used to authenticate all requests to `https://api.sunbird.ai` (STT, Sunflower, and TTS calls).

Reference file: `sunbird-app/.env.example`

## Usage (end-to-end walkthrough)
1. Open the app.
2. Choose **Text** or **Audio file** as input.
3. Enter English text (or upload a `.wav` English audio file).
4. Choose a target language (Acholi, Lugbara, Luganda, Runyankole, Ateso, Swahili).
5. Click **Run pipeline**.
6. Review outputs as they appear in order:
   - Transcript (only for audio input)
   - Summary
   - Translated Summary
   - Generated audio clip

### Screenshots
**1) Input stage (text mode selected; user enters source text and target language before running pipeline):**  
![Input stage](https://github.com/user-attachments/assets/a880bc28-8f78-446e-952d-41469f68a5e5)

**2) Selecting language stage (user selects the target language in which he or she wants the translation.):**  
![Intermediate text outputs](https://github.com/user-attachments/assets/ab49a9ea-e168-4b89-b086-ec371d7ba4ba)

**3) Intermediate stage (the pipeline is running and processing the user's input):**  
![Translated summary output](https://github.com/user-attachments/assets/4de5ee0f-2f9e-40d5-967a-c22eb69ee395)

**4) Final output stage (Summary, Translated Summary, and TTS generated audio ready for playback in the UI):**  
![Final audio output](https://github.com/user-attachments/assets/5d3ce6fc-cd9a-4ed5-a30e-30981b6885cd)

## Deployed link
https://huggingface.co/spaces/delight2004/sunbird_app

## Known limitations
- Audio upload currently supports **WAV only**.
- Audio files longer than **5 minutes** are rejected.
- Pipeline assumes English source for text input and transcription path.
- Available target languages are limited to configured voices: **Acholi, Lugbara, Luganda, Runyankole, Ateso, Swahili**.
- TTS input is truncated if translated text exceeds the API length ceiling (10,000 characters in this implementation).

  
