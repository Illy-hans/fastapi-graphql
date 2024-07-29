from sqlalchemy import Result, Sequence, Tuple, insert
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.interest_model import Interest as InterestModel
from app.models.user_model import User as UserModel

async def get_all_users(session: AsyncSession):
    stmt = (select(UserModel).options(selectinload(UserModel.interests)))
    result: Result[Tuple[UserModel]] = await session.execute(stmt)
    users: Sequence[UserModel] = result.scalars().all()
    return users

async def get_user(session: AsyncSession, user_id: int):
    stmt = (
        select(UserModel)
        .options(selectinload(UserModel.interests))
        .where(UserModel.id == user_id)
    )
    result: Result[Tuple[UserModel]] = await session.execute(stmt)
    user: UserModel = result.scalars().first()
    return user

async def get_all_interests(session: AsyncSession):
    result: Result[Tuple[InterestModel]]= await session.execute(select(InterestModel))
    interests: Sequence[InterestModel] = result.scalars().all()
    return interests
