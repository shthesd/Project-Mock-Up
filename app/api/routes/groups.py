from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user
from app.models.group import Group
from app.models.membership import Membership
from app.models.user import User
from app.schemas.group import GroupCreate, GroupUpdate, GroupOut, MemberChange, MemberOut

router = APIRouter(prefix="/groups", tags=["groups"])

@router.post("/", response_model=GroupOut, status_code=201)
def create_group(payload: GroupCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    g = Group(name=payload.name, created_by_id=user.id)
    db.add(g)
    db.flush()
    m = Membership(group_id=g.id, user_id=user.id, is_admin=True)
    db.add(m)
    db.commit()
    db.refresh(g)
    return g

@router.get("/", response_model=list[GroupOut])
def list_groups(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    groups = db.query(Group).join(Membership, Membership.group_id == Group.id).filter(Membership.user_id == user.id).all()
    return groups

@router.get("/{group_id}", response_model=GroupOut)
def get_group(group_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    g = db.get(Group, group_id)
    if not g:
        raise HTTPException(404, "Group not found")
    member = db.query(Membership).filter_by(group_id=group_id, user_id=user.id).first()
    if not member:
        raise HTTPException(403, "Not a member")
    return g

@router.patch("/{group_id}", response_model=GroupOut)
def update_group(group_id: int, payload: GroupUpdate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    g = db.get(Group, group_id)
    if not g:
        raise HTTPException(404, "Group not found")
    admin = db.query(Membership).filter_by(group_id=group_id, user_id=user.id, is_admin=True).first()
    if not admin:
        raise HTTPException(403, "Admin only")
    if payload.name is not None:
        g.name = payload.name
    db.commit()
    db.refresh(g)
    return g

@router.delete("/{group_id}", status_code=204)
def delete_group(group_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    g = db.get(Group, group_id)
    if not g:
        return
    admin = db.query(Membership).filter_by(group_id=group_id, user_id=user.id, is_admin=True).first()
    if not admin:
        raise HTTPException(403, "Admin only")
    db.delete(g)
    db.commit()

@router.get("/{group_id}/members", response_model=list[MemberOut])
def list_members(group_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    if not db.get(Group, group_id):
        raise HTTPException(404, "Group not found")
    m = db.query(Membership).filter_by(group_id=group_id).all()
    return m

@router.post("/{group_id}/members", response_model=MemberOut, status_code=201)
def add_member(group_id: int, change: MemberChange, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    admin = db.query(Membership).filter_by(group_id=group_id, user_id=user.id, is_admin=True).first()
    if not admin:
        raise HTTPException(403, "Admin only")
    if not db.get(User, change.user_id):
        raise HTTPException(404, "User not found")
    mem = Membership(group_id=group_id, user_id=change.user_id, is_admin=change.is_admin)
    db.add(mem)
    db.commit()
    db.refresh(mem)
    return mem

@router.patch("/{group_id}/members/{user_id}", response_model=MemberOut)
def update_member(group_id: int, user_id: int, change: MemberChange, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    admin = db.query(Membership).filter_by(group_id=group_id, user_id=user.id, is_admin=True).first()
    if not admin:
        raise HTTPException(403, "Admin only")
    mem = db.query(Membership).filter_by(group_id=group_id, user_id=user_id).first()
    if not mem:
        raise HTTPException(404, "Membership not found")
    mem.is_admin = change.is_admin
    db.commit()
    db.refresh(mem)
    return mem

@router.delete("/{group_id}/members/{user_id}", status_code=204)
def remove_member(group_id: int, user_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    admin = db.query(Membership).filter_by(group_id=group_id, user_id=user.id, is_admin=True).first()
    if not admin:
        raise HTTPException(403, "Admin only")
    mem = db.query(Membership).filter_by(group_id=group_id, user_id=user_id).first()
    if mem:
        db.delete(mem)
        db.commit()

