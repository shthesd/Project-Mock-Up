from pydantic import BaseModel
from datetime import datetime

class AuditOut(BaseModel):
    id: int
    group_id: int | None
    actor_id: int | None
    action: str
    details: str
    created_at: datetime
    class Config:
        from_attributes = True

