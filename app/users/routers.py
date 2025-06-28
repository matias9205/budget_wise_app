from uuid import UUID
from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload

from app.config.db import get_db
from app.transactions.models import Transaction
from app.users.schemas import NewUserSchema, UpdateUser, UserSchemaWithTransactions
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
        
        @self.user_router.post("/new", response_model=UserSchemaWithTransactions)
        def register_new_user(payload_: NewUserSchema, db: Session = Depends(get_db)) -> UserSchemaWithTransactions:
            return UserService(db).create_new_user(payload_)
        
        @self.user_router.patch("/update/{id}", response_model=UserSchemaWithTransactions)
        def update_user(id:int, payload: UpdateUser = Body(...), db: Session = Depends(get_db)) -> UserSchemaWithTransactions:
            return UserService(db).update_user(id, payload)
        
        @self.user_router.delete("/delete/{id}")
        def delete_user(id:int, db: Session = Depends(get_db)):
            return UserService(db).delete_user(id)