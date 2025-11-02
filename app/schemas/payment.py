from pydantic import BaseModel
from datetime import date

class PaymentCreate(BaseModel):
    group_id: int
    payer_id: int
    payee_id: int
    amount: float
    date: date

