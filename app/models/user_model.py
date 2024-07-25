from sqlalchemy import Integer, String, Float
from sqlalchemy.orm import DeclarativeBase, relationship, Mapped, mapped_column
from app.config.config import user_interest

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "User"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    balance: Mapped[float] = mapped_column(Float, default=0.0)


    interests = relationship(
        'Interest',
        secondary=user_interest,
        back_populates='users',
        # Handles the CASCADE ON DELETE for the User model 
        cascade="all, delete",  
        passive_deletes=True    
    )

    def as_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "password": self.password,
            "balance": self.balance
        }