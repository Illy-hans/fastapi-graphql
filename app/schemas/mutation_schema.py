from typing import Literal, Optional
import strawberry
from app.db.session import get_session
from app.resolver.interest.interest_mutation_resolvers import add_new_interest
from app.resolver.user.user_mutation_resolvers import add_new_interest_to_user, add_user, delete_user, update_user_data
from app.schemas.types_schema import InterestInput, UserInput


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
            update_interest_for_user: Literal['User id not found: user does not exist', 'Interest successfully added'] = await add_new_interest_to_user(session, user_id, interest)
            return update_interest_for_user
        
    @strawberry.field
    async def update_user(self, user_id: int, user: UserInput) -> str:
        async with get_session() as session:
            updated_user: Literal['User id not found: user does not exist', 'User details updated successfully'] = await update_user_data(session, user_id, user)
            return updated_user
    
    @strawberry.field
    async def delete_user(self, user_id: int) -> str:
        async with get_session() as session:
            deleted_user: Literal['User id not found: user does not exist', 'User deleted successfully'] = await delete_user(session, user_id)
            return deleted_user

    strawberry.field
    async def add_new_interest(self, interest_id) -> str:
        async with get_session() as session:
            new_interest_added: Literal['Interest name already in use', 'Interest added successfully'] = await add_new_interest(session, interest_id)
            return new_interest_added
