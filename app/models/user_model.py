from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id: int = Column(Integer, primary_key=True)
    name: str = Column(String, nullable=False)
    password: str = Column(String, nullable=False)
    balance: float = Column(Float, default=0.0)

    interest = relationship("InterestType",  cascade="all, delete", passive_deletes=True)

    def as_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "password": self.password,
            "balance": self.balance
        }