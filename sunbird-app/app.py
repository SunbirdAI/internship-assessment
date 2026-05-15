import streamlit as st
from backend.pipeline import run_pipeline
from backend.errors import PipelineError, SunbirdAPIError


st.title("LocGen\nTranscribe, Summarise, Translate & Get Audio all in your local language!")

input_mode = st.radio("Input type", ["Text", "Audio file"])

text_input = ""
audio_input = b""

if input_mode == "Text":
    text_input = st.text_area("Paste or type your English text here")
else:
    uploaded = st.file_uploader("Upload a 'wav' English audio file", type="wav")
    if uploaded:
        audio_input = uploaded.read()

target_language = st.selectbox(
    label="Translate summary to:",
    options=["Acholi", "Lugbara", "Luganda", "Runyankole", "Ateso", "Swahili"],
)

if st.button("Run pipeline"):
    if not text_input and not audio_input:
        st.error("Please provide text or an audio file.")
    else:
        # empty "placeholders" to be filled as the generator yields new states
        st_transcript = st.empty()
        st_summary = st.empty()
        st_translation = st.empty()
        st_audio = st.empty()
        #st_total_timing = st.empty()

        with st.spinner("Processing..."):
            try:
                # Iterate over the generator... 'update' is the dict we yielded.
                for update in run_pipeline(
                    target_language=target_language,
                    text_input=text_input,
                    audio_input=audio_input,
                ):
                    state = update["current_state"]
                    results = update["results"]

                    # As each step finishes, fill in its text block
                    if state == "transcription":
                        if results["transcript"]:
                            with st_transcript.container():
                                st.subheader("Transcript")
                                st.write(results["transcript"])
                                # st.write(f"Transcript timing: {results['timing']['transcription']}")

                    elif state == "summarization":
                        with st_summary.container():
                            st.subheader("Summary")
                            st.write(results["summary"])
                            # st.write(f"Transcript timing: {results['timing']['summarization']}")

                    elif state == "translation":
                        with st_translation.container():
                            st.subheader("Translated Summary")
                            st.write(results["translation"])
                            # st.write(f"Translation timing: {results['timing']['translation']}")

                    elif state == "audio_clip":
                        with st_audio.container():
                            st.subheader("Audio")
                            if results["truncated"] is True:
                                st.write("Note: Summary was truncated")
                            else:
                                st.write("Summary intact! (not truncated)")
                            st.audio(data=results["audio"])
                            # st.write(f"Audio clip timing: {results['timing']['audio_clip']}")

                    #elif state == "complete":
                     #   with st_total_timing.container():
                            # st.write(f"\n\nTotal timing: {results['timing']['total']}")

            except PipelineError as e:
                st.error(f"Processing failed: {e}")
                st.exception(e)
            except SunbirdAPIError as e:
                st.error("API error while processing. Please try again later.")
                st.exception(e)
            except Exception as e:
                st.error("An unexpected error occurred.")
                st.exception(e)
