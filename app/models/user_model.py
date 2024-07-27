from sqlalchemy import Integer, String, Float
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.models import user_interest
from app.db.session import Base


class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    balance: Mapped[float] = mapped_column(Float, default=0.0)

    interests: Mapped['Interest'] = relationship(
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

print(f"{__name__} module loaded, {User.__tablename__} table created")
