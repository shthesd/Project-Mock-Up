from pydantic import BaseModel
from typing import Dict, Optional
from datetime import date

class ExpenseCreate(BaseModel):
    description: str
    amount: float
    date: date
    payer_id: int
    shares: Dict[int, float]  # user_id -> amount

class ExpenseUpdate(BaseModel):
    description: Optional[str] = None
    amount: Optional[float] = None
    date: Optional[date] = None
    payer_id: Optional[int] = None
    shares: Optional[Dict[int, float]] = None

class ExpenseOut(BaseModel):
    id: int
    group_id: int
    payer_id: int
    created_by_id: int
    description: str
    amount: float
    date: date
    shares: dict
    class Config:
        from_attributes = True

