import time
from typing import Dict

import jwt
from config import config

from passlib.context import CryptContext

# JWT Verifications
JWT_SECRET = config.get("settings", "SECRET_KEY")
JWT_ALGORITHM = config.get("settings", "JWT_ALGO")
ACCESS_TOKEN_EXPIRE_MINUTES = int( config.get("settings", "ACCESS_TOKEN_EXPIRE_MINUTES") )

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def signJWT(username: str) -> Dict[str, str]:
    payload = {
        "username": username,
        "expires": time.time() + ACCESS_TOKEN_EXPIRE_MINUTES * 60
    }
    
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

def decodeJWT(token: bytes) -> dict:
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        return {}

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_user(req):
    auth = req.headers["Authorization"]
    scheme, credentials = auth.split()
    token = decodeJWT(credentials)
    return token