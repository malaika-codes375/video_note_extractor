import whisper
import yt_dlp
import os
import tempfile
import shutil
import streamlit as st

def _ensure_node_alias():
    # yt-dlp looks for a command called "node", but Debian installs it as "nodejs"
    if shutil.which("node") is None:
        nodejs_path = shutil.which("nodejs")
        if nodejs_path:
            bin_dir = os.path.join(tempfile.gettempdir(), "nodebin")
            os.makedirs(bin_dir, exist_ok=True)
            symlink_path = os.path.join(bin_dir, "node")
            if not os.path.exists(symlink_path):
                os.symlink(nodejs_path, symlink_path)
            os.environ["PATH"] = bin_dir + os.pathsep + os.environ.get("PATH", "")

def download_audio(youtube_url: str) -> str:
    _ensure_node_alias()

    temp_dir = tempfile.mkdtemp()
    output_path = os.path.join(temp_dir, "audio.%(ext)s")

    cookie_path = os.path.join(temp_dir, "cookies.txt")
    with open(cookie_path, "w") as f:
        f.write(st.secrets["YOUTUBE_COOKIES"])

    ydl_opts = {
        'format': 'best',
        'outtmpl': output_path,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': False,
        'verbose': True,
        'cookiefile': cookie_path,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_url])

    audio_file = os.path.join(temp_dir, "audio.mp3")
    return audio_file


def transcribe_audio(audio_path: str) -> dict:
    model = whisper.load_model("tiny")
    result = model.transcribe(audio_path, verbose=False)
    return result