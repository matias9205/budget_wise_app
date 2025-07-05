from fastapi import APIRouter, Body, Depends
from sqlmodel import Session

from app.auth.schemas import UserLogin
from app.auth.services import AuthService
from app.config.db import get_db

class AuthRouter:
    def __init__(self):
        self.auth_router = APIRouter()
        self._add_routes()

    def _add_routes(self):
        @self.auth_router.post("/login")
        def login_(payload: UserLogin = Body(), db: Session = Depends(get_db)):
            print(f"PAYLOAD IN POST LOGIN ROUTE: \n {payload}")
            return AuthService(db).login(payload)