import os
import re
from gtts import gTTS
from openai import OpenAI
from dotenv import load_dotenv
import uuid

load_dotenv()

def clean_text_for_speech(text):
    """
    Strips markdown formatting, HTML tags, list bullets, and emojis
    to make text-to-speech sound clean and professional.
    """
    # Remove HTML tags
    clean = re.sub(r'<[^>]*>', '', text)
    # Remove markdown bold, italic, headers, inline code
    clean = re.sub(r'\*\*|__|\*|_|~~|`|#+', '', clean)
    # Convert markdown links to plain text: [Link text](url) -> Link text
    clean = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', clean)
    # Remove bullet points at start of lines
    clean = re.sub(r'^[ \t]*[-\*\+]+[ \t]+', '', clean, flags=re.MULTILINE)
    # Remove table separators
    clean = re.sub(r'\|', ' ', clean)
    # Remove emojis
    clean = re.sub(r'[\u2600-\u27BF]|[\uE000-\uF8FF]|\uD83C[\uDC00-\uDFFF]|\uD83D[\uDC00-\uDFFF]|[\u2011-\u26FF]|\uD83E[\uDD10-\uDDFF]', '', clean)
    # Collapse multiple whitespace
    clean = re.sub(r'\s+', ' ', clean).strip()
    return clean

def text_to_speech(text, folder='static/audio'):
    """
    Converts text to speech. Uses OpenAI TTS if API key is available for premium sound,
    otherwise falls back to gTTS.
    """
    if not os.path.exists(folder):
        os.makedirs(folder)
        
    filename = f"response_{uuid.uuid4().hex}.mp3"
    filepath = os.path.join(folder, filename)
    
    # Clean text to prevent reading symbols out loud
    cleaned_text = clean_text_for_speech(text)
    if not cleaned_text:
        cleaned_text = "I have generated a response for you."
    
    from utils.db import get_setting
    api_key = get_setting("openai_api_key") or os.getenv("OPENAI_API_KEY")
    
    # Try OpenAI TTS for Professional "Alexa" feel
    if api_key and api_key != "your_openai_api_key_here":
        try:
            client = OpenAI(api_key=api_key)
            response = client.audio.speech.create(
                model="tts-1",
                voice="nova", # Professional "Alexa" like voice (Nova or Shimmer are good)
                input=cleaned_text[:4000] # OpenAI limit
            )
            response.stream_to_file(filepath)
            return f"/static/audio/{filename}"
        except Exception as e:
            print(f"OpenAI TTS failed: {e}. Falling back to gTTS.")

    # Fallback to gTTS (Free/Basic)
    try:
        tts = gTTS(text=cleaned_text, lang='en')
        tts.save(filepath)
        return f"/static/audio/{filename}"
    except Exception as e:
        print(f"Error in TTS fallback: {e}")
        return None
