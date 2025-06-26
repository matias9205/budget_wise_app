from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING, List, Optional
from sqlalchemy import Column, String
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.transactions.models import Transaction
    
def get_transaction_model():
    from app.transactions.models import Transaction
    return Transaction

class Category(SQLModel, table=True):
    __tablename__ = "categories"
    id: int = Field(default=None, primary_key=True)
    name: str = Field(sa_column=Column(String(250), nullable=False, unique=True))
    transactions: List["Transaction"] = Relationship(back_populates="category")

    class Config:
        orm_mode = True