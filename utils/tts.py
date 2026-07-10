import os
from gtts import gTTS
from openai import OpenAI
from dotenv import load_dotenv
import uuid

load_dotenv()

def text_to_speech(text, folder='static/audio'):
    """
    Converts text to speech. Uses OpenAI TTS if API key is available for premium sound,
    otherwise falls back to gTTS.
    """
    if not os.path.exists(folder):
        os.makedirs(folder)
        
    filename = f"response_{uuid.uuid4().hex}.mp3"
    filepath = os.path.join(folder, filename)
    
    from utils.db import get_setting
    api_key = get_setting("openai_api_key") or os.getenv("OPENAI_API_KEY")
    
    # Try OpenAI TTS for Professional "Alexa" feel
    if api_key and api_key != "your_openai_api_key_here":
        try:
            client = OpenAI(api_key=api_key)
            response = client.audio.speech.create(
                model="tts-1",
                voice="nova", # Professional "Alexa" like voice (Nova or Shimmer are good)
                input=text[:4000] # OpenAI limit
            )
            response.stream_to_file(filepath)
            return f"/static/audio/{filename}"
        except Exception as e:
            print(f"OpenAI TTS failed: {e}. Falling back to gTTS.")

    # Fallback to gTTS (Free/Basic)
    try:
        tts = gTTS(text=text, lang='en')
        tts.save(filepath)
        return f"/static/audio/{filename}"
    except Exception as e:
        print(f"Error in TTS fallback: {e}")
        return None
