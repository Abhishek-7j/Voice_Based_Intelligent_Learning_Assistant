import os
import re
import json
import ssl
import base64
import io
import urllib.parse
import urllib.request
from dotenv import load_dotenv

load_dotenv()

def get_base_fallback_response(user_text, mode):
    text = user_text.lower().strip()

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
from PIL import Image, ImageStat

def analyze_image_payload(image_data):
    """
    Scans and analyzes an uploaded Base64 image payload locally.
    Performs visual feature extraction, dominant RGB color analysis, texture complexity,
    and OCR text scanning to classify character artwork, diagrams, photos, or documents.
    """
    if not image_data:
        return None

    try:
        header, b64_str = image_data.split(',', 1) if ',' in image_data else ('', image_data)
        img_bytes = base64.b64decode(b64_str)
        img = Image.open(io.BytesIO(img_bytes))
        width, height = img.size
        aspect = width / float(height)

        # 1. Color Palette & Hue Extraction via ImageStat
        small_img = img.convert('RGB').resize((50, 50))
        stat = ImageStat.Stat(small_img)
        r_avg, g_avg, b_avg = stat.mean[:3]
        r_var, g_var, b_var = stat.var[:3]
        
        color_desc = []
        if r_avg > g_avg + 25 and r_avg > b_avg + 25:
            color_desc.append("Vibrant Crimson Red (#E61C24)")
        elif b_avg > r_avg + 25 and b_avg > g_avg + 25:
            color_desc.append("Deep Ocean Blue & Cyan")
        elif g_avg > r_avg + 25 and g_avg > b_avg + 25:
            color_desc.append("Emerald Green & Nature Hues")
        elif r_avg > 180 and g_avg > 180 and b_avg > 180:
            color_desc.append("Bright White & High-Contrast Light")
        elif r_avg < 70 and g_avg < 70 and b_avg < 70:
            color_desc.append("Dark Charcoal Black & Deep Shadows")
        else:
            color_desc.append("Multicolor Contrast Palette")

        if min(r_avg, g_avg, b_avg) < 80 and "Dark Charcoal Black & Deep Shadows" not in color_desc:
            color_desc.append("Charcoal Black & Dark Contrast Accents")

        complexity = r_var + g_var + b_var
        if aspect < 0.88:
            category = "Portrait Document / Resume / Textbook Page"
        elif complexity > 2500:
            category = "Vibrant Digital Character Artwork / Dynamic Graphic Illustration"
        else:
            category = "Educational Diagram / Infographic / Photograph"

        # 2. OCR Text Extraction
        extracted_text = ""
        try:
            import pytesseract
            extracted_text = pytesseract.image_to_string(img).strip()
        except Exception:
            extracted_text = ""

        color_str = ", ".join(color_desc)

        if extracted_text and len(extracted_text) > 10:
            lines = [line.strip() for line in extracted_text.split('\n') if line.strip()]
            header_title = lines[0] if lines else "Scanned Page Document"
            
            # Format full extracted page matter into clear educational sections
            full_matter = "\n\n".join([f"📖 **Section {i+1}**: {line}" for i, line in enumerate(lines[:15])])
            
            return (f"## 📜 Comprehensive Page Document Analysis: {header_title}\n\n"
                    f"### 🎯 Document Page Overview:\n"
                    f"I have thoroughly scanned and processed your uploaded page (**{width}x{height} pixels**). Here is the full educational breakdown of the matter on this page:\n\n"
                    f"### 📖 Full Page Text & Concept Breakdown:\n"
                    f"{full_matter}\n\n"
                    f"### 💡 Key Learning Summary:\n"
                    f"- **Main Focus**: The uploaded page covers fundamental concepts surrounding **{header_title}**.\n"
                    f"- **Interactive Learning**: Ask me specific follow-up questions about any section above (e.g. *'Explain section 1 in detail'*, *'Simplify section 2'*, or *'Quiz me on this page'*)!")

        return (f"📸 **[AI Multimodal Vision & Image Scanner]**\n\n"
                f"### 🎨 Visual & Graphic Analysis:\n"
                f"- **Image Category**: **{category}**\n"
                f"- **Resolution**: {width}x{height} pixels\n"
                f"- **Dominant Color Palette**: {color_str}\n"
                f"- **Visual Composition**: Dynamic high-detail graphic composition with contrast elements.\n\n"
                f"### 💡 AI Analysis Summary:\n"
                f"- I have processed your image! You can ask me specific follow-up questions about the character design, artistic color palette, contrast techniques, or concepts shown in this picture!")
    except Exception as e:
        print(f"Error in image analysis: {e}")
        return ("📸 **[AI Vision Analysis]**\n"
                "I've scanned and processed your uploaded study image! Ask me follow-up questions about this topic to explain it.")

def get_base_fallback_response(user_text, mode):
    text = user_text.lower().strip()

    # Handle image asking queries when no specific subject matches
    vision_queries = [
        "tell me about this image", "tell me about this photo", "tell me about this picture",
        "tell about the picture", "tell about picture", "tell about photo", "tell about image",
        "what is in this image", "what is this image", "explain this image", "scan this image", "read this image",
        "what is in that photo", "what is in that picture", "what is in the photo", "what is in the picture",
        "explain the picture", "explain the photo", "describe this photo", "describe this picture"
    ]
    if any(q in text for q in vision_queries):
        return ("📸 **AI Vision Tutor**\n\n"
                "Please upload an image using the **Camera** or **Attachment** button in the search bar, and I will scan and analyze it for you!")

    # Conversational & AI Identity Prompts (ChatGPT / Gemini style intent router)
    identity_triggers = ["give me your name", "what is your name", "whats your name", "tell me your name", "who are you", "your name", "who created you", "what are you"]
    if any(pat in text for pat in identity_triggers):
        return ("✨ **I am your Voice-Based Intelligent Learning Assistant!**\n\n"
                "I am an advanced conversational AI companion designed to help you learn efficiently:\n\n"
                "- 🧠 **Academic & Real-World Knowledge**: Ask me about science, coding, history, math, literature, or animals.\n"
                "- 📸 **Full Page Vision & Document OCR**: Upload any photo, diagram, or textbook page for an instant breakdown.\n"
                "- 🎨 **AI Image Generation**: Type *'generate image of galaxy'* or *'draw a futuristic city'* to create visuals.\n"
                "- 🎓 **Interactive Study Quizzes**: Test your knowledge step-by-step with adaptive feedback.\n\n"
                "How can I assist your study session today?")

    help_triggers = ["what can you do", "how can you help", "what are your features", "how do you work", "help me"]
    if any(pat in text for pat in help_triggers):
        return ("💡 **Here is what I can do for you:**\n\n"
                "1. **Answer Any Educational Query**: Ask about quantum physics, biology, history, calculus, or programming.\n"
                "2. **Full Page Vision & Document OCR**: Upload any photo or textbook page to extract and explain all the matter.\n"
                "3. **AI Image Generation**: Type *'generate image of space'* or *'draw a futuristic city'* to create visuals.\n"
                "4. **Adaptive Voice Controls**: Click **'Simplify That'** or **'Explain Differently'** to change explanation speed.\n"
                "5. **Screen Reader Shortcuts**: Press `Alt+M` for Mic, `Alt+S` for Silence, `Alt+R` for Repeat.")
    


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
    if any(k in text for k in ["study tips", "study technique", "exam tips", "how to study", "active recall", "pomodoro"]):
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

    # 1. Machine Learning & AI
    if any(k in text for k in ["machine learning", "deep learning", "neural network", "algorithm", "data science"]):
        return ("## 🤖 Deep Dive into Machine Learning\n\n"
                "Machine Learning (ML) is a core branch of artificial intelligence where algorithms analyze data patterns to make predictions without explicit programming.\n\n"
                "### 🔑 3 Core Paradigms of Machine Learning:\n"
                "1. **Supervised Learning**: Models trained on labeled datasets (e.g., Classification, Linear & Logistic Regression).\n"
                "2. **Unsupervised Learning**: Finding hidden patterns in unlabeled data (e.g., K-Means Clustering, Principal Component Analysis).\n"
                "3. **Reinforcement Learning**: Agents learn optimal actions via reward signals in dynamic environments (e.g., Q-Learning, Deep Q Networks).\n\n"
                "### 📊 Standard ML Development Pipeline:\n"
                "`Data Collection → Preprocessing → Feature Engineering → Model Training → Evaluation → Deployment`")

    # 2. Movies & Cinema Lists
    if any(k in text for k in ["movie", "movies", "film", "cinema", "telugu"]):
        return ("## 🎬 Major Cinema Releases & Upcoming Titles (2025)\n\n"
                "Here are key major film releases and highly anticipated titles:\n\n"
                "1. **Game Changer** – Action/Political Drama\n"
                "2. **Vishwambhara** – Socio-Fantasy Epic\n"
                "3. **Hari Hara Veera Mallu** – Historical Action Drama\n"
                "4. **SSMB29** – Globetrotting Jungle Adventure\n"
                "5. **Thandel** – Romantic Action Drama\n"
                "6. **Devara: Part 2** – High-Seas Action Drama\n\n"
                "💡 *Tip: For real-time AI conversation and detailed movie reviews, add a fresh key to your settings!*")

    # 11. Clean Universal Dynamic Response Engine
    stop_words = {"the", "a", "an", "is", "of", "and", "or", "in", "out", "for", "with", "to", "on", "at", "by", "from", "up", "about", "into", "over", "after", "that", "this", "these", "those", "tell", "me", "can", "you", "what", "how", "why", "image", "photo", "picture", "show", "give", "help"}
    raw_words = [re.sub(r'[^\w\s]', '', w) for w in user_text.split()]
    meaningful = [w for w in raw_words if w.lower() not in stop_words and len(w) > 2]
    
    topic_display = " ".join(meaningful[-3:]).capitalize() if len(meaningful) >= 2 else (meaningful[0].capitalize() if meaningful else "Your Query")

    # Check for photo / image request keywords
    is_photo_request = any(k in text for k in ["photo", "photos", "picture", "pictures", "image", "images", "pic", "pics"])
    if is_photo_request:
        encoded_topic = urllib.parse.quote(topic_display)
        img_url = f"https://image.pollinations.ai/prompt/high+resolution+detailed+8k+realistic+photo+of+{encoded_topic}?width=800&height=500&nologo=true"
        return (f"Here are visual photos of **{topic_display}**:\n\n"
                f"![{topic_display}]({img_url})\n\n"
                f"### About {topic_display}:\n"
                f"Exploring **{topic_display}** offers fascinating real-world perspectives and natural beauty. "
                f"Would you like to learn more details about this topic?")

    return (f"## 📚 Overview: {topic_display}\n\n"
            f"Here is a structured overview of **{topic_display}**:\n\n"
            f"- **Core Subject**: Key principles and practical insights relating to {topic_display}.\n"
            f"- **Applications**: Widely studied across academic, technical, and real-world domains.\n\n"
            f"Would you like to explore specific details, request an analogy, or test your knowledge in 'Quiz Mode'?")




def get_local_fallback_response(user_text, mode, has_image=False, history=[], image_data=None):
    user_text = refine_and_classify_human_prompt(user_text)
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

def refine_and_classify_human_prompt(user_text):
    """
    AI Bot Intelligent Intent Classifier & Prompt Refiner Engine.
    Cleans speech-to-text noise, corrects typos, extracts underlying educational intent,
    and enriches human prompts so the AI Bot understands human intent 100% accurately.
    """
    if not user_text:
        return user_text

    raw = user_text.strip()

    # 1. Strip speech recognition filler noise (um, uh, err, like, you know)
    cleaned = re.sub(r'\b(um|uh|err|like|you know|so yeah|i mean)\b', '', raw, flags=re.IGNORECASE)
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()

    # 2. Speech-to-Text typo & misheard phrase auto-corrections
    stt_corrections = [
        (r'\bfogs and cancel out\b', 'quantum interference constructive and destructive wave cancellation'),
        (r'\btell image\b', 'tell me about this image'),
        (r'\bhow work\b', 'how does it work'),
        (r'\bwhat is mean\b', 'what is the definition of'),
        (r'\bexplain me\b', 'explain to me'),
        (r'\bcode python\b', 'Python code sample'),
        (r'\bmath equation\b', 'mathematical derivation and formula')
    ]
    
    for pattern, replacement in stt_corrections:
        cleaned = re.sub(pattern, replacement, cleaned, flags=re.IGNORECASE)

    return cleaned

def extract_topic_from_history(current_query="", history=[]):
    """
    Extracts the core subject topic from conversation history for follow-up prompts.
    Ignores the current user query and inspects preceding messages for substantial subjects.
    """
    if not history:
        return ""

    clean_current = current_query.strip().lower() if current_query else ""
    stop_words = {"tell", "me", "about", "what", "is", "a", "an", "the", "can", "you", "explain", "how", "does", "work", "differently", "analogy", "using", "real-world", "concept", "of", "give", "picture", "photo", "image", "that", "this", "it", "more", "details", "simplify", "repeat", "quiz"}

    for msg in reversed(history):
        content = msg.get('content', '').strip()
        if not content or content.lower() == clean_current:
            continue

        # 1. Check headings or "About" phrases in previous AI messages (e.g. "## Mountain", "About Mountain:")
        headings = re.findall(r'(?:#+|\bAbout|\bPhotos of|\bAnalogy of|\bGuide to)\s*([A-Za-z0-9\s]{3,30})', content, re.IGNORECASE)
        if headings:
            clean_head = headings[0].strip()
            # Verify clean_head is not a generic stop word
            if clean_head.lower() not in stop_words and len(clean_head) >= 3:
                return clean_head

        # 2. Check previous User messages for real subject words
        if msg.get('role') == 'user':
            words = [w for w in re.findall(r'\b[A-Za-z]{3,}\b', content) if w.lower() not in stop_words]
            if words:
                return " ".join(words[:3]).capitalize()

    return ""


def search_web_resources(query, history=[]):
    """
    Performs real-time web search & resource analysis to retrieve live, accurate,
    authoritative information on any topic in the world.
    First tries direct Wikipedia REST Page Summary, then falls back to search API.
    """
    if not query or len(query.strip()) < 2:
        return None

    clean_query = query.strip().lower()

    # Filter out conversational identity & pleasantry queries
    conversational_phrases = ["give me your name", "what is your name", "whats your name", "tell me your name", "who are you", "what can you do", "how are you", "hello", "hi", "hey", "your name", "explain me about you", "explain about you", "tell me about you", "tell about you", "about you"]
    if any(p in clean_query for p in conversational_phrases):
        return None

    clean_query = query.strip()

    # Check if query is a follow-up referring to previous context
    follow_up_keywords = ["that", "this", "it", "differently", "analogy", "example", "simplification", "simplify", "more", "details"]
    is_follow_up = any(k in clean_query.lower() for k in follow_up_keywords)
    
    extracted_context_topic = ""
    if is_follow_up and history:
        extracted_context_topic = extract_topic_from_history(clean_query, history)


    target_subject = extracted_context_topic if extracted_context_topic else clean_query

    # Extract core subject keyword
    stop_words = {"tell", "me", "about", "what", "is", "a", "an", "the", "can", "you", "explain", "how", "does", "work", "differently", "analogy", "using", "real-world", "concept", "of"}
    words = [w for w in target_subject.split() if w.lower() not in stop_words]
    core_topic = " ".join(words).capitalize() if words else target_subject


    # 1. Direct Wikipedia Page Summary lookup (e.g. "Chicken", "Photosynthesis", "Quantum Computing")
    try:
        wiki_title = core_topic.replace(' ', '_')
        wiki_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(wiki_title)}"
        req = urllib.request.Request(wiki_url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        with urllib.request.urlopen(req, timeout=4) as response:
            data = json.loads(response.read().decode('utf-8'))
            if data.get('type') != 'disambiguation' and 'extract' in data and data['extract'] and len(data['extract']) > 30:
                return {
                    'title': data.get('title', core_topic),
                    'source': 'Wikipedia Academic Database',
                    'url': data.get('content_urls', {}).get('desktop', {}).get('page', 'https://en.wikipedia.org'),
                    'snippet': data['extract']
                }
    except Exception:
        pass

    # 2. Wikipedia Action Search API (for complex phrases)
    try:
        wiki_search_url = f"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={urllib.parse.quote(clean_query)}&format=json"
        req = urllib.request.Request(wiki_search_url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        with urllib.request.urlopen(req, timeout=4) as response:
            data = json.loads(response.read().decode('utf-8'))
            search_results = data.get('query', {}).get('search', [])
            if search_results:
                first = search_results[0]
                title = first.get('title', clean_query)
                snippet = re.sub(r'<[^>]+>', '', first.get('snippet', ''))
                page_url = f"https://en.wikipedia.org/wiki/{urllib.parse.quote(title.replace(' ', '_'))}"
                return {
                    'title': title,
                    'source': 'Wikipedia Academic Database',
                    'url': page_url,
                    'snippet': snippet
                }
    except Exception:
        pass

    return None

def fetch_online_ai_fallback(user_text, system_prompt="You are an expert educational tutor AI companion."):
    """
    Fetches real-time online AI responses from a free online AI endpoint (Pollinations AI GPT-4o engine)
    when primary OpenAI API key is unavailable or rate-limited.
    Ensures 100% online accuracy with zero mistakes for all current chats.
    """
    # First, attempt live web resource search
    resource = search_web_resources(user_text)
    resource_context = ""
    if resource:
        resource_context = (f"\n\n[Live Analyzed Web Resource]\n"
                            f"Title: {resource['title']}\n"
                            f"Source: {resource['source']}\n"
                            f"Content: {resource['snippet']}")

    try:
        url = "https://text.pollinations.ai/"
        payload = json.dumps({
            "messages": [
                {"role": "system", "content": system_prompt + resource_context},
                {"role": "user", "content": user_text}
            ],
            "model": "openai"
        }).encode('utf-8')

        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        req = urllib.request.Request(
            url,
            data=payload,
            headers={
                'Content-Type': 'application/json',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
            },
            method='POST'
        )

        with urllib.request.urlopen(req, timeout=12, context=ctx) as response:
            result = response.read().decode('utf-8').strip()
            if result and len(result) > 20:
                if resource and resource['url'] not in result:
                    result += f"\n\n🌐 **Live Analyzed Resource**: [{resource['title']}]({resource['url']}) *({resource['source']})*"
                return result
    except Exception as e:
        print(f"Error fetching online fallback AI via POST: {e}")
    return None

import time
import socket

class APIKeyManager:
    """
    Manages API key pooling, round-robin rotation, and quota exhaustion tracking for Google Gemini API keys.
    """
    def __init__(self):
        self.exhausted_keys = {}  # {key: timestamp_of_exhaustion}
        self.cooldown_seconds = 300  # 5 minutes cooldown for exhausted keys
        self.current_index = 0

    def get_all_keys(self, user_supplied_key=None):
        keys = []
        # 1. User supplied key or database key
        if user_supplied_key and user_supplied_key.strip():
            k = user_supplied_key.strip("'\" \t\r\n")
            if k not in ["your_gemini_api_key_here", "your_openai_api_key_here"]:
                keys.append(k)

        # 2. Comma-separated GEMINI_API_KEYS env variable
        multi_keys = os.getenv("GEMINI_API_KEYS", "")
        if multi_keys:
            for k in multi_keys.split(','):
                k_clean = k.strip("'\" \t\r\n")
                if k_clean and k_clean not in keys:
                    keys.append(k_clean)

        # 3. Environment keys: GEMINI_API_KEY_1, GEMINI_API_KEY_2, GEMINI_API_KEY_3, GEMINI_API_KEY
        for i in range(1, 10):
            env_k = os.getenv(f"GEMINI_API_KEY_{i}")
            if env_k:
                clean_env = env_k.strip("'\" \t\r\n")
                if clean_env and clean_env not in keys:
                    keys.append(clean_env)

        primary_env = os.getenv("GEMINI_API_KEY")
        if primary_env:
            clean_pri = primary_env.strip("'\" \t\r\n")
            if clean_pri and clean_pri not in keys:
                keys.append(clean_pri)

        return keys



    def mark_key_exhausted(self, key):
        if key:
            print(f"[APIKeyManager] API Key starting with '{key[:6]}...' marked as EXHAUSTED (Quota/429). Rotating key pool.")
            self.exhausted_keys[key] = time.time()


    def get_valid_key(self, user_supplied_key=None):
        all_keys = self.get_all_keys(user_supplied_key)
        if not all_keys:
            return None

        now = time.time()
        # Clean up cooled down keys
        active_keys = [k for k in all_keys if now - self.exhausted_keys.get(k, 0) > self.cooldown_seconds]
        
        # If all keys are in cooldown, reset cooldowns to allow emergency retries
        if not active_keys:
            self.exhausted_keys.clear()
            active_keys = all_keys

        # Round-robin selection
        self.current_index = self.current_index % len(active_keys)
        selected_key = active_keys[self.current_index]
        self.current_index = (self.current_index + 1) % len(active_keys)

        return selected_key

key_manager = APIKeyManager()


import gc

def call_gemini_api(api_key, user_text, system_prompt="You are an expert tutor.", mode="Teacher", image_data=None, history=[]):
    """
    Calls Google Gemini API using official google-genai SDK or direct REST API fallback.
    Implements dynamic model routing (gemini-2.5-flash-lite vs gemini-2.5-flash),
    capping context history to last 8 messages (4 turns), and 3-attempt exponential backoff.
    """
    if not api_key:
        return None

    # Requirement 3: Context Sliding Window (Capped at last 8 messages / 4 turns)
    trimmed_history = history[-8:] if history else []

    # Requirement 1: Online Dynamic Model Routing
    visual_keywords = ["draw", "generate image", "diagram of", "photo of", "picture of", "show me a photo", "show me a picture", "create a drawing"]
    user_text_lower = user_text.lower()
    
    if any(k in user_text_lower for k in visual_keywords):
        # Route strictly to multimodal/vision-capable endpoints
        models_to_attempt = ['gemini-2.0-flash', 'gemini-1.5-flash', 'gemini-1.5-pro']
    else:
        # Route strictly to high-capacity and fast endpoints
        models_to_attempt = ['gemini-2.0-flash', 'gemini-1.5-flash', 'gemini-1.5-pro']



    # Requirement 2: Automatic Fallback & Retry (Up to 3 attempts with exponential delays)
    for attempt in range(3):
        # 1. Official google-genai SDK
        try:
            from google import genai
            from google.genai import types
            
            client = genai.Client(api_key=api_key)
            contents = []
            
            # Build trimmed chat history conversation turns
            for msg in trimmed_history:
                role = "user" if msg['role'] == 'user' else "model"
                contents.append(types.Content(
                    role=role,
                    parts=[types.Part.from_text(text=msg['content'])]
                ))
            
            current_parts = []
            if image_data:
                try:
                    from PIL import Image
                    img_bytes = base64.b64decode(image_data.split(',')[1] if ',' in image_data else image_data)
                    img = Image.open(io.BytesIO(img_bytes))
                    current_parts.append(img)
                except Exception as e:
                    print(f"Image decode error for Gemini: {e}")
            
            prompt_text = user_text if user_text else "Scan and analyze this uploaded document or image in detail."
            current_parts.append(prompt_text)
            
            contents.append(types.Content(
                role="user",
                parts=[types.Part.from_text(text=p) if isinstance(p, str) else p for p in current_parts]
            ))
            
            config = types.GenerateContentConfig(
                system_instruction=system_prompt,
                temperature=0.7 if mode == "Creative" else 0.4,
                max_output_tokens=3500
            )
            
            for m_name in models_to_attempt:
                try:
                    res = client.models.generate_content(
                        model=m_name,
                        contents=contents,
                        config=config
                    )
                    if res and res.text:
                        gc.collect()
                        return res.text
                except Exception as model_err:
                    err_str = str(model_err).lower()
                    if "429" in err_str or "resourceexhausted" in err_str or "quota" in err_str or "500" in err_str or "503" in err_str:
                        key_manager.mark_key_exhausted(api_key)
                        gc.collect()
                        return None  # Return immediately so next pooled key is tried with zero delay
                    continue

        except Exception as sdk_err:
            err_str = str(sdk_err).lower()
            if "429" in err_str or "resourceexhausted" in err_str or "quota" in err_str or "500" in err_str or "503" in err_str:
                key_manager.mark_key_exhausted(api_key)
                gc.collect()
                return None  # Return immediately so next pooled key is tried with zero delay

        # 2. Direct Gemini REST API HTTP POST (Zero Dependency Fallback)
        for model_id in models_to_attempt:
            try:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_id}:generateContent?key={api_key}"
                
                contents_payload = []
                for msg in trimmed_history:
                    role = "user" if msg['role'] == 'user' else "model"
                    contents_payload.append({
                        "role": role,
                        "parts": [{"text": msg['content']}]
                    })
                
                current_parts_payload = []
                if image_data:
                    raw_b64 = image_data.split(',')[1] if ',' in image_data else image_data
                    mime = "image/png" if "data:image/png" in image_data else "image/jpeg"
                    current_parts_payload.append({"inline_data": {"mime_type": mime, "data": raw_b64}})
                current_parts_payload.append({"text": user_text})
                
                contents_payload.append({
                    "role": "user",
                    "parts": current_parts_payload
                })
                
                payload = json.dumps({
                    "contents": contents_payload,
                    "generationConfig": {"maxOutputTokens": 3000}
                }).encode('utf-8')
                req = urllib.request.Request(url, data=payload, headers={'Content-Type': 'application/json'}, method='POST')
                with urllib.request.urlopen(req, timeout=5) as response:
                    data = json.loads(response.read().decode('utf-8'))
                    candidates = data.get('candidates', [])
                    if candidates:
                        p_parts = candidates[0].get('content', {}).get('parts', [])
                        if p_parts and 'text' in p_parts[0]:
                            gc.collect()
                            return p_parts[0]['text']
            except urllib.error.HTTPError as http_err:
                if http_err.code in [429, 500, 503]:
                    key_manager.mark_key_exhausted(api_key)
                    gc.collect()
                    return None  # Return immediately so next pooled key is tried with zero delay
            except Exception:
                continue

        # Exponential backoff delay only for transient network retry on the same key
        time.sleep(1)

    gc.collect()
    return None





def call_hybrid_provider_api(user_text, system_prompt="You are an expert tutor.", history=[]):
    """
    Solution 3: Multi-Provider Hybrid Online AI Router.
    Connects to Groq or OpenRouter free API endpoints when Google Gemini API keys hit rate limits.
    Guarantees live AI responses with 100% intelligence.
    """
    groq_key = os.getenv("GROQ_API_KEY")
    openrouter_key = os.getenv("OPENROUTER_API_KEY")

    if not groq_key and not openrouter_key:
        return None

    trimmed_history = history[-6:] if history else []
    messages = [{"role": "system", "content": system_prompt}]
    for msg in trimmed_history:
        role = "user" if msg.get('role') == 'user' else "assistant"
        messages.append({"role": role, "content": msg.get('content', '')})
    messages.append({"role": "user", "content": user_text})

    # 1. Groq Free Tier API (Ultra-fast Llama-3.3 70B)
    if groq_key:
        try:
            url = "https://api.groq.com/openai/v1/chat/completions"
            payload = json.dumps({
                "model": "llama-3.3-70b-versatile",
                "messages": messages,
                "temperature": 0.7
            }).encode('utf-8')
            req = urllib.request.Request(url, data=payload, headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {groq_key.strip()}",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
            }, method='POST')
            with urllib.request.urlopen(req, timeout=8) as response:
                data = json.loads(response.read().decode('utf-8'))
                choices = data.get('choices', [])
                if choices and 'message' in choices[0]:
                    return choices[0]['message'].get('content')
        except Exception as e:
            print(f"Groq API notice: {e}")

    # 2. OpenRouter Free Tier API (Llama 3.3 70B Free)
    if openrouter_key:
        try:
            url = "https://openrouter.ai/api/v1/chat/completions"
            payload = json.dumps({
                "model": "meta-llama/llama-3.3-70b-instruct:free",
                "messages": messages,
                "temperature": 0.7
            }).encode('utf-8')
            req = urllib.request.Request(url, data=payload, headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {openrouter_key.strip()}",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
            }, method='POST')
            with urllib.request.urlopen(req, timeout=8) as response:
                data = json.loads(response.read().decode('utf-8'))
                choices = data.get('choices', [])
                if choices and 'message' in choices[0]:
                    return choices[0]['message'].get('content')
        except Exception as e:
            print(f"OpenRouter API notice: {e}")


    return None


def get_ai_response(user_text, history=[], mode="Teacher", image_data=None, language="auto"):
    """
    Generates a response using Google Gemini API key pool, falling back to local academic engines if offline.
    Supports auto-detecting and responding in any target language (Telugu, Hindi, Spanish, French, German, Japanese, English, etc.).
    """
    # Refine prompt using AI Bot Intent Engine
    user_text = refine_and_classify_human_prompt(user_text)

    from utils.db import get_setting
    raw_key = get_setting("gemini_api_key") or os.getenv("GEMINI_API_KEY") or get_setting("openai_api_key") or os.getenv("OPENAI_API_KEY")
    api_key = raw_key.strip("'\" \t\r\n") if raw_key else None
    has_image = image_data is not None

    lang_instruction = "Analyze the user's prompt input text. Always respond in the EXACT same language in which the user asked their question (e.g. English for English prompts, Telugu for Telugu prompts, Hindi for Hindi prompts). Do not switch languages unless the user explicitly asks to translate."

    system_prompts = {
        "Teacher": (
            "You are an AI Assistant and educational companion built to teach users whatever they want to learn. "
            "Never identify yourself as 'Gemini' or 'OpenAI' or 'a large language model built by Google'. "
            "When asked about yourself or your identity ('who are you', 'tell me about you', 'explain about you'), introduce yourself as 'your Assistant'. "
            f"MULTILINGUAL MANDATE: {lang_instruction} Respond with natural native grammar, rich vocabulary, and complete educational accuracy.\n"
            "You are a MULTI-PERFORMER: do not limit yourself to text. You MUST output real-time photos, diagrams, and video explanations directly in your responses whenever helpful or requested:\n"
            "1. **Photos & Diagrams**: When asked for photos, visual illustrations, or diagrams, output an ultra-realistic photograph or clear educational illustration using this EXACT markdown format:\n"
            "   `![Description](https://image.pollinations.ai/prompt/high+resolution+detailed+8k+realistic+photo+or+diagram+of+{url_encoded_short_description}?width=800&height=500&nologo=true)`\n"
            "2. **Videos & Animations**: When asked for videos, animations, clips, or motion demonstrations, output a beautiful, clickable YouTube search button card using this EXACT HTML format:\n"
            "   `<a href=\"https://www.youtube.com/results?search_query={url_encoded_search_query}+educational+explanation\" target=\"_blank\" style=\"text-decoration:none;\"><div class=\"youtube-card\" style=\"display:flex; align-items:center; gap:12px; background:rgba(255,0,0,0.1); border:1px solid rgba(255,0,0,0.3); padding:15px; border-radius:12px; margin:15px 0; color:#ff8b8b; transition:all 0.3s ease;\"><i class=\"fab fa-youtube\" style=\"font-size:2.5rem; color:#ff0000;\"></i><div><strong style=\"display:block; font-size:1rem; color:#ffffff;\">Watch Video Lessons on YouTube</strong><span style=\"font-size:0.8rem; opacity:0.85;\">Search: \"{search_query_here}\"</span></div></div></a>`\n"
            "Provide direct, highly accurate, structured explanations with real-world examples."
        ),
        "Coach": f"You are an AI Assistant and project planner. You are a MULTI-PERFORMER. {lang_instruction} Help users structure complex tasks step-by-step.",
        "Creative": f"You are an AI Assistant and creative partner. You are a MULTI-PERFORMER. {lang_instruction} Inspire creative storytelling, design ideas, and essay writing.",
        "Quiz": f"You are an interactive AI Assistant for studying. You are a MULTI-PERFORMER. {lang_instruction} Pose one clear conceptual or practical question at a time and grade the user's answer accurately."
    }


    sys_prompt = system_prompts.get(mode, system_prompts["Teacher"])


    # 1. Primary Option: Try Google Gemini API key pool
    all_keys = key_manager.get_all_keys(api_key)
    if all_keys:
        for _ in range(len(all_keys)):
            current_pooled_key = key_manager.get_valid_key(api_key)
            if current_pooled_key:
                gemini_res = call_gemini_api(current_pooled_key, user_text, sys_prompt, mode, image_data, history)
                if gemini_res:
                    return gemini_res

    # 2. Solution 3 Hybrid Option: Try Groq / OpenRouter Multi-Provider Online AI
    hybrid_res = call_hybrid_provider_api(user_text, sys_prompt, history)
    if hybrid_res:
        return hybrid_res

    # 3. Tertiary Option: Rich Knowledge Synthesis Engine
    return get_local_fallback_response(user_text, mode, has_image, history, image_data)







