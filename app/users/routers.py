from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload

from app.config.db import get_db
from app.transactions.models import Transaction
from app.users.schemas import UserSchema, NewUserSchema, UserSchemaWithTransactions
from app.users.services import UserService

class UserRouter:
    def __init__(self):
        self.user_router = APIRouter()
        self._add_routes()

    def _add_routes(self):
        @self.user_router.get("/", response_model=list[UserSchemaWithTransactions])
        def fetch_users(db: Session = Depends(get_db)):
            return UserService(db).get_all_users()
        
        @self.user_router.get("/{id}", response_model=UserSchemaWithTransactions)
        def fetch_one_user(id:int, db: Session = Depends(get_db)):
            return UserService(db).get_user(id)
        
        @self.user_router.post("/new", response_model=NewUserSchema)
        def register_new_user(payload_: NewUserSchema, db: Session = Depends(get_db)) -> UserSchema:
            return UserService(db).create_new_user(payload_)