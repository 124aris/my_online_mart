from jose import jwt, JWTError
from datetime import datetime, timedelta
from app import settings

def create_access_token(subject: str , expires_delta: timedelta) -> str:
    expire = datetime.utcnow() + expires_delta
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, str(settings.SECRET_KEY), algorithm = str(settings.ALGORITHM))
    return encoded_jwt

def decode_access_token(access_token: str):
    decoded_jwt = jwt.decode(access_token, str(settings.SECRET_KEY), algorithms = [str(settings.ALGORITHM)])
    return decoded_jwt