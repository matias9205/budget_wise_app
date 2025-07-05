from datetime import datetime, timedelta
from typing import Annotated, Optional
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import jwt
from starlette import status

from app.auth.schemas import NewAccessTokenSchema

class Security:
    def __init__(self, secret_key: str):
        self.SECRET_KEY = secret_key
        self.pwd_context = CryptContext(schemes=["bcrypt"], bcrypt__rounds=14, deprecated="auto")
        self.ALGORITHM = "HS256"
        self.ACCESS_TOKEN_EXPIRE_MINUTES = 30
        self.oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

    def hash_password(self, password:str) -> str:
        return self.pwd_context.hash(password)
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        print(f"REAL USER PASSWORDS VALIDATION: {self.pwd_context.verify(plain_password, hashed_password)}")
        return self.pwd_context.verify(plain_password, hashed_password)
    
    def create_access_token(self, data: NewAccessTokenSchema, expires_delta = timedelta(minutes=15)) -> str:
        print(f"PAYLOAD FOR ACCESS TOKEN: {data}")
        to_encode = data.copy()
        expire = datetime.utcnow() + (expires_delta or timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES))
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_jwt
    
    def decode_token(self, token):
        print(f"TOKEN IN DECODE_TOKEN(): {token}")
        return jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
    
    def get_current_user(self):
        return self._get_user
    
    def _get_user(self, token: str = Depends()):
        print(f"TOKEN FOR DECODE: {token}") 
        user = self.decode_token(token)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user