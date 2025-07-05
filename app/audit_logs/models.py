from typing import TYPE_CHECKING, Optional
from sqlalchemy import Column, String, Text
from sqlmodel import Field, Relationship, SQLModel
from enum import Enum
from datetime import datetime

if TYPE_CHECKING:
    from app.users.models import User

def get_user_model():
    from app.users.models import User
    return User

class Actions(str, Enum):
    create = "Create"
    update = "Update"
    delete = "Delete"
    sign_up = "SignUp"
    login = "Login"
    logout = "Logout"

class TargetType(str, Enum):
    auth = "Auth"
    users = "Users"
    transactions = "Transactions"
    categories = "Categories"

class AuditLog(SQLModel, table=True):
    __tablename__ = "audit_logs"
    id: int = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", nullable=False)
    action: Actions = Field(default=None)
    target_type: TargetType = Field(default=None)
    details: str = Field(sa_column=Column(Text()))
    ip_address: str = Field(sa_column=Column(String(20), nullable=False))
    created_at: datetime = Field(default_factory=datetime.utcnow)
    user: "User" = Relationship(back_populates="audit_log")

    class Config:
        orm_mode = True