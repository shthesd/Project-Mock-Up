from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import jwt, JWTError
from passlib.context import CryptContext
from app.core.config import settings

ALGORITHM = "HS256"
_pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(p: str) -> str:
    return _pwd.hash(p)

def verify_password(p: str, hp: str) -> bool:
    return _pwd.verify(p, hp)

def create_access_token(subject: str, expires_minutes: Optional[int] = None) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=expires_minutes or settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"sub": subject, "exp": expire}
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str):
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return None

