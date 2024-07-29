from typing import Optional
from sqlalchemy import Result, Sequence, Tuple, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.user_model import User as UserModel
from app.schemas.types_schema import InterestInput

# Adds new user 
async def add_user(session: AsyncSession, name: str, email: str, 
                password: str, balance: float, interest: Optional[InterestInput]):
    
    stmt = select(UserModel).where(UserModel.email == email)
    result = await session.execute(stmt)
    existing_user: UserModel | None = result.scalars().first()
    if existing_user is not None:
        return "Email address is in use"
    
    new_user: UserModel = UserModel(
        name=name, email=email, password=password, balance=balance)

    # checks for presence before adding
    if interest:
        new_user.interests.append(interest)

    session.add(new_user)
    await session.commit()
    
    return "User added successfully"


async def add_new_interest(session: AsyncSession, user_id: int, interest: InterestInput):
    stmt = select(UserModel).where(UserModel.id == user_id)
    result = await session.execute(stmt)
    existing_user: UserModel | None = result.scalars().first()
    if existing_user is None:
        return "User id not found: user does not exist"
    
    existing_user.interests.append(interest)

    session.add(existing_user)
    await session.commit()

    return "Interest successfully added"

