from datetime import datetime, timedelta
from typing import Annotated, Optional
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import JWTError, jwt
from starlette import status

from app.auth.schemas import NewAccessTokenSchema, UserTokenPayload

class Security:
    def __init__(self, secret_key: Optional[str]):
        self.SECRET_KEY = secret_key
        self.pwd_context = CryptContext(schemes=["bcrypt"], bcrypt__rounds=14, deprecated="auto")
        self.ALGORITHM = "HS256"
        self.ACCESS_TOKEN_EXPIRE_MINUTES = 30
        self.oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

    def hash_password(self, password:str) -> str:
        return self.pwd_context.hash(password)
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        print(f"REAL USER PASSWORDS VALIDATION: {self.pwd_context.verify(plain_password, hashed_password)}")
        return self.pwd_context.verify(plain_password, hashed_password)
    
    def create_access_token(self, data: NewAccessTokenSchema, expires_delta=timedelta(minutes=15)) -> str:
        print(f"PAYLOAD FOR ACCESS TOKEN: {data}")
        to_encode = {
            "sub": data.sub,
            "username": data.username,
            "role": data.role,
        }
        expire = datetime.utcnow() + (expires_delta or timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES))
        to_encode["exp"] = int(expire.timestamp())
        encoded_jwt = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_jwt
    
    def decode_token(self, token: str) -> UserTokenPayload:
        user = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
        print(f"DECODED PAYLOAD JSON: {user}")
        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token missing user_id")
        return user
    
    def get_oauth2_scheme(self):
        print(self.oauth2_scheme)
        return self.oauth2_scheme
    
    def get_current_user(self, token: str):
        try:
            user = self.decode_token(token)
            return user
        except Exception as e:
            print(f"Error in get_current_user: {e}")
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")