import os
import datetime
import sqlite3

from config import settings

def get_conn():
    return sqlite3.connect(settings.db_path)

def initialize_db():
    db_path = 'app.db'
    db_exists = os.path.exists(settings.db_path)
    
    if not db_exists:
        with get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    jwt_token TEXT,
                    created_at DATETIME,
                    updated_at DATETIME
                )
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title VARCHAR(50) NOT NULL,
                    content TEXT,
                    completed INTEGER,
                    created_at DATETIME,
                    updated_at DATETIME,
                    user_id INTEGER,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )
            ''')
        conn.commit()
