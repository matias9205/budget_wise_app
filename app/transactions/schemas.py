from decimal import Decimal
from typing import List, Optional
from fastapi import Depends
from pydantic import BaseModel, validator
from datetime import datetime

from app.categories.schemas import CategorySchema

from .models import TransactionType
class TransactionSchema(BaseModel):
    user_id: int
    concept: str
    amount: float
    type: TransactionType
    category: Optional[CategorySchema]
    created_at: datetime
    updated_at: datetime
    
class NewTransactionSchema(BaseModel):
    # user: str
    concept: str
    amount: float
    type: TransactionType
    category: str

    @validator("amount")
    def max_two_decimals(cls, val):
        decimal = Decimal(str(val))
        if abs(decimal.as_tuple().exponent) > 2:
            raise ValueError("El monto no puede tener más de 2 decimales")
        return val