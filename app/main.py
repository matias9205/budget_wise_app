import os
from fastapi import FastAPI
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from sqlalchemy import inspect
from sqlmodel import Session

from app.users.routers import UserRouter 
from app.users.models import User
from app.categories.routers import CategoryRouter 
from app.categories.models import Category
from app.transactions.routers import TransactionRouter
from app.transactions.models import Transaction
from app.config.db import Base, engine

load_dotenv()

print(f"Connected to {engine.url} database")

Base.metadata.create_all(bind=engine)
print(Base.metadata.create_all(bind=engine))
inspector = inspect(engine)
print(inspector.get_table_names())

app = FastAPI()
app.include_router(UserRouter().user_router, prefix="/users")
app.include_router(TransactionRouter().transaction_router, prefix="/transactions")
app.include_router(CategoryRouter().category_router, prefix="/categories")

@app.get("/")
async def index():
    return {"Hello": "World"}