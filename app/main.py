import os
from fastapi import FastAPI
from dotenv import load_dotenv
from sqlalchemy import inspect
from sqlmodel import SQLModel, Session

from app.auth.routers import AuthRouter
from app.core.exceptions import ExceptionsHandlers
from app.users.routers import UserRouter 
from app.categories.routers import CategoryRouter 
from app.transactions.routers import TransactionRouter
from app.config.db import db
from app.utils.populate_tables import PopulateTable

load_dotenv()

engine = db.create_db_connection()

print(f"Connected to {db.engine.url} database")

def init_models():
    from app.users.models import User
    from app.roles.models import Role
    from app.categories.models import Category
    from app.transactions.models import Transaction
    from app.audit_logs.models import AuditLog
    db.Base.metadata.create_all(bind=engine)
    print(db.Base.metadata.create_all(bind=engine))

init_models()

inspector = inspect(engine)
print(inspector.get_table_names())
PopulateTable(engine).populate_categories()
PopulateTable(engine).populate_roles()

app = FastAPI()
app.include_router(UserRouter().user_router, prefix="/users")
app.include_router(TransactionRouter().transaction_router, prefix="/transactions")
app.include_router(CategoryRouter().category_router, prefix="/categories")
app.include_router(AuthRouter().auth_router, prefix="/auth")
ExceptionsHandlers().add_exception_handlers(app)

@app.get("/")
async def index():
    return {"Hello": "World"}