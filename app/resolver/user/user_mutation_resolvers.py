from typing import Optional
from sqlalchemy import Delete, Update, delete, update
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from app.models.balance_model import Balance as BalanceModel
from app.models.interest_model import Interest
from app.models.user_interest import UserInterest
from app.models.user_model import User as UserModel
from app.resolver.interest.interest_query_resolvers import get_interest
from app.schemas.types_schema import UserInput
from app.utils.password_hasher import Hasher

# Adds new user 
async def add_user(session: AsyncSession,  name: str, email: str, 
                password: str, balance: float, interest_id: Optional[int] = None):
    try: 
        stmt = select(UserModel).where(UserModel.email == email)
        result = await session.execute(stmt)
        existing_user: UserModel | None = result.scalars().first()
        if existing_user is not None:
            return "Email address is in use"
        
        hashed_password: str = Hasher.hash_password(password)
        
        new_user: UserModel = UserModel(
            name=name, email=email, password=hashed_password)

        if interest_id:
            interest: Interest | None = await get_interest(session, interest_id)
            if interest is None: 
                return 'Interest id not found'
            new_user.interests.append(interest)

        session.add(new_user)
        # Generates ID for new user 
        await session.flush()

        # Add initial balance
        add_balance: BalanceModel = BalanceModel(
            user_id=new_user.id, total_balance=balance, interest_accrued_today=0.000, 
            cumulative_interest_accrued=0.000
        )
        
        session.add(add_balance)
        await session.commit()
        
        return "User added successfully"
    
    except SQLAlchemyError as error:
        await session.rollback()
        return f"Error occurred: {error}"

# Adds Interest object to user's list of interests
async def add_new_interest_to_user(session: AsyncSession, user_id: int, interest_id: int):
    stmt = select(UserModel).options(selectinload(UserModel.interests)).where(UserModel.id == user_id)
    result = await session.execute(stmt)
    existing_user: UserModel | None = result.scalars().first()
    if existing_user is None:
        return "User id not found: user does not exist"
    
    # Set the active column of all current interests for that user to False
    update_stmt: Update = (
        update(UserInterest)
        .where(UserInterest.user_id == user_id)
        .values(active=False)
    )
    await session.execute(update_stmt)

    # User interest default is set to True
    interest: Interest | None = await get_interest(session, interest_id)
    if interest is None: 
            return 'Interest id not found'
    existing_user.interests.append(interest)

    session.add(existing_user)
    await session.commit()

    return "Interest successfully added to user"

# Updates user data - not including interest
async def update_user_data(session: AsyncSession, user_id:int, user: UserInput): 
    stmt = select(UserModel).where(UserModel.id == user_id)
    result = await session.execute(stmt)
    existing_user: UserModel | None = result.scalars().first()
    if existing_user is None:
        return "User id not found: user does not exist"
    
    if user.email:
        existing_user.email = user.email
    
    if user.name:
        existing_user.name = user.name
    
    if user.password:
        hashed_password: str = Hasher.hash_password(user.password)
        existing_user.password = hashed_password
    
    session.add(existing_user)
    await session.commit()

    return "User details updated successfully"

# Deletes user and all corresponding records
async def delete_user(session: AsyncSession, user_id: int):
    stmt = select(UserModel).where(UserModel.id == user_id)
    result = await session.execute(stmt)
    existing_user: UserModel | None = result.scalars().first()
    if existing_user is None:
        return "User id not found: user does not exist"
    
    # delete record in UserInterest table 
    await session.execute(delete(UserInterest).where(UserInterest.user_id == user_id))

    # delete records from the Balances table
    await session.execute(delete(BalanceModel).where(BalanceModel.user_id == user_id))

    # delete user record
    delete_user: Delete = delete(UserModel).where(UserModel.id == user_id)
    await session.execute(delete_user)
    await session.commit()

    return "User deleted successfully"