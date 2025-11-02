from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import json
from app.api.deps import get_db, get_current_user
from app.models.expense import Expense
from app.models.group import Group
from app.models.membership import Membership
from app.schemas.expense import ExpenseCreate, ExpenseUpdate, ExpenseOut

router = APIRouter(prefix="/groups/{group_id}/expenses", tags=["expenses"])

@router.post("/", response_model=ExpenseOut, status_code=201)
def create_expense(group_id: int, body: ExpenseCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    group = db.get(Group, group_id)
    if not group:
        raise HTTPException(404, "Group not found")
    membership = db.query(Membership).filter_by(group_id=group_id, user_id=user.id).first()
    if not membership:
        raise HTTPException(403, "Not a member")
    e = Expense(group_id=group_id, payer_id=body.payer_id, created_by_id=user.id,
                description=body.description, amount=body.amount, date=body.date,
                shares_json=json.dumps(body.shares))
    db.add(e)
    db.commit()
    db.refresh(e)
    return ExpenseOut(id=e.id, group_id=e.group_id, payer_id=e.payer_id, created_by_id=e.created_by_id,
                      description=e.description, amount=float(e.amount), date=e.date,
                      shares=json.loads(e.shares_json))

@router.get("/", response_model=list[ExpenseOut])
def list_expenses(group_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    membership = db.query(Membership).filter_by(group_id=group_id, user_id=user.id).first()
    if not membership:
        raise HTTPException(403, "Not a member")
    items = db.query(Expense).filter_by(group_id=group_id).all()
    out = []
    for e in items:
        out.append(ExpenseOut(id=e.id, group_id=e.group_id, payer_id=e.payer_id, created_by_id=e.created_by_id,
                      description=e.description, amount=float(e.amount), date=e.date,
                      shares=json.loads(e.shares_json)))
    return out

@router.patch("/{expense_id}", response_model=ExpenseOut)
def update_expense(group_id: int, expense_id: int, body: ExpenseUpdate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    e = db.get(Expense, expense_id)
    if not e or e.group_id != group_id:
        raise HTTPException(404, "Expense not found")
    membership = db.query(Membership).filter_by(group_id=group_id, user_id=user.id).first()
    if not membership:
        raise HTTPException(403, "Not a member")
    # creator can edit their own, admins can edit any
    is_admin = db.query(Membership).filter_by(group_id=group_id, user_id=user.id, is_admin=True).first() is not None
    if not (is_admin or e.created_by_id == user.id):
        raise HTTPException(403, "Not allowed")
    if body.description is not None: e.description = body.description
    if body.amount is not None: e.amount = body.amount
    if body.date is not None: e.date = body.date
    if body.payer_id is not None: e.payer_id = body.payer_id
    if body.shares is not None:
        e.shares_json = json.dumps(body.shares)
    db.commit()
    db.refresh(e)
    return ExpenseOut(id=e.id, group_id=e.group_id, payer_id=e.payer_id, created_by_id=e.created_by_id,
                      description=e.description, amount=float(e.amount), date=e.date,
                      shares=json.loads(e.shares_json))

@router.delete("/{expense_id}", status_code=204)
def delete_expense(group_id: int, expense_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    e = db.get(Expense, expense_id)
    if not e or e.group_id != group_id:
        return
    is_admin = db.query(Membership).filter_by(group_id=group_id, user_id=user.id, is_admin=True).first() is not None
    if not (is_admin or e.created_by_id == user.id):
        raise HTTPException(403, "Not allowed")
    db.delete(e)
    db.commit()

