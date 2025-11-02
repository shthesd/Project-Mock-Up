from sqlalchemy import UniqueConstraint, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

class Membership(Base):
    __tablename__ = "memberships"
    __table_args__ = (UniqueConstraint("group_id", "user_id", name="uq_group_user"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    group_id: Mapped[int] = mapped_column(Integer, index=True)
    user_id: Mapped[int] = mapped_column(Integer, index=True)
    is_admin: Mapped[bool] = mapped_column(default=False)

    user = relationship("User", back_populates="memberships")
    group = relationship("Group", back_populates="memberships")

