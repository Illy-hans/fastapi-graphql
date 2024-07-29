from typing import Literal, Optional
import strawberry
from app.db.session import get_session
from app.resolver.mutation_resolvers import add_user
from app.schemas.types_schema import InterestInput, User 


@strawberry.type
class Mutation:

    @strawberry.field
    async def create_user(self, name: str, email: str, 
                password: str, balance: float, interest: Optional[InterestInput] = None) -> str:
        async with get_session() as session:
            new_user: Literal['Email address is in use', 'User added successfully'] = await add_user(session, name, email, password, balance, interest)
            return new_user