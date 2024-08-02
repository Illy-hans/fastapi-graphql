from sqlalchemy import Result, Sequence, Tuple
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.user_model import User as UserModel

async def get_all_users(session: AsyncSession):
    stmt = (select(UserModel)
            .options(selectinload(UserModel.balances), selectinload(UserModel.interests)))
    result: Result[Tuple[UserModel]] = await session.execute(stmt)
    users: Sequence[UserModel] = result.scalars().all()
    return users

async def get_user(session: AsyncSession, user_id: int):
    stmt = (
        select(UserModel)
        .options(selectinload(UserModel.balances), selectinload(UserModel.interests))
        .where(UserModel.id == user_id)
    )
    result: Result[Tuple[UserModel]] = await session.execute(stmt)
    user: UserModel = result.scalars().first()
    return user
