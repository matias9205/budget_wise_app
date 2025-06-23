from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.categories.models import Category
from app.config.db import get_db
from .schemas import TransactionSchema, NewTransactionSchema 
from .models import Transaction
from app.users.models import User

class TransactionRouter:
    def __init__(self):
        self.transaction_router = APIRouter(tags=["transactions"])
        self._add_routes()

    def _add_routes(self):
        @self.transaction_router.get("/", response_model=list[TransactionSchema])
        def fetch_transactions(db: Session = Depends(get_db)):
            transactions = db.query(Transaction).all()
            return transactions
        
        @self.transaction_router.get(f"/{id}", response_model=TransactionSchema)
        def fetch_transaction(db: Session = Depends(get_db)):
            try:
                print(f"ID TO FIND: {id}")
                transaction = db.query(Transaction).filter(Transaction.id==id).first()
                return transaction
            except:
                raise HTTPException(status_code=404, detail="No se encontró la transaccion con el ID proporcionado")
        
        @self.transaction_router.post("/new", response_model=TransactionSchema)
        def register_new_transaction(payload: NewTransactionSchema, db: Session = Depends(get_db)):
            print(f"PAYLOAD DATA: {payload}")
            try:
                user = db.query(User).filter(User.email == payload.user).first()
                if not user:
                    print(f"USER WITH EMAIL {payload.email} WAS NOT FOUND")
                    raise HTTPException(status_code=404, detail=f"User with email {payload} wasn't found")
                print({'user_id': user.id, 'user_email': user.email})
                if payload.type == 'expense' or payload.type == 'Expense':
                    print(f"PAYLOAD TYPE: {payload.type}")
                    user.balance = user.balance - payload.amount
                else:
                    print(f"PAYLOAD TYPE: {payload.type}")
                    user.balance = user.balance + payload.amount
                new_transaction = Transaction(
                    user_id = user.id,
                    concept = payload.concept,
                    amount = payload.amount,
                    type = payload.type,
                    category_id = payload.category_id,
                )
                db.add(new_transaction)
                db.commit()
                db.refresh(new_transaction)
                return new_transaction
            except:
                raise HTTPException(status_code=500, detail="There was an error")   