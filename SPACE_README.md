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

# Sunbird AI — Transcribe · Summarise · Translate · Speak

A Gradio web app powered entirely by [Sunbird AI](https://sunbird.ai/).

Provide text or an audio file and the pipeline will:
1. **Transcribe** audio → text (Sunbird STT, audio path only)
2. **Summarise** the text with the Sunflower LLM
3. **Translate** the summary into a Ugandan local language (Luganda, Runyankole, Ateso, Lugbara, or Acholi)
4. **Synthesise** the translation as speech (Sunbird TTS)
