from datetime import datetime
import socket
import time
from typing import List
from fastapi.responses import JSONResponse
from sqlmodel import Session
from fastapi import APIRouter, Depends, HTTPException

from app.audit_logs.models import AuditLog
from app.categories.models import Category
from app.config.db import get_db
from app.transactions.models import Transaction
from app.users.models import User
from app.users.schemas import NewUserSchema, UpdateUser, UserSchemaWithTransactions
from app.roles.models import Role

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
        
    def create_new_user(self, payload: NewUserSchema):
        print(f"PAYLOAD DATA: {payload}")
        try:
            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname)
            user = self.db.query(User).filter(User.email == payload.email).first()
            roles = [role.name for role in self.db.query(Role).all()]
            user_role = self.db.query(Role).filter(Role.name == payload.role).first()
            print(f"USER ROLE: {user_role.id}")
            if user:
                print(f"USER FOUND: {user}")
                raise HTTPException(status_code=409, detail="User is already registered")
            
            if not user_role:
                raise HTTPException(status_code=404, detail=f"Role was not found, role must be {','.join(roles)}")
            print("----------------------------------------------USER TO INSERT IN DB----------------------------------------------")
            print("")
            print("")
            new_user = User(
                name = payload.name,
                age = payload.age,
                email = payload.email,
                password = payload.password,
                country = payload.country,
                balance = payload.balance,
                role_id = user_role.id
            )
            self.db.add(new_user)
            self.db.commit()
            self.db.refresh(new_user)
            print("----------------------------------------------USER INSERTED IN DB----------------------------------------------")
            print("")
            print("")
            print(f"NEW USER ID: {new_user.id}")
            new_audit_log = AuditLog(
                user_id = new_user.id,
                action = "SignUp",
                target_type = "Users",
                details = f"New User: {new_user.email} was registered",
                ip_address = local_ip
            )

            print(f"New audit log: \n {new_audit_log}")
            
            self.db.add(new_audit_log)
            self.db.commit()
            self.db.refresh(new_audit_log)
            print("----------------------------------------------AUDIT LOG INSERTED IN DB----------------------------------------------")
            print("")
            print("")
            print(f"New user returned: \n {new_user}")
            return new_user
        except HTTPException:
            raise
        except Exception as e:
            print(f"Unexpected error: {e}")
            raise HTTPException(status_code=500, detail="There was an error")
        
    def update_user(self,id: int,  payload: UpdateUser):
        print("---------------------------------------------------------------------------")
        print(f"PAYLOAD DATA: {payload}")
        try:
            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname)
            if "email" in payload.dict().keys():
                user = self.db.query(User).filter(User.id == id).first()
            if not user:
                raise HTTPException(status_code=404, detail="User is not registered")
            print(f"USER FOUND: {user}")
            update_data = payload.dict(exclude_unset=True)
            print(f"PAYLOAD DICT: {update_data}")
            if "role" in update_data:
                role_instance = self.db.query(Role).filter(Role.name == update_data["role"]).first()
                if not role_instance:
                    raise HTTPException(status_code=404, detail="Role not found")
                user.role_id = role_instance.id
                update_data.pop("role")
            for key, value in update_data.items():
                if hasattr(user, key):
                    setattr(user, key, value)
            user.updated_at = datetime.utcnow()
            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)
            keys_updated = [key for key, value in payload.dict().items() if value is not None]
            print(f"User: {user.email} has updated {', '.join(keys_updated)}")
            new_audit_log = AuditLog(
                user_id = user.id,
                action = "Update",
                target_type = "Users",
                details = f"User: {user.email} has updated {', '.join(keys_updated)}",
                ip_address = local_ip
            )
            self.db.add(new_audit_log)
            self.db.commit()
            self.db.refresh(new_audit_log)
            return user
        except HTTPException:
            raise
        except Exception as e:
            print(f"Unexpected error: {e}")
            raise HTTPException(status_code=500, detail="There was an error")
        
    def delete_user(self, id: int):
        print("---------------------------------------------------------------------------")
        print(f"USER ID: {id}")
        try:
            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname)
            user = self.db.query(User).filter(User.id == id).first()
            if user:
                print("---------------------------------------------------------------------------")
                print(f"USER TO DELETE: {user}")
                self.db.query(Transaction).filter(Transaction.user_id == user.id).delete()
                self.db.commit()
                self.db.query(AuditLog).filter(AuditLog.user_id == user.id).delete()
                self.db.commit()
                self.db.delete(user)
                self.db.commit()
            else:
                raise HTTPException(status_code=404, detail="User is not registered")
            return user
        except HTTPException:
            raise
        except Exception as e:
            print(f"Unexpected error: {e}")
            raise HTTPException(status_code=500, detail="There was an error")