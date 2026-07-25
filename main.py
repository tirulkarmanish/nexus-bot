import os
import random
import asyncio
import google.generativeai as genai
import edge_tts
from moviepy.editor import AudioFileClip, ColorClip, TextClip, CompositeVideoClip

# --- 1. SCRIPT GENERATION ---
GENAI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GENAI_API_KEY)

CATEGORIES = [
    "Mobile apps that pay real cash for micro-tasks",
    "High-paying freelancing skills for beginners",
    "Best passive income tools & websites",
    "Student side-hustles with zero investment",
    "AI tools to make money online"
]

def generate_script():
    category = random.choice(CATEGORIES)
    prompt = f"""
    You are an expert content creator for YouTube channel 'Nexus Earning'.
    Write a fast-paced, highly engaging 25-second YouTube Short script in Hinglish about '{category}'.
    Rules:
    - Language: Energetic Hinglish (Hindi + English).
    - Output: Plain spoken text ONLY. No brackets, no captions, no metadata.
    """
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(prompt)
    return response.text.strip()

# --- 2. VOICEOVER GENERATION ---
async def generate_audio(text, output_file="voice.mp3"):
    communicate = edge_tts.Communicate(text, "hi-IN-MadhurNeural")
    await communicate.save(output_file)

# --- 3. VIDEO CREATION ---
def create_video(audio_path="voice.mp3", output_path="final_short.mp4"):
    audio = AudioFileClip(audio_path)
    
    # 1080x1920 Vertical Canvas (Shorts Format)
    bg = ColorClip(size=(1080, 1920), color=(15, 23, 42), duration=audio.duration)
    
    # Title Overlay
    text = TextClip("NEXUS EARNING", fontsize=75, color='yellow', font='Arial-Bold')
    text = text.set_position(('center', 300)).set_duration(audio.duration)
    
    final_video = CompositeVideoClip([bg, text]).set_audio(audio)
    final_video.write_videofile(output_path, fps=24, codec="libx264", audio_codec="aac")

# --- MAIN EXECUTION ---
if __name__ == "__main__":
    print("[1/3] Generating AI Script...")
    script = generate_script()
    print(f"Script: {script}\n")
    
    print("[2/3] Generating Voiceover...")
    asyncio.run(generate_audio(script))
    
    print("[3/3] Assembling Video...")
    create_video()
    
    print("✅ Video Successfully Generated: final_short.mp4")
