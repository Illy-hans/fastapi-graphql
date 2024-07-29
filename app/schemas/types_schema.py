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
    interests: list[Interest] | None