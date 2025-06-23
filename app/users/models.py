from datetime import datetime
from typing import TYPE_CHECKING, List
from sqlalchemy import Column, String, Float
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.transactions.models import Transaction
    
def get_transaction_model():
    from app.transactions.models import Transaction
    return Transaction

class User(SQLModel, table=True):
    __tablename__ = "users"
    id: int = Field(default=None, primary_key=True)
    name: str = Field(sa_column=Column(String(50), nullable=False, unique=True))
    last_name: str = Field(sa_column=Column(String(50), nullable=False))
    age: int
    email: str = Field(sa_column=Column(String(50), nullable=False, unique=True))
    password: str = Field(sa_column=Column(String(250), nullable=False))
    country: str = Field(default=None)
    balance: float = Field(sa_column=Column(Float()))
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    transactions: List["Transaction"] = Relationship(back_populates="user")