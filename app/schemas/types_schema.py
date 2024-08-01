from typing import Optional
from pydantic import Field
import strawberry
from datetime import datetime

@strawberry.type
class Interest:
    id: int
    name: str
    percentage: float
    date_added: datetime = strawberry.field(default=datetime.now())
    date_archived: Optional [datetime]
    active: Optional [bool]
    archived: Optional[bool]

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
    date_added: datetime = strawberry.field(default=datetime.now())
    date_archived: Optional[datetime]
    active: bool = strawberry.field(default=True)
    archived: Optional [bool]

@strawberry.input
class UserInput:
    name: Optional[str]
    email: Optional[str]
    password: Optional[str]
    