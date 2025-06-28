from typing import TYPE_CHECKING, Optional
from sqlalchemy import Column, String
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.users.models import User

def get_user_model():
    from app.users.models import User
    return User

class Role(SQLModel, table=True):
    __tablename__ = "roles"
    id: int = Field(default=None, primary_key=True)
    name: str = Field(sa_column=Column(String(50), nullable=False, unique=True))
    user: Optional["User"] = Relationship(back_populates="role")

    class Config:
        orm_mode = True
