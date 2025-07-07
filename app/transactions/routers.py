from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.categories.models import Category
from app.config.config import Settings
from app.config.db import get_db
from app.transactions.services import TransactionService
from app.utils.security import Security
from .schemas import TransactionSchema, NewTransactionSchema 
from .models import Transaction
from app.users.models import User

class TransactionRouter(Security):
    def __init__(self):
        super().__init__(Settings().SECRET_KEY)
        self.transaction_router = APIRouter(tags=["transactions"])
        self._add_routes()

    def _add_routes(self):
        @self.transaction_router.get("/", response_model=list[TransactionSchema])
        def fetch_transactions(db: Session = Depends(get_db)):
            return TransactionService(db).get_all_transactions()
        
        @self.transaction_router.get(f"/{id}", response_model=TransactionSchema)
        def fetch_transaction(id:int, db: Session = Depends(get_db)):
            return TransactionService(db).get_transaction(id)
        
        @self.transaction_router.post("/new", response_model=TransactionSchema)
        def register_new_transaction(payload: NewTransactionSchema, db: Session = Depends(get_db), token: str = Depends(self.get_oauth2_scheme())):
            print(f"ACCESS TOKEN IN auth user POST: {token}")
            user = self.get_current_user(token)
            print(f"User from token: {user['sub']}")
            print(f"PAYLOAD FOR A NEW TRANSACTION - IN POST ROUTER: {payload.__dict__}")
            return TransactionService(db).create_new_transaction(user['username'], payload)