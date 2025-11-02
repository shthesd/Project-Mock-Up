from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user
from app.models.audit import AuditLog

router = APIRouter(prefix="/audit", tags=["audit"]) 

@router.get("/", response_model=list)
def list_audit(db: Session = Depends(get_db), user=Depends(get_current_user)):
    logs = db.query(AuditLog).order_by(AuditLog.created_at.desc()).limit(200).all()
    return [
        {
            "id": l.id,
            "group_id": l.group_id,
            "actor_id": l.actor_id,
            "action": l.action,
            "details": l.details,
            "created_at": l.created_at,
        }
        for l in logs
    ]

