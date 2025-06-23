from datetime import datetime
from enum import Enum
from typing import Optional
from sqlalchemy import Column, String
from sqlmodel import Field, Relationship, SQLModel

class Category(SQLModel, table=True):
    __tablename__ = "categories"
    id: int = Field(default=None, primary_key=True)
    name: str = Field(sa_column=Column(String(250), nullable=False, unique=True))