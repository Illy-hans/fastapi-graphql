from sqlalchemy import Integer, String, Float, DateTime, Boolean
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime
from app.db.session import Base
from app.models.user_interest import UserInterest

class Interest(Base):
    __tablename__ = "interest"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    percentage: Mapped[float] = mapped_column(Float, nullable=False)
    date_added: Mapped[datetime] = mapped_column(DateTime, nullable=True, default=datetime.now())
    active: Mapped[bool] = mapped_column(Boolean, default=False)
    date_archived: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    archived: Mapped[bool] = mapped_column(Boolean, default=False)

    users = relationship(
        'User',
        secondary=UserInterest.__table__,
        back_populates='interests',
        collection_class=list,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.users is None:
            self.users = []

    def as_dict(self): {
        "id": self.id, 
        "name": self.name,
        "percentage": self.percentage,
        "date_started": self.date_started,
        "date_ended": self.date_ended,
        "active": self.active,
        "archived": self.archived
    }
