import jwt
from jwt.exceptions import InvalidTokenError
from datetime import datetime

from config import settings


def create_access_token(username):
    payload = {"sub": username, "iat": datetime.utcnow()}
    return jwt.encode(payload, settings.secret_key_jwt, algorithm=settings.algorithm)

def verify_token(token):
    try:
        payload = jwt.decode(token, settings.secret_key_jwt, algorithms=[settings.algorithm])
        return payload.get('sub')
    except jwt.InvalidTokenError:
        return None