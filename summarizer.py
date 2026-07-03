import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def summarize_transcript(transcript: str, segments: list) -> dict:
    timestamped_text = ""
    for seg in segments:
        start = int(seg['start'])
        minutes = start // 60
        seconds = start % 60
        timestamped_text += f"[{minutes:02d}:{seconds:02d}] {seg['text']}\n"
    
    prompt = f"""You are a smart note-taking assistant. Given this video transcript with timestamps, create:

1. A brief summary (3-4 sentences)
2. Key points with their timestamps (format: [MM:SS] - Key point)
3. Action items or important tasks mentioned

Transcript:
{timestamped_text[:4000]}

Format your response clearly with these 3 sections."""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=1000,
    )
    
    return {
        "notes": response.choices[0].message.content,
        "full_transcript": transcript,
        "timestamped": timestamped_text
    }