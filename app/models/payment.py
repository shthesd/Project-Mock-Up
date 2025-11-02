from sqlalchemy import Integer, Numeric, Date
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base

class Payment(Base):
    __tablename__ = "payments"
    id: Mapped[int] = mapped_column(primary_key=True)
    group_id: Mapped[int] = mapped_column(Integer, index=True)
    payer_id: Mapped[int] = mapped_column(Integer, index=True)
    payee_id: Mapped[int] = mapped_column(Integer, index=True)
    amount: Mapped[float] = mapped_column(Numeric(12, 2))
    date: Mapped[str] = mapped_column(Date)

