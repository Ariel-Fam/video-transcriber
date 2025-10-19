from moviepy import VideoFileClip
import whisper
import streamlit as st
import tempfile
import os
import nltk
from textblob import TextBlob

from nltk.tokenize import sent_tokenize


@st.cache_resource
def download_punked_tab():
    nltk.download('punkt_tab')


def extract_audio(video_path, audio_path):
    """
    Extracts audio from the given video file and saves it as a WAV file.
    """
    with VideoFileClip(video_path) as video:
        audio = video.audio
        if audio is None:
            raise ValueError("No audio stream found in the video.")
        audio.write_audiofile(audio_path, codec='pcm_s16le')  # Ensure WAV format
        audio.close()




def transcribe_audio(audio_path, model_size="base"):
    """
    Transcribes the given audio file using the specified Whisper model.
    """
    model = whisper.load_model(model_size)
    result = model.transcribe(audio_path)
    return result["text"]


def format_text(text):
    # blob = TextBlob(text)
    #
    # sentences = blob.sentences
    #
    # paragraphs = [sentences[i:i + 10] for i in range(0, len(sentences), 10)]
    #
    # essay = "\n\n".join(" ".join(str(sentence) for sentence in para) for para in paragraphs)

    sentences = sent_tokenize(text)

    # Group sentences into paragraphs (e.g., 2 sentences per paragraph)
    paragraphs = [sentences[i:i + 10] for i in range(0, len(sentences), 10)]

    # Format paragraphs
    essay = "\n\n".join(" ".join(paragraph) for paragraph in paragraphs)
    return essay


def main():



    st.set_page_config(
        page_title="Video Transcriber",
        layout="wide",
        initial_sidebar_state="expanded",
        page_icon="favicon.ico"
    )

    download_punked_tab()

    st.subheader("📹 Video Transcription App")
    st.write("Upload a video file, and this app will extract the audio and transcribe it for you.")

    # Initialize session state variables
    if 'transcript' not in st.session_state:
        st.session_state.transcript = None
    if 'processing' not in st.session_state:
        st.session_state.processing = False
    if 'error' not in st.session_state:
        st.session_state.error = None


    sidebar = st.sidebar

    with sidebar:
        logo = st.image("files/Space Pointer Logo.png")
    # File uploader allows various video formats
        uploaded_file = st.file_uploader(
            "Choose a video file",
            type=["mp4", "mov", "avi", "mkv", "flv", "wmv"]
        )

        app_logo = st.image("images/video_transriber_2.0.png")

    # Option to select Whisper model size
    model_size = st.selectbox(
        "Select Whisper Model Size",
        options=["tiny", "base", "small", "medium", "large"],
        index=1  # Default to 'base'
    )

    if uploaded_file is not None:
        # Display file details
        st.write(f"**Filename:** {uploaded_file.name}")
        st.write(f"**File Size:** {uploaded_file.size / (1024 * 1024):.2f} MB")

        # Check if transcript already exists for the uploaded file
        # To uniquely identify the file, we can use its name and size
        file_id = f"{uploaded_file.name}_{uploaded_file.size}"
        if 'file_id' not in st.session_state or st.session_state.get('file_id') != file_id:
            st.session_state.transcript = None  # Reset transcript if a new file is uploaded
            st.session_state.file_id = file_id

        if st.session_state.transcript is None and not st.session_state.processing:
            # Button to start transcription
            if st.button("Start Transcription"):
                with st.spinner("🎬 Extracting audio from the video..."):
                    st.session_state.processing = True
                    try:
                        with tempfile.TemporaryDirectory() as tmpdirname:
                            video_path = os.path.join(tmpdirname, uploaded_file.name)

                            # Save uploaded video to the temporary directory
                            with open(video_path, "wb") as f:
                                f.write(uploaded_file.getbuffer())

                            audio_path = os.path.join(tmpdirname, "extracted_audio.wav")

                            # Extract audio from the uploaded video
                            extract_audio(video_path, audio_path)

                            # Transcribe the extracted audio
                            with st.spinner("📝 Transcribing audio..."):
                                transcript = transcribe_audio(audio_path, model_size=model_size)
                                formatted_transcript = format_text(transcript)

                                st.session_state.transcript = formatted_transcript
                                st.success("✅ Transcription completed successfully!")

                    except Exception as e:
                        st.session_state.error = f"❌ An error occurred: {e}"
                        st.error(st.session_state.error)
                    finally:
                        st.session_state.processing = False

        # Display transcript if available
        if st.session_state.transcript:
            st.subheader("📝 Transcript:")
            st.text_area("Transcript:", st.session_state.transcript, height=700)

            # Option to download the transcript as a text file
            st.download_button(
                label="📥  Download Transcript",
                data=st.session_state.transcript,
                file_name="transcript.txt",
                mime="text/plain"
            )

    # Optionally, display errors
    if st.session_state.error:
        st.error(st.session_state.error)


if __name__ == "__main__":
    main()

