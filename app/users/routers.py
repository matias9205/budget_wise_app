from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload

from app.config.db import get_db
from app.transactions.models import Transaction
from app.users.schemas import UserSchema, NewUserSchema, UserSchemaWithTransactions
from app.users.models import User

class UserRouter:
    def __init__(self):
        self.user_router = APIRouter()
        self._add_routes()

    def _add_routes(self):
        @self.user_router.get("/", response_model=list[UserSchemaWithTransactions])
        def fetch_users(db: Session = Depends(get_db)):
            users = db.query(User).join(Transaction, Transaction.user_id == User.id).all()
            return users
        
        @self.user_router.get("/{id}", response_model=UserSchemaWithTransactions)
        def fetch_one_user(id:int, db: Session = Depends(get_db)):
            try:
                print(f"ID TO FIND: {id}")
                user = db.query(User).filter_by(id=id).one()
                return user
            except:
                raise HTTPException(status_code=404, detail="No se encontró el usuario con el ID proporcionado")
        
        @self.user_router.post("/new", response_model=NewUserSchema)
        def register_new_user(payload_: NewUserSchema, db: Session = Depends(get_db)):
            print(f"PAYLOAD DATA: {payload_}")
            try:
                user = db.query(User).filter(User.email == payload_.email).first()
                if user:
                    print(f"USER FOUND: {user}")
                    raise HTTPException(status_code=409, detail="User is already registered")
                new_user = User(
                    name = payload_.name,
                    last_name = payload_.last_name,
                    age = payload_.age,
                    email = payload_.email,
                    password = payload_.password,
                    country = payload_.country,
                    balance = payload_.balance
                )
                db.add(new_user)
                db.commit()
                db.refresh(new_user)
                return new_user
            except:
                raise HTTPException(status_code=500, detail="There was an error")    