import secrets
from datetime import datetime, timedelta, timezone
from typing import Optional
import pyseto
from pyseto import Key
from passlib.context import CryptContext
from app.core.config import settings
import bcrypt
import json
pwd_context = CryptContext(
    schemes=["bcrypt"], 
    deprecated="auto",
    truncate_error=False 
)

# In production, this should be a fixed 32-character string in your .env
SECRET_KEY = settings.SECRET_KEY
token_key = Key.new(version=4, purpose="local", key=SECRET_KEY.encode())

def get_password_hash(password: str) -> str:
    """
    Direct implementation using the native bcrypt library.
    This bypasses passlib to resolve persistent length errors.
    """
    # 1. Convert string to bytes
    password_bytes = password.encode('utf-8')
    
    # 2. Handle the 72-byte hard limit manually for safety
    if len(password_bytes) > 72:
        password_bytes = password_bytes[:72]
        
    # 3. Generate salt and hash
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    
    # 4. Return as a string to store in the DB
    return hashed_password.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify using native bcrypt.
    """
    password_bytes = plain_password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    
    return bcrypt.checkpw(password_bytes, hashed_bytes)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(days=1))
    to_encode.update({"exp": expire.isoformat()})
    
    # Standardized PASETO V4 Local Encoding
    # Use pyseto.encode instead of Paseto.encode
    token = pyseto.encode(
        key=token_key, 
        payload=to_encode
    )
    
    return token.decode()
    

def verify_access_token(token: str):
    try:
        # NOTICE: It's 'keys=' with an 's' for decoding
        decoded = pyseto.decode(
            keys=token_key, 
            token=token,
            deserializer=json
        )
        return decoded.payload
    except Exception as e:
        return None