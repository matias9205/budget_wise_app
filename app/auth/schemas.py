from typing import Optional
from pydantic import BaseModel, EmailStr, Field

class NewAccessTokenSchema(BaseModel):
    sub: str
    username: str
    role: str

class UserLogin(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    email: EmailStr
    password:str
    country: Optional[str] = None
    balance: Optional[float] = None
    role: Optional[str] = None

class Token(BaseModel):
    access_token: str
    token_type: str

class UserTokenPayload(BaseModel):
    sub: int
    username: str
    role: str