from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import json
from app.api.deps import get_db, get_current_user
from app.models.membership import Membership
from app.models.expense import Expense
from app.models.payment import Payment
from app.services.balances import compute_balances

router = APIRouter(prefix="/groups/{group_id}/balances", tags=["balances"])

@router.get("/")
def get_balances(group_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    membership = db.query(Membership).filter_by(group_id=group_id, user_id=user.id).first()
    if not membership:
        raise HTTPException(403, "Not a member")
    expenses = [
        {
            "amount": float(e.amount),
            "payer_id": e.payer_id,
            "shares": json.loads(e.shares_json),
        }
        for e in db.query(Expense).filter_by(group_id=group_id).all()
    ]
    payments = [
        {
            "payer_id": p.payer_id,
            "payee_id": p.payee_id,
            "amount": float(p.amount),
        }
        for p in db.query(Payment).filter_by(group_id=group_id).all()
    ]
    return {"balances": compute_balances(expenses, payments)}

