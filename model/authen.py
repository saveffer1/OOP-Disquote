
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, Request
from typing import Optional
import jwt
from dataclasses import dataclass
from . import EmailStr

@dataclass
class TokenData:
    secret: str
    algorithm: str = "HS256"

    def create_access_token(self, data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret, algorithm=self.algorithm)
        return encoded_jwt
    
    def decode_access_token(self, token: str):
        payload = jwt.decode(token, self.secret, algorithms=[self.algorithm])
        email: EmailStr = payload.get("sub")
        return email
