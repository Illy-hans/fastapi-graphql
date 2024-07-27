from sqlalchemy import Integer, String, Float, DateTime, Boolean
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime
from app.db.session import Base
from app.models import user_interest

class Interest(Base):
    __tablename__ = "interest"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    percentage: Mapped[float] = mapped_column(Float, nullable=False)
    date_started: Mapped[datetime] = mapped_column(DateTime)
    date_ended: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    active: Mapped[bool] = mapped_column(Boolean, default=False)

    users: Mapped['User'] = relationship(
        'User',
        secondary=user_interest,
        back_populates='interests'
    )

    def as_dict(self): {
        "id": self.id, 
        "name": self.name,
        "percentage": self.percentage,
        "date_started": self.date_started,
        "date_ended": self.date_ended,
        "active": self.active
    }
