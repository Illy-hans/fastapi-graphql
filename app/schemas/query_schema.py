from typing import Literal
import strawberry
from app.resolvers.interest.interest_query_resolvers import get_active_interest_percentage, get_all_interests, get_interest
from app.resolvers.user.user_query_resolvers import get_all_users, get_user
from app.db.session import get_session
from app.schemas.types_schema import User, Interest

@strawberry.type
class Query:

    # GET ALL users
    @strawberry.field
    async def users(self) -> list[User]: 
        async with get_session() as session:
            users = await get_all_users(session)
            return users

    # GET user
    @strawberry.field
    async def user(self, user_id: int) -> User | None:
        async with get_session() as session:
            user = await get_user(session, user_id)
            return user

    # GET ALL interest
    @strawberry.field
    async def interests(self) -> list[Interest]:
        async with get_session() as session:
            interests = await get_all_interests(session)
            return interests
    
    # GET interest
    @strawberry.field
    async def get_interest(self, interest_id: int) -> Interest | None:
        async with get_session() as session:
            interest = await get_interest(session, interest_id)
            return interest
    
    # GET active interest percentage for user
    @strawberry.field
    async def get_interest_percentage(self, user_id: int) -> float:
        async with get_session() as session:
            percentage: float | Literal['No active interest found'] = await get_active_interest_percentage(session, user_id)
            return percentage