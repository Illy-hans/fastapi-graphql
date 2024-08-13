from typing import Optional
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
class Balance:
    id: int
    user_id: int
    date: datetime
    total_balance: float
    interest_accrued_today: float
    cumulative_interest_accrued: float

@strawberry.type
class UserInterest:
    id: int
    user_id: int
    interest_id: int
    created: datetime
    active: bool

@strawberry.type
class User:
    id: int
    name: str
    email: str
    password: str
    balances: list[Balance]
    interests: list[Interest] 

@strawberry.type
class LoginResponse:
    access_token: str
    user_name: str

# Default value is set to True as it activates when applied at any point.
@strawberry.input
class InterestInput:
    name: str
    percentage: float
    date_added: datetime = strawberry.field(default=datetime.now())
    date_archived: Optional[datetime] = None
    active: bool = strawberry.field(default=True)
    archived: Optional [bool] = None

@strawberry.input
class UserInput:
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    

