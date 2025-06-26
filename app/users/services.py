from typing import List
from sqlmodel import Session
from fastapi import APIRouter, Depends, HTTPException

from app.categories.models import Category
from app.config.db import get_db
from app.transactions.models import Transaction
from app.users.models import User
from app.users.schemas import UserSchema, NewUserSchema, UserSchemaWithTransactions

class UserService:
    def __init__(self, db: Session):
        self.db = db

    def get_all_users(self) -> List[UserSchemaWithTransactions]:
        users = self.db.query(User).join(Transaction, Transaction.user_id == User.id).join(Category, Transaction.category_id == Category.id).all()
        return users
    
    def get_user(self, id: int) -> UserSchemaWithTransactions:
        try:
            print(f"ID TO FIND: {id}")
            user = self.db.query(User).filter_by(id=id).one()
            return user
        except:
            raise HTTPException(status_code=404, detail="No se encontró el usuario con el ID proporcionado")
        
    def create_new_user(self, payload):
        print(f"PAYLOAD DATA: {payload}")
        try:
            user = self.db.query(User).filter(User.email == payload.email).first()
            if user:
                print(f"USER FOUND: {user}")
                raise HTTPException(status_code=409, detail="User is already registered")
            
            new_user = User(
                name = payload.name,
                last_name = payload.last_name,
                age = payload.age,
                email = payload.email,
                password = payload.password,
                country = payload.country,
                balance = payload.balance
            )

            self.db.add(new_user)
            self.db.commit()
            self.db.refresh(new_user)
            return new_user
        except HTTPException:
            raise
        except Exception as e:
            print(f"Unexpected error: {e}")
            raise HTTPException(status_code=500, detail="There was an error")  