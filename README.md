# Voice-Based Intelligent Learning Assistant 🧠🎙️

A premium, interactive web application that allows users to learn any topic through voice and text. Powered by Google Gemini AI, Flask, and Web Speech AI.

## ✨ Features

- **Voice Interaction**: Record your voice directly in the browser.
- **Intelligent Responses**: Uses Google Gemini AI (gemini-2.5-flash / gemini-1.5-flash) to provide educational and concise answers.
- **Text-to-Speech (TTS)**: Automatically reads back answers using gTTS.
- **Modern UI**: Dark-themed, responsive design with glassmorphism and animations.
- **Chat History**: Maintains context during your learning session.

## 🛠️ Technology Stack

- **Backend**: Python, Flask
- **Frontend**: HTML5, CSS3 (Vanilla), JavaScript (ES6+)
- **AI/ML**: Google Gemini API (`google-genai`)
- **Voice**: Web Speech API (Input), gTTS (Output)

## 🚀 Installation & Setup

### 1. Prerequisite
- Python 3.8+ installed.
- A Google Gemini API Key.

### 2. Clone the Project
```bash
# In your terminal
cd Voice_Based_Intelligent_Learning_Assistant
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configuration
1. Create a `.env` file in the root directory (you can copy `.env.example`).
2. Add your Google Gemini API key:
   ```env
   GEMINI_API_KEY=your_actual_key_here
   SECRET_KEY=any_random_string
   ```

### 5. Run the Application
```bash
python app.py
```
Wait for the server to start, then open your browser at `http://127.0.0.1:5000`.

## 📂 Folder Structure

- `app.py`: Main Flask server and routes.
- `templates/`: HTML templates.
- `static/`: CSS, JS, and generated audio files.
- `utils/`: logic for AI (llm.py) and speech (tts.py).
- `requirements.txt`: Python package list.

## 📝 Usage Tips
- Click the **Microphone** icon to speak your question.
- Press **Enter** or click **Ask** to send text.
- Make sure to allow microphone permissions in your browser.
- The assistant is designed to be educational, so feel free to ask "Explain quantum physics like I'm five!"

## 📄 License
MIT License
