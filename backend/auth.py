from datetime import datetime, timedelta
from typing import Optional
import jwt
from pydantic import BaseModel
import os

SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class TokenData(BaseModel):
    username: str
    exp: datetime

class User(BaseModel):
    username: str
    email: Optional[str] = None
    is_active: bool = True

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> Optional[TokenData]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            return None
        return TokenData(username=username, exp=datetime.fromtimestamp(payload.get("exp")))
    except jwt.InvalidTokenError:
        return None

def get_user(username: str) -> Optional[User]:
    # This will be replaced with database lookup in Phase 2
    # For now, return mock users
    if username == "admin":
        return User(username="admin", email="admin@localhost")
    return None
