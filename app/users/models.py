from datetime import datetime
from typing import TYPE_CHECKING, List, Optional
from sqlalchemy import Column, Integer, String, Float
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.transactions.models import Transaction
    from app.roles.models import Role
    from app.audit_logs.models import AuditLog
    
def get_transaction_model():
    from app.transactions.models import Transaction
    return Transaction

def get_role_model():
    from app.roles.models import Role
    return Role

def get_audit_log_model():
    from app.audit_logs.models import AuditLog
    return AuditLog

class User(SQLModel, table=True):
    __tablename__ = "users"
    id: int = Field(default=None, primary_key=True)
    name: str = Field(sa_column=Column(String(50), nullable=False, unique=True))
    age: int = Field(sa_column=Column(Integer()))
    email: str = Field(sa_column=Column(String(50), nullable=False, unique=True))
    password: str = Field(sa_column=Column(String(250), nullable=False))
    role_id: int = Field(foreign_key="roles.id", nullable=False)
    country: str = Field(default=None)
    balance: float = Field(sa_column=Column(Float()))
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    transactions: List["Transaction"] = Relationship(back_populates="user")
    role: Optional["Role"] = Relationship(back_populates="user")
    audit_log: List["AuditLog"] = Relationship(back_populates="user")

    class Config:
        orm_mode = True