from datetime import datetime

from db.config import get_conn
from auth.token import create_access_token, verify_token
from auth.session import session
from werkzeug.security import generate_password_hash, check_password_hash

now = datetime.now()

def get_user(token):
    with get_conn() as conn:
        cursor = conn.cursor()
        username = verify_token(token)
        
        user = cursor.execute(
            'SELECT * FROM users WHERE username = ?', 
            (username, )
        ).fetchone()
        
    return user

def validate_data(username, password):
    if username == '' and password == '':
        raise ValueError('Username and Password not valid')
    elif username == '':
        raise ValueError('Username not valid')
    elif password == '':
        raise ValueError('Password not valid')
    else:
        pass

def authenticate_user(username, password):
    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute(
            'SELECT id, username, password FROM users WHERE username = ?', 
            (username,)
        )
        user = cursor.fetchone()
        
        if user is None:
            raise ValueError("User not exits")
        
        check_password = check_password_hash(user[2], password)
        if not check_password:
            raise ValueError("Credentials invalid")
    
        token = create_access_token(user[1])
        
        cursor.execute(
            "UPDATE users SET jwt_token = ?, created_at = ? WHERE id = ?", 
            (token, now, user[0])
        )
        conn.commit()
        
        session.token = token
        session.username = user[1]
        session.save_session()
    return token

def register_user(username, password):
    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute(
            'SELECT id, username, password FROM users WHERE username = ?', 
            (username,)
        )
        user = cursor.fetchone()
        
        if user:
            raise ValueError("User exits")
        
        password_hash = generate_password_hash(password, "pbkdf2:sha256:30", 30)
        
        token = create_access_token(username)
        cursor.execute(
            'INSERT INTO users (username, password, jwt_token, created_at) VALUES(?,?,?,?)',
            (username, password_hash, token, now)
        )
        conn.commit()        
        
        session.token = token
        session.username = username
        session.save_session()
    return token

def logout_user(token):
    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE users SET jwt_token = NULL WHERE jwt_token = ?", 
            (token,)
        )
        conn.commit()
        
        session.delete_file_session()
    return True