from sqlalchemy import Integer, String, Numeric, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

class Expense(Base):
    __tablename__ = "expenses"
    id: Mapped[int] = mapped_column(primary_key=True)
    group_id: Mapped[int] = mapped_column(Integer, index=True)
    payer_id: Mapped[int] = mapped_column(Integer, index=True)
    created_by_id: Mapped[int] = mapped_column(Integer, index=True)
    description: Mapped[str] = mapped_column(String(255))
    amount: Mapped[float] = mapped_column(Numeric(12, 2))
    date: Mapped[str] = mapped_column(Date)
    shares_json: Mapped[str] = mapped_column(String)  # JSON string of {user_id: amount}

    group = relationship("Group", back_populates="expenses")

