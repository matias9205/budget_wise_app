from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.config.db import get_db

from .models import Category 
from .schemas import CategorySchema, NewCategorySchema

class CategoryRouter:
    def __init__(self):
        self.category_router = APIRouter(tags=["categories"])
        self._add_routes()
    
    def _add_routes(self):
        @self.category_router.get("/", response_model=list[CategorySchema])
        def fetch_categories(db: Session = Depends(get_db)):
            categories = db.query(Category).all()
            return categories