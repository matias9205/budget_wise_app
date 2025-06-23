from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING, Optional
from sqlalchemy import Column, Date, Float, String
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.users.models import User

def get_user_model():
    from app.users.models import User
    return User

class TransactionType(str, Enum):
    income = "income"
    expense = "expense"

class Transaction(SQLModel, table=True):
    __tablename__ = "transactions"
    id: int = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", nullable=False)
    concept: str = Field(sa_column=Column(String(50)))
    amount: float = Field(sa_column=Column(Float()))
    type: TransactionType = Field(default=TransactionType.income)
    category_id: int = Field(foreign_key="categories.id", nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)    
    user: Optional["User"] = Relationship(back_populates="transactions")
