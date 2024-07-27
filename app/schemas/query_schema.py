import strawberry
from app.resolver.user_resolver import get_all_users
from app.db.session import get_session


@strawberry.type
class User:
    id: int
    name: str
    password: str
    balance: float


@strawberry.type
class Query:

    @strawberry.field
    async def users(self) -> list[User]: 
        async with get_session() as session:
            users = await get_all_users(session)
            return users