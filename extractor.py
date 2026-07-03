import whisper
import yt_dlp
import os
import tempfile

def download_audio(youtube_url: str) -> str:
    temp_dir = tempfile.mkdtemp()
    output_path = os.path.join(temp_dir, "audio.%(ext)s")
    
    ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': output_path,
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'quiet': True,
   'cookies_from_browser': ('edge',),
}
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_url])
    
    audio_file = os.path.join(temp_dir, "audio.mp3")
    return audio_file


def transcribe_audio(audio_path: str) -> dict:
    model = whisper.load_model("tiny")
    result = model.transcribe(audio_path, verbose=False)
    return result