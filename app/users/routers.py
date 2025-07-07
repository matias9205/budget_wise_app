from uuid import UUID
from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload

from app.auth.schemas import UserTokenPayload
from app.config.config import Settings
from app.config.db import get_db
from app.transactions.models import Transaction
from app.users.schemas import NewUserSchema, UpdateUser, UserSchemaWithTransactions
from app.users.services import UserService
from app.utils.security import Security

class UserRouter(Security):
    def __init__(self):
        super().__init__(Settings().SECRET_KEY)
        self.user_router = APIRouter()
        self._add_routes()

    def _add_routes(self):
        @self.user_router.get("/", response_model=list[UserSchemaWithTransactions])
        def fetch_users(db: Session = Depends(get_db)):
            return UserService(db).get_all_users()
        
        @self.user_router.get("/{id}", response_model=UserSchemaWithTransactions)
        def fetch_one_user(id:int, db: Session = Depends(get_db)):
            return UserService(db).get_user(id)
        
        @self.user_router.post("/auth_user", response_model=UserSchemaWithTransactions)
        def fetch_current_user(db: Session = Depends(get_db), token: str = Depends(self.get_oauth2_scheme())):
            print(f"ACCESS TOKEN IN auth user POST: {token}")
            user = self.get_current_user(token)
            print(f"User from token: {user['sub']}")
            return UserService(db).get_user(user['sub'])
        
        @self.user_router.post("/new", response_model=UserSchemaWithTransactions)
        def register_new_user(payload_: NewUserSchema, db: Session = Depends(get_db)) -> UserSchemaWithTransactions:
            return UserService(db).create_new_user(payload_)
        
        @self.user_router.patch("/update", response_model=UserSchemaWithTransactions)
        def update_user(id:int, payload: UpdateUser = Body(...), db: Session = Depends(get_db), token: str = Depends(self.get_oauth2_scheme())) -> UserSchemaWithTransactions:
            print(f"ACCESS TOKEN IN auth user POST: {token}")
            user = self.get_current_user(token)
            print(f"User from token: {user['sub']}")
            return UserService(db).update_user(user['sub'], payload)
        
        @self.user_router.delete("/delete")
        def delete_user(id:int, db: Session = Depends(get_db), token: str = Depends(self.get_oauth2_scheme())):
            print(f"ACCESS TOKEN IN auth user POST: {token}")
            user = self.get_current_user(token)
            print(f"User from token: {user['sub']}")
            return UserService(db).delete_user(user['sub'])