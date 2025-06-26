import re
from typing import List, Optional
from pydantic import BaseModel, EmailStr, validator

from app.transactions.schemas import TransactionSchema

class NewUserSchema(BaseModel):
    name: str
    last_name: str
    age: Optional[int]
    email : EmailStr
    password: str
    country: Optional[str]
    balance: float

    @validator('password')
    def validate_password_length(cls, pass_:str):
        special_characters = set("-@#$%^&+=")
        if len(pass_) <= 7:
            raise ValueError("Password must contains 8 characters")
        if bool(re.match(r'^[A-Z]', pass_)) == False:
            raise ValueError("Password must start with capital letter")
        if not any(c in special_characters for c in pass_):
            raise ValueError("Password must include at least one special character like '@', '#', etc.")
        if not any(char.isdigit() for char in pass_):
            raise ValueError("Password must contain at least one digit")
        return pass_
        
    @validator('balance')
    def validate_balance(cls, bal:int):
        if bal <= 0:
            raise ValueError("Balance must be more than zero")
        return bal
        
    @validator("name")
    def name_no_specials(cls, val: str):
        if not val.replace(" ", "").isalpha():
            raise ValueError("El nombre solo debe contener letras")
        return val
        

class UserSchema(BaseModel):
    id: int
    name: str
    last_name: str
    age: Optional[int]
    email : EmailStr
    password: str
    country: Optional[str]
    balance: float
    # transactions: List[Transaction]

class UserSchemaWithTransactions(BaseModel):
    id: int
    name: str
    last_name: str
    age: Optional[int]
    email: EmailStr
    country: Optional[str]
    balance: float
    transactions: List[TransactionSchema] = []

    class Config:
        orm_mode = True