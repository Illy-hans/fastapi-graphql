from sqlalchemy import Result, Sequence, Tuple, insert
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.interest_model import Interest
from app.models.user_model import User as UserModel

async def get_all_users(session: AsyncSession):
    result: Result[Tuple] = await session.execute(select(UserModel))
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

