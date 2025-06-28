from typing import List, Optional
from pydantic import BaseModel, EmailStr, validator

from app.roles.models import Role
from app.roles.schemas import RoleSchema
from app.transactions.schemas import TransactionSchema
from app.utils.schemas_validation import ValidateSchema

class NewUserSchema(BaseModel):
    name: str
    age: Optional[int]
    email : EmailStr
    password: str
    country: Optional[str]
    balance: float
    role: str

    @validator('password')
    def validate_password(cls, value: str):
        return ValidateSchema.validate_password_length(value)
        
    @validator('balance')
    def validate_balance_(cls, value):
        return ValidateSchema().validate_balance(value)
        
    @validator("name")
    def validate_name(cls, value: str):
        return ValidateSchema().name_no_specials(value)

class UserSchemaWithTransactions(BaseModel):
    name: str
    age: Optional[int]
    email: EmailStr
    country: Optional[str]
    role: Optional[RoleSchema]
    balance: float
    transactions: List[TransactionSchema] = []

class UpdateUser(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    country: Optional[str] = None
    balance: Optional[float] = None
    role: Optional[str] = None