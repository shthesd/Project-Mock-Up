from pydantic import BaseModel
from typing import Optional

class GroupCreate(BaseModel):
    name: str

class GroupUpdate(BaseModel):
    name: Optional[str] = None

class GroupOut(BaseModel):
    id: int
    name: str
    created_by_id: int
    class Config:
        from_attributes = True

class MemberChange(BaseModel):
    user_id: int
    is_admin: bool = False

class MemberOut(BaseModel):
    id: int
    group_id: int
    user_id: int
    is_admin: bool
    class Config:
        from_attributes = True

