from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from interest_model import 

Base = declarative_base()

class Interest(Base):
    __tablename__ = "Interest"
    id: int = Column(Integer, primary_key=True)
    name: str = Column(String, nullable=False)
    percentage: float = Column(Float, nullable=False)
    date_started: datetime = Column(DateTime)
    date_ended: datetime = Column(DateTime, nullable=True)
    active: bool = Column(Boolean, default=False)

    users = relationship(
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
