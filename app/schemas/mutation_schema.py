from typing import Literal, Optional
import strawberry
from app.db.session import get_session
from app.resolvers.authentication.authentication_resolver import login_resolver
from app.resolvers.balance.balance_mutation_resolver import add_deposit_into_account, all_daily, update_user_balance_daily
from app.resolvers.interest.interest_mutation_resolvers import add_new_interest, archive_interest
from app.resolvers.user.user_mutation_resolvers import add_new_interest_to_user, add_user, delete_user, update_user_data
from app.schemas.types_schema import InterestInput, LoginResponse, User, UserInput
from app.utils.authentication import Authentication

@strawberry.type
class Mutation:

    # CREATE user
    @strawberry.field
    async def create_user(self, name: str, email: str, 
                password: str, balance: float, interest_id: Optional[int] = None) -> str:
        async with get_session() as session:
            new_user: Literal['Email address is in use', 'User added successfully']= await add_user(session, name, email, password, balance, interest_id)
            return new_user
    
    # ADD Interest type to user
    @strawberry.field
    async def update_interest_for_user(self, user_id: int, interest_id: int) -> str: 
        async with get_session() as session:
            update_interest_for_user: Literal['User id not found: user does not exist', 'Interest successfully added'] = await add_new_interest_to_user(session, user_id, interest_id)
            return update_interest_for_user
    
    # UPDATE user details(name, email, password)
    @strawberry.field
    async def update_user(self, user_id: int, user: UserInput) -> str:
        async with get_session() as session:
            updated_user: Literal['User id not found: user does not exist', 'User details updated successfully'] = await update_user_data(session, user_id, user)
            return updated_user
        
    # DELETE user
    @strawberry.field
    async def delete_user(self, user_id: int) -> str:
        async with get_session() as session:
            deleted_user: Literal['User id not found: user does not exist', 'User deleted successfully'] = await delete_user(session, user_id)
            return deleted_user

    # ADD Interest type
    @strawberry.field
    async def add_new_interest(self, interest: InterestInput) -> str:
        async with get_session() as session:
            new_interest_added: Literal['Interest name already in use', 'Interest added successfully'] = await add_new_interest(session, interest)
            return new_interest_added

    # ARCHIVE Interest type
    @strawberry.field
    async def archive_interest(self, interest_id: int) -> str:
        async with get_session() as session:
            archived_interest: Literal['Interest id not found: interest does not exist', 'Interest archived successfully'] = await archive_interest(session, interest_id)
            return archived_interest

    # ADD deposit to account
    @strawberry.field
    async def add_deposit(self, user_id:int, deposit:float) -> str:
        async with get_session() as session:
            add_deposit_result: str = await add_deposit_into_account(session, user_id, deposit)
            return add_deposit_result
    
    # Calculates interest update for one user
    @strawberry.field
    async def create_new_balance(self, user_id:int) -> str:
        async with get_session() as session:
            update_daily_balance: Literal['User id not found: user does not exist', 'No existing balance found for user.', 'Daily Balance created'] = await update_user_balance_daily(session, user_id)
            return update_daily_balance
    
    # Updates all user balances daily
    @strawberry.field
    async def all_user_balances_updates(self) -> str:
        async with get_session() as session:
            all_user_balances_updated: str = await all_daily(session)
            return all_user_balances_updated
        
    # Returns access token valid for 30m and user Name 
    @strawberry.field
    async def login(self, email: str, password: str) -> LoginResponse:
        async with get_session() as session:
            access_token_return_dict = await login_resolver(session, email, password)
            return access_token_return_dict
    
    #Decodes token and returns User model
    @strawberry.field
    async def decode_user_from_token(self, token: str) -> User:
        async with get_session() as session:
            returned_user = await Authentication.decode_token(session, token)
            return returned_user