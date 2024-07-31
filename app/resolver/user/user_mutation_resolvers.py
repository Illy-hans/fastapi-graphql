from typing import Optional
from sqlalchemy import Delete, Update, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.user_interest import UserInterest
from app.models.user_model import User as UserModel
from app.schemas.types_schema import InterestInput, UserInput

# Adds new user 
async def add_user(session: AsyncSession, user: UserInput, interest: Optional[InterestInput]):
    
    stmt = select(UserModel).where(UserModel.email == user.email)
    result = await session.execute(stmt)
    existing_user: UserModel | None = result.scalars().first()
    if existing_user is not None:
        return "Email address is in use"
    
    new_user: UserModel = UserModel(
        name=user.name, email=user.email, password=user.password, balance=user.balance)

    if interest:
        new_user.interests.append(interest)

    session.add(new_user)
    await session.commit()
    
    return "User added successfully"

# Adds Interest object to user's list of interests
async def add_new_interest_to_user(session: AsyncSession, user_id: int, interest: InterestInput):
    stmt = select(UserModel).where(UserModel.id == user_id)
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
    existing_user.interests.append(interest)

    session.add(existing_user)
    await session.commit()

    return "Interest successfully added"

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
        existing_user.password = user.password
    
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

    # delete user record
    delete_user: Delete = delete(UserModel).where(UserModel.id == user_id)
    await session.execute(delete_user)
    await session.commit()

    return "User deleted successfully"