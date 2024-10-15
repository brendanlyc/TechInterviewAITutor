from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from fastapi import HTTPException
from datetime import datetime, timedelta, UTC
from jose import JWTError, jwt
import configparser
import os

hasher = PasswordHasher()

# Load configuration
config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), '../../config.ini'))

SECRET_KEY = config['jwt']['SECRET_KEY']
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def hash_password(password: str) -> str:
    return hasher.hash(password)

def verify_password(hashed_password: str, password: str) -> bool:
    try:
        return hasher.verify(hashed_password,password)
    except VerifyMismatchError:
        return False
    
def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(UTC) + expires_delta
    else:
        expire = datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str) -> str:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms = [ALGORITHM])
        return int(payload.get('sub'))
    except jwt.JWTError:
        raise HTTPException(status_code=403, detail="Invalid or expired token")