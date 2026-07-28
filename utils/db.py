import sqlite3
import os
from datetime import datetime

DB_PATH = 'conversations.db'

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    # Users table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            full_name TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    # Conversations table (Sidebar items)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS conversations (
            id TEXT PRIMARY KEY,
            user_id INTEGER DEFAULT 1,
            title TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            mode TEXT DEFAULT 'Teacher'
        )
    ''')
    # Try adding user_id column if table already existed without it
    try:
        conn.execute("ALTER TABLE conversations ADD COLUMN user_id INTEGER DEFAULT 1;")
    except Exception:
        pass

    # Messages table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            conversation_id TEXT NOT NULL,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (conversation_id) REFERENCES conversations (id)
        )
    ''')
    # Settings table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# --- User Account Management Queries ---
def create_user(email, password_hash, full_name):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (email, password_hash, full_name) VALUES (?, ?, ?)",
                       (email.lower().strip(), password_hash, full_name.strip()))
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()
        return user_id
    except sqlite3.IntegrityError:
        return None

def get_user_by_email(email):
    if not email:
        return None
    conn = get_db_connection()
    user = conn.execute("SELECT * FROM users WHERE LOWER(email) = LOWER(?)", (email.strip(),)).fetchone()
    conn.close()
    return dict(user) if user else None

def get_user_by_id(user_id):
    if not user_id:
        return None
    conn = get_db_connection()
    user = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    conn.close()
    return dict(user) if user else None


def get_setting(key, default=None):
    conn = get_db_connection()
    res = conn.execute("SELECT value FROM settings WHERE key = ?", (key,)).fetchone()
    conn.close()
    if res:
        return res['value']
    return default

def set_setting(key, value):
    conn = get_db_connection()
    conn.execute("INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)", (key, value))
    conn.commit()
    conn.close()

def save_message(conv_id, role, content, title="New Conversation", mode="Teacher", user_id=1):
    conn = get_db_connection()
    
    # Ensure conversation exists
    res = conn.execute("SELECT id FROM conversations WHERE id = ?", (conv_id,)).fetchone()
    if not res:
        conn.execute("INSERT INTO conversations (id, user_id, title, mode) VALUES (?, ?, ?, ?)", 
                     (conv_id, user_id or 1, title, mode))
    
    # Save message
    conn.execute("INSERT INTO messages (conversation_id, role, content) VALUES (?, ?, ?)", 
                 (conv_id, role, content))
    
    conn.commit()
    conn.close()

def get_history(conv_id):
    conn = get_db_connection()
    rows = conn.execute("SELECT role, content FROM messages WHERE conversation_id = ? ORDER BY timestamp ASC", (conv_id,)).fetchall()
    conn.close()
    return [{"role": r['role'], "content": r['content']} for r in rows]

def get_all_conversations(user_id=None):
    conn = get_db_connection()
    if user_id:
        rows = conn.execute("SELECT * FROM conversations WHERE user_id = ? OR user_id = 1 OR user_id IS NULL ORDER BY created_at DESC", (user_id,)).fetchall()
    else:
        rows = conn.execute("SELECT * FROM conversations ORDER BY created_at DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def delete_conversation(conv_id):
    conn = get_db_connection()
    conn.execute("DELETE FROM messages WHERE conversation_id = ?", (conv_id,))
    conn.execute("DELETE FROM conversations WHERE id = ?", (conv_id,))
    conn.commit()
    conn.close()

# Always run init_db to ensure settings and users tables exist
init_db()

