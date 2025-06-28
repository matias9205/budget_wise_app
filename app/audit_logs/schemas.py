from datetime import datetime
from typing import Optional
from pydantic import BaseModel

from app.audit_logs.models import Actions, TargetType
from app.users.schemas import UserSchema

class AuditLog(BaseModel):
    user: Optional[UserSchema]
    actions: Actions.value
    target_type: TargetType.value
    details: str
    ip_address: str
    created_at: datetime

class NewAuditLog(BaseModel):
    user: str
    actions: Actions
    target_type: TargetType
    details: str
    ip_address: str