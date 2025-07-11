import socket
from typing import List
from sqlmodel import Session
from fastapi import APIRouter, Depends, HTTPException

from app.audit_logs.models import AuditLog
from app.categories.models import Category
from app.transactions.schemas import TransactionSchema, NewTransactionSchema
from app.transactions.models import Transaction
from app.users.models import User

class TransactionService:
    def __init__(self, db: Session):
        self.db = db

    def get_all_transactions(self) -> List[TransactionSchema]:
        transactions = self.db.query(Transaction).all()
        return transactions
    
    def get_transaction(self, id:int) -> TransactionSchema:
        try:
            print(f"ID TO FIND: {id}")
            transaction = self.db.query(Transaction).filter(Transaction.id==id).first()
            return transaction
        except:
            raise HTTPException(status_code=404, detail="No se encontró la transaccion con el ID proporcionado")
        
    def create_new_transaction(self, username: str, payload:NewTransactionSchema):
        print(f"PAYLOAD DATA: {payload}")
        try:
            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname)
            user = self.db.query(User).filter(User.name == username).first()
            categories = [category.name for category in self.db.query(Category).all()]
            print(f"LIST OF CATEGORIES: {categories}")

            if not user:
                print(f"USER {username} WAS NOT FOUND")
                raise HTTPException(status_code=404, detail=f"User {username} wasn't found")
            print({'user_id': user.id, 'user_email': user.email})

            if payload.category not in categories:
                raise HTTPException(status_code=404, detail=f"Category {payload.category} was not found, category must be like {', '.join(categories)}")
            else:
                category = self.db.query(Category).filter(Category.name == payload.category).first()

            if user.balance < payload.amount and (payload.type == 'expense' or payload.type == 'Expense'):
                raise HTTPException(status_code=400, detail="Insufficient funds")
            
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
                type = payload.type.value,
                category_id = category.id,
            )
            self.db.add(new_transaction)
            self.db.commit()
            self.db.refresh(new_transaction)

            new_audit_log = AuditLog(
                user_id = new_transaction.user_id,
                action = "Create",
                target_type = "Transactions",
                details = f"New Transaction: {new_transaction.type} was registered",
                ip_address = local_ip
            )
            self.db.add(new_audit_log)
            self.db.commit()
            self.db.refresh(new_audit_log)

            return new_transaction
        except HTTPException:
            raise
        except:
            raise HTTPException(status_code=500, detail="There was an error")