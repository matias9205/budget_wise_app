import socket
from fastapi import HTTPException
from sqlmodel import Session

from app.audit_logs.models import AuditLog
from app.auth.schemas import Token, UserLogin
from app.config.config import Settings
from app.roles.models import Role
from app.users.models import User
from app.utils.security import Security

class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.secret_key = Settings().SECRET_KEY

    def login(self, payload: UserLogin):
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        print(f"USER TO FIND: {payload.email}")
        user = self.db.query(User).filter(User.email == payload.email).first()
        if not user:
            print(f"USER WITH EMAIL {payload.email} WAS NOT FOUND")
            raise HTTPException(status_code=404, detail=f"User with email {payload.email} wasn't found")
        print({'user_id': user.id, 'user_email': user.email})
        print(f"PASSWORD HASHED SAVED IN DB: {user.password}")
        if not Security(self.secret_key).verify_password(payload.password, user.password):
            print("INVALID CREDENTIALS, AUTHENTICATION FAIL")
            raise HTTPException(status_code=401, detail="Invalid credentials")
        print(user)
        user_role = self.db.query(Role).filter(Role.id == user.role_id).first()
        access_token_payload = {
            "sub": user.id,
            "username": user.name,
            "role": user_role.name
        }
        new_audit_event = {
            "user_id": user.id,
            "action": "Login",
            "target_type": "Auth",
            "details": f"New User: {user.email} has login",
            "ip_address": local_ip
        }
        print(f"NEW AUDIT LOG FOR LOGIN EVENT: \n {new_audit_event}")
        new_audit_log = AuditLog(
            user_id = user.id,
            action = "Login",
            target_type = "Auth",
            details = f"New User: {user.email} has login",
            ip_address = local_ip
        )
        self.db.add(new_audit_log)
        self.db.commit()
        self.db.refresh(new_audit_log)
        print("----------------------------------------------AUDIT LOG INSERTED IN DB----------------------------------------------")
        print("")
        print("")
        print(f"ACCESS TOKEN PAYLOAD: \n {access_token_payload}")
        access_token = Security(self.secret_key).create_access_token(access_token_payload)
        print(f"ACCESS TOKEN GENERATED: {access_token}")
        return Token(access_token=access_token, token_type="bearer")