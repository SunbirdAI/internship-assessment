# Project Learnings — Sunbird App

A collection of key engineering lessons learned while building the Sunbird pipeline app.

---

## 1. Validate at Trust Boundaries, Not Everywhere

**Principle:** Don't add heavy runtime validation unless a trust boundary changes.

Validating data multiple times that has already been verified hurts performance without improving security.

**How it works:**

- **At the edge** (API Gateway, form submission handler): Apply strict, thorough validation the moment untrusted data enters the system.
- **Inside the system**: Once data is inside, components trust each other. Data moves freely via safe Data Transfer Objects (DTOs) without repetitive parsing.
- **Exception**: If data crosses into another independent system (a new trust boundary), validate again.

---

## 2. Choosing the Right Python Data Structure

Use the right tool based on where your data lives and how it flows.

### TypedDict — Mostly Static Safety

TypedDict only helps you while writing code in your editor. It acts as a linting tool, checking that a dictionary has the correct keys and types.

**The catch:** It does not enforce anything at runtime. If your code receives a broken dictionary while running, TypedDict will not throw an error — it lets the bad data pass right through.

### Pydantic — Runtime Validation at External Boundaries

When data crosses a trust boundary (e.g., an API response sent to another app), you cannot rely on static tools like TypedDict. Use Pydantic instead. It actively inspects data at runtime and immediately blocks corrupt input or output with an explicit error.

### Dataclasses — Layered Transformations

When data passes through multiple steps or pipeline layers and changes shape along the way, raw dictionaries become messy. A Python dataclass wraps data into a real object with cleaner attribute access (`user.id` instead of `user["id"]`), making complex pipelines easier to read and maintain.

### Decision Guide

| Situation | Tool |
|---|---|
| Dict-shaped payload/DTO passed between layers | `TypedDict` |
| Data crossing an external API boundary | `Pydantic` |
| Data that transforms across multiple pipeline stages | `dataclass` |
| Object with methods, behavior, or invariants | `dataclass` |

**Rule of thumb:** Start with `TypedDict` for app-layer payloads. Upgrade to `dataclass` only when pain appears (repeated transformation logic, invariants, helper methods, or readability issues from dict key access).

---

## 3. Optimize the Bottleneck, Not the Fast Parts

**Principle:** Optimize the step that takes the most time.

If the pipeline takes ~150 seconds total and TTS accounts for ~83 seconds of that, making Summarization instant (0 seconds) only saves the user 7 seconds — barely noticeable. The correct target is the TTS step, since it dominates total wait time.

> Always look at where time is actually being spent before deciding what to optimize.

---

## 4. Streamlit Streaming Limitations

Streamlit cannot easily yield partial dictionary results from a standard synchronous function. To stream intermediate outputs to the UI, the pipeline function must be converted into a **generator** (using `yield` instead of `return`), or Streamlit's `st.write_stream` / callback mechanisms must be used.

---

## 5. Sunbird API Limitations

### What You Cannot Do

**Token-streaming (word-by-word generation):** The Sunbird API endpoints use standard REST — you `POST` a request, the server processes the full result, and returns a single final JSON response. There is no `stream=True` (Server-Sent Events or WebSocket) support, so you cannot receive partial hypotheses as they are generated.

This applies to all Sunbird endpoints:
- `/tasks/sunflower_simple` (Summarization) — standard REST block
- `/tasks/translate` (NLLB Translation) — standard REST block
- `/tasks/modal/stt` (Speech-to-Text) — standard REST block
- `/tasks/modal/tts` (Text-to-Speech) — standard REST block

**Fake-streaming audio generation:** The TTS endpoint does not return an audio stream. It processes the full audio, uploads the file to cloud storage, and returns a URL string. The ~83-second wait is spent entirely on that server-side processing. Once you receive the URL, `st.audio(url)` handles buffered playback automatically — but you cannot start streaming a file that hasn't been synthesized yet.

### What You Can Do

**Step-by-step yielding:** Highly viable. You can yield intermediate UI updates between pipeline steps — e.g., show the transcript as soon as it's ready, before starting summarization.

**Fake typing UX:** Once you receive the full text from Sunbird, you can simulate a typing effect using `st.write_stream` and a generator to make the UI feel more responsive:

```python
import time

def stream_text_to_ui(full_text):
    for word in full_text.split(" "):
        yield word + " "
        time.sleep(0.05)

# Inside the UI loop:
st_summary_box.write_stream(stream_text_to_ui(results["summary"]))
```

This doesn't change when the data arrives, but it makes the experience feel more dynamic once it does.

---

## 6. Parsing Audio In-Memory with the `wave` Module

To avoid saving files to disk or pulling in heavy dependencies like `ffmpeg`, audio files can be parsed in memory using Python's built-in `wave` module:

```python
import wave
import io

wav = wave.open(io.BytesIO(audio_bytes))
```

This is a lightweight, dependency-free approach that works well within time or environment constraints.