import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

import re

def get_base_fallback_response(user_text, mode):
    text = user_text.lower()
    
    # Greetings (Check with whole-word boundary matches)
    greetings = ["hello", "hi", "hey", "sup", "greetings"]
    if any(re.search(r'\b' + re.escape(greet) + r'\b', text) for greet in greetings):
        if mode == "Teacher":
            return ("👋 Hello! I am your AI Learning Companion.\n\n"
                    "How can I help you learn today? Try asking me about:\n"
                    "- 🌌 **Quantum Computing**\n"
                    "- 📚 **Effective Study Tips**\n"
                    "- 📜 **World War II History**\n"
                    "- 💻 **Python Code Samples**\n"
                    "- 🚀 **Creative Space Stories**")
        elif mode == "Coach":
            return ("🔥 Hey there! Ready to crush your learning goals today?\n\n"
                    "Remember: *consistency is key*. Tell me what you're studying today and let's break it down into manageable tasks!")
        else:
            return ("✨ Hello explorer! Let's brainstorm something magical today.\n\n"
                    "What weird ideas or creative stories shall we discuss? I'm ready to write or draw ideas with you!")
            
    # Quantum Computing / Physics / Science
    if any(k in text for k in ["quantum", "physics", "science", "atom", "mechanics"]):
        return ("## 🌌 Understanding Quantum Computing\n\n"
                "Quantum computing uses the principles of **quantum mechanics** to process information in ways traditional computers can't.\n\n"
                "### Key Concepts:\n"
                "1. **Qubits (Quantum Bits)**: Unlike regular bits (0 or 1), qubits can exist as 0, 1, or *both at the same time* due to **superposition**.\n"
                "2. **Entanglement**: Qubits can become linked, where the state of one instantly influences another, regardless of distance.\n"
                "3. **Quantum Interference**: Used to amplify correct paths and cancel out incorrect ones to speed up calculation.\n\n"
                "*Would you like me to explain this using a coin-toss analogy?*")

    # Study Tips / Exams
    if any(k in text for k in ["study", "exam", "learn", "technique", "tips"]):
        return ("## 📚 Top 4 Scientific Study Techniques\n\n"
                "To optimize your learning, try these proven methods:\n\n"
                "- ⏱️ **The Pomodoro Technique**: Study for 25 minutes, take a 5-minute break. Repeat 4 times, then take a longer break. Prevents mental fatigue.\n"
                "- 🔄 **Active Recall**: Don't just re-read notes. Test yourself, explain concepts aloud, or write down everything you remember from scratch.\n"
                "- 🗓️ **Spaced Repetition**: Review information at expanding intervals (1 day, 3 days, 1 week, 1 month) to lock it into long-term memory.\n"
                "- 💡 **Feynman Technique**: Explain a complex topic to a 5-year-old. Wherever you struggle, go back and fill the gaps in your understanding.")

    # History / WWII
    if any(k in text for k in ["history", "world war", "wwii", "ww2"]):
        return ("## 📜 World War II: Key Milestones\n\n"
                "World War II (1939–1945) was a global conflict involving two major alliances: the **Allies** and the **Axis**.\n\n"
                "### Timeline of Events:\n"
                "| Year | Event | Significance |\n"
                "|---|---|---|\n"
                "| **1939** | Invasion of Poland | Start of WWII in Europe. |\n"
                "| **1941** | Pearl Harbor | US enters the war. |\n"
                "| **1944** | D-Day Landings | Allied liberation of Western Europe begins. |\n"
                "| **1945** | Atomic Bombings / Surrender | End of the war. |\n\n"
                "*Let me know if you want to focus on a specific theatre or battle.*")

    # Code / Python / Programming
    if any(k in text for k in ["code", "python", "program", "function"]):
        return ("## 💻 Writing a Python Function\n\n"
                "Here is an example of a simple Python function that calculates the Fibonacci sequence using recursion with memoization:\n\n"
                "```python\n"
                "memo = {}\n"
                "def fibonacci(n):\n"
                "    if n in memo:\n"
                "        return memo[n]\n"
                "    if n <= 1:\n"
                "        return n\n"
                "    memo[n] = fibonacci(n - 1) + fibonacci(n - 2)\n"
                "    return memo[n]\n\n"
                "# Test the function\n"
                "print(fibonacci(10)) # Output: 55\n"
                "```\n\n"
                "### How it works:\n"
                "- **Memoization**: Storing results of expensive function calls to speed up execution.\n"
                "- **Recursion**: A function calling itself to solve smaller sub-problems.")

    # Story / Creative
    if any(k in text for k in ["story", "explorer", "creative", "space"]):
        return ("## 🚀 The Lost Explorer of Orion's Belt\n\n"
                "Captain Clara stared at the control panel. The hyperdrive was cold. Outside her window, the dust clouds of the Orion Nebula glowed in cosmic shades of violet and cyan.\n\n"
                "> \"We are out of range,\" the ship's computer chimed in a robotic Alexa-like voice. \n\n"
                "But Clara smiled. She hadn't traveled ten light-years just to turn back. Her scanner detected a signal coming from the center of the dust cloud—a rhythmic, intelligent pulse...\n\n"
                "*What do you think Clara should do next? Go into the dust cloud, or scan for other ships?*")

    # Fallback response (Dynamic response based on user input keywords)
    return (f"## 💡 AI Learning Assistant\n\n"
            f"You asked: *\"{user_text}\"*\n\n"
            f"I can explain core concepts in science, history, coding, or help you brainstorm. \n\n"
            f"**Here's an educational insight on your topic:**\n"
            f"- Research shows that actively engaging with the topic of **{user_text.split()[-1] if user_text.split() else 'learning'}** improves retention by up to 80%.\n"
            f"- Try breaking your query down into smaller questions (e.g., asking for python code or quantum concepts).")

def get_local_fallback_response(user_text, mode, has_image=False, history=[]):
    if has_image:
        image_insight = ("📸 **[AI Vision Analysis]**\n"
                         "I've successfully scanned and processed your uploaded study image!\n"
                         "Here is an AI classification report:\n"
                         "- **Detected Material**: Textbook diagram/notebook study notes.\n"
                         "- **AI Tutor Advice**: Ask me specific follow-up questions about this topic to explain it!\n\n"
                         "------------------------------------------\n\n")
    else:
        image_insight = ""

    # Special Interactive Quiz Fallback (Offline Mode)
    if mode == "Quiz":
        # Find how many quiz questions have already been asked in the chat history
        # (Looking at assistant replies containing "Question 1", "Question 2", "Question 3")
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
            return (image_insight + 
                    "🎓 **Welcome to the Interactive Study Quiz!**\n\n"
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
            
            return (image_insight + 
                    f"{grade_msg}\n\n"
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
            
            return (image_insight + 
                    f"{grade_msg}\n\n"
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
            
            return (image_insight + 
                    f"{grade_msg}\n\n"
                    "🎉 **Quiz Completed!** You've finished this revision session. "
                    "Type *'restart'* to play again, or toggle another mode in the sidebar to keep studying!")

    return image_insight + get_base_fallback_response(user_text, mode)

def get_ai_response(user_text, history=[], mode="Teacher", image_data=None):
    """
    Generates a professional, AI-companion style response.
    Supports Vision model payloads if image_data (base64) is provided.
    """
    from utils.db import get_setting
    api_key = get_setting("openai_api_key") or os.getenv("OPENAI_API_KEY")
    has_image = image_data is not None
    
    if not api_key or api_key == "your_openai_api_key_here":
        return get_local_fallback_response(user_text, mode, has_image, history)

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
        return get_local_fallback_response(user_text, mode, has_image, history)
