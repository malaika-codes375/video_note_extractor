import streamlit as st
import os
import tempfile
from audio_extractor import download_audio, transcribe_audio
from summarizer import summarize_transcript
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="Video Note Extractor",
    page_icon="🎥",
    layout="centered"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');
body { font-family: 'Inter', sans-serif; }
.main-header {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
    padding: 30px;
    border-radius: 14px;
    margin-bottom: 24px;
    text-align: center;
}
.main-header h1 { color: white; font-size: 28px; margin: 0; }
.main-header p { color: #a0aec0; margin: 8px 0 0 0; }
.notes-box {
    background: #f7f9fc;
    border-radius: 12px;
    padding: 20px;
    border: 1px solid #e2e8f0;
    margin-top: 16px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="main-header">
    <h1>🎥 Video Note Extractor</h1>
    <p>Convert YouTube videos and lectures into organized notes instantly</p>
</div>
""", unsafe_allow_html=True)

tab_youtube, tab_upload = st.tabs(["🔗 YouTube URL", "📁 Upload Audio/Video"])

with tab_youtube:
    st.markdown("### Paste a YouTube URL")
    youtube_url = st.text_input("", placeholder="https://www.youtube.com/watch?v=...")
    
    if st.button("Extract Notes", key="yt_btn", use_container_width=True):
        if not youtube_url:
            st.warning("Please enter a YouTube URL first.")
        else:
            with st.spinner("Downloading audio..."):
                try:
                    audio_path = download_audio(youtube_url)
                    st.success("Audio downloaded!")
                except Exception as e:
                    st.error(f"Failed to download: {e}")
                    st.stop()
            
            with st.spinner("Transcribing audio (this may take a few minutes)..."):
                try:
                    result = transcribe_audio(audio_path)
                    st.success("Transcription complete!")
                except Exception as e:
                    st.error(f"Transcription failed: {e}")
                    st.stop()
            
            with st.spinner("Generating notes with AI..."):
                try:
                    notes = summarize_transcript(result['text'], result['segments'])
                    st.success("Notes ready!")
                except Exception as e:
                    st.error(f"Summarization failed: {e}")
                    st.stop()
            
            st.markdown("## 📝 Your Notes")
            st.markdown(f'<div class="notes-box">{notes["notes"]}</div>', unsafe_allow_html=True)
            
            with st.expander("📄 Full Transcript"):
                st.text(notes["full_transcript"])
            
            with st.expander("⏱️ Timestamped Transcript"):
                st.text(notes["timestamped"])
            
            st.download_button(
                "⬇️ Download Notes",
                data=notes["notes"],
                file_name="video_notes.txt",
                mime="text/plain"
            )

with tab_upload:
    st.markdown("### Upload an audio or video file")
    uploaded_file = st.file_uploader("", type=["mp3", "mp4", "wav", "m4a"])
    
    if st.button("Extract Notes", key="upload_btn", use_container_width=True):
        if not uploaded_file:
            st.warning("Please upload a file first.")
        else:
            with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp:
                tmp.write(uploaded_file.read())
                tmp_path = tmp.name
            
            with st.spinner("Transcribing audio..."):
                try:
                    result = transcribe_audio(tmp_path)
                    st.success("Transcription complete!")
                except Exception as e:
                    st.error(f"Transcription failed: {e}")
                    st.stop()
            
            with st.spinner("Generating notes with AI..."):
                try:
                    notes = summarize_transcript(result['text'], result['segments'])
                    st.success("Notes ready!")
                except Exception as e:
                    st.error(f"Summarization failed: {e}")
                    st.stop()
            
            st.markdown("## 📝 Your Notes")
            st.markdown(f'<div class="notes-box">{notes["notes"]}</div>', unsafe_allow_html=True)
            
            with st.expander("📄 Full Transcript"):
                st.text(notes["full_transcript"])
            
            with st.expander("⏱️ Timestamped Transcript"):
                st.text(notes["timestamped"])
            
            st.download_button(
                "⬇️ Download Notes",
                data=notes["notes"],
                file_name="video_notes.txt",
                mime="text/plain"
            )