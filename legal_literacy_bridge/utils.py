import io
from typing import Tuple
from pydub import AudioSegment

def validate_audio_file(uploaded_file) -> Tuple[bytes, str]:
    """
    Accept a Streamlit UploadedFile object, validate duration, and return bytes.
    
    Args:
        uploaded_file: The Streamlit uploaded file object.
        
    Returns:
        A tuple containing (audio_bytes, file_extension).
        
    Raises:
        ValueError: If audio exceeds 5 minutes or cannot be processed.
    """
    audio_bytes = uploaded_file.read()
    extension = uploaded_file.name.split(".")[-1].lower()
    
    # Load audio to check duration and convert to standard WAV
    try:
        audio = AudioSegment.from_file(io.BytesIO(audio_bytes), format=extension)
        duration_seconds = len(audio) / 1000.0
        
        # We no longer hard-limit to 5 minutes as we will chunk long-form audio
        
        # --- AGGRESSIVE AUDIO CLEANING ---
        audio = audio.set_channels(1)
        
        # 1. Boost volume to the limit
        from pydub.effects import normalize
        audio = normalize(audio, headroom=0.1)
        
        # 2. Target human speech frequencies (300Hz to 3000Hz)
        # This aggressively cuts out deep bass and high-pitched music
        audio = audio.high_pass_filter(300).low_pass_filter(3000)
        
        # 3. Add extra gain to boost quiet speech
        audio = audio + 10 
        
        # 4. Final normalization
        audio = normalize(audio)
        
        audio = audio.set_frame_rate(16000)
        
        wav_buffer = io.BytesIO()
        audio.export(wav_buffer, format="wav")
        return wav_buffer.getvalue(), "wav"
        
    except Exception as e:
        if "Audio file exceeds" in str(e):
            raise e
        raise ValueError(f"Could not process audio file: {str(e)}")

def split_audio_into_chunks(audio_bytes: bytes, chunk_length_ms: int = 600000):
    """
    Split audio bytes into chunks of specified length (default 10 mins).
    """
    audio = AudioSegment.from_file(io.BytesIO(audio_bytes), format="wav")
    chunks = []
    
    for i in range(0, len(audio), chunk_length_ms):
        chunk = audio[i : i + chunk_length_ms]
        chunk_buffer = io.BytesIO()
        chunk.export(chunk_buffer, format="wav")
        chunks.append(chunk_buffer.getvalue())
        
    return chunks

def truncate_text(text: str, max_chars: int = 4000) -> str:
    """
    Truncate text if it exceeds the maximum character limit.
    
    Args:
        text: The input text string.
        max_chars: Maximum allowed characters.
        
    Returns:
        The (possibly truncated) text string.
    """
    if len(text) > max_chars:
        return text[:max_chars] + "... [truncated for processing]"
    return text

def format_error(error: Exception) -> str:
    """
    Format an exception into a user-friendly error message.
    
    Args:
        error: The exception to format.
        
    Returns:
        A clean, emoji-prefixed error string.
    """
    message = str(error)
    # Strip potential technical details if needed
    if "RuntimeError:" in message:
        message = message.split("RuntimeError:")[-1].strip()
    
    return f"⚠️ {message}"
