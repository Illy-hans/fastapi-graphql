from sqlalchemy import select, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.user_model import User


async def get_all_users(session: AsyncSession):
    result = await session.execute(select(User))
    users = result.scalars().all()
    return users