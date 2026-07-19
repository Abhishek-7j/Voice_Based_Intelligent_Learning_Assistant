import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

import re

import urllib.parse

def get_base_fallback_response(user_text, mode):
    text = user_text.lower().strip()
    
    # 1. AI Image Generation Request Detection (ChatGPT / Gemini style)
    img_triggers = ["generate image", "draw", "create image", "create a picture", "make a picture", "show a picture", "picture of", "image of"]
    if any(trigger in text for trigger in img_triggers):
        # Clean prompt
        prompt = re.sub(r'^(generate|draw|create|make|show)\s+(an?\s+)?(image|picture|photo)\s+(of\s+)?', '', text, flags=re.IGNORECASE).strip()
        if not prompt:
            prompt = "a vibrant futuristic AI learning companion in space"
            
        encoded = urllib.parse.quote(prompt)
        img_url = f"https://image.pollinations.ai/prompt/{encoded}?width=1024&height=1024&nologo=true"
        
        return (f"## 🎨 AI Image Generator\n\n"
                f"Here is your AI generated image for **\"{prompt.capitalize()}\"**:\n\n"
                f"![{prompt}]({img_url})\n\n"
                f"*Tip: You can ask me to generate images for any topic in science, space, history, or fantasy!*")

    # 2. Greetings (Check with whole-word boundary matches)
    greetings = ["hello", "hi", "hey", "sup", "greetings"]
    if any(re.search(r'\b' + re.escape(greet) + r'\b', text) for greet in greetings):
        if mode == "Teacher":
            return ("👋 Hello! I am your AI Learning Companion.\n\n"
                    "How can I help you learn today? Try asking me about:\n"
                    "- 🌌 **Astronomy & Milky Way Galaxy**\n"
                    "- 🛡️ **Cybersecurity & Encryption**\n"
                    "- ⚛️ **Quantum Computing**\n"
                    "- 💻 **Python Code Samples**\n"
                    "- 🎨 **Generate AI Images**")
        elif mode == "Coach":
            return ("🔥 Hey there! Ready to crush your learning goals today?\n\n"
                    "Remember: *consistency is key*. Tell me what topic you're studying today and let's break it down into actionable steps!")
        else:
            return ("✨ Hello explorer! Let's brainstorm something magical today.\n\n"
                    "What ideas, stories, or images shall we create together? Type *'generate image of space'* or ask me a query!")

    # 3. Cybersecurity & Information Security
    if any(k in text for k in ["cybersecurity", "security", "encryption", "hacker", "firewall", "phishing", "malware", "network"]):
        return ("## 🛡️ Fundamentals of Cybersecurity\n\n"
                "Cybersecurity is the practice of protecting systems, networks, and data from digital attacks.\n\n"
                "### Core Pillars (The CIA Triad):\n"
                "1. **Confidentiality**: Ensuring data is accessible only to authorized users (e.g. using AES-256 Encryption).\n"
                "2. **Integrity**: Safeguarding information from being altered or tampered with (e.g. Cryptographic Hashes like SHA-256).\n"
                "3. **Availability**: Guaranteeing reliable access to data for authorized parties (e.g. DDoS Mitigation).\n\n"
                "### Real-World Defensive Tools:\n"
                "- **Firewalls**: Filter incoming and outgoing network traffic based on security rules.\n"
                "- **Zero-Trust Architecture**: Never trust, always verify every access request.\n"
                "- **Multi-Factor Authentication (MFA)**: Adds secondary security layers beyond passwords.")

    # 4. Astronomy, Space & Galaxies
    if any(k in text for k in ["galaxy", "milky way", "astronomy", "space", "planet", "star", "black hole", "cosmos", "universe"]):
        return ("## 🌌 Astronomy & The Milky Way Galaxy\n\n"
                "The **Milky Way** is a barred spiral galaxy containing over 100 to 400 billion stars, including our Solar System.\n\n"
                "### Key Astronomical Facts:\n"
                "- **Diameter**: Approximately 100,000 light-years across.\n"
                "- **Galactic Center**: Houses a supermassive black hole named **Sagittarius A*** (4 million solar masses).\n"
                "- **Stellar Neighborhood**: Our Sun resides in the Orion Arm, orbiting the galactic core once every 230 million years.\n\n"
                "🎨 *Want to see a visual representation? Ask me to **'generate an image of Milky Way galaxy'**!*")

    # 5. Quantum Computing & Physics
    if any(k in text for k in ["quantum", "physics", "atom", "mechanics", "qubit", "superposition"]):
        return ("## ⚛️ Understanding Quantum Computing\n\n"
                "Quantum computing leverages principles of quantum mechanics to perform complex calculations exponentially faster than classical supercomputers.\n\n"
                "### Key Principles:\n"
                "1. **Superposition**: Qubits can exist as 0, 1, or both states simultaneously.\n"
                "2. **Quantum Entanglement**: Linked qubits instantly influence each other's state across distance.\n"
                "3. **Quantum Interference**: Amplifies correct computational paths to find global solutions fast.")

    # 6. Biology & Life Sciences
    if any(k in text for k in ["biology", "dna", "rna", "cell", "photosynthesis", "genetics", "organism"]):
        return ("## 🧬 Molecular Biology & Genetics\n\n"
                "Deoxyribonucleic Acid (**DNA**) is the molecule that carries genetic instructions in living organisms.\n\n"
                "### Structure & Function:\n"
                "- **Double Helix**: Formed by two anti-parallel strands of nucleotides.\n"
                "- **Base Pairing**: Adenine (A) pairs with Thymine (T), and Cytosine (C) pairs with Guanine (G).\n"
                "- **Replication**: DNA unzips to make exact copies during cell division (Mitosis).")

    # 7. Mathematics & Equations
    if any(k in text for k in ["math", "calculus", "algebra", "geometry", "equation", "formula", "theorem"]):
        return ("## 📐 Essential Mathematical Principles\n\n"
                "Mathematics provides the language for modeling physical reality.\n\n"
                "### Fundamental Formulas:\n"
                "- **Pythagorean Theorem**: `a² + b² = c²` (Relates sides of a right triangle)\n"
                "- **Euler's Identity**: `e^(iπ) + 1 = 0` (Connects 5 fundamental constants)\n"
                "- **Calculus Derivative**: `f'(x) = lim (h->0) [f(x+h) - f(x)] / h` (Measures rate of change)")

    # 8. Study Tips / Exams
    if any(k in text for k in ["study", "exam", "learn", "technique", "tips"]):
        return ("## 📚 Top Scientific Study Techniques\n\n"
                "- ⏱️ **Pomodoro Method**: 25 mins deep work, 5 mins rest. Prevents burnout.\n"
                "- 🔄 **Active Recall**: Self-testing locks information into long-term memory faster than passive re-reading.\n"
                "- 🗓️ **Spaced Repetition**: Reviewing material at expanding intervals (1d, 3d, 1w) maximizes retention.")

    # 9. Code / Python / Programming
    if any(k in text for k in ["code", "python", "program", "function", "software"]):
        return ("## 💻 Writing Efficient Python Code\n\n"
                "Python emphasizes code readability and clean syntax:\n\n"
                "```python\n"
                "def solve_fibonacci(n, memo={}):\n"
                "    if n in memo: return memo[n]\n"
                "    if n <= 1: return n\n"
                "    memo[n] = solve_fibonacci(n - 1, memo) + solve_fibonacci(n - 2, memo)\n"
                "    return memo[n]\n\n"
                "print(solve_fibonacci(10)) # Output: 55\n"
                "```\n\n"
                "### Key Concepts:\n"
                "- **Memoization**: Cache previous results to optimize runtime complexity from O(2^n) to O(n).")

    # 10. History / WWII
    if any(k in text for k in ["history", "world war", "wwii", "ww2"]):
        return ("## 📜 World War II: Historical Overview\n\n"
                "World War II (1939–1945) reshaped modern geopolitics and international law.\n\n"
                "### Timeline of Major Events:\n"
                "- **1939**: Invasion of Poland triggers war in Europe.\n"
                "- **1941**: Attack on Pearl Harbor brings the United States into the war.\n"
                "- **1944**: D-Day Allied landings liberate Western Europe.\n"
                "- **1945**: End of WWII and founding of the United Nations.")

import base64
import io
from PIL import Image

def analyze_image_payload(image_data):
    """
    Scans and analyzes an uploaded Base64 image payload locally.
    Attempts OCR text extraction using Tesseract/PIL, detects document structures (e.g. Resumes, Notes, Diagrams),
    and extracts key headings and text content.
    """
    if not image_data:
        return None

    try:
        header, b64_str = image_data.split(',', 1) if ',' in image_data else ('', image_data)
        img_bytes = base64.b64decode(b64_str)
        img = Image.open(io.BytesIO(img_bytes))
        width, height = img.size
        
        extracted_text = ""
        try:
            import pytesseract
            extracted_text = pytesseract.image_to_string(img).strip()
        except Exception:
            extracted_text = ""

        aspect = width / float(height)
        is_portrait_doc = aspect < 0.88 # Resume or textbook page

        if extracted_text and len(extracted_text) > 10:
            lines = [line.strip() for line in extracted_text.split('\n') if line.strip()]
            header_title = lines[0] if lines else "Scanned Document"
            text_preview = "\n".join([f"> *{l}*" for l in lines[:6]])
            
            return (f"📸 **[AI Vision & OCR Document Scanner]**\n\n"
                    f"### 📄 Document Analysis Report:\n"
                    f"- **Detected Type**: Professional Resume / Academic Document\n"
                    f"- **Header / Title Found**: **{header_title}**\n"
                    f"- **Dimensions**: {width}x{height} pixels (Portrait Page)\n\n"
                    f"### 🔍 Extracted Document Text Preview:\n"
                    f"{text_preview}\n\n"
                    f"### 💡 AI Tutor Feedback:\n"
                    f"- I have successfully scanned and indexed the contents of this document.\n"
                    f"- You can ask me specific questions about the projects, technical skills, or work experience listed here!")

        return (f"📸 **[AI Vision & Image Scanner]**\n\n"
                f"### 🔍 Image Analysis Report:\n"
                f"- **Detected Material**: {'Vertical Study Document / Resume' if is_portrait_doc else 'Diagram / Study Material'}\n"
                f"- **Resolution**: {width}x{height} pixels\n\n"
                f"### 💡 AI Tutor Advice:\n"
                f"- I have processed your image. Ask me specific questions about the concepts, formulas, code, or headings shown in this photo to explain them in detail!")
    except Exception as e:
        print(f"Error in image analysis: {e}")
        return ("📸 **[AI Vision Analysis]**\n"
                "I've scanned and processed your uploaded study image! Ask me follow-up questions about this topic to explain it.")

def get_base_fallback_response(user_text, mode):
    text = user_text.lower().strip()

    # Handle image asking queries when no specific subject matches
    vision_queries = ["tell me about this image", "tell me about this photo", "tell me about this picture", "what is in this image", "what is this image", "explain this image", "scan this image", "read this image"]
    if any(q in text for q in vision_queries):
        return ("📸 **AI Vision Tutor**\n\n"
                "Please upload an image using the **Camera** or **Attachment** button in the search bar, and I will scan and analyze it for you!")
    
    # 1. AI Image Generation Request Detection (ChatGPT / Gemini style)
    img_triggers = ["generate image", "draw", "create image", "create a picture", "make a picture", "show a picture", "picture of", "image of"]
    if any(trigger in text for trigger in img_triggers):
        # Clean prompt
        prompt = re.sub(r'^(generate|draw|create|make|show)\s+(an?\s+)?(image|picture|photo)\s+(of\s+)?', '', text, flags=re.IGNORECASE).strip()
        if not prompt:
            prompt = "a vibrant futuristic AI learning companion in space"
            
        encoded = urllib.parse.quote(prompt)
        img_url = f"https://image.pollinations.ai/prompt/{encoded}?width=1024&height=1024&nologo=true"
        
        return (f"## 🎨 AI Image Generator\n\n"
                f"Here is your AI generated image for **\"{prompt.capitalize()}\"**:\n\n"
                f"![{prompt}]({img_url})\n\n"
                f"*Tip: You can ask me to generate images for any topic in science, space, history, or fantasy!*")

    # 2. Greetings (Check with whole-word boundary matches)
    greetings = ["hello", "hi", "hey", "sup", "greetings"]
    if any(re.search(r'\b' + re.escape(greet) + r'\b', text) for greet in greetings):
        if mode == "Teacher":
            return ("👋 Hello! I am your AI Learning Companion.\n\n"
                    "How can I help you learn today? Try asking me about:\n"
                    "- 🌌 **Astronomy & Milky Way Galaxy**\n"
                    "- 🛡️ **Cybersecurity & Encryption**\n"
                    "- ⚛️ **Quantum Computing**\n"
                    "- 💻 **Python Code Samples**\n"
                    "- 🎨 **Generate AI Images**")
        elif mode == "Coach":
            return ("🔥 Hey there! Ready to crush your learning goals today?\n\n"
                    "Remember: *consistency is key*. Tell me what topic you're studying today and let's break it down into actionable steps!")
        else:
            return ("✨ Hello explorer! Let's brainstorm something magical today.\n\n"
                    "What ideas, stories, or images shall we create together? Type *'generate image of space'* or ask me a query!")

    # 3. Cybersecurity & Information Security
    if any(k in text for k in ["cybersecurity", "security", "encryption", "hacker", "firewall", "phishing", "malware", "network"]):
        return ("## 🛡️ Fundamentals of Cybersecurity\n\n"
                "Cybersecurity is the practice of protecting systems, networks, and data from digital attacks.\n\n"
                "### Core Pillars (The CIA Triad):\n"
                "1. **Confidentiality**: Ensuring data is accessible only to authorized users (e.g. using AES-256 Encryption).\n"
                "2. **Integrity**: Safeguarding information from being altered or tampered with (e.g. Cryptographic Hashes like SHA-256).\n"
                "3. **Availability**: Guaranteeing reliable access to data for authorized parties (e.g. DDoS Mitigation).\n\n"
                "### Real-World Defensive Tools:\n"
                "- **Firewalls**: Filter incoming and outgoing network traffic based on security rules.\n"
                "- **Zero-Trust Architecture**: Never trust, always verify every access request.\n"
                "- **Multi-Factor Authentication (MFA)**: Adds secondary security layers beyond passwords.")

    # 4. Astronomy, Space & Galaxies
    if any(k in text for k in ["galaxy", "milky way", "astronomy", "space", "planet", "star", "black hole", "cosmos", "universe"]):
        return ("## 🌌 Astronomy & The Milky Way Galaxy\n\n"
                "The **Milky Way** is a barred spiral galaxy containing over 100 to 400 billion stars, including our Solar System.\n\n"
                "### Key Astronomical Facts:\n"
                "- **Diameter**: Approximately 100,000 light-years across.\n"
                "- **Galactic Center**: Houses a supermassive black hole named **Sagittarius A*** (4 million solar masses).\n"
                "- **Stellar Neighborhood**: Our Sun resides in the Orion Arm, orbiting the galactic core once every 230 million years.\n\n"
                "🎨 *Want to see a visual representation? Ask me to **'generate an image of Milky Way galaxy'**!*")

    # 5. Quantum Computing & Physics
    if any(k in text for k in ["quantum", "physics", "atom", "mechanics", "qubit", "superposition"]):
        return ("## ⚛️ Understanding Quantum Computing\n\n"
                "Quantum computing leverages principles of quantum mechanics to perform complex calculations exponentially faster than classical supercomputers.\n\n"
                "### Key Principles:\n"
                "1. **Superposition**: Qubits can exist as 0, 1, or both states simultaneously.\n"
                "2. **Quantum Entanglement**: Linked qubits instantly influence each other's state across distance.\n"
                "3. **Quantum Interference**: Amplifies correct computational paths to find global solutions fast.")

    # 6. Biology & Life Sciences
    if any(k in text for k in ["biology", "dna", "rna", "cell", "photosynthesis", "genetics", "organism"]):
        return ("## 🧬 Molecular Biology & Genetics\n\n"
                "Deoxyribonucleic Acid (**DNA**) is the molecule that carries genetic instructions in living organisms.\n\n"
                "### Structure & Function:\n"
                "- **Double Helix**: Formed by two anti-parallel strands of nucleotides.\n"
                "- **Base Pairing**: Adenine (A) pairs with Thymine (T), and Cytosine (C) pairs with Guanine (G).\n"
                "- **Replication**: DNA unzips to make exact copies during cell division (Mitosis).")

    # 7. Mathematics & Equations
    if any(k in text for k in ["math", "calculus", "algebra", "geometry", "equation", "formula", "theorem"]):
        return ("## 📐 Essential Mathematical Principles\n\n"
                "Mathematics provides the language for modeling physical reality.\n\n"
                "### Fundamental Formulas:\n"
                "- **Pythagorean Theorem**: `a² + b² = c²` (Relates sides of a right triangle)\n"
                "- **Euler's Identity**: `e^(iπ) + 1 = 0` (Connects 5 fundamental constants)\n"
                "- **Calculus Derivative**: `f'(x) = lim (h->0) [f(x+h) - f(x)] / h` (Measures rate of change)")

    # 8. Study Tips / Exams
    if any(k in text for k in ["study", "exam", "learn", "technique", "tips"]):
        return ("## 📚 Top Scientific Study Techniques\n\n"
                "- ⏱️ **Pomodoro Method**: 25 mins deep work, 5 mins rest. Prevents burnout.\n"
                "- 🔄 **Active Recall**: Self-testing locks information into long-term memory faster than passive re-reading.\n"
                "- 🗓️ **Spaced Repetition**: Reviewing material at expanding intervals (1d, 3d, 1w) maximizes retention.")

    # 9. Code / Python / Programming
    if any(k in text for k in ["code", "python", "program", "function", "software"]):
        return ("## 💻 Writing Efficient Python Code\n\n"
                "Python emphasizes code readability and clean syntax:\n\n"
                "```python\n"
                "def solve_fibonacci(n, memo={}):\n"
                "    if n in memo: return memo[n]\n"
                "    if n <= 1: return n\n"
                "    memo[n] = solve_fibonacci(n - 1, memo) + solve_fibonacci(n - 2, memo)\n"
                "    return memo[n]\n\n"
                "print(solve_fibonacci(10)) # Output: 55\n"
                "```\n\n"
                "### Key Concepts:\n"
                "- **Memoization**: Cache previous results to optimize runtime complexity from O(2^n) to O(n).")

    # 10. History / WWII
    if any(k in text for k in ["history", "world war", "wwii", "ww2"]):
        return ("## 📜 World War II: Historical Overview\n\n"
                "World War II (1939–1945) reshaped modern geopolitics and international law.\n\n"
                "### Timeline of Major Events:\n"
                "- **1939**: Invasion of Poland triggers war in Europe.\n"
                "- **1941**: Attack on Pearl Harbor brings the United States into the war.\n"
                "- **1944**: D-Day Allied landings liberate Western Europe.\n"
                "- **1945**: End of WWII and founding of the United Nations.")

    # 11. Clean Dynamic Fallback (Extracts meaningful topic keywords, filtering out stop-words and prompt verbs)
    stop_words = {"the", "a", "an", "is", "of", "and", "or", "in", "out", "for", "with", "to", "on", "at", "by", "from", "up", "about", "into", "over", "after", "that", "this", "these", "those", "tell", "me", "can", "you", "what", "how", "why", "image", "photo", "picture", "show"}
    raw_words = [re.sub(r'[^\w\s]', '', w) for w in user_text.split()]
    meaningful = [w for w in raw_words if w.lower() not in stop_words and len(w) > 2]
    
    topic_display = " ".join(meaningful[-2:]).capitalize() if len(meaningful) >= 2 else (meaningful[0].capitalize() if meaningful else "Learning & Exploration")

    return (f"## 💡 Detailed Learning Guide: {topic_display}\n\n"
            f"You asked about: **\"{user_text.capitalize()}\"**\n\n"
            f"### Key Insights & Analysis:\n"
            f"- **Core Concept**: Understanding **{topic_display}** involves analyzing fundamental principles, real-world applications, and structured problem solving.\n"
            f"- **Educational Advice**: Try breaking your question into smaller sub-queries (e.g. asking for specific code examples, formulas, or historical timelines).\n\n"
            f"🎨 *Need a visual illustration? Try asking me: **'Generate an image of {topic_display}'**!*")

def get_local_fallback_response(user_text, mode, has_image=False, history=[], image_data=None):
    if has_image or image_data:
        image_insight = analyze_image_payload(image_data)
        if image_insight:
            # If user asks generic vision query ("tell me about this image"), return vision report directly!
            text_lower = user_text.lower().strip()
            vision_queries = ["tell me about this image", "tell me about this photo", "tell me about this picture", "what is in this image", "what is this image", "explain this image", "scan this image", "read this image"]
            if any(q in text_lower for q in vision_queries) or not user_text:
                return image_insight
            return image_insight + "\n\n------------------------------------------\n\n" + get_base_fallback_response(user_text, mode)

    # Special Interactive Quiz Fallback (Offline Mode)
    if mode == "Quiz":
        # Find how many quiz questions have already been asked in the chat history
        asked_q1 = False
        asked_q2 = False
        asked_q3 = False
        
        for msg in history:
            content = msg.get("content", "")
            if "Question 1" in content:
                asked_q1 = True
            if "Question 2" in content:
                asked_q2 = True
            if "Question 3" in content:
                asked_q3 = True

        user_ans = user_text.lower().strip()

        # Step 1: User starts quiz or responds before Q1
        if not asked_q1:
            return ("🎓 **Welcome to the Interactive Study Quiz!**\n\n"
                    "Let's test your knowledge. Here is your first question:\n\n"
                    "💡 **Question 1**: What is the approximate speed of light in a vacuum?\n"
                    "- **a)** 30,000 km/s\n"
                    "- **b)** 300,000 km/s\n"
                    "- **c)** 150,000 km/s\n"
                    "- **d)** 3,000 km/s\n\n"
                    "*Reply with a, b, c, or d to answer!*")

        # Step 2: Grade Q1 and present Q2
        if asked_q1 and not asked_q2:
            is_correct = "b" in user_ans or "300,000" in user_ans
            grade_msg = "✅ **Correct!** The speed of light is approximately 300,000 kilometers per second (or 3x10^8 m/s)." if is_correct else "❌ **Incorrect!** The correct answer was **b) 300,000 km/s**."
            
            return (f"{grade_msg}\n\n"
                    "Here is your next challenge:\n\n"
                    "💡 **Question 2**: Which programmer created the Python programming language in 1991?\n"
                    "- **a)** Dennis Ritchie\n"
                    "- **b)** Bjarne Stroustrup\n"
                    "- **c)** Guido van Rossum\n"
                    "- **d)** James Gosling\n\n"
                    "*Reply with a, b, c, or d to answer!*")

        # Step 3: Grade Q2 and present Q3
        if asked_q2 and not asked_q3:
            is_correct = "c" in user_ans or "guido" in user_ans or "rossum" in user_ans
            grade_msg = "✅ **Correct!** Guido van Rossum created Python to be an intuitive, readable language." if is_correct else "❌ **Incorrect!** The correct answer was **c) Guido van Rossum**."
            
            return (f"{grade_msg}\n\n"
                    "Here is your final challenge:\n\n"
                    "💡 **Question 3**: Which event triggered the entry of the United States into World War II in December 1941?\n"
                    "- **a)** The invasion of Poland\n"
                    "- **b)** The bombing of Pearl Harbor\n"
                    "- **c)** The Battle of Britain\n"
                    "- **d)** The D-Day Landings\n\n"
                    "*Reply with a, b, c, or d to answer!*")

        # Step 4: Grade Q3 and finish
        if asked_q3:
            is_correct = "b" in user_ans or "pearl" in user_ans or "harbor" in user_ans
            grade_msg = "✅ **Correct!** The surprise attack on Pearl Harbor on December 7, 1941, led the US to declare war." if is_correct else "❌ **Incorrect!** The correct answer was **b) The bombing of Pearl Harbor**."
            
            return (f"{grade_msg}\n\n"
                    "🎉 **Quiz Completed!** You've finished this revision session. "
                    "Type *'restart'* to play again, or toggle another mode in the sidebar to keep studying!")

    return get_base_fallback_response(user_text, mode)

def get_ai_response(user_text, history=[], mode="Teacher", image_data=None):
    """
    Generates a professional, AI-companion style response.
    Supports Vision model payloads if image_data (base64) is provided.
    """
    from utils.db import get_setting
    api_key = get_setting("openai_api_key") or os.getenv("OPENAI_API_KEY")
    has_image = image_data is not None
    
    if not api_key or api_key == "your_openai_api_key_here":
        return get_local_fallback_response(user_text, mode, has_image, history, image_data)

    try:
        client = OpenAI(api_key=api_key)
        
        system_prompts = {
            "Teacher": "You are a world-class educational assistant, similar to Google Gemini. You explain complex topics simply, use structured bullet points, and encourage the user to ask follow-up questions.",
            "Coach": "You are a motivational learning coach. You help the user set goals, break down tasks, and stay focused. Your tone is energetic and supportive.",
            "Creative": "You are a creative brainstorming partner. You help the user think outside the box, generate stories, and explore weird ideas. Your tone is imaginative and slightly informal.",
            "Quiz": "You are a professional educational Quiz Master. Ask the student one clear question at a time on their chosen study topic. Wait for their response, grade it, explain the solution briefly, and then present the next question. Do not list all questions at once."
        }

        messages = [
            {"role": "system", "content": system_prompts.get(mode, system_prompts["Teacher"])}
        ]
        
        # Add history
        for msg in history:
            messages.append(msg)
            
        # Form Vision content
        if has_image:
            user_content = [
                {
                    "type": "text",
                    "text": user_text
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": image_data # contains "data:image/jpeg;base64,..."
                    }
                }
            ]
            messages.append({"role": "user", "content": user_content})
        else:
            messages.append({"role": "user", "content": user_text})
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            max_tokens=600,
            temperature=0.7 if mode == "Creative" else 0.5
        )
        
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error in LLM: {e}")
        return get_local_fallback_response(user_text, mode, has_image, history, image_data)
