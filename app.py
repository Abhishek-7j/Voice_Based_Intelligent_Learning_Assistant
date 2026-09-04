from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_cors import CORS
import os
import uuid
from dotenv import load_dotenv
from utils.llm import get_ai_response
from utils.tts import text_to_speech
from utils.auth import hash_password, verify_password
from utils.db import (
    save_message, get_history, get_all_conversations, delete_conversation, 
    init_db, get_setting, set_setting, create_user, get_user_by_email, get_user_by_id
)

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "learning-assistant-secret-key-2026")
CORS(app)

# Ensure DB is initialized
init_db()

# --- Authentication Routes ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        user = get_user_by_email(email)
        if user and verify_password(password, user['password_hash']):
            session['user_id'] = user['id']
            session['user_email'] = user['email']
            session['user_name'] = user['full_name']
            return redirect(url_for('index'))
        return render_template('login.html', error="Invalid email address or password. Please try again!")
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        full_name = request.form.get('full_name', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        
        if not email or not password or not full_name:
            return render_template('signup.html', error="All fields are required!")
        
        if get_user_by_email(email):
            return render_template('signup.html', error="An account with this email address already exists.")
        
        pwd_hash = hash_password(password)
        user_id = create_user(email, pwd_hash, full_name)
        if user_id:
            session['user_id'] = user_id
            session['user_email'] = email
            session['user_name'] = full_name
            return redirect(url_for('index'))
        return render_template('signup.html', error="Could not create account. Please try again.")
    return render_template('signup.html')

@app.route('/demo_login', methods=['POST'])
def demo_login():
    guest_email = "guest@assistant.ai"
    user = get_user_by_email(guest_email)
    if not user:
        pwd_hash = hash_password("demo1234")
        user_id = create_user(guest_email, pwd_hash, "Guest Evaluator")
        user = get_user_by_id(user_id)
    
    session['user_id'] = user['id']
    session['user_email'] = user['email']
    session['user_name'] = user['full_name']
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/settings/api_key', methods=['GET'])
def get_api_key_status():
    key = get_setting('gemini_api_key') or os.getenv("GEMINI_API_KEY") or get_setting('openai_api_key') or os.getenv("OPENAI_API_KEY")
    configured = False
    masked = ""
    if key and key not in ["your_gemini_api_key_here", "your_openai_api_key_here"]:
        configured = True
        masked = key[:8] + "..." + key[-4:] if len(key) > 12 else "Configured"
    return jsonify({'configured': configured, 'masked': masked, 'provider': 'Gemini'})

@app.route('/settings/api_key', methods=['POST'])
def save_api_key():
    data = request.json
    key = data.get('api_key', '').strip()
    if not key:
        return jsonify({'error': 'API key cannot be empty'}), 400
    set_setting('gemini_api_key', key)
    return jsonify({'status': 'success', 'message': 'Gemini API Key updated successfully'})

@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({'status': 'alive', 'app': 'Assistant'})

@app.route('/sync', methods=['POST'])
def sync_data():
    try:
        user_id = session.get('user_id', 1)
        data = request.json or {}
        conversations = data.get('conversations', [])
        settings = data.get('settings', {})
        
        # Restore settings if server DB was reset
        for k, v in settings.items():
            if v and not get_setting(k):
                set_setting(k, v)
                
        # Restore conversations & messages if server DB was reset
        for conv in conversations:
            conv_id = conv.get('id')
            title = conv.get('title', 'Restored Session')
            mode = conv.get('mode', 'Teacher')
            messages = conv.get('messages', [])
            
            if conv_id and messages:
                for msg in messages:
                    role = msg.get('role')
                    content = msg.get('content')
                    if role and content:
                        save_message(conv_id, role, content, title, mode, user_id=user_id)
                        
        return jsonify({'status': 'synced', 'count': len(conversations)})
    except Exception as e:
        print(f"Error syncing client data: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/generate_image', methods=['POST'])
def generate_image_route():
    data = request.json or {}
    prompt = data.get('prompt', '').strip()
    if not prompt:
        return jsonify({'error': 'Prompt is required'}), 400
    
    import urllib.parse
    encoded = urllib.parse.quote(prompt)
    img_url = f"https://image.pollinations.ai/prompt/{encoded}?width=1024&height=1024&nologo=true"
    
    return jsonify({
        'status': 'success',
        'image_url': img_url,
        'prompt': prompt,
        'response': f"## 🎨 AI Image Generator\n\nHere is your generated image for **\"{prompt.capitalize()}\"**:\n\n![{prompt}]({img_url})"
    })

@app.route('/manifest.json')
def manifest():
    return app.send_static_file('manifest.json')

@app.route('/')
def index():
    if not session.get('user_id'):
        return redirect(url_for('login'))
    return render_template('index.html', user_name=session.get('user_name', 'Student'), user_email=session.get('user_email', ''), user_id=session.get('user_id', 1))

@app.route('/ask', methods=['POST'])
def ask():
    try:
        if not session.get('user_id'):
            return jsonify({'error': 'unauthorized', 'message': 'Please login to ask questions'}), 401
            
        user_id = session.get('user_id', 1)
        data = request.json or {}
        user_text = data.get('text', '').strip()
        mode = data.get('mode', 'Teacher')
        conv_id = data.get('conversation_id') or str(uuid.uuid4())
        voice = data.get('voice', 'nova')
        image_data = data.get('image_data') # base64 string
        language = data.get('language', 'auto')
        
        if not user_text:
            return jsonify({'error': 'Empty message'}), 400

        # Get history from DB
        history = get_history(conv_id, user_id=user_id)
        
        # Get AI response
        ai_response_text = get_ai_response(user_text, history, mode, image_data, language)
        if not ai_response_text:
            from utils.llm import get_base_fallback_response
            ai_response_text = get_base_fallback_response(user_text, mode)
        
        if isinstance(ai_response_text, str) and "CONFIG_ERROR:" in ai_response_text:
            return jsonify({'error': 'configuration_needed', 'message': ai_response_text}), 401

        
        # Generate a title if it's new (using first message)
        title = user_text[:30] + '...' if len(user_text) > 30 else user_text
        
        # Save to DB
        save_message(conv_id, 'user', user_text, title, mode, user_id=user_id)
        save_message(conv_id, 'assistant', ai_response_text, title, mode, user_id=user_id)
        
        # Generate Audio (guaranteed non-blocking & fast)
        audio_url = text_to_speech(ai_response_text, language=language)
        
        return jsonify({
            'response': ai_response_text,
            'audio_url': audio_url,
            'conversation_id': conv_id
        })
    except Exception as e:
        print(f"Unhandled error in /ask route: {e}")
        return jsonify({
            'response': "I encountered a momentary issue processing your request. Please try asking your question again!",
            'audio_url': None,
            'conversation_id': data.get('conversation_id') if 'data' in locals() else None
        }), 200

@app.route('/history', methods=['GET'])
def history():
    user_id = session.get('user_id', 1)
    convs = get_all_conversations(user_id=user_id)
    return jsonify(convs)

@app.route('/history/<conv_id>', methods=['GET'])
def get_conv_history(conv_id):
    user_id = session.get('user_id', 1)
    messages = get_history(conv_id, user_id=user_id)
    return jsonify(messages)

@app.route('/clear/<conv_id>', methods=['POST'])
def clear_one(conv_id):
    user_id = session.get('user_id', 1)
    delete_conversation(conv_id, user_id=user_id)
    return jsonify({'status': 'deleted'})


if __name__ == '__main__':
    app.run(debug=True, port=5000)

