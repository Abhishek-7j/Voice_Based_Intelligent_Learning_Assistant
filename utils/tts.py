import os
import re
from gtts import gTTS
from openai import OpenAI
from dotenv import load_dotenv
import uuid

load_dotenv()

def clean_text_for_speech(text):
    """
    Cleans response text for TTS to ensure pure, natural human voice output.
    Completely strips out image markdown tags (![alt](url)), bracketed headers,
    small icons, emojis, and structural labels so TTS reads only natural educational text.
    """
    if not text:
        return ""

    clean = text

    # 1. Remove markdown image tags ![alt](url) and links [text](url)
    clean = re.sub(r'!\[[^\]]*\]\([^)]+\)', '', clean)
    clean = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', clean)

    # 2. Remove bracketed headers and meta tags like [AI Vision Analysis], [AI Image Generator]
    clean = re.sub(r'\[[^\]]*\]', '', clean)

    # 3. Remove structural intro labels and screen tags
    meta_patterns = [
        r'📸\s*\*?\*?AI Vision Analysis\*?\*?',
        r'Here is an AI classification report:?',
        r'##\s*💡\s*AI Learning Assistant',
        r'##\s*💡\s*Learning Assistant.*',
        r'You asked:\s*\*?"[^"]*"\*?',
        r'I can explain core concepts in science, history, coding, or help you brainstorm\.?',
        r'\*?\*?Here\'s an educational insight on your topic:\*?\*?',
        r'-\s*\*?\*?Detected Material\*?\*?:?',
        r'-\s*\*?\*?AI Tutor Advice\*?\*?:?',
        r'🎓\s*\*?\*?Welcome to the Interactive Study Quiz!\*?\*?',
        r'Reply with a, b, c, or d to answer!?',
        r'Need a visual illustration\?.*',
        r'Tip: You can ask me to generate images.*'
    ]

    for pattern in meta_patterns:
        clean = re.sub(pattern, '', clean, flags=re.IGNORECASE)

    # 4. Remove markdown formatting symbols (*, #, `, _, ~, |)
    clean = re.sub(r'#{1,6}\s*', '', clean)
    clean = re.sub(r'\*\*|__|\*|_|~~|`', '', clean)
    clean = re.sub(r'\|', ' ', clean)

    # 5. Remove list bullet symbols at line starts
    clean = re.sub(r'^\s*[-\*\+]\s+', '', clean, flags=re.MULTILINE)
    clean = re.sub(r'^\s*\d+\.\s+', '', clean, flags=re.MULTILINE)

    # 6. Remove HTML tags
    clean = re.sub(r'<[^>]*>', '', clean)

    # 7. Remove all emojis and small icons so voice never reads icons out loud
    clean = re.sub(r'[\u2600-\u27BF]|[\uE000-\uF8FF]|\uD83C[\uDC00-\uDFFF]|\uD83D[\uDC00-\uDFFF]|[\u2011-\u26FF]|\uD83E[\uDD10-\uDDFF]', '', clean)

    # 8. Collapse whitespace and trim
    clean = re.sub(r'\s+', ' ', clean).strip()

    return clean

def text_to_speech(text, folder='static/audio'):
    """
    Converts text to speech using gTTS (Google Text-to-Speech).
    Operates 100% keyless with zero API key dependencies and zero quota limits.
    """
    if not os.path.exists(folder):
        os.makedirs(folder)
        
    filename = f"response_{uuid.uuid4().hex}.mp3"
    filepath = os.path.join(folder, filename)
    
    # Clean text to prevent reading symbols out loud
    cleaned_text = clean_text_for_speech(text)
    if not cleaned_text:
        cleaned_text = "I have generated a response for you."
    
    # Primary Keyless gTTS Speech Generator
    try:
        tts = gTTS(text=cleaned_text[:2500], lang='en')
        tts.save(filepath)
        return f"/static/audio/{filename}"
    except Exception as e:
        print(f"Error in keyless gTTS generation: {e}")
        return None
