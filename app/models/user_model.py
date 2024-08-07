from sqlalchemy import Integer, String
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.db.session import Base
from app.models.user_interest import UserInterest

class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)

    balances = relationship(
        'Balance', 
        back_populates='user', 
        order_by='Balance.date',
        # Handles the CASCADE ON DELETE for the User model 
        cascade="all, delete",
        passive_deletes=True,
        collection_class=list,
    )

    interests = relationship(
        'Interest',
        secondary=UserInterest.__table__,
        back_populates='users',
        cascade="all, delete",  
        passive_deletes=True,
        collection_class=list,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.interests is None:
            self.interests = []


    def as_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "password": self.password,
            "balances": [balance.as_dict() for balance in self.balances],
            "interests": [interest.as_dict() for interest in self.interests]

        }
