import json
from datetime import datetime, timedelta
from typing import Optional

from fastapi import HTTPException, status
from jose import jwt, JWTError
from passlib.context import CryptContext

from app.core.config import settings


class JWTUtils:
    def __init__(self, secret_key: str, algorithm: str):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    def create_token(self, subject: dict, expires_delta: Optional[timedelta] = None):
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode = {"exp": expire, "sub": json.dumps(subject)}
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt
    
    def verify_token(self, token: str):
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            subject = payload["sub"]
        except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        return subject
    
    def verify_password(self, plain_password: str, hashed_password: str):
        return self.pwd_context.verify(plain_password, hashed_password)
    
    def get_password_hash(self, password: str):
        return self.pwd_context.hash(password)


jwt_utils = JWTUtils(settings.SECRET_KEY, settings.ALGORITHM)
