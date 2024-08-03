from sqlalchemy import Integer, ForeignKey, DateTime, Float, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from app.db.session import Base

class Balance(Base):
    __tablename__ = "balance"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'), nullable=False)
    date: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now())
    total_balance: Mapped[Numeric] = mapped_column(Numeric(precision=10, scale=2), nullable=False)
    interest_accrued_today: Mapped[Numeric] = mapped_column(Numeric(precision=10, scale=4))
    cumulative_interest_accrued: Mapped[Numeric] = mapped_column(Numeric(precision=10, scale=4))

    user = relationship('User', back_populates="balances")