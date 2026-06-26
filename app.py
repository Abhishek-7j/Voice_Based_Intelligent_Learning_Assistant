from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
import os
import uuid
from dotenv import load_dotenv
from utils.llm import get_ai_response
from utils.tts import text_to_speech
from utils.db import save_message, get_history, get_all_conversations, delete_conversation, init_db

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "learning-assistant-secret-key-2026")
CORS(app)

# Ensure DB is initialized
init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    user_text = data.get('text', '').strip()
    mode = data.get('mode', 'Teacher')
    conv_id = data.get('conversation_id') or str(uuid.uuid4())
    voice = data.get('voice', 'nova')
    
    if not user_text:
        return jsonify({'error': 'Empty message'}), 400

    # Get history from DB
    history = get_history(conv_id)
    
    # Get AI response
    ai_response_text = get_ai_response(user_text, history, mode)
    
    if "CONFIG_ERROR:" in ai_response_text:
        return jsonify({'error': 'configuration_needed', 'message': ai_response_text}), 401
    
    # Generate a title if it's new (using first message)
    title = user_text[:30] + '...' if len(user_text) > 30 else user_text
    
    # Save to DB
    save_message(conv_id, 'user', user_text, title, mode)
    save_message(conv_id, 'assistant', ai_response_text, title, mode)
    
    # Generate Audio
    audio_url = text_to_speech(ai_response_text)
    
    return jsonify({
        'response': ai_response_text,
        'audio_url': audio_url,
        'conversation_id': conv_id
    })

@app.route('/history', methods=['GET'])
def history():
    convs = get_all_conversations()
    return jsonify(convs)

@app.route('/history/<conv_id>', methods=['GET'])
def get_conv_history(conv_id):
    messages = get_history(conv_id)
    return jsonify(messages)

@app.route('/clear/<conv_id>', methods=['POST'])
def clear_one(conv_id):
    delete_conversation(conv_id)
    return jsonify({'status': 'deleted'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
