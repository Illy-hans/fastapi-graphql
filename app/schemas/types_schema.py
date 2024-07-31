from typing import Optional
from pydantic import Field
import strawberry
from datetime import datetime

@strawberry.type
class Interest:
    id: int
    name: str
    percentage: float
    date_started: datetime
    date_ended: datetime | None
    active: bool

@strawberry.type
class User:
    id: int
    name: str
    email: str
    password: str
    balance: float
    interests: list[Interest] 

# Default value is set to True as it activates when applied at any point.
@strawberry.input
class InterestInput:
    name: str
    percentage: float
    date_started: datetime
    date_ended: datetime | None
    active: bool = Field(default=True)


@strawberry.input
class UserInput:
    name: Optional[str]
    email: Optional[str]
    password: Optional[str]
    interests : Optional[InterestInput]
    