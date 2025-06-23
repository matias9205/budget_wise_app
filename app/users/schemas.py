from typing import List, Optional
from pydantic import BaseModel, EmailStr

from app.transactions.schemas import TransactionSchema

class NewUserSchema(BaseModel):
    name: str
    last_name: str
    age: Optional[int]
    email : EmailStr
    password: str
    country: Optional[str]
    balance: float

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