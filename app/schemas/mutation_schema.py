from typing import Literal, Optional
import strawberry
from app.db.session import get_session
from app.resolver.mutation_resolvers import add_new_interest, add_user
from app.schemas.types_schema import InterestInput


@strawberry.type
class Mutation:

    @strawberry.field
    async def create_user(self, name: str, email: str, 
                password: str, balance: float, interest: Optional[InterestInput] = None) -> str:
        async with get_session() as session:
            new_user: Literal['Email address is in use', 'User added successfully'] = await add_user(session, name, email, password, balance, interest)
            return new_user
        
    @strawberry.field
    async def add_interest(self, user_id: int, interest: InterestInput) -> str: 
        async with get_session () as session:
            update_interest_for_user: Literal['User id not found: user does not exist', 'Interest successfully added'] = await add_new_interest(session, user_id, interest)
            return update_interest_for_user