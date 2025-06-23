from pydantic import BaseModel
from datetime import datetime

from .models import TransactionType

class TransactionSchema(BaseModel):
    user_id: int
    concept: str
    amount: float
    type: TransactionType
    category_id: int
    created_at: datetime
    updated_at: datetime
    
class NewTransactionSchema(BaseModel):
    user: str
    concept: str
    amount: float
    type: TransactionType
    category_id: int