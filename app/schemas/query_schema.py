import strawberry
from app.resolver.user_resolver import get_all_interests, get_all_users, get_user
from app.db.session import get_session
from app.schemas.types_schema import User, Interest

@strawberry.type
class Query:

    @strawberry.field
    async def users(self) -> list[User]: 
        async with get_session() as session:
            users = await get_all_users(session)
            return users

    @strawberry.field
    async def user(self, user_id: int) -> User | None:
        async with get_session() as session:
            user = await get_user(session, user_id)
            return user

    @strawberry.field
    async def interests(self) -> list[Interest]:
        async with get_session() as session:
            interests = await get_all_interests(session)
            return interests