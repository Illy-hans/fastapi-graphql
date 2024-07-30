from sqlalchemy import Boolean, Integer, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from app.db.session import Base

class UserInterest(Base):
    __tablename__ = "user_interest"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'), nullable=False)
    interest_id: Mapped[int] = mapped_column(Integer, ForeignKey('interest.id'), nullable=False)
    created: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())
    active: Mapped[bool] = mapped_column(Boolean, default=True)
